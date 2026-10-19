# Goodfire/Llama-3.3-70B-Instruct-SAE-l50

[Model hub](../README.md) · [All checkpoint repositories](README.md)

Published SAE dictionaries for **meta-llama/Llama-3.3-70B-Instruct**. Page 1 of 1.

[Author checkpoint repository](https://huggingface.co/Goodfire/Llama-3.3-70B-Instruct-SAE-l50)

Select a dictionary below, download its author weights, and preserve its source model, hook and input conventions when converting to the native artifact format.

Pages: [1](goodfire-llama-3-3-70b-instruct-sae-l50-fc45854c-p1.md)

<a id="sae-238447a2c9870a399a3e6ad9"></a>

## layer_50 on meta-llama/Llama-3.3-70B-Instruct

**Model ID:** `sae-238447a2c9870a399a3e6ad9`

[Download weights](https://huggingface.co/Goodfire/Llama-3.3-70B-Instruct-SAE-l50/resolve/main/Llama-3.3-70B-Instruct-SAE-l50.pt)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `meta-llama/Llama-3.3-70B-Instruct` |
| Method | [relu](../../relu.md) |
| Source hook / output | `blocks.50.hook_resid_post` |
| Layer | 50 |
| Activation width | 8192 |
| Dictionary features | 65536 |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"apply_b_dec_to_input": false}`

**Published release names:** `goodfire-llama-3.3-70b-instruct` / `layer_50`

---

## Metadata sources

- [Pinned published listing 1](https://github.com/decoderesearch/SAELens/blob/30c4502466785dd7809a307f7b705df187978aa3/sae_lens/pretrained_saes.yaml)
