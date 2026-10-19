"""Native optional-backend parity, normalization, training and safe artifacts."""
import importlib.util
import json
from pathlib import Path
import sys

import pytest
import torch
from torch.utils.data import DataLoader, TensorDataset

from vlmprobe.sae.backends import overcomplete as backend


def binding():
    return {"model_id": "toy@sha256:weights", "tokenizer_id": "sha256:tokenizer",
            "preprocessing_id": "identity-v1", "calibration_id": "separate-train-validation-v1",
            "site": "residual.0", "layer": 0,
            "hook": {"module": "blocks.0", "kind": "output", "selector": None, "tensor_slice": None}}


@pytest.fixture(autouse=True)
def optional_backend():
    if importlib.util.find_spec("overcomplete") is None:
        pytest.skip("optional overcomplete package is not installed")
    try:
        backend._upstream()
    except ImportError as error:
        pytest.skip(str(error))
    torch.set_num_threads(1)


def make(architecture="topk", **kwargs):
    torch.manual_seed(53)
    if architecture.startswith("archetypal_"):
        kwargs.setdefault("points", torch.randn(12, 4))
    if "topk" in architecture:
        kwargs.setdefault("top_k", 2)
    return backend.create(architecture, 4, 8, binding=binding(), **kwargs)


@pytest.mark.parametrize("architecture", list(backend.ARCHITECTURES))
def test_real_native_encode_decode_and_raw_space_roundtrip(tmp_path, architecture):
    model = make(architecture, input_mean=[1., 2., 3., 4.], input_scale=[2., 3., 4., 5.])
    values = torch.randn(2, 3, 4)
    normalized = (values - model.input_mean) / model.input_scale
    model.sae(normalized.reshape(-1, 4))  # Initializes native BatchTopK threshold.
    model.is_fitted = True
    model.eval()
    _, expected = model.sae.encode(normalized.reshape(-1, 4))
    actual = model.encode(values)
    assert torch.equal(actual, expected.reshape(2, 3, 8))
    expected_reconstruction = model.sae.decode(expected).reshape(2, 3, 4) * model.input_scale + model.input_mean
    assert torch.equal(model.decode(actual), expected_reconstruction)
    artifact = tmp_path / "safe.pt"
    model.save(artifact)
    loaded = backend.load(artifact, binding=binding())
    assert torch.equal(loaded.encode(values), actual)
    assert torch.equal(loaded.decode(actual), expected_reconstruction)
    assert torch.load(artifact, weights_only=True)["schema"] == backend.SCHEMA
    if architecture == "batchtopk":
        assert torch.equal(loaded.sae.running_threshold, model.sae.running_threshold)
    wrong = {**binding(), "model_id": "another-model"}
    with pytest.raises(ValueError, match="binding"):
        backend.load(artifact, binding=wrong)


def test_batchtopk_missing_trained_threshold_is_not_silently_guessed():
    _, classes = backend._upstream()
    native = classes.BatchTopKSAE(4, 8, top_k=3)
    with pytest.raises(ValueError, match="running_threshold"):
        backend.wrap(native, binding=binding(), is_fitted=True)


def test_vision_attention_encoder_is_not_flattened_as_pointwise_tokens():
    _, classes = backend._upstream()
    native = classes.SAE((3, 8), 8, encoder_module="attention_1b")
    with pytest.raises(ValueError, match="geometry"):
        backend.wrap(native, binding=binding())


def test_device_dtype_move_preserves_native_nonbuffer_thresholds_and_fused_dictionary():
    model = make("batchtopk")
    model.sae(torch.randn(4, 4))
    model.is_fitted = True
    model.eval()
    values = torch.randn(3, 4)
    baseline = model(values)[0]
    model.to(dtype=torch.float64)
    assert model.sae.running_threshold.dtype == torch.float64
    assert model.sae.dictionary._fused_dictionary.dtype == torch.float64
    assert torch.allclose(model(values.double())[0], baseline.double(), atol=1e-6)
    jump = make("jumprelu").to(dtype=torch.float64)
    assert jump.sae.bandwidth.dtype == torch.float64


def data():
    generator = torch.Generator().manual_seed(41)
    train = torch.rand(64, 4, generator=generator) * 2
    validation = torch.rand(24, 4, generator=generator) * 2
    return (DataLoader(train, batch_size=16, shuffle=True, generator=torch.Generator().manual_seed(17)),
            DataLoader(validation, batch_size=8))


def test_real_upstream_training_improves_heldout_and_preserves_optimizer_resume(tmp_path):
    continuous = make("relu")
    train_data, validation = data()
    report = backend.train(model=continuous, train_data=train_data, validation_data=validation,
        output_dir=tmp_path / "continuous", binding=binding(), nb_epochs=4,
        lr=.02, patience=8, seed=17, provenance={"corpus": "toy-v1"})
    assert report["training_implementation"].startswith("overcomplete.sae.train.train_sae")
    history = json.loads((tmp_path / "continuous/history.json").read_text())
    assert history[-1]["validation"]["objective"] < history[0]["validation"]["objective"]
    interrupted = make("relu")
    train_data, validation = data()
    backend.train(model=interrupted, train_data=train_data, validation_data=validation,
        output_dir=tmp_path / "resumed", binding=binding(), nb_epochs=2,
        lr=.02, patience=8, seed=17, provenance={"corpus": "toy-v1"})
    resumed = make("relu")
    train_data, validation = data()
    backend.train(model=resumed, train_data=train_data, validation_data=validation,
        output_dir=tmp_path / "resumed", binding=binding(), nb_epochs=4,
        lr=.02, patience=8, seed=17, provenance={"corpus": "toy-v1"})
    for key, value in continuous.state_dict().items():
        assert torch.equal(value, resumed.state_dict()[key]), key
    with pytest.raises(ValueError, match="provenance"):
        backend.train(model=make("relu"), train_data=train_data, validation_data=validation,
            output_dir=tmp_path / "resumed", binding=binding(), nb_epochs=5,
            lr=.02, patience=8, seed=17, provenance={"corpus": "DIFFERENT"})


