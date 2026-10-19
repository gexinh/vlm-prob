"""Locally controlled pinned SAELens core and activation-source trainer.

Model activation collection is separate from dictionary training. SAETrainer
accepts language, vision or multimodal vectors. TransformerLens hook names are
never translated automatically to native module names: bindings are explicit.
"""
from __future__ import annotations

from dataclasses import asdict
import json
import math
from pathlib import Path
import re
from types import SimpleNamespace
from typing import Any

import torch
from torch import Tensor, nn

from ..models import validate_sae_binding


SOURCE = "https://github.com/decoderesearch/SAELens"
AUDITED_COMMIT = "30c4502466785dd7809a307f7b705df187978aa3"
INFERENCE_ARCHITECTURES = ("standard", "gated", "topk", "jumprelu", "abstopk", "matching_pursuit")
TRAINING_ARCHITECTURES = (*INFERENCE_ARCHITECTURES, "batchtopk", "matryoshka_batchtopk")


def _version(*, required=True):
    """Pinned source version, independent of installed official distributions."""
    return "6.54.6"


def backend_info() -> dict[str, Any]:
    """Capabilities without loading vendored core or downloading weights."""
    return {"name": "saelens", "package": "vlmprobe", "version": "6.54.6+vlmprobe.1",
            "implementation": "vendored", "vendored_revision": 1, "upstream_package": "sae-lens",
            "verified_version": "6.54.6", "supported_major_version": "6", "license": "MIT", "source": SOURCE,
            "source_commit": AUDITED_COMMIT, "architectures": list(INFERENCE_ARCHITECTURES),
            "training_architectures": list(TRAINING_ARCHITECTURES),
            "modalities": ["language", "vision", "multimodal"],
            "pretrained_scope": "Pinned vendored upstream registry; entries are candidates, not automatic native-hook compatibility.",
            "training_scope": "Locally controlled pinned SAETrainer over caller-provided batches from any frozen model; no official-package/model-stack dependency.",
            "limitations": ["Independent-vector same-space dictionaries only; transcoders and temporal SAEs require different contracts.",
                            "Inference requires normalize_activations='none', including upstream-folded scaling or whitening; runtime normalization and head reshaping are rejected."]}


def _meta(metadata, key, default=None):
    return metadata.get(key, default) if isinstance(metadata, dict) else getattr(metadata, key, default) if metadata is not None else default


