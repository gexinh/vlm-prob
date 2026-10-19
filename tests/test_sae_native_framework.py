"""Native API on actual LM, ViT and VLM forwards, not cached measurements."""
import ast
import copy
from pathlib import Path
import subprocess
import sys
import pytest
import torch

from vlmprobe import Prober
from vlmprobe.sae import SAETrainingConfig, list_methods, list_models
from vlmprobe.sae.data import model_identity

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "examples"))


def case(family):
    import transformers as hf
    if family == "language":
        cfg = hf.GPT2Config(vocab_size=40, n_positions=32, n_embd=16, n_layer=2, n_head=2,
                            resid_pdrop=0, embd_pdrop=0, attn_pdrop=0)
        cfg._attn_implementation = "eager"
        model = hf.GPT2LMHeadModel(cfg)
        train = {"input_ids": torch.tensor([[1, 2, 3, 4], [2, 3, 4, 5]])}
        validation = {"input_ids": torch.tensor([[6, 7, 8, 9]])}
        tokens = "all"
    elif family == "vision":
        cfg = hf.ViTConfig(image_size=8, patch_size=4, hidden_size=16, num_hidden_layers=2,
                           num_attention_heads=2, intermediate_size=24, num_labels=3)
        cfg._attn_implementation = "eager"
        model = hf.ViTForImageClassification(cfg)
        train = {"pixel_values": torch.randn(3, 3, 8, 8)}
        validation = {"pixel_values": torch.randn(1, 3, 8, 8)}
        tokens = "visual"
    else:
        from hf_model_matrix import make_model
        model, train = make_model("qwen3_vl")
        validation = {key: value.clone() for key, value in train.items()}
        validation["pixel_values"] = validation["pixel_values"] + .3
        validation["input_ids"][0, 0] = 5
        tokens = "visual"
    return model, train, validation, tokens


@pytest.mark.parametrize("family", ["language", "vision", "multimodal"])
@pytest.mark.parametrize("architecture", ["topk", "gated", "batchtopk"])
def test_same_fit_run_load_and_feature_control_contract(family, architecture, tmp_path):
    torch.set_num_threads(1)
    torch.manual_seed(72)
    model, train, validation, tokens = case(family)
    probe = Prober(model)
    model.train()
    next(iter(model.modules())).training = False
    original = copy.deepcopy(model.state_dict())
    flags = [m.training for m in model.modules()]
    method = probe.sae.method(architecture, layer=0, tokens=tokens, d_sae=24, k=4)
    method.fit([train], [validation], output_dir=tmp_path / "fit",
        train_ids=["document-or-image-A"], validation_ids=["document-or-image-B"],
        preprocessing_id="unit-integration-prepared-v1",
        training=SAETrainingConfig(max_steps=2, batch_size=4))
    assert [m.training for m in model.modules()] == flags
    for key, value in original.items():
        assert torch.equal(value, model.state_dict()[key])
    assert all(parameter.grad is None for parameter in model.parameters())
    result = method.run(validation)
    assert result.tensors["features"].shape[-1] == 24
    assert result.metadata["binding"]["modality"] == family
    assert result.tensors["positions"].shape[1] == 2
    edited = method.edit(feature_ids=[0], scale=1).run(validation)
    assert torch.equal(edited.tensors["baseline_logits"], edited.tensors["edited_logits"])
    control = method.reconstruct().run(validation)
    assert control.metadata["mode"] == "reconstruction"
    method.save(tmp_path / "native", registry_dir=tmp_path / "cards")
    card = list_models(registry_dir=tmp_path / "cards", include_builtin=False)[0]
    assert card["evidence"]["backbone_compatibility"] == "exact_weight_fingerprint_and_native_hook"
    restored = probe.sae.load(tmp_path / "native")
    torch.testing.assert_close(restored.run(validation).tensors["features"], result.tensors["features"])
    via_card = probe.sae.load(card["id"], registry_dir=tmp_path / "cards", binding=method.sae.binding)
    torch.testing.assert_close(via_card.run(validation).tensors["features"], result.tensors["features"])
    # An identical architecture and dimension are not enough: actual weights bind the dictionary.
    with torch.no_grad():
        next(model.parameters()).add_(.125)
    with pytest.raises(ValueError, match="fingerprint"):
        probe.sae.load(tmp_path / "native")


