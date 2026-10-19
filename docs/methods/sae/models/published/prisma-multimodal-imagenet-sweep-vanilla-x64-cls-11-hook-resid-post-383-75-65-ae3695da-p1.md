# Prisma-Multimodal/imagenet-sweep-vanilla-x64-CLS_11-hook_resid_post-383.75-65

[Model hub](../README.md) · [All checkpoint repositories](README.md)

Published SAE dictionaries for **open-clip:laion/CLIP-ViT-B-32-DataComp.XL-s13B-b90K**. Page 1 of 1.

[Author checkpoint repository](https://huggingface.co/Prisma-Multimodal/imagenet-sweep-vanilla-x64-CLS_11-hook_resid_post-383.75-65)

Select a dictionary below, download its author weights, and preserve its source model, hook and input conventions when converting to the native artifact format.

Pages: [1](prisma-multimodal-imagenet-sweep-vanilla-x64-cls-11-hook-resid-post-383-75-65-ae3695da-p1.md)

<a id="sae-a1a1057ac74f9290dcc5a4d8"></a>

## weights.pt on open-clip:laion/CLIP-ViT-B-32-DataComp.XL-s13B-b90K

**Model ID:** `sae-a1a1057ac74f9290dcc5a4d8`

[Download weights](https://huggingface.co/Prisma-Multimodal/imagenet-sweep-vanilla-x64-CLS_11-hook_resid_post-383.75-65/resolve/ff2600336274e7c17b8d1dd691a691a8c86a93c6/weights.pt)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `open-clip:laion/CLIP-ViT-B-32-DataComp.XL-s13B-b90K` |
| Method | [relu](../../relu.md) |
| Source hook / output | `blocks.11.hook_resid_post` |
| Layer | 11 |
| Activation width | 768 |
| Dictionary features | 49152 |
| Checkpoint license | Not specified |
| Checkpoint revision | `ff2600336274e7c17b8d1dd691a691a8c86a93c6` |
| Tensor format | prisma |

**Input / activation conventions:**

`{"normalize_activations": "layer_norm", "token_scope": "Vanilla SAEs (CLS only)", "cls_token_only": true, "use_patches_only": false, "image_size": 224, "context_size": 1}`

**Published release names:** `Prisma-Multimodal/imagenet-sweep-vanilla-x64-CLS_11-hook_resid_post-383.75-65` / `weights.pt`

---

## Metadata sources

- [Pinned published listing 1](https://github.com/Prisma-Multimodal/ViT-Prisma/blob/64daf1425f7e5311844213fd0fb6f4127a30cd16/docs/sae_table.md)
