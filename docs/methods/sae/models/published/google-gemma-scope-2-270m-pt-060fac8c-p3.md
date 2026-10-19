# google/gemma-scope-2-270m-pt

[Model hub](../README.md) · [All checkpoint repositories](README.md)

Published SAE dictionaries for **google/gemma-3-270m**. Page 3 of 7.

[Author checkpoint repository](https://huggingface.co/google/gemma-scope-2-270m-pt)

Select a dictionary below, download its author weights, and preserve its source model, hook and input conventions when converting to the native artifact format.

Pages: [1](google-gemma-scope-2-270m-pt-060fac8c-p1.md) · [2](google-gemma-scope-2-270m-pt-060fac8c-p2.md) · [3](google-gemma-scope-2-270m-pt-060fac8c-p3.md) · [4](google-gemma-scope-2-270m-pt-060fac8c-p4.md) · [5](google-gemma-scope-2-270m-pt-060fac8c-p5.md) · [6](google-gemma-scope-2-270m-pt-060fac8c-p6.md) · [7](google-gemma-scope-2-270m-pt-060fac8c-p7.md)

<a id="sae-b450ca470d8eed2109235186"></a>

## layer_5_width_65k_l0_small on google/gemma-3-270m

**Model ID:** `sae-b450ca470d8eed2109235186`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-270m-pt/tree/main/attn_out/layer_5_width_65k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-270m` |
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

**Published release names:** `gemma-scope-2-270m-pt-att` / `layer_5_width_65k_l0_small`

---

<a id="sae-94f2bad9be452692126dc198"></a>

## layer_5_width_65k_l0_small on google/gemma-3-270m

**Model ID:** `sae-94f2bad9be452692126dc198`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-270m-pt/tree/main/mlp_out/layer_5_width_65k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-270m` |
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

**Published release names:** `gemma-scope-2-270m-pt-mlp` / `layer_5_width_65k_l0_small`

---

<a id="sae-1a895d0095ce8cc6ed0b507a"></a>

## layer_5_width_65k_l0_small on google/gemma-3-270m

**Model ID:** `sae-1a895d0095ce8cc6ed0b507a`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-270m-pt/tree/main/resid_post/layer_5_width_65k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-270m` |
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

**Published release names:** `gemma-scope-2-270m-pt-res` / `layer_5_width_65k_l0_small`

---

<a id="sae-459a623151242e800ac2a4d9"></a>

## layer_6_width_16k_l0_big on google/gemma-3-270m

**Model ID:** `sae-459a623151242e800ac2a4d9`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-270m-pt/tree/main/attn_out_all/layer_6_width_16k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-270m` |
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

**Published release names:** `gemma-scope-2-270m-pt-att-all` / `layer_6_width_16k_l0_big`

---

<a id="sae-fdc83eeb6551094c0465ca79"></a>

## layer_6_width_16k_l0_big on google/gemma-3-270m

**Model ID:** `sae-fdc83eeb6551094c0465ca79`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-270m-pt/tree/main/mlp_out_all/layer_6_width_16k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-270m` |
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

**Published release names:** `gemma-scope-2-270m-pt-mlp-all` / `layer_6_width_16k_l0_big`

---

<a id="sae-21f88b2bbfbd4902697db3c4"></a>

## layer_6_width_16k_l0_big on google/gemma-3-270m

**Model ID:** `sae-21f88b2bbfbd4902697db3c4`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-270m-pt/tree/main/resid_post_all/layer_6_width_16k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-270m` |
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

**Published release names:** `gemma-scope-2-270m-pt-res-all` / `layer_6_width_16k_l0_big`

---

<a id="sae-7092f8a6cc5eef666c1f5910"></a>

## layer_6_width_16k_l0_small on google/gemma-3-270m

**Model ID:** `sae-7092f8a6cc5eef666c1f5910`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-270m-pt/tree/main/attn_out_all/layer_6_width_16k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-270m` |
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

**Published release names:** `gemma-scope-2-270m-pt-att-all` / `layer_6_width_16k_l0_small`

---

<a id="sae-a40b5dfa9a47182453b49e8f"></a>

## layer_6_width_16k_l0_small on google/gemma-3-270m

**Model ID:** `sae-a40b5dfa9a47182453b49e8f`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-270m-pt/tree/main/mlp_out_all/layer_6_width_16k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-270m` |
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

**Published release names:** `gemma-scope-2-270m-pt-mlp-all` / `layer_6_width_16k_l0_small`

---

<a id="sae-a6500f4a1027e427bcbff719"></a>

## layer_6_width_16k_l0_small on google/gemma-3-270m

**Model ID:** `sae-a6500f4a1027e427bcbff719`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-270m-pt/tree/main/resid_post_all/layer_6_width_16k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-270m` |
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

**Published release names:** `gemma-scope-2-270m-pt-res-all` / `layer_6_width_16k_l0_small`

---

<a id="sae-2d4fef5936189bb0a9ccd81a"></a>

## layer_6_width_262k_l0_big on google/gemma-3-270m

**Model ID:** `sae-2d4fef5936189bb0a9ccd81a`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-270m-pt/tree/main/attn_out_all/layer_6_width_262k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-270m` |
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

**Published release names:** `gemma-scope-2-270m-pt-att-all` / `layer_6_width_262k_l0_big`

---

<a id="sae-5f51c8396b51228d3b88cced"></a>

## layer_6_width_262k_l0_big on google/gemma-3-270m

**Model ID:** `sae-5f51c8396b51228d3b88cced`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-270m-pt/tree/main/mlp_out_all/layer_6_width_262k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-270m` |
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

**Published release names:** `gemma-scope-2-270m-pt-mlp-all` / `layer_6_width_262k_l0_big`

---

<a id="sae-85cd8bfeb480bed00b477d1e"></a>

## layer_6_width_262k_l0_big on google/gemma-3-270m

**Model ID:** `sae-85cd8bfeb480bed00b477d1e`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-270m-pt/tree/main/resid_post_all/layer_6_width_262k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-270m` |
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

**Published release names:** `gemma-scope-2-270m-pt-res-all` / `layer_6_width_262k_l0_big`

---

<a id="sae-edcd48ae1e58c5e9cfbda137"></a>

## layer_6_width_262k_l0_small on google/gemma-3-270m

**Model ID:** `sae-edcd48ae1e58c5e9cfbda137`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-270m-pt/tree/main/attn_out_all/layer_6_width_262k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-270m` |
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

**Published release names:** `gemma-scope-2-270m-pt-att-all` / `layer_6_width_262k_l0_small`

---

<a id="sae-56ef6b21ae56b136802c86ad"></a>

## layer_6_width_262k_l0_small on google/gemma-3-270m

**Model ID:** `sae-56ef6b21ae56b136802c86ad`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-270m-pt/tree/main/mlp_out_all/layer_6_width_262k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-270m` |
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

**Published release names:** `gemma-scope-2-270m-pt-mlp-all` / `layer_6_width_262k_l0_small`

---

<a id="sae-174d8a0e22b754c2d424169f"></a>

## layer_6_width_262k_l0_small on google/gemma-3-270m

**Model ID:** `sae-174d8a0e22b754c2d424169f`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-270m-pt/tree/main/resid_post_all/layer_6_width_262k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-270m` |
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

**Published release names:** `gemma-scope-2-270m-pt-res-all` / `layer_6_width_262k_l0_small`

---

<a id="sae-1a390a9fc53b728b700691d7"></a>

## layer_7_width_16k_l0_big on google/gemma-3-270m

**Model ID:** `sae-1a390a9fc53b728b700691d7`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-270m-pt/tree/main/attn_out_all/layer_7_width_16k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-270m` |
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

**Published release names:** `gemma-scope-2-270m-pt-att-all` / `layer_7_width_16k_l0_big`

---

<a id="sae-c7189ae679b8072b7a9591b1"></a>

## layer_7_width_16k_l0_big on google/gemma-3-270m

**Model ID:** `sae-c7189ae679b8072b7a9591b1`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-270m-pt/tree/main/mlp_out_all/layer_7_width_16k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-270m` |
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

**Published release names:** `gemma-scope-2-270m-pt-mlp-all` / `layer_7_width_16k_l0_big`

---

<a id="sae-17323e4d01dcf504c068aa17"></a>

## layer_7_width_16k_l0_big on google/gemma-3-270m

**Model ID:** `sae-17323e4d01dcf504c068aa17`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-270m-pt/tree/main/resid_post_all/layer_7_width_16k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-270m` |
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

**Published release names:** `gemma-scope-2-270m-pt-res-all` / `layer_7_width_16k_l0_big`

---

<a id="sae-e106192a3b7c92413e82c339"></a>

## layer_7_width_16k_l0_small on google/gemma-3-270m

**Model ID:** `sae-e106192a3b7c92413e82c339`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-270m-pt/tree/main/attn_out_all/layer_7_width_16k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-270m` |
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

**Published release names:** `gemma-scope-2-270m-pt-att-all` / `layer_7_width_16k_l0_small`

---

<a id="sae-3b7740b3ccaab54acf61d29a"></a>

## layer_7_width_16k_l0_small on google/gemma-3-270m

**Model ID:** `sae-3b7740b3ccaab54acf61d29a`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-270m-pt/tree/main/mlp_out_all/layer_7_width_16k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-270m` |
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

**Published release names:** `gemma-scope-2-270m-pt-mlp-all` / `layer_7_width_16k_l0_small`

---

<a id="sae-ebc5d9883c872062045000c2"></a>

## layer_7_width_16k_l0_small on google/gemma-3-270m

**Model ID:** `sae-ebc5d9883c872062045000c2`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-270m-pt/tree/main/resid_post_all/layer_7_width_16k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-270m` |
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

**Published release names:** `gemma-scope-2-270m-pt-res-all` / `layer_7_width_16k_l0_small`

---

<a id="sae-8192841a8cffb8534cbbd6a9"></a>

## layer_7_width_262k_l0_big on google/gemma-3-270m

**Model ID:** `sae-8192841a8cffb8534cbbd6a9`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-270m-pt/tree/main/attn_out_all/layer_7_width_262k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-270m` |
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

**Published release names:** `gemma-scope-2-270m-pt-att-all` / `layer_7_width_262k_l0_big`

---

<a id="sae-f963a0fafba0dbcbc4652c1a"></a>

## layer_7_width_262k_l0_big on google/gemma-3-270m

**Model ID:** `sae-f963a0fafba0dbcbc4652c1a`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-270m-pt/tree/main/mlp_out_all/layer_7_width_262k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-270m` |
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

**Published release names:** `gemma-scope-2-270m-pt-mlp-all` / `layer_7_width_262k_l0_big`

---

<a id="sae-647ab9a1521bc6c0f946ad30"></a>

## layer_7_width_262k_l0_big on google/gemma-3-270m

**Model ID:** `sae-647ab9a1521bc6c0f946ad30`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-270m-pt/tree/main/resid_post_all/layer_7_width_262k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-270m` |
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

**Published release names:** `gemma-scope-2-270m-pt-res-all` / `layer_7_width_262k_l0_big`

---

<a id="sae-89a034dd9047e0dcf251d824"></a>

## layer_7_width_262k_l0_small on google/gemma-3-270m

**Model ID:** `sae-89a034dd9047e0dcf251d824`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-270m-pt/tree/main/attn_out_all/layer_7_width_262k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-270m` |
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

**Published release names:** `gemma-scope-2-270m-pt-att-all` / `layer_7_width_262k_l0_small`

---

<a id="sae-6999a4f73067683e4ce40e7a"></a>

## layer_7_width_262k_l0_small on google/gemma-3-270m

**Model ID:** `sae-6999a4f73067683e4ce40e7a`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-270m-pt/tree/main/mlp_out_all/layer_7_width_262k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-270m` |
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

**Published release names:** `gemma-scope-2-270m-pt-mlp-all` / `layer_7_width_262k_l0_small`

---

<a id="sae-f6cfc328fd4936001b34656b"></a>

## layer_7_width_262k_l0_small on google/gemma-3-270m

**Model ID:** `sae-f6cfc328fd4936001b34656b`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-270m-pt/tree/main/resid_post_all/layer_7_width_262k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-270m` |
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

**Published release names:** `gemma-scope-2-270m-pt-res-all` / `layer_7_width_262k_l0_small`

---

<a id="sae-91ee86f392b096778c357eca"></a>

## layer_8_width_16k_l0_big on google/gemma-3-270m

**Model ID:** `sae-91ee86f392b096778c357eca`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-270m-pt/tree/main/attn_out_all/layer_8_width_16k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-270m` |
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

**Published release names:** `gemma-scope-2-270m-pt-att-all` / `layer_8_width_16k_l0_big`

---

<a id="sae-0fd3e0d52b407df2e90d332d"></a>

## layer_8_width_16k_l0_big on google/gemma-3-270m

**Model ID:** `sae-0fd3e0d52b407df2e90d332d`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-270m-pt/tree/main/mlp_out_all/layer_8_width_16k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-270m` |
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

**Published release names:** `gemma-scope-2-270m-pt-mlp-all` / `layer_8_width_16k_l0_big`

---

<a id="sae-f567df02c854e8177120b440"></a>

## layer_8_width_16k_l0_big on google/gemma-3-270m

**Model ID:** `sae-f567df02c854e8177120b440`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-270m-pt/tree/main/resid_post_all/layer_8_width_16k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-270m` |
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

**Published release names:** `gemma-scope-2-270m-pt-res-all` / `layer_8_width_16k_l0_big`

---

<a id="sae-69f05b7e499ed569b57f37c4"></a>

## layer_8_width_16k_l0_small on google/gemma-3-270m

**Model ID:** `sae-69f05b7e499ed569b57f37c4`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-270m-pt/tree/main/attn_out_all/layer_8_width_16k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-270m` |
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

**Published release names:** `gemma-scope-2-270m-pt-att-all` / `layer_8_width_16k_l0_small`

---

<a id="sae-3cece3dc957b2fb9da86adf0"></a>

## layer_8_width_16k_l0_small on google/gemma-3-270m

**Model ID:** `sae-3cece3dc957b2fb9da86adf0`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-270m-pt/tree/main/mlp_out_all/layer_8_width_16k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-270m` |
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

**Published release names:** `gemma-scope-2-270m-pt-mlp-all` / `layer_8_width_16k_l0_small`

---

<a id="sae-e1d2fdf58599646b4d7f3820"></a>

## layer_8_width_16k_l0_small on google/gemma-3-270m

**Model ID:** `sae-e1d2fdf58599646b4d7f3820`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-270m-pt/tree/main/resid_post_all/layer_8_width_16k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-270m` |
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

**Published release names:** `gemma-scope-2-270m-pt-res-all` / `layer_8_width_16k_l0_small`

---

<a id="sae-823bae1097f4f9a6e2e26813"></a>

## layer_8_width_262k_l0_big on google/gemma-3-270m

**Model ID:** `sae-823bae1097f4f9a6e2e26813`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-270m-pt/tree/main/attn_out_all/layer_8_width_262k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-270m` |
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

**Published release names:** `gemma-scope-2-270m-pt-att-all` / `layer_8_width_262k_l0_big`

---

<a id="sae-11ef96082c83da0187c1f128"></a>

## layer_8_width_262k_l0_big on google/gemma-3-270m

**Model ID:** `sae-11ef96082c83da0187c1f128`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-270m-pt/tree/main/mlp_out_all/layer_8_width_262k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-270m` |
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

**Published release names:** `gemma-scope-2-270m-pt-mlp-all` / `layer_8_width_262k_l0_big`

---

<a id="sae-6c109be294c21342c341b6fb"></a>

## layer_8_width_262k_l0_big on google/gemma-3-270m

**Model ID:** `sae-6c109be294c21342c341b6fb`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-270m-pt/tree/main/resid_post_all/layer_8_width_262k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-270m` |
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

**Published release names:** `gemma-scope-2-270m-pt-res-all` / `layer_8_width_262k_l0_big`

---

<a id="sae-a423d905aa149e146b3ae704"></a>

## layer_8_width_262k_l0_small on google/gemma-3-270m

**Model ID:** `sae-a423d905aa149e146b3ae704`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-270m-pt/tree/main/attn_out_all/layer_8_width_262k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-270m` |
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

**Published release names:** `gemma-scope-2-270m-pt-att-all` / `layer_8_width_262k_l0_small`

---

<a id="sae-286ecae4596a336e210e108d"></a>

## layer_8_width_262k_l0_small on google/gemma-3-270m

**Model ID:** `sae-286ecae4596a336e210e108d`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-270m-pt/tree/main/mlp_out_all/layer_8_width_262k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-270m` |
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

**Published release names:** `gemma-scope-2-270m-pt-mlp-all` / `layer_8_width_262k_l0_small`

---

<a id="sae-24b68d96b1b1ce00ce60b6c4"></a>

## layer_8_width_262k_l0_small on google/gemma-3-270m

**Model ID:** `sae-24b68d96b1b1ce00ce60b6c4`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-270m-pt/tree/main/resid_post_all/layer_8_width_262k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-270m` |
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

**Published release names:** `gemma-scope-2-270m-pt-res-all` / `layer_8_width_262k_l0_small`

---

<a id="sae-079575463c049ef53c31af4e"></a>

## layer_9_width_16k_l0_big on google/gemma-3-270m

**Model ID:** `sae-079575463c049ef53c31af4e`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-270m-pt/tree/main/attn_out/layer_9_width_16k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-270m` |
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

**Published release names:** `gemma-scope-2-270m-pt-att` / `layer_9_width_16k_l0_big`

---

<a id="sae-4fc69ac6cdf6b3730b070d1d"></a>

## layer_9_width_16k_l0_big on google/gemma-3-270m

**Model ID:** `sae-4fc69ac6cdf6b3730b070d1d`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-270m-pt/tree/main/attn_out_all/layer_9_width_16k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-270m` |
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

**Published release names:** `gemma-scope-2-270m-pt-att-all` / `layer_9_width_16k_l0_big`

---

<a id="sae-1057e1038b8f34cea485ac03"></a>

## layer_9_width_16k_l0_big on google/gemma-3-270m

**Model ID:** `sae-1057e1038b8f34cea485ac03`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-270m-pt/tree/main/mlp_out/layer_9_width_16k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-270m` |
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

**Published release names:** `gemma-scope-2-270m-pt-mlp` / `layer_9_width_16k_l0_big`

---

<a id="sae-9e461f37b529a1480e03a5f6"></a>

## layer_9_width_16k_l0_big on google/gemma-3-270m

**Model ID:** `sae-9e461f37b529a1480e03a5f6`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-270m-pt/tree/main/mlp_out_all/layer_9_width_16k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-270m` |
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

**Published release names:** `gemma-scope-2-270m-pt-mlp-all` / `layer_9_width_16k_l0_big`

---

<a id="sae-b436b33ab93b327d3879e23b"></a>

## layer_9_width_16k_l0_big on google/gemma-3-270m

**Model ID:** `sae-b436b33ab93b327d3879e23b`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-270m-pt/tree/main/resid_post/layer_9_width_16k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-270m` |
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

**Published release names:** `gemma-scope-2-270m-pt-res` / `layer_9_width_16k_l0_big`

---

<a id="sae-46e3060c3d80ff2e3042fd90"></a>

## layer_9_width_16k_l0_big on google/gemma-3-270m

**Model ID:** `sae-46e3060c3d80ff2e3042fd90`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-270m-pt/tree/main/resid_post_all/layer_9_width_16k_l0_big)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-270m` |
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

**Published release names:** `gemma-scope-2-270m-pt-res-all` / `layer_9_width_16k_l0_big`

---

<a id="sae-38a9ef338968c56b201c1398"></a>

## layer_9_width_16k_l0_medium on google/gemma-3-270m

**Model ID:** `sae-38a9ef338968c56b201c1398`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-270m-pt/tree/main/attn_out/layer_9_width_16k_l0_medium)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-270m` |
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

