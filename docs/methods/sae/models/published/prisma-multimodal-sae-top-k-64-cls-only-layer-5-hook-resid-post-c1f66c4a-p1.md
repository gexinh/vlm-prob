# Prisma-Multimodal/sae-top_k-64-cls_only-layer_5-hook_resid_post

[Model hub](../README.md) · [All checkpoint repositories](README.md)

Published SAE dictionaries for **open-clip:laion/CLIP-ViT-B-32-DataComp.XL-s13B-b90K**. Page 1 of 1.

[Author checkpoint repository](https://huggingface.co/Prisma-Multimodal/sae-top_k-64-cls_only-layer_5-hook_resid_post)

Select a dictionary below, download its author weights, and preserve its source model, hook and input conventions when converting to the native artifact format.

Pages: [1](prisma-multimodal-sae-top-k-64-cls-only-layer-5-hook-resid-post-c1f66c4a-p1.md)

<a id="sae-cf8f20e859b7ca81ff242e94"></a>

## weights.pt on open-clip:laion/CLIP-ViT-B-32-DataComp.XL-s13B-b90K

**Model ID:** `sae-cf8f20e859b7ca81ff242e94`

[Download weights](https://huggingface.co/Prisma-Multimodal/sae-top_k-64-cls_only-layer_5-hook_resid_post/resolve/cf8840b023929b709d6c7238b7cdefe97511e967/weights.pt)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `open-clip:laion/CLIP-ViT-B-32-DataComp.XL-s13B-b90K` |
| Method | [topk](../../topk.md) |
| Source hook / output | `blocks.5.hook_resid_post` |
| Layer | 5 |
| Activation width | 768 |
| Dictionary features | 49152 |
| Checkpoint license | Not specified |
| Checkpoint revision | `cf8840b023929b709d6c7238b7cdefe97511e967` |
| Tensor format | prisma |

**Input / activation conventions:**

`{"token_scope": "Top K SAEs (CLS only, k = 64)", "cls_token_only": true, "use_patches_only": false, "image_size": 224, "context_size": 1}`

**Published release names:** `Prisma-Multimodal/sae-top_k-64-cls_only-layer_5-hook_resid_post` / `weights.pt`

---

## Metadata sources

- [Pinned published listing 1](https://github.com/Prisma-Multimodal/ViT-Prisma/blob/64daf1425f7e5311844213fd0fb6f4127a30cd16/docs/sae_table.md)
