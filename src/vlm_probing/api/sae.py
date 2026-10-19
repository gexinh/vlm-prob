"""Model-bound sparse feature readouts and explicit feature interventions."""
import math

import torch

from .common import BoundMethod, evaluate, layers_for, model_eval
from ..core import ProbeResult
from ..sae.binding import check_runtime_binding


class SAEProbe(BoundMethod):
    def __init__(self, probe, layer, sae, checkpoint, binding, tokens, *,
                 feature_ids=None, scale=0., mode="error_preserving", operation=None, top_k=10):
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
        operation = operation or ("edit" if feature_ids is not None else "features")
        if operation not in {"features", "edit", "profile", "reconstruct"}:
            raise ValueError("unknown SAE operation")
        if type(top_k) is not int or top_k < 1:
            raise ValueError("top_k must be a positive integer")
        super().__init__(probe, "sae." + operation, [layer])
        self.sae, self.layer, self.tokens = sae, layer, tokens
        self.feature_ids, self.scale, self.mode = feature_ids, scale, mode
        self.operation, self.top_k = operation, top_k

    def _encode(self, values):
        contextual = callable(getattr(self.sae, "encode_with_context", None))
        if contextual != callable(getattr(self.sae, "decode_with_context", None)):
            raise ValueError("context-aware dictionaries must provide both encode and decode context methods")
        features, context = self.sae.encode_with_context(values) if contextual else (self.sae.encode(values), None)
        if (not isinstance(features, torch.Tensor) or features.shape != (values.shape[0], self.sae.config.d_sae)
                or not torch.isfinite(features).all()):
            raise ValueError("SAE features must be finite [selected_position,dictionary_feature]")
        return features, context, contextual

    def _decode(self, features, context, contextual):
        decoded = (self.sae.decode_with_context(features, context) if contextual else self.sae.decode(features))
        if (not isinstance(decoded, torch.Tensor) or decoded.shape != (features.shape[0], self.sae.config.d_in)
                or not torch.isfinite(decoded).all()):
            raise ValueError("SAE reconstruction must be finite [selected_position,native_width]")
        return decoded

    def _output(self, trace):
        if self.probe.spec.output_kind != "representation":
            return trace.logits
        if not isinstance(trace.output, torch.Tensor):
            raise TypeError("representation adapters must return a tensor of native output vectors")
        return trace.output

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
        features, context, contextual = self._encode(values)
        reconstruction = self._decode(features, context, contextual)
        positions = mask.nonzero()
        metadata = {"binding": self.sae.binding, "architecture": self.sae.config.architecture,
                    "backend": getattr(self.sae, "source_metadata", {}).get("backend", "native"),
                    "source": getattr(self.sae, "source_metadata", {}),
                    "output_kind": self.probe.spec.output_kind,
                    "normalization_context_preserved": contextual,
                    "visual_only": bool(layout.visual is not None and not (mask & ~layout.visual).any()),
                    "feature_axes": ["selected_position", "dictionary_feature"],
                    "position_axes": ["batch", "expanded_token"],
                    "interpretation": "Dictionary features require empirical interpretation; feature IDs are not named concepts."}
        if self.operation == "profile":
            indices = features.abs().topk(min(self.top_k, len(features)), dim=0).indices
            return self._finish(ProbeResult(self.name, {
                "mean_activation": features.mean(0),
                "activation_variance": features.var(0, unbiased=False),
                "firing_frequency": (features != 0).float().mean(0),
                "max_activation": features.max(0).values, "min_activation": features.min(0).values,
                "top_activation_values": features.gather(0, indices),
                "top_positions": positions.to(indices.device)[indices],
                "positions": positions,
            }, {**metadata, "ranking": "absolute activation per feature; signed values retained"}))
        if self.operation == "features":
            result = ProbeResult(self.name, {
                "features": features, "activation": values,
                "reconstruction": reconstruction,
                "reconstruction_error": values - reconstruction,
                "l0": (features != 0).sum(-1), "positions": positions,
            }, metadata)
            return self._finish(result)
        if self.operation != "reconstruct" and self.mode == "error_preserving" and self.scale == 1.:
            # Return the same native output exactly, including bfloat16 rounding.
            edited_trace = trace
        else:
            changed = features.clone()
            if self.operation != "reconstruct":
                changed[:, self.feature_ids] *= self.scale
            decoded = self._decode(changed, context, contextual)
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
        baseline_output, edited_output = self._output(trace), self._output(edited_trace)
        output_name = "output" if self.probe.spec.output_kind == "representation" else "logits"
        tensors = {"baseline_" + output_name: baseline_output, "edited_" + output_name: edited_output,
                   "positions": positions}
        if metric is not None:
            if self.probe.spec.output_kind == "representation":
                from ..metrics import ClassScore, TokenMargin, SequenceLogProb
                if isinstance(metric, (ClassScore, TokenMargin, SequenceLogProb)):
                    raise ValueError("representation outputs require a vector metric, not a language/classification logit score")
            baseline = evaluate(metric, baseline_output, layout)
            edited = evaluate(metric, edited_output, layout)
            tensors.update(baseline_score=baseline, edited_score=edited, score_change=edited - baseline)
        return self._finish(ProbeResult(self.name, tensors, {
            **metadata, "feature_ids": self.feature_ids, "scale": self.scale, "mode": self.mode,
            "intervention": ("native residual plus decoded feature difference; reconstruction error retained"
                             if self.mode == "error_preserving" else "replace selected residuals by SAE reconstruction"),
        }))


class SAEMethods:
    def __init__(self, probe):
        self.probe = probe

    def load(self, backend, *, binding, **kwargs):
        """Load an external SAE after validating its declared runtime hook."""
        from ..sae.providers import load_sae
        check_runtime_binding(self.probe, binding.get("layer"), binding)
        return load_sae(backend, binding=binding, **kwargs)

    def features(self, *, layer, sae=None, checkpoint=None, binding, tokens="all"):
        """Encode one layer using a trained dictionary; positions are explicit."""
        return SAEProbe(self.probe, layer, sae, checkpoint, binding, tokens)

    def edit(self, *, layer, feature_ids, sae=None, checkpoint=None, binding,
             tokens="all", scale=0., mode="error_preserving"):
        """Scale chosen features, preserving reconstruction error by default."""
        return SAEProbe(self.probe, layer, sae, checkpoint, binding, tokens,
                        feature_ids=feature_ids, scale=scale, mode=mode)

    def profile(self, *, layer, sae=None, checkpoint=None, binding, tokens="all", top_k=10):
        """Summarize feature firing and retrieve top positions by absolute activation."""
        return SAEProbe(self.probe, layer, sae, checkpoint, binding, tokens,
                        operation="profile", top_k=top_k)

    def reconstruct(self, *, layer, sae=None, checkpoint=None, binding, tokens="all"):
        """Replace selected states by the reconstruction as a separate control."""
        return SAEProbe(self.probe, layer, sae, checkpoint, binding, tokens,
                        operation="reconstruct", mode="reconstruction")
