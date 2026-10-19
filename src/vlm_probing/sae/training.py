"""Persistent SAE training with train-only normalization and held-out metrics."""
from __future__ import annotations

from dataclasses import asdict
import json
import os
from pathlib import Path
import time

import torch


def _json(path: Path, value):
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")
    os.replace(temporary, path)


def _torch(path: Path, value):
    temporary = path.with_name(path.name + ".tmp")
    torch.save(value, temporary)
    os.replace(temporary, path)


def _save_model(model, path: Path):
    temporary = path.with_name(path.name + ".tmp")
    model.save(temporary)
    os.replace(temporary, path)


def _batch(value, d_in):
    value = value["activations"] if isinstance(value, dict) else value
    if (not isinstance(value, torch.Tensor) or value.ndim != 2 or value.shape[-1] != d_in
            or not value.is_floating_point() or not value.shape[0] or not torch.isfinite(value).all()):
        raise ValueError("SAE batches require finite floating activations[B,d_in] with B > 0")
    return value.detach()


@torch.no_grad()
def fit_normalization(train_batches, d_in: int):
    """Compute raw-coordinate mean and scalar RMS from training positions only."""
    total = torch.zeros(d_in, dtype=torch.float64)
    square, count = 0., 0
    for batch in train_batches:
        values = _batch(batch, d_in).to(device="cpu", dtype=torch.float64)
        total += values.sum(0)
        square += float(values.square().sum())
        count += len(values)
    if not count:
        raise ValueError("SAE training iterable is empty")
    rms = (square / (count * d_in)) ** .5
    if not rms > 0:
        raise ValueError("training activations must have positive RMS")
    return {"input_rms": rms, "mean": (total / count).float(), "positions": count}


@torch.no_grad()
def evaluate_sae(model, batches, *, reference_mean=None):
    """Position-weighted reconstruction/sparsity metrics in raw input units.

    If supplied, ``reference_mean`` fixes the FVU denominator to a training-only
    constant predictor. Otherwise FVU uses this evaluation set's centered
    variance as a descriptive metric; it does not change model normalization.
    Dead features mean zero positive activations in this evaluation iterable.
    """
    parameter = next(model.parameters())
    count, squared_error, squared_reference, squared_input = 0, 0., 0., 0.
    summed_input = torch.zeros(model.config.d_in, dtype=torch.float64)
    frequencies = torch.zeros(model.config.d_sae, dtype=torch.long)
    totals = {key: 0. for key in ("loss", "reconstruction", "sparsity", "auxiliary")}
    reference = None if reference_mean is None else torch.as_tensor(reference_mean, device=parameter.device,
                                                                   dtype=parameter.dtype)
    if reference is not None and reference.shape != (model.config.d_in,):
        raise ValueError("FVU reference_mean must have shape [d_in]")
    was_training = model.training
    model.eval()
    try:
        for batch in batches:
            values = _batch(batch, model.config.d_in).to(parameter)
            reconstructed, features = model(values)
            losses = model.loss(values)
            if reconstructed.shape != values.shape or features.shape != (len(values), model.config.d_sae):
                raise ValueError("SAE reconstruction and feature shapes do not match batch")
            if not torch.isfinite(reconstructed).all() or not torch.isfinite(features).all():
                raise ValueError("SAE evaluation produced nonfinite outputs")
            for key in totals:
                if not torch.isfinite(losses[key]):
                    raise ValueError("SAE evaluation objective is nonfinite")
                totals[key] += float(losses[key]) * len(values)
            squared_error += float((reconstructed.float() - values.float()).square().double().sum())
            if reference is not None:
                squared_reference += float((values.float() - reference.float()).square().double().sum())
            else:
                raw = values.double()
                summed_input += raw.sum(0).cpu()
                squared_input += float(raw.square().sum())
            frequencies += (features > 0).sum(0).cpu()
            count += len(values)
    finally:
        model.train(was_training)
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
        "dead_feature_definition": "zero positive activations in this evaluation split",
        "feature_frequencies": (frequencies.double() / count).tolist(), "positions": count}


