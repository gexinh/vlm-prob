"""Provider discovery and shared SAE contracts, without optional dependencies."""
import gzip
import json
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace
from unittest.mock import Mock

import pytest
import torch
from torch import nn

from vlmprobe import (ClassScore, HookPoint, ModelSpec, Prober,
                      TokenLayout, TorchModelAdapter)
from vlmprobe.sae import providers
from vlmprobe.sae.binding import build_sae_binding


def test_provider_discovery_is_lazy_in_fresh_process():
    source = """
import json, sys
from vlmprobe.sae import list_backends
rows = list_backends()
print(json.dumps({'names': sorted(r['backend'] for r in rows),
 'imports': [n for n in ('sae_lens', 'vit_prisma', 'overcomplete') if n in sys.modules]}))
"""
    result = subprocess.run([sys.executable, "-c", source], check=True,
                            capture_output=True, text=True)
    value = json.loads(result.stdout)
    assert value["names"] == ["overcomplete", "prisma", "saelens"]
    assert value["imports"] == []


def test_provider_dispatch_preserves_native_configuration(monkeypatch):
    module = SimpleNamespace(load=Mock(return_value="loaded"), wrap=Mock(return_value="wrapped"),
                             train=Mock(return_value={"state": "complete"}))
    selector = Mock(return_value=module)
    monkeypatch.setattr(providers, "_module", selector)
    binding = {"exact": "binding"}
    assert providers.load_sae("saelens", binding=binding, release="gemma", sae_id="x") == "loaded"
    module.load.assert_called_once_with(binding=binding, release="gemma", sae_id="x")
    native = object()
    assert providers.wrap_sae("prisma", native, binding=binding, normalization="none") == "wrapped"
    module.wrap.assert_called_once_with(native, binding=binding, normalization="none")
    result = providers.train_backend("overcomplete", model=native, nb_epochs=2, objective="mse")
    assert result["state"] == "complete"
    module.train.assert_called_once_with(model=native, nb_epochs=2, objective="mse")
    assert [call.args[0] for call in selector.call_args_list] == ["saelens", "prisma", "overcomplete"]


def test_snapshot_catalog_filters_without_fetching_weights(monkeypatch, tmp_path):
    directory = tmp_path / "resources"
    directory.mkdir()
    value = {"schema": "test", "sources": [{"commit": "immutable"}], "entries": [
        {"backend": "saelens", "model": "google/gemma-2-2b", "sae_id": "layer_1"},
        {"backend": "prisma", "model": "openai/clip-vit-large", "sae_id": "blocks.2"},
        {"backend": "saelens", "model": "gpt2-small", "sae_id": "layer_0"}]}
    (directory / "pretrained_catalog.json.gz").write_bytes(gzip.compress(json.dumps(value).encode()))
    monkeypatch.setattr(providers, "files", lambda _: tmp_path)
    assert len(providers.list_pretrained("sae-lens")) == 2
    assert providers.list_pretrained(model="CLIP", query="blocks")[0]["backend"] == "prisma"
    assert len(providers.list_pretrained(limit=1)) == 1
    assert providers.list_pretrained("overcomplete") == []
    assert providers.catalog_provenance() == {"schema": "test", "sources": [{"commit": "immutable"}]}
    with pytest.raises(ValueError, match="limit"):
        providers.list_pretrained(limit=0)
    with pytest.raises(ValueError, match="requires a backend"):
        providers.list_pretrained(source="installed")
    with pytest.raises(ValueError, match="unknown SAE backend"):
        providers.list_pretrained("imaginary")


def test_bundled_catalog_retains_upstream_resource_scope():
    resource = Path(providers.__file__).parent / "resources/pretrained_catalog.json.gz"
    if not resource.exists():
        pytest.skip("catalog snapshot is being built separately")
    rows = providers.list_pretrained()
    assert len([row for row in rows if row["backend"] == "saelens"]) >= 10000
    assert len([row for row in rows if row["backend"] == "prisma"]) >= 80
    assert providers.list_pretrained("overcomplete") == []
    assert "entries" not in providers.catalog_provenance()


class ContextSAE(nn.Module):
    """A deliberately stateful per-input centering contract with a biased decoder."""
    def __init__(self, binding, width=6):
        super().__init__()
        self.weight = nn.Parameter(torch.eye(width))
        self.config = SimpleNamespace(d_in=width, d_sae=width, architecture="test-contextual")
        self.binding, self.is_fitted = binding, True
        self.contexts, self.encodes = [], 0

    def encode(self, values):
        raise AssertionError("context-aware dictionaries must use encode_with_context")

    def decode(self, features):
        raise AssertionError("context-aware dictionaries must use decode_with_context")

    def encode_with_context(self, values):
        self.encodes += 1
        context = {"mean": values.mean(-1, keepdim=True), "serial": self.encodes}
        return values - context["mean"], context

    def decode_with_context(self, features, context):
        self.contexts.append(context)
        return features + context["mean"] + .25


