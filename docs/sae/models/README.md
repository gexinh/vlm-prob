# SAE models and artifacts

VLMProbe publishes a pretrained model only after end-to-end verification with
its exact backbone, activation hook, input preparation and native artifact.
There are currently no released pretrained SAE models. `list_models()` returns
an empty list until a verified model is released or you supply your own local
registry.

Every supported SAE method can be trained on your own model and data, saved in
the same artifact format, and restored through `probe.sae.load(...)`.

## Train, save and reload

This example uses a pretrained language model and a small text split. Use your
own independent training and validation documents for a useful dictionary.

```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from vlmprobe import Prober
from vlmprobe.sae import SAETrainingConfig, list_models, get_model_card

model_id = "gpt2"
device = "cuda" if torch.cuda.is_available() else "cpu"
tokenizer = AutoTokenizer.from_pretrained(model_id)
tokenizer.pad_token = tokenizer.eos_token
model = AutoModelForCausalLM.from_pretrained(model_id).to(device)
probe = Prober(model, tokenizer)


def prepare(texts):
    return tokenizer(texts, padding=True, return_tensors="pt").to(device)


train = [prepare([
    "The telescope captured a distant galaxy.",
    "A botanist examined the leaves under a microscope.",
    "The artist mixed blue and yellow paint.",
    "A train crossed the bridge before sunrise.",
])]
validation = [prepare([
    "Researchers recorded the movement of nearby stars.",
    "The gardener planted flowers beside the window.",
])]

fitted = probe.sae.topk(layer=3, tokens="text", d_sae=3072, k=16)
fitted.fit(
    train, validation,
    output_dir="outputs/text_topk",
    train_ids=["training-document-group"],
    validation_ids=["validation-document-group"],
    preprocessing_id="gpt2-tokenizer-padding-v1",
    training=SAETrainingConfig(max_steps=200, batch_size=128),
)
fitted.save(
    "outputs/text_topk/final",
    registry_dir="outputs/model_cards",
    model_card={"id": "my-text-topk-v1", "title": "My text TopK dictionary"},
)

restored = probe.sae.load("outputs/text_topk/final")
result = restored.run(validation[0])
print(result.tensors["features"].shape)

cards = list_models(registry_dir="outputs/model_cards", include_builtin=False)
card = get_model_card("my-text-topk-v1", registry_dir="outputs/model_cards")
restored = probe.sae.load("my-text-topk-v1", registry_dir="outputs/model_cards")
```

The same save/load interface applies to vision and multimodal models and to
all native SAE algorithms. Model-specific loading and input preparation remain
in the [model guides](../../models/README.md); training and probing operations
are described in the [SAE guide](../README.md).

A local registry belongs to your experiment. Registering an artifact there does
not publish it as a reviewed pretrained model. The loader checks the source
model and processor fingerprints and the saved layer/hook binding. A matching
hidden width alone is insufficient.

## Artifact layout

```text
final/
  config.json       complete SAE configuration, binding and checksums
  weights.pt        tensor-only parameters and persistent buffers
  model_card.json   model identity, training provenance and artifact location
```

`best.pt` inference checkpoints store the same information in a safe single-file
envelope, with a model-card sidecar for local discovery. Optimizer and RNG state
are kept in a separate checkpoint for training resume.

Lower-level code can use `save_artifact(model, path)` and
`load_artifact(path, expected_binding=...)` on the native dictionary class.
Loading preserves feature order, biases, normalization and threshold buffers,
checks file/tensor integrity, and uses safe tensor deserialization. Legacy native
v1 checkpoints are migrated explicitly; unrelated external formats require a
reviewed one-time conversion.
