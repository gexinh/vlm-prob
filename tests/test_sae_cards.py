"""Our model catalog is small, evidence-bounded and independent of providers."""
import json
from pathlib import Path
import sys

import pytest
import torch

from vlm_probing.sae.cards import get_model_card, list_models, load_model, render_model_card


def _model_bound_dictionary(*, fingerprinted=False, imported=False):
    """Use an actual hooked backbone, with no expensive SAE fit needed here."""
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "examples"))
    from tiny_model import TinyModel
    from vlmprobe import Prober
    from vlmprobe.sae import SAEConfig, SparseAutoencoder
    from vlmprobe.sae.binding import build_sae_binding
    from vlmprobe.sae.data import model_identity, processor_identity

    torch.manual_seed(19)
    backbone = TinyModel()
    probe = Prober(backbone)
    binding = build_sae_binding(probe, 0,
        model_id=model_identity(backbone) if fingerprinted else "declared-tiny-model-v1",
        tokenizer_id=processor_identity(probe.processor) if fingerprinted else "declared-integer-tokens-v1",
        preprocessing_id="visual-vectors-and-token-ids-v1", calibration_id="independent-training-v1")
    sae = SparseAutoencoder(SAEConfig("relu", 6, 12, k=3), binding=binding)
    sae.is_fitted = True
    if imported:
        sae.source_metadata = {"conversion": "direct_tensor_mapping_to_native_sae",
                               "source_format": "prisma"}
    inputs = {"input_ids": torch.tensor([[1, 2, 3]]), "image_tokens": torch.randn(1, 2, 6)}
    return probe, sae, binding, inputs


def test_release_registry_contains_no_unverified_pretrained_models():
    assert list_models() == []
    assert list_models(modality="vision") == []
    assert list_models(method="topk") == []
    for old_id in ("gpt2-layer8-relu-768-imported", "clip-b32-layer11-relu-49152-imported"):
        with pytest.raises(KeyError):
            get_model_card(old_id)


@pytest.mark.parametrize("status,verification", [
    ("local", {}),
    ("imported", {"end_to_end": "passed", "report": "verification.md"}),
    ("validated", {}),
    ("validated", {"end_to_end": "failed", "report": "verification.md"}),
    ("validated", {"end_to_end": "passed"}),
])
def test_release_registry_fails_closed_on_unverified_insertions(tmp_path, monkeypatch, status, verification):
    from vlm_probing.sae import cards

    resources = tmp_path / "resources"
    resources.mkdir()
    card = {"schema": cards.CARD_SCHEMA, "id": "not-release-ready", "title": "Unverified dictionary",
            "method": "relu", "status": status, "modality": "language", "evidence": {},
            "verification": verification}
    (resources / "native_model_cards.json").write_text(json.dumps({"models": [card]}))
    monkeypatch.setattr(cards, "files", lambda _: tmp_path)
    with pytest.raises(ValueError, match="passed end-to-end verification report"):
        cards.list_models()


def test_locally_trained_card_discovery_rendering_and_loading(tmp_path):
    from vlmprobe.sae import SAETrainingConfig

    probe, _, _, train = _model_bound_dictionary()
    validation = {"input_ids": torch.tensor([[4, 5, 6]]),
                  "image_tokens": train["image_tokens"] + 0.3}
    fitted = probe.sae.topk(layer=0, d_sae=12, k=3)
    fitted.fit([train], [validation], output_dir=tmp_path / "fit",
               train_ids=["train-image-A"], validation_ids=["validation-image-B"],
               preprocessing_id="prepared-tiny-inputs-v1",
               training=SAETrainingConfig(max_steps=2, batch_size=4))
    fitted.save(tmp_path / "final", registry_dir=tmp_path / "registry",
                model_card={"id": "trained-domain-topk-v1", "title": "My domain dictionary"})
    cards = list_models(registry_dir=tmp_path / "registry", method="topk", status="trained")
    assert len(cards) == 1
    card = get_model_card("trained-domain-topk-v1", registry_dir=tmp_path / "registry")
    assert card["evidence"]["backbone_compatibility"] == "exact_weight_fingerprint_and_native_hook"
    assert list_models() == []  # Explicit local registration never publishes a release.
    restored = probe.sae.load(card["id"], registry_dir=tmp_path / "registry")
    torch.testing.assert_close(restored.run(validation).tensors["features"],
                               fitted.run(validation).tensors["features"])
    md = render_model_card(card, tmp_path / "model.md")
    page = render_model_card(card, tmp_path / "model.html")
    assert "My domain dictionary" in md.read_text()
    assert "trained-domain-topk-v1" in page.read_text()
    assert "<!doctype html>" in page.read_text()
    assert list_models(registry_dir=tmp_path / "registry", method="relu") == []


