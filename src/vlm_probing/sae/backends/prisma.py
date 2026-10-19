"""Optional ViT-Prisma dictionaries, native image hooks and activation training.

Importing this module does not import ViT-Prisma. The implementation delegates
dictionary computations and training objectives to the installed upstream
classes; it does not translate Prisma checkpoints into a different SAE family.
"""
from __future__ import annotations

from dataclasses import asdict, fields, is_dataclass
import hashlib
from importlib.metadata import PackageNotFoundError, version
import json
import math
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import torch
from torch import Tensor, nn

from ..models import validate_sae_binding

SOURCE_URL = "https://github.com/Prisma-Multimodal/ViT-Prisma"
AUDITED_REVISION = "64daf1425f7e5311844213fd0fb6f4127a30cd16"
SNAPSHOT_DATE = "2026-10-19"
_RECOMMENDED = "Prisma-Multimodal/sparse-autoencoder-clip-b-32-sae-vanilla-x64-layer-11-hook_resid_post-l1-1e-05"
_RECOMMENDED_REVISION = "2b1cb17ffb8b06e7f45a699dfc97d417f9879be4"


def _version():
    try:
        return version("vit-prisma")
    except PackageNotFoundError:
        return None


def backend_info() -> dict[str, Any]:
    return {
        "name": "prisma", "package": "vit-prisma", "version": _version(),
        "license": "MIT (code); checkpoint licenses remain checkpoint-specific",
        "source_url": SOURCE_URL, "audited_revision": AUDITED_REVISION,
        "architectures": ["standard/relu", "standard/topk", "gated"],
        "modalities": ["vision"],
        "pretrained_scope": "Native HookedViT CLIP and DINO SAEs; transcoders are distinct and rejected",
        "training_scope": "Native Prisma objectives on explicit disjoint activation splits; optional native VisionSAETrainer",
        "normalization": [None, "none", "layer_norm", "constant_norm_rescale"],
    }


def list_pretrained() -> list[dict[str, Any]]:
    """One verified starter checkpoint; the full official table is linked.

    A catalog entry is a discovery record, not permission to attach its
    dictionary to an arbitrary CLIP implementation with the same width.
    """
    return [{
        "backend": "prisma", "release": _RECOMMENDED,
        "sae_id": "weights.pt", "revision": _RECOMMENDED_REVISION,
        "model": "open-clip:laion/CLIP-ViT-B-32-DataComp.XL-s13B-b90K",
        "hook": "blocks.11.hook_resid_post", "architecture": "standard/relu",
        "d_in": 768, "d_sae": 49152, "token_scope": "CLS and spatial patches",
        "normalize_activations": None, "image_size": 224, "context_size": 50,
        "license": "apache-2.0", "source_url": f"https://huggingface.co/{_RECOMMENDED}",
        "catalog_url": f"{SOURCE_URL}/blob/{AUDITED_REVISION}/docs/sae_table.md",
        "snapshot_date": SNAPSHOT_DATE,
        "loading": "load(release=release, revision=revision, binding=explicit_native_binding)",
    }]


def _native_classes():
    installed = _version()
    if installed is not None and installed.split(".", 1)[0] != "2":
        raise ImportError(
            f"Prisma bridge is audited against GitHub's 2.0 API, not vit-prisma {installed}; "
            f"install git+{SOURCE_URL}.git@{AUDITED_REVISION}"
        )
    try:
        from vit_prisma.sae.config import VisionModelSAERunnerConfig
        from vit_prisma.sae.sae import GatedSparseAutoencoder, StandardSparseAutoencoder
    except ImportError as error:
        raise ImportError(
            f"ViT-Prisma backend requires the audited optional source: git+{SOURCE_URL}.git@{AUDITED_REVISION}. "
            "Install vit-prisma without its legacy [sae] extra; that extra pins sae-lens 2.1.3."
        ) from error
    return VisionModelSAERunnerConfig, StandardSparseAutoencoder, GatedSparseAutoencoder


