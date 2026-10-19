# SAE models and checkpoints

Browse **9,660 published SAE checkpoint variants** across 151 author weight repositories,
covering GPT-2, Gemma, Llama, Qwen, CLIP and DINO backbones. Each dictionary has
our own information card with its method, source model, activation hook,
available dimensions and input conventions, plus direct weight/repository links.
Published names that resolve to the same checkpoint are merged as aliases.
A checkpoint count includes different layers, dictionary widths, sparsity settings
and training runs; it is not a count of distinct backbone models.

[Browse every checkpoint repository](published/README.md) ·
[Searchable catalog: web and local browsing](web/README.md) ·
[Load a pretrained SAE without training](../loading.md) ·
[Vision backbones for training](backbones.md)

The repository index and paginated model cards render directly on GitHub.
The interactive catalog searches a separate index and loads individual model
details on demand; use the linked browsing instructions to open it.

## Published weight examples by method

The following are example entry points, **not a complete model list or a claim
that only these methods have pretrained weights**. Use the complete repository
index or searchable catalog above for the full snapshot.

| SAE method | Example model information in this repository | Author configuration |
| --- | --- | --- |
| [ReLU + L1](../relu.md) | [GPT-2 feature splitting](published/jbloom-gpt2-small-feature-splitting-experiment-layer-8-dbe4582b-p1.md#gpt2-layer8-relu-768), [Goodfire Llama](published/goodfire-llama-3-1-8b-instruct-sae-l19-c605baef-p1.md#sae-67c6bcd9c84048110d5346b4), [CLIP patches](published/prisma-multimodal-sparse-autoencoder-clip-b-32-sae-vanilla-x64-layer-11-hook-resid-post-l1-1e-0-19d81acc-p1.md#clip-b32-layer11-relu-49152), [DINO](published/prisma-multimodal-dino-vanilla-x64-all-patches-0-resid-post-507-98-3a6c7680-p1.md#sae-f1ea8668fa9868f9acfb0a14) | Follow the individual cards for the exact source configuration and weight links. |
| [TopK](../topk.md) | [GPT-2 OAI layer 0](published/jbloom-gpt2-small-oai-v5-32k-resid-post-saes-c2dcb058-p1.md#sae-6783018355728933dae6d812), [Qwen Scope](published/qwen-sae-res-qwen3-1-7b-base-w32k-l0-100-f6e0808c-p1.md#sae-91dd570b8052f3f388447247), [CLIP CLS](published/prisma-multimodal-sae-top-k-64-cls-only-layer-11-hook-resid-post-5eda9b30-p1.md#sae-0fafbffebcc920f372943f8f) | [GPT-2 configuration](https://huggingface.co/jbloom/GPT2-Small-OAI-v5-32k-resid-post-SAEs/blob/21df74db7b9f690cd2403a20485cf75f46330d0d/v5_32k_layer_0.pt/cfg.json) |
| [JumpReLU](../jumprelu.md) | [Gemma Scope](published/google-gemma-scope-2b-pt-att-da0daf1e-p1.md#sae-40fd7a489d37f2b8bd438f17), [Gemma Scope 2](published/google-gemma-scope-2-4b-pt-568216a4-p5.md#sae-821c7f9ab3a7f8afbd9678fd) | Follow the individual cards for the exact source configuration and weight links. |
| [Gated](../gated.md) | [Pythia Gated dictionary](published/canrager-lm-sae-f1118512-p1.md#sae-21911514d66bc703e7143b75) | [GatedAutoEncoder / GatedSAETrainer](https://huggingface.co/canrager/lm_sae/blob/main/pythia70m_sweep_gated_ctx128_0730/resid_post_layer_3/trainer_0/config.json) |
| [BatchTopK](../batchtopk.md) | [Llama-3.1 BatchTopK dictionary](published/andyrdt-saes-llama-3-1-8b-instruct-8ffd883b-p1.md#sae-2c2c35702492e87a6b39f81e) | [BatchTopKSAE / BatchTopKTrainer](https://huggingface.co/andyrdt/saes-llama-3.1-8b-instruct/blob/main/resid_post_layer_11/trainer_1/config.json) |
| [Matryoshka BatchTopK](../matryoshka_batchtopk.md) | [Gemma-2 Matryoshka dictionary](published/adamkarvonen-saebench-gemma-2-2b-width-2pow12-date-0108-04a978f7-p1.md#sae-cbd3b7eaf315451abbf902c4) | [MatryoshkaBatchTopKSAE / trainer](https://huggingface.co/adamkarvonen/saebench_gemma-2-2b_width-2pow12_date-0108/blob/main/MatryoshkaBatchTopK_gemma-2-2b__0108/resid_post_layer_12/trainer_0/config.json) |

Some records in the current snapshot retain an unclassified method label even
though the author's checkpoint configuration identifies the algorithm. In
particular, 40 Gated, 20 BatchTopK and 18 Matryoshka BatchTopK entries are already
included among the 1,117 unclassified records. The linked configurations above
identify representative examples. An empty method-filter result does not
establish that a method has no published weights.

Published checkpoint availability differs across algorithms and backbones.
The [method index](../README.md) lists the library's trainable recipes; it does
not promise a pretrained dictionary for every recipe, backbone or layer. This
snapshot is also not an exhaustive inventory of all author releases: for
example, the separately published [RA-SAE DINOv2 dictionary](https://huggingface.co/matybohacek/RA-SAE-DINOv2-32k)
is outside these indexed source listings. Its source artifact is not an
automatically supported native loading recipe.

A model information card provides discovery and download information. Automatic
`probe.sae.from_pretrained(...)` loading currently supports the pinned GPT-2
layer-0 TopK recipe. Other source checkpoints need compatible conversion and
exact backbone/hook/preprocessing binding; see the [loading guide](../loading.md).

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
Use the [pretrained loading guide](../loading.md) for supported automatic
download/conversion recipes and existing native dictionaries. Other author
formats require an explicit conversion with the exact model/hook/preprocessing;
the [shared API](../API.md) describes that binding. Fields absent from the source
remain unspecified.

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
