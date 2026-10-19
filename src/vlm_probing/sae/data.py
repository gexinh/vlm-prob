"""Frozen-model activation collection and explicit, reproducible identities."""
from collections.abc import Mapping
from importlib import metadata
import hashlib
import json
import math
from functools import wraps
from pathlib import Path

import torch

from ..api.common import model_eval, unpack


def tensor_digest(value):
    if value.is_meta:
        raise ValueError("SAE identities require loaded model weights, not meta tensors")
    value = value.detach().cpu().contiguous()
    if value.is_quantized:
        value = value.dequantize()
    digest = hashlib.sha256()
    digest.update(str((str(value.dtype), list(value.shape))).encode())
    digest.update(value.reshape(-1).view(torch.uint8).numpy().tobytes())
    return digest.hexdigest()


def model_identity(model):
    """Bind actual tensors to their declared architecture and numerical stack.

    Tensor bytes alone cannot distinguish GELU/ReLU, normalization epsilon or
    different model configurations. Training flags and checkpoint/cache paths
    are deliberately excluded; they do not define the frozen evaluation model.
    Arbitrary external globals used by custom forward code remain the caller's
    responsibility and are not claimed to be verified by this fingerprint.
    """
    digest = hashlib.sha256()
    config = getattr(model, "config", None)
    if callable(getattr(config, "to_dict", None)):
        config = config.to_dict()
    elif config is not None and not isinstance(config, Mapping):
        config = {key: value for key, value in vars(config).items() if not key.startswith("_")}
    config = _configuration_identity(config)
    modules = []
    for name, module in model.named_modules():
        attributes = {}
        for key, value in vars(module).items():
            if key.startswith("_") or key in {"training", "config", "device", "dtype", "hf_device_map",
                    "warnings_issued", "gradient_checkpointing", "max_seq_len_cached"}:
                continue
            # Public scalar/container settings cover custom module options that
            # are not always printed by extra_repr (e.g. attention scaling).
            try:
                attributes[key] = _identity_value(value)
            except ValueError:
                pass  # Modules/tensors are recorded separately; opaque objects are not guessed.
        modules.append({"path": name, "class": _class_name(module),
                        "extra_repr": module.extra_repr(), "attributes": attributes})
    envelope = {"schema": "vlmprobe-model-identity-v2", "class": _class_name(model),
                "configuration": config, "modules": modules,
                "torch_version": str(torch.__version__)}
    # Querying package metadata never imports the optional Transformers stack.
    if type(model).__module__.startswith("transformers."):
        try:
            envelope["transformers_version"] = metadata.version("transformers")
        except metadata.PackageNotFoundError:
            envelope["transformers_version"] = "unavailable"
    digest.update(json.dumps(envelope, sort_keys=True, allow_nan=False).encode())
    for name, value in sorted(model.state_dict().items()):
        digest.update(name.encode())
        if not isinstance(value, torch.Tensor):
            raise ValueError("model extra state requires an explicit verified SAE binding")
        digest.update(tensor_digest(value).encode())
    return "sha256:" + digest.hexdigest()


