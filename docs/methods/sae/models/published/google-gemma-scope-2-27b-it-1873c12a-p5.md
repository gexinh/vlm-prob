# google/gemma-scope-2-27b-it

[Model hub](../README.md) · [All checkpoint repositories](README.md)

Published SAE dictionaries for **google/gemma-3-27b-it**. Page 5 of 18.

[Author checkpoint repository](https://huggingface.co/google/gemma-scope-2-27b-it)

Select a dictionary below, download its author weights, and preserve its source model, hook and input conventions when converting to the native artifact format.

Pages: [1](google-gemma-scope-2-27b-it-1873c12a-p1.md) · [2](google-gemma-scope-2-27b-it-1873c12a-p2.md) · [3](google-gemma-scope-2-27b-it-1873c12a-p3.md) · [4](google-gemma-scope-2-27b-it-1873c12a-p4.md) · [5](google-gemma-scope-2-27b-it-1873c12a-p5.md) · [6](google-gemma-scope-2-27b-it-1873c12a-p6.md) · [7](google-gemma-scope-2-27b-it-1873c12a-p7.md) · [8](google-gemma-scope-2-27b-it-1873c12a-p8.md) · [9](google-gemma-scope-2-27b-it-1873c12a-p9.md) · [10](google-gemma-scope-2-27b-it-1873c12a-p10.md) · [11](google-gemma-scope-2-27b-it-1873c12a-p11.md) · [12](google-gemma-scope-2-27b-it-1873c12a-p12.md) · [13](google-gemma-scope-2-27b-it-1873c12a-p13.md) · [14](google-gemma-scope-2-27b-it-1873c12a-p14.md) · [15](google-gemma-scope-2-27b-it-1873c12a-p15.md) · [16](google-gemma-scope-2-27b-it-1873c12a-p16.md) · [17](google-gemma-scope-2-27b-it-1873c12a-p17.md) · [18](google-gemma-scope-2-27b-it-1873c12a-p18.md)

<a id="sae-d04c18ebfdc969542920dec2"></a>

## layer_16_width_16k_l0_medium on google/gemma-3-27b-it

**Model ID:** `sae-d04c18ebfdc969542920dec2`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post/layer_16_width_16k_l0_medium)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.16.hook_resid_post` |
| Layer | 16 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res` / `layer_16_width_16k_l0_medium`

---

<a id="sae-c5b4b341e1ed46a54d199579"></a>

## layer_16_width_16k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-c5b4b341e1ed46a54d199579`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out/layer_16_width_16k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.16.attn.hook_z` |
| Layer | 16 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att` / `layer_16_width_16k_l0_small`

---

<a id="sae-954e4d460a1977ee29d4c0d3"></a>

## layer_16_width_16k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-954e4d460a1977ee29d4c0d3`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_16_width_16k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.16.attn.hook_z` |
| Layer | 16 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_16_width_16k_l0_small`

---

<a id="sae-ed35f3cf5b95d637152be333"></a>

## layer_16_width_16k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-ed35f3cf5b95d637152be333`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out/layer_16_width_16k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.16.hook_mlp_out` |
| Layer | 16 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp` / `layer_16_width_16k_l0_small`

---

<a id="sae-f52cda91237ce223b4882bf3"></a>

## layer_16_width_16k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-f52cda91237ce223b4882bf3`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out_all/layer_16_width_16k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.16.hook_mlp_out` |
| Layer | 16 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp-all` / `layer_16_width_16k_l0_small`

---

<a id="sae-bc2bcb4cda635bcc203e332b"></a>

## layer_16_width_16k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-bc2bcb4cda635bcc203e332b`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post/layer_16_width_16k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.16.hook_resid_post` |
| Layer | 16 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res` / `layer_16_width_16k_l0_small`

---

<a id="sae-fa24f776ed000f30f3df4550"></a>

## layer_16_width_16k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-fa24f776ed000f30f3df4550`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_16_width_16k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.16.hook_resid_post` |
| Layer | 16 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_16_width_16k_l0_small`

---

<a id="sae-a730453c5e1ce80155f66661"></a>

