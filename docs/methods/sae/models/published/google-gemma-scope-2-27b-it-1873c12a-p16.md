# google/gemma-scope-2-27b-it

[Model hub](../README.md) · [All checkpoint repositories](README.md)

Published SAE dictionaries for **google/gemma-3-27b-it**. Page 16 of 18.

[Author checkpoint repository](https://huggingface.co/google/gemma-scope-2-27b-it)

Select a dictionary below, download its author weights, and preserve its source model, hook and input conventions when converting to the native artifact format.

Pages: [1](google-gemma-scope-2-27b-it-1873c12a-p1.md) · [2](google-gemma-scope-2-27b-it-1873c12a-p2.md) · [3](google-gemma-scope-2-27b-it-1873c12a-p3.md) · [4](google-gemma-scope-2-27b-it-1873c12a-p4.md) · [5](google-gemma-scope-2-27b-it-1873c12a-p5.md) · [6](google-gemma-scope-2-27b-it-1873c12a-p6.md) · [7](google-gemma-scope-2-27b-it-1873c12a-p7.md) · [8](google-gemma-scope-2-27b-it-1873c12a-p8.md) · [9](google-gemma-scope-2-27b-it-1873c12a-p9.md) · [10](google-gemma-scope-2-27b-it-1873c12a-p10.md) · [11](google-gemma-scope-2-27b-it-1873c12a-p11.md) · [12](google-gemma-scope-2-27b-it-1873c12a-p12.md) · [13](google-gemma-scope-2-27b-it-1873c12a-p13.md) · [14](google-gemma-scope-2-27b-it-1873c12a-p14.md) · [15](google-gemma-scope-2-27b-it-1873c12a-p15.md) · [16](google-gemma-scope-2-27b-it-1873c12a-p16.md) · [17](google-gemma-scope-2-27b-it-1873c12a-p17.md) · [18](google-gemma-scope-2-27b-it-1873c12a-p18.md)

<a id="sae-ac03a85d022988b7936caa1c"></a>

## layer_53_width_262k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-ac03a85d022988b7936caa1c`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out_all/layer_53_width_262k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.53.hook_mlp_out` |
| Layer | 53 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp-all` / `layer_53_width_262k_l0_big`

---

<a id="sae-7ddb681b4be90e9348bdbbe9"></a>

## layer_53_width_262k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-7ddb681b4be90e9348bdbbe9`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post/layer_53_width_262k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.53.hook_resid_post` |
| Layer | 53 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res` / `layer_53_width_262k_l0_big`

---

<a id="sae-7af3d98a0aac8e644fd10820"></a>

## layer_53_width_262k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-7af3d98a0aac8e644fd10820`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_53_width_262k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.53.hook_resid_post` |
| Layer | 53 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_53_width_262k_l0_big`

---

<a id="sae-b5e31cd346135d96bc889ce1"></a>

## layer_53_width_262k_l0_medium on google/gemma-3-27b-it

**Model ID:** `sae-b5e31cd346135d96bc889ce1`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out/layer_53_width_262k_l0_medium)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.53.attn.hook_z` |
| Layer | 53 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att` / `layer_53_width_262k_l0_medium`

---

<a id="sae-1e9a923341274689509b70d1"></a>

## layer_53_width_262k_l0_medium on google/gemma-3-27b-it

**Model ID:** `sae-1e9a923341274689509b70d1`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out/layer_53_width_262k_l0_medium)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.53.hook_mlp_out` |
| Layer | 53 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp` / `layer_53_width_262k_l0_medium`

---

<a id="sae-4c90a37827b246445d48af27"></a>

## layer_53_width_262k_l0_medium on google/gemma-3-27b-it

**Model ID:** `sae-4c90a37827b246445d48af27`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post/layer_53_width_262k_l0_medium)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.53.hook_resid_post` |
| Layer | 53 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res` / `layer_53_width_262k_l0_medium`

---

<a id="sae-7aa9b724ea381f8de91f7176"></a>

## layer_53_width_262k_l0_medium_seed_1 on google/gemma-3-27b-it

**Model ID:** `sae-7aa9b724ea381f8de91f7176`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post/layer_53_width_262k_l0_medium_seed_1)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.53.hook_resid_post` |
| Layer | 53 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res` / `layer_53_width_262k_l0_medium_seed_1`

---

<a id="sae-ebc55f94e882488102acb998"></a>

## layer_53_width_262k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-ebc55f94e882488102acb998`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out/layer_53_width_262k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.53.attn.hook_z` |
| Layer | 53 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att` / `layer_53_width_262k_l0_small`

---

<a id="sae-909826c3cc9ba7ff35f3b82c"></a>

## layer_53_width_262k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-909826c3cc9ba7ff35f3b82c`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_53_width_262k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.53.attn.hook_z` |
| Layer | 53 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_53_width_262k_l0_small`

---

<a id="sae-e4ad341fc864d0389172f1b4"></a>

## layer_53_width_262k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-e4ad341fc864d0389172f1b4`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out/layer_53_width_262k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.53.hook_mlp_out` |
| Layer | 53 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp` / `layer_53_width_262k_l0_small`

---

<a id="sae-3763505938c92a4c1c433129"></a>

## layer_53_width_262k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-3763505938c92a4c1c433129`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out_all/layer_53_width_262k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.53.hook_mlp_out` |
| Layer | 53 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp-all` / `layer_53_width_262k_l0_small`

---

<a id="sae-5634fc8d4f95c096c531ec35"></a>

## layer_53_width_262k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-5634fc8d4f95c096c531ec35`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post/layer_53_width_262k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.53.hook_resid_post` |
| Layer | 53 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res` / `layer_53_width_262k_l0_small`

---

<a id="sae-8f8e01fc88ead2c7c9f71b06"></a>

## layer_53_width_262k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-8f8e01fc88ead2c7c9f71b06`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_53_width_262k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.53.hook_resid_post` |
| Layer | 53 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_53_width_262k_l0_small`

---

<a id="sae-84e3aca7d3a8fac113244748"></a>

## layer_53_width_65k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-84e3aca7d3a8fac113244748`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out/layer_53_width_65k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.53.attn.hook_z` |
| Layer | 53 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att` / `layer_53_width_65k_l0_big`

---

<a id="sae-8cc4848f443a9649609a6b65"></a>

## layer_53_width_65k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-8cc4848f443a9649609a6b65`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out/layer_53_width_65k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.53.hook_mlp_out` |
| Layer | 53 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp` / `layer_53_width_65k_l0_big`

---

<a id="sae-080bece0724584ad2741bfa0"></a>

## layer_53_width_65k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-080bece0724584ad2741bfa0`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post/layer_53_width_65k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.53.hook_resid_post` |
| Layer | 53 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res` / `layer_53_width_65k_l0_big`

---

<a id="sae-76a8d78122a0ad9d1f6e8ca9"></a>

## layer_53_width_65k_l0_medium on google/gemma-3-27b-it

**Model ID:** `sae-76a8d78122a0ad9d1f6e8ca9`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out/layer_53_width_65k_l0_medium)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.53.attn.hook_z` |
| Layer | 53 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att` / `layer_53_width_65k_l0_medium`

