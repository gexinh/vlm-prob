"""Pinned MIT-licensed Overcomplete SAE core; no upstream installation required.

Only the integrated sparse autoencoder dependency closure is included. See
LICENSE and VENDOR_MANIFEST.json for origin, hashes and local changes.
"""
__version__ = "0.3.0"
from .sae import SAE, TopKSAE, BatchTopKSAE, JumpSAE, RATopKSAE, RAJumpSAE
__all__ = ["SAE", "TopKSAE", "BatchTopKSAE", "JumpSAE", "RATopKSAE", "RAJumpSAE"]
