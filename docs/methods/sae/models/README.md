# SAE models and checkpoints

Find SAE dictionaries for language and vision backbones. The [model directory](published/README.md) groups **9,660 checkpoint variants** from **151 weight repositories** by backbone, with activation layers, hooks and download links.

[Browse models by backbone](published/README.md) · [Search the catalog](web/README.md) · [Load a pretrained SAE](../loading.md) · [Train an SAE](../training/README.md)

## Featured checkpoints

| Backbone / collection | SAE method | Model information | Author weights |
| --- | --- | --- | --- |
| GPT-2 Small | [TopK](../topk.md) | [Model card](published/jbloom-gpt2-small-oai-v5-32k-resid-post-saes-c2dcb058-p1.md#sae-6783018355728933dae6d812) | [Download](https://huggingface.co/jbloom/GPT2-Small-OAI-v5-32k-resid-post-SAEs/resolve/21df74db7b9f690cd2403a20485cf75f46330d0d/v5_32k_layer_0.pt/sae_weights.safetensors) |
| Gemma-2 2B · Gemma Scope | [JumpReLU](../jumprelu.md) | [Model card](published/google-gemma-scope-2b-pt-att-da0daf1e-p1.md#sae-40fd7a489d37f2b8bd438f17) | [Checkpoint files](https://huggingface.co/google/gemma-scope-2b-pt-att/tree/main/layer_0/width_16k/average_l0_104) |
| Gemma-3 4B · Gemma Scope 2 | [JumpReLU](../jumprelu.md) | [Model card](published/google-gemma-scope-2-4b-pt-568216a4-p5.md#sae-821c7f9ab3a7f8afbd9678fd) | [Checkpoint files](https://huggingface.co/google/gemma-scope-2-4b-pt/tree/main/attn_out/layer_17_width_16k_l0_big) |
| Llama-3.1 8B Instruct · Goodfire | [ReLU + L1](../relu.md) | [Model card](published/goodfire-llama-3-1-8b-instruct-sae-l19-c605baef-p1.md#sae-67c6bcd9c84048110d5346b4) | [Download](https://huggingface.co/Goodfire/Llama-3.1-8B-Instruct-SAE-l19/resolve/main/Llama-3.1-8B-Instruct-SAE-l19.pth) |
| Llama-3.1 8B Instruct | [BatchTopK](../batchtopk.md) | [Model card](published/andyrdt-saes-llama-3-1-8b-instruct-8ffd883b-p1.md#sae-2c2c35702492e87a6b39f81e) | [Checkpoint files](https://huggingface.co/andyrdt/saes-llama-3.1-8b-instruct/tree/main/resid_post_layer_11/trainer_1) |
| Qwen3 1.7B Base · Qwen Scope | [TopK](../topk.md) | [Model card](published/qwen-sae-res-qwen3-1-7b-base-w32k-l0-100-f6e0808c-p1.md#sae-91dd570b8052f3f388447247) | [Download](https://huggingface.co/Qwen/SAE-Res-Qwen3-1.7B-Base-W32K-L0_100/resolve/main/layer0.sae.pt) |
| Pythia 70M | [Gated](../gated.md) | [Model card](published/canrager-lm-sae-f1118512-p1.md#sae-21911514d66bc703e7143b75) | [Checkpoint files](https://huggingface.co/canrager/lm_sae/tree/main/pythia70m_sweep_gated_ctx128_0730/resid_post_layer_3/trainer_0) |
| Gemma-2 2B | [Matryoshka BatchTopK](../matryoshka_batchtopk.md) | [Model card](published/adamkarvonen-saebench-gemma-2-2b-width-2pow12-date-0108-04a978f7-p1.md#sae-cbd3b7eaf315451abbf902c4) | [Checkpoint files](https://huggingface.co/adamkarvonen/saebench_gemma-2-2b_width-2pow12_date-0108/tree/main/MatryoshkaBatchTopK_gemma-2-2b__0108/resid_post_layer_12/trainer_0) |
| CLIP ViT-B/32 · all patches | [ReLU + L1](../relu.md) | [Model card](published/prisma-multimodal-sparse-autoencoder-clip-b-32-sae-vanilla-x64-layer-11-hook-resid-post-l1-1e-0-19d81acc-p1.md#clip-b32-layer11-relu-49152) | [Download](https://huggingface.co/Prisma-Multimodal/sparse-autoencoder-clip-b-32-sae-vanilla-x64-layer-11-hook_resid_post-l1-1e-05/resolve/2b1cb17ffb8b06e7f45a699dfc97d417f9879be4/weights.pt) |
| CLIP ViT-B/32 · CLS token | [TopK](../topk.md) | [Model card](published/prisma-multimodal-sae-top-k-64-cls-only-layer-11-hook-resid-post-5eda9b30-p1.md#sae-0fafbffebcc920f372943f8f) | [Download](https://huggingface.co/Prisma-Multimodal/sae-top_k-64-cls_only-layer_11-hook_resid_post/resolve/73611b78df558947515c213b56be74c3b2be91f0/weights.pt) |
| DINO ViT-B/16 · all patches | [ReLU + L1](../relu.md) | [Model card](published/prisma-multimodal-dino-vanilla-x64-all-patches-0-resid-post-507-98-3a6c7680-p1.md#sae-f1ea8668fa9868f9acfb0a14) | [Download](https://huggingface.co/Prisma-Multimodal/DINO-vanilla-x64-all_patches_0-resid_post-507-98/resolve/c44792cf34df589b145a8f9f2d7751e9e0d4c6f3/weights.pt) |

## Find a dictionary in Python

Search by backbone or select a specific dictionary to inspect its activation coordinates, input conventions and weights.

```python
from vlmprobe.sae import list_models, get_model_card

qwen_models = list_models(query="Qwen", limit=20)
vision_topk = list_models(modality="vision", method="topk")
card = get_model_card("clip-b32-layer11-relu-49152")
print(card["base_model"], card["hook"], card["dimensions"])
print(card["links"]["checkpoint"])
```

Use the [loading guide](../loading.md) to load a supported published checkpoint or a saved native dictionary with the matching backbone and input preparation.

## Train and register your own dictionary

The [training guide](../training/README.md) covers activation collection, train/validation splits, configuration, checkpointing and resume. The [shared API](../API.md) describes native artifacts and local model-card registration. For image activations, choose a [vision backbone](backbones.md) and follow its input preprocessing.
