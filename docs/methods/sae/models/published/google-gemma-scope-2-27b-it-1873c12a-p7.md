# google/gemma-scope-2-27b-it

[Model hub](../README.md) · [All checkpoint repositories](README.md)

Published SAE dictionaries for **google/gemma-3-27b-it**. Page 7 of 18.

[Author checkpoint repository](https://huggingface.co/google/gemma-scope-2-27b-it)

Select a dictionary below, download its author weights, and preserve its source model, hook and input conventions when converting to the native artifact format.

Pages: [1](google-gemma-scope-2-27b-it-1873c12a-p1.md) · [2](google-gemma-scope-2-27b-it-1873c12a-p2.md) · [3](google-gemma-scope-2-27b-it-1873c12a-p3.md) · [4](google-gemma-scope-2-27b-it-1873c12a-p4.md) · [5](google-gemma-scope-2-27b-it-1873c12a-p5.md) · [6](google-gemma-scope-2-27b-it-1873c12a-p6.md) · [7](google-gemma-scope-2-27b-it-1873c12a-p7.md) · [8](google-gemma-scope-2-27b-it-1873c12a-p8.md) · [9](google-gemma-scope-2-27b-it-1873c12a-p9.md) · [10](google-gemma-scope-2-27b-it-1873c12a-p10.md) · [11](google-gemma-scope-2-27b-it-1873c12a-p11.md) · [12](google-gemma-scope-2-27b-it-1873c12a-p12.md) · [13](google-gemma-scope-2-27b-it-1873c12a-p13.md) · [14](google-gemma-scope-2-27b-it-1873c12a-p14.md) · [15](google-gemma-scope-2-27b-it-1873c12a-p15.md) · [16](google-gemma-scope-2-27b-it-1873c12a-p16.md) · [17](google-gemma-scope-2-27b-it-1873c12a-p17.md) · [18](google-gemma-scope-2-27b-it-1873c12a-p18.md)

<a id="sae-0d8b3b3f676291a2b6799478"></a>

## layer_22_width_16k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-0d8b3b3f676291a2b6799478`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_22_width_16k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.22.hook_resid_post` |
| Layer | 22 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_22_width_16k_l0_small`

---

<a id="sae-077cc72f871adf0d5fbdd878"></a>

## layer_22_width_262k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-077cc72f871adf0d5fbdd878`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_22_width_262k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.22.attn.hook_z` |
| Layer | 22 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_22_width_262k_l0_big`

---

<a id="sae-6fbca81a132ee739ccfd9f2a"></a>

## layer_22_width_262k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-6fbca81a132ee739ccfd9f2a`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out_all/layer_22_width_262k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.22.hook_mlp_out` |
| Layer | 22 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp-all` / `layer_22_width_262k_l0_big`

---

<a id="sae-d30b8123fc827e1d8392200a"></a>

## layer_22_width_262k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-d30b8123fc827e1d8392200a`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_22_width_262k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.22.hook_resid_post` |
| Layer | 22 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_22_width_262k_l0_big`

---

<a id="sae-5aa5506672b34ee4ffc32064"></a>

## layer_22_width_262k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-5aa5506672b34ee4ffc32064`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_22_width_262k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.22.attn.hook_z` |
| Layer | 22 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_22_width_262k_l0_small`

---

<a id="sae-350d01fa08ba97fa6730c69c"></a>

## layer_22_width_262k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-350d01fa08ba97fa6730c69c`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out_all/layer_22_width_262k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.22.hook_mlp_out` |
| Layer | 22 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp-all` / `layer_22_width_262k_l0_small`

---

<a id="sae-2543064d909dc7db8d0a9021"></a>

## layer_22_width_262k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-2543064d909dc7db8d0a9021`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_22_width_262k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.22.hook_resid_post` |
| Layer | 22 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_22_width_262k_l0_small`

---

<a id="sae-cde508136cc3857b1b0d823a"></a>

## layer_23_width_16k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-cde508136cc3857b1b0d823a`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_23_width_16k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.23.attn.hook_z` |
| Layer | 23 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_23_width_16k_l0_big`

---

<a id="sae-0188aa56511933f4aa075da6"></a>

## layer_23_width_16k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-0188aa56511933f4aa075da6`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out_all/layer_23_width_16k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.23.hook_mlp_out` |
| Layer | 23 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp-all` / `layer_23_width_16k_l0_big`

---

<a id="sae-cea7cc0df3580e27a0c1547f"></a>

## layer_23_width_16k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-cea7cc0df3580e27a0c1547f`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_23_width_16k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.23.hook_resid_post` |
| Layer | 23 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_23_width_16k_l0_big`

---

<a id="sae-715db61dab075dab9b0391e5"></a>

## layer_23_width_16k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-715db61dab075dab9b0391e5`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_23_width_16k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.23.attn.hook_z` |
| Layer | 23 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_23_width_16k_l0_small`

---

<a id="sae-11243403c2e4535eb761312b"></a>

## layer_23_width_16k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-11243403c2e4535eb761312b`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out_all/layer_23_width_16k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.23.hook_mlp_out` |
| Layer | 23 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp-all` / `layer_23_width_16k_l0_small`

---

<a id="sae-5da0fa2a8b3077b417a43fce"></a>

## layer_23_width_16k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-5da0fa2a8b3077b417a43fce`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_23_width_16k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.23.hook_resid_post` |
| Layer | 23 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_23_width_16k_l0_small`

---

<a id="sae-72b48cfc8508875886ab1678"></a>

## layer_23_width_262k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-72b48cfc8508875886ab1678`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_23_width_262k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.23.attn.hook_z` |
| Layer | 23 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_23_width_262k_l0_big`

---

<a id="sae-92206f5b3304e092c537a9ad"></a>

## layer_23_width_262k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-92206f5b3304e092c537a9ad`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out_all/layer_23_width_262k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.23.hook_mlp_out` |
| Layer | 23 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp-all` / `layer_23_width_262k_l0_big`

---

<a id="sae-cfd005cc7f5d7f538d688ec2"></a>

## layer_23_width_262k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-cfd005cc7f5d7f538d688ec2`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_23_width_262k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.23.hook_resid_post` |
| Layer | 23 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_23_width_262k_l0_big`

---

<a id="sae-c1a27bf0e69b7a8722e13b42"></a>

## layer_23_width_262k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-c1a27bf0e69b7a8722e13b42`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_23_width_262k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.23.attn.hook_z` |
| Layer | 23 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_23_width_262k_l0_small`

---

<a id="sae-8564d5b56db26063bdbdc469"></a>

## layer_23_width_262k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-8564d5b56db26063bdbdc469`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out_all/layer_23_width_262k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.23.hook_mlp_out` |
| Layer | 23 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp-all` / `layer_23_width_262k_l0_small`

---

<a id="sae-31e9a6b9d50dcd203182255d"></a>

## layer_23_width_262k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-31e9a6b9d50dcd203182255d`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_23_width_262k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.23.hook_resid_post` |
| Layer | 23 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_23_width_262k_l0_small`

---

<a id="sae-427eca65df6eb51a7d9457e5"></a>

## layer_24_width_16k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-427eca65df6eb51a7d9457e5`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_24_width_16k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.24.attn.hook_z` |
| Layer | 24 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_24_width_16k_l0_big`

---

<a id="sae-d565279e0794f9125a6b2436"></a>

## layer_24_width_16k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-d565279e0794f9125a6b2436`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out_all/layer_24_width_16k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.24.hook_mlp_out` |
| Layer | 24 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp-all` / `layer_24_width_16k_l0_big`

---

<a id="sae-b5c332f1cd87ae9f4dea2d3c"></a>

## layer_24_width_16k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-b5c332f1cd87ae9f4dea2d3c`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_24_width_16k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.24.hook_resid_post` |
| Layer | 24 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_24_width_16k_l0_big`

---

<a id="sae-b5879a095fe4181ef2b67486"></a>

## layer_24_width_16k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-b5879a095fe4181ef2b67486`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_24_width_16k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.24.attn.hook_z` |
| Layer | 24 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_24_width_16k_l0_small`

---

<a id="sae-3cd9416f708413b971ade693"></a>

## layer_24_width_16k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-3cd9416f708413b971ade693`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out_all/layer_24_width_16k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.24.hook_mlp_out` |
| Layer | 24 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp-all` / `layer_24_width_16k_l0_small`

---

<a id="sae-bd147af55e83859080c67b53"></a>

## layer_24_width_16k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-bd147af55e83859080c67b53`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_24_width_16k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.24.hook_resid_post` |
| Layer | 24 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_24_width_16k_l0_small`

---

<a id="sae-22438ece53c44664d0f7cf95"></a>

## layer_24_width_262k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-22438ece53c44664d0f7cf95`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_24_width_262k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.24.attn.hook_z` |
| Layer | 24 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_24_width_262k_l0_big`

---

<a id="sae-949650730e576c011efd0a7e"></a>

## layer_24_width_262k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-949650730e576c011efd0a7e`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out_all/layer_24_width_262k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.24.hook_mlp_out` |
| Layer | 24 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp-all` / `layer_24_width_262k_l0_big`

---

<a id="sae-c91d770be6b9a614bffb2679"></a>

## layer_24_width_262k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-c91d770be6b9a614bffb2679`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_24_width_262k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.24.hook_resid_post` |
| Layer | 24 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_24_width_262k_l0_big`

---

<a id="sae-ab5577e77c5f9d2cfbc257f1"></a>

## layer_24_width_262k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-ab5577e77c5f9d2cfbc257f1`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_24_width_262k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.24.attn.hook_z` |
| Layer | 24 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_24_width_262k_l0_small`

---

<a id="sae-0e5ca75e23b1044742d19ab7"></a>

## layer_24_width_262k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-0e5ca75e23b1044742d19ab7`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out_all/layer_24_width_262k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.24.hook_mlp_out` |
| Layer | 24 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp-all` / `layer_24_width_262k_l0_small`

---

<a id="sae-3c12b63258a2d4cf1c0006d5"></a>

## layer_24_width_262k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-3c12b63258a2d4cf1c0006d5`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_24_width_262k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.24.hook_resid_post` |
| Layer | 24 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_24_width_262k_l0_small`

---

<a id="sae-1486faad84956939ace4b859"></a>

## layer_25_width_16k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-1486faad84956939ace4b859`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_25_width_16k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.25.attn.hook_z` |
| Layer | 25 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_25_width_16k_l0_big`

---

<a id="sae-aab14561eb3966328119f519"></a>

## layer_25_width_16k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-aab14561eb3966328119f519`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out_all/layer_25_width_16k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.25.hook_mlp_out` |
| Layer | 25 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp-all` / `layer_25_width_16k_l0_big`

---

<a id="sae-6afce0ad0c7098161e7a2c0c"></a>

## layer_25_width_16k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-6afce0ad0c7098161e7a2c0c`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_25_width_16k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.25.hook_resid_post` |
| Layer | 25 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_25_width_16k_l0_big`

---

<a id="sae-a7be95ed7ae3307805ea0fa1"></a>

## layer_25_width_16k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-a7be95ed7ae3307805ea0fa1`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_25_width_16k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.25.attn.hook_z` |
| Layer | 25 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_25_width_16k_l0_small`

---

<a id="sae-79f1240957f07b72a2ea6197"></a>

## layer_25_width_16k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-79f1240957f07b72a2ea6197`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out_all/layer_25_width_16k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.25.hook_mlp_out` |
| Layer | 25 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp-all` / `layer_25_width_16k_l0_small`

---

<a id="sae-b07663390f55b1d5a85d0e62"></a>

## layer_25_width_16k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-b07663390f55b1d5a85d0e62`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_25_width_16k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.25.hook_resid_post` |
| Layer | 25 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_25_width_16k_l0_small`

---

<a id="sae-00b135c8943da24fdd77126d"></a>

## layer_25_width_262k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-00b135c8943da24fdd77126d`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_25_width_262k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.25.attn.hook_z` |
| Layer | 25 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_25_width_262k_l0_big`

---

<a id="sae-7cde637c16ee24de71f9106a"></a>

## layer_25_width_262k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-7cde637c16ee24de71f9106a`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out_all/layer_25_width_262k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.25.hook_mlp_out` |
| Layer | 25 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp-all` / `layer_25_width_262k_l0_big`

---

<a id="sae-91aaf81453ef3a3508020616"></a>

## layer_25_width_262k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-91aaf81453ef3a3508020616`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_25_width_262k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.25.hook_resid_post` |
| Layer | 25 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_25_width_262k_l0_big`

---

<a id="sae-1ceba8704c9a4d27fc0a1c5b"></a>

## layer_25_width_262k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-1ceba8704c9a4d27fc0a1c5b`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_25_width_262k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.25.attn.hook_z` |
| Layer | 25 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_25_width_262k_l0_small`

---

<a id="sae-b7ed6bf8be76613d81c1679d"></a>

## layer_25_width_262k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-b7ed6bf8be76613d81c1679d`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out_all/layer_25_width_262k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.25.hook_mlp_out` |
| Layer | 25 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp-all` / `layer_25_width_262k_l0_small`

---

<a id="sae-39490caac3e4c94b3f189aca"></a>

## layer_25_width_262k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-39490caac3e4c94b3f189aca`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_25_width_262k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.25.hook_resid_post` |
| Layer | 25 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_25_width_262k_l0_small`

---

<a id="sae-cb7c101d9bcf2b9c52fa05a4"></a>

## layer_26_width_16k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-cb7c101d9bcf2b9c52fa05a4`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_26_width_16k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.26.attn.hook_z` |
| Layer | 26 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_26_width_16k_l0_big`

---

<a id="sae-3c7792ce2a0a03939c4313d8"></a>

## layer_26_width_16k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-3c7792ce2a0a03939c4313d8`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out_all/layer_26_width_16k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.26.hook_mlp_out` |
| Layer | 26 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp-all` / `layer_26_width_16k_l0_big`

---

<a id="sae-9d4a7f07281c6f903edbd1bf"></a>

## layer_26_width_16k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-9d4a7f07281c6f903edbd1bf`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_26_width_16k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.26.hook_resid_post` |
| Layer | 26 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_26_width_16k_l0_big`

---

<a id="sae-27e2e5b0676d2f7ddb15c20a"></a>

## layer_26_width_16k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-27e2e5b0676d2f7ddb15c20a`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_26_width_16k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.26.attn.hook_z` |
| Layer | 26 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_26_width_16k_l0_small`

---

<a id="sae-d72f26f7dc2804f51ccf9e9e"></a>

## layer_26_width_16k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-d72f26f7dc2804f51ccf9e9e`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out_all/layer_26_width_16k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.26.hook_mlp_out` |
| Layer | 26 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp-all` / `layer_26_width_16k_l0_small`

---

<a id="sae-bafdde731e03d4705274b1c2"></a>

## layer_26_width_16k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-bafdde731e03d4705274b1c2`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_26_width_16k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.26.hook_resid_post` |
| Layer | 26 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_26_width_16k_l0_small`

---

<a id="sae-8f1457abb574d452e49cb8b8"></a>

## layer_26_width_262k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-8f1457abb574d452e49cb8b8`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_26_width_262k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.26.attn.hook_z` |
| Layer | 26 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_26_width_262k_l0_big`

---

## Metadata sources

- [Pinned published listing 1](https://github.com/decoderesearch/SAELens/blob/30c4502466785dd7809a307f7b705df187978aa3/sae_lens/pretrained_saes.yaml)