---

<a id="sae-ce8230a672f220334620fd03"></a>

## layer_53_width_65k_l0_medium on google/gemma-3-27b-it

**Model ID:** `sae-ce8230a672f220334620fd03`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out/layer_53_width_65k_l0_medium)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.53.hook_mlp_out` |
| Layer | 53 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp` / `layer_53_width_65k_l0_medium`

---

<a id="sae-332c0b921ab4c84369b68cd6"></a>

## layer_53_width_65k_l0_medium on google/gemma-3-27b-it

**Model ID:** `sae-332c0b921ab4c84369b68cd6`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post/layer_53_width_65k_l0_medium)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.53.hook_resid_post` |
| Layer | 53 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res` / `layer_53_width_65k_l0_medium`

---

<a id="sae-e60eba75f26fc089a55a8177"></a>

## layer_53_width_65k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-e60eba75f26fc089a55a8177`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out/layer_53_width_65k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.53.attn.hook_z` |
| Layer | 53 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att` / `layer_53_width_65k_l0_small`

---

<a id="sae-4fc0653fedfde53124db41b1"></a>

## layer_53_width_65k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-4fc0653fedfde53124db41b1`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out/layer_53_width_65k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.53.hook_mlp_out` |
| Layer | 53 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp` / `layer_53_width_65k_l0_small`

---

<a id="sae-8e6731fc1570ebd2c0f06411"></a>

