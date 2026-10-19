# Prisma-Multimodal/imagenet-sweep-vanilla-x64-Spatial_max_6-hook_resid_post-1006.57165527344-99

[Model hub](../README.md) · [All checkpoint repositories](README.md)

Published SAE dictionaries for **open-clip:laion/CLIP-ViT-B-32-DataComp.XL-s13B-b90K**. Page 1 of 1.

[Author checkpoint repository](https://huggingface.co/Prisma-Multimodal/imagenet-sweep-vanilla-x64-Spatial_max_6-hook_resid_post-1006.57165527344-99)

Select a dictionary below, download its author weights, and preserve its source model, hook and input conventions when converting to the native artifact format.

Pages: [1](prisma-multimodal-imagenet-sweep-vanilla-x64-spatial-max-6-hook-resid-post-1006-57165527344-99-9ca90cc0-p1.md)

<a id="sae-be8aea5e5d803797fa3d84dd"></a>

## weights.pt on open-clip:laion/CLIP-ViT-B-32-DataComp.XL-s13B-b90K

**Model ID:** `sae-be8aea5e5d803797fa3d84dd`

[Download weights](https://huggingface.co/Prisma-Multimodal/imagenet-sweep-vanilla-x64-Spatial_max_6-hook_resid_post-1006.57165527344-99/resolve/6e85800f1878b775a73c4962f05dcfdfb47f68bd/weights.pt)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `open-clip:laion/CLIP-ViT-B-32-DataComp.XL-s13B-b90K` |
| Method | [relu](../../relu.md) |
| Source hook / output | `blocks.6.hook_resid_post` |
| Layer | 6 |
| Activation width | 768 |
| Dictionary features | 49152 |
| Checkpoint license | Not specified |
| Checkpoint revision | `6e85800f1878b775a73c4962f05dcfdfb47f68bd` |
| Tensor format | prisma |

**Input / activation conventions:**

`{"normalize_activations": "layer_norm", "token_scope": "Vanilla Spatial Patches", "cls_token_only": false, "use_patches_only": true, "image_size": 224, "context_size": 49}`

**Published release names:** `Prisma-Multimodal/imagenet-sweep-vanilla-x64-Spatial_max_6-hook_resid_post-1006.57165527344-99` / `weights.pt`

---

## Metadata sources

- [Pinned published listing 1](https://github.com/Prisma-Multimodal/ViT-Prisma/blob/64daf1425f7e5311844213fd0fb6f4127a30cd16/docs/sae_table.md)
