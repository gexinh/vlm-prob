"""Optional, native Overcomplete SAE training and pointwise inference.

No upstream code or weights are bundled.  In particular, Overcomplete's vision
backbone loaders are not a registry of pretrained sparse autoencoders.
"""
from __future__ import annotations

from functools import partial
from importlib import import_module
from collections.abc import Iterator
import hashlib
import json
import math
import os
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import torch
from torch import Tensor, nn
from torch.utils.data import DataLoader, TensorDataset

from ..models import validate_sae_binding


ARCHITECTURES = {
    "relu": "SAE", "topk": "TopKSAE", "batchtopk": "BatchTopKSAE",
    "jumprelu": "JumpSAE", "archetypal_topk": "RATopKSAE",
    "archetypal_jumprelu": "RAJumpSAE",
}
SOURCE = "https://github.com/KempnerInstitute/overcomplete"
SCHEMA = "vlmprobe-overcomplete-sae-v1"


def backend_info() -> dict:
    return {"name": "overcomplete", "package": "overcomplete", "version": ">=0.3,<0.4",
            "license": "MIT", "source": SOURCE,
            "audited_revision": "a1781af49c6e4bbfdbfd763b9757bcf6c5dd6403",
            "architectures": list(ARCHITECTURES), "modalities": ["vision", "language", "multimodal"],
            "pretrained_scope": "Caller-loaded SAE weights; upstream has no central pretrained SAE registry. Pretrained vision backbones are not SAEs.",
            "training_scope": "Native pointwise SAE, TopK, BatchTopK, JumpReLU, relaxed-archetypal TopK/JumpReLU; native train_sae and explicit upstream objective.",
            "scope": "Audited pointwise encoders only; convolutional and attention encoders require geometry-aware adapters. NMF/PCA/ICA are not SAEs."}


def list_pretrained() -> list:
    """No fabricated registry: upstream supplies training tools, not SAE releases."""
    return []


def _upstream():
    try:
        module = import_module("overcomplete")
    except ImportError as error:
        raise ImportError("Install vlmprobe[overcomplete] in an environment with Python <3.13 to use this optional backend") from error
    except AttributeError as error:
        if "get_cmap" in str(error):
            raise ImportError("Overcomplete 0.3 requires matplotlib>=3.7,<3.9; use the overcomplete optional extra or a separate environment") from error
        raise
    installed = getattr(module, "__version__", "")
    if not installed.startswith("0.3."):
        raise ValueError(f"Overcomplete backend was audited for 0.3.x, got {installed!r}")
    return module, import_module("overcomplete.sae")


def _json(value, name):
    try:
        return json.loads(json.dumps(value, allow_nan=False))
    except (ValueError, TypeError) as error:
        raise ValueError(f"{name} must contain finite JSON values") from error


