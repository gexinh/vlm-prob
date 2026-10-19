"""Optional SAELens v6 inference adapter; importing this module is lightweight.

External model/hook compatibility is declared explicitly by the caller and
validated by the model-bound API. Matching widths alone never establish it.
Only SAELens ``normalize_activations='none'`` is accepted in this first adapter;
per-token or external scaling cannot safely be inverted without its full state.
"""
from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version
from types import SimpleNamespace
from typing import Any

import torch
from torch import Tensor, nn

from .models import validate_sae_binding


class SAELensAdapter(nn.Module):
    """Wrap a caller-loaded pretrained SAE using native encode/decode.

    ``binding`` must describe the exact model, native hook and calibration
    provenance. Metadata about the backend hook is retained, not silently
    translated from TransformerLens hook names to native HF module names.
    The current VLMProbe model adapter checks the declared native hook again.
    """

    def __init__(self, sae: nn.Module, binding: dict[str, Any], *,
                 expected_binding: dict[str, Any] | None = None,
                 source_metadata: dict[str, Any] | None = None):
        super().__init__()
        if not isinstance(sae, nn.Module) or not callable(getattr(sae, "encode", None)) or not callable(getattr(sae, "decode", None)):
            raise TypeError("a loaded SAELens nn.Module with encode/decode is required")
        self.binding = validate_sae_binding(binding)
        if expected_binding is not None and validate_sae_binding(expected_binding) != self.binding:
            raise ValueError("external SAE binding differs from expected native model/hook identities")
        config = getattr(sae, "cfg", None)
        if config is None or getattr(config, "normalize_activations", None) != "none":
            raise ValueError("SAELens v1 adapter accepts only explicit normalize_activations='none'; other scaling is unsupported")
        if type(getattr(config, "apply_b_dec_to_input", None)) is not bool:
            raise ValueError("external SAE must explicitly specify apply_b_dec_to_input")
        if getattr(config, "reshape_activations", "none") != "none":
            raise ValueError("head reshaping requires a separate explicitly verified adapter")
        d_in, d_sae = getattr(config, "d_in", None), getattr(config, "d_sae", None)
        if any(type(value) is not int or value < 1 for value in (d_in, d_sae)):
            raise ValueError("external SAE dimensions must be explicit positive integers")
        architecture = config.architecture() if callable(getattr(config, "architecture", None)) else getattr(config, "architecture", None)
        if not isinstance(architecture, str) or not architecture:
            raise ValueError("external SAE architecture must be explicit")
        self.sae = sae
        self.config = SimpleNamespace(d_in=d_in, d_sae=d_sae,
                                      architecture="saelens:" + architecture)
        metadata = getattr(config, "metadata", None)
        hook_layer = getattr(metadata, "hook_layer", None) if metadata is not None else None
        if hook_layer is not None and hook_layer != self.binding["layer"]:
            raise ValueError("SAELens declared layer differs from explicit native binding")
        backend_model = getattr(metadata, "model_name", None) if metadata is not None else None
        if backend_model is not None:
            expected_model = self.binding.get("backend_model_name", self.binding["model_id"].split("@", 1)[0])
            if backend_model != expected_model:
                raise ValueError("SAELens declared model differs from explicit native/source model binding")
        backend_hook = getattr(metadata, "hook_name", None) if metadata is not None else None
        if backend_hook is not None and self.binding.get("backend_hook_name") != backend_hook:
            raise ValueError("declare the exact SAELens backend_hook_name alongside the verified native hook; automatic hook translation is unsupported")
        backend_tokenizer = getattr(metadata, "tokenizer_name", None) if metadata is not None else None
        if backend_tokenizer is not None:
            expected_tokenizer = self.binding.get("backend_tokenizer_name", self.binding["tokenizer_id"].split("@", 1)[0])
            if backend_tokenizer != expected_tokenizer:
                raise ValueError("SAELens declared tokenizer differs from explicit tokenizer binding")
        self.source_metadata = {"backend": "sae-lens-v6", "architecture": architecture,
            "normalize_activations": "none", "apply_b_dec_to_input": config.apply_b_dec_to_input,
            "backend_hook_name": backend_hook, "backend_model_name": backend_model,
            "compatibility": "explicit caller-declared native model/module/tokenizer binding; no dimension-based inference",
            **(source_metadata or {})}
        self.is_fitted = True

    def encode(self, raw: Tensor) -> Tensor:
        if not isinstance(raw, Tensor) or raw.ndim < 1 or raw.shape[-1] != self.config.d_in:
            raise ValueError("external SAE input must match its bound activation width")
        return self.sae.encode(raw)

    def decode(self, features: Tensor) -> Tensor:
        if not isinstance(features, Tensor) or features.ndim < 1 or features.shape[-1] != self.config.d_sae:
            raise ValueError("external SAE features must match its dictionary width")
        return self.sae.decode(features)

    def forward(self, raw: Tensor) -> tuple[Tensor, Tensor]:
        features = self.encode(raw)
        return self.decode(features), features

    @classmethod
    def from_pretrained(cls, release: str, sae_id: str, *, binding: dict[str, Any],
                        device="cpu", dtype="float32",
                        expected_binding: dict[str, Any] | None = None) -> "SAELensAdapter":
        """Use the verified v6 API; this is the only optional import location."""
        validate_sae_binding(binding)
        if expected_binding is not None and validate_sae_binding(expected_binding) != validate_sae_binding(binding):
            raise ValueError("external SAE binding differs from expected native identities")
        try:
            installed = version("sae-lens")
        except PackageNotFoundError as error:
            raise ImportError("install the optional sae-lens v6 dependency to load external dictionaries") from error
        if installed.split(".")[0] != "6":
            raise ValueError(f"external loader is verified for sae-lens v6, got {installed}")
        from sae_lens import SAE
        # SAELens v6 returns an SAE object. The v5 three-tuple API is now named
        # from_pretrained_with_cfg_and_sparsity and is intentionally not guessed.
        sae = SAE.from_pretrained(release=release, sae_id=sae_id, device=device, dtype=dtype)
        return cls(sae, binding, expected_binding=expected_binding,
                   source_metadata={"backend_version": installed, "release": release, "sae_id": sae_id})
