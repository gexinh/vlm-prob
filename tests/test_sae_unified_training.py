"""One trainer for the native method union, including precise resume budgets."""
from copy import deepcopy
import json
from types import SimpleNamespace

import pytest
import torch
from torch import nn
from torch.utils.data import DataLoader, RandomSampler

from vlmprobe.sae import SAEConfig, SparseAutoencoder
from vlmprobe.sae.models import ARCHITECTURES
from vlmprobe.sae.training import SAETrainingConfig, evaluate_sae, fit_sae


def binding():
    return {"model_id": "tiny@fixed", "tokenizer_id": "none@vectors", "preprocessing_id": "raw-v1",
            "calibration_id": "independent-sources-v1", "site": "residual.0", "layer": 0,
            "hook": {"module": "layers.0", "kind": "output", "selector": None, "tensor_slice": None}}


def data():
    generator = torch.Generator().manual_seed(71)
    return torch.randn(64, 4, generator=generator), torch.randn(19, 4, generator=generator) + .2


def model(architecture="relu", **kwargs):
    return SparseAutoencoder(SAEConfig(architecture, 4, 12, k=3, seed=9,
        archetypal_candidates=16, **kwargs), binding())


@pytest.mark.parametrize("architecture", ARCHITECTURES)
def test_every_native_method_uses_identical_engine_and_portable_artifact(tmp_path, architecture):
    train, validation = data()
    method = model(architecture)
    history = fit_sae(method, train, validation, tmp_path,
        training=SAETrainingConfig(max_steps=2, batch_size=16, seed=17))
    assert history["completed_steps"] == 2
    assert history["training_vectors"] == 32
    assert history["normalization"]["fit_split"] == "train"
    json.dumps(history, allow_nan=False)
    restored = SparseAutoencoder.load(history["checkpoint"], expected_binding=binding())
    restored.eval()
    torch.testing.assert_close(restored(train[:4])[0], method(train[:4])[0])
    assert all(parameter.grad is None or torch.isfinite(parameter.grad).all() for parameter in method.parameters())


@pytest.mark.parametrize("unit,first,total", [("max_steps", 3, 6), ("max_vectors", 19, 53)])
def test_mid_epoch_resume_matches_uninterrupted_including_partial_vector_batches(tmp_path, unit, first, total):
    train, validation = data()
    full, resumed = model("topk"), model("topk")
    common = dict(batch_size=16, seed=17, patience=20, progress_every=1)
    complete = fit_sae(full, train, validation, tmp_path / "complete", training=SAETrainingConfig(**{unit: total}, **common))
    fit_sae(model("topk"), train, validation, tmp_path / "resumed", training=SAETrainingConfig(**{unit: first}, **common))
    # Opening a completed short run must retain its replay boundary for a later
    # extension; otherwise an intervening no-op resume changes the trajectory.
    fit_sae(model("topk"), train, validation, tmp_path / "resumed", training=SAETrainingConfig(**{unit: first}, **common))
    continued = fit_sae(resumed, train, validation, tmp_path / "resumed", training=SAETrainingConfig(**{unit: total}, **common))
    for name, value in full.state_dict().items():
        assert torch.equal(value, resumed.state_dict()[name]), name
    one = torch.load(complete["training_state"], weights_only=True)
    two = torch.load(continued["training_state"], weights_only=True)
    assert one["steps"] == two["steps"]
    assert one["vectors"] == two["vectors"]
    assert one["cursor"] == two["cursor"]
    for name, value in one["model"].items():
        assert torch.equal(value, two["model"][name]), name
    assert continued["training_vectors"] == (total if unit == "max_vectors" else total * 16)
    if unit == "max_vectors":
        assert continued["resume_rolled_back_partial_vectors"] == 3


def test_strict_resume_rejects_changed_content_objective_and_optimizer(tmp_path):
    train, validation = data()
    common = dict(max_steps=2, batch_size=16, seed=17)
    fit_sae(model(), train, validation, tmp_path, training=SAETrainingConfig(**common))
    for changed_model, changed_train, changed_config in [
        (model(), train + .01, SAETrainingConfig(**common)),
        (model(l1_coefficient=.02), train, SAETrainingConfig(**common)),
        (model(), train, SAETrainingConfig(**common, lr=.002)),
    ]:
        with pytest.raises(ValueError, match="configuration|fingerprints|provenance"):
            fit_sae(changed_model, changed_train, validation, tmp_path, training=changed_config)

    state_path = tmp_path / "training_state.pt"
    state = torch.load(state_path, weights_only=True)
    state["optimizer"]["param_groups"][0]["lr"] = .9
    torch.save(state, state_path)
    with pytest.raises(ValueError, match="optimizer state"):
        fit_sae(model(), train, validation, tmp_path, training=SAETrainingConfig(**common))


