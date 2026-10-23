"""Averaged causal transport: https://github.com/anthropics/jacobian-lens."""
from collections.abc import Callable, Mapping
from pathlib import Path
import warnings

import torch
from torch import Tensor

from .base import BaseLens, decoded, floating_tensor, load_artifact, save_artifact
from ..core.types import ProbeResult


class _JacobianReplacementWarning(RuntimeWarning):
    """A one-batch estimate will replace an already calibrated Jacobian."""


def _warn_replacement(*, stacklevel=2):
    warnings.warn(
        "Jacobian Lens fit replaces the existing estimate; it does not accumulate "
        "calibration batches. Use vlmprobe.training.fit_jacobian_lenses(...) for "
        "prompt-weighted dataset calibration.",
        _JacobianReplacementWarning, stacklevel=stacklevel,
    )


def _selector_description(selector):
    if isinstance(selector, Tensor):
        return f"tensor(shape={tuple(selector.shape)}, dtype={selector.dtype})"
    return repr(selector)


def _calibration_selection(layout, tokens):
    """Let Jacobian preflight diagnose an entirely empty, otherwise valid selector."""
    try:
        return layout.select(tokens)
    except ValueError as error:
        if str(error) != "token selection is empty":
            raise
        return torch.zeros_like(layout.valid)


def _calibration_masks(valid, *, source_mask=None, target_mask=None, skip_first=16,
                       exclude_last=True, context="Jacobian calibration"):
    """Apply the reference exclusions and diagnose every failing prompt before VJPs."""
    if not isinstance(skip_first, int) or skip_first < 0:
        raise ValueError("skip_first must be a nonnegative integer")
    shape = tuple(valid.shape)

    def checked(mask, name):
        if mask is None:
            return torch.ones_like(valid)
        if not isinstance(mask, Tensor) or mask.dtype != torch.bool or tuple(mask.shape) != shape:
            raise ValueError(f"{context}: {name} must be boolean with shape {shape}")
        return mask.to(valid.device)

    source_mask, target_mask = checked(source_mask, "source_mask"), checked(target_mask, "target_mask")
    retained = valid.clone()
    for batch in range(len(valid)):
        positions = valid[batch].nonzero(as_tuple=True)[0]
        retained[batch, positions[:skip_first]] = False
        if exclude_last and len(positions):
            retained[batch, positions[-1]] = False
    sources, targets = retained & source_mask, retained & target_mask
    source_counts, target_counts = sources.sum(-1), targets.sum(-1)
    failures = ((source_counts == 0) | (target_counts == 0)).nonzero(as_tuple=True)[0]
    if len(failures):
        minimum = skip_first + int(bool(exclude_last)) + 1
        raise ValueError(
            f"{context}: every prompt must retain at least one source and target position; "
            f"failing rows={failures.tolist()}; valid_counts={valid.sum(-1).tolist()}; "
            f"retained_source_counts={source_counts.tolist()}; "
            f"retained_target_counts={target_counts.tolist()}; "
            f"skip_first={skip_first}, exclude_last={exclude_last}; "
            f"source_mask_counts={source_mask.sum(-1).tolist()}, "
            f"target_mask_counts={target_mask.sum(-1).tolist()}. "
            f"Unrestricted masks need at least {minimum} valid expanded tokens per prompt. "
            "Use longer calibration contexts or explicitly adjust skip_first/exclude_last, "
            "and ensure selectors/masks intersect the retained positions. "
            "With an all-prompt layout, tokens='last_prompt' conflicts with exclude_last=True. "
            "No rows were dropped."
        )
    return sources, targets


