# google/gemma-scope-2-27b-it

[Model hub](../README.md) · [All checkpoint repositories](README.md)

Published SAE dictionaries for **google/gemma-3-27b-it**. Page 3 of 18.

[Author checkpoint repository](https://huggingface.co/google/gemma-scope-2-27b-it)

Select a dictionary below, download its author weights, and preserve its source model, hook and input conventions when converting to the native artifact format.

Pages: [1](google-gemma-scope-2-27b-it-1873c12a-p1.md) · [2](google-gemma-scope-2-27b-it-1873c12a-p2.md) · [3](google-gemma-scope-2-27b-it-1873c12a-p3.md) · [4](google-gemma-scope-2-27b-it-1873c12a-p4.md) · [5](google-gemma-scope-2-27b-it-1873c12a-p5.md) · [6](google-gemma-scope-2-27b-it-1873c12a-p6.md) · [7](google-gemma-scope-2-27b-it-1873c12a-p7.md) · [8](google-gemma-scope-2-27b-it-1873c12a-p8.md) · [9](google-gemma-scope-2-27b-it-1873c12a-p9.md) · [10](google-gemma-scope-2-27b-it-1873c12a-p10.md) · [11](google-gemma-scope-2-27b-it-1873c12a-p11.md) · [12](google-gemma-scope-2-27b-it-1873c12a-p12.md) · [13](google-gemma-scope-2-27b-it-1873c12a-p13.md) · [14](google-gemma-scope-2-27b-it-1873c12a-p14.md) · [15](google-gemma-scope-2-27b-it-1873c12a-p15.md) · [16](google-gemma-scope-2-27b-it-1873c12a-p16.md) · [17](google-gemma-scope-2-27b-it-1873c12a-p17.md) · [18](google-gemma-scope-2-27b-it-1873c12a-p18.md)

<a id="sae-178856c490a2a1b9116d05bc"></a>

## layer_8_width_16k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-178856c490a2a1b9116d05bc`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out_all/layer_8_width_16k_l0_small)

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

**Published release names:** `gemma-scope-2-27b-it-mlp-all` / `layer_8_width_16k_l0_small`

---

<a id="sae-a2f2f3f0563097ebaa671757"></a>

## layer_8_width_16k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-a2f2f3f0563097ebaa671757`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_8_width_16k_l0_small)

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

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_8_width_16k_l0_small`

---

<a id="sae-f223ff348ae8dde7d92c26d1"></a>

## layer_8_width_262k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-f223ff348ae8dde7d92c26d1`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_8_width_262k_l0_big)

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

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_8_width_262k_l0_big`

---

<a id="sae-a810fed4c52f071cd386153b"></a>

## layer_8_width_262k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-a810fed4c52f071cd386153b`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out_all/layer_8_width_262k_l0_big)

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

**Published release names:** `gemma-scope-2-27b-it-mlp-all` / `layer_8_width_262k_l0_big`

---

<a id="sae-4572679738881b7024bcc90a"></a>

## layer_8_width_262k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-4572679738881b7024bcc90a`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_8_width_262k_l0_big)

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

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_8_width_262k_l0_big`

---

<a id="sae-3599fcab52ce588d6bb7e5e4"></a>

## layer_8_width_262k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-3599fcab52ce588d6bb7e5e4`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_8_width_262k_l0_small)

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

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_8_width_262k_l0_small`

---

<a id="sae-b1a1f38e70620337bae6f2a9"></a>

## layer_8_width_262k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-b1a1f38e70620337bae6f2a9`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out_all/layer_8_width_262k_l0_small)

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

**Published release names:** `gemma-scope-2-27b-it-mlp-all` / `layer_8_width_262k_l0_small`

---

<a id="sae-4c92b97df966d28c3fb36e05"></a>