def tiny():
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "examples"))
    from tiny_model import TinyModel
    torch.manual_seed(12)
    torch.set_num_threads(1)
    probe = Prober(TinyModel())
    values = {"input_ids": torch.tensor([[1, 2, 3], [4, 5, 6]]),
              "image_tokens": torch.randn(2, 2, 6)}
    binding = build_sae_binding(probe, 0, model_id="tiny-seed12-v1", tokenizer_id="integer-v1",
        preprocessing_id="native-v1", calibration_id="independent-v1")
    return probe, values, binding


def test_runtime_hook_is_verified_before_provider_download(monkeypatch):
    probe, _, binding = tiny()
    download = Mock(return_value="unexpected")
    monkeypatch.setattr(providers, "load_sae", download)
    wrong = {**binding, "hook": {**binding["hook"], "module": "different.module"}}
    with pytest.raises(ValueError, match="hook"):
        probe.sae.load("saelens", binding=wrong, release="anything", sae_id="anything")
    download.assert_not_called()
    assert probe.sae.load("saelens", binding=binding, release="actual", sae_id="id") == "unexpected"
    download.assert_called_once_with("saelens", binding=binding, release="actual", sae_id="id")


def test_profile_retains_signed_values_and_native_top_positions():
    probe, values, binding = tiny()
    sae = ContextSAE(binding)
    features = probe.sae.features(layer=0, sae=sae, binding=binding).run(values)
    result = probe.sae.profile(layer=0, sae=sae, binding=binding, top_k=3).run(values)
    z = features.tensors["features"]
    indices = z.abs().topk(3, dim=0).indices
    torch.testing.assert_close(result.tensors["mean_activation"], z.mean(0))
    torch.testing.assert_close(result.tensors["activation_variance"], z.var(0, unbiased=False))
    torch.testing.assert_close(result.tensors["firing_frequency"], (z != 0).float().mean(0))
    torch.testing.assert_close(result.tensors["top_activation_values"], z.gather(0, indices))
    assert torch.equal(result.tensors["top_positions"], features.tensors["positions"][indices])
    assert (result.tensors["top_activation_values"] < 0).any()


def test_context_is_reused_for_baseline_and_actual_feature_edit():
    probe, values, binding = tiny()
    sae = ContextSAE(binding)
    result = probe.sae.edit(layer=0, sae=sae, binding=binding,
                           feature_ids=[0], scale=0.).run(values)
    assert sae.encodes == 1
    assert len(sae.contexts) == 2 and sae.contexts[0] is sae.contexts[1]
    hidden = probe.adapter.run(values, capture=["residual.0"]).activations["residual.0"]
    mean = hidden.mean(-1, keepdim=True)
    replacement = hidden.clone()
    replacement[..., 0] = mean[..., 0]
    expected = probe.adapter.run(values, interventions={"residual.0": lambda _: replacement}).logits
    torch.testing.assert_close(result.tensors["edited_logits"], expected)
    assert result.metadata["normalization_context_preserved"]


def test_reconstruction_is_an_actual_control_and_half_context_protocol_rejects():
    probe, values, binding = tiny()
    sae = ContextSAE(binding)
    result = probe.sae.reconstruct(layer=0, sae=sae, binding=binding).run(values)
    assert result.metadata["mode"] == "reconstruction"
    assert not torch.equal(result.tensors["baseline_logits"], result.tensors["edited_logits"])
    sae.decode_with_context = None
    with pytest.raises(ValueError, match="both"):
        probe.sae.features(layer=0, sae=sae, binding=binding).run(values)


class VectorEncoder(nn.Module):
    def __init__(self):
        super().__init__()
        self.block = nn.Linear(4, 4, bias=False)

    def forward(self, inputs):
        return self.block(inputs).mean(1)


def test_representation_outputs_are_not_fabricated_logits():
    torch.manual_seed(21)
    model = VectorEncoder()
    spec = ModelSpec({0: "residual.0"}, output_kind="representation",
        layout=lambda inputs: TokenLayout(torch.ones(inputs["inputs"].shape[:2], dtype=torch.bool)))
    adapter = TorchModelAdapter(model, {"residual.0": HookPoint("block")}, model_id="vector-v1", spec=spec)
    probe = Prober(model, adapter=adapter)
    inputs = {"inputs": torch.randn(2, 3, 4)}
    trace = adapter.run(inputs)
    with pytest.raises(TypeError, match="representation"):
        _ = trace.logits
    binding = build_sae_binding(probe, 0, model_id="vector-seed21-v1", tokenizer_id="none-v1",
                               preprocessing_id="identity-v1", calibration_id="independent-v1")
    sae = ContextSAE(binding, width=4)
    result = probe.sae.edit(layer=0, sae=sae, binding=binding, feature_ids=[0], scale=0.).run(
        inputs, metric=lambda output: output.square().sum(-1))
    assert {"baseline_output", "edited_output", "score_change"} <= result.tensors.keys()
    assert "baseline_logits" not in result.tensors
    assert result.tensors["baseline_output"].shape == (2, 4)
    with pytest.raises(ValueError, match="vector metric"):
        probe.sae.edit(layer=0, sae=sae, binding=binding, feature_ids=[0]).run(inputs, metric=ClassScore(0))
    advertised = probe.describe()["methods"]
    assert all(name.startswith("sae.") for name, info in advertised.items() if info["available"])
    assert all(advertised[name]["available"] for name in ("sae.features", "sae.edit", "sae.profile", "sae.reconstruct"))