## layer_16_width_1m_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-a730453c5e1ce80155f66661`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post/layer_16_width_1m_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.16.hook_resid_post` |
| Layer | 16 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res` / `layer_16_width_1m_l0_big`

---

<a id="sae-1934bbd59d2c0fb9f522e114"></a>

## layer_16_width_1m_l0_medium on google/gemma-3-27b-it

**Model ID:** `sae-1934bbd59d2c0fb9f522e114`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post/layer_16_width_1m_l0_medium)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.16.hook_resid_post` |
| Layer | 16 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res` / `layer_16_width_1m_l0_medium`

---

<a id="sae-79b4db2911748cb12c4901d2"></a>

## layer_16_width_1m_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-79b4db2911748cb12c4901d2`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post/layer_16_width_1m_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.16.hook_resid_post` |
| Layer | 16 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res` / `layer_16_width_1m_l0_small`

---

<a id="sae-ad6c5fe151abf91c2e69024a"></a>

## layer_16_width_262k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-ad6c5fe151abf91c2e69024a`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out/layer_16_width_262k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.16.attn.hook_z` |
| Layer | 16 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att` / `layer_16_width_262k_l0_big`

---

<a id="sae-feae5b49f9c99cb2f44e744b"></a>

## layer_16_width_262k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-feae5b49f9c99cb2f44e744b`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_16_width_262k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.16.attn.hook_z` |
| Layer | 16 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_16_width_262k_l0_big`

---

<a id="sae-769f53c2101d1209e4972c76"></a>

## layer_16_width_262k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-769f53c2101d1209e4972c76`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out/layer_16_width_262k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.16.hook_mlp_out` |
| Layer | 16 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp` / `layer_16_width_262k_l0_big`

---

<a id="sae-9ce1dfd8f66af70a825258eb"></a>

## layer_16_width_262k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-9ce1dfd8f66af70a825258eb`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out_all/layer_16_width_262k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.16.hook_mlp_out` |
| Layer | 16 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp-all` / `layer_16_width_262k_l0_big`

---

<a id="sae-949b220482661c70f84ee3b7"></a>

## layer_16_width_262k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-949b220482661c70f84ee3b7`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post/layer_16_width_262k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.16.hook_resid_post` |
| Layer | 16 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res` / `layer_16_width_262k_l0_big`

---

<a id="sae-e07a20791e9a47a9ceeed1d6"></a>

## layer_16_width_262k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-e07a20791e9a47a9ceeed1d6`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_16_width_262k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.16.hook_resid_post` |
| Layer | 16 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_16_width_262k_l0_big`

---

<a id="sae-e6620a0e19d3c504b7f9897c"></a>

## layer_16_width_262k_l0_medium on google/gemma-3-27b-it

**Model ID:** `sae-e6620a0e19d3c504b7f9897c`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out/layer_16_width_262k_l0_medium)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.16.attn.hook_z` |
| Layer | 16 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att` / `layer_16_width_262k_l0_medium`

---

<a id="sae-3b0540c508897c93b388f726"></a>

## layer_16_width_262k_l0_medium on google/gemma-3-27b-it

**Model ID:** `sae-3b0540c508897c93b388f726`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out/layer_16_width_262k_l0_medium)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.16.hook_mlp_out` |
| Layer | 16 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp` / `layer_16_width_262k_l0_medium`

---

<a id="sae-19fa8a5154250a1b2865776c"></a>

## layer_16_width_262k_l0_medium on google/gemma-3-27b-it

**Model ID:** `sae-19fa8a5154250a1b2865776c`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post/layer_16_width_262k_l0_medium)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.16.hook_resid_post` |
| Layer | 16 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res` / `layer_16_width_262k_l0_medium`

---

<a id="sae-c6fd8a45963d42dab32eb23f"></a>

## layer_16_width_262k_l0_medium_seed_1 on google/gemma-3-27b-it

**Model ID:** `sae-c6fd8a45963d42dab32eb23f`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post/layer_16_width_262k_l0_medium_seed_1)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.16.hook_resid_post` |
| Layer | 16 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res` / `layer_16_width_262k_l0_medium_seed_1`

---

<a id="sae-a9c697fe34def4a2a242c96c"></a>

## layer_16_width_262k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-a9c697fe34def4a2a242c96c`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out/layer_16_width_262k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.16.attn.hook_z` |
| Layer | 16 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att` / `layer_16_width_262k_l0_small`

---

<a id="sae-828571d9084c0c132128a067"></a>

## layer_16_width_262k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-828571d9084c0c132128a067`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_16_width_262k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.16.attn.hook_z` |
| Layer | 16 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_16_width_262k_l0_small`

