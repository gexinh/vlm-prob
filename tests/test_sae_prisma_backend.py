"""Native-hook compatibility, reversible normalization and real Prisma bridges."""
import json
from types import SimpleNamespace

import pytest
import torch
from torch import nn

from vlm_probing.sae.backends import prisma


def binding(layer=0, model="tiny-prisma"):
    hook = f"blocks.{layer}.hook_resid_post"
    return {"model_id": model + "@frozen-test-revision", "tokenizer_id": "not-applicable:vision-only",
        "preprocessing_id": "test-native-preprocessing@v1", "calibration_id": "disjoint-test-data@v1",
        "site": hook, "layer": layer,
        "hook": {"module": hook, "kind": "output", "selector": None, "tensor_slice": None},
        "backend_model_name": model, "backend_hook_name": hook}


class NativeContractSAE(nn.Module):
    """Test double only for upstream return/state conventions, not SAE numerics."""
    def __init__(self, norm=None):
        super().__init__()
        self.weight = nn.Parameter(torch.eye(4))
        self.cfg = SimpleNamespace(d_in=4, d_sae=4, architecture="standard", activation_fn_str="relu",
            normalize_activations=norm, hook_point_layer=0, hook_point="blocks.0.hook_resid_post",
            model_name="tiny-prisma", is_transcoder=False, cls_token_only=False, use_patches_only=False)

    def encode(self, x):
        if self.cfg.normalize_activations == "constant_norm_rescale":
            self.x_norm_coeff = 2 / x.norm(dim=-1, keepdim=True)
            x = x * self.x_norm_coeff
        elif self.cfg.normalize_activations == "layer_norm":
            self.ln_mu, self.ln_std = x.mean(-1, keepdim=True), x.std(-1, keepdim=True)
            x = (x - self.ln_mu) / (self.ln_std + 1e-5)
        return x, x @ self.weight

    def decode(self, features):
        value = features @ self.weight.T
        if self.cfg.normalize_activations == "constant_norm_rescale":
            value = value / self.x_norm_coeff
            del self.x_norm_coeff
        elif self.cfg.normalize_activations == "layer_norm":
            value = value * self.ln_std + self.ln_mu
        return value


@pytest.mark.parametrize("norm", [None, "none", "layer_norm", "constant_norm_rescale"])
def test_context_preserves_input_specific_coordinates_across_interleaved_inputs(norm):
    native = NativeContractSAE(norm)
    adapter = prisma.wrap(native, binding=binding())
    first = torch.tensor([[1., 2., 4., 8.], [2., 3., 7., 11.]])
    second = first * 3 + 17
    features, context = adapter.encode_with_context(first)
    baseline = adapter.decode_with_context(features, context)
    adapter.encode_with_context(second)
    assert torch.equal(adapter.decode_with_context(features, context), baseline)
    assert torch.equal(adapter.decode_with_context(features.clone(), context), baseline)
    changed = features.clone()
    changed[:, 0] = 0
    assert torch.isfinite(adapter.decode_with_context(changed, context)).all()


@pytest.mark.parametrize("field,value", [("model_id", "wrong-model@v1"), ("layer", 1)])
def test_wrong_native_binding_is_rejected(field, value):
    wrong = binding()
    wrong[field] = value
    if field == "model_id":
        wrong.pop("backend_model_name")
    with pytest.raises(ValueError, match="layer|model"):
        prisma.wrap(NativeContractSAE(), binding=wrong)


def test_hook_width_does_not_permit_cross_backend_translation():
    wrong = binding()
    wrong["hook"]["module"] = "vision_model.encoder.layers.0"
    with pytest.raises(ValueError, match="hook"):
        prisma.wrap(NativeContractSAE(), binding=wrong)