## layer_8_width_262k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-4c92b97df966d28c3fb36e05`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_8_width_262k_l0_small)

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

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_8_width_262k_l0_small`

---

<a id="sae-d78dbd26ac47729568d4abb2"></a>

## layer_9_width_16k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-d78dbd26ac47729568d4abb2`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_9_width_16k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.9.attn.hook_z` |
| Layer | 9 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_9_width_16k_l0_big`

---

<a id="sae-9abac8c7d3fbda48bcfbba71"></a>

## layer_9_width_16k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-9abac8c7d3fbda48bcfbba71`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out_all/layer_9_width_16k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.9.hook_mlp_out` |
| Layer | 9 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp-all` / `layer_9_width_16k_l0_big`

---

<a id="sae-43add6c3d58503c58210ce46"></a>

## layer_9_width_16k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-43add6c3d58503c58210ce46`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_9_width_16k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.9.hook_resid_post` |
| Layer | 9 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_9_width_16k_l0_big`

---

<a id="sae-0652b22787affa2c198727a4"></a>

## layer_9_width_16k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-0652b22787affa2c198727a4`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_9_width_16k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.9.attn.hook_z` |
| Layer | 9 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_9_width_16k_l0_small`

---

<a id="sae-06a0ece6ba62d18ff4b19147"></a>

## layer_9_width_16k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-06a0ece6ba62d18ff4b19147`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out_all/layer_9_width_16k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.9.hook_mlp_out` |
| Layer | 9 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp-all` / `layer_9_width_16k_l0_small`

---

<a id="sae-2cd2e74f74a030cbfadc0a34"></a>

## layer_9_width_16k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-2cd2e74f74a030cbfadc0a34`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_9_width_16k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.9.hook_resid_post` |
| Layer | 9 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_9_width_16k_l0_small`

---

<a id="sae-4fdbfe92ca3fcfe3e02b7ac1"></a>

## layer_9_width_262k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-4fdbfe92ca3fcfe3e02b7ac1`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_9_width_262k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.9.attn.hook_z` |
| Layer | 9 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_9_width_262k_l0_big`

---

<a id="sae-d905c92361df853992df24fd"></a>

## layer_9_width_262k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-d905c92361df853992df24fd`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out_all/layer_9_width_262k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.9.hook_mlp_out` |
| Layer | 9 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp-all` / `layer_9_width_262k_l0_big`

---

<a id="sae-d5525f74ac7c64310207484a"></a>

## layer_9_width_262k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-d5525f74ac7c64310207484a`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_9_width_262k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.9.hook_resid_post` |
| Layer | 9 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_9_width_262k_l0_big`

---

<a id="sae-ab9d9b59c6463c0ed87c7319"></a>

## layer_9_width_262k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-ab9d9b59c6463c0ed87c7319`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_9_width_262k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.9.attn.hook_z` |
| Layer | 9 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_9_width_262k_l0_small`

---

<a id="sae-3ada3009143b1152ede3f462"></a>

## layer_9_width_262k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-3ada3009143b1152ede3f462`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out_all/layer_9_width_262k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.9.hook_mlp_out` |
| Layer | 9 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp-all` / `layer_9_width_262k_l0_small`

---

<a id="sae-e9dfc7772015afc10c038c4e"></a>

## layer_9_width_262k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-e9dfc7772015afc10c038c4e`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_9_width_262k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.9.hook_resid_post` |
| Layer | 9 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_9_width_262k_l0_small`

---

<a id="sae-ae072f489756332a398884c6"></a>

## layer_10_width_16k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-ae072f489756332a398884c6`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_10_width_16k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.10.attn.hook_z` |
| Layer | 10 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_10_width_16k_l0_big`

---

<a id="sae-ec82dfc8ca6201015a17363b"></a>

## layer_10_width_16k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-ec82dfc8ca6201015a17363b`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out_all/layer_10_width_16k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.10.hook_mlp_out` |
| Layer | 10 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp-all` / `layer_10_width_16k_l0_big`

---

<a id="sae-55f3d6b3fa711b1e1085e6d3"></a>

## layer_10_width_16k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-55f3d6b3fa711b1e1085e6d3`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_10_width_16k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.10.hook_resid_post` |
| Layer | 10 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_10_width_16k_l0_big`