def processor_identity(processor):
    if processor is None:
        return "none:caller-prepared-inputs"
    tokenizer = getattr(processor, "tokenizer", processor)
    value = {"schema": "vlmprobe-processor-identity-v2", "class": _class_name(processor),
             "tokenizer_class": _class_name(tokenizer)}
    if hasattr(tokenizer, "get_vocab"):
        value.update(vocab=_identity_value(tokenizer.get_vocab()),
                     special_tokens=_identity_value(getattr(tokenizer, "special_tokens_map", {})),
                     chat_template=getattr(tokenizer, "chat_template", None))
    backend = getattr(tokenizer, "backend_tokenizer", None)
    if callable(getattr(backend, "to_str", None)):
        backend_config = json.loads(backend.to_str())
        # HF temporarily changes these during individual calls. The actual
        # prepared inputs/layout and caller preprocessing_id record that choice.
        backend_config.pop("padding", None)
        backend_config.pop("truncation", None)
        value["tokenizer_backend"] = backend_config
    sentencepiece = getattr(tokenizer, "sp_model", None)
    if callable(getattr(sentencepiece, "serialized_model_proto", None)):
        value["sentencepiece_sha256"] = hashlib.sha256(sentencepiece.serialized_model_proto()).hexdigest()
    if hasattr(tokenizer, "bpe_ranks"):
        value["bpe_ranks"] = _identity_value(tokenizer.bpe_ranks)
    if hasattr(tokenizer, "init_kwargs"):
        configuration = dict(tokenizer.init_kwargs)
        source_files = set(getattr(tokenizer, "vocab_files_names", {})) | {
            "vocab_file", "merges_file", "tokenizer_file", "added_tokens_file",
            "special_tokens_map_file", "tokenizer_config_file", "chat_template_file",
        }
        for name in source_files & configuration.keys():
            if "tokenizer_backend" in value:
                # The complete runtime backend already includes vocabulary,
                # merge ranks, added tokens and normalization rules. Source
                # filenames describe where these were loaded, not behavior.
                configuration.pop(name)
            elif isinstance(configuration[name], (str, Path)) and Path(configuration[name]).is_file():
                # Slow/custom tokenizers may not expose a complete backend.
                # Preserve file semantics without binding to a cache location.
                configuration[name] = {"file_sha256": hashlib.sha256(
                    Path(configuration[name]).read_bytes()).hexdigest()}
        value["tokenizer_configuration"] = _configuration_identity(configuration)
    value["tokenizer_options"] = {key: _identity_value(getattr(tokenizer, key)) for key in (
        "model_max_length", "padding_side", "truncation_side", "clean_up_tokenization_spaces",
        "split_special_tokens", "do_lower_case", "add_prefix_space") if hasattr(tokenizer, key)}
    if hasattr(processor, "to_dict"):
        value["processor"] = _configuration_identity(processor.to_dict())
    # Also include sub-processors explicitly: older/custom ProcessorMixin
    # serializers may omit image/audio transforms even when the tokenizer agrees.
    for name in ("image_processor", "feature_extractor", "video_processor", "audio_processor"):
        component = getattr(processor, name, None)
        if callable(getattr(component, "to_dict", None)):
            value[name] = {"class": _class_name(component), "configuration": _configuration_identity(component.to_dict())}
    return "sha256:" + hashlib.sha256(json.dumps(value, sort_keys=True, allow_nan=False).encode()).hexdigest()


def _class_name(value):
    return type(value).__module__ + "." + type(value).__qualname__


def _identity_value(value):
    if value is None or type(value) in {bool, int}:
        return value
    if isinstance(value, str):
        return value.value if hasattr(value, "value") and isinstance(value.value, str) else str(value)
    if type(value) is float:
        if not math.isfinite(value):
            raise ValueError("identity metadata must be finite")
        return value
    if isinstance(value, (torch.dtype, torch.device)):
        return str(value)
    if isinstance(value, Mapping):
        if all(isinstance(key, str) for key in value):
            return {key: _identity_value(item) for key, item in value.items()}
        # Slow BPE rank maps use token-pair tuple keys; preserve both the pairs
        # and their rank rather than stringify away tokenization semantics.
        entries = [[_identity_value(key), _identity_value(item)] for key, item in value.items()]
        return {"mapping_entries": sorted(entries, key=lambda row: json.dumps(row[0], sort_keys=True))}
    if isinstance(value, (tuple, list)):
        return [_identity_value(item) for item in value]
    if isinstance(value, (set, frozenset)):
        return sorted((_identity_value(item) for item in value), key=lambda item: json.dumps(item, sort_keys=True))
    if type(value).__name__ == "AddedToken":
        return {name: _identity_value(getattr(value, name)) for name in
                ("content", "single_word", "lstrip", "rstrip", "normalized", "special")}
    if type(value).__module__.startswith("numpy") and callable(getattr(value, "tolist", None)):
        return _identity_value(value.tolist())
    raise ValueError(f"unsupported opaque identity metadata: {_class_name(value)}")


def _configuration_identity(value):
    if value is None:
        return None
    if not isinstance(value, Mapping):
        return _identity_value(value)
    ignored = {"_name_or_path", "name_or_path", "_commit_hash", "transformers_version", "device", "device_map"}
    return {key: _configuration_identity(item) for key, item in value.items() if key not in ignored}


def _input_digest(values):
    digest = hashlib.sha256()
    for key, value in sorted(values.items()):
        digest.update(key.encode())
        if isinstance(value, torch.Tensor):
            digest.update(tensor_digest(value).encode())
        elif value is None or isinstance(value, (str, int, float, bool, list, tuple, dict)):
            digest.update(json.dumps(value, sort_keys=True, allow_nan=False).encode())
        else:
            raise ValueError(f"cannot fingerprint prepared input {key!r}; supply tensors and JSON values")
    return digest.hexdigest()


