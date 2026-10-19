#!/usr/bin/env python3
"""Capture your own native residual activations for SAE training.

Input JSONL rows: {"id":"unique", "split":"train|validation|test",
"group":"source-group", "text":"prompt", "image":"optional/relative.jpg"}.
Split and group labels are supplied by the user before model extraction.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path

import torch


def file_hash(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(8 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, default=str).encode()).hexdigest()


def validate_records(records):
    seen, groups, splits = set(), {}, set()
    for row in records:
        if not isinstance(row.get("id"), str) or not row["id"] or row["id"] in seen:
            raise ValueError("manifest requires unique nonempty string IDs")
        seen.add(row["id"])
        if row.get("split") not in {"train", "validation", "test"}:
            raise ValueError("manifest split must be train, validation or test")
        if not isinstance(row.get("group"), str) or not row["group"]:
            raise ValueError("manifest requires a source group for every record")
        if row["group"] in groups and groups[row["group"]] != row["split"]:
            raise ValueError("source group overlap across manifest splits")
        if not isinstance(row.get("text"), str) or not row["text"]:
            raise ValueError("manifest requires nonempty input text")
        groups[row["group"]] = row["split"]
        splits.add(row["split"])
    if splits != {"train", "validation", "test"}:
        raise ValueError("manifest must provide all three independent splits")


def immutable_model_identity(model_source, model, explicit=None):
    if explicit:
        return explicit
    source = Path(model_source)
    if source.is_dir():
        names = sorted({path for pattern in ("*.safetensors", "*.bin", "config.json") for path in source.glob(pattern)})
        if not names or not any(path.suffix in {".bin", ".safetensors"} for path in names):
            raise ValueError("local model has no recognizable weight files; pass --model-id with immutable identity")
        hashes = {str(path.relative_to(source)): file_hash(path) for path in names}
        return str(model_source) + "@sha256:" + fingerprint(hashes)
    revision = getattr(model.config, "_commit_hash", None)
    if not revision:
        raise ValueError("cannot resolve immutable model commit; pass --model-id explicitly")
    return model_source + "@" + revision


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--revision", help="Prefer an immutable HF commit when downloading a model")
    parser.add_argument("--model-id", help="Explicit immutable checkpoint ID, otherwise resolved/hashed")
    parser.add_argument("--tokenizer-id", help="Explicit immutable tokenizer ID, otherwise hashed")
    parser.add_argument("--vlm", action="store_true", help="Use the native image-text model/processor instead of a text LM")
    parser.add_argument("--layer", type=int, required=True)
    parser.add_argument("--tokens", choices=["all", "text", "visual", "last_prompt"], default="all")
    parser.add_argument("--device", default="cuda:0" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--max-length", type=int, default=2048)
    parser.add_argument("--image-side", type=int, help="Optional max image side before native processor resizing")
    parser.add_argument("--threads", type=int, default=4)
    args = parser.parse_args(argv)
    if args.max_length < 1 or args.threads < 1 or (args.image_side is not None and args.image_side < 1):
        parser.error("length, threads and optional image size must be positive")
    records = [json.loads(line) for line in args.manifest.read_text().splitlines() if line.strip()]
    validate_records(records)
    if not args.vlm and any(row.get("image") for row in records):
        parser.error("image inputs require --vlm")
    if args.tokens == "visual" and not args.vlm:
        parser.error("visual token selection requires a VLM")
    torch.set_num_threads(args.threads)
    from PIL import Image
    from transformers import AutoModelForCausalLM, AutoModelForImageTextToText, AutoProcessor, AutoTokenizer
    from vlmprobe import Prober
    from vlmprobe.sae.binding import build_sae_binding

    dtype = torch.bfloat16 if args.device.startswith("cuda") else torch.float32
    model_class = AutoModelForImageTextToText if args.vlm else AutoModelForCausalLM
    model = model_class.from_pretrained(args.model, revision=args.revision, dtype=dtype,
                                        attn_implementation="eager").to(args.device).eval().requires_grad_(False)
    processor = (AutoProcessor if args.vlm else AutoTokenizer).from_pretrained(args.model, revision=args.revision)
    tokenizer = processor.tokenizer if hasattr(processor, "tokenizer") else processor
    probe = Prober(model, processor)
    if args.layer not in probe.spec.residuals:
        parser.error(f"layer {args.layer} is unavailable; inspect Prober(model).describe()")
    model_id = immutable_model_identity(args.model, model, args.model_id)
    tokenizer_content = {"special_tokens": tokenizer.special_tokens_map,
                         "chat_template": getattr(tokenizer, "chat_template", None),
                         "backend": tokenizer.backend_tokenizer.to_str() if hasattr(tokenizer, "backend_tokenizer") else tokenizer.get_vocab()}
    tokenizer_id = args.tokenizer_id or "sha256:" + fingerprint(tokenizer_content)
    preprocessing = {"vlm": args.vlm, "tokens": args.tokens, "max_length": args.max_length,
                     "image_side": args.image_side, "processor": processor.to_dict() if hasattr(processor, "to_dict") else type(processor).__name__,
                     "chat_template": getattr(tokenizer, "chat_template", None)}
    binding = build_sae_binding(probe, args.layer, model_id=model_id, tokenizer_id=tokenizer_id,
        preprocessing_id="sha256:" + fingerprint(preprocessing), calibration_id="sha256:" + file_hash(args.manifest))
    values = {split: [] for split in ("train", "validation", "test")}
    groups = {split: [] for split in values}
    positions, image_hashes = [], {}
    with torch.no_grad():
        for number, row in enumerate(records):
            image = None
            if row.get("image"):
                path = Path(row["image"])
                path = path if path.is_absolute() else args.manifest.parent / path
                path = path.resolve()
                image_hashes[str(path)] = file_hash(path)
                with Image.open(path) as original:
                    image = original.convert("RGB")
                if args.image_side:
                    image.thumbnail((args.image_side, args.image_side), Image.Resampling.LANCZOS)
            if args.vlm:
                content = ([{"type": "image"}] if image is not None else []) + [{"type": "text", "text": row["text"]}]
                prompt = processor.apply_chat_template([{"role": "user", "content": content}],
                    tokenize=False, add_generation_prompt=True)
                inputs = probe.prepare(prompt=prompt, image=image, device=args.device)
                if inputs.kwargs["input_ids"].shape[-1] > args.max_length:
                    raise ValueError("expanded VLM sequence exceeds --max-length; reduce image/text size explicitly")
            else:
                inputs = {key: value.to(args.device) for key, value in tokenizer(row["text"],
                    return_tensors="pt", truncation=True, max_length=args.max_length).items()}
            site = probe.spec.residuals[args.layer]
            trace = probe._run(inputs, capture=[site])
            hidden = trace.activations[site]
            mask = probe._layout(inputs, hidden).select(args.tokens)
            selected = hidden[mask].detach().cpu().float()
            values[row["split"]].append(selected)
            groups[row["split"]].extend([row["group"]] * len(selected))
            positions.append({"id": row["id"], "split": row["split"], "group": row["group"],
                              "positions": mask.nonzero().cpu().tolist(), "count": len(selected)})
            del trace
            print(json.dumps({"state": "capturing", "records": number + 1, "total": len(records),
                              "last_id": row["id"], "selected_positions": len(selected)}), flush=True)
    bundle = {"format": "vlmprobe-sae-activations-v1", "binding": binding,
              **{name: torch.cat(rows) for name, rows in values.items()}, "groups": groups,
              "provenance": {"manifest_sha256": file_hash(args.manifest), "preprocessing": preprocessing,
                             "image_sha256": image_hashes, "record_positions": positions}}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    temporary = args.output.with_name(args.output.name + ".tmp")
    torch.save(bundle, temporary)
    os.replace(temporary, args.output)
    print(json.dumps({"state": "complete", "output": str(args.output), "sha256": file_hash(args.output),
                      "positions": {name: len(bundle[name]) for name in values}}))


if __name__ == "__main__":
    main()