def test_context_owner_geometry_and_zero_norm_are_checked():
    first = prisma.wrap(NativeContractSAE("constant_norm_rescale"), binding=binding())
    second = prisma.wrap(NativeContractSAE("constant_norm_rescale"), binding=binding())
    features, context = first.encode_with_context(torch.ones(2, 4))
    with pytest.raises(ValueError, match="same adapter"):
        second.decode_with_context(features, context)
    with pytest.raises(ValueError, match="token geometry"):
        first.decode_with_context(features[:1], context)
    with pytest.raises(ValueError, match="zero-norm"):
        first.encode(torch.zeros(2, 4))


def test_transcoders_are_not_same_hook_dictionaries():
    native = NativeContractSAE()
    native.cfg.is_transcoder = True
    with pytest.raises(ValueError, match="transcoder"):
        prisma.wrap(native, binding=binding())


def test_hub_requires_immutable_revision_before_optional_import_or_download():
    with pytest.raises(ValueError, match="40-character"):
        prisma.load(release="Prisma-Multimodal/example", revision="main", binding=binding())


def test_backend_metadata_and_offline_starter_catalog_are_json_serializable():
    data = {"info": prisma.backend_info(), "catalog": prisma.list_pretrained()}
    json.dumps(data, allow_nan=False)
    assert data["catalog"][0]["normalize_activations"] is None
    assert len(data["catalog"][0]["revision"]) == 40


def native_classes():
    pytest.importorskip("einops")
    return prisma._native_classes()


def tiny_config(*, architecture="standard", activation="relu", norm=None):
    config_cls, _, _ = native_classes()
    return config_cls(_device="cpu", d_in=8, expansion_factor=2,
        activation_fn_str=activation, activation_fn_kwargs={"k": 3} if activation == "topk" else {},
        normalize_activations=norm, model_name="tiny-prisma", hook_point_layer=0,
        layer_subtype="hook_resid_post", architecture=architecture, log_to_wandb=False)


@pytest.mark.parametrize("architecture,activation", [("standard", "relu"), ("standard", "topk"), ("gated", "relu")])
@pytest.mark.parametrize("norm", [None, "layer_norm", "constant_norm_rescale"])
def test_actual_upstream_dictionary_numerics_and_context(architecture, activation, norm):
    cfg = tiny_config(architecture=architecture, activation=activation, norm=norm)
    sae = prisma._new_sae(cfg)
    adapter = prisma.wrap(sae, binding=binding())
    raw = torch.randn(2, 5, 8)
    _, expected_features = sae.encode(raw)
    expected_reconstruction = sae.decode(expected_features)
    features, context = adapter.encode_with_context(raw)
    assert torch.equal(features, expected_features)
    assert torch.equal(adapter.decode_with_context(features, context), expected_reconstruction)
    adapter.encode_with_context(raw * 4 + 7)
    assert torch.equal(adapter.decode_with_context(features, context), expected_reconstruction)
    assert torch.equal(adapter.decode_with_context(features, context), expected_reconstruction)


def test_actual_prisma_training_resume_and_safe_loading(tmp_path):
    cfg = tiny_config(norm="layer_norm")
    generator = torch.Generator().manual_seed(19)
    train = torch.randn(48, 8, generator=generator)
    validation = torch.randn(12, 8, generator=generator)
    kwargs = dict(config=cfg, dataset=train, eval_dataset=validation, binding=binding(),
                  batch_size=8, patience=8, seed=11, lr=.001,
                  train_ids=["slide-a"], eval_ids=["slide-b"])
    first = prisma.train(output_dir=tmp_path / "resume", epochs=2, **kwargs)
    resumed = prisma.train(output_dir=tmp_path / "resume", epochs=4, **kwargs)
    full = prisma.train(output_dir=tmp_path / "full", epochs=4, **kwargs)
    assert first["completed_epochs"] == 2
    assert resumed["history"] == full["history"]
    assert resumed["source_disjointness_checked"]
    resumed_weights = torch.load(resumed["checkpoint"], weights_only=True)
    full_weights = torch.load(full["checkpoint"], weights_only=True)
    assert all(torch.equal(value, full_weights[key]) for key, value in resumed_weights.items())
    loaded = prisma.load(weights_path=resumed["checkpoint"], binding=binding())
    features, context = loaded.encode_with_context(validation[:2])
    assert loaded.is_fitted
    assert torch.isfinite(loaded.decode_with_context(features, context)).all()
    wrong = binding()
    wrong["preprocessing_id"] = "different-transform@v2"
    with pytest.raises(ValueError, match="saved Prisma binding"):
        prisma.load(weights_path=resumed["checkpoint"], binding=wrong)
    with pytest.raises(ValueError, match="resume data/config"):
        prisma.train(output_dir=tmp_path / "resume", epochs=5, **{**kwargs, "dataset": train + 1})
    with pytest.raises(ValueError, match="identifiers overlap"):
        prisma.train(output_dir=tmp_path / "overlap", epochs=1,
                     **{**kwargs, "eval_ids": ["slide-a"]})


