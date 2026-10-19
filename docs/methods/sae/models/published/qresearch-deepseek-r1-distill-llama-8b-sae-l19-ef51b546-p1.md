# qresearch/DeepSeek-R1-Distill-Llama-8B-SAE-l19

[Model hub](../README.md) · [All checkpoint repositories](README.md)

Published SAE dictionaries for **deepseek-ai/DeepSeek-R1-Distill-Llama-8B**. Page 1 of 1.

[Author checkpoint repository](https://huggingface.co/qresearch/DeepSeek-R1-Distill-Llama-8B-SAE-l19)

Select a dictionary below, download its author weights, and preserve its source model, hook and input conventions when converting to the native artifact format.

Pages: [1](qresearch-deepseek-r1-distill-llama-8b-sae-l19-ef51b546-p1.md)

<a id="sae-f80de4274d1467f86b0b08c0"></a>

## blocks.19.hook_resid_post on deepseek-ai/DeepSeek-R1-Distill-Llama-8B

**Model ID:** `sae-f80de4274d1467f86b0b08c0`

[Download weights](https://huggingface.co/qresearch/DeepSeek-R1-Distill-Llama-8B-SAE-l19/resolve/main/DeepSeek-R1-Distill-Llama-8B-SAE-l19.pt)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `deepseek-ai/DeepSeek-R1-Distill-Llama-8B` |
| Method | [relu](../../relu.md) |
| Source hook / output | `blocks.19.hook_resid_post` |
| Layer | 19 |
| Activation width | 4096 |
| Dictionary features | 65536 |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "normalize_activations": "none", "apply_b_dec_to_input": false}`

**Published release names:** `deepseek-r1-distill-llama-8b-qresearch` / `blocks.19.hook_resid_post`

---

## Metadata sources

- [Pinned published listing 1](https://github.com/decoderesearch/SAELens/blob/30c4502466785dd7809a307f7b705df187978aa3/sae_lens/pretrained_saes.yaml)
