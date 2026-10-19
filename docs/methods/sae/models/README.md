# SAE models and checkpoints

Browse **9,660 published SAE checkpoints** across 151 author weight repositories,
covering GPT-2, Gemma, Llama, Qwen, CLIP and DINO backbones. Each dictionary has
our own information card with its method, source model, activation hook,
available dimensions and input conventions, plus direct weight/repository links.
Published names that resolve to the same checkpoint are merged as aliases.

[Browse every checkpoint repository](published/README.md) ·
[Open the standalone searchable catalog](catalog.html) ·
[Vision backbones for training](backbones.md)

The searchable HTML page includes its data and can be downloaded and opened
locally. The Markdown cards below are also readable directly on GitHub.

| Published collection | Methods | Our model information | Checkpoint weights |
| --- | --- | --- | --- |
| GPT-2 feature-splitting dictionaries | ReLU | [GPT-2 layer 8](published/jbloom-gpt2-small-feature-splitting-experiment-layer-8-dbe4582b-p1.md#gpt2-layer8-relu-768) | [Download](https://huggingface.co/jbloom/GPT2-Small-Feature-Splitting-Experiment-Layer-8/resolve/174d298f1633aab71e440685c3292ce8108a5a73/blocks.8.hook_resid_pre_768/sae_weights.safetensors) |
| Gemma Scope | JumpReLU | [Gemma-2 dictionary](published/google-gemma-scope-2b-pt-att-da0daf1e-p1.md#sae-40fd7a489d37f2b8bd438f17) | [Checkpoint files](https://huggingface.co/google/gemma-scope-2b-pt-att/tree/main/layer_0/width_16k/average_l0_104) |
| Gemma Scope 2 | JumpReLU | [Gemma-3 dictionary](published/google-gemma-scope-2-4b-pt-568216a4-p5.md#sae-821c7f9ab3a7f8afbd9678fd) | [Checkpoint files](https://huggingface.co/google/gemma-scope-2-4b-pt/tree/main/attn_out/layer_17_width_16k_l0_big) |
| Qwen Scope | TopK | [Qwen dictionary](published/qwen-sae-res-qwen3-1-7b-base-w32k-l0-100-f6e0808c-p1.md#sae-91dd570b8052f3f388447247) | [Download](https://huggingface.co/Qwen/SAE-Res-Qwen3-1.7B-Base-W32K-L0_100/resolve/main/layer0.sae.pt) |
| Goodfire Llama dictionaries | ReLU | [Llama-3.1 layer 19](published/goodfire-llama-3-1-8b-instruct-sae-l19-c605baef-p1.md#sae-67c6bcd9c84048110d5346b4) | [Download](https://huggingface.co/Goodfire/Llama-3.1-8B-Instruct-SAE-l19/resolve/main/Llama-3.1-8B-Instruct-SAE-l19.pth) |
| CLIP ViT-B/32 patch dictionaries | ReLU | [CLIP layer 11](published/prisma-multimodal-sparse-autoencoder-clip-b-32-sae-vanilla-x64-layer-11-hook-resid-post-l1-1e-0-19d81acc-p1.md#clip-b32-layer11-relu-49152) | [Download](https://huggingface.co/Prisma-Multimodal/sparse-autoencoder-clip-b-32-sae-vanilla-x64-layer-11-hook_resid_post-l1-1e-05/resolve/2b1cb17ffb8b06e7f45a699dfc97d417f9879be4/weights.pt) |
| CLIP CLS dictionaries | TopK | [CLS-only layer 11](published/prisma-multimodal-sae-top-k-64-cls-only-layer-11-hook-resid-post-5eda9b30-p1.md#sae-0fafbffebcc920f372943f8f) | [Download](https://huggingface.co/Prisma-Multimodal/sae-top_k-64-cls_only-layer_11-hook_resid_post/resolve/73611b78df558947515c213b56be74c3b2be91f0/weights.pt) |
| DINO ViT-B/16 dictionaries | ReLU | [DINO layer 0](published/prisma-multimodal-dino-vanilla-x64-all-patches-0-resid-post-507-98-3a6c7680-p1.md#sae-f1ea8668fa9868f9acfb0a14) | [Download](https://huggingface.co/Prisma-Multimodal/DINO-vanilla-x64-all_patches_0-resid_post-507-98/resolve/c44792cf34df589b145a8f9f2d7751e9e0d4c6f3/weights.pt) |

The five [vision backbone cards](backbones.md) describe DINOv2, SigLIP, ViT,
ResNet-V2-BiT and ConvNeXt models used for activation collection in Overcomplete.
They are pretrained backbones for training your own SAE, and are explicitly
marked as backbones rather than SAE weight releases. Overcomplete does not
provide a central pretrained SAE checkpoint registry in the audited source.

## Search the model information

```python
from vlmprobe.sae import list_models, get_model_card

vision_topk = list_models(modality="vision", method="topk")
qwen_models = list_models(query="Qwen", limit=20)
card = get_model_card("clip-b32-layer11-relu-49152")
print(card["dimensions"], card["input_conventions"])
print(card["links"]["checkpoint"])  # Direct weights or checkpoint directory.
print(card["links"]["card"])        # Our own information page and model anchor.

backbones = list_models(artifact_kind="backbone")
```

These are author-published model records, not a claim that every raw weight
format is automatically runnable with an arbitrary Hugging Face backbone.
Download the selected checkpoint, preserve its exact model/hook/preprocessing,
and convert a supported tensor layout using `import_checkpoint` before
`probe.sae.load(...)`. The [shared API](../API.md) describes native artifact
conversion and binding. Fields absent from the source remain unspecified.

The metadata snapshot uses the pinned SAELens and ViT-Prisma published listings
and source loading recipes; it includes same-activation SAE dictionaries and
excludes cross-layer transcoders and temporal contracts. Model and checkpoint
licenses are recorded independently from the framework's code license.

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
model = AutoModelForCausalLM.from_pretrained(model_id, attn_implementation="eager").to(device)
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
in the [model guides](../../../models/README.md); training and probing operations
are described in the [SAE guide](../README.md).

A local registry adds your own trained dictionaries to the same model-card interface. The native loader checks source model and processor fingerprints and the saved layer/hook binding. Preserve the exact extraction coordinates when converting published author weights.

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