def _preserve_collection_rng(function):
    """Preserve Torch/model-device and explicit loader/sampler RNG state.

    This does not rewind Python/NumPy randomness inside arbitrary transforms or
    independent/persistent worker-process RNGs. Such preprocessing requires its
    own deterministic dataset/caching protocol.
    """
    @wraps(function)
    def wrapped(self, batches, *args, **kwargs):
        candidates = (getattr(batches, "generator", None),
                      getattr(getattr(batches, "sampler", None), "generator", None))
        generators = {id(item): item for item in candidates if isinstance(item, torch.Generator)}
        saved = {key: generator.get_state().clone() for key, generator in generators.items()}
        tensors = list(self.probe.model.parameters()) + list(self.probe.model.buffers())
        cuda_devices = sorted({value.device.index for value in tensors if value.device.type == "cuda"})
        try:
            with torch.random.fork_rng(devices=cuda_devices):
                return function(self, batches, *args, **kwargs)
        finally:
            for key, state in saved.items():
                generators[key].set_state(state)
    return wrapped


class ActivationCollector:
    """Materialize small/medium activation splits with an explicit memory cap.

    Inputs are actual native model kwargs/ProbeInputs, never prepared results.
    Source-group independence is declared separately by the caller; tensor
    hashes detect repeated complete batches, not patient/slide overlap.
    Torch RNG and explicit loader/sampler generator states are restored. This
    does not promise deterministic arbitrary transforms or persistent workers.
    """

    def __init__(self, probe, layer, tokens, max_cache_bytes=1 << 30):
        self.probe, self.layer, self.tokens = probe, layer, tokens
        if type(max_cache_bytes) is not int or max_cache_bytes < 1:
            raise ValueError("max_cache_bytes must be a positive integer")
        self.max_cache_bytes = max_cache_bytes

    @_preserve_collection_rng
    @model_eval
    @torch.no_grad()
    def collect(self, batches):
        from ..adapters import ProbeInputs
        if isinstance(batches, (Mapping, ProbeInputs)):
            batches = [batches]
        site = self.probe.spec.residuals[self.layer]
        rows, hashes, coordinate_hashes, size, count, visual_vectors = [], [], [], 0, 0, 0
        for inputs in batches:
            values, _ = unpack(inputs)
            trace = self.probe._run(inputs, capture=[site])
            hidden = trace.activations[site]
            if hidden.ndim != 3:
                raise ValueError("this SAE collector requires native [batch,token,hidden] activations")
            layout = self.probe._layout(inputs, hidden)
            mask = layout.select(self.tokens)
            if layout.visual is not None:
                visual_vectors += int((mask & layout.visual).sum())
            selected = hidden[mask.to(hidden.device)].detach().float().cpu()
            if not len(selected) or not torch.isfinite(selected).all():
                raise ValueError("SAE capture must select nonempty finite activation vectors")
            size += selected.numel() * selected.element_size()
            if size > self.max_cache_bytes:
                raise ValueError("activation capture exceeds max_cache_bytes; use a smaller split or explicit cached activations")
            rows.append(selected)
            hashes.append(_input_digest(values))
            coordinate_hashes.append(tensor_digest(mask.nonzero()))
            count += hidden.shape[0]
        if not rows:
            raise ValueError("SAE input split is empty")
        widths = {row.shape[-1] for row in rows}
        if len(widths) != 1:
            raise ValueError("activation width changed between prepared input batches")
        result = torch.cat(rows)
        return result, {"input_batches": len(rows), "examples": count,
                        "visual_vectors": visual_vectors,
                        "activation_vectors": len(result), "bytes": size,
                        "input_hashes": hashes, "coordinate_hashes": coordinate_hashes,
                        "activations_sha256": tensor_digest(result)}


def checked_source_ids(train_ids, validation_ids):
    if (train_ids is None) != (validation_ids is None):
        raise ValueError("supply both train_ids and validation_ids for source-group checking")
    if train_ids is None:
        return {"source_groups_checked": False}
    def ids(value):
        result = list(value)
        if not result or any(not isinstance(item, str) or not item for item in result):
            raise ValueError("source IDs must be nonempty collections of nonempty strings")
        return sorted(set(result))
    train, validation = ids(train_ids), ids(validation_ids)
    if set(train) & set(validation):
        raise ValueError("source group overlap between training and validation")
    return {"source_groups_checked": True, "train_ids": train, "validation_ids": validation}
