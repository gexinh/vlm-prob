# Prisma-Multimodal/sae-top_k-64-cls_only-layer_1-hook_resid_post

[Model hub](../README.md) · [All checkpoint repositories](README.md)

Published SAE dictionaries for **open-clip:laion/CLIP-ViT-B-32-DataComp.XL-s13B-b90K**. Page 1 of 1.

[Author checkpoint repository](https://huggingface.co/Prisma-Multimodal/sae-top_k-64-cls_only-layer_1-hook_resid_post)

Select a dictionary below, download its author weights, and preserve its source model, hook and input conventions when converting to the native artifact format.

Pages: [1](prisma-multimodal-sae-top-k-64-cls-only-layer-1-hook-resid-post-29b9f564-p1.md)

<a id="sae-1d0d97efc1c45a769bfe9dee"></a>

## weights.pt on open-clip:laion/CLIP-ViT-B-32-DataComp.XL-s13B-b90K

**Model ID:** `sae-1d0d97efc1c45a769bfe9dee`

[Download weights](https://huggingface.co/Prisma-Multimodal/sae-top_k-64-cls_only-layer_1-hook_resid_post/resolve/8f0be31adc16157e158c3b9d14c4bc4f282e337f/weights.pt)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `open-clip:laion/CLIP-ViT-B-32-DataComp.XL-s13B-b90K` |
| Method | [topk](../../topk.md) |
| Source hook / output | `blocks.1.hook_resid_post` |
| Layer | 1 |
| Activation width | 768 |
| Dictionary features | 49152 |
| Checkpoint license | Not specified |
| Checkpoint revision | `8f0be31adc16157e158c3b9d14c4bc4f282e337f` |
| Tensor format | prisma |

**Input / activation conventions:**

`{"token_scope": "Top K SAEs (CLS only, k = 64)", "cls_token_only": true, "use_patches_only": false, "image_size": 224, "context_size": 1}`

**Published release names:** `Prisma-Multimodal/sae-top_k-64-cls_only-layer_1-hook_resid_post` / `weights.pt`

---

## Metadata sources

- [Pinned published listing 1](https://github.com/Prisma-Multimodal/ViT-Prisma/blob/64daf1425f7e5311844213fd0fb6f4127a30cd16/docs/sae_table.md)
