#!/usr/bin/env python3
"""Apply pinned author-config evidence to the published SAE card catalog.

The checked-in cache contains verbatim author configuration files, their source
commits, and SHA256 hashes. This command is deterministic and offline by default;
``--verify-source`` also checks those immutable URLs against Hugging Face. It
does not load weights, convert dictionaries, or register native loading recipes.
"""
from __future__ import annotations

import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import gzip
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import quote
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
RESOURCES = ROOT / "src/vlm_probing/sae/resources"
CACHE = ROOT / "tools/data/sae_author_configs.json.gz"
METHODS = {
    ("GatedAutoEncoder", "GatedSAETrainer"): "gated",
    ("BatchTopKSAE", "BatchTopKTrainer"): "batchtopk",
    ("MatryoshkaBatchTopKSAE", "MatryoshkaBatchTopKTrainer"): "matryoshka_batchtopk",
}


def read_evidence(path=CACHE):
    payload = json.loads(gzip.decompress(Path(path).read_bytes()))
    if payload.get("schema") != "vlmprobe-author-sae-config-evidence-v1":
        raise ValueError("unsupported author-config evidence schema")
    records = payload["records"]
    if len({row["id"] for row in records}) != len(records):
        raise ValueError("duplicate card IDs in author-config evidence")
    for row in records:
        content = row["content"].encode("utf-8")
        if hashlib.sha256(content).hexdigest() != row["sha256"]:
            raise ValueError(f"source configuration checksum mismatch: {row['id']}")
        if not re.fullmatch(r"[0-9a-f]{40}", row["revision"]):
            raise ValueError("source configuration must pin a full repository commit")
        expected = (f"https://huggingface.co/{row['repo_id']}/resolve/"
                    f"{row['revision']}/{quote(row['path'], safe='/')}")
        if row["url"] != expected:
            raise ValueError("source URL differs from its pinned repository/path")
        config = json.loads(content)
        trainer = config["trainer"]
        if (trainer["dict_class"], trainer["trainer_class"]) not in METHODS:
            raise ValueError("unsupported dictionary/trainer pair in source evidence")
        for field in ("activation_dim", "dict_size"):
            if type(trainer[field]) is not int or trainer[field] < 1:
                raise ValueError(f"invalid source {field}")
        if type(trainer["layer"]) is not int or trainer["layer"] < 0:
            raise ValueError("invalid source layer")
        if trainer["submodule_name"] != f"resid_post_layer_{trainer['layer']}":
            raise ValueError("source submodule/layer require explicit compatible evidence")
        if config["buffer"]["d_submodule"] != trainer["activation_dim"]:
            raise ValueError("source buffer and dictionary activation widths differ")
    return payload


def verify_source(records):
    def verify(row):
        request = Request(row["url"], headers={"User-Agent": "vlmprobe-metadata-audit/1.0"})
        with urlopen(request, timeout=60) as response:
            content = response.read()
        if hashlib.sha256(content).hexdigest() != row["sha256"]:
            raise ValueError(f"live pinned configuration checksum mismatch: {row['id']}")

    with ThreadPoolExecutor(max_workers=8) as pool:
        list(pool.map(verify, records))


def enrich(catalog, evidence):
    """Fill only fields explicitly declared by each author training config."""
    catalog = json.loads(json.dumps(catalog))
    cards = {card["id"]: card for card in catalog["models"]}
    for row in evidence["records"]:
        card = cards[row["id"]]
        if (card["download"]["repo_id"] != row["repo_id"]
                or card["download"]["path"].rstrip("/") + "/config.json" != row["path"]):
            raise ValueError(f"source evidence does not bind the indexed dictionary: {row['id']}")
        config = json.loads(row["content"])
        trainer, buffer = config["trainer"], config["buffer"]
        method = METHODS[(trainer["dict_class"], trainer["trainer_class"])]
        if card["method"] not in {"unknown", method}:
            raise ValueError(f"conflicting published method: {row['id']}")
        card.update(method=method, modality="language",
                    layer=trainer["layer"], hook=trainer["submodule_name"],
                    dimensions={"activation": trainer["activation_dim"], "features": trainer["dict_size"]})
        card["origin"].update(revision=row["revision"], source_architecture=trainer["dict_class"],
                               source_trainer_class=trainer["trainer_class"],
                               source_model_id=trainer["lm_name"], method_metadata_source=row["url"])
        if row.get("checkpoint_license"):
            card["origin"]["checkpoint_license"] = row["checkpoint_license"]
        checkpoint = (f"https://huggingface.co/{row['repo_id']}/tree/{row['revision']}/"
                      + quote(card["download"]["path"], safe="/"))
        card["origin"]["source_url"] = checkpoint
        card["links"].update(config=row["url"], checkpoint=checkpoint)
        card["download"]["revision"] = row["revision"]
        card["input_conventions"].update(context_size=buffer["ctx_len"],
                                            source_activation_io=buffer["io"],
                                            source_submodule=trainer["submodule_name"])
        if "k" in trainer:
            card["input_conventions"]["k"] = trainer["k"]
        card["source_configuration"] = config
        card["evidence"].update(
            metadata_source="upstream_registry_and_pinned_author_config",
            author_config={"url": row["url"], "revision": row["revision"], "sha256": row["sha256"],
                           "verified_date": evidence["verified_date"]})
        # Stable IDs, backbone aliases, titles, card anchors and loading
        # capabilities are retained. The qualified author model ID is recorded
        # separately rather than splitting the published backbone identity.
    catalog["counts"]["methods"] = dict(Counter(
        card["method"] for card in catalog["models"] if card["artifact_kind"] == "sae"))
    source = {"metadata_source": "pinned_author_training_configurations",
              "source_configurations": len(evidence["records"]),
              "repositories": len({row["repo_id"] for row in evidence["records"]}),
              "evidence_cache": "tools/data/sae_author_configs.json.gz",
              "verified_date": evidence["verified_date"]}
    catalog["sources"] = [item for item in catalog["sources"]
                          if item.get("metadata_source") != source["metadata_source"]] + [source]
    return catalog


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify-source", action="store_true", help="verify cached checksums against pinned HF URLs")
    parser.add_argument("--catalog", type=Path, default=RESOURCES / "published_model_cards.json.gz")
    parser.add_argument("--descriptor", type=Path, default=RESOURCES / "native_model_cards.json")
    args = parser.parse_args()
    evidence = read_evidence()
    if args.verify_source:
        verify_source(evidence["records"])
    catalog = enrich(json.loads(gzip.decompress(args.catalog.read_bytes())), evidence)
    data = (json.dumps(catalog, separators=(",", ":"), ensure_ascii=False, allow_nan=False) + "\n").encode()
    args.catalog.write_bytes(gzip.compress(data, mtime=0))
    descriptor = json.loads(args.descriptor.read_text())
    descriptor["counts"] = catalog["counts"]
    args.descriptor.write_text(json.dumps(descriptor, indent=2) + "\n")
    print(json.dumps({"author_configs": len(evidence["records"]), "counts": catalog["counts"]}, indent=2))


if __name__ == "__main__":
    main()
