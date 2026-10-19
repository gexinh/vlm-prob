# Prisma-Multimodal/DINO-vanilla-x64-all_patches_7-resid_post-1086-98

[Model hub](../README.md) · [All checkpoint repositories](README.md)

Published SAE dictionaries for **facebook/dino-vitb16**. Page 1 of 1.

[Author checkpoint repository](https://huggingface.co/Prisma-Multimodal/DINO-vanilla-x64-all_patches_7-resid_post-1086-98)

Select a dictionary below, download its author weights, and preserve its source model, hook and input conventions when converting to the native artifact format.

Pages: [1](prisma-multimodal-dino-vanilla-x64-all-patches-7-resid-post-1086-98-5de834b7-p1.md)

<a id="sae-71e3dbf4a4616a3f32ed1d7f"></a>

## weights.pt on facebook/dino-vitb16

**Model ID:** `sae-71e3dbf4a4616a3f32ed1d7f`

[Download weights](https://huggingface.co/Prisma-Multimodal/DINO-vanilla-x64-all_patches_7-resid_post-1086-98/resolve/195a814def34f86e6b78fefd45a643eb246508dc/weights.pt)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `facebook/dino-vitb16` |
| Method | [relu](../../relu.md) |
| Source hook / output | `blocks.7.hook_resid_post` |
| Layer | 7 |
| Activation width | 768 |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `195a814def34f86e6b78fefd45a643eb246508dc` |
| Tensor format | prisma |

**Input / activation conventions:**

`{"normalize_activations": "layer_norm", "token_scope": "Vanilla SAEs (All Patches)", "cls_token_only": false, "use_patches_only": false, "image_size": 224, "context_size": 197}`

**Published release names:** `Prisma-Multimodal/DINO-vanilla-x64-all_patches_7-resid_post-1086-98` / `weights.pt`

---

## Metadata sources

- [Pinned published listing 1](https://github.com/Prisma-Multimodal/ViT-Prisma/blob/64daf1425f7e5311844213fd0fb6f4127a30cd16/docs/sae_table.md)
