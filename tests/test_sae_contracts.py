"""Shared sparse feature contracts, independent of checkpoint source."""
from pathlib import Path
import sys
from types import SimpleNamespace
import pytest
import torch
from torch import nn
from vlmprobe import ClassScore, HookPoint, ModelSpec, Prober, TokenLayout, TorchModelAdapter
from vlmprobe.sae.binding import build_sae_binding


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