---

<a id="sae-216217a616b9c2b0ca858c43"></a>

## layer_10_width_16k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-216217a616b9c2b0ca858c43`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_10_width_16k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.10.attn.hook_z` |
| Layer | 10 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_10_width_16k_l0_small`

---

<a id="sae-7a8548b72e78924fa2da033c"></a>

## layer_10_width_16k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-7a8548b72e78924fa2da033c`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out_all/layer_10_width_16k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.10.hook_mlp_out` |
| Layer | 10 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp-all` / `layer_10_width_16k_l0_small`

---

<a id="sae-b2fe13240695b3b6b137a772"></a>

## layer_10_width_16k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-b2fe13240695b3b6b137a772`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_10_width_16k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.10.hook_resid_post` |
| Layer | 10 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_10_width_16k_l0_small`

---

<a id="sae-2c8a12e556add4d4a07e9f25"></a>

## layer_10_width_262k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-2c8a12e556add4d4a07e9f25`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_10_width_262k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.10.attn.hook_z` |
| Layer | 10 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_10_width_262k_l0_big`

---

<a id="sae-bf63cd42a534dec6c7b90095"></a>

## layer_10_width_262k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-bf63cd42a534dec6c7b90095`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out_all/layer_10_width_262k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.10.hook_mlp_out` |
| Layer | 10 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp-all` / `layer_10_width_262k_l0_big`

---

<a id="sae-d4ea5b3a38078765964c0a3e"></a>

## layer_10_width_262k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-d4ea5b3a38078765964c0a3e`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_10_width_262k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.10.hook_resid_post` |
| Layer | 10 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_10_width_262k_l0_big`

---

<a id="sae-446114e2fde4047113bd8657"></a>

## layer_10_width_262k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-446114e2fde4047113bd8657`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_10_width_262k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.10.attn.hook_z` |
| Layer | 10 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_10_width_262k_l0_small`

---

<a id="sae-58e973930cc3c4fd70b9efa6"></a>

## layer_10_width_262k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-58e973930cc3c4fd70b9efa6`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out_all/layer_10_width_262k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.10.hook_mlp_out` |
| Layer | 10 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp-all` / `layer_10_width_262k_l0_small`

---

<a id="sae-d70cb05f5e02cff9afe480ae"></a>

## layer_10_width_262k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-d70cb05f5e02cff9afe480ae`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_10_width_262k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.10.hook_resid_post` |
| Layer | 10 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_10_width_262k_l0_small`

---

<a id="sae-ce6911671f3ac5f29c2bd166"></a>

## layer_11_width_16k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-ce6911671f3ac5f29c2bd166`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_11_width_16k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.11.attn.hook_z` |
| Layer | 11 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_11_width_16k_l0_big`

---

<a id="sae-66b2283c9bf5dade9e8d204b"></a>

## layer_11_width_16k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-66b2283c9bf5dade9e8d204b`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out_all/layer_11_width_16k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.11.hook_mlp_out` |
| Layer | 11 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp-all` / `layer_11_width_16k_l0_big`

---

<a id="sae-945cfddb78bfbf738c1a4ce8"></a>

## layer_11_width_16k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-945cfddb78bfbf738c1a4ce8`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_11_width_16k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.11.hook_resid_post` |
| Layer | 11 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_11_width_16k_l0_big`

---

<a id="sae-3486c397678917fcf04a1ae5"></a>

## layer_11_width_16k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-3486c397678917fcf04a1ae5`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_11_width_16k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.11.attn.hook_z` |
| Layer | 11 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_11_width_16k_l0_small`

---

<a id="sae-b5b2d87cd4cbe8c5a5b4854d"></a>

## layer_11_width_16k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-b5b2d87cd4cbe8c5a5b4854d`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out_all/layer_11_width_16k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.11.hook_mlp_out` |
| Layer | 11 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp-all` / `layer_11_width_16k_l0_small`

