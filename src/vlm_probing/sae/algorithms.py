"""Provider-independent sparse coding primitives.

JumpReLU/Step surrogate conventions follow the MIT-licensed SAELens reference
(Joseph Bloom and contributors), including the option to pass STE gradients to
the input. Signed TopK follows the MIT-licensed AbsTopK reference (GoXzascc).
Matching pursuit follows its classical greedy residual algorithm. See
docs/sae/methods/README.md and retained source licenses for precise provenance.
No upstream package or vendored SAE class is imported here.
"""
from __future__ import annotations

import torch
from torch import Tensor


def topk(values: Tensor, k: int, *, signed=False) -> Tensor:
    ranked = values.abs() if signed else values
    indices = ranked.topk(k, dim=-1, sorted=False).indices
    selected = values.gather(-1, indices)
    if not signed:
        selected = selected.relu()
    return torch.zeros_like(values).scatter(-1, indices, selected)


def batch_topk(values: Tensor, count: int) -> tuple[Tensor, Tensor | None]:
    positive = values.relu()
    flat = positive.reshape(-1)
    selected, indices = flat.topk(min(count, flat.numel()), sorted=False)
    output = torch.zeros_like(flat).scatter(-1, indices, selected).reshape_as(values)
    nonzero = selected[selected > 0]
    threshold = nonzero.min().detach() if nonzero.numel() else None
    return output, threshold


class JumpReLU(torch.autograd.Function):
    @staticmethod
    def forward(ctx, values, threshold, bandwidth, ste_to_input):
        ctx.save_for_backward(values, threshold)
        ctx.bandwidth, ctx.ste_to_input = bandwidth, ste_to_input
        return values * (values > threshold).to(values)

    @staticmethod
    def backward(ctx, output_gradient):
        values, threshold = ctx.saved_tensors
        window = (((values - threshold) / ctx.bandwidth).abs() < .5).to(values)
        surrogate = threshold / ctx.bandwidth * window * output_gradient
        value_gradient = (values > threshold) * output_gradient
        if ctx.ste_to_input:
            value_gradient = value_gradient + surrogate
        axes = tuple(range(values.ndim - 1))
        threshold_gradient = -surrogate.sum(dim=axes) if axes else -surrogate
        return value_gradient, threshold_gradient, None, None


class Step(torch.autograd.Function):
    @staticmethod
    def forward(ctx, values, threshold, bandwidth, ste_to_input):
        ctx.save_for_backward(values, threshold)
        ctx.bandwidth, ctx.ste_to_input = bandwidth, ste_to_input
        return (values > threshold).to(values)

    @staticmethod
    def backward(ctx, output_gradient):
        values, threshold = ctx.saved_tensors
        window = (((values - threshold) / ctx.bandwidth).abs() < .5).to(values)
        surrogate = window * output_gradient / ctx.bandwidth
        axes = tuple(range(values.ndim - 1))
        threshold_gradient = -surrogate.sum(dim=axes) if axes else -surrogate
        return surrogate if ctx.ste_to_input else None, threshold_gradient, None, None


def matching_pursuit(values: Tensor, dictionary: Tensor, *, iterations: int,
                     signed=False, tolerance=0., stop_on_duplicate=True) -> Tensor:
    """Greedy tied-dictionary encoding; dictionary is [input,feature].

    Selection is discrete, while selected coefficients and dictionary atoms
    retain gradients. Coefficients account for non-unit imported atom norms.
    """
    original_shape = values.shape
    residual = values.reshape(-1, values.shape[-1])
    atoms = dictionary.T
    codes = values.new_zeros(residual.shape[0], atoms.shape[0])
    done = torch.zeros(residual.shape[0], dtype=torch.bool, device=values.device)
    previous_support = torch.zeros_like(codes, dtype=torch.bool)
    norms = atoms.square().sum(-1).clamp_min(torch.finfo(values.dtype).eps)
    for _ in range(iterations):
        with torch.no_grad():
            correlations = residual @ atoms.T
            ranking = correlations.abs() if signed else correlations.relu()
            indices = ranking.argmax(-1, keepdim=True)
        selected = atoms[indices.squeeze(-1)]
        coefficients = (residual * selected).sum(-1, keepdim=True) / norms[indices]
        if not signed:
            coefficients = coefficients.relu()
        coefficients = coefficients * (~done).unsqueeze(-1)
        codes = codes.scatter_add(-1, indices, coefficients)
        residual = residual - coefficients * selected
        with torch.no_grad():
            support = codes != 0
            if stop_on_duplicate:
                done = done | (support == previous_support).all(-1)
                previous_support = support
            if tolerance > 0:
                done = done | (residual.norm(dim=-1) < tolerance)
            if done.all():
                break
    return codes.reshape(*original_shape[:-1], atoms.shape[0])


def orthogonal_matching_pursuit(values: Tensor, dictionary: Tensor, *,
                                iterations: int, signed=False, tolerance=0.,
                                nnls_iterations=32) -> Tensor:
    """Greedy unique support with joint coefficient refits.

    Signed OMP solves least squares on each growing support. Nonnegative OMP
    uses a differentiable projected-gradient NNLS refit with an explicit finite
    iteration budget. The latter is an approximate NNLS solver, not an exact
    active-set solution. Both retain gradients through the selected atoms.
    """
    original_shape = values.shape
    flat = values.reshape(-1, values.shape[-1])
    atoms = dictionary.T
    residual, support = flat, None
    coefficients = None
    for _ in range(min(iterations, atoms.shape[0])):
        with torch.no_grad():
            correlations = residual @ atoms.T
            ranking = correlations.abs() if signed else correlations
            if support is not None:
                ranking = ranking.scatter(-1, support, -torch.inf)
            selected = ranking.argmax(-1, keepdim=True)
            support = selected if support is None else torch.cat((support, selected), -1)
        selected_atoms = atoms[support]  # [position, support, input]
        design = selected_atoms.transpose(-2, -1)
        # torch.linalg CPU/CUDA solvers require fp32/fp64; preserve autograd.
        solve_dtype = torch.float64 if values.dtype == torch.float64 else torch.float32
        design_work, targets = design.to(solve_dtype), flat.to(solve_dtype)
        if signed:
            coefficients = torch.linalg.lstsq(design_work, targets.unsqueeze(-1)).solution.squeeze(-1)
        else:
            gram = design_work.transpose(-2, -1) @ design_work
            rhs = (design_work.transpose(-2, -1) @ targets.unsqueeze(-1)).squeeze(-1)
            with torch.no_grad():
                lipschitz = torch.linalg.eigvalsh(gram).amax(-1, keepdim=True).clamp_min(1e-8)
            coefficients = torch.zeros_like(rhs)
            for _ in range(nnls_iterations):
                gradient = (gram @ coefficients.unsqueeze(-1)).squeeze(-1) - rhs
                coefficients = (coefficients - gradient / lipschitz).relu()
        coefficients = coefficients.to(values.dtype)
        residual = flat - (coefficients.unsqueeze(-1) * selected_atoms).sum(-2)
        if tolerance > 0 and bool((residual.detach().norm(dim=-1) < tolerance).all()):
            break
    codes = flat.new_zeros(len(flat), atoms.shape[0]).scatter(-1, support, coefficients)
    return codes.reshape(*original_shape[:-1], atoms.shape[0])
