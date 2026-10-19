"""Pinned Overcomplete metric dependency subset; see VENDOR_MANIFEST.json."""
import torch

Epsilon = 1e-6


def l2(v, dims=None):
    """
    Compute the L2 norm, across 'dims'.

    Parameters
    ----------
    v : torch.Tensor
        Input tensor.
    dims : tuple, optional
        Dimensions over which to compute the L2 norm, by default None.

    Returns
    -------
    torch.Tensor
        L2 norm of v if dims=None else L2 norm across dims.
    """
    if dims is None:
        return v.square().sum().sqrt()
    return v.square().sum(dims).sqrt()



def l1(v, dims=None):
    """
    Compute the L1 norm, across 'dims'.

    Parameters
    ----------
    v : torch.Tensor
        Input tensor.
    dims : tuple, optional
        Dimensions over which to compute the L1 norm, by default None.

    Returns
    -------
    torch.Tensor
        L1 norm of v if dims=None else L1 for across dims.
    """
    if dims is None:
        return torch.abs(v).sum()
    return torch.abs(v).sum(dims)



def lp(v, p=0.5, dims=None):
    """
    Compute the Lp norm, across 'dims'.

    Parameters
    ----------
    v : torch.Tensor
        Input tensor.
    p : float, optional
        Power of the norm, by default 0.5.
    dims : tuple, optional
        Dimensions over which to compute the Lp norm, by default None.

    Returns
    -------
    torch.Tensor
        Lp norm of v if dims=None else Lp norm across dims.
    """
    if dims is None:
        return torch.norm(v, p)
    return torch.norm(v, p, dims)



def l0_eps(x, dims=None, threshold=1e-6):
    """
    Compute the l0 norm allowing for an epsilon tolerance.

    Parameters
    ----------
    x : torch.Tensor
        Input tensor.
    dims : tuple, optional
        Dimensions over which to average the l0 norm, by default all dims.
    threshold : float, optional
        Epsilon tolerance, by default 1e-6.

    Returns
    -------
    torch.Tensor
        Average l0 if dims=None else l0 across dims.
    """
    if dims is None:
        return torch.mean((torch.abs(x) >= threshold).float())
    return torch.mean((torch.abs(x) >= threshold).float(), dims)



def l1_l2_ratio(x, dims=-1):
    """
    Compute the L1/L2 ratio of a tensor. By default, the ratio is computed across
    the last dimension. This score is a useful metric to evaluate the sparsity of
    a tensor. It is however sensitive to the dimensions of the data, for an unbiased
    metric, consider using the Hoyer score.

    Parameters
    ----------
    x : torch.Tensor
        Input tensor.
    dims : tuple, optional
        Dimensions over which to compute the ratio, by default -1.

    Returns
    -------
    torch.Tensor
        the l1/l2 ratio.
    """
    l1_norm = l1(x, dims)
    l2_norm = l2(x, dims) + Epsilon

    return l1_norm / l2_norm



def hoyer(x):
    """
    Compute the Hoyer sparsity of a tensor. The hoyer score include the dimension normalization
    factor. A score of 1 indicates a perfectly sparse representation, while a score of 0 indicates
    a dense representation.

    hoyer(x) = d^0.5 - (||x||_1 / ||x||_2) / (d^0.5 - 1).

    The score is computed across the last dimension.

    Parameters
    ----------
    x : torch.Tensor
        A 2D tensor of shape (batch_size, d).

    Returns
    -------
    torch.Tensor (batch_size,)
        Hoyer sparsity for each vector in the batch.
    """
    assert len(x.shape) == 2, "Input tensor must be 2D"

    d_sqrt = torch.sqrt(torch.tensor(x.shape[1]))
    l1_l2 = l1_l2_ratio(x, 1)

    score = (d_sqrt - l1_l2) / (d_sqrt - 1)

    return score



def kappa_4(x):
    """
    Compute the Kappa-4 sparsity of a tensor. The Kappa-4 score is a metric to evaluate the sparsity
    of a distribution. It is the kurtosis, which measure the "peakedness" of a distribution.

    See the following papers for more details:
    "Sparse coding of sensory inputs", by Olshausen and Field, 2004.
    "Comparing Measures of Sparsity", by Niall Hurley and Scott Rickard, 2009.

    @tfel: there is a little inconsistency between the two papers, for theoretical considerations
    I implemented the version from the second paper.

    Parameters
    ----------
    x : torch.Tensor
        Input tensor.
    dims : tuple, optional
        Dimensions over which to compute the ratio, by default -1.

    Returns
    -------
    torch.Tensor
        the Kappa-4 sparsity.
    """
    assert len(x.shape) == 2, "Input tensor must be 2D"

    x4 = (x ** 4).sum(1)
    x2_2 = x.square().sum(1).square()

    score = x4 / (x2_2 + Epsilon)

    return score



def r2_score(x, x_hat):
    """
    Compute the R^2 score (coefficient of determination) for the reconstruction.
    A score of 1 indicates a perfect reconstruction while a score of 0 indicates
    that the reconstruction is as good as the mean.

    Parameters
    ----------
    x : torch.Tensor
        Original input tensor of shape (batch_size, d).
    x_hat : torch.Tensor
        Reconstructed input tensor of shape (batch_size, d).

    Returns
    -------
    float
        R^2 score.
    """
    assert x.shape == x_hat.shape, "Input tensors must have the same shape"
    assert len(x.shape) == 2, "Input tensors must be 2D"

    ss_res = torch.mean((x - x_hat) ** 2)
    ss_tot = torch.mean((x - x.mean()) ** 2)

    r2 = 1 - (ss_res / (ss_tot + Epsilon))

    return torch.mean(r2)



def dead_codes(z):
    """
    Check for codes that never fire and return the percentage of codes that never fire.

    Parameters
    ----------
    z : torch.Tensor
        Input tensor of shape (batch_size, num_codes).

    Returns
    -------
    torch.Tensor
        Tensor indicating which codes are dead.
    """
    assert len(z.shape) == 2, "Input tensor must be 2D"
    is_dead = (z.sum(0) == 0).float()
    return is_dead
