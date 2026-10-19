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
    # Keep public module/class identity across both import names, without
    # traversing private vendored code and importing its optional dependencies.
    # Vendored implementations use the canonical internal namespace only.
    def visit(paths, prefix):
        for info in _pkgutil.iter_modules(paths, prefix):
            if info.name == "vlm_probing._vendor":
                continue
            module = _importlib.import_module(info.name)
            suffix = info.name.removeprefix("vlm_probing.")
            _sys.modules[f"{__name__}.{suffix}"] = module
            if "." not in suffix:
                globals()[suffix] = module
            if info.ispkg:
                visit(module.__path__, info.name + ".")

    visit(_canonical.__path__, "vlm_probing.")


_install_aliases()
del _install_aliases


def __getattr__(name):
    return getattr(_canonical, name)


def __dir__():
    return sorted(set(globals()) | set(dir(_canonical)))