---

<a id="sae-105988f321942d5d7e966910"></a>

## layer_11_width_16k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-105988f321942d5d7e966910`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_11_width_16k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.11.hook_resid_post` |
| Layer | 11 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_11_width_16k_l0_small`

---

<a id="sae-11318f9ce29ff32c57ed26b4"></a>

## layer_11_width_262k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-11318f9ce29ff32c57ed26b4`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_11_width_262k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.11.attn.hook_z` |
| Layer | 11 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_11_width_262k_l0_big`

---

<a id="sae-42ead1cb4a4f1916174e37cb"></a>

## layer_11_width_262k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-42ead1cb4a4f1916174e37cb`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out_all/layer_11_width_262k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.11.hook_mlp_out` |
| Layer | 11 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp-all` / `layer_11_width_262k_l0_big`

---

<a id="sae-57ebf8fbf03b34c86a651413"></a>

## layer_11_width_262k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-57ebf8fbf03b34c86a651413`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_11_width_262k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.11.hook_resid_post` |
| Layer | 11 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_11_width_262k_l0_big`

---

<a id="sae-2d2b27df6b1b7c50b0cdccec"></a>

## layer_11_width_262k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-2d2b27df6b1b7c50b0cdccec`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_11_width_262k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.11.attn.hook_z` |
| Layer | 11 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_11_width_262k_l0_small`

---

<a id="sae-ded33ac0308b90a321aab659"></a>

## layer_11_width_262k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-ded33ac0308b90a321aab659`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out_all/layer_11_width_262k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.11.hook_mlp_out` |
| Layer | 11 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp-all` / `layer_11_width_262k_l0_small`

---

<a id="sae-b90704c70d6bc5a4b8b380fd"></a>

## layer_11_width_262k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-b90704c70d6bc5a4b8b380fd`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_11_width_262k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.11.hook_resid_post` |
| Layer | 11 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_11_width_262k_l0_small`

---

<a id="sae-b47e90319ec597bef6e92f46"></a>

## layer_12_width_16k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-b47e90319ec597bef6e92f46`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_12_width_16k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.12.attn.hook_z` |
| Layer | 12 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_12_width_16k_l0_big`

---

<a id="sae-93513cbd83d0bb5eb05fec9e"></a>

## layer_12_width_16k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-93513cbd83d0bb5eb05fec9e`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out_all/layer_12_width_16k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.12.hook_mlp_out` |
| Layer | 12 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp-all` / `layer_12_width_16k_l0_big`

---

<a id="sae-7bd9d6fd85338a907b9918a0"></a>

## layer_12_width_16k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-7bd9d6fd85338a907b9918a0`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_12_width_16k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.12.hook_resid_post` |
| Layer | 12 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_12_width_16k_l0_big`

---

<a id="sae-280fe6936cde35b4707de00a"></a>

## layer_12_width_16k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-280fe6936cde35b4707de00a`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_12_width_16k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.12.attn.hook_z` |
| Layer | 12 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_12_width_16k_l0_small`

---

<a id="sae-e4af72b0d35c1a689cd59123"></a>

## layer_12_width_16k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-e4af72b0d35c1a689cd59123`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out_all/layer_12_width_16k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.12.hook_mlp_out` |
| Layer | 12 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp-all` / `layer_12_width_16k_l0_small`

---

<a id="sae-77c404f8159f22f88f73ffaa"></a>

## layer_12_width_16k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-77c404f8159f22f88f73ffaa`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_12_width_16k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.12.hook_resid_post` |
| Layer | 12 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_12_width_16k_l0_small`

---

## Metadata sources

- [Pinned published listing 1](https://github.com/decoderesearch/SAELens/blob/30c4502466785dd7809a307f7b705df187978aa3/sae_lens/pretrained_saes.yaml)
