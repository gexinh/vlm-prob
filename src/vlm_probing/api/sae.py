"""Model-bound sparse feature readouts and explicit feature interventions."""
import math

import torch

from .common import BoundMethod, evaluate, layers_for, model_eval
from ..core import ProbeResult
from ..sae.binding import check_runtime_binding


class SAEProbe(BoundMethod):
    def __init__(self, probe, layer, sae, checkpoint, binding, tokens, *,
                 feature_ids=None, scale=0., mode="error_preserving"):
        if type(layer) is not int:
            raise ValueError("one SAE artifact must select exactly one integer layer")
        layers_for(probe, layer)
        if (sae is None) == (checkpoint is None):
            raise ValueError("provide exactly one of sae or checkpoint")
        if not isinstance(binding, dict) or not binding:
            raise ValueError("supply the expected checkpoint binding explicitly")
        check_runtime_binding(probe, layer, binding)
        if checkpoint is not None:
            from ..sae.models import SparseAutoencoder
            device = next(probe.model.parameters()).device
            sae = SparseAutoencoder.load(checkpoint, expected_binding=binding, device=device)
        if getattr(sae, "binding", None) != binding:
            raise ValueError("SAE artifact binding does not match expected identities")
        if not getattr(sae, "is_fitted", False):
            raise ValueError("fit or load a trained dictionary before using model-bound SAE methods")
        if mode not in {"error_preserving", "reconstruction"}:
            raise ValueError("mode must be error_preserving or reconstruction")
        if not math.isfinite(scale):
            raise ValueError("scale must be finite")
        if feature_ids is not None:
            feature_ids = list(feature_ids)
            if (not feature_ids or len(set(feature_ids)) != len(feature_ids)
                    or any(type(i) is not int or not 0 <= i < sae.config.d_sae for i in feature_ids)):
                raise ValueError("feature_ids must be nonempty unique dictionary feature indices")
        super().__init__(probe, "sae.edit" if feature_ids is not None else "sae.features", [layer])
        self.sae, self.layer, self.tokens = sae, layer, tokens
        self.feature_ids, self.scale, self.mode = feature_ids, scale, mode

    def _device_dtype(self):
        parameter = next(self.sae.parameters())
        return parameter.device, parameter.dtype

    def _capture(self, inputs):
        site = self.probe.spec.residuals[self.layer]
        trace = self.probe._run(inputs, capture=[site])
        hidden = trace.activations[site]
        if hidden.ndim != 3 or hidden.shape[-1] != self.sae.config.d_in:
            raise ValueError("SAE width must match the native [batch,token,hidden] residual tensor")
        layout = self.probe._layout(inputs, hidden)
        mask = layout.select(self.tokens)
        return trace, hidden, layout, mask, site

    @model_eval
    @torch.no_grad()
    def run(self, inputs, *, metric=None):
        trace, hidden, layout, mask, site = self._capture(inputs)
        device, dtype = self._device_dtype()
        native = hidden[mask.to(hidden.device)]
        values = native.to(device=device, dtype=dtype)
        features = self.sae.encode(values)
        reconstruction = self.sae.decode(features)
        positions = mask.nonzero()
        metadata = {"binding": self.sae.binding, "architecture": self.sae.config.architecture,
                    "visual_only": bool(layout.visual is not None and not (mask & ~layout.visual).any()),
                    "feature_axes": ["selected_position", "dictionary_feature"],
                    "position_axes": ["batch", "expanded_token"],
                    "interpretation": "Dictionary features require empirical interpretation; feature IDs are not named concepts."}
        if self.feature_ids is None:
            result = ProbeResult(self.name, {
                "features": features, "activation": values,
                "reconstruction": reconstruction,
                "reconstruction_error": values - reconstruction,
                "l0": (features != 0).sum(-1), "positions": positions,
            }, metadata)
            return self._finish(result)
        if self.mode == "error_preserving" and self.scale == 1.:
            # Return the same native output exactly, including bfloat16 rounding.
            edited_trace = trace
        else:
            changed = features.clone()
            changed[:, self.feature_ids] *= self.scale
            decoded = self.sae.decode(changed)
            # Form the decoded difference first, then add it to the original
            # native tensor. Casting the baseline through the SAE dtype can
            # corrupt precision even when the selected feature was inactive.
            replacement = (native + (decoded - reconstruction).to(native)
                           if self.mode == "error_preserving" else decoded.to(native))

            def edit(current):
                if current.shape != hidden.shape:
                    raise ValueError("residual geometry changed between baseline and edited forwards")
                output = current.clone()
                output[mask.to(current.device)] = replacement.to(current)
                return output

            edited_trace = self.probe._run(inputs, interventions={site: edit})
        tensors = {"baseline_logits": trace.logits, "edited_logits": edited_trace.logits,
                   "positions": positions}
        if metric is not None:
            baseline = evaluate(metric, trace.logits, layout)
            edited = evaluate(metric, edited_trace.logits, layout)
            tensors.update(baseline_score=baseline, edited_score=edited, score_change=edited - baseline)
        return self._finish(ProbeResult(self.name, tensors, {
            **metadata, "feature_ids": self.feature_ids, "scale": self.scale, "mode": self.mode,
            "intervention": ("native residual plus decoded feature difference; reconstruction error retained"
                             if self.mode == "error_preserving" else "replace selected residuals by SAE reconstruction"),
        }))


class SAEMethods:
    def __init__(self, probe):
        self.probe = probe

    def features(self, *, layer, sae=None, checkpoint=None, binding, tokens="all"):
        """Encode one layer using a trained dictionary; positions are explicit."""
        return SAEProbe(self.probe, layer, sae, checkpoint, binding, tokens)

    def edit(self, *, layer, feature_ids, sae=None, checkpoint=None, binding,
             tokens="all", scale=0., mode="error_preserving"):
        """Scale chosen features, preserving reconstruction error by default."""
        return SAEProbe(self.probe, layer, sae, checkpoint, binding, tokens,
                        feature_ids=feature_ids, scale=scale, mode=mode)