def test_training_cannot_learn_from_validation_or_one_shot_iterators(tmp_path):
    model = make()
    values = torch.randn(4, 4)
    with pytest.raises(ValueError, match="independent"):
        backend.train(model=model, train_data=values, validation_data=values,
                      output_dir=tmp_path, binding=binding(), nb_epochs=1)
    with pytest.raises(ValueError, match="re-iterable"):
        backend.train(model=model, train_data=iter([values]), validation_data=[values + 1],
                      output_dir=tmp_path, binding=binding(), nb_epochs=1)
    with pytest.raises(ValueError, match="at least one"):
        backend.create("archetypal_topk", 4, 8, binding=binding(),
                       points=torch.empty(0, 4), top_k=2)


def test_raw_tensor_resume_rejects_changed_content_without_manual_provenance(tmp_path):
    generator = torch.Generator().manual_seed(71)
    train = torch.randn(16, 4, generator=generator)
    validation = torch.randn(8, 4, generator=generator)
    backend.train(model=make("relu"), train_data=train, validation_data=validation,
        output_dir=tmp_path, binding=binding(), nb_epochs=1, patience=3)
    changed = train.clone()
    changed[0, 0] += .125
    with pytest.raises(ValueError, match="resume protocol"):
        backend.train(model=make("relu"), train_data=changed, validation_data=validation,
            output_dir=tmp_path, binding=binding(), nb_epochs=2, patience=3)
    with pytest.raises(ValueError, match="resume protocol"):
        backend.train(model=make("relu"), train_data=train, validation_data=validation + .25,
            output_dir=tmp_path, binding=binding(), nb_epochs=2, patience=3)


def test_cloned_identical_split_is_rejected_and_fingerprinting_does_not_iterate_loader(tmp_path):
    values = torch.randn(16, 4)
    with pytest.raises(ValueError, match="identical activation tensors"):
        backend.train(model=make("relu"), train_data=values, validation_data=values.clone(),
            output_dir=tmp_path, binding=binding(), nb_epochs=1)

    class NoIterationLoader(DataLoader):
        def __iter__(self):
            raise AssertionError("fingerprinting must not construct a loader iterator")

    generator = torch.Generator().manual_seed(111)
    loader = NoIterationLoader(TensorDataset(values, torch.arange(len(values))),
                              batch_size=4, shuffle=True, generator=generator)
    before = generator.get_state().clone()
    fingerprint = backend._data_fingerprint(loader)
    assert torch.equal(generator.get_state(), before)
    assert fingerprint["automatic"] and len(fingerprint["tensors"]) == 2
    assert fingerprint["tensors"][0] == backend._data_fingerprint(values)["tensors"][0]
    with pytest.raises(ValueError, match="identical activation tensors"):
        backend.train(model=make("relu"), train_data=loader,
            validation_data=NoIterationLoader(TensorDataset(values.clone()), batch_size=4),
            output_dir=tmp_path, binding=binding(), nb_epochs=1)


def test_no_fabricated_pretrained_registry_or_misclassified_nmf():
    assert backend.list_pretrained() == []
    assert "NMF/PCA/ICA are not SAEs" in backend.backend_info()["scope"]
    with pytest.raises(ValueError, match="architecture"):
        backend.create("nmf", 4, 8, binding=binding())


def test_real_model_bound_features_and_error_preserving_intervention(tmp_path):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "examples"))
    from tiny_model import TinyModel
    from vlmprobe import Prober, TokenMargin
    from vlmprobe.sae.binding import build_sae_binding
    torch.manual_seed(89)
    probe = Prober(TinyModel())
    inputs = {"input_ids": torch.tensor([[1, 2, 3], [4, 5, 6]]),
              "image_tokens": torch.randn(2, 2, 6)}
    actual_binding = build_sae_binding(probe, 0, model_id="tiny-seed89-v1",
        tokenizer_id="integer-ids-v1", preprocessing_id="two-image-three-text-v1",
        calibration_id="independent-synthetic-vectors-v1")
    model = backend.create("topk", 6, 12, top_k=3, binding=actual_binding)
    backend.train(model=model, train_data=[torch.randn(32, 6)],
        validation_data=[torch.randn(16, 6)], output_dir=tmp_path,
        binding=actual_binding, nb_epochs=2, patience=3)
    result = probe.sae.features(layer=0, sae=model, binding=actual_binding).run(inputs)
    hidden = probe.adapter.run(inputs, capture=["residual.0"]).activations["residual.0"]
    torch.testing.assert_close(result.tensors["features"], model.encode(hidden.reshape(-1, 6)))
    edited = probe.sae.edit(layer=0, sae=model, binding=actual_binding,
        feature_ids=[0], scale=1.).run(inputs, metric=TokenMargin(4, 5))
    assert torch.equal(edited.tensors["baseline_logits"], edited.tensors["edited_logits"])
    assert torch.equal(edited.tensors["score_change"], torch.zeros(2))