class SAELensAdapter(nn.Module):
    """Use the controlled pinned encode/decode implementation in raw coordinates.

    Binding identifies exact model, tokenizer, preprocessing, calibration and
    native hook. Declare upstream names separately as backend_model_name and
    backend_hook_name when naming differs. Width alone is never compatibility.
    """

    def __init__(self, sae: nn.Module, binding: dict[str, Any], *,
                 expected_binding=None, source_metadata=None):
        super().__init__()
        if not isinstance(sae, nn.Module) or not callable(getattr(sae, "encode", None)) or not callable(getattr(sae, "decode", None)):
            raise TypeError("a loaded SAELens nn.Module with encode/decode is required")
        self.binding = validate_sae_binding(binding)
        if expected_binding is not None and validate_sae_binding(expected_binding) != self.binding:
            raise ValueError("external SAE binding differs from expected native model/hook identities")
        config = getattr(sae, "cfg", None)
        if config is None or getattr(config, "normalize_activations", None) != "none":
            raise ValueError("SAELens adapter requires normalize_activations='none'; use upstream-folded normalization before wrapping")
        if type(getattr(config, "apply_b_dec_to_input", None)) is not bool:
            raise ValueError("external SAE must explicitly specify apply_b_dec_to_input")
        if getattr(config, "reshape_activations", "none") != "none":
            raise ValueError("head reshaping requires a separate explicitly verified adapter")
        d_in, d_sae = getattr(config, "d_in", None), getattr(config, "d_sae", None)
        if any(type(value) is not int or value < 1 for value in (d_in, d_sae)):
            raise ValueError("external SAE dimensions must be explicit positive integers")
        architecture = config.architecture() if callable(getattr(config, "architecture", None)) else getattr(config, "architecture", None)
        if architecture not in INFERENCE_ARCHITECTURES:
            raise ValueError(f"unsupported independent-vector same-space architecture {architecture!r}; transcoders/temporal SAEs require different hook/context contracts")
        if getattr(config, "d_out", d_in) != d_in:
            raise ValueError("external SAE decoder must reconstruct the same native activation space")
        metadata = getattr(config, "metadata", None)
        hook_layer = _meta(metadata, "hook_layer")
        if hook_layer is not None and hook_layer != self.binding["layer"]:
            raise ValueError("SAELens declared layer differs from explicit native binding")
        if _meta(metadata, "hook_head_index") is not None:
            raise ValueError("head-specific SAEs cannot be applied to a full native residual tensor")
        backend_model = _meta(metadata, "model_name")
        if backend_model is not None and backend_model != self.binding.get("backend_model_name", self.binding["model_id"].split("@", 1)[0]):
            raise ValueError("SAELens declared model differs from explicit native/source model binding")
        backend_hook = _meta(metadata, "hook_name")
        if backend_hook is not None and self.binding.get("backend_hook_name") != backend_hook:
            raise ValueError("declare the exact SAELens backend_hook_name alongside the verified native hook; automatic hook translation is unsupported")
        backend_tokenizer = _meta(metadata, "tokenizer_name")
        if backend_tokenizer is not None and backend_tokenizer != self.binding.get("backend_tokenizer_name", self.binding["tokenizer_id"].split("@", 1)[0]):
            raise ValueError("SAELens declared tokenizer differs from explicit tokenizer binding")
        backend_kwargs = _meta(metadata, "model_from_pretrained_kwargs")
        if backend_kwargs and self.binding.get("backend_model_from_pretrained_kwargs") != backend_kwargs:
            raise ValueError("declare and verify backend_model_from_pretrained_kwargs; upstream model processing can change activation coordinates")
        self.sae = sae
        self.config = SimpleNamespace(d_in=d_in, d_sae=d_sae, architecture="saelens:" + architecture)
        self.source_metadata = {"backend": "saelens", "architecture": architecture,
            "normalize_activations": "none", "apply_b_dec_to_input": config.apply_b_dec_to_input,
            "backend_hook_name": backend_hook, "backend_model_name": backend_model,
            "backend_model_from_pretrained_kwargs": backend_kwargs,
            "source": SOURCE, "license": "MIT",
            "compatibility": "explicit native model/module/tokenizer binding; no dimension-based inference",
            **(source_metadata or {})}
        self.is_fitted = True

    @staticmethod
    def _check(value, width, label):
        if not isinstance(value, Tensor) or not value.is_floating_point() or value.ndim < 1 or value.shape[-1] != width:
            raise ValueError(f"external SAE {label} must be floating [...,{width}]")
        if value.numel() == 0 or not torch.isfinite(value).all():
            raise ValueError(f"external SAE {label} must be finite and nonempty")

    def encode(self, raw: Tensor) -> Tensor:
        self._check(raw, self.config.d_in, "input")
        features = self.sae.encode(raw)
        if not isinstance(features, Tensor) or features.shape != (*raw.shape[:-1], self.config.d_sae):
            raise ValueError("upstream encode changed token geometry or dictionary width")
        return features

    def decode(self, features: Tensor) -> Tensor:
        self._check(features, self.config.d_sae, "features")
        reconstruction = self.sae.decode(features)
        if not isinstance(reconstruction, Tensor) or reconstruction.shape != (*features.shape[:-1], self.config.d_in):
            raise ValueError("upstream decode changed token geometry or native activation width")
        return reconstruction

    def forward(self, raw: Tensor) -> tuple[Tensor, Tensor]:
        features = self.encode(raw)
        return self.decode(features), features

    @classmethod
    def from_pretrained(cls, release, sae_id, *, binding, device="cpu", dtype="float32",
                        expected_binding=None, force_download=False):
        """v6 returns an SAE object and folds recorded scaling when available."""
        binding = validate_sae_binding(binding)
        if expected_binding is not None and validate_sae_binding(expected_binding) != binding:
            raise ValueError("external SAE binding differs from expected native identities")
        installed = _version()
        from vlm_probing._vendor.saelens import SAE
        sae = SAE.from_pretrained(release=release, sae_id=sae_id, device=device,
                                  dtype=dtype, force_download=force_download)
        return cls(sae, binding, expected_binding=expected_binding,
                   source_metadata={"backend_version": installed, "implementation": "vendored", "release": release, "sae_id": sae_id})


