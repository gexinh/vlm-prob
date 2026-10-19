# Prisma-Multimodal/sparse-autoencoder-clip-b-32-sae-vanilla-x64-layer-4-hook_mlp_out-l1-1e-05

[Model hub](../README.md) · [All checkpoint repositories](README.md)

Published SAE dictionaries for **open-clip:laion/CLIP-ViT-B-32-DataComp.XL-s13B-b90K**. Page 1 of 1.

[Author checkpoint repository](https://huggingface.co/Prisma-Multimodal/sparse-autoencoder-clip-b-32-sae-vanilla-x64-layer-4-hook_mlp_out-l1-1e-05)

Select a dictionary below, download its author weights, and preserve its source model, hook and input conventions when converting to the native artifact format.

Pages: [1](prisma-multimodal-sparse-autoencoder-clip-b-32-sae-vanilla-x64-layer-4-hook-mlp-out-l1-1e-05-c406e95a-p1.md)

<a id="sae-f68d7273774eba2b107a77fa"></a>

## n_images_2600058.pt on open-clip:laion/CLIP-ViT-B-32-DataComp.XL-s13B-b90K

**Model ID:** `sae-f68d7273774eba2b107a77fa`

[Download weights](https://huggingface.co/Prisma-Multimodal/sparse-autoencoder-clip-b-32-sae-vanilla-x64-layer-4-hook_mlp_out-l1-1e-05/resolve/5292d390fdb6212fed88eba19a7fedea0c7bc261/n_images_2600058.pt)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `open-clip:laion/CLIP-ViT-B-32-DataComp.XL-s13B-b90K` |
| Method | [relu](../../relu.md) |
| Source hook / output | `blocks.4.hook_mlp_out` |
| Layer | 4 |
| Activation width | 768 |
| Dictionary features | 49152 |
| Checkpoint license | apache-2.0 |
| Checkpoint revision | `5292d390fdb6212fed88eba19a7fedea0c7bc261` |
| Tensor format | prisma |

**Input / activation conventions:**

`{"token_scope": "Vanilla SAEs (All Patches)", "cls_token_only": false, "use_patches_only": false, "image_size": 224, "context_size": 50}`

**Published release names:** `Prisma-Multimodal/sparse-autoencoder-clip-b-32-sae-vanilla-x64-layer-4-hook_mlp_out-l1-1e-05` / `n_images_2600058.pt`

---

## Metadata sources

- [Pinned published listing 1](https://github.com/Prisma-Multimodal/ViT-Prisma/blob/64daf1425f7e5311844213fd0fb6f4127a30cd16/docs/sae_table.md)
