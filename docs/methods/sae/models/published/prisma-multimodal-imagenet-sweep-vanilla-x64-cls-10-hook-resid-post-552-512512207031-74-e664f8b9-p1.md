# Prisma-Multimodal/imagenet-sweep-vanilla-x64-CLS_10-hook_resid_post-552.512512207031-74

[Model hub](../README.md) · [All checkpoint repositories](README.md)

Published SAE dictionaries for **open-clip:laion/CLIP-ViT-B-32-DataComp.XL-s13B-b90K**. Page 1 of 1.

[Author checkpoint repository](https://huggingface.co/Prisma-Multimodal/imagenet-sweep-vanilla-x64-CLS_10-hook_resid_post-552.512512207031-74)

Select a dictionary below, download its author weights, and preserve its source model, hook and input conventions when converting to the native artifact format.

Pages: [1](prisma-multimodal-imagenet-sweep-vanilla-x64-cls-10-hook-resid-post-552-512512207031-74-e664f8b9-p1.md)

<a id="sae-86ac8a2e9b4ff0a886d24057"></a>

## weights.pt on open-clip:laion/CLIP-ViT-B-32-DataComp.XL-s13B-b90K

**Model ID:** `sae-86ac8a2e9b4ff0a886d24057`

[Download weights](https://huggingface.co/Prisma-Multimodal/imagenet-sweep-vanilla-x64-CLS_10-hook_resid_post-552.512512207031-74/resolve/765c2de91f9453f0bad5c80312f59e61964f2e49/weights.pt)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `open-clip:laion/CLIP-ViT-B-32-DataComp.XL-s13B-b90K` |
| Method | [relu](../../relu.md) |
| Source hook / output | `blocks.10.hook_resid_post` |
| Layer | 10 |
| Activation width | 768 |
| Dictionary features | 49152 |
| Checkpoint license | Not specified |
| Checkpoint revision | `765c2de91f9453f0bad5c80312f59e61964f2e49` |
| Tensor format | prisma |

**Input / activation conventions:**

`{"normalize_activations": "layer_norm", "token_scope": "Vanilla SAEs (CLS only)", "cls_token_only": true, "use_patches_only": false, "image_size": 224, "context_size": 1}`

**Published release names:** `Prisma-Multimodal/imagenet-sweep-vanilla-x64-CLS_10-hook_resid_post-552.512512207031-74` / `weights.pt`

---

## Metadata sources

- [Pinned published listing 1](https://github.com/Prisma-Multimodal/ViT-Prisma/blob/64daf1425f7e5311844213fd0fb6f4127a30cd16/docs/sae_table.md)
