"""Algorithm-oriented SAE discovery, independent of checkpoint source tools."""
from copy import deepcopy


_MONO = "https://transformer-circuits.pub/2023/monosemantic-features/index.html"
_TOPK = "https://arxiv.org/abs/2406.04093"
_GATED = "https://arxiv.org/abs/2404.16014"
_JUMP = "https://arxiv.org/abs/2407.14435"
_BATCH = "https://arxiv.org/abs/2412.06410"
_MATRYOSHKA = "https://arxiv.org/abs/2503.17547"
_ARCHETYPAL = "https://arxiv.org/abs/2502.12892"
_PURSUIT = "https://doi.org/10.1109/78.258082"


def _entry(name, title, description, defaults, sources, *, status="supported", notes=""):
    return {"name": name, "architecture": name, "title": title, "description": description,
            "family": "sae", "status": status, "defaults": defaults,
            "input_contract": "Floating native residuals [...,d_in], one exact model/hook binding; dictionary decoder returns raw coordinates.",
            "training": True, "inference": True,
            "capabilities": ["fit", "features", "profile", "reconstruction", "feature_edit"],
            "sources": sources, "math_notes": notes}


_METHODS = [
    _entry("relu", "ReLU + L1 SAE", "Nonnegative dictionary codes with an explicit L1 penalty.",
           {"l1_coefficient": .01}, [_MONO]),
    _entry("topk", "TopK SAE", "Per-vector positive TopK selection.",
           {"k": 32, "auxk_coefficient": 0.}, [_TOPK],
           notes="Legacy core MSE recipe by default; optional dead-feature AuxK is an explicit recipe."),
    _entry("gated", "Gated SAE", "Separate feature selection and magnitude; fixed-decoder auxiliary gate reconstruction.",
           {"l1_coefficient": .01}, [_GATED]),
    _entry("jumprelu", "JumpReLU SAE", "Learned nonnegative activation thresholds with a rectangle surrogate.",
           {"jumprelu_threshold": .1, "jumprelu_bandwidth": .05, "jumprelu_sparsity": "l0", "l0_coefficient": .01}, [_JUMP]),
    _entry("abstopk", "Absolute TopK SAE", "Select largest magnitudes and retain signed feature values.",
           {"k": 32}, ["https://arxiv.org/abs/2510.00404", _TOPK]),
    _entry("batchtopk", "BatchTopK SAE", "Shared training sparsity budget and a saved evaluation threshold.",
           {"k": 32, "batch_budget": "average", "threshold_ema": .99}, [_BATCH],
           notes="average means k times training vector count; global means exactly k selections across the batch. Evaluation is per-vector thresholding."),
    _entry("matryoshka_batchtopk", "Matryoshka BatchTopK SAE", "BatchTopK with explicit nested dictionary-width reconstruction losses.",
           {"k": 32, "batch_budget": "average"}, [_MATRYOSHKA, _BATCH],
           notes="Widths must end at d_sae; losses are a weighted sum. Inner-level dead-feature AuxK variants are outside this recipe."),
    _entry("matching_pursuit", "Matching Pursuit", "Greedily explain residuals with nonnegative tied-dictionary coefficients.",
           {"residual_tolerance": .01, "stop_on_duplicate_support": True}, [_PURSUIT],
           notes="Discrete support selection; gradients flow through selected coefficients and atoms."),
    _entry("archetypal_topk", "Archetypal TopK SAE", "TopK codes over convex combinations of TRAIN anchors with bounded relaxation.",
           {"k": 32, "dictionary": "archetypal", "archetypal_candidates": 128, "archetypal_delta": 1.}, [_ARCHETYPAL, _TOPK],
           notes="Native softmax mixture parameterization; not a reproduction of an upstream optimizer recipe."),
    _entry("archetypal_jumprelu", "Archetypal JumpReLU SAE", "JumpReLU codes with the same TRAIN-anchor dictionary component.",
           {"dictionary": "archetypal", "archetypal_candidates": 128, "archetypal_delta": 1.}, [_ARCHETYPAL, _JUMP]),
    _entry("signed_matching_pursuit", "Signed Matching Pursuit", "Greedy residual coding with both signs of each dictionary direction.",
           {"residual_tolerance": .01}, [_PURSUIT], status="experimental"),
    _entry("orthogonal_matching_pursuit", "Nonnegative Orthogonal Matching Pursuit", "Unique greedy support with joint nonnegative coefficient refits.",
           {"omp_nnls_iterations": 32}, [_PURSUIT], status="experimental",
           notes="Finite projected-gradient NNLS on the selected support; explicit approximate solver budget, not exact active-set NNLS."),
    _entry("signed_orthogonal_matching_pursuit", "Signed Orthogonal Matching Pursuit", "Unique greedy support with unconstrained least-squares refits.",
           {"residual_tolerance": .01}, [_PURSUIT], status="experimental"),
    _entry("qsae", "Quantized SAE", "Learned scalar quantization levels with a straight-through code path.",
           {"quantization_levels": 4, "hard_quantization": False},
           ["https://github.com/KempnerInstitute/overcomplete"], status="experimental",
           notes="Upstream marks this unpublished and experimental. Quantization is not a guarantee of sparse codes; no biological-concept claim."),
]
_ALIASES = {"standard": "relu", "abs_topk": "abstopk", "mp": "matching_pursuit",
            "omp": "orthogonal_matching_pursuit", "signed_mp": "signed_matching_pursuit",
            "signed_omp": "signed_orthogonal_matching_pursuit"}


def list_methods(*, status=None):
    """Return independent JSON metadata, organized by algorithms, not providers."""
    if status is not None and status not in {"supported", "experimental"}:
        raise ValueError("status must be supported or experimental")
    return deepcopy([row for row in _METHODS if status is None or row["status"] == status])


def get_method(name):
    name = _ALIASES.get(name, name)
    for row in _METHODS:
        if row["name"] == name:
            return deepcopy(row)
    raise ValueError(f"unknown SAE method {name!r}; use list_methods()")


def method_config(name, *, d_in, d_sae, **kwargs):
    from .models import SAEConfig
    method = get_method(name)
    return SAEConfig(architecture=method["architecture"], d_in=d_in, d_sae=d_sae,
                     **{**method["defaults"], **kwargs})