def test_legacy_pickle_is_not_silently_unpickled(tmp_path):
    cfg = tiny_config()
    (tmp_path / "config.json").write_text(json.dumps(prisma._json_value(cfg)))
    torch.save({"cfg": cfg, "state_dict": prisma._new_sae(cfg).state_dict()}, tmp_path / "weights.pt")
    with pytest.raises(Exception, match="Weights only load failed|weights_only|Unsupported global"):
        prisma.load(weights_path=tmp_path / "weights.pt", binding=binding())


def tiny_hooked_vit():
    pytest.importorskip("einops")
    HookedViT, HookedViTConfig = prisma.HookedViT, prisma.HookedViTConfig
    cfg = HookedViTConfig(n_layers=2, d_model=8, d_head=4, d_mlp=16, n_heads=2,
        n_channels=3, patch_size=8, image_size=16, device="cpu",
        model_name="tiny-prisma", return_type="pre_logits")
    return HookedViT(cfg)


def test_actual_hooked_vit_capture_and_model_bound_features_and_edit():
    from vlm_probing import Prober
    from vlm_probing.sae.binding import build_sae_binding
    model = tiny_hooked_vit()
    model.train()
    images = torch.randn(3, 3, 16, 16)
    captured = prisma.capture_activations(model, images, hook_name="blocks.0.hook_resid_post", token_scope="spatial", batch_size=2)
    assert captured.shape == (12, 8)
    assert model.training
    adapter = prisma.make_model_adapter(model, model_id="native-prisma-test@frozen", layers=[0])
    assert adapter.spec.output_kind == "representation"
    probe = Prober(model, adapter=adapter)
    bound = build_sae_binding(probe, 0, model_id="tiny-prisma@frozen",
        tokenizer_id="not-applicable:vision-only", preprocessing_id="native-test@v1", calibration_id="train-slide-a@v1")
    bound.update(backend_model_name="tiny-prisma", backend_hook_name="blocks.0.hook_resid_post")
    sae = prisma.wrap(prisma._new_sae(tiny_config(norm="constant_norm_rescale")), binding=bound)
    result = probe.sae.features(layer=0, sae=sae, binding=bound, tokens="visual").run({"input": images})
    assert result.tensors["features"].shape == (12, 16)
    changed = probe.sae.edit(layer=0, sae=sae, binding=bound, tokens="visual", feature_ids=[0], scale=1).run({"input": images})
    assert "baseline_logits" not in changed.tensors
    assert torch.equal(changed.tensors["baseline_output"], changed.tensors["edited_output"])
    assert model.training
    with pytest.raises(ValueError, match="not classifier logits"):
        prisma.make_model_adapter(model, model_id="native-prisma-test@frozen", output_kind="classification")


