"""Train-only statistics, exact resume and source-group isolation contracts."""
import copy
import importlib.util
from pathlib import Path

import pytest
import torch
from torch.utils.data import DataLoader

from vlmprobe.sae import SAEConfig, SparseAutoencoder
from vlmprobe.sae.training import evaluate_sae, fit_normalization, train_sae


def binding():
    return {"model_id": "toy@sha256:weights", "tokenizer_id": "sha256:tokenizer",
        "preprocessing_id": "identity-v1", "calibration_id": "train-independent-v1",
        "site": "residual.0", "layer": 0,
        "hook": {"module": "blocks.0", "kind": "output", "selector": None, "tensor_slice": None}}


def data_loaders():
    generator = torch.Generator().manual_seed(91)
    basis = torch.randn(2, 4, generator=generator)
    train = torch.randn(64, 2, generator=generator) @ basis + 2.
    validation = torch.randn(24, 2, generator=generator) @ basis + 2.
    return train, validation, DataLoader(train, batch_size=16, shuffle=True,
        generator=torch.Generator().manual_seed(17)), DataLoader(validation, batch_size=9)


def model(architecture="relu"):
    return SparseAutoencoder(SAEConfig(architecture, 4, 12, k=3, l1_coefficient=.01, seed=3), binding())


def test_fit_normalization_uses_all_train_positions_without_batch_weighting():
    values = torch.tensor([[1., 2.], [2., 3.], [3., 4.], [20., 30.]])
    stats = fit_normalization(DataLoader(values, batch_size=3), 2)
    assert stats["positions"] == 4
    assert torch.allclose(stats["mean"], values.mean(0))
    assert stats["input_rms"] == pytest.approx(float(values.double().square().mean().sqrt()))


@pytest.mark.parametrize("architecture", ["relu", "topk", "gated"])
def test_training_statistics_do_not_include_validation_and_test_is_not_required(tmp_path, architecture):
    train, validation, train_batches, _ = data_loaders()
    sae = model(architecture)
    shifted_validation = DataLoader(validation + 100., batch_size=9)
    history = train_sae(sae, train_batches, shifted_validation, tmp_path, epochs=2,
                        lr=.005, patience=4, seed=17, provenance={"data": "fixed"})
    assert history["normalization"]["fit_split"] == "train"
    assert torch.allclose(torch.tensor(history["normalization"]["mean"]), train.mean(0))
    assert history["normalization"]["input_rms"] == pytest.approx(float(train.double().square().mean().sqrt()))
    assert history["status"] == "complete"
    assert sae.is_fitted
    restored = SparseAutoencoder.load(tmp_path / "best.pt", expected_binding=binding())
    assert torch.equal(restored.input_scale, sae.input_scale)
    assert torch.allclose(restored(train[:3])[0], sae(train[:3])[0])


def test_resume_matches_uninterrupted_optimizer_and_loader_order(tmp_path):
    _, _, train, validation = data_loaders()
    continuous = model()
    train_sae(continuous, train, validation, tmp_path / "continuous", epochs=4, lr=.005,
              patience=6, seed=17, provenance={"content": "identical"})
    _, _, train, validation = data_loaders()
    interrupted = model()
    train_sae(interrupted, train, validation, tmp_path / "resumed", epochs=2, lr=.005,
              patience=6, seed=17, provenance={"content": "identical"})
    _, _, train, validation = data_loaders()
    resumed = model()
    train_sae(resumed, train, validation, tmp_path / "resumed", epochs=4, lr=.005,
              patience=6, seed=17, provenance={"content": "identical"})
    for name, value in continuous.state_dict().items():
        assert torch.equal(value, resumed.state_dict()[name]), name
    _, _, train, validation = data_loaders()
    with pytest.raises(ValueError, match="provenance"):
        train_sae(model(), train, validation, tmp_path / "resumed", epochs=5, lr=.005,
                  patience=6, seed=17, provenance={"content": "CHANGED"})


def test_metric_weighting_and_dead_feature_definition():
    sae = model()
    with torch.no_grad():
        for parameter in sae.parameters():
            parameter.zero_()
    values = torch.tensor([[1.] * 4, [1.] * 4, [1.] * 4, [5.] * 4])
    metrics = evaluate_sae(sae, DataLoader(values, batch_size=3), reference_mean=torch.zeros(4))
    assert metrics["positions"] == 4
    assert metrics["mse"] == pytest.approx(7.)
    assert metrics["fvu"] == pytest.approx(1.)
    assert metrics["l0"] == 0.
    assert metrics["dead_feature_fraction"] == 1.
    assert metrics["fvu_reference"] == "training_mean"


def test_portable_bundle_rejects_group_overlap_and_misaligned_group_counts():
    path = Path(__file__).resolve().parents[1] / "examples/train_sae.py"
    specification = importlib.util.spec_from_file_location("sae_training_example", path)
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    bundle = {"binding": binding(), "train": torch.randn(4, 4), "validation": torch.randn(2, 4),
              "test": torch.randn(2, 4), "groups": {
                  "train": ["train-slide"] * 4, "validation": ["val-slide"] * 2, "test": ["test-slide"] * 2}}
    _, summary = module.validate_bundle(bundle)
    assert summary["train"] == {"positions": 4, "source_groups": 1}
    changed = copy.deepcopy(bundle)
    changed["groups"]["validation"] = ["train-slide"] * 2
    with pytest.raises(ValueError, match="group overlap"):
        module.validate_bundle(changed)
    changed = copy.deepcopy(bundle)
    changed["groups"]["test"] = ["test-slide"]
    with pytest.raises(ValueError, match="per activation row"):
        module.validate_bundle(changed)


def test_cache_manifest_groups_rejected_before_model_loading():
    path = Path(__file__).resolve().parents[1] / "examples/cache_sae_activations.py"
    specification = importlib.util.spec_from_file_location("sae_cache_example", path)
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    rows = [{"id": name, "split": name, "group": f"group-{name}", "text": "input"}
            for name in ("train", "validation", "test")]
    module.validate_records(rows)
    rows[1]["group"] = rows[0]["group"]
    with pytest.raises(ValueError, match="group overlap"):
        module.validate_records(rows)