**Published release names:** `gemma-scope-2-270m-pt-att` / `layer_9_width_16k_l0_medium`

---

<a id="sae-914c9bb770a5b476d35892f5"></a>

## layer_9_width_16k_l0_medium on google/gemma-3-270m

**Model ID:** `sae-914c9bb770a5b476d35892f5`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-270m-pt/tree/main/mlp_out/layer_9_width_16k_l0_medium)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-270m` |
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

**Published release names:** `gemma-scope-2-270m-pt-mlp` / `layer_9_width_16k_l0_medium`

---

<a id="sae-76444d6193d62a1e7f340762"></a>

## layer_9_width_16k_l0_medium on google/gemma-3-270m

**Model ID:** `sae-76444d6193d62a1e7f340762`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-270m-pt/tree/main/resid_post/layer_9_width_16k_l0_medium)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-270m` |
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

**Published release names:** `gemma-scope-2-270m-pt-res` / `layer_9_width_16k_l0_medium`

---

<a id="sae-4cded45508a986eba3ff6285"></a>

## layer_9_width_16k_l0_small on google/gemma-3-270m

**Model ID:** `sae-4cded45508a986eba3ff6285`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-270m-pt/tree/main/attn_out/layer_9_width_16k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-270m` |
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

**Published release names:** `gemma-scope-2-270m-pt-att` / `layer_9_width_16k_l0_small`

---

<a id="sae-383e357e8ce8e5c566529956"></a>

## layer_9_width_16k_l0_small on google/gemma-3-270m

**Model ID:** `sae-383e357e8ce8e5c566529956`

[Checkpoint files](https://huggingface.co/google/gemma-scope-2-270m-pt/tree/main/attn_out_all/layer_9_width_16k_l0_small)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `google/gemma-3-270m` |
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

**Published release names:** `gemma-scope-2-270m-pt-att-all` / `layer_9_width_16k_l0_small`

---

## Metadata sources

- [Pinned published listing 1](https://github.com/decoderesearch/SAELens/blob/30c4502466785dd7809a307f7b705df187978aa3/sae_lens/pretrained_saes.yaml)