def wrap(sae, *, binding, **kwargs):
    """Wrap compatible caller-loaded weights with explicit model/data binding."""
    return SAELensAdapter(sae, binding, **kwargs)


def load(*, binding, release=None, sae_id=None, path=None, device="cpu", dtype="float32",
         expected_binding=None, force_download=False):
    """Load an upstream release or a native SAELens inference directory.

    Saved VLMProbe bindings are checked before loading weights from a local
    directory written by train(). Upstream directories without that metadata
    require the same explicit caller-verified binding as remote releases.
    """
    binding = validate_sae_binding(binding)
    if path is None:
        if not release or not sae_id:
            raise ValueError("provide release and sae_id, or one local path")
        return SAELensAdapter.from_pretrained(release, sae_id, binding=binding,
            device=device, dtype=dtype, expected_binding=expected_binding, force_download=force_download)
    if release is not None or sae_id is not None:
        raise ValueError("local path and pretrained release identifiers are mutually exclusive")
    if expected_binding is not None and validate_sae_binding(expected_binding) != binding:
        raise ValueError("external SAE binding differs from expected native identities")
    path = Path(path)
    saved_binding = path / "vlmprobe_binding.json"
    if saved_binding.exists() and validate_sae_binding(json.loads(saved_binding.read_text())) != binding:
        raise ValueError("saved SAELens checkpoint binding differs from requested model/data/hook identities")
    installed = _version()
    from vlm_probing._vendor.saelens import SAE
    return wrap(SAE.load_from_disk(path, device=device, dtype=dtype), binding=binding,
                expected_binding=expected_binding, source_metadata={"backend_version": installed, "implementation": "vendored", "path": str(path)})


def list_pretrained(*, release=None, model=None, sae_id=None):
    """Pinned vendored upstream registry without weight downloads or hook guessing."""
    installed = _version()
    from vlm_probing._vendor.saelens.loading.pretrained_saes_directory import get_pretrained_saes_directory
    registry = get_pretrained_saes_directory()
    if release is not None and release not in registry:
        raise ValueError(f"unknown SAELens release {release!r}")
    rows = []
    for release_name, item in sorted(registry.items()):
        if (release is not None and release != release_name) or (model is not None and model != item.model):
            continue
        for entry_id, path in sorted(item.saes_map.items()):
            if sae_id is not None and sae_id != entry_id:
                continue
            hook = entry_id if re.fullmatch(r"blocks\.\d+\.hook_(resid_pre|resid_post|resid_mid|attn_out|mlp_out|z)", entry_id) else None
            known_special = any(value in str(item.conversion_func) for value in ("transcoder", "temporal")) or "transcoder" in release_name or release_name.startswith("temporal-")
            rows.append({"backend": "saelens", "release": release_name,
                         "sae_id": entry_id, "model": item.model, "hook": hook,
                         "architecture": None, "repo_id": item.repo_id,
                         "path": path, "source_url": f"https://huggingface.co/{item.repo_id}/tree/main/{path}",
                         "registry_version": installed, "neuronpedia_id": item.neuronpedia_id.get(entry_id),
                         "norm_scaling_factor": item.norm_scaling_factor.get(entry_id),
                         "adapter_compatible": False if known_special else None,
                         "native_compatibility": "requires_verified_model_hook_and_preprocessing_binding"})
    return rows


