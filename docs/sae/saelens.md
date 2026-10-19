# SAELens backend

[SAELens](https://github.com/decoderesearch/SAELens) supplies pretrained dictionaries, architecture-specific losses and a native training loop. VLMProbe preserves that implementation and connects the dictionary to its shared sparse-feature analysis and intervention interface. Optional code is imported only when loading a release, inspecting the installed registry or running its trainer.

Verified upstream: **sae-lens 6.54.6**, commit [`30c45024`](https://github.com/decoderesearch/SAELens/tree/30c4502466785dd7809a307f7b705df187978aa3), MIT code license. Checkpoint and source-model licenses remain those specified by their publishers.

```bash
pip install -e '.[saelens,visualization]'
```

Run this from the development checkout; these additions are not yet released on PyPI.

SAELens v6 supports more than language models. Its [`SAETrainer`](https://github.com/decoderesearch/SAELens/blob/30c4502466785dd7809a307f7b705df187978aa3/docs/extending_saelens.md) accepts any iterator of activation vectors, including vision and multimodal activations. `LanguageModelSAETrainingRunner` is its higher-level convenience runner for language-model data.

## Discover pretrained dictionaries

```python
from vlmprobe.sae.backends import saelens

print(saelens.backend_info())
for entry in saelens.list_pretrained(
    release="goodfire-llama-3.1-8b-instruct"
):
    print(entry)
```

The audited upstream registry contains 170 releases and 13,857 dictionary entries. Examples include GPT-2 dictionaries, Gemma Scope, Llama Scope and Goodfire Llama dictionaries. `list_pretrained` reads the installed SAELens registry and does not download weights. Its `release`, `model` and `sae_id` filters use exact matches. A registry entry may not declare its architecture or hook; those fields remain `None` rather than being guessed. The bundled VLMProbe catalog is a versioned snapshot, whereas this backend function reflects the installed package.

Registry inclusion is not a claim that a dictionary works with every VLMProbe model. A GPT-2 residual dictionary cannot be applied to Qwen or a ViT by matching dimensions. The registry also contains transcoders and temporal SAEs, whose different contracts are excluded from this backend's same-space, independent-vector inference adapter.

## Load or wrap a dictionary

```python
adapter = saelens.load(
    release="YOUR_RELEASE",
    sae_id="YOUR_SAE_ID",
    binding=verified_binding,
    device="cuda:0",
    dtype="float32",
)

# Or preserve a dictionary you have already loaded with SAELens:
# adapter = saelens.wrap(upstream_sae, binding=verified_binding)

features = adapter.encode(raw_activations)       # [..., dictionary_width]
reconstruction = adapter.decode(features)       # [..., original_width]
```

`binding` records exact model, tokenizer, input preprocessing, calibration dataset, layer and native hook identities. Use `build_sae_binding` with the actual VLMProbe model and retain the source extraction manifest. When upstream metadata uses TransformerLens names, add its exact `backend_model_name`, `backend_hook_name`, and, where needed, `backend_tokenizer_name`. Nonempty `model_from_pretrained_kwargs` must also be recorded as `backend_model_from_pretrained_kwargs`: operations such as centering writing weights change activation coordinates. A declaration should accompany an independently verified equivalence; it is not a conversion of the model.

Supported inference architectures are Standard/ReLU, Gated, TopK, JumpReLU, AbsTopK and Matching Pursuit. SAELens performs their encode/decode operations directly. Runtime `layer_norm` and `constant_norm_rescale` are rejected because decoding depends on transient per-input state. Scaling or whitening already folded by upstream into raw-space weights is supported when the resulting `normalize_activations` is `"none"`. Unresolved `expected_average_only_in`, head reshaping, head-only dictionaries, cross-hook transcoders and context-dependent temporal dictionaries are rejected. No unsupported configuration is silently treated as a standard residual SAE.

## Native training protocol

```python
report = saelens.train(
    config={
        "seed": 42,
        "sae": {
            "architecture": "topk",
            "d_in": 768,
            "d_sae": 6144,
            "k": 32,
            "normalize_activations": "none",
            "device": "cuda:0",
        },
        "trainer": {
            "total_training_samples": 1_000_000,
            "train_batch_size_samples": 1024,
            "lr": 3e-4,
            "lr_end": 3e-5,
            "lr_scheduler_name": "cosineannealing",
            "device": "cuda:0",
            "autocast": True,
            "dead_feature_window": 1000,
            "feature_sampling_window": 2000,
            "logger": {"log_to_wandb": False},
        },
    },
    activation_source=train_activation_batches,
    validation_source=held_out_activation_batches,
    output_dir="runs/my_saelens_dictionary",
    binding=verified_binding,
)
```

| Argument | Meaning |
| --- | --- |
| `config["sae"]` | Native architecture configuration. `d_in` is the selected activation width, `d_sae` the dictionary width, `k` the TopK budget. Standard/Gated use `l1_coefficient`. Unknown parameters raise. |
| `config["trainer"]` | Native `SAETrainerConfig`: training-vector budget, vectors per batch, optimizer, schedule, precision, dead-feature statistics and logging. The backend defaults missing `lr_end` to `lr`. |
| `activation_source` | Iterator of raw floating `[N, d_in]` training batches. Extract from the frozen source model; flatten only explicitly known token or image-patch axes. |
| `validation_source` | Separate finite iterator for evaluation of final raw-space reconstruction and sparsity. Default maximum: 100 batches. It never feeds the training optimizer. |
| `max_validation_batches` | Positive cap on held-out evaluation batches. |
| `model` | Optional already constructed upstream `TrainingSAE`. When supplied, `config` may instead be a native `SAETrainerConfig`. This is the dictionary, not the frozen backbone. |
| `evaluator` | Optional upstream evaluator callback, following SAELens's native trainer/logging protocol. Use `validation_source` for the backend's independent final evaluation. |
| `resume_from` | Saved native `training_state` directory. Dictionary objective parameters and optimizer/schedule/batch/normalization protocols must match. Device and dtype moves are allowed; logging and checkpoint destinations may change. Increasing the vector budget is allowed only for a constant learning rate without warmup, decay or restarts and is explicitly recorded. Exact data-order replay additionally requires restoring the activation iterator position. Final checkpoints trained with folded normalization are inference-only in this wrapper; resumable training requires `normalize_activations="none"`. |
| `binding` | Explicit checkpoint/data/preprocessing/native-hook provenance. Local checkpoint loads and resumes reject different bindings. |

Training uses the actual upstream `SAETrainer` and architecture-specific losses, not VLMProbe's separate native SAE kernels. In addition to the inference architectures, the runner accepts upstream BatchTopK and Matryoshka BatchTopK training configurations and their native inference export. The native protocol trains for a fixed activation-vector budget; the wrapper does not claim validation-based early stopping. Validation reports MSE per vector, squared reconstruction error relative to a zero reconstruction, mean L0 and fraction of unseen features.

Split before collecting activations. For text, split by document; for pathology, split by source slide or patient when available. Shuffling tokens or patches from the same document/slide into both train and validation does not establish generalization. Record source model revision, tokenizer, image transformation, native hook, activation shape and split manifest with `binding`.

Artifacts are `inference/{cfg.json,sae_weights.safetensors,vlmprobe_binding.json}`, native `training_state` weights plus optimizer/scheduler/counters and `vlmprobe_training_protocol.json`, and a run-level `protocol.json` with complete configuration and status. Resume compares both the retained protocol and native dictionary/optimizer state; matching dimensions and a matching dataset binding alone are insufficient. A changed TopK budget, sparsity penalty, normalization or learning rate is rejected. Load `inference` with `saelens.load(path=..., binding=...)`. Pass the resulting adapter to `probe.sae.features` or `probe.sae.edit` using the same verified binding.

## Complete CPU protocol self-test

This example starts with synthetic activation vectors, trains, saves, reloads and obtains sparse features and reconstructions. It checks API interoperability; it does not claim that these vectors yield interpretable biological or linguistic concepts. Replace the two independent sources with activations extracted from your own source-level dataset split for an actual experiment.

```python
import itertools
from pathlib import Path
import torch
from vlmprobe import ProbeResult, visualization as viz
from vlmprobe.sae.backends import saelens

generator = torch.Generator().manual_seed(42)
train_vectors = torch.randn(256, 8, generator=generator)
validation_vectors = torch.randn(64, 8, generator=generator)
binding = {
    "model_id": "synthetic-source@seed42",
    "tokenizer_id": "none@vector-input",
    "preprocessing_id": "identity-v1",
    "calibration_id": "synthetic-independent-draws@seed42",
    "site": "residual.0",
    "layer": 0,
    "hook": {
        "module": "blocks.0", "kind": "output",
        "selector": None, "tensor_slice": None,
    },
}
train_batches = list(train_vectors.split(16))
output = Path("runs/saelens_cpu_example")  # Choose a fresh directory.
report = saelens.train(
    config={
        "seed": 42,
        "sae": {
            "architecture": "topk", "d_in": 8, "d_sae": 32, "k": 4,
            "device": "cpu", "normalize_activations": "none",
        },
        "trainer": {
            "total_training_samples": 1024,
            "train_batch_size_samples": 16,
            "lr": 1e-3,
            "device": "cpu",
            "logger": {"log_to_wandb": False},
        },
    },
    activation_source=itertools.cycle(train_batches),
    validation_source=iter(validation_vectors.split(16)),
    output_dir=output,
    binding=binding,
)
adapter = saelens.load(
    path=report["artifacts"]["inference_dir"], binding=binding
)
features = adapter.encode(validation_vectors)
reconstruction = adapter.decode(features)
print(features.shape, reconstruction.shape)  # [64, 32], [64, 8]
print(report["validation"])
activity = ProbeResult("sae.features", {"features": features},
                       {"source": "synthetic held-out activation vectors"})
ax = viz.plot_sae_activity(activity, top_k=16)
ax.figure.tight_layout()
ax.figure.savefig(output / "heldout_feature_activity.png", dpi=160)
```

The integration tests run real upstream Standard/Gated/TopK training and reload, compare Standard/Gated/TopK/JumpReLU encoding and decoding with the original upstream implementation, verify source-identity rejection, and verify exact fixed-data constant-learning-rate resume for the unnormalized protocol. A separate 4.7 MB official GPT-2 feature-splitting dictionary was loaded and tested on CPU synthetic vectors; this is dictionary interoperability evidence, not a reproduction of its pretrained model or hook coordinates.
