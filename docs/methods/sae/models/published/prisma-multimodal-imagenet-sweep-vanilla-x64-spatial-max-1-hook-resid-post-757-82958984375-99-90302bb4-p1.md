# Prisma-Multimodal/imagenet-sweep-vanilla-x64-Spatial_max_1-hook_resid_post-757.82958984375-99

[Model hub](../README.md) · [All checkpoint repositories](README.md)

Published SAE dictionaries for **open-clip:laion/CLIP-ViT-B-32-DataComp.XL-s13B-b90K**. Page 1 of 1.

[Author checkpoint repository](https://huggingface.co/Prisma-Multimodal/imagenet-sweep-vanilla-x64-Spatial_max_1-hook_resid_post-757.82958984375-99)

Select a dictionary below, download its author weights, and preserve its source model, hook and input conventions when converting to the native artifact format.

Pages: [1](prisma-multimodal-imagenet-sweep-vanilla-x64-spatial-max-1-hook-resid-post-757-82958984375-99-90302bb4-p1.md)

<a id="sae-c3eb199bf05436ceaca478fd"></a>

## weights.pt on open-clip:laion/CLIP-ViT-B-32-DataComp.XL-s13B-b90K

**Model ID:** `sae-c3eb199bf05436ceaca478fd`

[Download weights](https://huggingface.co/Prisma-Multimodal/imagenet-sweep-vanilla-x64-Spatial_max_1-hook_resid_post-757.82958984375-99/resolve/67f252c3e77dd4c72e705d292981a56c1444d846/weights.pt)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `open-clip:laion/CLIP-ViT-B-32-DataComp.XL-s13B-b90K` |
| Method | [relu](../../relu.md) |
| Source hook / output | `blocks.1.hook_resid_post` |
| Layer | 1 |
| Activation width | 768 |
| Dictionary features | 49152 |
| Checkpoint license | Not specified |
| Checkpoint revision | `67f252c3e77dd4c72e705d292981a56c1444d846` |
| Tensor format | prisma |

**Input / activation conventions:**

`{"normalize_activations": "layer_norm", "token_scope": "Vanilla Spatial Patches", "cls_token_only": false, "use_patches_only": true, "image_size": 224, "context_size": 49}`

**Published release names:** `Prisma-Multimodal/imagenet-sweep-vanilla-x64-Spatial_max_1-hook_resid_post-757.82958984375-99` / `weights.pt`

---

## Metadata sources

- [Pinned published listing 1](https://github.com/Prisma-Multimodal/ViT-Prisma/blob/64daf1425f7e5311844213fd0fb6f4127a30cd16/docs/sae_table.md)
