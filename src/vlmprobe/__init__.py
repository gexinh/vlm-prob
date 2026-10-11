"""VLM Probing's public import name, backed by one canonical implementation.

The ``vlm_probing`` namespace remains available for existing integrations and
serialized objects. Both names resolve to the same classes and submodules.
"""
import importlib as _importlib
import pkgutil as _pkgutil
import sys as _sys

import vlm_probing as _canonical

__all__ = list(_canonical.__all__)
__version__ = _canonical.__version__
globals().update({name: getattr(_canonical, name) for name in __all__})


def _install_aliases():
    # Eagerly register the small module tree so nested imports share class and
    # registry identity. These modules defer optional dependencies until use;
    # a fresh-process test enforces that contract. No import finder is needed.
    for info in _pkgutil.walk_packages(_canonical.__path__, "vlm_probing."):
        module = _importlib.import_module(info.name)
        suffix = info.name.removeprefix("vlm_probing.")
        _sys.modules[f"{__name__}.{suffix}"] = module
        if "." not in suffix:
            globals()[suffix] = module


_install_aliases()
del _install_aliases


def __getattr__(name):
    return getattr(_canonical, name)


def __dir__():
    return sorted(set(globals()) | set(dir(_canonical)))