---

<a id="sae-c7ee367bb5e2bbd712fe08d2"></a>

## layer_16_width_262k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-c7ee367bb5e2bbd712fe08d2`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out/layer_16_width_262k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.16.hook_mlp_out` |
| Layer | 16 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp` / `layer_16_width_262k_l0_small`

---

<a id="sae-999ec53a3f253d9dac984abd"></a>

## layer_16_width_262k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-999ec53a3f253d9dac984abd`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out_all/layer_16_width_262k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.16.hook_mlp_out` |
| Layer | 16 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp-all` / `layer_16_width_262k_l0_small`

---

<a id="sae-2b68532eb19b3a1a1095acc3"></a>

## layer_16_width_262k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-2b68532eb19b3a1a1095acc3`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post/layer_16_width_262k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.16.hook_resid_post` |
| Layer | 16 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res` / `layer_16_width_262k_l0_small`

---

<a id="sae-957f726f424d9ea8ef76ae8b"></a>

## layer_16_width_262k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-957f726f424d9ea8ef76ae8b`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_16_width_262k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.16.hook_resid_post` |
| Layer | 16 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_16_width_262k_l0_small`

---

<a id="sae-a65c6c98db6bcb87b501986e"></a>

## layer_16_width_65k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-a65c6c98db6bcb87b501986e`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out/layer_16_width_65k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.16.attn.hook_z` |
| Layer | 16 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att` / `layer_16_width_65k_l0_big`

---

<a id="sae-d1d2d6ff38c132770bc2d3d2"></a>

## layer_16_width_65k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-d1d2d6ff38c132770bc2d3d2`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out/layer_16_width_65k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.16.hook_mlp_out` |
| Layer | 16 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp` / `layer_16_width_65k_l0_big`

---

<a id="sae-5a31a9112a25d4e5a8db00b3"></a>

## layer_16_width_65k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-5a31a9112a25d4e5a8db00b3`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post/layer_16_width_65k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.16.hook_resid_post` |
| Layer | 16 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res` / `layer_16_width_65k_l0_big`

---

<a id="sae-21a0172391f7110924b6718a"></a>

## layer_16_width_65k_l0_medium on google/gemma-3-27b-it

**Model ID:** `sae-21a0172391f7110924b6718a`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out/layer_16_width_65k_l0_medium)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.16.attn.hook_z` |
| Layer | 16 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att` / `layer_16_width_65k_l0_medium`

---

<a id="sae-c16ace61a1fb46b5f60fe175"></a>

## layer_16_width_65k_l0_medium on google/gemma-3-27b-it

**Model ID:** `sae-c16ace61a1fb46b5f60fe175`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out/layer_16_width_65k_l0_medium)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.16.hook_mlp_out` |
| Layer | 16 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp` / `layer_16_width_65k_l0_medium`

---

<a id="sae-420a8d178dc82b957b6135b3"></a>

## layer_16_width_65k_l0_medium on google/gemma-3-27b-it

**Model ID:** `sae-420a8d178dc82b957b6135b3`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post/layer_16_width_65k_l0_medium)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.16.hook_resid_post` |
| Layer | 16 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res` / `layer_16_width_65k_l0_medium`

---

<a id="sae-71dc2b9f1d43cdb17c4bb729"></a>

## layer_16_width_65k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-71dc2b9f1d43cdb17c4bb729`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out/layer_16_width_65k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.16.attn.hook_z` |
| Layer | 16 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att` / `layer_16_width_65k_l0_small`

---

<a id="sae-0e08fb839c917f2fb53c8fc3"></a>

## layer_16_width_65k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-0e08fb839c917f2fb53c8fc3`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out/layer_16_width_65k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.16.hook_mlp_out` |
| Layer | 16 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp` / `layer_16_width_65k_l0_small`

---

<a id="sae-7e722aeca22262c95652e0bc"></a>

## layer_16_width_65k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-7e722aeca22262c95652e0bc`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post/layer_16_width_65k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.16.hook_resid_post` |
| Layer | 16 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res` / `layer_16_width_65k_l0_small`

---

