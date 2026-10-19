# Prisma-Multimodal/DINO-vanilla-x64-all_patches_1-resid_post-549-95

[Model hub](../README.md) · [All checkpoint repositories](README.md)

Published SAE dictionaries for **facebook/dino-vitb16**. Page 1 of 1.

[Author checkpoint repository](https://huggingface.co/Prisma-Multimodal/DINO-vanilla-x64-all_patches_1-resid_post-549-95)

Select a dictionary below, download its author weights, and preserve its source model, hook and input conventions when converting to the native artifact format.

Pages: [1](prisma-multimodal-dino-vanilla-x64-all-patches-1-resid-post-549-95-8b19f0dc-p1.md)

<a id="sae-9ca27cce3fb7724e72b47056"></a>

## weights.pt on facebook/dino-vitb16

**Model ID:** `sae-9ca27cce3fb7724e72b47056`

[Download weights](https://huggingface.co/Prisma-Multimodal/DINO-vanilla-x64-all_patches_1-resid_post-549-95/resolve/8d826594ece0ba46ba75eca1148dcde74eea7dea/weights.pt)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `facebook/dino-vitb16` |
| Method | [relu](../../relu.md) |
| Source hook / output | `blocks.1.hook_resid_post` |
| Layer | 1 |
| Activation width | 768 |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `8d826594ece0ba46ba75eca1148dcde74eea7dea` |
| Tensor format | prisma |

**Input / activation conventions:**

`{"normalize_activations": "layer_norm", "token_scope": "Vanilla SAEs (All Patches)", "cls_token_only": false, "use_patches_only": false, "image_size": 224, "context_size": 197}`

**Published release names:** `Prisma-Multimodal/DINO-vanilla-x64-all_patches_1-resid_post-549-95` / `weights.pt`

---

## Metadata sources

- [Pinned published listing 1](https://github.com/Prisma-Multimodal/ViT-Prisma/blob/64daf1425f7e5311844213fd0fb6f4127a30cd16/docs/sae_table.md)