def test_custom_image_training_uses_frozen_native_model_and_real_hooks(tmp_path):
    model = tiny_hooked_vit()
    before = {key: value.clone() for key, value in model.state_dict().items()}
    cfg = tiny_config()
    report = prisma.train(config=cfg, model=model, input_kind="images", dataset=torch.randn(5, 3, 16, 16),
        eval_dataset=torch.randn(3, 3, 16, 16), output_dir=tmp_path, binding=binding(),
        epochs=2, batch_size=8, seed=2, train_ids=["train-image-group"], eval_ids=["validation-image-group"])
    assert report["training_rows"] == 25
    assert report["validation_rows"] == 15
    assert all(torch.equal(before[key], value) for key, value in model.state_dict().items())


def test_native_mlp_hook_has_distinct_representation_binding():
    from vlm_probing import Prober
    from vlm_probing.sae.binding import build_sae_binding
    model = tiny_hooked_vit()
    adapter = prisma.make_model_adapter(model, model_id="tiny-prisma@frozen", layers=[0], layer_subtype="hook_mlp_out")
    assert adapter.spec.residuals[0] == "blocks.0.hook_mlp_out"
    assert adapter.site_representations["blocks.0.hook_mlp_out"] == "native_mlp_output"
    probe = Prober(model, adapter=adapter)
    bound = build_sae_binding(probe, 0, model_id="tiny-prisma@frozen", tokenizer_id="not-applicable:vision-only",
                              preprocessing_id="native-test@v1", calibration_id="train-slide-a@v1")
    assert bound["representation"] == "native_mlp_output"


def test_native_runner_schedule_is_explicitly_guarded(tmp_path):
    cfg = tiny_config()
    with pytest.raises(ValueError, match="not vendored"):
        prisma.train(config=cfg, dataset=[], eval_dataset=[], output_dir=tmp_path,
                     binding=binding(), native_runner=True)


def test_vendored_source_manifest_and_license_are_complete():
    import hashlib
    from importlib.resources import files
    root = files("vlm_probing._vendor.prisma")
    manifest = json.loads(root.joinpath("SOURCE.json").read_text())
    assert manifest["commit"] == prisma.AUDITED_REVISION
    assert "MIT License" in root.joinpath("LICENSE").read_text()
    for filename, expected in manifest["local_files"].items():
        assert hashlib.sha256(root.joinpath(filename).read_bytes()).hexdigest() == expected
    for item in manifest["files"]:
        assert len(item["upstream_sha256"]) == 64
        assert item["local_changes"]


def test_vendored_training_does_not_import_official_packages(tmp_path):
    import os
    import subprocess
    import sys
    pytest.importorskip("einops")
    script = r'''
import importlib.abc, sys, tempfile, torch
class BlockOfficial(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in {'vit_prisma','sae_lens','overcomplete'}:
            raise AssertionError('official package import attempted: '+fullname)
sys.meta_path.insert(0,BlockOfficial())
from vlmprobe.sae.backends import prisma
cfg=prisma.VisionModelSAERunnerConfig(_device='cpu',d_in=8,expansion_factor=2,
 activation_fn_str='relu',normalize_activations='layer_norm',model_name='tiny',
 hook_point_layer=0,layer_subtype='hook_resid_post')
hook='blocks.0.hook_resid_post'
binding={'model_id':'tiny@frozen','tokenizer_id':'none:vision','preprocessing_id':'identity:v1',
 'calibration_id':'separate-splits:v1','site':hook,'layer':0,
 'hook':{'module':hook,'kind':'output','selector':None,'tensor_slice':None}}
with tempfile.TemporaryDirectory() as out:
 report=prisma.train(config=cfg,dataset=torch.randn(32,8),eval_dataset=torch.randn(12,8),
                    output_dir=out,binding=binding,epochs=1,batch_size=8)
 sae=prisma.load(weights_path=report['checkpoint'],binding=binding)
 z,ctx=sae.encode_with_context(torch.randn(2,8)); assert sae.decode_with_context(z,ctx).shape==(2,8)
assert not {'vit_prisma','sae_lens','overcomplete'} & set(sys.modules)
'''
    result = subprocess.run([sys.executable, "-c", script], capture_output=True, text=True, env=os.environ.copy())
    assert result.returncode == 0, result.stderr


