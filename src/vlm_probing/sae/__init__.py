"""Sparse dictionary kernels and an optional, lazily loaded external backend."""
from .models import SAEConfig, SparseAutoencoder, validate_sae_binding
from .external import SAELensAdapter
from .binding import build_sae_binding

__all__ = ["SAEConfig", "SparseAutoencoder", "SAELensAdapter",
           "build_sae_binding", "validate_sae_binding"]