def create_training_sae(*, architecture="standard", d_in, d_sae, device="cpu", dtype="float32", **sae_config):
    """Build a locally maintained pinned TrainingSAE; unknown arguments raise.

    Pass native arguments such as l1_coefficient (standard/gated), k (TopK), or
    the architecture-specific BatchTopK/Matryoshka settings.
    """
    _version()
    if architecture not in TRAINING_ARCHITECTURES:
        raise ValueError(f"unsupported SAELens training architecture {architecture!r}")
    from vlm_probing._vendor.saelens import TrainingSAE
    cfg_class = TrainingSAE.get_sae_config_class_for_architecture(architecture)
    cfg = cfg_class(d_in=d_in, d_sae=d_sae, device=str(device), dtype=dtype, **sae_config)
    return TrainingSAE.from_dict(cfg.to_dict())


def _resume_sae_config(config):
    """Remove device/precision moves and upstream final-summary statistics."""
    value = json.loads(json.dumps(config, allow_nan=False))
    value.pop("device", None)
    value.pop("dtype", None)
    metadata = value.get("metadata")
    if isinstance(metadata, dict):
        # SAETrainer.set_final_sae_metadata adds these after fitting. They are
        # observations of the previous fit, not changed dictionary objectives.
        metadata.pop("l0", None)
        metadata.pop("num_dead_features", None)
    return value


def _verify_resume_protocol(path, *, binding, sae_config, trainer_config, installed, optimizer):
    """Verify optimizer/objective semantics before restoring native state."""
    saved_binding = path / "vlmprobe_binding.json"
    if not saved_binding.exists() or validate_sae_binding(json.loads(saved_binding.read_text())) != binding:
        raise ValueError("resume checkpoint requires the same saved native/data binding")
    saved_protocol = path / "vlmprobe_training_protocol.json"
    if not saved_protocol.exists():
        # Compatibility with this adapter's earlier local runs, which retained
        # the same configuration beside training_state rather than inside it.
        saved_protocol = path.parent / "protocol.json"
    if not saved_protocol.exists():
        raise ValueError("resume requires a saved SAELens training protocol; optimizer semantics cannot be inferred from weights")
    saved = json.loads(saved_protocol.read_text())
    if not isinstance(saved, dict) or saved.get("backend") != "saelens" or saved.get("status") != "complete" or saved.get("binding") != binding:
        raise ValueError("resume training protocol must be complete and match the saved backend/data binding")
    if saved.get("backend_version") != installed:
        raise ValueError("resume training protocol backend version differs; native optimizer/scheduler compatibility is unverified")
    previous_sae = saved.get("sae_config")
    previous_trainer = saved.get("trainer_config")
    if not isinstance(previous_sae, dict) or not isinstance(previous_trainer, dict):
        raise ValueError("resume training protocol requires complete sae_config and trainer_config")
    if _resume_sae_config(previous_sae) != _resume_sae_config(sae_config):
        raise ValueError("resume SAE configuration differs; k, losses, normalization and objective parameters must match")
    requested = asdict(trainer_config)
    noncritical = {"device", "logger", "checkpoint_path", "n_checkpoints", "save_final_checkpoint", "total_training_samples"}
    old_critical = {key: value for key, value in previous_trainer.items() if key not in noncritical}
    new_critical = {key: value for key, value in requested.items() if key not in noncritical}
    if old_critical != new_critical:
        changed = sorted(key for key in old_critical.keys() | new_critical.keys() if old_critical.get(key) != new_critical.get(key))
        raise ValueError(f"resume trainer configuration differs for {changed}; optimizer, schedule and activation protocol must match")
    old_total = previous_trainer.get("total_training_samples")
    completed = saved.get("training_samples")
    new_total = requested["total_training_samples"]
    if type(old_total) is not int or type(completed) is not int or completed < 1:
        raise ValueError("resume training protocol lacks a valid previous sample budget/completed count")
    if new_total < old_total or new_total < completed:
        raise ValueError("resume training budget cannot precede the previous target or completed sample count")
    extension = new_total != old_total
    if extension and not (
        requested["lr_scheduler_name"] == "constant"
        and requested["lr_warm_up_steps"] == 0
        and requested["lr_decay_steps"] == 0
        and requested["n_restart_cycles"] == 1
        and requested["lr_end"] == requested["lr"]
    ):
        raise ValueError("resume budget extension requires constant learning rate with no warmup/decay/restarts; other schedules depend on the original budget")
    from vlm_probing._vendor.saelens.constants import TRAINER_STATE_FILENAME
    state = torch.load(path / TRAINER_STATE_FILENAME, map_location="cpu", weights_only=True)
    if state.get("n_training_samples") != completed or state.get("n_training_steps") != saved.get("training_steps"):
        raise ValueError("resume native trainer counters differ from the saved completed protocol")
    groups = state.get("optimizer", {}).get("param_groups")
    fresh_groups = optimizer.state_dict()["param_groups"]
    if not isinstance(groups, list) or len(groups) != len(fresh_groups):
        raise ValueError("resume native optimizer parameter groups differ")
    for old_group, fresh_group in zip(groups, fresh_groups):
        ignored = {"params", "lr", "initial_lr"}
        if ({key: value for key, value in old_group.items() if key not in ignored}
                != {key: value for key, value in fresh_group.items() if key not in ignored}
                or len(old_group.get("params", [])) != len(fresh_group["params"])):
            raise ValueError("resume native optimizer options differ from the verified trainer configuration")
        rate = old_group.get("lr")
        if not isinstance(rate, (int, float)) or not math.isfinite(rate) or rate < 0:
            raise ValueError("resume native optimizer learning rate must be finite and nonnegative")
        if old_group.get("initial_lr") != requested["lr"]:
            raise ValueError("resume native optimizer initial learning rate differs from the training protocol")
        if requested["lr_scheduler_name"] == "constant" and requested["lr_warm_up_steps"] == 0 and rate != requested["lr"]:
            raise ValueError("resume native optimizer learning rate differs from the constant-learning-rate protocol")
    return {"protocol": str(saved_protocol), "previous_target_samples": old_total,
            "previous_completed_samples": completed, "requested_target_samples": new_total,
            "budget_extension": "constant_learning_rate_only" if extension else "none",
            "native_optimizer_verified": True,
            "allowed_changes": ["device", "dtype", "logging/checkpoint output settings"],
            "data_order": "caller must restore the activation iterator position"}


