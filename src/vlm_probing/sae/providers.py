"""Discovery, checkpoint catalogs and training through bundled SAE cores.

The backend implementations retain their upstream normalization, objectives and
checkpoint formats. A shared entry point does not make those contracts equal.
"""
from __future__ import annotations

import gzip
from importlib import import_module
from importlib.resources import files
import json


_PROVIDERS = {
    "saelens": {"upstream_package": "sae-lens", "extra": "saelens",
                "source_url": "https://github.com/decoderesearch/SAELens"},
    "prisma": {"upstream_package": "vit-prisma", "extra": "prisma",
               "source_url": "https://github.com/Prisma-Multimodal/ViT-Prisma"},
    "overcomplete": {"upstream_package": "overcomplete", "extra": "overcomplete",
                     "source_url": "https://github.com/KempnerInstitute/overcomplete"},
}
_ALIASES = {"sae-lens": "saelens", "vit-prisma": "prisma", "vit_prisma": "prisma"}


def _name(backend):
    name = _ALIASES.get(backend, backend)
    if name not in _PROVIDERS:
        raise ValueError(f"unknown SAE backend {backend!r}; choose {list(_PROVIDERS)}")
    return name


def _module(backend):
    name = _name(backend)
    return import_module(f".backends.{name}", package=__package__)


def list_backends():
    """Describe bundled implementations without importing their numerical cores.

    Upstream package installation and version never select the implementation.
    Generic dependencies are deferred until the requested operation.
    """
    result = []
    for name, descriptor in _PROVIDERS.items():
        info = _module(name).backend_info()
        result.append({**descriptor, **info, "backend": name,
                       "implementation": "bundled", "core_bundled": True,
                       "external_package_required": False})
    return result


def list_pretrained(backend=None, *, model=None, query=None, limit=None, source="snapshot", **filters):
    """Search versioned upstream checkpoint metadata, without fetching weights.

    The bundled catalog records author-listed resources, not model/checkpoint
    compatibility guarantees or completed reproductions. ``source='installed'``
    is a compatibility alias for ``source='bundled'`` and queries the pinned
    bundled provider registry. Snapshot discovery needs no numerical dependencies
    or internet connection.
    """
    name = None if backend is None else _name(backend)
    if limit is not None and (type(limit) is not int or limit < 1):
        raise ValueError("limit must be a positive integer or None")
    if source in {"bundled", "installed"}:
        if name is None:
            raise ValueError("provider discovery requires a backend")
        rows = _module(name).list_pretrained(**filters)
    elif source == "snapshot":
        if filters:
            raise ValueError("provider-specific filters require source='bundled'; use query for snapshot search")
        resource = files(__package__).joinpath("resources/pretrained_catalog.json.gz")
        with resource.open("rb") as stream:
            catalog = json.loads(gzip.decompress(stream.read()))
        rows = catalog["entries"]
    else:
        raise ValueError("source must be snapshot or bundled (installed is a compatibility alias)")
    selected = []
    for row in rows:
        if name is not None and row.get("backend") != name:
            continue
        if model is not None and model.casefold() not in str(row.get("model", "")).casefold():
            continue
        if query is not None and query.casefold() not in json.dumps(row, ensure_ascii=False).casefold():
            continue
        selected.append(dict(row))
        if limit is not None and len(selected) >= limit:
            break
    return selected


def catalog_provenance():
    """Return snapshot source commits and collection scope without model weights."""
    resource = files(__package__).joinpath("resources/pretrained_catalog.json.gz")
    with resource.open("rb") as stream:
        catalog = json.loads(gzip.decompress(stream.read()))
    return {key: value for key, value in catalog.items() if key != "entries"}


def wrap_sae(backend, model, *, binding, **kwargs):
    """Adapt a caller-loaded dictionary, with explicit native model/hook binding."""
    return _module(backend).wrap(model, binding=binding, **kwargs)


def load_sae(backend, *, binding, **kwargs):
    """Load an upstream checkpoint through its provider's verified loader."""
    return _module(backend).load(binding=binding, **kwargs)


def train_backend(backend, **kwargs):
    """Run a provider's training protocol using its documented native options.

    Inspect the per-provider guide for the required configuration and input
    types. Objectives, validation, schedules, resume support and artifacts are
    reported by each protocol; no universal optimizer recipe is implied.
    """
    return _module(backend).train(**kwargs)