@pytest.mark.parametrize("imported", [False, True])
def test_public_resave_does_not_upgrade_imported_or_declared_binding_evidence(tmp_path, imported):
    from vlmprobe.sae import save_artifact

    probe, sae, binding, inputs = _model_bound_dictionary(imported=imported)
    expected = "not_verified" if imported else "caller_declared_binding"
    save_artifact(sae, tmp_path / "source", model_card={"evidence": {
        "backbone_compatibility": expected, "numerical_parity": "synthetic_tensor_check",
        "semantic_quality": "not_evaluated"}})
    fitted = probe.sae.load(tmp_path / "source", binding=binding)
    original = fitted.run(inputs).tensors["features"]
    for generation in range(2):
        destination = tmp_path / f"resaved-{generation}"
        fitted.save(destination)
        card = json.loads((destination / "model_card.json").read_text())
        assert card["evidence"]["backbone_compatibility"] == expected
        assert card["evidence"]["numerical_parity"] == "synthetic_tensor_check"
        fitted = probe.sae.load(destination, binding=binding)
        torch.testing.assert_close(fitted.run(inputs).tensors["features"], original)


def test_public_local_card_load_uses_saved_fingerprints_without_explicit_binding(tmp_path):
    from vlmprobe.sae import save_artifact

    probe, sae, _, inputs = _model_bound_dictionary(fingerprinted=True)
    save_artifact(sae, tmp_path / "artifact", registry_dir=tmp_path / "registry",
                  model_card={"id": "my-native-dictionary-v1"})
    direct = probe.sae.load(tmp_path / "artifact")
    restored = probe.sae.load("my-native-dictionary-v1", registry_dir=tmp_path / "registry")
    torch.testing.assert_close(restored.run(inputs).tensors["features"],
                               direct.run(inputs).tensors["features"])
    with torch.no_grad():
        next(probe.model.parameters()).add_(0.25)
    with pytest.raises(ValueError, match="fingerprint"):
        probe.sae.load("my-native-dictionary-v1", registry_dir=tmp_path / "registry")


def test_public_card_cannot_self_declare_nonfingerprinted_runtime_compatibility(tmp_path):
    from vlmprobe.sae import save_artifact
    probe, sae, binding, _ = _model_bound_dictionary(fingerprinted=False)
    save_artifact(sae, tmp_path / "dictionary", registry_dir=tmp_path / "registry",
                  model_card={"id": "declared-source-dictionary"})
    with pytest.raises(ValueError, match="explicitly verified binding"):
        probe.sae.load("declared-source-dictionary", registry_dir=tmp_path / "registry")
    assert probe.sae.load("declared-source-dictionary", registry_dir=tmp_path / "registry",
                          binding=binding).sae.is_fitted


def test_public_resave_invalidates_numerical_evidence_after_dictionary_change(tmp_path):
    from vlmprobe.sae import save_artifact
    probe, sae, binding, _ = _model_bound_dictionary(imported=True)
    save_artifact(sae, tmp_path / "source", model_card={"evidence": {
        "backbone_compatibility": "not_verified", "numerical_parity": "verified_tensor_io"}})
    loaded = probe.sae.load(tmp_path / "source", binding=binding)
    with torch.no_grad():
        loaded.sae.encoder.weight.add_(.125)
    loaded.save(tmp_path / "modified")
    card = json.loads((tmp_path / "modified/model_card.json").read_text())
    assert card["evidence"]["numerical_parity"] == "not_evaluated_after_state_change"
    assert card["evidence"]["backbone_compatibility"] == "not_verified"
    assert card["training"]["state_modified_since_model_card"] is True
    with pytest.raises(ValueError, match="warm-start"):
        loaded.fit([], [], output_dir=tmp_path / "not-a-warm-start")