def train(*, config, activation_source=None, model=None, output_dir, binding,
          evaluator=None, validation_source=None, max_validation_batches=100,
          resume_from=None, **kwargs):
    """Execute the vendored SAETrainer over raw training-only activation batches.

    model is a controlled-core TrainingSAE, not the frozen source model. Alternatively
    config={'sae': {...}, 'trainer': {...}, 'seed': 0} constructs one. The source
    yields [N,d_in] tensors. The caller supplies dataset-level splitting and a
    separate held-out validation iterator. Optimizer/trainer state is saved; exact replay
    requires the caller to restore the activation iterator position too.
    """
    if kwargs:
        raise TypeError(f"unknown SAELens training arguments: {sorted(kwargs)}")
    installed = _version()
    binding = validate_sae_binding(binding)
    if activation_source is None:
        raise ValueError("supply an iterator yielding training-only raw [N,d_in] activation tensors")
    if evaluator is not None:
        raise ValueError("the upstream remote-logging evaluator hook is outside the vendored core; provide validation_source for independent local evaluation")
    if type(max_validation_batches) is not int or max_validation_batches < 1:
        raise ValueError("max_validation_batches must be a positive integer")
    from vlm_probing._vendor.saelens import SAE, SAETrainer, TrainingSAE
    from vlm_probing._vendor.saelens.config import LoggingConfig, SAETrainerConfig
    if isinstance(config, dict):
        if set(config) - {"sae", "trainer", "seed"}:
            raise ValueError(f"unknown training config fields: {sorted(set(config) - {'sae', 'trainer', 'seed'})}")
        if model is None:
            if "sae" not in config:
                raise ValueError("config['sae'] is required when no TrainingSAE model is supplied")
            seed = config.get("seed", 0)
            if type(seed) is not int or not 0 <= seed < 2 ** 63:
                raise ValueError("seed must be an integer in [0, 2**63)")
            target = torch.device(config["sae"].get("device", "cpu"))
            devices = [torch.cuda.current_device() if target.index is None else target.index] if target.type == "cuda" else []
            with torch.random.fork_rng(devices=devices):
                torch.random.default_generator.manual_seed(seed)
                for index in devices:
                    torch.cuda.default_generators[index].manual_seed(seed)
                model = create_training_sae(**config["sae"])
        arguments = dict(config.get("trainer", {}))
        if isinstance(arguments.get("logger"), dict):
            arguments["logger"] = LoggingConfig(**arguments["logger"])
        arguments.setdefault("logger", LoggingConfig(log_to_wandb=False))
        arguments.setdefault("save_final_checkpoint", False)
        trainer_config = SAETrainerConfig(**arguments)
    elif isinstance(config, SAETrainerConfig):
        trainer_config = config
        if model is None:
            raise ValueError("supply a controlled-core TrainingSAE with its SAETrainerConfig")
    else:
        raise TypeError("config must be a dictionary or controlled-core SAETrainerConfig")
    if not isinstance(model, TrainingSAE):
        raise TypeError("model must be a TrainingSAE from VLMProbe's vendored SAELens core; pass frozen-backbone activations through activation_source")
    if trainer_config.total_training_samples < 1 or trainer_config.train_batch_size_samples < 1 or trainer_config.total_training_steps < 1:
        raise ValueError("positive training sample count must cover at least one full batch")
    if trainer_config.lr_end is None:
        trainer_config.lr_end = trainer_config.lr
    for name in ("lr", "lr_end"):
        value = getattr(trainer_config, name)
        if isinstance(value, bool) or not isinstance(value, (float, int)) or not math.isfinite(value) or value < 0 or (name == "lr" and value == 0):
            raise ValueError(f"{name} must be a finite {'positive' if name == 'lr' else 'nonnegative'} learning rate")
    for name in ("adam_beta1", "adam_beta2"):
        value = getattr(trainer_config, name)
        if isinstance(value, bool) or not isinstance(value, (float, int)) or not math.isfinite(value) or not 0 <= value < 1:
            raise ValueError(f"{name} must be finite and in [0, 1)")
    if model.cfg.normalize_activations not in {"none", "expected_average_only_in", "covariance_whitening"}:
        raise ValueError("training export supports none or upstream-folded scaling/whitening, not stateful runtime normalization")
    architecture = model.cfg.architecture()
    if architecture not in TRAINING_ARCHITECTURES:
        raise ValueError("training model architecture is not supported by this independent-vector backend")
    if getattr(model.cfg, "reshape_activations", "none") != "none":
        raise ValueError("head reshaping requires a separately verified activation contract")
    if resume_from is not None and model.cfg.normalize_activations != "none":
        raise ValueError("resume of exported final checkpoints currently requires normalize_activations='none'; folded normalization changes optimizer coordinates")
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    protocol_path = output_dir / "protocol.json"
    if protocol_path.exists():
        if json.loads(protocol_path.read_text()).get("binding") != binding:
            raise ValueError("output directory already contains a different model/data/hook binding")
        if resume_from is None:
            raise ValueError("output directory contains an earlier run; choose a new directory or explicitly resume")
    source = iter(activation_source)

    def checked_source():
        while True:
            batch = next(source)
            SAELensAdapter._check(batch, model.cfg.d_in, "training input")
            if batch.ndim != 2:
                raise ValueError("activation source must yield [N,d_in]; flatten only known token/patch axes")
            # SAE training must not backpropagate through a caller's backbone.
            yield batch.detach()

    protocol = {"backend": "saelens", "status": "running", "backend_version": installed, "implementation": "vendored", "vendored_revision": 1,
                "source": SOURCE, "license": "MIT", "binding": binding, "architecture": architecture,
                "sae_config": model.cfg.to_dict(), "trainer_config": asdict(trainer_config),
                "data_protocol": "Caller-supplied train-only raw activation iterator; caller owns source-level splits and independent evaluation.",
                "resume_protocol": "Upstream optimizer/trainer state for normalize_activations=none; caller restores source position for exact data-order replay. Final folded-normalization checkpoints are inference-only in this wrapper.",
                "resume_from": str(resume_from) if resume_from is not None else None}
    protocol_path.write_text(json.dumps(protocol, indent=2, default=str, allow_nan=False) + "\n")
    try:
        trainer = SAETrainer(cfg=trainer_config, sae=model, data_provider=checked_source(), evaluator=evaluator)
        if resume_from is not None:
            resume_from = Path(resume_from)
            protocol["resume_validation"] = _verify_resume_protocol(resume_from,
                binding=binding, sae_config=model.cfg.to_dict(),
                trainer_config=trainer_config, installed=installed, optimizer=trainer.optimizer)
            restored = TrainingSAE.load_from_disk(resume_from, device=trainer_config.device, dtype=model.cfg.dtype)
            if _resume_sae_config(restored.cfg.to_dict()) != _resume_sae_config(model.cfg.to_dict()):
                raise ValueError("resume checkpoint native SAE configuration differs from the verified training protocol")
            model.load_state_dict(restored.state_dict(), strict=True)
            trainer.load_trainer_state(resume_from)
        trained = trainer.fit()
        inference_dir = output_dir / "inference"
        weights, cfg_path = trained.save_inference_model(inference_dir)
        (inference_dir / "vlmprobe_binding.json").write_text(json.dumps(binding, indent=2) + "\n")
        state_dir = output_dir / "training_state"
        trained.save_model(state_dir)
        trainer.save_trainer_state(state_dir)
        (state_dir / "vlmprobe_binding.json").write_text(json.dumps(binding, indent=2) + "\n")
        adapter = wrap(SAE.load_from_disk(inference_dir, device=trainer_config.device), binding=binding)
        validation = _evaluate(adapter, validation_source, max_validation_batches) if validation_source is not None else None
        report = {**protocol, "status": "complete", "training_steps": trainer.n_training_steps,
                  "training_samples": trainer.n_training_samples, "inference_architecture": adapter.config.architecture,
                  "validation": validation,
                  "artifacts": {"weights": str(weights), "config": str(cfg_path),
                                "binding": str(inference_dir / "vlmprobe_binding.json"),
                                "inference_dir": str(inference_dir), "training_state": str(state_dir), "protocol": str(protocol_path)}}
        protocol_path.write_text(json.dumps(report, indent=2, default=str, allow_nan=False) + "\n")
        (state_dir / "vlmprobe_training_protocol.json").write_text(json.dumps(
            {"schema": "vlmprobe-saelens-training-contract-v1", **report}, indent=2,
            default=str, allow_nan=False) + "\n")
        return report
    except Exception as error:
        protocol_path.write_text(json.dumps({**protocol, "status": "failed", "error": str(error)}, indent=2, default=str) + "\n")
        raise