## layer_53_width_65k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-8e6731fc1570ebd2c0f06411`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post/layer_53_width_65k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.53.hook_resid_post` |
| Layer | 53 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res` / `layer_53_width_65k_l0_small`

---

<a id="sae-2bcb2e3de5300d7b6c7b1172"></a>

## layer_54_width_16k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-2bcb2e3de5300d7b6c7b1172`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_54_width_16k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.54.attn.hook_z` |
| Layer | 54 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_54_width_16k_l0_big`

---

<a id="sae-509419ee905ea6bed5f733b0"></a>

## layer_54_width_16k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-509419ee905ea6bed5f733b0`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out_all/layer_54_width_16k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.54.hook_mlp_out` |
| Layer | 54 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp-all` / `layer_54_width_16k_l0_big`

---

<a id="sae-fb263264fb6e91d5dbe7957f"></a>

## layer_54_width_16k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-fb263264fb6e91d5dbe7957f`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_54_width_16k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.54.hook_resid_post` |
| Layer | 54 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_54_width_16k_l0_big`

---

<a id="sae-6d19eb49c6e0e2c97d3a48a5"></a>

## layer_54_width_16k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-6d19eb49c6e0e2c97d3a48a5`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_54_width_16k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.54.attn.hook_z` |
| Layer | 54 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_54_width_16k_l0_small`

---

<a id="sae-366107178dc0d63e415eae51"></a>

## layer_54_width_16k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-366107178dc0d63e415eae51`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out_all/layer_54_width_16k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.54.hook_mlp_out` |
| Layer | 54 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp-all` / `layer_54_width_16k_l0_small`

---

<a id="sae-fa9bde09663b149099963604"></a>

## layer_54_width_16k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-fa9bde09663b149099963604`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_54_width_16k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.54.hook_resid_post` |
| Layer | 54 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_54_width_16k_l0_small`

---

<a id="sae-9c6c72993fc6f22c81923f71"></a>

## layer_54_width_262k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-9c6c72993fc6f22c81923f71`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_54_width_262k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.54.attn.hook_z` |
| Layer | 54 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_54_width_262k_l0_big`

---

<a id="sae-b125d3af5b6c58baf9c2b0ea"></a>

## layer_54_width_262k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-b125d3af5b6c58baf9c2b0ea`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out_all/layer_54_width_262k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.54.hook_mlp_out` |
| Layer | 54 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp-all` / `layer_54_width_262k_l0_big`

---

<a id="sae-1b562c3fb7c14a534d476fbb"></a>

## layer_54_width_262k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-1b562c3fb7c14a534d476fbb`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_54_width_262k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.54.hook_resid_post` |
| Layer | 54 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_54_width_262k_l0_big`

---

<a id="sae-a5f78aa90b3f51afd7d1b9b6"></a>

## layer_54_width_262k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-a5f78aa90b3f51afd7d1b9b6`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_54_width_262k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.54.attn.hook_z` |
| Layer | 54 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_54_width_262k_l0_small`

---

<a id="sae-211bc6cf966df6c264b51e85"></a>

## layer_54_width_262k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-211bc6cf966df6c264b51e85`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out_all/layer_54_width_262k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.54.hook_mlp_out` |
| Layer | 54 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp-all` / `layer_54_width_262k_l0_small`

---

<a id="sae-a70cd545b1dd815e01ea7fbd"></a>

## layer_54_width_262k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-a70cd545b1dd815e01ea7fbd`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_54_width_262k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.54.hook_resid_post` |
| Layer | 54 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_54_width_262k_l0_small`

---

<a id="sae-c8406d52230093a78e2de2f3"></a>

## layer_55_width_16k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-c8406d52230093a78e2de2f3`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_55_width_16k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.55.attn.hook_z` |
| Layer | 55 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_55_width_16k_l0_big`

---

<a id="sae-e40a72bf872024c36d2a8126"></a>

## layer_55_width_16k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-e40a72bf872024c36d2a8126`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out_all/layer_55_width_16k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.55.hook_mlp_out` |
| Layer | 55 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp-all` / `layer_55_width_16k_l0_big`

---

<a id="sae-2d0145f00a2ebf50749d98c0"></a>

## layer_55_width_16k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-2d0145f00a2ebf50749d98c0`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_55_width_16k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.55.hook_resid_post` |
| Layer | 55 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_55_width_16k_l0_big`

---

<a id="sae-92d33f55fe26849a469a39d9"></a>

