# Prisma-Multimodal/imagenet-sweep-vanilla-x64-Spatial_max_9-hook_resid_post-854.891540527344-99

[Model hub](../README.md) · [All checkpoint repositories](README.md)

Published SAE dictionaries for **open-clip:laion/CLIP-ViT-B-32-DataComp.XL-s13B-b90K**. Page 1 of 1.

[Author checkpoint repository](https://huggingface.co/Prisma-Multimodal/imagenet-sweep-vanilla-x64-Spatial_max_9-hook_resid_post-854.891540527344-99)

Select a dictionary below, download its author weights, and preserve its source model, hook and input conventions when converting to the native artifact format.

Pages: [1](prisma-multimodal-imagenet-sweep-vanilla-x64-spatial-max-9-hook-resid-post-854-891540527344-99-34b94475-p1.md)

<a id="sae-2f43929f73123055f0abc341"></a>

## weights.pt on open-clip:laion/CLIP-ViT-B-32-DataComp.XL-s13B-b90K

**Model ID:** `sae-2f43929f73123055f0abc341`

[Download weights](https://huggingface.co/Prisma-Multimodal/imagenet-sweep-vanilla-x64-Spatial_max_9-hook_resid_post-854.891540527344-99/resolve/103552e06f03dfe68ab6096c1c798af468a6807c/weights.pt)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `open-clip:laion/CLIP-ViT-B-32-DataComp.XL-s13B-b90K` |
| Method | [relu](../../relu.md) |
| Source hook / output | `blocks.9.hook_resid_post` |
| Layer | 9 |
| Activation width | 768 |
| Dictionary features | 49152 |
| Checkpoint license | Not specified |
| Checkpoint revision | `103552e06f03dfe68ab6096c1c798af468a6807c` |
| Tensor format | prisma |

**Input / activation conventions:**

`{"normalize_activations": "layer_norm", "token_scope": "Vanilla Spatial Patches", "cls_token_only": false, "use_patches_only": true, "image_size": 224, "context_size": 49}`

**Published release names:** `Prisma-Multimodal/imagenet-sweep-vanilla-x64-Spatial_max_9-hook_resid_post-854.891540527344-99` / `weights.pt`

---

## Metadata sources

- [Pinned published listing 1](https://github.com/Prisma-Multimodal/ViT-Prisma/blob/64daf1425f7e5311844213fd0fb6f4127a30cd16/docs/sae_table.md)
