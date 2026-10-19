#!/usr/bin/env python3
"""Train native ReLU, TopK or Gated SAEs from your own frozen activations.

Portable input is a weights-only-safe .pt bundle with binding, train/validation/
test[N,D], and groups={split: [source group per activation row]}. Alternatively,
convert the separate pathology pilot's native visual-feature cache once.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import time

import torch
from torch.utils.data import DataLoader


def digest_file(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(8 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def atomic_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")
    os.replace(temporary, path)


def validate_bundle(bundle):
    """Reject missing source groups and cross-split leakage before fitting."""
    if not isinstance(bundle.get("binding"), dict) or not bundle["binding"]:
        raise ValueError("activation bundle requires an explicit immutable binding")
    splits, groups, dimensions = {}, {}, set()
    for name in ("train", "validation", "test"):
        value = bundle.get(name)
        if isinstance(value, dict):
            group_values = value.get("groups", value.get("group_ids"))
            value = value.get("activations")
        else:
            group_values = bundle.get("groups", bundle.get("group_ids", {})).get(name)
        if (not isinstance(value, torch.Tensor) or value.ndim != 2 or not value.is_floating_point()
                or min(value.shape) < 1 or not torch.isfinite(value).all()):
            raise ValueError(f"{name} must contain finite, nonempty floating activations[N,D]")
        if (not isinstance(group_values, (list, tuple)) or len(group_values) != len(value)
                or any(not isinstance(group, str) or not group for group in group_values)):
            raise ValueError(f"{name} requires a nonempty source group string per activation row")
        splits[name] = value.detach().cpu().contiguous()
        groups[name] = set(group_values)
        dimensions.add(value.shape[1])
    if len(dimensions) != 1:
        raise ValueError("all activation splits must have the same hidden width")
    for left, right in (("train", "validation"), ("train", "test"), ("validation", "test")):
        if groups[left] & groups[right]:
            raise ValueError(f"source group overlap between {left} and {right}")
    summary = {name: {"positions": len(splits[name]), "source_groups": len(groups[name])} for name in splits}
    return splits, summary


def pathology_bundle(cache_dir: Path, layer: int, model_source: Path):
    """Convert audited native visual features; no model weights or GPU needed."""
    from accelerate import init_empty_weights
    from transformers import AutoConfig, AutoModelForImageTextToText
    from vlmprobe import Prober
    from vlmprobe.sae.binding import build_sae_binding

    directory = cache_dir.resolve()
    index_path = directory / "index.json"
    index = json.loads(index_path.read_text())
    if index.get("state") != "complete":
        raise ValueError("pathology activation extraction must be complete")
    metadata = index["metadata"]
    if layer not in metadata["layer_ids"]:
        raise ValueError("requested SAE layer is absent from pathology cache")
    config_rows = [row for row in metadata["model_files"] if row["path"] == "config.json"]
    if len(config_rows) != 1 or digest_file(model_source / "config.json") != config_rows[0]["sha256"]:
        raise ValueError("local model architecture config differs from cached checkpoint")
    config = AutoConfig.from_pretrained(model_source, local_files_only=True)
    with init_empty_weights():
        model = AutoModelForImageTextToText.from_config(config, attn_implementation="eager")
    probe = Prober(model)
    if probe.spec.residuals[layer] != metadata["sites"][str(layer)]:
        raise ValueError("native adapter residual site differs from pathology feature metadata")
    frame = {key: metadata.get(key) for key in ("image_side", "caption_prompt", "site", "dtype")}
    frame.update(tokens="visual_valid_mask", geometry="aspect-preserving white letterbox; native Qwen merged grid")
    preprocessing_hash = hashlib.sha256(json.dumps(frame, sort_keys=True).encode()).hexdigest()
    index_hash = digest_file(index_path)
    binding = build_sae_binding(probe, layer,
        model_id=metadata["model_id"] + "@sha256:" + metadata["checkpoint_sha256"],
        tokenizer_id="sha256:" + metadata["tokenizer_sha256"],
        preprocessing_id="sha256:" + preprocessing_hash, calibration_id="sha256:" + index_hash)
    del probe, model
    values = {name: [] for name in ("train", "validation", "test")}
    groups = {name: [] for name in values}
    file_hashes, seen = [], set()
    for reference in index["records"]:
        identity = str(reference["id"])
        if identity in seen:
            raise ValueError("duplicate pathology cache record IDs")
        seen.add(identity)
        path = (directory / reference["path"]).resolve()
        if not path.is_relative_to(directory):
            raise ValueError("pathology cache tensor path escapes cache directory")
        payload = path.read_bytes()
        checksum = hashlib.sha256(payload).hexdigest()
        if reference.get("sha256") != checksum:
            raise ValueError("pathology feature cache checksum mismatch")
        record = torch.load(io.BytesIO(payload), map_location="cpu", weights_only=True)
        split = "validation" if reference["split"] == "val" else reference["split"]
        record_split = "validation" if record["split"] == "val" else record["split"]
        if split not in values or record_split != split or str(record["id"]) != identity:
            raise ValueError("pathology record ID/split differs from index")
        if record["layer_ids"] != metadata["layer_ids"]:
            raise ValueError("pathology record layer ordering differs from index")
        hidden = record["visual_features"][record["layer_ids"].index(layer)]
        mask = record["visual_valid_mask"]
        if mask.dtype != torch.bool or mask.shape != hidden.shape[:1] or not mask.any():
            raise ValueError("pathology visual_valid_mask must select native visual positions")
        selected = hidden[mask].clone()
        source = record["source_slide"]
        if not isinstance(source, str) or not source:
            raise ValueError("pathology records need reconstructed source-slide groups")
        values[split].append(selected)
        groups[split].extend([source] * len(selected))
        file_hashes.append({"path": reference["path"], "sha256": checksum})
    bundle = {"format": "vlmprobe-sae-activations-v1", "binding": binding, "groups": groups,
              **{name: torch.cat(rows) for name, rows in values.items()},
              "provenance": {"pathology_cache_index_sha256": index_hash,
                  "pathology_cache_files_sha256": hashlib.sha256(json.dumps(file_hashes, sort_keys=True).encode()).hexdigest(),
                  "layer": layer, "selected_tokens": "native visual tokens passing recorded valid mask",
                  "source_group_scope": "reconstructed source-slide filename groups; patient independence not established"}}
    validate_bundle(bundle)
    return bundle


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--activations", type=Path)
    source.add_argument("--pathology-cache", type=Path)
    parser.add_argument("--model", type=Path, help="Local model directory for verifying native pathology module structure")
    parser.add_argument("--layer", type=int, default=7)
    parser.add_argument("--export-bundle", type=Path)
    parser.add_argument("--prepare-only", action="store_true")
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--architecture", choices=["relu", "topk", "gated"], default="topk")
    parser.add_argument("--d-sae", type=int, default=4096)
    parser.add_argument("--k", type=int, default=32)
    parser.add_argument("--l1-coefficient", type=float, default=.01)
    parser.add_argument("--epochs", type=int, default=10)
    parser.add_argument("--batch-size", type=int, default=512)
    parser.add_argument("--lr", type=float, default=1e-3)
    parser.add_argument("--patience", type=int, default=3)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--threads", type=int, default=4)
    parser.add_argument("--device", default="cuda:0" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--no-resume", action="store_true")
    args = parser.parse_args(argv)
    if args.batch_size < 1 or args.threads < 1:
        parser.error("batch size and thread count must be positive")
    torch.set_num_threads(args.threads)
    if args.pathology_cache:
        if args.model is None:
            parser.error("--pathology-cache requires --model with the cache's local model directory")
        bundle = pathology_bundle(args.pathology_cache, args.layer, args.model)
    else:
        bundle = torch.load(args.activations, map_location="cpu", weights_only=True)
    splits, summary = validate_bundle(bundle)
    if args.export_bundle:
        args.export_bundle.parent.mkdir(parents=True, exist_ok=True)
        temporary = args.export_bundle.with_name(args.export_bundle.name + ".tmp")
        torch.save(bundle, temporary)
        os.replace(temporary, args.export_bundle)
    if args.prepare_only:
        if not args.export_bundle:
            parser.error("--prepare-only requires --export-bundle")
        print(json.dumps({"state": "prepared", "bundle": str(args.export_bundle), "splits": summary}))
        return
    if args.output_dir is None:
        parser.error("--output-dir is required for training")
    from vlmprobe.sae import SAEConfig, SparseAutoencoder
    from vlmprobe.sae.training import evaluate_sae, train_sae

    args.output_dir.mkdir(parents=True, exist_ok=True)
    status = args.output_dir / "run_status.json"
    atomic_json(status, {"state": "training", "architecture": args.architecture, "splits": summary})
    started = time.monotonic()
    try:
        generator = torch.Generator().manual_seed(args.seed)
        loaders = {name: DataLoader(values, batch_size=args.batch_size, shuffle=name == "train",
            generator=generator if name == "train" else None, num_workers=0) for name, values in splits.items()}
        config = SAEConfig(architecture=args.architecture, d_in=splits["train"].shape[-1],
            d_sae=args.d_sae, k=args.k, l1_coefficient=args.l1_coefficient, seed=args.seed)
        model = SparseAutoencoder(config, binding=bundle["binding"], device=args.device)
        bundle_path = args.export_bundle or args.activations
        provenance = {"bundle_sha256": digest_file(bundle_path) if bundle_path else None,
                      "source": bundle.get("provenance", {}), "splits": summary,
                      "batch_size": args.batch_size, "source_groups_disjoint": True}
        history = train_sae(model, loaders["train"], loaders["validation"], args.output_dir,
            epochs=args.epochs, lr=args.lr, patience=args.patience, seed=args.seed,
            resume=not args.no_resume, provenance=provenance)
        # No test positions are consulted until validation-selected weights reload.
        reference_mean = torch.tensor(history["normalization"]["mean"])
        validation = evaluate_sae(model, loaders["validation"], reference_mean=reference_mean)
        test = evaluate_sae(model, loaders["test"], reference_mean=reference_mean)
        metrics = {"state": "complete", "architecture": args.architecture, "configuration": config.__dict__,
            "binding": model.binding, "provenance": provenance, "normalization": history["normalization"],
            "best_epoch": history["best_epoch"], "validation": validation, "test": test,
            "checkpoint": str(args.output_dir / "best.pt"), "elapsed_seconds": time.monotonic() - started,
            "scope": "reconstruction and sparsity metrics; not automatic feature semantic validation"}
        atomic_json(args.output_dir / "metrics.json", metrics)
        atomic_json(status, {"state": "complete", "metrics": str(args.output_dir / "metrics.json"),
                            "best_epoch": history["best_epoch"], "elapsed_seconds": metrics["elapsed_seconds"]})
        print(json.dumps({"state": "complete", "architecture": args.architecture,
                          "test_mse": test["mse"], "test_fvu": test["fvu"], "test_l0": test["l0"]}))
    except BaseException as error:
        atomic_json(status, {"state": "interrupted" if isinstance(error, KeyboardInterrupt) else "failed",
            "error_type": type(error).__name__, "error": str(error), "elapsed_seconds": time.monotonic() - started})
        raise


if __name__ == "__main__":
    main()
