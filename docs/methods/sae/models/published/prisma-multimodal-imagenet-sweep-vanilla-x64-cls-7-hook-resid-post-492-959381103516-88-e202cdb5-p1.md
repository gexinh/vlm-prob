# Prisma-Multimodal/imagenet-sweep-vanilla-x64-CLS_7-hook_resid_post-492.959381103516-88

[Model hub](../README.md) · [All checkpoint repositories](README.md)

Published SAE dictionaries for **open-clip:laion/CLIP-ViT-B-32-DataComp.XL-s13B-b90K**. Page 1 of 1.

[Author checkpoint repository](https://huggingface.co/Prisma-Multimodal/imagenet-sweep-vanilla-x64-CLS_7-hook_resid_post-492.959381103516-88)

Select a dictionary below, download its author weights, and preserve its source model, hook and input conventions when converting to the native artifact format.

Pages: [1](prisma-multimodal-imagenet-sweep-vanilla-x64-cls-7-hook-resid-post-492-959381103516-88-e202cdb5-p1.md)

<a id="sae-b3e2f3c2d6074ac51cb81c0e"></a>

## weights.pt on open-clip:laion/CLIP-ViT-B-32-DataComp.XL-s13B-b90K

**Model ID:** `sae-b3e2f3c2d6074ac51cb81c0e`

[Download weights](https://huggingface.co/Prisma-Multimodal/imagenet-sweep-vanilla-x64-CLS_7-hook_resid_post-492.959381103516-88/resolve/36ee6452a83a0101b8ffee2ca6b4459b76bd037b/weights.pt)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `open-clip:laion/CLIP-ViT-B-32-DataComp.XL-s13B-b90K` |
| Method | [relu](../../relu.md) |
| Source hook / output | `blocks.7.hook_resid_post` |
| Layer | 7 |
| Activation width | 768 |
| Dictionary features | 49152 |
| Checkpoint license | Not specified |
| Checkpoint revision | `36ee6452a83a0101b8ffee2ca6b4459b76bd037b` |
| Tensor format | prisma |

**Input / activation conventions:**

`{"normalize_activations": "layer_norm", "token_scope": "Vanilla SAEs (CLS only)", "cls_token_only": true, "use_patches_only": false, "image_size": 224, "context_size": 1}`

**Published release names:** `Prisma-Multimodal/imagenet-sweep-vanilla-x64-CLS_7-hook_resid_post-492.959381103516-88` / `weights.pt`

---

## Metadata sources

- [Pinned published listing 1](https://github.com/Prisma-Multimodal/ViT-Prisma/blob/64daf1425f7e5311844213fd0fb6f4127a30cd16/docs/sae_table.md)