def _json_value(value):
    if is_dataclass(value):
        value = asdict(value)
    if isinstance(value, dict):
        return {key: _json_value(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_json_value(item) for item in value]
    if isinstance(value, (torch.device, torch.dtype)):
        return str(value).replace("torch.", "")
    return value


def _dtype(value):
    if isinstance(value, str):
        value = getattr(torch, value.removeprefix("torch."), None)
    if value not in {torch.float16, torch.bfloat16, torch.float32, torch.float64}:
        raise ValueError("dtype must be an explicit floating torch dtype")
    return value


def _make_config(config, *, device="cpu", dtype=torch.float32):
    config_cls, _, _ = _native_classes()
    values = _json_value(config) if is_dataclass(config) else dict(config)

    def reconstruct(value):
        if isinstance(value, dict):
            if "__type__" in value:
                return value["value"]
            return {key: reconstruct(item) for key, item in value.items()}
        if isinstance(value, list):
            return [reconstruct(item) for item in value]
        return value

    values = reconstruct(values)
    required = {"model_name", "hook_point_layer", "layer_subtype", "d_in", "expansion_factor", "architecture", "activation_fn_str", "normalize_activations"}
    if not required <= values.keys():
        raise ValueError(f"Prisma config missing explicit fields: {sorted(required - values.keys())}")
    if values.get("is_transcoder", False):
        raise ValueError("transcoders map different representations and are not same-hook SAEs")
    if values["architecture"] not in {"standard", "vanilla", "gated"}:
        raise ValueError("verified Prisma SAE architectures are standard/vanilla and gated")
    if values["activation_fn_str"] not in {"relu", "topk"}:
        raise ValueError("verified Prisma activation functions are relu and topk")
    if values["normalize_activations"] not in {None, "none", "layer_norm", "constant_norm_rescale"}:
        raise ValueError("unknown Prisma activation normalization")
    if any(type(values[key]) is not int or values[key] < 1 for key in ("d_in", "expansion_factor")):
        raise ValueError("Prisma d_in and expansion_factor must be positive integers")
    expected_width = values["d_in"] * values["expansion_factor"]
    if "d_sae" in values and values["d_sae"] != expected_width:
        raise ValueError("Prisma d_sae must equal d_in times expansion_factor")
    if values["activation_fn_str"] == "topk":
        k = values.get("activation_fn_kwargs", {}).get("k")
        if type(k) is not int or not 1 <= k <= expected_width:
            raise ValueError("Prisma TopK requires explicit activation_fn_kwargs.k in [1,d_sae]")
    # Never instantiate legacy configs on their saved/default CUDA device.
    values["_device"] = str(torch.device(device))
    values["_dtype"] = str(_dtype(dtype)).removeprefix("torch.")
    allowed = {item.name for item in fields(config_cls)}
    cfg = config_cls(**{key: value for key, value in values.items() if key in allowed})
    return cfg


def _new_sae(config):
    _, standard, gated = _native_classes()
    return (gated if config.architecture == "gated" else standard)(config)


def _check_config_binding(cfg, binding):
    if getattr(cfg, "hook_point_layer", None) != binding["layer"]:
        raise ValueError("Prisma checkpoint layer differs from bound layer")
    hook_name = getattr(cfg, "hook_point", None)
    declared_hook = binding.get("backend_hook_name", binding["hook"]["module"])
    if hook_name != declared_hook or binding["hook"]["module"] != hook_name:
        raise ValueError("bind the exact native Prisma hook; automatic HF/OpenCLIP hook translation is unsupported")
    if binding["hook"] != {"module": hook_name, "kind": "output", "selector": None, "tensor_slice": None}:
        raise ValueError("Prisma binding must identify the complete native hook output")
    declared_model = binding.get("backend_model_name", binding["model_id"].split("@", 1)[0])
    if getattr(cfg, "model_name", None) != declared_model:
        raise ValueError("Prisma checkpoint model differs from explicitly bound model")


class PrismaAdapter(nn.Module):
    """Adapt a loaded native Prisma SAE, retaining its exact input coordinates.

    ``encode_with_context`` / ``decode_with_context`` retain per-input
    normalization statistics and support repeated baseline/edited decodes.
    Plain ``encode`` / ``decode`` retain upstream's single-chain semantics;
    use the explicit-context API for interleaved inputs or feature edits.
    Instances are not intended for concurrent threaded calls.
    """

    def __init__(self, sae: nn.Module, binding: dict[str, Any], *,
                 expected_binding=None, source_metadata=None, is_fitted=True):
        super().__init__()
        self.binding = validate_sae_binding(binding)
        if expected_binding is not None and validate_sae_binding(expected_binding) != self.binding:
            raise ValueError("Prisma binding differs from expected model/hook/preprocessing identity")
        if not isinstance(sae, nn.Module) or not callable(getattr(sae, "encode", None)) or not callable(getattr(sae, "decode", None)):
            raise TypeError("a loaded native Prisma SAE with encode/decode is required")
        cfg = getattr(sae, "cfg", None)
        if cfg is None:
            raise ValueError("Prisma SAE must retain its native cfg")
        if getattr(cfg, "is_transcoder", False):
            raise ValueError("Prisma transcoders require separate input/output bindings")
        norm = getattr(cfg, "normalize_activations", "missing")
        if norm not in {None, "none", "layer_norm", "constant_norm_rescale"}:
            raise ValueError("unsupported Prisma normalization")
        architecture = getattr(cfg, "architecture", None)
        if architecture not in {"standard", "vanilla", "gated"}:
            raise ValueError("unsupported Prisma dictionary architecture")
        if any(type(getattr(cfg, key, None)) is not int or getattr(cfg, key) < 1 for key in ("d_in", "d_sae")):
            raise ValueError("Prisma dimensions must be positive integers")
        _check_config_binding(cfg, self.binding)
        hook_name = getattr(cfg, "hook_point", None)
        self.sae = sae
        self.normalization = norm
        self.config = SimpleNamespace(d_in=cfg.d_in, d_sae=cfg.d_sae,
            architecture=f"prisma:{architecture}/{getattr(cfg, 'activation_fn_str', 'unknown')}")
        self.source_metadata = {
            "backend": "prisma", "backend_version": _version(), "source_url": SOURCE_URL,
            "audited_revision": AUDITED_REVISION, "backend_model_name": cfg.model_name,
            "backend_hook_name": hook_name, "normalize_activations": norm,
            "token_scope": "CLS only" if getattr(cfg, "cls_token_only", False) else
                "spatial only" if getattr(cfg, "use_patches_only", False) else "CLS and spatial patches",
            "compatibility": "explicit native HookedViT model/hook/preprocessing identity; no width-based transfer",
            **(source_metadata or {}),
        }
        self.is_fitted = bool(is_fitted)

    def _validate(self, value, width, label):
        if not isinstance(value, Tensor) or not value.is_floating_point() or value.ndim < 1 or value.shape[-1] != width:
            raise ValueError(f"Prisma {label} must be floating [...,{width}]")
        if value.numel() == 0 or not torch.isfinite(value).all():
            raise ValueError(f"Prisma {label} must contain finite nonempty values")
        return value

    def encode(self, raw: Tensor) -> Tensor:
        raw = self._validate(raw, self.config.d_in, "activations")
        if self.normalization == "constant_norm_rescale" and (raw.norm(dim=-1) == 0).any():
            raise ValueError("Prisma constant_norm_rescale cannot normalize zero-norm rows")
        if self.normalization == "layer_norm" and self.config.d_in == 1:
            raise ValueError("Prisma layer_norm uses sample std and requires d_in > 1")
        result = self.sae.encode(raw)
        if not isinstance(result, tuple) or len(result) != 2:
            raise ValueError("native Prisma encode must return (sae_input, features)")
        return self._validate(result[1], self.config.d_sae, "encoded features")

    def decode(self, features: Tensor) -> Tensor:
        features = self._validate(features, self.config.d_sae, "features")
        return self._validate(self.sae.decode(features), self.config.d_in, "reconstruction")

    def encode_with_context(self, raw: Tensor):
        features = self.encode(raw)
        names = {"constant_norm_rescale": ("x_norm_coeff",), "layer_norm": ("ln_mu", "ln_std")}.get(self.normalization, ())
        context = {"normalization": self.normalization, "shape": tuple(features.shape[:-1]),
                   "owner": id(self), "statistics": {}}
        for name in names:
            statistic = getattr(self.sae, name, None)
            if not isinstance(statistic, Tensor) or not torch.isfinite(statistic).all():
                raise ValueError(f"native Prisma normalization did not expose finite {name}")
            context["statistics"][name] = statistic.clone()
        return features, context

    def decode_with_context(self, features: Tensor, context):
        if (not isinstance(context, dict) or context.get("owner") != id(self)
                or context.get("normalization") != self.normalization
                or context.get("shape") != tuple(features.shape[:-1])):
            raise ValueError("Prisma decode requires the same adapter and token geometry as its encoding context")
        names = {"constant_norm_rescale": {"x_norm_coeff"}, "layer_norm": {"ln_mu", "ln_std"}}.get(self.normalization, set())
        statistics = context.get("statistics", {})
        if set(statistics) != names:
            raise ValueError("Prisma normalization context is incomplete")
        for name, value in statistics.items():
            setattr(self.sae, name, value.to(device=features.device, dtype=features.dtype))
        return self.decode(features)

    def forward(self, raw):
        features, context = self.encode_with_context(raw)
        return self.decode_with_context(features, context), features


def wrap(sae, *, binding, **kwargs):
    return PrismaAdapter(sae, binding, **kwargs)


def load(*, binding, weights_path=None, config_path=None, release=None,
         revision=None, filename="weights.pt", sae_id=None, device="cpu", dtype=torch.float32,
         expected_binding=None, local_files_only=False, **kwargs):
    """Load explicit JSON config plus tensor-only weights; no legacy pickle.

    Hub loads require an immutable commit revision, retained in provenance.
    ``weights_only=True`` deliberately rejects legacy pickled config objects.
    """
    validate_sae_binding(binding)
    if expected_binding is not None and validate_sae_binding(expected_binding) != validate_sae_binding(binding):
        raise ValueError("Prisma binding differs from expected identities")
    if sae_id is not None:
        if filename != "weights.pt" and filename != sae_id:
            raise ValueError("sae_id and filename refer to different checkpoint files")
        filename = sae_id
    if release is not None:
        if weights_path is not None or config_path is not None:
            raise ValueError("provide either local paths or a Hub release")
        if not isinstance(revision, str) or len(revision) != 40 or any(c not in "0123456789abcdef" for c in revision.lower()):
            raise ValueError("Prisma Hub loading requires an exact 40-character commit revision")
        from huggingface_hub import hf_hub_download
        weights_path = hf_hub_download(release, filename=filename, revision=revision, local_files_only=local_files_only)
        config_path = hf_hub_download(release, filename="config.json", revision=revision, local_files_only=local_files_only)
    if weights_path is None:
        raise ValueError("provide weights_path or release")
    weights_path = Path(weights_path)
    config_path = Path(config_path) if config_path is not None else weights_path.with_name("config.json")
    saved_binding_path = weights_path.with_name("binding.json")
    if saved_binding_path.exists() and validate_sae_binding(json.loads(saved_binding_path.read_text())) != validate_sae_binding(binding):
        raise ValueError("saved Prisma binding differs from requested model/hook/preprocessing identity")
    raw_config = json.loads(config_path.read_text())
    cfg = _make_config(raw_config, device=device, dtype=dtype)
    sae = _new_sae(cfg)
    state = torch.load(weights_path, map_location=device, weights_only=True)
    if isinstance(state, dict) and set(state) == {"state_dict"}:
        state = state["state_dict"]
    if not isinstance(state, dict) or not state or any(not isinstance(value, Tensor) for value in state.values()):
        raise ValueError("Prisma loader accepts tensor-only state_dict weights and a separate JSON config")
    sae.load_state_dict(state, strict=True)
    sae.eval()
    return PrismaAdapter(sae, binding, expected_binding=expected_binding,
        source_metadata={"release": release, "revision": revision,
            "weights_sha256": hashlib.sha256(weights_path.read_bytes()).hexdigest(),
            "config_sha256": hashlib.sha256(config_path.read_bytes()).hexdigest(),
            **kwargs.pop("source_metadata", {})}, **kwargs)


def make_model_adapter(model, *, model_id, layers=None, layer_subtype="hook_resid_post",
                       output_kind="representation"):
    """Expose exact native HookedViT residual/MLP hooks and explicit patch layout.

    Inputs are ``{'input': already_preprocessed_BCHW_tensor}``. No preprocessing
    is inferred and no language/vocabulary readout is invented. Feature edits
    return the model's native output, which may be a CLIP embedding.
    """
    from ...adapters import HookPoint, ModelSpec, TokenLayout, TorchModelAdapter
    cfg = getattr(model, "cfg", None)
    hook_dict = getattr(model, "hook_dict", None)
    if cfg is None or not isinstance(hook_dict, dict) or not callable(getattr(model, "run_with_cache", None)):
        raise TypeError("model must expose native HookedViT cfg, hook_dict and run_with_cache")
    if getattr(cfg, "is_video_transformer", False):
        raise ValueError("video token geometry needs a separate explicit adapter")
    if not isinstance(model_id, str) or not model_id.strip() or model_id == "unspecified":
        raise ValueError("supply an immutable native model identity")
    if output_kind not in {"representation", "classification"}:
        raise ValueError("Prisma output_kind must be representation or explicit classification")
    if output_kind == "classification" and getattr(cfg, "return_type", None) == "pre_logits":
        raise ValueError("native pre_logits outputs are representations, not classifier logits")
    if layer_subtype not in {"hook_resid_post", "hook_mlp_out"}:
        raise ValueError("verified native Prisma hook kinds are hook_resid_post and hook_mlp_out")
    n_layers = getattr(cfg, "n_layers", None)
    layers = list(range(n_layers)) if layers is None and type(n_layers) is int else list(layers or [])
    if not layers or len(set(layers)) != len(layers) or any(type(layer) is not int or not 0 <= layer < n_layers for layer in layers):
        raise ValueError("layers must select unique native HookedViT blocks")
    sites = {f"blocks.{layer}.{layer_subtype}": HookPoint(f"blocks.{layer}.{layer_subtype}") for layer in layers}
    if not sites.keys() <= hook_dict.keys():
        raise ValueError("requested native Prisma hooks are not present in model.hook_dict")
    image_size, patch_size = getattr(cfg, "image_size", None), getattr(cfg, "patch_size", None)
    if any(type(value) is not int or value < 1 for value in (image_size, patch_size)) or image_size % patch_size:
        raise ValueError("native HookedViT cfg must define exact image/patch geometry")
    has_cls = getattr(cfg, "use_cls_token", None)
    if type(has_cls) is not bool:
        raise ValueError("native HookedViT CLS token convention must be explicit")

    def layout(values):
        image = values.get("input")
        if (not isinstance(image, Tensor) or image.ndim != 4
                or image.shape[1] != getattr(cfg, "n_channels", None)
                or tuple(image.shape[-2:]) != (image_size, image_size)):
            raise ValueError("Prisma input must match native cfg's preprocessed BCHW geometry")
        count = (image_size // patch_size) ** 2 + int(has_cls)
        valid = torch.ones((image.shape[0], count), dtype=torch.bool, device=image.device)
        visual = valid.clone()
        if has_cls:
            visual[:, 0] = False
        return TokenLayout(valid=valid, visual=visual)

    spec = ModelSpec(residuals={layer: f"blocks.{layer}.{layer_subtype}" for layer in layers},
        layout=layout, output_kind=output_kind,
        notes=("Native Prisma residuals; model output may be an embedding rather than class logits.",
               "Use cfg-specific upstream preprocessing; visual tokens exclude CLS."))
    adapter = TorchModelAdapter(model, sites, model_id=model_id, spec=spec)
    adapter.site_representations = {site: "native_mlp_output" if layer_subtype == "hook_mlp_out"
                                    else "native_residual_output" for site in sites}
    return adapter


def capture_activations(model, images, *, hook_name, token_scope="all", batch_size=32):
    """Capture a declared native image hook; no layer or token-grid guessing."""
    if token_scope not in {"all", "cls", "spatial"}:
        raise ValueError("token_scope must be all, cls or spatial")
    cfg = getattr(model, "cfg", None)
    if hook_name not in getattr(model, "hook_dict", {}):
        raise ValueError("hook_name must exist in the native model hook_dict")
    if not isinstance(images, Tensor) or images.ndim != 4 or not images.is_floating_point():
        raise ValueError("images must be already preprocessed floating BCHW tensors")
    if (tuple(images.shape[-2:]) != (getattr(cfg, "image_size", None),) * 2
            or images.shape[1] != getattr(cfg, "n_channels", None)):
        raise ValueError("images must match the native cfg's exact channel/image geometry")
    has_cls = getattr(cfg, "use_cls_token", None)
    if token_scope != "all" and type(has_cls) is not bool:
        raise ValueError("CLS convention must be explicit")
    if token_scope == "cls" and not has_cls:
        raise ValueError("native model has no CLS token")
    if type(batch_size) is not int or batch_size < 1:
        raise ValueError("batch_size must be positive")
    states = [(module, module.training) for module in model.modules()]
    device = next(model.parameters()).device
    chunks = []
    try:
        model.eval()
        with torch.no_grad():
            for batch in images.split(batch_size):
                _, cache = model.run_with_cache(batch.to(device), names_filter=[hook_name])
                values = cache[hook_name]
                if values.ndim != 3:
                    raise ValueError("native image hook must expose [batch,token,hidden]")
                if token_scope == "cls":
                    values = values[:, :1]
                elif token_scope == "spatial" and has_cls:
                    values = values[:, 1:]
                chunks.append(values.flatten(0, 1).detach().cpu())
    finally:
        for module, training in states:
            module.training = training
    if not chunks:
        raise ValueError("image dataset is empty")
    return torch.cat(chunks)


def _tensor_hash(value):
    value = value.detach().cpu().contiguous()
    signature = hashlib.sha256()
    signature.update(str((tuple(value.shape), str(value.dtype))).encode())
    signature.update(value.view(torch.uint8).numpy().tobytes())
    return signature.hexdigest()


def train(*, config, dataset, eval_dataset, output_dir, binding, model=None,
          input_kind="activations", epochs=10, batch_size=256, lr=None,
          patience=5, seed=0, device="cpu", dtype=torch.float32, resume=True,
          train_ids=None, eval_ids=None, native_runner=False,
          acknowledge_imagenet_schedule=False):
    """Train actual upstream Prisma dictionaries on user activation/image data.

    The default uses native SAE.forward losses with persistent Adam, independent
    validation selection and exact data/config-bound resume. It deliberately
    bypasses VisionSAETrainer's hardcoded 1.3M-image schedule. The optional native
    runner is available only after explicit acknowledgement of that schedule.
    """
    binding = validate_sae_binding(binding)
    cfg = _make_config(config, device=device, dtype=dtype)
    _check_config_binding(cfg, binding)
    if native_runner:
        if not acknowledge_imagenet_schedule:
            raise ValueError("native Prisma runner assumes 1,300,000 images/epoch; acknowledge_imagenet_schedule=True is required")
        if model is None or input_kind != "images":
            raise ValueError("native runner requires a native model and image datasets")
        from vit_prisma.sae.train_sae import VisionSAETrainer
        cfg.checkpoint_path = str(output_dir)
        runner = VisionSAETrainer(cfg, model, dataset, eval_dataset=eval_dataset)
        runner.run()
        return {"backend": "prisma", "protocol": "native VisionSAETrainer; ImageNet-sized schedule explicitly acknowledged",
                "output_dir": str(output_dir), "binding": binding}
    if input_kind not in {"activations", "images"}:
        raise ValueError("input_kind must be activations or images")
    if type(epochs) is not int or epochs < 1 or type(batch_size) is not int or batch_size < 2:
        raise ValueError("epochs must be positive and batch_size at least two")
    if type(patience) is not int or patience < 1 or type(seed) is not int or seed < 0:
        raise ValueError("patience must be positive and seed nonnegative")
    lr = cfg.lr if lr is None else lr
    if not isinstance(lr, (int, float)) or not math.isfinite(lr) or lr <= 0:
        raise ValueError("lr must be finite and positive")
    if (train_ids is None) != (eval_ids is None):
        raise ValueError("provide both train_ids and eval_ids, or neither")
    if train_ids is not None and set(train_ids) & set(eval_ids):
        raise ValueError("training and validation source identifiers overlap")
    if input_kind == "images":
        if model is None:
            raise ValueError("image training requires the native HookedViT model")
        expected_model = binding.get("backend_model_name", binding["model_id"].split("@", 1)[0])
        if getattr(model.cfg, "model_name", None) != expected_model:
            raise ValueError("image model differs from bound native Prisma model")
        scope = "cls" if cfg.cls_token_only else "spatial" if cfg.use_patches_only else "all"
        dataset = capture_activations(model, dataset, hook_name=cfg.hook_point, token_scope=scope)
        eval_dataset = capture_activations(model, eval_dataset, hook_name=cfg.hook_point, token_scope=scope)
    for label, values in (("training", dataset), ("validation", eval_dataset)):
        if (not isinstance(values, Tensor) or values.ndim != 2 or values.shape[1] != cfg.d_in
                or len(values) < 2 or not values.is_floating_point() or not torch.isfinite(values).all()):
            raise ValueError(f"{label} data must contain at least two finite [N,{cfg.d_in}] activation rows")
    dataset, eval_dataset = dataset.detach().cpu(), eval_dataset.detach().cpu()
    train_hash, validation_hash = _tensor_hash(dataset), _tensor_hash(eval_dataset)
    if train_hash == validation_hash:
        raise ValueError("training and validation activation datasets must be independent")
    target_device = torch.device(device)
    rng_devices = [target_device.index if target_device.index is not None else torch.cuda.current_device()] if target_device.type == "cuda" else []
    with torch.random.fork_rng(devices=rng_devices):
        torch.random.default_generator.manual_seed(seed)
        if rng_devices:
            with torch.cuda.device(rng_devices[0]):
                torch.cuda.manual_seed(seed)
        sae = _new_sae(cfg)
    adapter = PrismaAdapter(sae, binding, is_fitted=False)
    optimizer = torch.optim.Adam(sae.parameters(), lr=lr)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    cfg_values = _json_value(cfg)
    protocol = {"backend": "prisma", "binding": binding, "native_config": cfg_values,
        "batch_size": batch_size, "lr": lr, "seed": seed,
        "train_sha256": train_hash, "validation_sha256": validation_hash,
        "train_ids": list(train_ids) if train_ids is not None else None,
        "eval_ids": list(eval_ids) if eval_ids is not None else None,
        "protocol": "native Prisma SAE.forward objectives; Adam and held-out validation; no fixed ImageNet epoch schedule"}
    protocol_json = json.dumps(protocol, sort_keys=True, allow_nan=False)
    signature = hashlib.sha256(protocol_json.encode()).hexdigest()
    state_path, best_path = directory / "training_state.pt", directory / "weights.pt"
    start, best, bad, history = 0, float("inf"), 0, []
    if resume and state_path.exists():
        saved = torch.load(state_path, map_location=device, weights_only=True)
        if saved.get("signature") != signature:
            raise ValueError("Prisma resume data/config/model binding differs from this run")
        sae.load_state_dict(saved["state_dict"])
        optimizer.load_state_dict(saved["optimizer"])
        start, best, bad, history = saved["epoch"], saved["best"], saved["bad"], saved["history"]
    elif not resume and (state_path.exists() or best_path.exists()):
        raise ValueError("output already contains a Prisma run; use a new directory or resume=True")
    elif not state_path.exists() and any(directory.iterdir()):
        raise ValueError("output directory is nonempty without a resumable Prisma state")
    (directory / "config.json").write_text(json.dumps(cfg_values, indent=2, allow_nan=False) + "\n")
    (directory / "binding.json").write_text(json.dumps(binding, indent=2, allow_nan=False) + "\n")
    (directory / "protocol.json").write_text(json.dumps(protocol, indent=2, allow_nan=False) + "\n")

    def batches(values, indices=None):
        # Native normalized MSE uses a batch center and is undefined for one row.
        order = torch.arange(len(values)) if indices is None else indices
        parts = list(order.split(batch_size))
        if len(parts[-1]) == 1 and len(parts) > 1:
            parts[-2] = torch.cat((parts[-2], parts.pop()))
        return (values[index].to(device=device, dtype=_dtype(dtype)) for index in parts)

    def validate():
        sae.eval()
        total, count = 0., 0
        with torch.no_grad():
            for values in batches(eval_dataset):
                objective = sae(values)[2]
                if not torch.isfinite(objective):
                    raise ValueError("native Prisma validation objective is nonfinite; check activation variance/normalization")
                total += float(objective) * len(values)
                count += len(values)
        return total / count

    for epoch in range(start, epochs):
        if bad >= patience:
            break
        sae.train()
        generator = torch.Generator().manual_seed(seed + epoch)
        permutation = torch.randperm(len(dataset), generator=generator)
        total, count = 0., 0
        for values in batches(dataset, permutation):
            optimizer.zero_grad(set_to_none=True)
            objective = sae(values)[2]
            if not torch.isfinite(objective):
                raise ValueError("native Prisma training objective is nonfinite; check activation variance/normalization")
            objective.backward()
            if cfg.max_grad_norm:
                nn.utils.clip_grad_norm_(sae.parameters(), cfg.max_grad_norm)
            optimizer.step()
            sae.set_decoder_norm_to_unit_norm()
            total += float(objective.detach()) * len(values)
            count += len(values)
        validation_loss = validate()
        history.append({"epoch": epoch + 1, "train_objective": total / count, "validation_objective": validation_loss})
        if validation_loss < best:
            best, bad = validation_loss, 0
            torch.save({key: value.detach().cpu() for key, value in sae.state_dict().items()}, best_path)
        else:
            bad += 1
        torch.save({"signature": signature, "epoch": epoch + 1, "best": best, "bad": bad,
                    "history": history, "state_dict": sae.state_dict(), "optimizer": optimizer.state_dict()}, state_path)
        (directory / "history.json").write_text(json.dumps(history, indent=2) + "\n")
    if not best_path.exists():
        raise ValueError("no completed Prisma checkpoint available")
    sae.load_state_dict(torch.load(best_path, map_location=device, weights_only=True))
    sae.eval()
    adapter.is_fitted = True
    report = {"backend": "prisma", "output_dir": str(directory), "checkpoint": str(best_path),
        "best_validation_objective": best, "completed_epochs": len(history),
        "training_rows": len(dataset), "validation_rows": len(eval_dataset),
        "source_disjointness_checked": train_ids is not None,
        "protocol": protocol["protocol"], "binding": binding, "history": history}
    (directory / "report.json").write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    return report