class JacobianLens(BaseLens):
    """Fit a source-residual to final-residual average Jacobian at one site.

    ``downstream`` must be a differentiable causal continuation: [B,S,D] to
    [B,S,D_final], with no cross-example coupling. The estimator sums effects
    over valid current/future targets, averages valid sources within each
    prompt, then averages prompts equally. It is not a per-token gradient
    saliency score. This exact output-dimension loop is a small CPU/reference
    implementation; fitting a large VLM requires a separately budgeted job.
    """

    name = "jacobian_lens"
    estimator = "sum_valid_causal_targets_mean_sources_mean_prompts"

    def __init__(
        self, readout: Callable[[Tensor], Tensor], *, binding: Mapping[str, str] | None = None,
    ) -> None:
        self.readout, self.binding = readout, dict(binding or {})
        self.jacobian: Tensor | None = None
        self.calibration: dict[str, object] = {}

    def fit(
        self, activations: Tensor, downstream: Callable[[Tensor], Tensor], *,
        valid_mask: Tensor | None = None, source_mask: Tensor | None = None,
        target_mask: Tensor | None = None, skip_first: int = 16, exclude_last: bool = True,
        max_sources: int | None = None, seed: int = 0,
    ) -> "JacobianLens":
        """Estimate J[out,in]; explicit source/target masks restrict valid positions.

        The default excludes the first sixteen valid tokens and the final valid
        token of each prompt, matching the reference calibration convention.
        Use skip_first=0/exclude_last=False to retain those positions. Optional
        source subsampling draws only from the remaining valid source set.
        Call fit once on the supplied calibration batch; replacing prior J emits
        RuntimeWarning. Use training.fit_jacobian_lenses for multiple batches.
        """
        if torch.is_inference_mode_enabled():
            raise ValueError("Jacobian calibration cannot run inside torch.inference_mode()")
        floating_tensor(activations, "activations", ndim=3)
        if max_sources is not None and (not isinstance(max_sources, int) or max_sources < 1):
            raise ValueError("max_sources must be positive")
        shape = tuple(activations.shape[:2])
        if valid_mask is None:
            valid = torch.ones(shape, dtype=torch.bool, device=activations.device)
        elif (not isinstance(valid_mask, Tensor) or valid_mask.dtype != torch.bool
              or tuple(valid_mask.shape) != shape):
            raise ValueError(f"valid_mask must be boolean with shape {shape}")
        else:
            valid = valid_mask.to(activations.device)
        sources, targets = _calibration_masks(valid, source_mask=source_mask,
            target_mask=target_mask, skip_first=skip_first, exclude_last=exclude_last)
        if self.jacobian is not None:
            _warn_replacement(stacklevel=3)
        if max_sources is not None:
            generator = torch.Generator(device="cpu").manual_seed(seed)
            for batch in range(shape[0]):
                positions = sources[batch].nonzero(as_tuple=True)[0]
                if len(positions) > max_sources:
                    subset = torch.randperm(len(positions), generator=generator)[:max_sources]
                    sources[batch] = False
                    sources[batch, positions[subset.to(positions.device)]] = True
        with torch.enable_grad():
            hidden = activations.detach().clone().requires_grad_(True)
            final = downstream(hidden)
            floating_tensor(final, "downstream final residual", ndim=3)
            if tuple(final.shape[:2]) != shape or not final.requires_grad:
                raise ValueError("downstream must preserve batch/sequence and the differentiable graph")
            rows = []
            for dimension in range(final.shape[-1]):
                objective = (final[..., dimension] * targets).sum()
                gradient = torch.autograd.grad(
                    objective, hidden, retain_graph=dimension + 1 < final.shape[-1],
                )[0]
                # A causal continuation has zero influence on earlier targets.
                per_prompt = (gradient.float() * sources[..., None]).sum(1)
                per_prompt = per_prompt / sources.sum(1)[:, None]
                rows.append(per_prompt.mean(0))
        jacobian = torch.stack(rows).detach()
        floating_tensor(jacobian, "estimated Jacobian", ndim=2)
        self.jacobian = jacobian
        self.calibration = {
            "estimator": self.estimator, "n_prompts": shape[0],
            "source_counts": sources.sum(1).tolist(), "target_counts": targets.sum(1).tolist(),
            "skip_first": skip_first, "exclude_last": exclude_last,
            "max_sources": max_sources, "seed": seed,
            "source_positions": [row.nonzero(as_tuple=True)[0].tolist() for row in sources],
            "target_positions": [row.nonzero(as_tuple=True)[0].tolist() for row in targets],
        }
        return self

    @torch.no_grad()
    def run(self, activations: Tensor, *, layer: int | None = None) -> ProbeResult:
        floating_tensor(activations, "activations")
        if self.jacobian is None:
            raise RuntimeError("fit or load the Jacobian lens before running it")
        if activations.shape[-1] != self.jacobian.shape[-1]:
            raise ValueError("activations do not match the fitted source hidden width")
        # Preserve the caller's dtype for model readout, as in model inference.
        transported = activations @ self.jacobian.to(activations).T
        return ProbeResult(self.name, {"logits": decoded(self.readout, transported),
                                       "transported": transported}, {
            "layer": layer, "binding": dict(self.binding), **self.calibration,
        })

    def save(self, path: str | Path) -> None:
        if self.jacobian is None:
            raise RuntimeError("fit the Jacobian lens before saving it")
        save_artifact(path, self.name, self.binding, {"estimator": self.estimator},
                      {"jacobian": self.jacobian.cpu(), "calibration": self.calibration})

    def load(self, path: str | Path) -> "JacobianLens":
        state = load_artifact(path, self.name, self.binding, {"estimator": self.estimator})
        floating_tensor(state["jacobian"], "artifact Jacobian", ndim=2)
        self.jacobian = state["jacobian"]
        self.calibration = dict(state["calibration"])
        return self
