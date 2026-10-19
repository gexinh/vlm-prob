# google/gemma-scope-2-27b-it

[Model hub](../README.md) · [All checkpoint repositories](README.md)

Published SAE dictionaries for **google/gemma-3-27b-it**. Page 2 of 18.

[Author checkpoint repository](https://huggingface.co/google/gemma-scope-2-27b-it)

Select a dictionary below, download its author weights, and preserve its source model, hook and input conventions when converting to the native artifact format.

Pages: [1](google-gemma-scope-2-27b-it-1873c12a-p1.md) · [2](google-gemma-scope-2-27b-it-1873c12a-p2.md) · [3](google-gemma-scope-2-27b-it-1873c12a-p3.md) · [4](google-gemma-scope-2-27b-it-1873c12a-p4.md) · [5](google-gemma-scope-2-27b-it-1873c12a-p5.md) · [6](google-gemma-scope-2-27b-it-1873c12a-p6.md) · [7](google-gemma-scope-2-27b-it-1873c12a-p7.md) · [8](google-gemma-scope-2-27b-it-1873c12a-p8.md) · [9](google-gemma-scope-2-27b-it-1873c12a-p9.md) · [10](google-gemma-scope-2-27b-it-1873c12a-p10.md) · [11](google-gemma-scope-2-27b-it-1873c12a-p11.md) · [12](google-gemma-scope-2-27b-it-1873c12a-p12.md) · [13](google-gemma-scope-2-27b-it-1873c12a-p13.md) · [14](google-gemma-scope-2-27b-it-1873c12a-p14.md) · [15](google-gemma-scope-2-27b-it-1873c12a-p15.md) · [16](google-gemma-scope-2-27b-it-1873c12a-p16.md) · [17](google-gemma-scope-2-27b-it-1873c12a-p17.md) · [18](google-gemma-scope-2-27b-it-1873c12a-p18.md)

<a id="sae-02e26d1cdcf0269407bb467a"></a>

## layer_4_width_16k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-02e26d1cdcf0269407bb467a`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_4_width_16k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.4.hook_resid_post` |
| Layer | 4 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_4_width_16k_l0_big`

---

<a id="sae-9a4399a5db5ffc022a307654"></a>

## layer_4_width_16k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-9a4399a5db5ffc022a307654`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_4_width_16k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.4.attn.hook_z` |
| Layer | 4 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_4_width_16k_l0_small`

---

<a id="sae-b0a30089f6c7d179dfb67751"></a>

## layer_4_width_16k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-b0a30089f6c7d179dfb67751`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out_all/layer_4_width_16k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.4.hook_mlp_out` |
| Layer | 4 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp-all` / `layer_4_width_16k_l0_small`

---

<a id="sae-39284f33440c2d445826191a"></a>

## layer_4_width_16k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-39284f33440c2d445826191a`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_4_width_16k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.4.hook_resid_post` |
| Layer | 4 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_4_width_16k_l0_small`

---

<a id="sae-11fcde97386af49309fa1d48"></a>

## layer_4_width_262k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-11fcde97386af49309fa1d48`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_4_width_262k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.4.attn.hook_z` |
| Layer | 4 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_4_width_262k_l0_big`

---

<a id="sae-5055dc850ea33df227b34af6"></a>

## layer_4_width_262k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-5055dc850ea33df227b34af6`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out_all/layer_4_width_262k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.4.hook_mlp_out` |
| Layer | 4 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp-all` / `layer_4_width_262k_l0_big`

---

<a id="sae-2345f49b62bae286f47f5354"></a>

## layer_4_width_262k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-2345f49b62bae286f47f5354`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_4_width_262k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.4.hook_resid_post` |
| Layer | 4 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_4_width_262k_l0_big`

---

<a id="sae-81e4ca3a634a4a81f052d86f"></a>

## layer_4_width_262k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-81e4ca3a634a4a81f052d86f`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_4_width_262k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.4.attn.hook_z` |
| Layer | 4 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_4_width_262k_l0_small`

---

<a id="sae-60032e3ed1209bb2bbf457d3"></a>

## layer_4_width_262k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-60032e3ed1209bb2bbf457d3`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out_all/layer_4_width_262k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.4.hook_mlp_out` |
| Layer | 4 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp-all` / `layer_4_width_262k_l0_small`

---

<a id="sae-382edbb55ec7add39fac3fef"></a>

## layer_4_width_262k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-382edbb55ec7add39fac3fef`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_4_width_262k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.4.hook_resid_post` |
| Layer | 4 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_4_width_262k_l0_small`

---

<a id="sae-a53f45453def8436ecf79521"></a>

## layer_5_width_16k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-a53f45453def8436ecf79521`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_5_width_16k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.5.attn.hook_z` |
| Layer | 5 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_5_width_16k_l0_big`

---

<a id="sae-1e007dfee6f01a93b62f8c13"></a>

## layer_5_width_16k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-1e007dfee6f01a93b62f8c13`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out_all/layer_5_width_16k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.5.hook_mlp_out` |
| Layer | 5 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp-all` / `layer_5_width_16k_l0_big`

---

<a id="sae-d0b137bb8f711f812d673967"></a>

## layer_5_width_16k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-d0b137bb8f711f812d673967`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_5_width_16k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.5.hook_resid_post` |
| Layer | 5 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_5_width_16k_l0_big`

---

<a id="sae-a1b00b3fa08034d666e1b226"></a>

## layer_5_width_16k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-a1b00b3fa08034d666e1b226`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_5_width_16k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.5.attn.hook_z` |
| Layer | 5 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_5_width_16k_l0_small`

---

<a id="sae-c1193f4174fd86b7023e4519"></a>

## layer_5_width_16k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-c1193f4174fd86b7023e4519`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out_all/layer_5_width_16k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.5.hook_mlp_out` |
| Layer | 5 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp-all` / `layer_5_width_16k_l0_small`

---

<a id="sae-fc660bbe6397b921577d3b6c"></a>

## layer_5_width_16k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-fc660bbe6397b921577d3b6c`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_5_width_16k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.5.hook_resid_post` |
| Layer | 5 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_5_width_16k_l0_small`

---

<a id="sae-7d9d6fd032a9dd91d26d33f0"></a>

## layer_5_width_262k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-7d9d6fd032a9dd91d26d33f0`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_5_width_262k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.5.attn.hook_z` |
| Layer | 5 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_5_width_262k_l0_big`

---

<a id="sae-2d6f0fd7a4d7383af123a46e"></a>

## layer_5_width_262k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-2d6f0fd7a4d7383af123a46e`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out_all/layer_5_width_262k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.5.hook_mlp_out` |
| Layer | 5 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp-all` / `layer_5_width_262k_l0_big`

---

<a id="sae-39a7971012103e718d1a48c9"></a>

## layer_5_width_262k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-39a7971012103e718d1a48c9`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_5_width_262k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.5.hook_resid_post` |
| Layer | 5 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_5_width_262k_l0_big`

---

<a id="sae-d2d19e2589b2e544723f73e2"></a>

## layer_5_width_262k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-d2d19e2589b2e544723f73e2`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_5_width_262k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.5.attn.hook_z` |
| Layer | 5 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_5_width_262k_l0_small`

---

<a id="sae-b0f2369a7472b1d04b5b55bd"></a>

## layer_5_width_262k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-b0f2369a7472b1d04b5b55bd`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out_all/layer_5_width_262k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.5.hook_mlp_out` |
| Layer | 5 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp-all` / `layer_5_width_262k_l0_small`

---

<a id="sae-b23a3b44d9638d7302e48469"></a>

## layer_5_width_262k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-b23a3b44d9638d7302e48469`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_5_width_262k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.5.hook_resid_post` |
| Layer | 5 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_5_width_262k_l0_small`

---

<a id="sae-a344fe8adf3c6bad6ef3f66b"></a>

## layer_6_width_16k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-a344fe8adf3c6bad6ef3f66b`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_6_width_16k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.6.attn.hook_z` |
| Layer | 6 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_6_width_16k_l0_big`

---

<a id="sae-2ce03c24605cf9eeb1931f3e"></a>

## layer_6_width_16k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-2ce03c24605cf9eeb1931f3e`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out_all/layer_6_width_16k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.6.hook_mlp_out` |
| Layer | 6 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp-all` / `layer_6_width_16k_l0_big`

---

<a id="sae-353eb2d3f388626e6887a7a1"></a>

## layer_6_width_16k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-353eb2d3f388626e6887a7a1`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_6_width_16k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.6.hook_resid_post` |
| Layer | 6 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_6_width_16k_l0_big`

---

<a id="sae-ac66c500046a4aaa26a8ebba"></a>

## layer_6_width_16k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-ac66c500046a4aaa26a8ebba`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_6_width_16k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.6.attn.hook_z` |
| Layer | 6 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_6_width_16k_l0_small`

---

<a id="sae-d836c504c0647c0ddb0a47eb"></a>

## layer_6_width_16k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-d836c504c0647c0ddb0a47eb`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out_all/layer_6_width_16k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.6.hook_mlp_out` |
| Layer | 6 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp-all` / `layer_6_width_16k_l0_small`

---

<a id="sae-6bbe5d48d919310c72d64dd7"></a>

## layer_6_width_16k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-6bbe5d48d919310c72d64dd7`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_6_width_16k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.6.hook_resid_post` |
| Layer | 6 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_6_width_16k_l0_small`

---

<a id="sae-10f7fe397e5c6d30f547d0e3"></a>

## layer_6_width_262k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-10f7fe397e5c6d30f547d0e3`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_6_width_262k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.6.attn.hook_z` |
| Layer | 6 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_6_width_262k_l0_big`

---

<a id="sae-b4e7f312fcd9a1ffe790eff7"></a>

## layer_6_width_262k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-b4e7f312fcd9a1ffe790eff7`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out_all/layer_6_width_262k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.6.hook_mlp_out` |
| Layer | 6 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp-all` / `layer_6_width_262k_l0_big`

---

<a id="sae-4b2cc45ca0f212a0934bd9a0"></a>

## layer_6_width_262k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-4b2cc45ca0f212a0934bd9a0`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_6_width_262k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.6.hook_resid_post` |
| Layer | 6 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_6_width_262k_l0_big`

---

<a id="sae-e3b76221f3691e8a83bef8af"></a>

## layer_6_width_262k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-e3b76221f3691e8a83bef8af`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_6_width_262k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.6.attn.hook_z` |
| Layer | 6 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_6_width_262k_l0_small`

---

<a id="sae-497241f9f650184167a74719"></a>

## layer_6_width_262k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-497241f9f650184167a74719`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out_all/layer_6_width_262k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.6.hook_mlp_out` |
| Layer | 6 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp-all` / `layer_6_width_262k_l0_small`

---

<a id="sae-99e3a3efd38ba011716690c4"></a>

## layer_6_width_262k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-99e3a3efd38ba011716690c4`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_6_width_262k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.6.hook_resid_post` |
| Layer | 6 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_6_width_262k_l0_small`

---

<a id="sae-7cae32ba382bacd05c9951c1"></a>

## layer_7_width_16k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-7cae32ba382bacd05c9951c1`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_7_width_16k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.7.attn.hook_z` |
| Layer | 7 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_7_width_16k_l0_big`

---

<a id="sae-27ae5c0dff850e8980f50dad"></a>

## layer_7_width_16k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-27ae5c0dff850e8980f50dad`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out_all/layer_7_width_16k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.7.hook_mlp_out` |
| Layer | 7 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp-all` / `layer_7_width_16k_l0_big`

---

<a id="sae-7d77c20be02c79a8744912d5"></a>

## layer_7_width_16k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-7d77c20be02c79a8744912d5`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_7_width_16k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.7.hook_resid_post` |
| Layer | 7 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_7_width_16k_l0_big`

---

<a id="sae-a10b68981e4f39c2113b11b3"></a>

## layer_7_width_16k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-a10b68981e4f39c2113b11b3`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_7_width_16k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.7.attn.hook_z` |
| Layer | 7 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_7_width_16k_l0_small`

---

<a id="sae-a10016002958af148af038e9"></a>

## layer_7_width_16k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-a10016002958af148af038e9`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out_all/layer_7_width_16k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.7.hook_mlp_out` |
| Layer | 7 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp-all` / `layer_7_width_16k_l0_small`

---

<a id="sae-ea476b73e0000496a178080e"></a>

## layer_7_width_16k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-ea476b73e0000496a178080e`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_7_width_16k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.7.hook_resid_post` |
| Layer | 7 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_7_width_16k_l0_small`

---

<a id="sae-2cf8b765ed506d40c96cddcb"></a>

## layer_7_width_262k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-2cf8b765ed506d40c96cddcb`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_7_width_262k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.7.attn.hook_z` |
| Layer | 7 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_7_width_262k_l0_big`

---

<a id="sae-ff9f7afcb10dc99dbb3dfc6b"></a>

## layer_7_width_262k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-ff9f7afcb10dc99dbb3dfc6b`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out_all/layer_7_width_262k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.7.hook_mlp_out` |
| Layer | 7 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp-all` / `layer_7_width_262k_l0_big`

---

<a id="sae-909914fbb552cbdf6d8619e9"></a>

## layer_7_width_262k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-909914fbb552cbdf6d8619e9`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_7_width_262k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.7.hook_resid_post` |
| Layer | 7 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_7_width_262k_l0_big`

---

<a id="sae-963f4aa733fd2523283f76d5"></a>

## layer_7_width_262k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-963f4aa733fd2523283f76d5`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_7_width_262k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.7.attn.hook_z` |
| Layer | 7 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_7_width_262k_l0_small`

---

<a id="sae-a01ad534ff1db8c0dfdf97dd"></a>

## layer_7_width_262k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-a01ad534ff1db8c0dfdf97dd`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out_all/layer_7_width_262k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.7.hook_mlp_out` |
| Layer | 7 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp-all` / `layer_7_width_262k_l0_small`

---

<a id="sae-b3677154e39d3f7c514c19c6"></a>

## layer_7_width_262k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-b3677154e39d3f7c514c19c6`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_7_width_262k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.7.hook_resid_post` |
| Layer | 7 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_7_width_262k_l0_small`

---

<a id="sae-31697fdc00fa0536744015bb"></a>

## layer_8_width_16k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-31697fdc00fa0536744015bb`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_8_width_16k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.8.attn.hook_z` |
| Layer | 8 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_8_width_16k_l0_big`

---

<a id="sae-30421ca90452b2a5513f8669"></a>

## layer_8_width_16k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-30421ca90452b2a5513f8669`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out_all/layer_8_width_16k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.8.hook_mlp_out` |
| Layer | 8 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp-all` / `layer_8_width_16k_l0_big`

---

<a id="sae-85a83ddd6d4239c4d803922b"></a>

## layer_8_width_16k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-85a83ddd6d4239c4d803922b`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_8_width_16k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.8.hook_resid_post` |
| Layer | 8 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_8_width_16k_l0_big`

---

<a id="sae-b07993abd3948f7f13f5d3d8"></a>

## layer_8_width_16k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-b07993abd3948f7f13f5d3d8`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_8_width_16k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.8.attn.hook_z` |
| Layer | 8 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_8_width_16k_l0_small`

---

## Metadata sources

- [Pinned published listing 1](https://github.com/decoderesearch/SAELens/blob/30c4502466785dd7809a307f7b705df187978aa3/sae_lens/pretrained_saes.yaml)