## layer_55_width_16k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-92d33f55fe26849a469a39d9`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_55_width_16k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.55.attn.hook_z` |
| Layer | 55 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_55_width_16k_l0_small`

---

<a id="sae-a227fe38d6b3053a5722ced3"></a>

## layer_55_width_16k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-a227fe38d6b3053a5722ced3`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out_all/layer_55_width_16k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.55.hook_mlp_out` |
| Layer | 55 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp-all` / `layer_55_width_16k_l0_small`

---

<a id="sae-723447593b01d3478b398aca"></a>

## layer_55_width_16k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-723447593b01d3478b398aca`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_55_width_16k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.55.hook_resid_post` |
| Layer | 55 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_55_width_16k_l0_small`

---

<a id="sae-2f7c18219fd280e7b909dc75"></a>

## layer_55_width_262k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-2f7c18219fd280e7b909dc75`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_55_width_262k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.55.attn.hook_z` |
| Layer | 55 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_55_width_262k_l0_big`

---

<a id="sae-9c8f856bab24db3de373be1b"></a>

## layer_55_width_262k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-9c8f856bab24db3de373be1b`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out_all/layer_55_width_262k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.55.hook_mlp_out` |
| Layer | 55 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp-all` / `layer_55_width_262k_l0_big`

---

<a id="sae-6c4ee29f9c81860d4464fdb9"></a>

## layer_55_width_262k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-6c4ee29f9c81860d4464fdb9`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_55_width_262k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.55.hook_resid_post` |
| Layer | 55 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_55_width_262k_l0_big`

---

<a id="sae-0719c4055e6ffa02e0a3309a"></a>

## layer_55_width_262k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-0719c4055e6ffa02e0a3309a`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_55_width_262k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.55.attn.hook_z` |
| Layer | 55 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_55_width_262k_l0_small`

---

<a id="sae-8c85ebe6e082c1bab9342911"></a>

## layer_55_width_262k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-8c85ebe6e082c1bab9342911`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out_all/layer_55_width_262k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.55.hook_mlp_out` |
| Layer | 55 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp-all` / `layer_55_width_262k_l0_small`

---

<a id="sae-dae9d883fdaaa27eaae9d457"></a>

## layer_55_width_262k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-dae9d883fdaaa27eaae9d457`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_55_width_262k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.55.hook_resid_post` |
| Layer | 55 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_55_width_262k_l0_small`

---

<a id="sae-117aa17d239921e1d5703e70"></a>

## layer_56_width_16k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-117aa17d239921e1d5703e70`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_56_width_16k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.56.attn.hook_z` |
| Layer | 56 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_56_width_16k_l0_big`

---

<a id="sae-f447aabf94f17bca71ded599"></a>

## layer_56_width_16k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-f447aabf94f17bca71ded599`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/mlp_out_all/layer_56_width_16k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.56.hook_mlp_out` |
| Layer | 56 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-mlp-all` / `layer_56_width_16k_l0_big`

---

<a id="sae-bd54fb15a27dc352ac136b97"></a>

## layer_56_width_16k_l0_big on google/gemma-3-27b-it

**Model ID:** `sae-bd54fb15a27dc352ac136b97`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/resid_post_all/layer_56_width_16k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.56.hook_resid_post` |
| Layer | 56 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-res-all` / `layer_56_width_16k_l0_big`

---

<a id="sae-c3c2a5e6839f471b05d342ef"></a>

## layer_56_width_16k_l0_small on google/gemma-3-27b-it

**Model ID:** `sae-c3c2a5e6839f471b05d342ef`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-27b-it/tree/main/attn_out_all/layer_56_width_16k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-27b-it` |
| Method | [jumprelu](../../jumprelu.md) |
| Source hook / output | `blocks.56.attn.hook_z` |
| Layer | 56 |
| Activation width | Not specified |
| Dictionary features | Not specified |
| Checkpoint license | Not specified |
| Checkpoint revision | `Not specified` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"context_size": 1024, "prepend_bos": true, "apply_b_dec_to_input": false, "normalize_activations": "none"}`

**Published release names:** `gemma-scope-2-27b-it-att-all` / `layer_56_width_16k_l0_small`

---

## Metadata sources

- [Pinned published listing 1](https://github.com/decoderesearch/SAELens/blob/30c4502466785dd7809a307f7b705df187978aa3/sae_lens/pretrained_saes.yaml)
