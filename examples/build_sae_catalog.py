#!/usr/bin/env python3
"""Build a compressed, source-versioned metadata catalog, without model weights.

Inputs are JSON exports from the provider's discovery function or a verified
official release table. This keeps optional dependencies out of catalog usage.
"""
import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path


def read_rows(path, backend):
    value = json.loads(path.read_text())
    rows = value if isinstance(value, list) else value["entries"]
    if not isinstance(rows, list) or any(row.get("backend") != backend for row in rows):
        raise ValueError(f"input rows must identify backend {backend}")
    return rows


def build(saelens_path, prisma_path, output, *, snapshot_date="2026-10-19",
          verification_path=None,
          saelens_commit="30c4502466785dd7809a307f7b705df187978aa3",
          saelens_yaml_sha256="bea73bf39c2a345ce03fca3d9d44e133085e9ff2aea74c8ae5b26de0819c96d2",
          prisma_commit="64daf1425f7e5311844213fd0fb6f4127a30cd16",
          overcomplete_commit="a1781af49c6e4bbfdbfd763b9757bcf6c5dd6403"):
    rows = read_rows(saelens_path, "saelens") + read_rows(prisma_path, "prisma")
    seen = set()
    for row in rows:
        identity = (row["backend"], row["release"], row["sae_id"])
        if identity in seen:
            raise ValueError(f"duplicate catalog identity {identity}")
        seen.add(identity)
        if not str(row.get("source_url", "")).startswith("https://"):
            raise ValueError("every catalog entry needs a primary-source URL")
        description = " ".join(str(row.get(key, "")) for key in ("release", "token_scope", "architecture")).lower()
        transcoder = row.get("is_transcoder") is True or "transcoder" in description
        temporal = "temporal" in description
        row["resource_kind"] = "transcoder" if transcoder else "temporal_sae" if temporal else "sae"
        if transcoder or temporal or row.get("hook_point_head_index") is not None:
            row["adapter_compatible"] = False
        row["verification"] = "upstream_config_metadata" if row.get("config_only_verified") else "upstream_registry_listing"
        row["weights_verified"] = False
        row["compatibility_note"] = "Loading still requires the exact model, hook, preprocessing and activation convention; metadata is not a completed model transfer."
    verified = []
    if verification_path is not None:
        proofs = json.loads(verification_path.read_text())
        if not isinstance(proofs, list):
            raise ValueError("verification input must be a list of numerical checks")
        by_identity = {(row["backend"], row["release"], row["sae_id"]): row for row in rows}
        proof_ids = set()
        for proof in proofs:
            identity = (proof["backend"], proof["release"], proof["sae_id"])
            if identity in proof_ids or identity not in by_identity:
                raise ValueError(f"duplicate or unknown verified resource {identity}")
            proof_ids.add(identity)
            if (proof.get("features_finite") is not True or
                    proof.get("reconstruction_finite") is not True or not proof.get("scope")):
                raise ValueError("numerical checks require finite outputs and an explicit scope")
            row = by_identity[identity]
            row.update(weights_verified=True, verification="pretrained_dictionary_cpu_vectors",
                       verification_scope=proof["scope"])
            for key in ("d_in", "d_sae", "weights_sha256", "weights_size_bytes"):
                if key in proof:
                    row[key] = proof[key]
            if proof.get("revision"):
                if row.get("revision") and row["revision"] != proof["revision"]:
                    raise ValueError(f"verified revision differs from catalog for {identity}")
                row["revision"] = proof["revision"]
            verified.append({key: proof[key] for key in ("backend", "release", "sae_id", "scope")})
    rows.sort(key=lambda row: (row["backend"], row["release"], row["sae_id"]))
    counts = dict(Counter(row["backend"] for row in rows))
    catalog = {
        "schema": "vlmprobe-sae-catalog-v1", "snapshot_date": snapshot_date,
        "counts": {**counts, "overcomplete": 0}, "entry_count": len(rows),
        "resource_kinds": dict(Counter(row["resource_kind"] for row in rows)),
        "numerical_checks": verified,
        "scope": "Author-listed metadata. Registry inclusion does not establish that a checkpoint is an independent-vector SAE or compatible with a native model.",
        "sources": [
            {"backend": "saelens", "source_url": f"https://github.com/decoderesearch/SAELens/blob/{saelens_commit}/sae_lens/pretrained_saes.yaml",
             "source_commit": saelens_commit,
             "registry_versions": sorted({row.get("registry_version", "unknown") for row in rows if row["backend"] == "saelens"}),
             "source_sha256": saelens_yaml_sha256,
             "releases": len({row["release"] for row in rows if row["backend"] == "saelens"})},
            {"backend": "prisma", "source_url": f"https://github.com/Prisma-Multimodal/ViT-Prisma/blob/{prisma_commit}/docs/sae_table.md",
             "source_commit": prisma_commit,
             "metadata_scope": "Every listed repository's Hugging Face file inventory and config were checked; weights were not loaded for the complete catalog."},
            {"backend": "overcomplete", "source_url": f"https://github.com/KempnerInstitute/overcomplete/tree/{overcomplete_commit}",
             "source_commit": overcomplete_commit,
             "metadata_scope": "No central pretrained SAE registry; trained vision backbones are separate resources."},
        ],
        "input_sha256": {"saelens": hashlib.sha256(saelens_path.read_bytes()).hexdigest(),
                         "prisma": hashlib.sha256(prisma_path.read_bytes()).hexdigest()},
        "entries": rows,
    }
    if verification_path is not None:
        catalog["input_sha256"]["verification"] = hashlib.sha256(verification_path.read_bytes()).hexdigest()
    payload = json.dumps(catalog, ensure_ascii=False, separators=(",", ":"), allow_nan=False).encode()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(gzip.compress(payload, compresslevel=9, mtime=0))
    print(json.dumps({"output": str(output), "entries": len(rows), "counts": catalog["counts"],
                      "compressed_bytes": output.stat().st_size}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--saelens-json", type=Path, required=True)
    parser.add_argument("--prisma-json", type=Path, required=True)
    parser.add_argument("--verification-json", type=Path,
                        help="Optional recorded numerical checks; does not imply backbone compatibility")
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parents[1] / "src/vlm_probing/sae/resources/pretrained_catalog.json.gz")
    parser.add_argument("--snapshot-date", default="2026-10-19")
    parser.add_argument("--saelens-commit", default="30c4502466785dd7809a307f7b705df187978aa3")
    parser.add_argument("--saelens-yaml-sha256", default="bea73bf39c2a345ce03fca3d9d44e133085e9ff2aea74c8ae5b26de0819c96d2")
    parser.add_argument("--prisma-commit", default="64daf1425f7e5311844213fd0fb6f4127a30cd16")
    parser.add_argument("--overcomplete-commit", default="a1781af49c6e4bbfdbfd763b9757bcf6c5dd6403")
    options = parser.parse_args()
    build(options.saelens_json, options.prisma_json, options.output,
          verification_path=options.verification_json,
          snapshot_date=options.snapshot_date, saelens_commit=options.saelens_commit,
          saelens_yaml_sha256=options.saelens_yaml_sha256, prisma_commit=options.prisma_commit,
          overcomplete_commit=options.overcomplete_commit)
