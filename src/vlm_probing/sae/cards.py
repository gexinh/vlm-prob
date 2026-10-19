"""Published SAE model information and registered native artifacts."""
from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
import gzip
import html
from importlib.resources import files
import json
from pathlib import Path
import re

CARD_SCHEMA = "vlmprobe-sae-model-card-v1"


def _json(value):
    try:
        return json.loads(json.dumps(value, allow_nan=False))
    except (TypeError, ValueError) as error:
        raise ValueError("model cards require finite JSON metadata") from error


def validate_model_card(card):
    card = _json(card)
    if not isinstance(card, dict) or card.get("schema") != CARD_SCHEMA:
        raise ValueError("unsupported SAE model card schema")
    if not isinstance(card.get("id"), str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", card["id"]):
        raise ValueError("model card id must be a simple stable identifier")
    for field in ("title", "method", "status"):
        if not isinstance(card.get(field), str) or not card[field].strip():
            raise ValueError(f"model card requires {field}")
    if card.get("modality") not in {None, "language", "vision", "multimodal", "activation"}:
        raise ValueError("model card modality must be language, vision, multimodal, activation or unknown")
    evidence = card.get("evidence")
    if not isinstance(evidence, dict):
        raise ValueError("model card requires separate numerical and backbone evidence")
    if card.get("artifact_kind", "sae") not in {"sae", "backbone"}:
        raise ValueError("model card artifact_kind must be sae or backbone")
    return card


def make_model_card(config, binding, *, state_sha256, is_fitted=False, metadata=None,
                    source_metadata=None, training_metadata=None):
    """Build an honest local card; a fitted flag is not an experiment result."""
    config, binding = _json(config), _json(binding)
    source_metadata, training_metadata = _json(source_metadata or {}), _json(training_metadata or {})
    supplied = _json(metadata or {})
    method = config["architecture"]
    if supplied.get("method", method) != method:
        raise ValueError("model card method differs from the saved dictionary")
    imported = source_metadata.get("conversion") == "direct_tensor_mapping_to_native_sae"
    completed_training = training_metadata.get("history", {}).get("status") == "complete"
    card = {
        "schema": CARD_SCHEMA,
        "id": supplied.get("id", f"local-{method}-{state_sha256[:16]}"),
        "title": f"{method} SAE on {binding['model_id']}",
        "method": method, "modality": binding.get("modality"),
        "status": "imported" if imported else "trained" if completed_training else "local",
        "base_model": binding["model_id"], "layer": binding["layer"],
        "dimensions": {"activation": config["d_in"], "features": config["d_sae"]},
        "config": config, "binding": binding, "is_fitted": bool(is_fitted),
        "origin": {"kind": "imported_checkpoint" if imported else "local_artifact", "source_metadata": source_metadata},
        "training": training_metadata,
        "evidence": {
            "tensor_integrity": "checksum_recorded",
            "numerical_parity": "not_evaluated",
            "backbone_compatibility": "not_verified" if imported else "caller_declared_binding",
            "semantic_quality": "not_evaluated",
            "training_validation": "reported_by_native_training_run" if completed_training else "not_evaluated",
        },
        "interpretation": "Feature IDs require empirical interpretation. Fitted status and tensor integrity do not establish named concepts.",
    }
    card.update(supplied)
    # Actual tensor/config identity cannot be overwritten by a descriptive card.
    card.update(method=method, config=config, binding=binding,
                dimensions={"activation": config["d_in"], "features": config["d_sae"]},
                is_fitted=bool(is_fitted))
    return validate_model_card(card)


@lru_cache(maxsize=1)
def _builtin_cards():
    resource = files(__package__).joinpath("resources/native_model_cards.json")
    with resource.open("r", encoding="utf-8") as stream:
        payload = json.load(stream)
    catalog_name = payload.get("catalog_resource")
    if catalog_name != "published_model_cards.json.gz":
        raise ValueError("unsupported published SAE catalog resource")
    with files(__package__).joinpath("resources/" + catalog_name).open("rb") as stream:
        catalog = json.loads(gzip.decompress(stream.read()))
    return tuple(validate_model_card(value) for value in catalog["models"])


def _local_cards(registry_dir):
    if registry_dir is None:
        return []
    directory = Path(registry_dir)
    if not directory.exists():
        return []
    paths = [directory] if directory.is_file() else sorted(directory.rglob("*model_card.json"))
    result = []
    for path in paths:
        card = validate_model_card(json.loads(path.read_text()))
        artifact_path = card.get("artifact", {}).get("path")
        if artifact_path is not None:
            candidate = Path(artifact_path)
            candidate = candidate if candidate.is_absolute() else path.parent / candidate
            card["artifact"] = {**card["artifact"], "resolved_path": str(candidate.resolve())}
        result.append(card)
    return result


def list_models(*, modality=None, method=None, status=None, query=None,
                artifact_kind="sae", registry_dir=None, include_builtin=True, limit=None):
    """Search author-published SAE weights and explicit local artifacts.

    Backbone resources are available with artifact_kind="backbone"; use None
    for both kinds. Published information includes direct checkpoint links and
    our own card pages. It does not automatically convert raw author weights.
    """
    if limit is not None and (type(limit) is not int or limit < 1):
        raise ValueError("limit must be a positive integer")
    rows = _builtin_cards() if include_builtin else []
    # An explicitly supplied local card can materialize a particular artifact.
    rows = {card["id"]: card for card in rows}
    rows.update({card["id"]: card for card in _local_cards(registry_dir)})
    selected = []
    for card in sorted(rows.values(), key=lambda value: value["id"]):
        if artifact_kind is not None and card.get("artifact_kind", "sae") != artifact_kind:
            continue
        if modality is not None and card.get("modality") != modality:
            continue
        if method is not None and card["method"] != method:
            continue
        if status is not None and card["status"] != status:
            continue
        if query is not None and query.casefold() not in json.dumps(card).casefold():
            continue
        selected.append(deepcopy(card))
        if limit is not None and len(selected) >= limit:
            break
    return selected


def get_model_card(card_id, *, registry_dir=None):
    # Avoid deep-copying the complete published catalog for one lookup.
    for card in reversed(_local_cards(registry_dir)):
        if card["id"] == card_id:
            return deepcopy(card)
    for card in _builtin_cards():
        if card["id"] == card_id:
            return deepcopy(card)
    raise KeyError(f"unknown native SAE model card: {card_id}")


def register_model_card(card, *, registry_dir, artifact_path=None):
    """Register only in the caller's explicitly selected local directory."""
    card = validate_model_card(card)
    if artifact_path is not None:
        card["artifact"] = {**card.get("artifact", {}), "path": str(Path(artifact_path).resolve())}
    directory = Path(registry_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{card['id']}.model_card.json"
    path.write_text(json.dumps(card, indent=2, ensure_ascii=False, allow_nan=False) + "\n")
    return path


def load_model(card_id, *, binding=None, expected_binding=None, registry_dir=None,
               artifact_dir=None, device="cpu"):
    """Load a registered artifact using its saved native binding.

    The model-bound public loader additionally verifies the actual runtime
    backbone and processor fingerprints. Author-published raw checkpoints need
    an explicit supported conversion before they become native artifacts.
    """
    from .artifacts import load_artifact
    from .models import validate_sae_binding
    card = get_model_card(card_id, registry_dir=registry_dir)
    local = artifact_dir or card.get("artifact", {}).get("resolved_path")
    if local is None:
        raise ValueError("published checkpoint information is not a native artifact; download its weights and use import_checkpoint, or supply artifact_dir for a converted artifact")
    if binding is None:
        binding = expected_binding
    if binding is None and local is not None:
        # A local native card records the saved identities. The model-bound
        # loader verifies those identities against the actual runtime model.
        binding = card.get("binding")
    if binding is None:
        raise ValueError("supply the expected native model/hook/preprocessing binding")
    binding = validate_sae_binding(binding)
    if expected_binding is not None and validate_sae_binding(expected_binding) != binding:
        raise ValueError("expected binding differs from the supplied binding")
    return load_artifact(local, expected_binding=binding, device=device)


def render_model_card(card, path):
    """Write a readable Markdown or standalone HTML view of the same metadata."""
    card = validate_model_card(card)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    dimensions = card.get("dimensions", {})
    lines = [f"# {card['title']}", "", f"**Model ID:** `{card['id']}`", "",
        f"**Method:** {card['method']} · **Modality:** {card.get('modality') or 'unknown'} · **Status:** {card['status']}", "",
        f"Activation width: {dimensions.get('activation', 'unknown')}; dictionary features: {dimensions.get('features', 'unknown')}.", "",
        "## Evidence", ""]
    lines += [f"- **{key.replace('_', ' ')}:** {value}" for key, value in card["evidence"].items()]
    lines += ["", card.get("interpretation", ""), "", "## Complete metadata", "", "```json", json.dumps(card, indent=2, ensure_ascii=False), "```", ""]
    markdown = "\n".join(lines)
    if path.suffix.lower() == ".html":
        title = html.escape(card["title"])
        content = f"<!doctype html><html lang='en'><meta charset='utf-8'><meta name='viewport' content='width=device-width'><title>{title}</title><style>body{{font:16px system-ui;max-width:1000px;margin:3rem auto;padding:0 1.5rem;color:#172b44}}pre{{white-space:pre-wrap;background:#f2f5fa;padding:1.4rem;border-radius:10px;line-height:1.5}}h1{{color:#17657a}}p{{line-height:1.6}}</style><h1>{title}</h1><p>Native VLMProbe model card. Method: <b>{html.escape(card['method'])}</b>. Status: <b>{html.escape(card['status'])}</b>.</p><pre>{html.escape(markdown)}</pre></html>"
        path.write_text(content)
    else:
        path.write_text(markdown)
    return path