@torch.no_grad()
def _evaluate(adapter, batches, maximum):
    """Evaluate final native-space inference on an independent finite source."""
    parameter = next(adapter.parameters())
    count, squared_error, squared_norm, l0 = 0, 0., 0., 0.
    active = torch.zeros(adapter.config.d_sae, device=parameter.device, dtype=torch.bool)
    for index, batch in enumerate(batches):
        if index >= maximum:
            break
        SAELensAdapter._check(batch, adapter.config.d_in, "validation input")
        if batch.ndim != 2:
            raise ValueError("validation source must yield [N,d_in] tensors")
        raw = batch.to(parameter)
        features = adapter.encode(raw)
        reconstruction = adapter.decode(features)
        squared_error += float((reconstruction.float() - raw.float()).square().sum())
        squared_norm += float(raw.float().square().sum())
        l0 += float((features != 0).sum())
        active |= (features != 0).any(0)
        count += raw.shape[0]
    if count == 0:
        raise ValueError("validation source contains no activation vectors")
    return {"samples": count, "mse_per_vector": squared_error / count,
            "relative_squared_error_to_zero": squared_error / squared_norm if squared_norm else None,
            "mean_l0": l0 / count, "fraction_unseen_features": float((~active).float().mean()),
            "selection": "final native trainer state; validation is evaluation only, not early stopping"}
