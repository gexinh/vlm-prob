"""Sparse feature maps use explicit native visual geometry, never guessed grids."""
import torch

from .attention import plot_attention_overlay


def plot_sae_feature_overlay(image, result, *, feature_id, grid_shape,
                             batch_index=0, image_alpha=.2, alpha=1., ax=None, **kwargs):
    """Plot one dictionary feature over the exact image passed to the model.

    Run ``probe.sae.features(tokens='visual')`` first. A model-specific image
    transform and grid must be supplied by the caller; mixed text/image
    positions, multiple images and adaptive tiling are not inferred.
    """
    values, positions = result.tensors["features"], result.tensors["positions"]
    if not result.metadata.get("visual_only", False):
        raise ValueError("feature overlays require exclusively visual token positions")
    if type(feature_id) is not int or not 0 <= feature_id < values.shape[-1]:
        raise ValueError("feature_id must be a dictionary index")
    if len(grid_shape) != 2 or any(type(n) is not int or n <= 0 for n in grid_shape):
        raise ValueError("grid_shape must contain two positive integers")
    selected = positions[:, 0] == batch_index
    if int(selected.sum()) != grid_shape[0] * grid_shape[1]:
        raise ValueError("selected positions do not match the declared visual grid")
    heatmap = values[selected, feature_id].detach().float().cpu().reshape(grid_shape)
    kwargs.setdefault("value_label", "Feature activation")
    return plot_attention_overlay(image, heatmap, image_alpha=image_alpha,
                                  alpha=alpha, ax=ax, **kwargs)


def plot_sae_activity(result, *, top_k=20, ax=None):
    """Show feature firing frequency over the selected positions."""
    from ._common import axes
    values = result.tensors["features"]
    if type(top_k) is not int or not 1 <= top_k <= values.shape[-1]:
        raise ValueError("top_k must be between one and the dictionary width")
    frequency = (values != 0).float().mean(0).cpu()
    scores, indices = torch.topk(frequency, top_k)
    ax = axes(ax, figsize=(9, 3))
    ax.bar(range(top_k), scores.numpy(), color="#7350cf")
    ax.set_xticks(range(top_k), [str(i) for i in indices.tolist()], rotation=45)
    ax.set(xlabel="Dictionary feature ID", ylabel="Fraction of selected positions active", ylim=(0, 1))
    return ax
