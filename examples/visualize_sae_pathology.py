#!/usr/bin/env python3
"""Run trained dictionaries on real held-out PathVG images and plot features.

Images are read from the offline dataset and passed through a live native VLM.
Cached training activations select features using validation variance only;
they do not stand in for the live demonstration forwards.
"""
from __future__ import annotations
import argparse
import base64
import hashlib
from io import BytesIO
import json
from pathlib import Path
import random
import zipfile

import numpy as np
import torch
from PIL import Image
from transformers import AutoModelForImageTextToText, AutoProcessor
from vlmprobe import Prober, TokenMargin, visualization as viz
from vlmprobe.sae import SparseAutoencoder
from vlmprobe.sae.binding import build_sae_binding


def digest(path):
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 << 20), b""):
            value.update(block)
    return value.hexdigest()


def thumbnail(image, record):
    """Replay the exact audited transform; check original and rounded dimensions."""
    frame = record["transform"]
    if list(image.size) != frame["original_size"]:
        raise ValueError("dataset image geometry changed")
    canvas = Image.new("RGB", frame["canvas_size"], "white")
    canvas.paste(image.resize(frame["resized_size"], Image.Resampling.LANCZOS), frame["padding_xy"])
    return canvas


@torch.no_grad()
def select_validation_feature(sae, values):
    """Choose the largest activation variance without inspecting any test map."""
    parameter = next(sae.parameters())
    total = torch.zeros(sae.config.d_sae, device=parameter.device, dtype=torch.float64)
    square, frequency = total.clone(), total.clone()
    for chunk in values.split(1024):
        z = sae.encode(chunk.to(parameter)).double()
        total += z.sum(0)
        square += z.square().sum(0)
        frequency += (z > 0).sum(0)
    variance = (square / len(values) - (total / len(values)).square()).clamp_min(0)
    index = int(variance.argmax())
    return index, {"validation_variance": float(variance[index]),
                   "validation_firing_fraction": float(frequency[index] / len(values)),
                   "rule": "largest validation activation variance; never test-selected"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-root", type=Path, required=True)
    parser.add_argument("--pathology-run", type=Path, required=True)
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--dataset-zip", type=Path, default=Path("/tealab-data/WSI/RefPath/refpath_image.zip"))
    parser.add_argument("--device", default="cuda:0")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    torch.set_num_threads(4)
    cache = args.pathology_run / "cache"
    index = json.loads((cache / "index.json").read_text())
    if index.get("state") != "complete":
        raise ValueError("a completed pathology cache is required for held-out provenance")
    metadata = index["metadata"]
    processor_hashes = {path.name: digest(path) for pattern in ("*preprocessor_config.json", "processor_config.json")
                        for path in args.model.glob(pattern)}
    for item in metadata["model_files"] + metadata["tokenizer_files"]:
        if digest(args.model / item["path"]) != item["sha256"]:
            raise ValueError("native demonstration model/tokenizer differs from training checkpoint")
    bundle = torch.load(args.run_root / "activations.pt", map_location="cpu", weights_only=True)
    if bundle["provenance"]["pathology_cache_index_sha256"] != digest(cache / "index.json"):
        raise ValueError("SAE training and image demonstration use different source caches")
    model = AutoModelForImageTextToText.from_pretrained(args.model, local_files_only=True,
        dtype=torch.bfloat16, attn_implementation="sdpa").to(args.device).eval()
    processor = AutoProcessor.from_pretrained(args.model, use_fast=False, local_files_only=True)
    probe = Prober(model, processor)
    architectures = ("relu", "topk", "gated")
    kernels, selected, histories = {}, {}, {}
    for architecture in architectures:
        kernel = SparseAutoencoder.load(args.run_root / architecture / "best.pt",
            expected_binding=bundle["binding"], device=args.device)
        expected = build_sae_binding(probe, kernel.binding["layer"], **{
            key: kernel.binding[key] for key in ("model_id", "tokenizer_id", "preprocessing_id", "calibration_id")})
        if expected != kernel.binding:
            raise ValueError("trained SAE hook does not match the live model")
        kernels[architecture] = kernel
        feature_id, selection = select_validation_feature(kernel, bundle["validation"])
        selected[architecture] = {"feature_id": feature_id, **selection}
        histories[architecture] = json.loads((args.run_root / architecture / "metrics.json").read_text())
    rows = sorted((r for r in index["records"] if r["split"] == "test"), key=lambda r: r["id"])
    random.Random(args.seed).shuffle(rows)
    rows = sorted(rows[:3], key=lambda r: r["id"])
    destination = args.run_root / "results"
    destination.mkdir(exist_ok=True)
    measured, gallery = [], []
    with zipfile.ZipFile(args.dataset_zip) as archive:
        for reference in rows:
            if digest(cache / reference["path"]) != reference["sha256"]:
                raise ValueError("held-out cached record checksum changed")
            record = torch.load(cache / reference["path"], map_location="cpu", weights_only=True)
            original = Image.open(BytesIO(archive.read(record["zip_entry"]))).convert("RGB")
            canvas = thumbnail(original, record)
            with Image.open(cache / record["image_path"]) as cached_image:
                if not np.array_equal(np.asarray(canvas), np.asarray(cached_image.convert("RGB"))):
                    raise ValueError("live replayed thumbnail differs from the recorded model canvas")
            canvas_hash = hashlib.sha256(np.asarray(canvas).tobytes()).hexdigest()
            # This is a real image/prompt -> native processor -> Prober forward.
            inputs = dict(processor(text=record["prompt"], images=canvas, return_tensors="pt"))
            grid = inputs["image_grid_thw"][0].tolist()
            merge = model.config.vision_config.spatial_merge_size
            if [grid[1] // merge, grid[2] // merge] != record["grid_shape"]:
                raise ValueError("native processor grid differs from training geometry")
            inputs = {key: value.to(args.device) if isinstance(value, torch.Tensor) else value
                      for key, value in inputs.items()}
            maps = {}
            for architecture, kernel in kernels.items():
                feature_id = selected[architecture]["feature_id"]
                result = probe.sae.features(layer=kernel.binding["layer"], sae=kernel,
                    binding=kernel.binding, tokens="visual").run(inputs)
                cached_native = record["visual_features"][record["layer_ids"].index(kernel.binding["layer"])].float()
                native_difference = float((result.tensors["activation"].float() - cached_native).abs().max())
                maps[architecture] = result
                # Retain complete structured outputs for independent inspection.
                safe_id = hashlib.sha256(record["id"].encode()).hexdigest()[:16]
                result.save(destination / "native_results" / architecture / safe_id)
                baseline = probe._run(inputs).logits[0, -1]
                candidates = baseline.topk(2).indices.tolist()
                metric = TokenMargin(*candidates)
                conditions = {}
                for condition, scale, mode in (("identity", 1., "error_preserving"),
                                               ("feature_ablation", 0., "error_preserving"),
                                               ("reconstruction", 1., "reconstruction")):
                    edited = probe.sae.edit(layer=kernel.binding["layer"], sae=kernel,
                        binding=kernel.binding, tokens="visual", feature_ids=[feature_id],
                        scale=scale, mode=mode).run(inputs, metric=metric)
                    conditions[condition] = {
                        "baseline_margin": float(edited.tensors["baseline_score"].item()),
                        "edited_margin": float(edited.tensors["edited_score"].item()),
                        "score_change": float(edited.tensors["score_change"].item()),
                        "max_logit_difference": float((edited.tensors["edited_logits"] - edited.tensors["baseline_logits"]).abs().max())}
                    if condition == "identity" and conditions[condition]["max_logit_difference"] != 0.:
                        raise RuntimeError("identity feature intervention must be exactly a no-op")
                measured.append({"id": record["id"], "architecture": architecture,
                    "source_record_sha256": reference["sha256"], "canvas_rgb_sha256": canvas_hash,
                    "live_vs_cached_residual_max_abs": native_difference,
                    "feature_id": feature_id, "positive_token": candidates[0], "negative_token": candidates[1],
                    "positive_text": processor.tokenizer.decode([candidates[0]]),
                    "negative_text": processor.tokenizer.decode([candidates[1]]), "conditions": conditions})
            gallery.append({"id": record["id"], "canvas": canvas, "record": record, "maps": maps})
    fig, axes = plt.subplots(len(gallery), 4, figsize=(14, 3.4 * len(gallery)), layout="constrained")
    maxima = {architecture: max(float(row["maps"][architecture].tensors["features"][:,
                       selected[architecture]["feature_id"]].max()) for row in gallery) for architecture in architectures}
    for row_index, row in enumerate(gallery):
        x0, y0, x1, y1 = row["record"]["bbox_canvas"]
        boxes = [(x0, y0, x1 - x0, y1 - y0)]
        viz.plot_input(row["canvas"], bounding_boxes=boxes, ax=axes[row_index, 0])
        axes[row_index, 0].set_title("Input patch + annotated region", fontsize=11)
        for column, architecture in enumerate(architectures, start=1):
            feature_id = selected[architecture]["feature_id"]
            viz.plot_sae_feature_overlay(row["canvas"], row["maps"][architecture],
                feature_id=feature_id, grid_shape=row["record"]["grid_shape"], bounding_boxes=boxes,
                vmin=0., vmax=max(maxima[architecture], 1e-8), cmap="magma", ax=axes[row_index, column])
            name = {"relu": "ReLU", "topk": "TopK", "gated": "Gated"}[architecture]
            axes[row_index, column].set_title(f"{name} · feature {feature_id}", fontsize=11)
    fig.savefig(destination / "heldout_sparse_features.png", dpi=170, bbox_inches="tight")
    plt.close(fig)
    (destination / "feature_selection.json").write_text(json.dumps(selected, indent=2))
    (destination / "interventions.json").write_text(json.dumps(measured, indent=2))
    lines = ["# SAE pathology pilot", "", "Three native dictionary architectures trained on the same frozen layer-7 visual activations.",
        "", "| Architecture | Test MSE | Test FVU | Mean active features | Zero-fire fraction |", "| --- | --- | --- | --- | --- |"]
    for architecture, history in histories.items():
        metric = history["test"]
        lines.append(f"| {architecture} | {metric['mse']:.5f} | {metric['fvu']:.5f} | {metric['l0']:.2f} | {metric['dead_feature_fraction']:.3f} |")
    lines += ["", "FVU uses the training mean as the fixed constant-predictor reference. Sparsity differs across architectures; this is a functional pilot, not a matched-L0 architecture benchmark.",
        "", f"Feature IDs were chosen by validation activation variance. Images are fixed by seed {args.seed}; no test-map quality selects examples. Features are unnamed and do not establish pathology concepts.",
        "", "In these examples, the validation-selected ReLU and Gated features concentrate near image corners. This suggests positional structure and does not justify a named pathology interpretation.",
        "", "Every map was recomputed from the original dataset image through the native model. Annotation boxes are spatial context, not targets used for SAE training.",
        "", "The intervention report measures the model's own top-one versus top-two next-token margin. It is a mechanism demonstration, not ground-truth pathology accuracy. Identity edits preserve logits exactly; feature ablation and reconstruction replacement are separate controls.",
        "", "ReLU uses L1 sparsity, TopK uses the core per-token selection rule without AuxK/resampling, and Gated uses a paper-inspired frozen-decoder auxiliary loss with detached auxiliary centering. No complete paper-scale training recipe is claimed.",
        "", "Selected source record hashes and replayed canvas pixels were checked. Runtime processor config hashes are recorded; the original extraction did not hash those processor files, so equality with a historical processor configuration is not established. Fresh-versus-cached native residual differences are recorded in interventions.json."]
    (destination / "RESULTS.md").write_text("\n".join(lines) + "\n")
    (destination / "runtime_provenance.json").write_text(json.dumps({"processor_config_sha256": processor_hashes,
        "processor_historical_comparison": "original cache did not hash processor files",
        "cache_index_sha256": digest(cache / "index.json"), "gallery_seed": args.seed}, indent=2))
    encoded = base64.b64encode((destination / "heldout_sparse_features.png").read_bytes()).decode()
    rows_html = "".join(f"<tr><td>{name}</td><td>{h['test']['mse']:.4f}</td><td>{h['test']['fvu']:.4f}</td><td>{h['test']['l0']:.1f}</td></tr>" for name, h in histories.items())
    document = f"""<!doctype html><meta charset='utf-8'><title>SAE pathology pilot</title>
<style>body{{max-width:1250px;margin:40px auto;padding:20px;font:17px/1.6 system-ui;color:#18374f;background:#f6f9fc}}img{{width:100%}}table{{border-collapse:collapse}}td,th{{padding:10px 24px;border-bottom:1px solid #ccd6e1}}pre{{white-space:pre-wrap}}</style>
<h1>Sparse feature dictionaries on pathology patches</h1><p>Three trained architectures · native VLM inputs · validation-selected features</p>
<p>Feature IDs are unnamed. These reconstruction experiments do not establish clinical concepts. The three models use different sparsity constraints and are not a matched-sparsity benchmark.</p>
<table><tr><th>Architecture</th><th>Test MSE</th><th>Test FVU</th><th>Mean L0</th></tr>{rows_html}</table>
<img src='data:image/png;base64,{encoded}' alt='Real held-out sparse feature maps'>
<p>Green boxes are annotations shown for context. Feature selection uses validation variance; the image opacity is 0.2. Each feature retains its native activation scale.</p>
<p><a href='interventions.json'>Native model feature interventions and identity/reconstruction controls</a> · <a href='feature_selection.json'>Validation selection</a> · <a href='RESULTS.md'>Scope and results</a></p>
"""
    (destination / "index.html").write_text(document)
    print(json.dumps({"state": "complete", "results": str(destination), "examples": len(gallery), "intervention_measurements": len(measured)}))


if __name__ == "__main__":
    main()