def train_sae(model, train_batches, validation_batches, checkpoint_dir, *,
              epochs=10, lr=1e-3, patience=3, min_delta=1e-4, seed=0,
              resume=True, provenance=None, progress_every=20):
    """Fit an SAE with persistent Adam and validation-only checkpoint selection.

    Supply separate re-iterable DataLoaders. Statistics initialize only from
    train batches. Epoch count can increase on resume; objective/binding/data
    provenance and optimizer settings cannot silently change. Test data has no
    place in this training interface and must be evaluated after selection.
    """
    if torch.is_inference_mode_enabled():
        raise ValueError("SAE training cannot run under torch.inference_mode()")
    if train_batches is validation_batches:
        raise ValueError("independent train and validation iterables are required")
    if epochs < 1 or lr <= 0 or patience < 1 or min_delta < 0 or progress_every < 1:
        raise ValueError("invalid SAE optimization or early stopping settings")
    if not all(torch.isfinite(torch.tensor(value)) for value in (lr, min_delta)):
        raise ValueError("SAE optimization settings must be finite")
    directory = Path(checkpoint_dir)
    directory.mkdir(parents=True, exist_ok=True)
    parameter = next(model.parameters())
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    generator = getattr(train_batches, "generator", None)
    configuration = {"model": asdict(model.config), "lr": lr, "patience": patience,
                     "min_delta": min_delta, "seed": seed,
                     "selection": "minimum validation total objective"}
    provenance = dict(provenance or {})
    state_path, best_path = directory / "training_state.pt", directory / "best.pt"
    start_epoch, stale, best = 0, 0, float("inf")
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    if resume and state_path.is_file():
        state = torch.load(state_path, map_location="cpu", weights_only=True)
        if (state["configuration"] != configuration or state["binding"] != dict(model.binding)
                or state["provenance"] != provenance):
            raise ValueError("SAE resume configuration, binding, or provenance does not match")
        if not best_path.is_file():
            raise ValueError("SAE resume state exists without its best checkpoint")
        model.load_state_dict(state["model"])
        optimizer.load_state_dict(state["optimizer"])
        torch.set_rng_state(state["rng"])
        if state.get("cuda_rng") is not None and torch.cuda.is_available():
            torch.cuda.set_rng_state_all(state["cuda_rng"])
        if generator is not None and state.get("loader_rng") is not None:
            generator.set_state(state["loader_rng"])
        normalization = state["normalization"]
        start_epoch, stale, best, history = state["epoch"], state["stale"], state["best"], state["history"]
    else:
        if best_path.exists() or state_path.exists():
            raise ValueError("SAE output contains an earlier run; resume it or choose a new directory")
        normalization = fit_normalization(train_batches, model.config.d_in)
        model.set_normalization_(normalization["input_rms"])
        model.initialize_bias_(normalization["mean"])
        model.normalize_decoder_()
        initial = evaluate_sae(model, validation_batches, reference_mean=normalization["mean"])
        best = initial["loss"]
        model.is_fitted = True
        _save_model(model, best_path)
        history = {"configuration": configuration, "binding": dict(model.binding),
            "provenance": provenance, "normalization": {**normalization, "mean": normalization["mean"].tolist(),
            "fit_split": "train"}, "initial_validation": initial, "best_epoch": 0, "epochs": []}
        # An interruption in the very first epoch can restart from the fully
        # initialized, train-only baseline instead of leaving an orphan best.pt.
        _torch(state_path, {"configuration": configuration, "binding": dict(model.binding),
            "provenance": provenance, "model": model.state_dict(), "optimizer": optimizer.state_dict(),
            "normalization": normalization, "epoch": 0, "stale": 0, "best": best,
            "history": history, "rng": torch.get_rng_state(),
            "cuda_rng": torch.cuda.get_rng_state_all() if torch.cuda.is_available() else None,
            "loader_rng": generator.get_state() if generator is not None else None})
        _json(directory / "history.json", history)
    started = time.monotonic()
    for epoch in range(start_epoch, epochs if stale < patience else start_epoch):
        model.train()
        totals, count = {key: 0. for key in ("loss", "reconstruction", "sparsity", "auxiliary")}, 0
        for step, batch in enumerate(train_batches):
            values = _batch(batch, model.config.d_in).to(parameter)
            optimizer.zero_grad(set_to_none=True)
            losses = model.loss(values)
            if not torch.isfinite(losses["loss"]):
                raise ValueError("SAE training objective is nonfinite")
            losses["loss"].backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 5., error_if_nonfinite=True)
            optimizer.step()
            model.normalize_decoder_()
            for key in totals:
                totals[key] += float(losses[key].detach()) * len(values)
            count += len(values)
            if (step + 1) % progress_every == 0:
                _json(directory / "status.json", {"state": "training", "epoch": epoch + 1,
                    "steps": step + 1, "positions": count, "train_loss": totals["loss"] / count,
                    "elapsed_seconds": time.monotonic() - started})
        if not count:
            raise ValueError("SAE training iterable is empty")
        validation = evaluate_sae(model, validation_batches, reference_mean=normalization["mean"])
        row = {"epoch": epoch + 1, "train": {key: value / count for key, value in totals.items()},
               "train_positions": count, "validation": validation,
               "elapsed_seconds": time.monotonic() - started}
        history["epochs"].append(row)
        if validation["loss"] < best - min_delta:
            best, stale, history["best_epoch"] = validation["loss"], 0, epoch + 1
            model.is_fitted = True
            _save_model(model, best_path)
        else:
            stale += 1
        _torch(state_path, {"configuration": configuration, "binding": dict(model.binding),
            "provenance": provenance, "model": model.state_dict(), "optimizer": optimizer.state_dict(),
            "normalization": normalization, "epoch": epoch + 1, "stale": stale, "best": best,
            "history": history, "rng": torch.get_rng_state(),
            "cuda_rng": torch.cuda.get_rng_state_all() if torch.cuda.is_available() else None,
            "loader_rng": generator.get_state() if generator is not None else None})
        _json(directory / "history.json", history)
        _json(directory / "status.json", {"state": "training", "epoch": epoch + 1,
            "best_epoch": history["best_epoch"], "best_validation_loss": best, "stale_epochs": stale})
        print(json.dumps({"architecture": model.config.architecture, "epoch": epoch + 1,
                          "train_loss": totals["loss"] / count, "validation_loss": validation["loss"],
                          "best_validation_loss": best}), flush=True)
        if stale >= patience:
            break
    restored = type(model).load(best_path, expected_binding=dict(model.binding), device=parameter.device)
    model.load_state_dict(restored.state_dict())
    model.is_fitted = restored.is_fitted
    model.eval()
    history.update(status="complete", completed_epochs=len(history["epochs"]), best_validation_loss=best,
                   checkpoint=str(best_path))
    _json(directory / "history.json", history)
    _json(directory / "status.json", {"state": "complete", "best_epoch": history["best_epoch"],
                                      "best_validation_loss": best, "checkpoint": str(best_path)})
    return history
