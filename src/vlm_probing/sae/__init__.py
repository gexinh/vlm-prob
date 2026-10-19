"""Sparse dictionary kernels and an optional, lazily loaded external backend."""
from .models import SAEConfig, SparseAutoencoder, validate_sae_binding
from .external import SAELensAdapter
from .binding import build_sae_binding
from .providers import (list_backends, list_pretrained, catalog_provenance,
                        load_sae, wrap_sae, train_backend)

__all__ = ["SAEConfig", "SparseAutoencoder", "SAELensAdapter",
           "build_sae_binding", "validate_sae_binding", "list_backends",
           "list_pretrained", "catalog_provenance", "load_sae", "wrap_sae", "train_backend"]
