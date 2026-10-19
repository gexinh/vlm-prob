"""Pinned selected ViT-Prisma core, imported lazily by the maintained backend.

See LICENSE and SOURCE.json for upstream revision and local modifications.
"""
from importlib import import_module
_EXPORTS={"VisionModelSAERunnerConfig":".config","HookedViTConfig":".vision_config","HookedViT":".vision","StandardSparseAutoencoder":".sae","GatedSparseAutoencoder":".sae"}
def __getattr__(name):
    if name not in _EXPORTS: raise AttributeError(name)
    value=getattr(import_module(_EXPORTS[name],__name__),name)
    globals()[name]=value
    return value
__all__=list(_EXPORTS)
