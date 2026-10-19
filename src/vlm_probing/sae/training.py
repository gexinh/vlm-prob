"""One native SAE training engine, independent of checkpoint source libraries."""
from __future__ import annotations

from collections.abc import Iterator
from copy import deepcopy
from dataclasses import asdict, dataclass
import hashlib
import json
import math
import os
from pathlib import Path
import time

import torch
from torch.utils.data import BatchSampler, DataLoader, RandomSampler, SequentialSampler, TensorDataset, default_collate


@dataclass(frozen=True)
class SAETrainingConfig:
    """An epoch budget, or exactly one optimizer-step/activation-vector budget.

    ``max_steps`` or ``max_vectors`` takes precedence over ``epochs``. Every
    dictionary uses this same Adam loop; architecture-specific objectives and
    post-step constraints belong to the dictionary implementation.
    """
    epochs: int = 10
    lr: float = 1e-3
    batch_size: int = 256
    patience: int = 3
    min_delta: float = 1e-4
    seed: int = 0
    normalization: str = "rms"
    max_steps: int | None = None
    max_vectors: int | None = None
    device: str = "cpu"
    resume: bool = True
    grad_clip: float = 5.
    progress_every: int = 20

    def __post_init__(self):
        for name in ("epochs", "batch_size", "patience", "progress_every"):
            if type(getattr(self, name)) is not int or getattr(self, name) < 1:
                raise ValueError(f"{name} must be a positive integer")
        for name in ("max_steps", "max_vectors"):
            if getattr(self, name) is not None and (type(getattr(self, name)) is not int or getattr(self, name) < 1):
                raise ValueError(f"{name} must be a positive integer or None")
        if self.max_steps is not None and self.max_vectors is not None:
            raise ValueError("choose one budget unit: max_steps or max_vectors")
        for name in ("lr", "min_delta", "grad_clip"):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0 or (name != "min_delta" and value == 0):
                raise ValueError(f"{name} must be finite and {'nonnegative' if name == 'min_delta' else 'positive'}")
        if type(self.seed) is not int or not 0 <= self.seed < 2 ** 63:
            raise ValueError("seed must be an integer in [0, 2**63)")
        if self.normalization not in {"rms", "none"}:
            raise ValueError("normalization must be 'rms' or 'none'")
        if type(self.resume) is not bool:
            raise ValueError("resume must be a boolean")
        if torch.device(self.device).type not in {"cpu", "cuda"}:
            raise ValueError("the native trainer currently supports cpu or cuda")

    @property
    def budget(self):
        if self.max_steps is not None:
            return "steps", self.max_steps
        if self.max_vectors is not None:
            return "vectors", self.max_vectors
        return "epochs", self.epochs


def _json(path, value):
    path = Path(path)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")
    os.replace(temporary, path)


def _torch(path, value):
    path = Path(path)
    temporary = path.with_name(path.name + ".tmp")
    torch.save(value, temporary)
    os.replace(temporary, path)


