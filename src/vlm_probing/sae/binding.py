"""Explicit checkpoint identity and the adapter's actual residual hook contract."""
from dataclasses import asdict, is_dataclass


def build_sae_binding(probe, layer, *, model_id, tokenizer_id,
                      preprocessing_id, calibration_id):
    """Bind one dictionary to one native residual tensor.

    Immutable model/tokenizer/preprocessing identities are supplied by the
    caller. Runtime checking validates the actual adapter and hook; it cannot
    establish that a caller's model checksum is truthful without rehashing the
    underlying checkpoint. Keep the extraction manifest with the artifact.
    """
    if type(layer) is not int or layer not in probe.spec.residuals:
        raise ValueError("layer must identify an available residual layer")
    identities = dict(model_id=model_id, tokenizer_id=tokenizer_id,
                      preprocessing_id=preprocessing_id, calibration_id=calibration_id)
    if any(not isinstance(value, str) or not value.strip() or value == "unspecified"
           for value in identities.values()):
        raise ValueError("supply explicit immutable model/tokenizer/preprocessing/calibration identities")
    site = probe.spec.residuals[layer]
    point = getattr(probe.adapter, "sites", {}).get(site)
    if point is None or not is_dataclass(point):
        raise ValueError("SAE binding requires an adapter exposing explicit HookPoint metadata")
    hook = asdict(point)
    if hook.get("tensor_slice") is not None:
        hook["tensor_slice"] = list(hook["tensor_slice"])
    return {**identities, "site": site, "layer": layer, "hook": hook,
            "representation": "native_residual_output",
            "adapter_model_id": probe.adapter.model_id}


def check_runtime_binding(probe, layer, binding):
    """Reject a dictionary trained on a different layer, module or adapter."""
    fields = ("model_id", "tokenizer_id", "preprocessing_id", "calibration_id")
    try:
        expected = build_sae_binding(probe, layer, **{key: binding[key] for key in fields})
    except KeyError as error:
        raise ValueError(f"SAE binding missing {error.args[0]}") from error
    for key in ("site", "layer", "hook", "representation", "adapter_model_id"):
        if binding.get(key) != expected[key]:
            raise ValueError(f"SAE artifact {key} differs from the runtime model hook")
