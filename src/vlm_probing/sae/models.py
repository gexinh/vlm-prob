"""Small native SAE kernels with explicit data/model binding and raw-space IO.

The trainable dictionary operates on ``raw_activation / input_scale``. The
single scalar scale is fitted on training activations only and is saved as a
buffer. ``decode`` returns native activation coordinates, including that scale.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import math
import os
from pathlib import Path
from typing import Any

import torch
from torch import Tensor, nn
from torch.nn import functional as F


@dataclass(frozen=True)
class SAEConfig:
    architecture: str
    d_in: int
    d_sae: int
    k: int = 32
    l1_coefficient: float = .01
    seed: int = 0

    def __post_init__(self):
        if self.architecture not in {"relu", "topk", "gated"}:
            raise ValueError("architecture must be relu, topk or gated")
        if any(type(value) is not int or value < 1 for value in (self.d_in, self.d_sae)):
            raise ValueError("d_in and d_sae must be positive integers")
        if type(self.k) is not int or self.k < 1 or (self.architecture == "topk" and self.k > self.d_sae):
            raise ValueError("k must be positive and cannot exceed d_sae for TopK")
        if not math.isfinite(self.l1_coefficient) or self.l1_coefficient < 0:
            raise ValueError("l1_coefficient must be finite and nonnegative")
        if type(self.seed) is not int or not 0 <= self.seed < 2 ** 63:
            raise ValueError("seed must be an integer in [0, 2**63)")


def validate_sae_binding(binding: dict[str, Any]) -> dict[str, Any]:
    """Return a JSON-normalized exact identity; never infer hook compatibility."""
    if not isinstance(binding, dict) or not binding or any(not isinstance(key, str) for key in binding):
        raise ValueError("SAE binding must be a nonempty JSON dictionary with string keys")
    try:
        value = json.loads(json.dumps(binding, allow_nan=False))
    except (TypeError, ValueError) as error:
        raise ValueError("SAE binding must contain finite JSON values") from error
    for name in ("model_id", "tokenizer_id", "preprocessing_id", "calibration_id", "site"):
        item = value.get(name)
        if not isinstance(item, str) or not item.strip() or item.strip().lower() == "unspecified":
            raise ValueError(f"SAE binding requires an explicit nonempty {name}")
    if type(value.get("layer")) is not int or value["layer"] < 0:
        raise ValueError("SAE binding requires a nonnegative integer layer")
    hook = value.get("hook")
    if not isinstance(hook, dict) or not {"module", "kind", "selector", "tensor_slice"} <= hook.keys():
        raise ValueError("SAE binding hook requires actual module, kind, selector and tensor_slice")
    if not isinstance(hook["module"], str) or not hook["module"].strip() or hook["kind"] not in {"input", "output"}:
        raise ValueError("SAE binding must identify the actual nonempty module and hook kind")
    if hook["selector"] is not None and not isinstance(hook["selector"], (int, str)):
        raise ValueError("hook selector must be an integer, string or None")
    if hook["kind"] == "input" and hook["selector"] is None:
        raise ValueError("input hook binding requires its positional or keyword selector")
    selection = hook["tensor_slice"]
    if selection is not None and (not isinstance(selection, list) or len(selection) != 2
            or any(type(item) is not int for item in selection) or not 0 <= selection[0] < selection[1]):
        raise ValueError("hook tensor_slice must be None or [start, stop] with 0 <= start < stop")
    return value


class SparseAutoencoder(nn.Module):
    """ReLU+L1, per-token TopK, or tied-direction Gated SAE.

    Decoder columns are constrained to unit length by ``normalize_decoder_``;
    trainers call it after optimizer steps. TopK implements the core per-token
    TopK/ReLU reconstruction objective and does not claim the paper's AuxK
    dead-feature training recipe. Gated uses a frozen decoder in its auxiliary
    gate-reconstruction path, with detached auxiliary centering bias as well.
    """

    def __init__(self, config: SAEConfig, binding: dict[str, Any],
                 device: str | torch.device = "cpu", dtype: torch.dtype = torch.float32):
        super().__init__()
        if not isinstance(config, SAEConfig):
            raise TypeError("config must be SAEConfig")
        if dtype not in {torch.float16, torch.bfloat16, torch.float32, torch.float64}:
            raise ValueError("SAE dtype must be a supported floating-point dtype")
        self.config, self.binding = config, validate_sae_binding(binding)
        self.is_fitted = False
        # Local CPU initialization restores global RNG state and avoids seeding
        # unrelated CUDA workloads owned by the caller.
        with torch.random.fork_rng(devices=[]):
            torch.random.default_generator.manual_seed(config.seed)
            self.encoder = nn.Linear(config.d_in, config.d_sae, bias=True)
            self.decoder = nn.Linear(config.d_sae, config.d_in, bias=True)
            if config.architecture == "gated":
                self.magnitude_bias = nn.Parameter(torch.zeros(config.d_sae))
                self.log_magnitude_scale = nn.Parameter(torch.zeros(config.d_sae))
            self.register_buffer("input_scale", torch.tensor(1.))
            with torch.no_grad():
                nn.init.normal_(self.decoder.weight)
                self.normalize_decoder_()
                self.encoder.weight.copy_(self.decoder.weight.T)
                self.encoder.bias.zero_()
                self.decoder.bias.zero_()
        self.to(device=device, dtype=dtype)

    def _input(self, value: Tensor, width: int, label: str) -> Tensor:
        if not isinstance(value, Tensor) or not value.is_floating_point() or value.ndim < 1 or value.shape[-1] != width:
            raise ValueError(f"{label} must be floating [...,{width}]")
        if value.numel() == 0 or not torch.isfinite(value).all():
            raise ValueError(f"{label} must contain finite, nonempty values")
        return value.to(self.encoder.weight)

    def _encode_normalized(self, normalized: Tensor) -> tuple[Tensor, Tensor]:
        centered = normalized - self.decoder.bias
        gate = self.encoder(centered)
        if self.config.architecture == "relu":
            features = gate.relu()
        elif self.config.architecture == "topk":
            values, indices = gate.topk(self.config.k, dim=-1, sorted=False)
            features = torch.zeros_like(gate).scatter(-1, indices, values.relu())
        else:
            weight = self.encoder.weight * self.log_magnitude_scale.exp()[:, None]
            magnitude = F.linear(centered, weight, self.magnitude_bias).relu()
            features = (gate > 0).to(magnitude.dtype) * magnitude
        return features, gate

    def encode(self, raw: Tensor) -> Tensor:
        raw = self._input(raw, self.config.d_in, "activations")
        return self._encode_normalized(raw / self.input_scale)[0]

    def decode(self, features: Tensor) -> Tensor:
        features = self._input(features, self.config.d_sae, "features")
        return self.decoder(features) * self.input_scale

    def forward(self, raw: Tensor) -> tuple[Tensor, Tensor]:
        features = self.encode(raw)
        return self.decode(features), features

    def loss(self, raw: Tensor) -> dict[str, Tensor]:
        raw = self._input(raw, self.config.d_in, "activations")
        normalized = raw / self.input_scale
        features, gate = self._encode_normalized(normalized)
        reconstruction = (self.decoder(features) - normalized).square().sum(-1).mean()
        zero = reconstruction.new_zeros(())
        sparsity, auxiliary = zero, zero
        if self.config.architecture == "relu":
            sparsity = self.config.l1_coefficient * features.abs().sum(-1).mean()
        elif self.config.architecture == "gated":
            sparsity = self.config.l1_coefficient * gate.relu().sum(-1).mean()
            # The discrete main gate has no useful threshold gradient. The
            # rectified auxiliary gate learns reconstruction through a fixed
            # decoder, preventing that auxiliary task from moving its columns.
            auxiliary_gate = F.linear(normalized - self.decoder.bias.detach(),
                                      self.encoder.weight, self.encoder.bias).relu()
            auxiliary_reconstruction = F.linear(auxiliary_gate,
                self.decoder.weight.detach(), self.decoder.bias.detach())
            auxiliary = (auxiliary_reconstruction - normalized).square().sum(-1).mean()
        return {"loss": reconstruction + sparsity + auxiliary,
                "reconstruction": reconstruction, "sparsity": sparsity,
                "auxiliary": auxiliary}

    @torch.no_grad()
    def normalize_decoder_(self) -> "SparseAutoencoder":
        """Project every decoder feature direction (column) to unit L2 norm."""
        norm = self.decoder.weight.norm(dim=0, keepdim=True)
        if not torch.isfinite(norm).all() or (norm <= 0).any():
            raise ValueError("decoder columns must be finite and nonzero before normalization")
        self.decoder.weight.div_(norm)
        return self

    @torch.no_grad()
    def initialize_bias_(self, raw_mean: Tensor) -> "SparseAutoencoder":
        """Initialize the normalized decoder bias from the raw TRAIN mean."""
        if self.is_fitted:
            raise ValueError("bias initialization requires an unfitted dictionary")
        raw_mean = self._input(raw_mean, self.config.d_in, "training mean")
        if raw_mean.ndim != 1:
            raise ValueError("training mean must be one [d_in] vector")
        self.decoder.bias.copy_(raw_mean / self.input_scale)
        return self

    @torch.no_grad()
    def set_normalization_(self, train_rms: float | Tensor) -> "SparseAutoencoder":
        """Set raw-coordinate scalar RMS fitted on the TRAIN split only.

        Call before ``initialize_bias_`` and optimization. This changes the
        preprocessing contract; it is not an inference-time rescaling option.
        """
        if self.is_fitted:
            raise ValueError("normalization changes require an unfitted dictionary")
        scale = torch.as_tensor(train_rms, device=self.input_scale.device, dtype=self.input_scale.dtype)
        if scale.numel() != 1 or not torch.isfinite(scale).all() or scale <= 0:
            raise ValueError("training RMS must be a finite positive scalar")
        self.input_scale.copy_(scale.reshape(()))
        return self

    def save(self, path: str | Path) -> None:
        """Save portable tensor-only weights plus exact JSON-safe identities."""
        binding = validate_sae_binding(self.binding)
        if not all(torch.isfinite(value).all() for value in self.state_dict().values()):
            raise ValueError("cannot save nonfinite SAE parameters")
        variants = {"relu": "relu_l1_unit_decoder_columns",
                    "topk": "per_token_topk_relu_core_mse_without_auxk",
                    "gated": "gated_frozen_decoder_aux_and_detached_aux_centering"}
        artifact = {"schema": "vlmprobe-native-sae-v1", "config": asdict(self.config),
                    "binding": binding, "dtype": str(self.encoder.weight.dtype).removeprefix("torch."),
                    "state_dict": {key: value.detach().cpu() for key, value in self.state_dict().items()},
                    "is_fitted": bool(self.is_fitted),
                    "implementation_variant": variants[self.config.architecture],
                    "loss_units": "mean activation vectors of summed squared normalized coordinates; sparsity coefficient included",
                    "normalization": "raw activation divided by saved positive scalar training RMS; decoder returns raw coordinates"}
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_name(path.name + ".tmp")
        torch.save(artifact, temporary)
        os.replace(temporary, path)

    @classmethod
    def load(cls, path: str | Path, expected_binding: dict[str, Any] | None = None,
             device: str | torch.device = "cpu") -> "SparseAutoencoder":
        artifact = torch.load(path, map_location="cpu", weights_only=True)
        if not isinstance(artifact, dict) or artifact.get("schema") != "vlmprobe-native-sae-v1":
            raise ValueError("unsupported native SAE artifact schema")
        binding = validate_sae_binding(artifact["binding"])
        if expected_binding is not None and validate_sae_binding(expected_binding) != binding:
            raise ValueError("SAE checkpoint binding differs from expected model/data/hook identities")
        dtype = {"float16": torch.float16, "bfloat16": torch.bfloat16,
                 "float32": torch.float32, "float64": torch.float64}.get(artifact["dtype"])
        if dtype is None:
            raise ValueError("unsupported SAE artifact dtype")
        model = cls(SAEConfig(**artifact["config"]), binding, device=device, dtype=dtype)
        model.load_state_dict(artifact["state_dict"], strict=True)
        if model.input_scale.ndim or not torch.isfinite(model.input_scale) or model.input_scale <= 0:
            raise ValueError("artifact RMS normalization must be a finite positive scalar")
        if not all(torch.isfinite(value).all() for value in model.state_dict().values()):
            raise ValueError("artifact SAE parameters must be finite")
        model.is_fitted = bool(artifact["is_fitted"])
        return model