<a id="sae-b4694ff131a58156383ff403"></a>

## layer_17_width_16k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-b4694ff131a58156383ff403`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_17_width_16k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.17.attn.hook_z` |
| Layer | 17 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_17_width_16k_l0_big`

---

<a id="sae-2711eae3e73e7fb7440c8ba0"></a>

## layer_17_width_16k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-2711eae3e73e7fb7440c8ba0`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out_all/layer_17_width_16k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.17.hook_mlp_out` |
| Layer | 17 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp-all` / `layer_17_width_16k_l0_big`

---

<a id="sae-fe4589269044cac1411838a2"></a>

## layer_17_width_16k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-fe4589269044cac1411838a2`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_17_width_16k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.17.hook_resid_post` |
| Layer | 17 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_17_width_16k_l0_big`

---

<a id="sae-4a9f21504507fb151f42bd07"></a>

## layer_17_width_16k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-4a9f21504507fb151f42bd07`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_17_width_16k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.17.attn.hook_z` |
| Layer | 17 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_17_width_16k_l0_small`

---

<a id="sae-bc566974f6d494cbc2ba14af"></a>

## layer_17_width_16k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-bc566974f6d494cbc2ba14af`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out_all/layer_17_width_16k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.17.hook_mlp_out` |
| Layer | 17 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp-all` / `layer_17_width_16k_l0_small`

---

<a id="sae-f0285786244a2e382930462b"></a>

## layer_17_width_16k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-f0285786244a2e382930462b`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_17_width_16k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.17.hook_resid_post` |
| Layer | 17 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_17_width_16k_l0_small`

---

<a id="sae-4d0e3e83cdaa8592f2ef9534"></a>

## layer_17_width_262k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-4d0e3e83cdaa8592f2ef9534`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_17_width_262k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.17.attn.hook_z` |
| Layer | 17 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_17_width_262k_l0_big`

---

<a id="sae-e86cda9afd3bea62f9b46099"></a>

## layer_17_width_262k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-e86cda9afd3bea62f9b46099`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out_all/layer_17_width_262k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.17.hook_mlp_out` |
| Layer | 17 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp-all` / `layer_17_width_262k_l0_big`

---

<a id="sae-edc682c5b5e73efca0761ae2"></a>

## layer_17_width_262k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-edc682c5b5e73efca0761ae2`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_17_width_262k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.17.hook_resid_post` |
| Layer | 17 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_17_width_262k_l0_big`

---

<a id="sae-cfba0814d695c668afcd20c7"></a>

## layer_17_width_262k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-cfba0814d695c668afcd20c7`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_17_width_262k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.17.attn.hook_z` |
| Layer | 17 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_17_width_262k_l0_small`

---

<a id="sae-ce139423d2fb98138fbc023b"></a>

## layer_17_width_262k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-ce139423d2fb98138fbc023b`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out_all/layer_17_width_262k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.17.hook_mlp_out` |
| Layer | 17 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp-all` / `layer_17_width_262k_l0_small`

---

<a id="sae-5933aaa445dcf5bd114cee77"></a>

## layer_17_width_262k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-5933aaa445dcf5bd114cee77`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_17_width_262k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.17.hook_resid_post` |
| Layer | 17 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_17_width_262k_l0_small`

---

<a id="sae-31714ec0f858d09d231b1599"></a>

## layer_18_width_16k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-31714ec0f858d09d231b1599`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_18_width_16k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.18.attn.hook_z` |
| Layer | 18 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_18_width_16k_l0_big`

---

<a id="sae-e2cc26002e02a0e47c6c0f0f"></a>

## layer_18_width_16k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-e2cc26002e02a0e47c6c0f0f`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out_all/layer_18_width_16k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.18.hook_mlp_out` |
| Layer | 18 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp-all` / `layer_18_width_16k_l0_big`

---

<a id="sae-7ec6af3056c34ff497089a3b"></a>

## layer_18_width_16k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-7ec6af3056c34ff497089a3b`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_18_width_16k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.18.hook_resid_post` |
| Layer | 18 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_18_width_16k_l0_big`

---

## Metadata sources

- [Pinned published listing 1](https://github.com/decoderesearch/SAELens/blob/30c4502466785dd7809a307f7b705df187978aa3/sae_lens/pretrained_saes.yaml)
