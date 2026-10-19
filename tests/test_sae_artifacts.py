"""Native artifacts preserve methods, coordinates, feature order and buffers."""
from dataclasses import asdict
import json

import pytest
import torch

from vlm_probing.sae.artifacts import LEGACY_SCHEMA, SCHEMA, load_artifact, save_artifact
from vlm_probing.sae.models import ARCHITECTURES, SAEConfig, SparseAutoencoder


def binding():
    return {"model_id": "frozen-model@revision", "tokenizer_id": "native-tokenizer@revision",
        "preprocessing_id": "image-or-text-transform@v1", "calibration_id": "source-disjoint-splits@v1",
        "site": "residual.0", "layer": 0, "modality": "activation",
        "hook": {"module": "blocks.0", "kind": "output", "selector": None, "tensor_slice": None}}


@pytest.mark.parametrize("method", ARCHITECTURES)
@pytest.mark.parametrize("directory", [False, True])
def test_every_native_method_round_trips(method, directory, tmp_path):
    model = SparseAutoencoder(SAEConfig(method, 4, 8, k=2, archetypal_candidates=4,
        pursuit_iterations=2, omp_nnls_iterations=3), binding())
    if model.config.dictionary == "archetypal":
        model.initialize_dictionary_(torch.randn(12, 4))
    model.batch_threshold.fill_(.2)
    model.batch_threshold_initialized.fill_(True)
    model.training_steps.fill_(17)
    model.inactive_steps.copy_(torch.arange(8))
    model.input_scale.fill_(1.4)
    model.is_fitted = True
    model.eval()
    inputs = torch.randn(3, 4)
    expected = model(inputs)
    path = tmp_path / ("artifact" if directory else "best.pt")
    save_artifact(model, path)
    restored = load_artifact(path, expected_binding=binding())
    actual = restored(inputs)
    assert restored.config == model.config
    assert restored.is_fitted
    assert all(torch.equal(value, restored.state_dict()[key]) for key, value in model.state_dict().items())
    # Least-squares pursuit may choose numerically different LAPACK paths on
    # repeated identical calls; every saved tensor is checked exactly above.
    for before, after in zip(expected, actual):
        torch.testing.assert_close(before, after, rtol=1e-5, atol=2e-6)
    if directory:
        assert {"config.json", "weights.pt", "model_card.json"} <= {p.name for p in path.iterdir()}
        assert json.loads((path / "config.json").read_text())["schema"] == SCHEMA
    else:
        assert torch.load(path, weights_only=True)["schema"] == SCHEMA


@pytest.mark.parametrize("method", ["relu", "topk", "gated"])
def test_explicit_legacy_v1_upgrade_preserves_numerics(method, tmp_path):
    model = SparseAutoencoder(SAEConfig(method, 4, 8, k=2), binding())
    model.input_scale.fill_(2.)
    old_config = {key: value for key, value in asdict(model.config).items()
                  if key in {"architecture", "d_in", "d_sae", "k", "l1_coefficient", "seed"}}
    state = {key: value for key, value in model.state_dict().items()
             if key not in {"training_steps", "inactive_steps", "batch_threshold", "batch_threshold_initialized"}}
    path = tmp_path / "old.pt"
    torch.save({"schema": LEGACY_SCHEMA, "config": old_config, "binding": binding(),
                "dtype": "float32", "state_dict": state, "is_fitted": True}, path)
    restored = load_artifact(path, expected_binding=binding())
    raw = torch.randn(3, 4)
    assert torch.equal(model.encode(raw), restored.encode(raw))
    assert restored.source_metadata["source_schema"] == LEGACY_SCHEMA
    assert restored.training_steps.item() == 0


def test_corruption_and_wrong_binding_are_rejected(tmp_path):
    model = SparseAutoencoder(SAEConfig("relu", 4, 8), binding())
    save_artifact(model, tmp_path / "directory")
    wrong = {**binding(), "preprocessing_id": "different-transform@v2"}
    with pytest.raises(ValueError, match="binding differs"):
        load_artifact(tmp_path / "directory", expected_binding=wrong)
    weights = tmp_path / "directory" / "weights.pt"
    state = torch.load(weights, weights_only=True)
    state["encoder.bias"] += 1
    torch.save(state, weights)
    with pytest.raises(ValueError, match="checksum"):
        load_artifact(tmp_path / "directory")
    path = tmp_path / "best.pt"
    save_artifact(model, path)
    envelope = torch.load(path, weights_only=True)
    envelope["state_dict"]["decoder.bias"] += 1
    torch.save(envelope, path)
    with pytest.raises(ValueError, match="checksum"):
        load_artifact(path)


def test_no_nonfinite_tensor_or_unsafe_metadata_saved(tmp_path):
    model = SparseAutoencoder(SAEConfig("relu", 4, 8), binding())
    with torch.no_grad():
        model.encoder.bias[0] = float("nan")
    with pytest.raises(ValueError, match="finite"):
        save_artifact(model, tmp_path / "invalid")


def test_local_card_registration_is_explicit(tmp_path):
    from vlm_probing.sae.cards import list_models, load_model
    model = SparseAutoencoder(SAEConfig("relu", 4, 8), binding())
    model.is_fitted = True
    artifact = tmp_path / "my-model"
    registry = tmp_path / "my-registry"
    save_artifact(model, artifact, registry_dir=registry)
    rows = list_models(registry_dir=registry, include_builtin=False)
    assert len(rows) == 1
    assert rows[0]["method"] == "relu"
    restored = load_model(rows[0]["id"], registry_dir=registry, binding=binding())
    assert isinstance(restored, SparseAutoencoder)
    declared = load_model(rows[0]["id"], registry_dir=registry)
    assert declared.binding == binding()


@pytest.mark.parametrize("normalization", ["layer_norm", "constant_norm"])
def test_contextual_normalization_survives_artifact_load(normalization, tmp_path):
    model = SparseAutoencoder(SAEConfig("relu", 4, 8, input_normalization=normalization,
                                       normalization_std_correction=1), binding())
    path = save_artifact(model, tmp_path / "model")
    restored = load_artifact(path)
    raw = torch.randn(3, 4) + 2
    before, context_before = model.encode_with_context(raw)
    after, context_after = restored.encode_with_context(raw)
    assert torch.equal(before, after)
    assert torch.equal(model.decode_with_context(before, context_before), restored.decode_with_context(after, context_after))


@pytest.mark.parametrize("directory", [False, True])
def test_bfloat16_jumprelu_preserves_activation_and_threshold_dtypes(directory, tmp_path):
    model = SparseAutoencoder(SAEConfig("jumprelu", 4, 8, k=2), binding(), dtype=torch.bfloat16)
    model.is_fitted = True
    assert model.encoder.weight.dtype == torch.bfloat16
    assert model.threshold.dtype == torch.float32
    raw = torch.randn(3, 4, dtype=torch.bfloat16)
    before = model(raw)
    path = save_artifact(model, tmp_path / ("mixed" if directory else "mixed.pt"))
    restored = load_artifact(path)
    assert restored.encoder.weight.dtype == torch.bfloat16
    assert restored.threshold.dtype == torch.float32
    for key, value in model.state_dict().items():
        assert restored.state_dict()[key].dtype == value.dtype
        assert torch.equal(restored.state_dict()[key], value)
    for expected, actual in zip(before, restored(raw)):
        assert torch.equal(expected, actual)