def test_optional_differential_against_exact_upstream_source():
    """Only this differential test may use an external comparison checkout."""
    pytest.importorskip("vit_prisma.sae.sae")
    from vit_prisma.sae.config import VisionModelSAERunnerConfig as UpstreamConfig
    from vit_prisma.sae.sae import StandardSparseAutoencoder, GatedSparseAutoencoder
    from dataclasses import asdict
    raw = torch.randn(3, 8)
    for architecture, activation in [("standard", "relu"), ("standard", "topk"), ("gated", "relu")]:
        for norm in [None, "layer_norm", "constant_norm_rescale"]:
            cfg = UpstreamConfig(_device="cpu", d_in=8, expansion_factor=2,
                architecture=architecture, activation_fn_str=activation,
                activation_fn_kwargs={"k": 3} if activation == "topk" else {}, normalize_activations=norm)
            source = (GatedSparseAutoencoder if architecture == "gated" else StandardSparseAutoencoder)(cfg)
            selected = prisma._new_sae(prisma._make_config(asdict(cfg)))
            selected.load_state_dict(source.state_dict())
            expected, actual = source(raw), selected(raw)
            for before, after in zip(expected, actual):
                assert before is None and after is None or isinstance(before, torch.Tensor) and torch.equal(before, after)
            expected[2].backward()
            actual[2].backward()
            for (source_name, before), (selected_name, after) in zip(source.named_parameters(), selected.named_parameters()):
                assert source_name == selected_name
                if before.grad is None or after.grad is None:
                    assert before.grad is None and after.grad is None
                else:
                    torch.testing.assert_close(before.grad, after.grad, rtol=2e-6, atol=2e-6)


@pytest.mark.parametrize("config_updates", [{}, {"normalization_type": "LNPre", "layer_norm_pre": True},
                                         {"use_bert_block": True, "activation_name": "quick_gelu"},
                                         {"use_attn_result": True, "use_split_qkv_input": True}])
def test_optional_differential_hooked_vit_forward_and_hooks(config_updates):
    pytest.importorskip("vit_prisma.models.base_vit")
    from vit_prisma.models.base_vit import HookedViT as UpstreamViT
    from vit_prisma.configs.HookedViTConfig import HookedViTConfig as UpstreamConfig
    from dataclasses import asdict
    source = UpstreamViT(UpstreamConfig(n_layers=2, d_model=8, d_head=4, d_mlp=16,
        n_heads=2, n_channels=3, patch_size=8, image_size=16, device="cpu", dtype=torch.float64,
        model_name="tiny-prisma", **config_updates)).double()
    selected = prisma.HookedViT(prisma.HookedViTConfig(**asdict(source.cfg))).double()
    selected.load_state_dict(source.state_dict())
    source.eval(); selected.eval()
    values = torch.randn(2, 3, 16, 16, dtype=torch.float64)
    names = ["blocks.0.hook_resid_post", "blocks.1.hook_mlp_out"]
    expected, before = source.run_with_cache(values, names_filter=names)
    actual, after = selected.run_with_cache(values, names_filter=names)
    # Float64 isolates algebraic parity from fp32 contraction-order rounding.
    torch.testing.assert_close(expected, actual, rtol=1e-10, atol=1e-10)
    for name in names:
        torch.testing.assert_close(before[name], after[name], rtol=1e-10, atol=1e-10)
    projection = torch.randn_like(expected)
    (expected * projection).sum().backward()
    (actual * projection).sum().backward()
    for (source_name, before), (selected_name, after) in zip(source.named_parameters(), selected.named_parameters()):
        assert source_name == selected_name
        if before.grad is None or after.grad is None:
            assert before.grad is None and after.grad is None
        else:
            torch.testing.assert_close(before.grad, after.grad, rtol=1e-9, atol=1e-9)