@pytest.mark.parametrize("custom_collate", [False, True])
def test_rng_and_caller_loader_state_are_preserved(tmp_path, custom_collate):
    train, validation = data()

    def collate(rows):
        torch.rand(())  # A fallback collator can consume the global Torch RNG.
        return {"activations": torch.stack(rows)}

    sampler = RandomSampler(train, generator=torch.Generator().manual_seed(71))
    options = {"collate_fn": collate} if custom_collate else {}
    loader = DataLoader(train, batch_size=16, sampler=sampler,
                        generator=torch.Generator().manual_seed(83), **options)
    method = model()
    before, loader_before = torch.get_rng_state().clone(), loader.generator.get_state().clone()
    sampler_before = sampler.generator.get_state().clone()
    fit_sae(method, loader, validation, tmp_path, training=SAETrainingConfig(max_steps=2, batch_size=16))
    assert torch.equal(before, torch.get_rng_state())
    assert torch.equal(loader_before, loader.generator.get_state())
    assert torch.equal(sampler_before, sampler.generator.get_state())


def test_cache_source_independence_is_checked_before_training(tmp_path):
    all_values, validation = data()
    with pytest.raises(ValueError, match="overlap"):
        fit_sae(model(), all_values[:40], all_values[30:], tmp_path / "overlap")
    with pytest.raises(ValueError, match="identical"):
        fit_sae(model(), all_values, all_values.clone(), tmp_path / "clone")
    with pytest.raises(ValueError, match="overlapping"):
        fit_sae(model(), all_values, validation, tmp_path / "groups", provenance={
            "groups": {"train": ["source1"], "validation": ["source1"]}})
    history = fit_sae(model(), all_values[:40], all_values[40:], tmp_path / "disjoint",
        training=SAETrainingConfig(max_steps=1, batch_size=16))
    assert history["completed_steps"] == 1


class SignedDictionary(nn.Module):
    def __init__(self, mutate=False):
        super().__init__()
        self.weight = nn.Parameter(torch.zeros(()))
        self.config = SimpleNamespace(d_in=2, d_sae=2)
        self.register_buffer("updates", torch.zeros((), dtype=torch.long))
        self.mutate = mutate

    def forward(self, raw):
        return raw + self.weight, -torch.ones_like(raw)

    def loss(self, raw):
        if self.mutate:
            self.updates.add_(1)
        zero = self.weight * 0
        return {key: zero for key in ("loss", "reconstruction", "sparsity", "auxiliary")}


def test_signed_nonzero_activity_and_validation_stat_safety():
    raw = torch.ones(4, 2)
    metrics = evaluate_sae(SignedDictionary(), [raw], reference_mean=torch.zeros(2))
    assert metrics["l0"] == 2
    assert metrics["dead_feature_fraction"] == 0
    bad = SignedDictionary(mutate=True)
    with pytest.raises(RuntimeError, match="mutated training statistics"):
        evaluate_sae(bad, [raw])
    assert bad.updates == 0


def test_validation_never_updates_batch_threshold_or_dead_feature_counters(tmp_path):
    train, validation = data()
    method = model("batchtopk", auxk_coefficient=.01)
    fit_sae(method, train, validation, tmp_path,
        training=SAETrainingConfig(max_steps=2, batch_size=16))
    buffers = {key: value.clone() for key, value in method.named_buffers()}
    evaluate_sae(method, [validation])
    assert all(torch.equal(value, buffers[key]) for key, value in method.named_buffers())


@pytest.mark.parametrize("normalizer", ["none", "layer_norm", "constant_norm"])
def test_method_normalization_does_not_receive_an_extra_global_rms_scale(tmp_path, normalizer):
    train, validation = data()
    train, validation = train * 10, validation * 10
    history = fit_sae(model("topk", input_normalization=normalizer), train, validation, tmp_path,
        training=SAETrainingConfig(max_steps=1, batch_size=16, normalization="rms"))
    assert history["normalization"]["scale"] == 1
    assert history["normalization"]["method"] == normalizer


@pytest.mark.parametrize("architecture", ["jumprelu", "archetypal_jumprelu"])
def test_mixed_precision_jump_training_and_evaluation_use_activation_dtype(tmp_path, architecture):
    train, validation = data()
    method = model(architecture).to(dtype=torch.bfloat16)
    assert next(method.parameters()).dtype == torch.float32  # Learned jump threshold.
    assert method.activation_parameter.dtype == torch.bfloat16
    received = []
    original_loss = method.loss

    def recorded_loss(raw):
        received.append(raw.dtype)
        return original_loss(raw)

    method.loss = recorded_loss
    history = fit_sae(method, train, validation, tmp_path,
        training=SAETrainingConfig(max_steps=2, batch_size=16))
    assert received and set(received) == {torch.bfloat16}
    assert history["configuration"]["model_dtype"] == "torch.bfloat16"
    assert method.threshold.dtype == torch.float32
    assert torch.isfinite(method.threshold).all()
    assert history["validation"]["positions"] == len(validation)
    restored = SparseAutoencoder.load(history["checkpoint"], expected_binding=binding())
    assert restored.activation_parameter.dtype == torch.bfloat16
    assert restored.threshold.dtype == torch.float32
    received.clear()
    evaluate_sae(method, [validation])
    assert received == [torch.bfloat16]
    torch.testing.assert_close(restored(train[:4])[0], method(train[:4])[0])


@pytest.mark.parametrize("kwargs", [dict(lr=float("inf")), dict(batch_size=0), dict(seed=-1),
    dict(max_steps=2, max_vectors=3), dict(normalization="mystery"), dict(max_vectors=0)])
def test_training_configuration_rejects_invalid_options(kwargs):
    with pytest.raises(ValueError):
        SAETrainingConfig(**kwargs)
