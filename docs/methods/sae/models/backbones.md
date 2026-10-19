# Vision backbones for SAE training

[Model hub](README.md) · [Training guide](../training/README.md)

Use these pretrained **vision backbones** to collect activations and train an SAE. Each card lists the model checkpoint and output layer; the [training guide](../training/README.md) covers activation collection, dictionary fitting and evaluation.

<a id="backbone-siglip-vit-b16"></a>

## SigLIP ViT-B/16

**Model ID:** `backbone-siglip-vit-b16`

[Download weights](https://huggingface.co/timm/vit_base_patch16_siglip_224.webli/resolve/8db107e594ed7552e44e108f16650d81ac6de9a6/model.safetensors)

| Property | Value |
| --- | --- |
| Artifact | Vision backbone; no SAE dictionary |
| Base model | `timm/vit_base_patch16_siglip_224.webli` |
| Method | not_applicable |
| Source hook / output | `forward_features` |
| Layer | Not specified |
| Activation width | 768 |
| Dictionary features | Not specified |
| Checkpoint license | apache-2.0 |
| Checkpoint revision | `8db107e594ed7552e44e108f16650d81ac6de9a6` |
| Tensor format | timm |

**Input / activation conventions:**

`{"image_size": 224, "resize": "square 224, bicubic, antialias", "mean": [0.5, 0.5, 0.5], "std": [0.5, 0.5, 0.5], "scope": "Overcomplete wrapper input transform; preserve checkpoint-specific input conventions when training a new SAE"}`

**Weight SHA256:** `b07f8a4bad267232a87888b2527d054d130b1fba18f75e6e26c17766dc26bdc2`

[Checkpoint configuration](https://huggingface.co/timm/vit_base_patch16_siglip_224.webli/resolve/8db107e594ed7552e44e108f16650d81ac6de9a6/config.json)

[Model repository](https://huggingface.co/timm/vit_base_patch16_siglip_224.webli)

---

<a id="backbone-vit-b16"></a>

## ViT-B/16, explicit AugReg2 variant

**Model ID:** `backbone-vit-b16`

[Download weights](https://huggingface.co/timm/vit_base_patch16_224.augreg2_in21k_ft_in1k/resolve/063c6c38a5d8510b2e57df480445e94b231dad2c/model.safetensors)

| Property | Value |
| --- | --- |
| Artifact | Vision backbone; no SAE dictionary |
| Base model | `timm/vit_base_patch16_224.augreg2_in21k_ft_in1k` |
| Method | not_applicable |
| Source hook / output | `forward_features` |
| Layer | Not specified |
| Activation width | 768 |
| Dictionary features | Not specified |
| Checkpoint license | apache-2.0 |
| Checkpoint revision | `063c6c38a5d8510b2e57df480445e94b231dad2c` |
| Tensor format | timm |

**Input / activation conventions:**

`{"image_size": 224, "resize": "square 224, bicubic, antialias", "mean": [0.5, 0.5, 0.5], "std": [0.5, 0.5, 0.5], "scope": "Overcomplete wrapper input transform; preserve checkpoint-specific input conventions when training a new SAE"}`

**Weight SHA256:** `32aa17d6e17b43500f531d5f6dc9bc93e56ed8841b8a75682e1bb295d722405b`

[Checkpoint configuration](https://huggingface.co/timm/vit_base_patch16_224.augreg2_in21k_ft_in1k/resolve/063c6c38a5d8510b2e57df480445e94b231dad2c/config.json)

The upstream wrapper uses untagged vit_base_patch16_224. This card pins one explicit published variant; it does not claim the alias pins these weights.

[Model repository](https://huggingface.co/timm/vit_base_patch16_224.augreg2_in21k_ft_in1k)

---

<a id="backbone-resnet-v2-bit"></a>

## ResNet-V2-BiT 50x1

**Model ID:** `backbone-resnet-v2-bit`

[Download weights](https://huggingface.co/timm/resnetv2_50x1_bit.goog_distilled_in1k/resolve/39aef79105c877c0d9f9410a761fab8ea28542c3/model.safetensors)

| Property | Value |
| --- | --- |
| Artifact | Vision backbone; no SAE dictionary |
| Base model | `timm/resnetv2_50x1_bit.goog_distilled_in1k` |
| Method | not_applicable |
| Source hook / output | `forward_features` |
| Layer | Not specified |
| Activation width | 2048 |
| Dictionary features | Not specified |
| Checkpoint license | apache-2.0 |
| Checkpoint revision | `39aef79105c877c0d9f9410a761fab8ea28542c3` |
| Tensor format | timm |

**Input / activation conventions:**

`{"image_size": 224, "resize": "square 224, bicubic, antialias", "mean": [0.5, 0.5, 0.5], "std": [0.5, 0.5, 0.5], "scope": "Overcomplete wrapper input transform; preserve checkpoint-specific input conventions when training a new SAE"}`

**Weight SHA256:** `d8a84ddc4683b81fb691141c571960a6e64be1c50a3e543a62bd959bf43c98f3`

[Checkpoint configuration](https://huggingface.co/timm/resnetv2_50x1_bit.goog_distilled_in1k/resolve/39aef79105c877c0d9f9410a761fab8ea28542c3/config.json)

[Model repository](https://huggingface.co/timm/resnetv2_50x1_bit.goog_distilled_in1k)

---

<a id="backbone-convnext-small"></a>

## ConvNeXt Small

**Model ID:** `backbone-convnext-small`

[Download weights](https://huggingface.co/timm/convnext_small.fb_in1k/resolve/7941c0c00f3ca64f5048de06464b90ad12da0ccb/model.safetensors)

| Property | Value |
| --- | --- |
| Artifact | Vision backbone; no SAE dictionary |
| Base model | `timm/convnext_small.fb_in1k` |
| Method | not_applicable |
| Source hook / output | `forward_features` |
| Layer | Not specified |
| Activation width | 768 |
| Dictionary features | Not specified |
| Checkpoint license | apache-2.0 |
| Checkpoint revision | `7941c0c00f3ca64f5048de06464b90ad12da0ccb` |
| Tensor format | timm |

**Input / activation conventions:**

`{"image_size": 224, "resize": "square 224, bicubic, antialias", "mean": [0.485, 0.456, 0.406], "std": [0.229, 0.224, 0.225], "scope": "Overcomplete wrapper input transform; preserve checkpoint-specific input conventions when training a new SAE"}`

**Weight SHA256:** `5ec5ed9e97fb835093aaf3e6c3fce406b160b367117b6a2b8c7b703386218d1b`

[Checkpoint configuration](https://huggingface.co/timm/convnext_small.fb_in1k/resolve/7941c0c00f3ca64f5048de06464b90ad12da0ccb/config.json)

[Model repository](https://huggingface.co/timm/convnext_small.fb_in1k)

---

<a id="backbone-dinov2-s14"></a>

## DINOv2 ViT-S/14

**Model ID:** `backbone-dinov2-s14`

[Download weights](https://dl.fbaipublicfiles.com/dinov2/dinov2_vits14/dinov2_vits14_pretrain.pth)

| Property | Value |
| --- | --- |
| Artifact | Vision backbone; no SAE dictionary |
| Base model | `facebookresearch/dinov2:dinov2_vits14` |
| Method | not_applicable |
| Source hook / output | `x_norm_patchtokens` |
| Layer | Not specified |
| Activation width | 384 |
| Dictionary features | Not specified |
| Checkpoint license | apache-2.0 |
| Checkpoint revision | `Not specified` |
| Tensor format | torch_hub |

**Input / activation conventions:**

`{"image_size": 224, "resize": "square 224, bicubic, antialias", "mean": [0.485, 0.456, 0.406], "std": [0.229, 0.224, 0.225]}`

[Model repository](https://github.com/facebookresearch/dinov2)

---