def _atomic_save(value, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    torch.save(value, temporary)
    os.replace(temporary, path)


def _write_json(value, path):
    path = Path(path)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")
    os.replace(temporary, path)


class OvercompleteAdapter(nn.Module):
    """Bridge native ``encode -> (pre_codes, codes)`` to sparse feature IO.

    An explicit affine preprocessing contract is inverted by ``decode``:
    ``u=(raw-input_mean)/input_scale``. Identity preprocessing is the default;
    no normalization is fitted or guessed. A loaded, trained model must be
    declared ``is_fitted=True`` by its caller. Width alone proves no model/hook
    compatibility; the exact VLMProbe binding is always required.
    """

    def __init__(self, sae: nn.Module, binding: dict[str, Any], *,
                 expected_binding=None, source_metadata=None, input_mean=0.,
                 input_scale=1., is_fitted=True, init_config=None):
        super().__init__()
        upstream, classes = _upstream()
        architecture = next((key for key, name in ARCHITECTURES.items()
                             if type(sae) is getattr(classes, name)), None)
        if architecture is None:
            raise TypeError("wrap a supported native Overcomplete SAE; optimization factorizations and experimental pursuit/quantized models are not supported")
        modules = import_module("overcomplete.sae.modules")
        pointwise = (modules.MLPEncoder, modules.IdentityEncoder, modules.TieableEncoder)
        if not isinstance(sae.encoder, pointwise):
            raise ValueError("only audited pointwise MLP/identity/tied encoders are supported; attention and convolutional encoders require preserved image geometry")
        self.binding = validate_sae_binding(binding)
        if expected_binding is not None and validate_sae_binding(expected_binding) != self.binding:
            raise ValueError("Overcomplete binding differs from expected model/hook/preprocessing identities")
        d_in, d_sae = getattr(sae.dictionary, "in_dimensions", None), getattr(sae, "nb_concepts", None)
        if any(type(size) is not int or size < 1 for size in (d_in, d_sae)):
            raise ValueError("native dictionary must declare positive activation and feature widths")
        self.sae = sae
        self.config = SimpleNamespace(d_in=d_in, d_sae=d_sae, architecture="overcomplete:" + architecture)
        parameter = next(sae.parameters())
        mean = torch.as_tensor(input_mean, device=parameter.device, dtype=parameter.dtype)
        scale = torch.as_tensor(input_scale, device=parameter.device, dtype=parameter.dtype)
        if mean.shape not in (torch.Size([]), torch.Size([d_in])) or scale.shape not in (torch.Size([]), torch.Size([d_in])):
            raise ValueError("input_mean and input_scale must be scalars or [d_in] vectors")
        if not torch.isfinite(mean).all() or not torch.isfinite(scale).all() or (scale <= 0).any():
            raise ValueError("preprocessing must be finite with positive input_scale")
        self.register_buffer("input_mean", mean.clone())
        self.register_buffer("input_scale", scale.clone())
        if type(is_fitted) is not bool:
            raise ValueError("is_fitted must explicitly be boolean")
        self.is_fitted = is_fitted
        if architecture == "batchtopk" and self.is_fitted and getattr(sae, "running_threshold", None) is None:
            raise ValueError("a fitted BatchTopK SAE requires its trained running_threshold; upstream state_dict alone omits it")
        self.init_config = _json(init_config, "init_config") if init_config is not None else None
        if self.init_config is not None and any(self.init_config.get(key) != value for key, value in
                (("architecture", architecture), ("d_in", d_in), ("d_sae", d_sae))):
            raise ValueError("init_config must describe this exact native architecture and dimensions")
        self.source_metadata = {**_json(source_metadata or {}, "source_metadata"),
            "backend": "overcomplete", "backend_version": upstream.__version__, "architecture": architecture,
            "source": SOURCE, "license": "MIT", "preprocessing": "explicit (raw-input_mean)/input_scale; decoder returns raw coordinates",
            "batchtopk_semantics": "top_k is a global count across the native training batch; evaluation uses saved running_threshold"}
        # Upstream dictionaries fuse a tensor when entering eval; initialize it
        # before inference instead of assuming that state_dict contains it.
        if self.is_fitted:
            self.train(False)

    def _apply(self, function, recurse=True):
        super()._apply(function, recurse=recurse)
        # These native 0.3 values are plain tensor attributes, not buffers.
        # Preserve them when device/dtype changes, including fused dictionaries.
        for module in self.sae.modules():
            for name in ("running_threshold", "bandwidth", "_fused_dictionary"):
                value = getattr(module, name, None)
                if isinstance(value, Tensor):
                    setattr(module, name, function(value))
            if hasattr(module, "device"):
                module.device = str(self.input_scale.device)
        return self

    def train(self, mode=True):
        if not isinstance(mode, bool):
            raise ValueError("training mode must be boolean")
        return super().train(mode)

    def _input(self, value, width, label):
        if not isinstance(value, Tensor) or not value.is_floating_point() or value.ndim < 1 or value.shape[-1] != width:
            raise ValueError(f"{label} must be floating [...,{width}]")
        if value.numel() == 0 or not torch.isfinite(value).all():
            raise ValueError(f"{label} must be nonempty and finite")
        return value.to(self.input_scale)

    def encode(self, raw):
        raw = self._input(raw, self.config.d_in, "activations")
        if not self.training and self.source_metadata["architecture"] == "batchtopk" and self.sae.running_threshold is None:
            raise ValueError("BatchTopK evaluation requires a training running_threshold")
        normalized = (raw - self.input_mean) / self.input_scale
        _, features = self.sae.encode(normalized.reshape(-1, self.config.d_in))
        return features.reshape(*raw.shape[:-1], self.config.d_sae)

    def decode(self, features):
        features = self._input(features, self.config.d_sae, "features")
        decoded = self.sae.decode(features.reshape(-1, self.config.d_sae))
        return decoded.reshape(*features.shape[:-1], self.config.d_in) * self.input_scale + self.input_mean

    def forward(self, raw):
        features = self.encode(raw)
        return self.decode(features), features

    def save(self, path):
        if self.init_config is None:
            raise ValueError("portable saving needs an explicit native init_config; use create() or supply the constructor configuration when wrapping")
        state = {key: value.detach().cpu() for key, value in self.state_dict().items()}
        if any(not torch.isfinite(value).all() for value in state.values()):
            raise ValueError("cannot save nonfinite Overcomplete state")
        auxiliary = {name: getattr(self.sae, name).detach().cpu()
                     for name in ("running_threshold", "bandwidth")
                     if isinstance(getattr(self.sae, name, None), Tensor)}
        fused = getattr(self.sae.dictionary, "_fused_dictionary", None)
        if isinstance(fused, Tensor) and not self.sae.dictionary.training:
            # Save the exact eval composition. Re-entering native train->eval
            # would project dictionary weights an additional time on resume.
            auxiliary["fused_dictionary"] = fused.detach().cpu()
        if any(not torch.isfinite(value).all() for value in auxiliary.values()):
            raise ValueError("cannot save nonfinite native auxiliary state")
        _atomic_save({"schema": SCHEMA, "binding": self.binding, "config": self.init_config,
                      "state_dict": state, "auxiliary_tensors": auxiliary,
                      "is_fitted": self.is_fitted, "source_metadata": self.source_metadata,
                      "dtype": str(self.input_scale.dtype).removeprefix("torch.")}, path)


def wrap(sae, *, binding, **kwargs):
    return OvercompleteAdapter(sae, binding, **kwargs)


def create(architecture, d_in, d_sae, *, binding, device="cpu", input_mean=0., input_scale=1., **kwargs):
    """Construct the actual upstream architecture, keeping native hyperparameters.

    ``points`` for archetypal models must come from TRAIN activations only.
    Native parameters such as ``top_k``, ``bandwidth``, ``kernel``, ``delta`` and
    ``dictionary_params`` are passed through; no architecture is reimplemented.
    """
    if architecture not in ARCHITECTURES:
        raise ValueError(f"architecture must be one of {list(ARCHITECTURES)}")
    binding = validate_sae_binding(binding)
    if any(type(size) is not int or size < 1 for size in (d_in, d_sae)):
        raise ValueError("d_in and d_sae must be positive integers")
    if "top_k" in kwargs and (type(kwargs["top_k"]) is not int or not 1 <= kwargs["top_k"] <= d_sae):
        raise ValueError("top_k must be a positive integer no larger than d_sae")
    if kwargs.get("encoder_module") not in (None, "linear", "mlp_ln_1", "mlp_ln_3", "mlp_bn_1", "mlp_bn_3", "identity"):
        raise ValueError("create supports named pointwise encoders; use an explicit audited wrapper for custom modules")
    constructor = dict(kwargs)
    points = constructor.pop("points", None)
    config = {"architecture": architecture, "d_in": d_in, "d_sae": d_sae,
              "kwargs": _json(constructor, "native constructor kwargs")}
    if architecture.startswith("archetypal_"):
        if not isinstance(points, Tensor) or points.ndim != 2 or points.shape[1] != d_in or not points.is_floating_point() or not torch.isfinite(points).all():
            raise ValueError("archetypal points must be finite floating TRAIN activations [candidates,d_in]")
        if points.shape[0] < 1:
            raise ValueError("at least one archetypal candidate is required")
        kwargs["points"] = points.to(device)
        config["nb_candidates"] = points.shape[0]
    elif points is not None:
        raise ValueError("points is only valid for archetypal architectures")
    else:
        kwargs.pop("points", None)
    _, classes = _upstream()
    native = getattr(classes, ARCHITECTURES[architecture])(d_in, d_sae, device=device, **kwargs)
    return OvercompleteAdapter(native, binding, input_mean=input_mean, input_scale=input_scale,
                               is_fitted=False, init_config=config)


def load(path=None, *, binding, checkpoint=None, device="cpu", expected_binding=None):
    """Load this bridge's tensor-only artifact; never unpickle upstream objects."""
    if (path is None) == (checkpoint is None):
        raise ValueError("provide exactly one path or checkpoint")
    binding = validate_sae_binding(binding)
    if expected_binding is not None and validate_sae_binding(expected_binding) != binding:
        raise ValueError("expected binding differs")
    artifact = torch.load(path if path is not None else checkpoint, map_location="cpu", weights_only=True)
    if artifact.get("schema") != SCHEMA:
        raise ValueError("not a VLMProbe Overcomplete tensor-only artifact; wrap a trusted, explicitly loaded native model instead")
    if validate_sae_binding(artifact.get("binding")) != binding:
        raise ValueError("checkpoint binding differs from expected native identities")
    config = artifact["config"]
    kwargs = dict(config["kwargs"])
    if config["architecture"].startswith("archetypal_"):
        # Candidate values are restored from dictionary.C in state_dict.
        kwargs["points"] = torch.zeros(config["nb_candidates"], config["d_in"])
    state = artifact["state_dict"]
    if any(not isinstance(value, Tensor) or not torch.isfinite(value).all() for value in state.values()):
        raise ValueError("checkpoint has nonfinite or invalid tensor state")
    adapter = create(config["architecture"], config["d_in"], config["d_sae"], binding=binding,
                     input_mean=state["input_mean"], input_scale=state["input_scale"], **kwargs)
    dtype = getattr(torch, artifact.get("dtype", "float32"), None)
    if dtype not in (torch.float16, torch.bfloat16, torch.float32, torch.float64):
        raise ValueError("unsupported checkpoint dtype")
    adapter.to(dtype=dtype)
    adapter.load_state_dict(state, strict=True)
    for name, value in artifact.get("auxiliary_tensors", {}).items():
        if name not in {"running_threshold", "bandwidth", "fused_dictionary"} or not isinstance(value, Tensor) or not torch.isfinite(value).all():
            raise ValueError("invalid auxiliary tensor state")
        if name == "fused_dictionary":
            if tuple(value.shape) != (config["d_sae"], config["d_in"]):
                raise ValueError("invalid fused dictionary shape")
            adapter.sae.dictionary._fused_dictionary = value.to(adapter.input_scale)
            adapter.sae.dictionary.training = False
        else:
            if value.numel() != 1 or (name == "bandwidth" and value.item() <= 0):
                raise ValueError("native threshold/bandwidth must be scalar, with positive bandwidth")
            setattr(adapter.sae, name, value.to(adapter.input_scale))
    adapter.is_fitted = bool(artifact["is_fitted"])
    if config["architecture"] == "batchtopk" and adapter.is_fitted and adapter.sae.running_threshold is None:
        raise ValueError("fitted BatchTopK checkpoint is missing running_threshold")
    adapter.source_metadata = _json(artifact["source_metadata"], "source_metadata")
    adapter.to(device)
    if adapter.is_fitted:
        adapter.eval()
    return adapter


def _batches(data):
    if isinstance(data, Tensor):
        yield data
    else:
        yield from data


def _batch(batch):
    if isinstance(batch, dict):
        batch = batch.get("activations", batch.get("data"))
    elif isinstance(batch, (tuple, list)):
        batch = batch[0]
    if not isinstance(batch, Tensor) or batch.ndim != 2 or not batch.is_floating_point() or not batch.numel() or not torch.isfinite(batch).all():
        raise ValueError("training/validation batches must contain finite floating [positions,d_in] activations")
    return batch


def _criterion(name, coefficient):
    losses = import_module("overcomplete.sae.losses")
    if name == "mse":
        return lambda x, reconstruction, pre, z, dictionary: (x - reconstruction).square().mean()
    if name == "mse_l1":
        return partial(losses.mse_l1, penalty=coefficient)
    if name == "topk_auxiliary":
        return partial(losses.top_k_auxiliary_loss, penalty=coefficient)
    raise ValueError("objective must be mse, mse_l1, or topk_auxiliary")


def _data_fingerprint(data):
    """Hash stored tensor values without constructing a DataLoader iterator.

    Arbitrary datasets/iterables remain the caller's provenance responsibility;
    reading them here could execute transforms, consume RNG or exhaust streams.
    """
    loader = data if isinstance(data, DataLoader) else None
    dataset = loader.dataset if loader is not None else data
    if isinstance(dataset, Tensor):
        tensors = (dataset,)
    elif isinstance(dataset, TensorDataset):
        tensors = dataset.tensors
    else:
        return {"automatic": False,
                "scope": "caller-supplied provenance required for content identity; arbitrary dataset/iterable was not read"}
    records = []
    for tensor in tensors:
        if tensor.layout != torch.strided:
            raise ValueError("automatic data fingerprinting requires dense strided tensors")
        value = tensor.detach().cpu().contiguous()
        metadata = {"shape": list(value.shape), "dtype": str(value.dtype)}
        digest = hashlib.sha256(json.dumps(metadata, sort_keys=True).encode())
        digest.update(memoryview(value.reshape(-1).view(torch.uint8).numpy()))
        records.append({**metadata, "sha256": digest.hexdigest()})
    result = {"automatic": True, "kind": "TensorDataset" if isinstance(dataset, TensorDataset) else "Tensor",
              "tensors": records,
              "scope": "stored tensor shape/dtype/bytes; arbitrary dataset transforms are not inferred"}
    if loader is not None:
        result["loader"] = {"batch_size": loader.batch_size, "drop_last": loader.drop_last,
                            "sampler": type(loader.sampler).__qualname__}
    return result


def train(*, model, train_data, validation_data, output_dir, binding, nb_epochs=20,
          lr=1e-3, objective=None, l1_coefficient=.01, auxiliary_coefficient=.1,
          clip_grad=1., patience=5, min_delta=0., seed=0, resume=True,
          provenance=None, monitoring=0, device=None) -> dict:
    """Train via upstream ``train_sae`` with held-out selection and safe resume.

    The optimizer is constructed once and persists across native one-epoch calls.
    Losses retain Overcomplete's coordinate-mean MSE and upstream L1 reduction.
    JumpReLU defaults to its native generic L1 objective, not a claimed replica
    of the JumpReLU paper's L0 training recipe. Data must be re-iterable; fit any
    preprocessing/candidate archetypes using the training split only.
    """
    if not isinstance(model, OvercompleteAdapter):
        raise TypeError("model must be an OvercompleteAdapter returned by create/wrap")
    if validate_sae_binding(binding) != model.binding:
        raise ValueError("training binding differs from model binding")
    if train_data is validation_data:
        raise ValueError("training and validation must be independent objects/splits")
    if any(type(value) is not int or value < 1 for value in (nb_epochs, patience)):
        raise ValueError("nb_epochs and patience must be positive integers")
    if type(seed) is not int or not 0 <= seed < 2**63:
        raise ValueError("seed must be a nonnegative integer")
    if not math.isfinite(lr) or lr <= 0 or any(not math.isfinite(value) or value < 0 for value in (l1_coefficient, auxiliary_coefficient, clip_grad, min_delta)):
        raise ValueError("training coefficients must be finite and nonnegative, with positive lr")
    for name, value in (("train_data", train_data), ("validation_data", validation_data)):
        if isinstance(value, Iterator):
            raise ValueError(f"{name} must be re-iterable, not a one-shot iterator")
    fingerprints = {"train": _data_fingerprint(train_data),
                    "validation": _data_fingerprint(validation_data)}
    if (all(item["automatic"] for item in fingerprints.values())
            and fingerprints["train"]["tensors"][0] == fingerprints["validation"]["tensors"][0]):
        raise ValueError("training and validation contain identical activation tensors; use independent splits")
    architecture = model.source_metadata["architecture"]
    objective = objective or ("mse" if "topk" in architecture else "mse_l1")
    criterion = _criterion(objective, auxiliary_coefficient if objective == "topk_auxiliary" else l1_coefficient)
    protocol = _json({"objective": objective, "lr": lr, "l1_coefficient": l1_coefficient,
        "auxiliary_coefficient": auxiliary_coefficient, "clip_grad": clip_grad,
        "patience": patience, "min_delta": min_delta, "seed": seed,
        "binding": binding, "constructor": model.init_config,
        "input_mean": model.input_mean.detach().cpu().tolist(),
        "input_scale": model.input_scale.detach().cpu().tolist(),
        "data_fingerprints": fingerprints,
        "provenance": provenance or {}}, "training protocol")
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    if device is not None:
        model.to(device)
    device = model.input_scale.device
    optimizer = torch.optim.Adam(model.sae.parameters(), lr=lr)
    native_train = import_module("overcomplete.sae.train").train_sae

    class NormalizedBatches:
        count = 0

        def __iter__(self):
            for item in _batches(train_data):
                values = model._input(_batch(item), model.config.d_in, "training activations")
                self.count += values.shape[0]
                yield (values - model.input_mean) / model.input_scale

    @torch.no_grad()
    def validate():
        model.eval()
        total, count, mse, l0 = 0., 0, 0., 0.
        for item in _batches(validation_data):
            raw = model._input(_batch(item), model.config.d_in, "validation activations")
            normalized = (raw - model.input_mean) / model.input_scale
            pre, features = model.sae.encode(normalized)
            reconstruction = model.sae.decode(features)
            loss = criterion(normalized, reconstruction, pre, features, model.sae.get_dictionary())
            if not torch.isfinite(loss):
                raise ValueError("nonfinite validation objective")
            size = raw.shape[0]
            total += float(loss) * size
            mse += float((reconstruction * model.input_scale + model.input_mean - raw).square().mean()) * size
            l0 += float((features != 0).sum(-1).float().mean()) * size
            count += size
        if not count:
            raise ValueError("validation data is empty")
        return {"objective": total / count, "mse": mse / count, "l0": l0 / count, "positions": count}

    history, start, best, bad = [], 0, float("inf"), 0
    training_path = output_dir / "training_state.pt"
    torch.manual_seed(seed)
    if resume and training_path.exists():
        saved = torch.load(training_path, map_location="cpu", weights_only=True)
        if saved.get("schema") != SCHEMA + "-training" or saved["protocol"] != protocol:
            raise ValueError("resume protocol, data provenance or model binding differs")
        restored = load(output_dir / "latest.pt", binding=binding, device=device)
        model.load_state_dict(restored.state_dict())
        for name in ("running_threshold", "bandwidth"):
            if hasattr(restored.sae, name):
                setattr(model.sae, name, getattr(restored.sae, name))
        model.sae.dictionary._fused_dictionary = restored.sae.dictionary._fused_dictionary
        model.sae.dictionary.training = restored.sae.dictionary.training
        model.is_fitted = restored.is_fitted
        optimizer.load_state_dict(saved["optimizer"])
        torch.set_rng_state(saved["rng_state"])
        if device.type == "cuda" and "cuda_rng_state" in saved:
            torch.cuda.set_rng_state(saved["cuda_rng_state"], device)
        for key, data in (("train", train_data), ("validation", validation_data)):
            generator = getattr(data, "generator", None)
            if generator is not None and key in saved.get("loader_rng", {}):
                generator.set_state(saved["loader_rng"][key])
        history, start, best, bad = saved["history"], saved["epoch"], saved["best"], saved["bad_epochs"]
    try:
        for epoch in range(start, nb_epochs):
            if bad >= patience:
                break
            _write_json({"state": "training", "epoch": epoch + 1, "target_epochs": nb_epochs}, output_dir / "status.json")
            model.train(True)
            native_batches = NormalizedBatches()
            logs = native_train(model.sae, native_batches, criterion, optimizer,
                                nb_epochs=1, clip_grad=clip_grad, monitoring=monitoring, device=str(device))
            # The upstream trainer tolerates empty loaders. This bridge does not.
            if native_batches.count == 0:
                raise ValueError("training data is empty")
            model.is_fitted = True
            metrics = validate()
            row = {"epoch": epoch + 1, "validation": metrics,
                   "native_logs": {key: [float(value) for value in values]
                                   for key, values in logs.items() if all(isinstance(value, (float, int)) for value in values)}}
            history.append(row)
            if metrics["objective"] < best - min_delta:
                best, bad = metrics["objective"], 0
                model.save(output_dir / "best.pt")
            else:
                bad += 1
            model.save(output_dir / "latest.pt")
            loader_rng = {key: data.generator.get_state() for key, data in (("train", train_data), ("validation", validation_data))
                          if getattr(data, "generator", None) is not None}
            _atomic_save({"schema": SCHEMA + "-training", "protocol": protocol,
                "epoch": epoch + 1, "history": history, "best": best, "bad_epochs": bad,
                "optimizer": optimizer.state_dict(), "rng_state": torch.get_rng_state(),
                "loader_rng": loader_rng,
                **({"cuda_rng_state": torch.cuda.get_rng_state(device)} if device.type == "cuda" else {})}, training_path)
            _write_json(history, output_dir / "history.json")
        if not (output_dir / "best.pt").exists():
            raise ValueError("training produced no finite held-out checkpoint")
        restored = load(output_dir / "best.pt", binding=binding, device=device)
        model.load_state_dict(restored.state_dict())
        for name in ("running_threshold", "bandwidth"):
            if hasattr(restored.sae, name):
                setattr(model.sae, name, getattr(restored.sae, name))
        model.sae.dictionary._fused_dictionary = restored.sae.dictionary._fused_dictionary
        model.sae.dictionary.training = restored.sae.dictionary.training
        model.is_fitted = True
        model.eval()
        report = {"state": "complete", "backend": "overcomplete", "epochs": len(history),
                  "best_validation_objective": best, "validation": validate(),
                  "checkpoint": str(output_dir / "best.pt"), "protocol": protocol,
                  "loss_units": "upstream coordinate-mean MSE; upstream penalty reduction; preprocessing explicitly saved",
                  "batchtopk_semantics": model.source_metadata["batchtopk_semantics"],
                  "training_implementation": "overcomplete.sae.train.train_sae with one persistent Adam optimizer"}
        _write_json(report, output_dir / "metrics.json")
        _write_json({"state": "complete", "epochs": len(history)}, output_dir / "status.json")
        return report
    except Exception as error:
        _write_json({"state": "failed", "error": str(error), "epochs": len(history)}, output_dir / "status.json")
        raise
