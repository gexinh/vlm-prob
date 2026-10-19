"""Published model metadata and local native artifact contracts."""
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


def test_published_model_information_is_unified_and_deduplicated():
    cards = list_models()
    assert len(cards) == 9660
    assert len({card["id"] for card in cards}) == len(cards)
    assert len({(c["download"]["repo_id"], c["download"]["path"]) for c in cards}) == len(cards)
    assert {card["status"] for card in cards} == {"published"}
    assert {card["artifact_kind"] for card in cards} == {"sae"}
    assert sum(len(card["registry_aliases"]) for card in cards) == 10089
    assert all("transcoder" not in str(c["origin"].get("conversion_recipe", "")) for c in cards)
    assert len(list_models(artifact_kind="backbone")) == 5
    assert len(list_models(artifact_kind=None)) == 9665
    assert len(list_models(method="topk", modality="vision")) == 12
    assert all(card["method"] == "unknown" for card in list_models(method="unknown", limit=3))


def test_published_cards_have_direct_weights_and_our_own_information_pages():
    cards = list_models(artifact_kind=None)
    root = Path(__file__).resolve().parents[1]
    pages = {}
    for card in cards:
        page, anchor = card["links"]["card"].split("#")
        assert page.startswith("docs/methods/sae/models/")
        path = root / page
        assert path.is_file(), page
        if path not in pages:
            pages[path] = path.read_text()
        assert f'id="{anchor}"' in pages[path], card["id"]
        assert card["links"]["checkpoint"].startswith(("https://huggingface.co/", "https://dl.fbaipublicfiles.com/"))
        assert card["links"]["repository"].startswith(("https://huggingface.co/", "https://github.com/facebookresearch/dinov2"))
        if card["artifact_kind"] == "sae":
            assert "candidate" not in card["id"]
            assert "/resolve/" in card["links"]["checkpoint"] or "/tree/" in card["links"]["checkpoint"]
    assert len(pages) == 308  # 307 paginated SAE pages plus one backbone page.


def test_published_download_metadata_preserves_known_source_settings():
    gpt2 = get_model_card("gpt2-layer8-relu-768")
    assert gpt2["dimensions"] == {"activation": 768, "features": 768}
    assert gpt2["input_conventions"]["model_from_pretrained_kwargs"] == {"center_writing_weights": True}
    assert len(gpt2["download"]["sha256"]) == 64
    clip = get_model_card("clip-b32-layer11-relu-49152")
    assert clip["dimensions"] == {"activation": 768, "features": 49152}
    assert clip["image_geometry"]["patch_grid"] == [7, 7]
    assert clip["download"]["revision"] == "2b1cb17ffb8b06e7f45a699dfc97d417f9879be4"
    with pytest.raises(ValueError, match="download its weights and use import_checkpoint"):
        load_model(clip["id"])
    # Cards are descriptive copies; callers cannot mutate the packaged records.
    clip["dimensions"]["activation"] = -1
    assert get_model_card(clip["id"])["dimensions"]["activation"] == 768


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
    assert all(c["id"] != card["id"] for c in list_models())  # Local registration is explicit.
    restored = probe.sae.load(card["id"], registry_dir=tmp_path / "registry")
    torch.testing.assert_close(restored.run(validation).tensors["features"],
                               fitted.run(validation).tensors["features"])
    md = render_model_card(card, tmp_path / "model.md")
    page = render_model_card(card, tmp_path / "model.html")
    assert "My domain dictionary" in md.read_text()
    assert "trained-domain-topk-v1" in page.read_text()
    assert "<!doctype html>" in page.read_text()
    assert list_models(registry_dir=tmp_path / "registry", method="relu", include_builtin=False) == []


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