def test_fit_rejects_source_leakage_before_capture_and_cached_batch_overlap(tmp_path):
    model, train, validation, _ = case("vision")
    method = Prober(model).sae.topk(layer=0, d_sae=24, k=4)
    with pytest.raises(ValueError, match="source group overlap"):
        method.fit([train], [validation], output_dir=tmp_path, train_ids=["A"], validation_ids=["A"])
    with pytest.raises(ValueError, match="repeated prepared input"):
        method.fit([train], [train], output_dir=tmp_path)
    with pytest.raises(ValueError, match="max_cache_bytes"):
        method.fit([train], [validation], output_dir=tmp_path, max_cache_bytes=1)


def test_boolean_token_mask_retains_selection_after_artifact_load(tmp_path):
    model, train, validation, _ = case("language")
    validation["input_ids"] = validation["input_ids"].expand(2, -1).clone()
    probe = Prober(model)
    mask = torch.tensor([[True, False, False, True], [False, True, True, False]])
    method = probe.sae.topk(layer=0, tokens=mask, d_sae=24, k=4)
    method.fit([train], [validation], output_dir=tmp_path / "fit",
               training=SAETrainingConfig(max_steps=1, batch_size=4))
    expected = method.run(validation)
    restored = probe.sae.load(tmp_path / "fit/artifact").run(validation)
    assert expected.tensors["positions"].tolist() == mask.nonzero().tolist()
    assert restored.tensors["positions"].tolist() == mask.nonzero().tolist()
    torch.testing.assert_close(restored.tensors["features"], expected.tensors["features"])


def test_framework_does_not_ship_provider_backends_and_runs_without_official_packages():
    forbidden = {"sae_lens", "vit_prisma", "overcomplete", "transformer_lens"}
    for path in (ROOT / "src/vlm_probing/sae").rglob("*.py"):
        for node in ast.walk(ast.parse(path.read_text())):
            names = ([item.name for item in node.names] if isinstance(node, ast.Import)
                     else [node.module or ""] if isinstance(node, ast.ImportFrom) and node.level == 0 else [])
            assert not any(name.split(".")[0] in forbidden for name in names), path
    assert not (ROOT / "src/vlm_probing/sae/backends").exists()
    for name in ("saelens", "prisma", "overcomplete"):
        assert not (ROOT / "src/vlm_probing/_vendor" / name).exists()
    source = '''
import importlib.abc, sys
class BlockOfficial(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in {'sae_lens','vit_prisma','overcomplete','transformer_lens'}:
            raise AssertionError(fullname)
sys.meta_path.insert(0, BlockOfficial())
from vlmprobe.sae import list_methods, list_models, method_config, SparseAutoencoder
import torch
binding={'model_id':'tensor-test','tokenizer_id':'none','preprocessing_id':'identity',
'calibration_id':'independent','site':'x','layer':0,
'hook':{'module':'block','kind':'output','selector':None,'tensor_slice':None}}
for method in list_methods():
    model=SparseAutoencoder(method_config(method['name'],d_in=4,d_sae=8,k=2),binding)
    model.initialize_dictionary_(torch.randn(12,4))
    model.calibrate_(torch.randn(12,4))
    model.eval()
    assert torch.isfinite(model(torch.randn(3,4))[0]).all()
print(len(list_methods()),len(list_models()))
'''
    completed = subprocess.run([sys.executable, "-c", source], check=True, capture_output=True, text=True)
    method_count, model_count = map(int, completed.stdout.split())
    assert method_count == 14
    assert model_count > 0  # Author checkpoint cards load from packaged metadata without an official toolkit.
