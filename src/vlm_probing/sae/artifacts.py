"""One tensor-only artifact format for every native sparse dictionary.

Directory artifacts contain config.json, weights.pt and model_card.json.
Single .pt envelopes use the same metadata and are convenient for best-model
checkpoints. Loading never imports an external SAE implementation.
"""
from __future__ import annotations

from dataclasses import asdict
import hashlib
import json
import os
from pathlib import Path

import torch

SCHEMA = "vlmprobe-sae-artifact-v2"
LEGACY_SCHEMA = "vlmprobe-native-sae-v1"


def _json(value):
    try:
        return json.loads(json.dumps(value, allow_nan=False))
    except (TypeError, ValueError) as error:
        raise ValueError("artifact metadata must contain finite JSON values") from error


def file_sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def state_sha256(state):
    digest = hashlib.sha256()
    if not isinstance(state, dict) or not state:
        raise ValueError("artifact state must be a nonempty tensor dictionary")
    for name, value in sorted(state.items()):
        if not isinstance(name, str) or not isinstance(value, torch.Tensor):
            raise ValueError("artifact state must map strings to tensors")
        if value.layout != torch.strided or not torch.isfinite(value).all():
            raise ValueError("artifact tensors must be finite dense tensors")
        tensor = value.detach().cpu().contiguous()
        digest.update(json.dumps([name, list(tensor.shape), str(tensor.dtype)], separators=(",", ":")).encode())
        digest.update(tensor.reshape(-1).view(torch.uint8).numpy().tobytes())
    return digest.hexdigest()


def _atomic_json(value, path):
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n")
    os.replace(temporary, path)


def _atomic_torch(value, path):
    temporary = path.with_name(path.name + ".tmp")
    torch.save(value, temporary)
    os.replace(temporary, path)


def save_artifact(model, path, *, model_card=None, registry_dir=None):
    """Save exact config, binding, all state buffers and a local model card.

    ``registry_dir`` explicitly registers a local card; no user-global registry
    is modified automatically. Inference artifacts remain separate from a
    trainer's optimizer/RNG resume state.
    """
    from .models import validate_sae_binding
    from .cards import make_model_card, register_model_card
    binding = validate_sae_binding(model.binding)
    state = {name: value.detach().cpu() for name, value in model.state_dict().items()}
    checksum = state_sha256(state)
    config = _json(asdict(model.config))
    # JumpReLU keeps its threshold in FP32 even when the encoder is BF16.
    # The inference dtype is the activation projection's dtype, not parameter
    # registration order (which can put that root-level threshold first).
    parameter = model.activation_parameter
    dtype = str(parameter.dtype).removeprefix("torch.")
    metadata = {
        "schema": SCHEMA, "config": config, "binding": binding,
        "dtype": dtype, "state_sha256": checksum,
        "is_fitted": bool(getattr(model, "is_fitted", False)),
        "source_metadata": _json(getattr(model, "source_metadata", {})),
        "training_metadata": _json(getattr(model, "training_metadata", {})),
        "implementation_variant": getattr(model, "implementation_variant", config["architecture"]),
    }
    card = make_model_card(config, binding, state_sha256=checksum,
        is_fitted=metadata["is_fitted"], metadata=model_card,
        source_metadata=metadata["source_metadata"], training_metadata=metadata["training_metadata"])
    path = Path(path)
    if path.suffix in {".pt", ".pth"}:
        path.parent.mkdir(parents=True, exist_ok=True)
        card["artifact"] = {"schema": SCHEMA, "path": path.name, "state_sha256": checksum}
        _atomic_torch({**metadata, "state_dict": state, "model_card": card}, path)
        card_path = path.with_name(path.name + ".model_card.json")
        _atomic_json(card, card_path)
    else:
        path.mkdir(parents=True, exist_ok=True)
        weight_path = path / "weights.pt"
        _atomic_torch(state, weight_path)
        metadata["weights"] = {"filename": "weights.pt", "sha256": file_sha256(weight_path)}
        card["artifact"] = {"schema": SCHEMA, "path": ".", "state_sha256": checksum}
        _atomic_json(metadata, path / "config.json")
        card_path = path / "model_card.json"
        _atomic_json(card, card_path)
    if registry_dir is not None:
        register_model_card(card, registry_dir=registry_dir, artifact_path=path.resolve())
    return path


def _read(path):
    if path.is_dir():
        metadata = json.loads((path / "config.json").read_text())
        if metadata.get("schema") != SCHEMA:
            raise ValueError("not a canonical SAE artifact directory; use import_checkpoint for external formats")
        weights = metadata.get("weights", {})
        filename = weights.get("filename")
        if filename not in {"weights.pt", "weights.safetensors"}:
            raise ValueError("artifact must name its supported tensor weights file")
        weight_path = path / filename
        if file_sha256(weight_path) != weights.get("sha256"):
            raise ValueError("artifact weight-file checksum differs")
        if filename.endswith(".safetensors"):
            from safetensors.torch import load_file
            state = load_file(str(weight_path), device="cpu")
        else:
            state = torch.load(weight_path, map_location="cpu", weights_only=True)
        metadata["state_dict"] = state
        metadata["model_card"] = json.loads((path / "model_card.json").read_text())
    else:
        metadata = torch.load(path, map_location="cpu", weights_only=True)
    if not isinstance(metadata, dict):
        raise ValueError("SAE artifact must contain a safe metadata/tensor envelope")
    return metadata


def load_artifact(path, *, expected_binding=None, device="cpu"):
    """Restore one native model, preserving exact feature order and raw units.

    Native v1 envelopes are upgraded through the canonical model's explicitly
    whitelisted legacy-buffer migration; unrelated external formats are rejected.
    """
    from .models import SAEConfig, SparseAutoencoder, validate_sae_binding
    path = Path(path)
    metadata = _read(path)
    schema = metadata.get("schema")
    if schema not in {SCHEMA, LEGACY_SCHEMA}:
        raise ValueError("unsupported SAE artifact schema; use import_checkpoint for an external format")
    binding = validate_sae_binding(metadata.get("binding"))
    if expected_binding is not None and validate_sae_binding(expected_binding) != binding:
        raise ValueError("SAE checkpoint binding differs from expected model/data/hook identities")
    state = metadata.get("state_dict")
    checksum = state_sha256(state)
    if schema == SCHEMA and checksum != metadata.get("state_sha256"):
        raise ValueError("artifact tensor checksum differs")
    dtype = getattr(torch, metadata.get("dtype", ""), None)
    if dtype not in {torch.float16, torch.bfloat16, torch.float32, torch.float64}:
        raise ValueError("unsupported SAE artifact dtype")
    model = SparseAutoencoder(SAEConfig(**metadata["config"]), binding, device=device, dtype=dtype)
    if schema == LEGACY_SCHEMA:
        from .models import upgrade_legacy_state_dict
        state = upgrade_legacy_state_dict(model, state)
    model.load_state_dict(state, strict=True)
    if not torch.isfinite(model.input_scale).all() or (model.input_scale <= 0).any():
        raise ValueError("artifact normalization scale must be finite and positive")
    model.is_fitted = bool(metadata.get("is_fitted", False))
    model.source_metadata = _json(metadata.get("source_metadata", {}))
    model.training_metadata = _json(metadata.get("training_metadata", {}))
    model.model_card = _json(metadata.get("model_card", {}))
    if schema == LEGACY_SCHEMA:
        model.source_metadata = {**model.source_metadata,
            "conversion": "native_v1_to_canonical_artifact", "source_schema": LEGACY_SCHEMA,
            "source_artifact_sha256": file_sha256(path)}
    model.eval()
    return model