def _cpu(value):
    if isinstance(value, torch.Tensor):
        return value.detach().cpu().clone()
    if isinstance(value, dict):
        return {key: _cpu(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_cpu(item) for item in value]
    if isinstance(value, tuple):
        return tuple(_cpu(item) for item in value)
    return deepcopy(value)


def _batch(value, d_in):
    if isinstance(value, dict):
        value = value["activations"]
    if isinstance(value, (tuple, list)) and len(value) == 1:
        value = value[0]
    if (not isinstance(value, torch.Tensor) or value.ndim != 2 or value.shape[-1] != d_in
            or not value.is_floating_point() or not value.shape[0] or not torch.isfinite(value).all()):
        raise ValueError("SAE batches require finite floating activations[B,d_in] with B > 0")
    return value.detach()


def _loader_generator(source):
    return getattr(source, "generator", None)


def _source_tensor(source):
    if isinstance(source, torch.Tensor):
        return source
    if isinstance(source, DataLoader):
        sampler = source.sampler
        complete = (isinstance(sampler, SequentialSampler) or
                    isinstance(sampler, RandomSampler) and not sampler.replacement and sampler.num_samples == len(source.dataset))
        if (not complete or source.collate_fn is not default_collate
                or type(source.batch_sampler) is not BatchSampler
                or source.batch_sampler.sampler is not sampler):
            return None
        if isinstance(source.dataset, torch.Tensor):
            return source.dataset
        if isinstance(source.dataset, TensorDataset) and len(source.dataset.tensors) == 1:
            return source.dataset.tensors[0]
    return None


def _overlapping_storage(first, second):
    first, second = _source_tensor(first), _source_tensor(second)
    if first is None or second is None or first.device != second.device:
        return False
    if first.untyped_storage().data_ptr() != second.untyped_storage().data_ptr():
        return False
    if not first.is_contiguous() or not second.is_contiguous():
        return True  # Overlap cannot be excluded safely for arbitrary strided views.
    return max(first.data_ptr(), second.data_ptr()) < min(
        first.data_ptr() + first.numel() * first.element_size(),
        second.data_ptr() + second.numel() * second.element_size())


def _vectors(source, d_in):
    """Read a finite activation cache without advancing caller RNG or sampler."""
    if isinstance(source, torch.Tensor):
        return _batch(source, d_in).cpu().contiguous()
    if isinstance(source, DataLoader):
        if source.drop_last:
            raise ValueError("activation cache loaders must use drop_last=False")
        tensor = _source_tensor(source)
        if tensor is not None:
            return _batch(tensor, d_in).cpu().contiguous()
    if isinstance(source, Iterator):
        raise ValueError("provide a tensor or finite re-iterable activation cache, not a one-shot/infinite iterator")
    candidates = [_loader_generator(source), getattr(getattr(source, "sampler", None), "generator", None)]
    generators = {id(item): item for item in candidates if item is not None}
    saved = {key: item.get_state() for key, item in generators.items()}
    try:
        with torch.random.fork_rng(devices=[]):
            chunks = [_batch(item, d_in).cpu().contiguous() for item in source]
    finally:
        for key, state in saved.items():
            generators[key].set_state(state)
    if not chunks:
        raise ValueError("SAE activation cache is empty")
    if len({chunk.dtype for chunk in chunks}) != 1:
        raise ValueError("activation cache batches must have one explicit floating dtype")
    return torch.cat(chunks)


def _fingerprint(values):
    digest = hashlib.sha256()
    digest.update(json.dumps({"shape": list(values.shape), "dtype": str(values.dtype)}).encode())
    digest.update(values.contiguous().view(torch.uint8).numpy().tobytes())
    return digest.hexdigest()


def _provenance(value):
    if value is not None and not isinstance(value, dict):
        raise ValueError("SAE provenance must be a finite JSON dictionary")

    def json_default(item):
        if isinstance(item, Path):
            return str(item)
        raise TypeError("unsupported provenance object")

    try:
        result = json.loads(json.dumps(value or {}, allow_nan=False, default=json_default))
    except (TypeError, ValueError) as error:
        raise ValueError("SAE provenance must contain finite JSON metadata") from error
    pairs = [(result.get("train_ids"), result.get("validation_ids")),
             (result.get("train_groups"), result.get("validation_groups")),
             (result.get("train_image_ids"), result.get("validation_image_ids"))]
    groups = result.get("groups", {})
    if isinstance(groups, dict):
        pairs.append((groups.get("train"), groups.get("validation")))
    for train, validation in pairs:
        if train is not None and validation is not None:
            if set(map(str, train)) & set(map(str, validation)):
                raise ValueError("SAE provenance declares overlapping train/validation source IDs or groups")
    return result


@torch.no_grad()
def fit_normalization(train_batches, d_in):
    """Raw train-only position-weighted mean and scalar coordinate RMS."""
    raw = _vectors(train_batches, d_in)
    values = raw.double()
    return {"input_rms": float(values.square().mean().sqrt()),
            "mean": values.mean(0).to(torch.float64 if raw.dtype == torch.float64 else torch.float32),
            "positions": len(values)}


def _losses(model, values):
    losses = model.loss(values)
    required = ("loss", "reconstruction", "sparsity", "auxiliary")
    if not isinstance(losses, dict) or not all(key in losses for key in required):
        raise TypeError("native SAE loss must return loss/reconstruction/sparsity/auxiliary scalars")
    for key in required:
        if not isinstance(losses[key], torch.Tensor) or losses[key].numel() != 1 or not torch.isfinite(losses[key]):
            raise ValueError(f"SAE {key} objective must be a finite scalar tensor")
    return losses


def _activation_parameter(model):
    """Activation coordinates need not share a learned threshold's dtype."""
    parameter = getattr(model, "activation_parameter", None)
    return parameter if parameter is not None else next(model.parameters())


@torch.no_grad()
def evaluate_sae(model, batches, *, reference_mean=None):
    """Raw-unit MSE/FVU and signed nonzero activity, without model-stat updates."""
    parameter = _activation_parameter(model)
    values_all = _vectors(batches, model.config.d_in) if isinstance(batches, torch.Tensor) else None
    iterable = values_all.split(256) if values_all is not None else batches
    flags = [(module, module.training) for module in model.modules()]
    before = {name: value.detach().clone() for name, value in model.named_buffers()}
    count, squared_error, squared_reference, squared_input = 0, 0., 0., 0.
    summed_input = torch.zeros(model.config.d_in, dtype=torch.float64)
    frequencies = torch.zeros(model.config.d_sae, dtype=torch.long)
    totals = {key: 0. for key in ("loss", "reconstruction", "sparsity", "auxiliary")}
    reference = None if reference_mean is None else torch.as_tensor(reference_mean).to(parameter)
    if reference is not None and reference.shape != (model.config.d_in,):
        raise ValueError("FVU reference_mean must have shape [d_in]")
    model.eval()
    changed = []
    try:
        for batch in iterable:
            values = _batch(batch, model.config.d_in).to(parameter)
            reconstruction, features = model(values)
            losses = _losses(model, values)
            if reconstruction.shape != values.shape or features.shape != (len(values), model.config.d_sae):
                raise ValueError("SAE reconstruction and feature shapes do not match batch")
            if not torch.isfinite(reconstruction).all() or not torch.isfinite(features).all():
                raise ValueError("SAE evaluation produced nonfinite outputs")
            for key in totals:
                totals[key] += float(losses[key]) * len(values)
            squared_error += float((reconstruction.double() - values.double()).square().sum())
            if reference is not None:
                squared_reference += float((values.double() - reference.double()).square().sum())
            else:
                raw = values.double()
                summed_input += raw.sum(0).cpu()
                squared_input += float(raw.square().sum())
            frequencies += (features != 0).sum(0).cpu()
            count += len(values)
    finally:
        changed = [name for name, value in model.named_buffers() if name not in before or not torch.equal(value, before[name])]
        if changed:
            for name, value in model.named_buffers():
                if name in before:
                    value.copy_(before[name])
        for module, flag in flags:
            module.training = flag
    if changed:
        raise RuntimeError(f"SAE validation mutated training statistics: {changed}")
    if not count:
        raise ValueError("SAE evaluation iterable is empty")
    denominator = squared_reference if reference is not None else max(0., squared_input - float(summed_input.square().sum()) / count)
    return {**{key: value / count for key, value in totals.items()},
            "mse": squared_error / (count * model.config.d_in),
            "fvu": squared_error / denominator if denominator > 0 else None,
            "fvu_reference": "training_mean" if reference is not None else "evaluation_mean",
            "fvu_denominator_degenerate": denominator <= 0,
            "l0": float(frequencies.sum()) / count,
            "dead_feature_fraction": float((frequencies == 0).float().mean()),
            "dead_feature_definition": "zero nonzero activations in this evaluation split",
            "feature_frequencies": (frequencies.double() / count).tolist(), "positions": count}


def _post_step(model):
    hook = getattr(model, "post_optimizer_step_", None)
    if callable(hook):
        hook()
    else:
        model.normalize_decoder_()


def _restore_best(model, state, path):
    model.load_state_dict(state)
    model.is_fitted = True
    model.eval()
    model.save(path)


def _verify_optimizer_state(saved, optimizer):
    actual = saved.get("param_groups", [])
    expected = optimizer.state_dict()["param_groups"]
    if len(actual) != len(expected):
        raise ValueError("SAE resume optimizer groups differ from the declared configuration")
    for old, new in zip(actual, expected):
        if ({key: value for key, value in old.items() if key != "params"}
                != {key: value for key, value in new.items() if key != "params"}
                or len(old.get("params", [])) != len(new["params"])):
            raise ValueError("SAE resume optimizer state differs from the declared learning-rate/options configuration")


def fit_sae(model, train_vectors, validation_vectors, output_dir, *, training=None, provenance=None):
    """Fit every native SAE architecture with one deterministic training loop.

    Input is a finite raw-activation cache. Independent contents and optional
    source-group metadata are checked before training. Exact cached-vector
    permutations/cursors, optimizer, method buffers and RNG are checkpointed.
    """
    training = SAETrainingConfig() if training is None else training
    if not isinstance(training, SAETrainingConfig):
        raise TypeError("training must be SAETrainingConfig")
    if torch.is_inference_mode_enabled():
        raise ValueError("SAE training cannot run under torch.inference_mode()")
    if train_vectors is validation_vectors:
        raise ValueError("independent train and validation activation caches are required")
    if _overlapping_storage(train_vectors, validation_vectors):
        raise ValueError("independent train and validation caches must not overlap in tensor storage")
    train = _vectors(train_vectors, model.config.d_in)
    validation = _vectors(validation_vectors, model.config.d_in)
    train_hash, validation_hash = _fingerprint(train), _fingerprint(validation)
    if train_hash == validation_hash:
        raise ValueError("independent train/validation caches cannot contain the identical activation tensor")
    provenance = _provenance(provenance)
    device = torch.device(training.device)
    cuda_devices = [torch.cuda.current_device() if device.index is None else device.index] if device.type == "cuda" else []
    with torch.random.fork_rng(devices=cuda_devices):
        torch.random.default_generator.manual_seed(training.seed)
        for index in cuda_devices:
            torch.cuda.default_generators[index].manual_seed(training.seed)
        return _fit_cached(model, train, validation, output_dir, training, provenance,
                           {"train": train_hash, "validation": validation_hash}, cuda_devices)


def _fit_cached(model, train, validation, output_dir, training, provenance, fingerprints, cuda_devices):
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    state_path, best_path = directory / "training_state.pt", directory / "best.pt"
    unit, target = training.budget
    config = asdict(training)
    critical = {key: value for key, value in config.items() if key not in {"epochs", "max_steps", "max_vectors", "device", "resume", "progress_every"}}
    critical.update(model=asdict(model.config), model_dtype=str(_activation_parameter(model).dtype),
                    budget_unit=unit, engine_revision=1, torch_version=str(torch.__version__))
    model.to(device=training.device)
    parameter = _activation_parameter(model)
    optimizer = torch.optim.Adam(model.parameters(), lr=training.lr)
    generator = torch.Generator().manual_seed(training.seed)
    cursor, epoch, steps, vectors, stale = 0, 0, 0, 0, 0
    permutation = None
    totals = {key: 0. for key in ("loss", "reconstruction", "sparsity", "auxiliary")}
    epoch_vectors = 0
    resumed_rollback = 0
    rollback = None

    if state_path.exists():
        if not training.resume:
            raise ValueError("SAE output contains an earlier run; resume it or choose a new directory")
        saved = torch.load(state_path, map_location="cpu", weights_only=True)
        if saved.get("schema") != "vlmprobe-sae-training-v4":
            raise ValueError("resume requires a canonical v4 training state")
        if saved["configuration"] != critical or saved["binding"] != dict(model.binding) or saved["provenance"] != provenance or saved["fingerprints"] != fingerprints:
            raise ValueError("SAE resume configuration, binding, content fingerprints, or provenance does not match")
        if target < saved["budget_target"]:
            raise ValueError("resume budget cannot shrink below its previous target")
        if target > saved["budget_target"] and saved.get("budget_rollback") is not None:
            resumed_rollback = saved["vectors"] - saved["budget_rollback"]["vectors"]
            saved = saved["budget_rollback"]
        rollback = saved.get("budget_rollback")
        _verify_optimizer_state(saved["optimizer"], optimizer)
        model.load_state_dict(saved["model"])
        optimizer.load_state_dict(saved["optimizer"])
        generator.set_state(saved["permutation_rng"])
        torch.set_rng_state(saved["rng"])
        for index, value in zip(cuda_devices, saved.get("cuda_rng", [])):
            torch.cuda.set_rng_state(value, index)
        epoch, cursor, steps, vectors, stale = (saved[key] for key in ("epoch", "cursor", "steps", "vectors", "stale"))
        permutation, totals, epoch_vectors = saved["permutation"], saved["totals"], saved["epoch_vectors"]
        normalization, best_model, best, history = saved["normalization"], saved["best_model"], saved["best"], saved["history"]
        if (any(type(value) is not int or value < 0 for value in (epoch, cursor, steps, vectors, stale))
                or cursor > len(train) or vectors != epoch * len(train) + cursor or epoch_vectors != cursor):
            raise ValueError("SAE resume vector/epoch counters and minibatch cursor are inconsistent")
        if permutation is not None and (not isinstance(permutation, torch.Tensor)
                or permutation.dtype != torch.long or permutation.shape != (len(train),)
                or not torch.equal(permutation.sort().values, torch.arange(len(train)))):
            raise ValueError("SAE resume permutation is not a complete activation-cache ordering")
        if permutation is None and cursor != 0:
            raise ValueError("SAE resume cursor requires the saved activation-cache permutation")
    else:
        if best_path.exists():
            raise ValueError("SAE output contains an earlier best artifact; choose a new directory")
        normalization = fit_normalization(train, model.config.d_in)
        normalizer = getattr(model.config, "input_normalization", "scalar")
        scale = normalization["input_rms"] if training.normalization == "rms" and normalizer == "scalar" else 1.
        if scale <= 0:
            raise ValueError("RMS normalization requires nonzero training activations")
        normalization.update(scale=scale, method=training.normalization if normalizer == "scalar" else normalizer)
        model.set_normalization_(scale)
        model.initialize_bias_(normalization["mean"])
        initialize = getattr(model, "initialize_dictionary_", None)
        if callable(initialize):
            candidates = min(len(train), getattr(model.config, "archetypal_candidates", 128))
            initialize(train[:candidates].to(parameter))
        calibrate = getattr(model, "calibrate_", None)
        if callable(calibrate):
            calibrate(train[:training.batch_size].to(parameter))
        _post_step(model)
        initial = evaluate_sae(model, list(validation.split(training.batch_size)), reference_mean=normalization["mean"])
        best, best_model = initial["loss"], _cpu(model.state_dict())
        history = {"configuration": critical, "binding": dict(model.binding), "provenance": provenance,
                   "fingerprints": fingerprints, "normalization": {**normalization, "mean": normalization["mean"].tolist(), "fit_split": "train"},
                   "initial_validation": initial, "best_epoch": 0, "epochs": []}

    def snapshot(include_rollback=True):
        return {"schema": "vlmprobe-sae-training-v4", "configuration": critical, "binding": dict(model.binding),
                "provenance": provenance, "fingerprints": fingerprints, "budget_target": target,
                "model": _cpu(model.state_dict()), "optimizer": _cpu(optimizer.state_dict()),
                "normalization": _cpu(normalization), "best_model": _cpu(best_model), "best": best,
                "history": deepcopy(history), "epoch": epoch, "cursor": cursor, "steps": steps,
                "vectors": vectors, "stale": stale, "permutation": _cpu(permutation),
                "totals": dict(totals), "epoch_vectors": epoch_vectors, "permutation_rng": generator.get_state(),
                "rng": torch.get_rng_state(), "cuda_rng": [torch.cuda.get_rng_state(index) for index in cuda_devices],
                "budget_rollback": rollback if include_rollback else None}

    def reached():
        return (epoch >= target if unit == "epochs" else steps >= target if unit == "steps" else vectors >= target)

    started = time.monotonic()
    _torch(state_path, snapshot())
    # Keep a usable artifact even before the first complete optimizer update.
    original = _cpu(model.state_dict())
    _restore_best(model, best_model, best_path)
    model.load_state_dict(original)
    try:
        while not reached() and stale < training.patience:
            if permutation is None:
                permutation = torch.randperm(len(train), generator=generator)
                cursor, epoch_vectors = 0, 0
                totals = {key: 0. for key in totals}
            model.train()
            length = min(training.batch_size, len(train) - cursor)
            if unit == "vectors" and target - vectors < length:
                rollback = snapshot(include_rollback=False)
                length = target - vectors
            values = train[permutation[cursor:cursor + length]].to(parameter)
            optimizer.zero_grad(set_to_none=True)
            losses = _losses(model, values)
            losses["loss"].backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), training.grad_clip, error_if_nonfinite=True)
            optimizer.step()
            _post_step(model)
            cursor, steps, vectors = cursor + length, steps + 1, vectors + length
            epoch_vectors += length
            for key in totals:
                totals[key] += float(losses[key].detach()) * length
            if cursor == len(train):
                metrics = evaluate_sae(model, list(validation.split(training.batch_size)), reference_mean=normalization["mean"])
                epoch += 1
                row = {"epoch": epoch, "train": {key: value / epoch_vectors for key, value in totals.items()},
                       "train_positions": epoch_vectors, "validation": metrics, "steps": steps, "vectors": vectors}
                history["epochs"].append(row)
                if metrics["loss"] < best - training.min_delta:
                    best, stale, history["best_epoch"] = metrics["loss"], 0, epoch
                    best_model = _cpu(model.state_dict())
                else:
                    stale += 1
                permutation, cursor, epoch_vectors = None, 0, 0
                totals = {key: 0. for key in totals}
                _torch(state_path, snapshot())
                _json(directory / "history.json", history)
            if steps % training.progress_every == 0:
                _torch(state_path, snapshot())
                _json(directory / "status.json", {"state": "training", "epoch": epoch, "steps": steps,
                    "vectors": vectors, "budget_unit": unit, "budget_target": target,
                    "elapsed_seconds": time.monotonic() - started})
        _torch(state_path, snapshot())
        last_model = _cpu(model.state_dict())
        terminal = evaluate_sae(model, list(validation.split(training.batch_size)), reference_mean=normalization["mean"])
        # A budget can stop inside an epoch. Its descriptive terminal validation
        # is provisional: it cannot alter persistent epoch-based early stopping
        # or selection when a later call extends this run's budget.
        selected_model, selected_loss = (last_model, terminal["loss"]) if terminal["loss"] < best else (best_model, best)
        _restore_best(model, selected_model, best_path)
        final_validation = evaluate_sae(model, list(validation.split(training.batch_size)), reference_mean=normalization["mean"])
        final_train = evaluate_sae(model, list(train.split(training.batch_size)), reference_mean=normalization["mean"])
        report = {**history, "status": "complete", "completed_epochs": epoch, "completed_steps": steps,
                  "training_vectors": vectors, "best_validation_loss": selected_loss,
                  "checkpoint": str(best_path), "training_state": str(state_path),
                  "budget": {"unit": unit, "target": target}, "early_stopped": stale >= training.patience,
                  "terminal_validation": terminal, "validation": final_validation, "train": final_train,
                  "resume_rolled_back_partial_vectors": resumed_rollback,
                  "normalization": {**history["normalization"], "scale": normalization["scale"]}}
        _json(directory / "history.json", report)
        _json(directory / "status.json", {"state": "complete", "epoch": epoch, "steps": steps,
            "vectors": vectors, "best_validation_loss": selected_loss, "checkpoint": str(best_path)})
        return report
    except Exception as error:
        _json(directory / "status.json", {"state": "failed", "error": str(error), "epoch": epoch,
            "steps": steps, "vectors": vectors, "resume_state": str(state_path)})
        raise


def train_sae(model, train_batches, validation_batches, checkpoint_dir, *,
              epochs=10, lr=1e-3, patience=3, min_delta=1e-4, seed=0,
              resume=True, provenance=None, progress_every=20):
    """Legacy batch-input spelling; delegates to the sole canonical engine."""
    batch_size = getattr(train_batches, "batch_size", None)
    if batch_size is None and isinstance(train_batches, (list, tuple)) and train_batches:
        batch_size = len(_batch(train_batches[0], model.config.d_in))
    configuration = SAETrainingConfig(epochs=epochs, lr=lr, batch_size=batch_size or 256,
        patience=patience, min_delta=min_delta, seed=seed, resume=resume,
        device=str(_activation_parameter(model).device), progress_every=progress_every)
    return fit_sae(model, train_batches, validation_batches, checkpoint_dir,
                   training=configuration, provenance=provenance)
