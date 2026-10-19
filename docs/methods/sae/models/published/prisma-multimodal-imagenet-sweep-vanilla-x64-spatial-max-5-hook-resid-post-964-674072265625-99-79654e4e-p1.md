# Prisma-Multimodal/imagenet-sweep-vanilla-x64-Spatial_max_5-hook_resid_post-964.674072265625-99

[Model hub](../README.md) · [All checkpoint repositories](README.md)

Published SAE dictionaries for **open-clip:laion/CLIP-ViT-B-32-DataComp.XL-s13B-b90K**. Page 1 of 1.

[Author checkpoint repository](https://huggingface.co/Prisma-Multimodal/imagenet-sweep-vanilla-x64-Spatial_max_5-hook_resid_post-964.674072265625-99)

Select a dictionary below, download its author weights, and preserve its source model, hook and input conventions when converting to the native artifact format.

Pages: [1](prisma-multimodal-imagenet-sweep-vanilla-x64-spatial-max-5-hook-resid-post-964-674072265625-99-79654e4e-p1.md)

<a id="sae-459f715adb690bdfc13187be"></a>

## weights.pt on open-clip:laion/CLIP-ViT-B-32-DataComp.XL-s13B-b90K

**Model ID:** `sae-459f715adb690bdfc13187be`

[Download weights](https://huggingface.co/Prisma-Multimodal/imagenet-sweep-vanilla-x64-Spatial_max_5-hook_resid_post-964.674072265625-99/resolve/b706687068d7c14ae6e96e168a83cffa39ab8e27/weights.pt)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `open-clip:laion/CLIP-ViT-B-32-DataComp.XL-s13B-b90K` |
| Method | [relu](../../relu.md) |
| Source hook / output | `blocks.5.hook_resid_post` |
| Layer | 5 |
| Activation width | 768 |
| Dictionary features | 49152 |
| Checkpoint license | Not specified |
| Checkpoint revision | `b706687068d7c14ae6e96e168a83cffa39ab8e27` |
| Tensor format | prisma |

**Input / activation conventions:**

`{"normalize_activations": "layer_norm", "token_scope": "Vanilla Spatial Patches", "cls_token_only": false, "use_patches_only": true, "image_size": 224, "context_size": 49}`

**Published release names:** `Prisma-Multimodal/imagenet-sweep-vanilla-x64-Spatial_max_5-hook_resid_post-964.674072265625-99` / `weights.pt`

---

## Metadata sources

- [Pinned published listing 1](https://github.com/Prisma-Multimodal/ViT-Prisma/blob/64daf1425f7e5311844213fd0fb6f4127a30cd16/docs/sae_table.md)
