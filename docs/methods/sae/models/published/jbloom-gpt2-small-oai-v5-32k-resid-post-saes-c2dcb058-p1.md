# jbloom/GPT2-Small-OAI-v5-32k-resid-post-SAEs

[Model hub](../README.md) · [All checkpoint repositories](README.md)

Published SAE dictionaries for **gpt2-small**. Page 1 of 1.

[Author checkpoint repository](https://huggingface.co/jbloom/GPT2-Small-OAI-v5-32k-resid-post-SAEs)

Select a dictionary below, download its author weights, and preserve its source model, hook and input conventions when converting to the native artifact format.

Pages: [1](jbloom-gpt2-small-oai-v5-32k-resid-post-saes-c2dcb058-p1.md)

<a id="sae-6783018355728933dae6d812"></a>

## blocks.0.hook_resid_post on gpt2-small

**Model ID:** `sae-6783018355728933dae6d812`

[Download weights](https://huggingface.co/jbloom/GPT2-Small-OAI-v5-32k-resid-post-SAEs/resolve/21df74db7b9f690cd2403a20485cf75f46330d0d/v5_32k_layer_0.pt/sae_weights.safetensors)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `gpt2-small` |
| Method | [topk](../../topk.md) |
| Source hook / output | `blocks.0.hook_resid_post` |
| Layer | 0 |
| Activation width | 768 |
| Dictionary features | 32768 |
| Checkpoint license | mit |
| Checkpoint revision | `21df74db7b9f690cd2403a20485cf75f46330d0d` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"normalize_activations": "layer_norm", "context_size": 64, "prepend_bos": false, "apply_b_dec_to_input": true, "k": 32}`

**Weight SHA256:** `ebc8b6af7ebe5485809248f43df4bcdae0ddd59f28201412438cd5b43eb9db80`

[Checkpoint configuration](https://huggingface.co/jbloom/GPT2-Small-OAI-v5-32k-resid-post-SAEs/resolve/21df74db7b9f690cd2403a20485cf75f46330d0d/v5_32k_layer_0.pt/cfg.json)

**Load without fitting:**

```python
method = probe.sae.from_pretrained("sae-6783018355728933dae6d812")
result = method.run(inputs)
```

[Complete matching-backbone and inference example](../../loading.md).

**Published release names:** `gpt2-small-resid-post-v5-32k` / `blocks.0.hook_resid_post`

---

<a id="sae-9392fad18105516172bcfe0e"></a>

## blocks.1.hook_resid_post on gpt2-small

**Model ID:** `sae-9392fad18105516172bcfe0e`

[Download weights](https://huggingface.co/jbloom/GPT2-Small-OAI-v5-32k-resid-post-SAEs/resolve/21df74db7b9f690cd2403a20485cf75f46330d0d/v5_32k_layer_1.pt/sae_weights.safetensors)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `gpt2-small` |
| Method | [topk](../../topk.md) |
| Source hook / output | `blocks.1.hook_resid_post` |
| Layer | 1 |
| Activation width | 768 |
| Dictionary features | 32768 |
| Checkpoint license | mit |
| Checkpoint revision | `21df74db7b9f690cd2403a20485cf75f46330d0d` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"normalize_activations": "layer_norm", "context_size": 64, "prepend_bos": false, "apply_b_dec_to_input": true, "k": 32}`

**Weight SHA256:** `b3a1b0368a39fea67c71e063889f1b26de892bccbdb463f5db5ddd47fe1f8541`

[Checkpoint configuration](https://huggingface.co/jbloom/GPT2-Small-OAI-v5-32k-resid-post-SAEs/resolve/21df74db7b9f690cd2403a20485cf75f46330d0d/v5_32k_layer_1.pt/cfg.json)

**Published release names:** `gpt2-small-resid-post-v5-32k` / `blocks.1.hook_resid_post`

---

<a id="sae-115ac2afa07e162c56458be0"></a>

## blocks.2.hook_resid_post on gpt2-small

**Model ID:** `sae-115ac2afa07e162c56458be0`

[Download weights](https://huggingface.co/jbloom/GPT2-Small-OAI-v5-32k-resid-post-SAEs/resolve/21df74db7b9f690cd2403a20485cf75f46330d0d/v5_32k_layer_2.pt/sae_weights.safetensors)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `gpt2-small` |
| Method | [topk](../../topk.md) |
| Source hook / output | `blocks.2.hook_resid_post` |
| Layer | 2 |
| Activation width | 768 |
| Dictionary features | 32768 |
| Checkpoint license | mit |
| Checkpoint revision | `21df74db7b9f690cd2403a20485cf75f46330d0d` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"normalize_activations": "layer_norm", "context_size": 64, "prepend_bos": false, "apply_b_dec_to_input": true, "k": 32}`

**Weight SHA256:** `d7b245e1877fa01897c4ec452c743547cf305dcb817710ce1b67d3e82e988510`

[Checkpoint configuration](https://huggingface.co/jbloom/GPT2-Small-OAI-v5-32k-resid-post-SAEs/resolve/21df74db7b9f690cd2403a20485cf75f46330d0d/v5_32k_layer_2.pt/cfg.json)

**Published release names:** `gpt2-small-resid-post-v5-32k` / `blocks.2.hook_resid_post`

---

<a id="sae-0fe3ac581d627b1800af528b"></a>

## blocks.3.hook_resid_post on gpt2-small

**Model ID:** `sae-0fe3ac581d627b1800af528b`

[Download weights](https://huggingface.co/jbloom/GPT2-Small-OAI-v5-32k-resid-post-SAEs/resolve/21df74db7b9f690cd2403a20485cf75f46330d0d/v5_32k_layer_3.pt/sae_weights.safetensors)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `gpt2-small` |
| Method | [topk](../../topk.md) |
| Source hook / output | `blocks.3.hook_resid_post` |
| Layer | 3 |
| Activation width | 768 |
| Dictionary features | 32768 |
| Checkpoint license | mit |
| Checkpoint revision | `21df74db7b9f690cd2403a20485cf75f46330d0d` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"normalize_activations": "layer_norm", "context_size": 64, "prepend_bos": false, "apply_b_dec_to_input": true, "k": 32}`

**Weight SHA256:** `7693e9d88d8a5c34bd0519a3b04f4cb4020204df3bca87fa56c5079f5c84b057`

[Checkpoint configuration](https://huggingface.co/jbloom/GPT2-Small-OAI-v5-32k-resid-post-SAEs/resolve/21df74db7b9f690cd2403a20485cf75f46330d0d/v5_32k_layer_3.pt/cfg.json)

**Published release names:** `gpt2-small-resid-post-v5-32k` / `blocks.3.hook_resid_post`

---

<a id="sae-4d6ba19dcf4b964b8585f95d"></a>

## blocks.4.hook_resid_post on gpt2-small

**Model ID:** `sae-4d6ba19dcf4b964b8585f95d`

[Download weights](https://huggingface.co/jbloom/GPT2-Small-OAI-v5-32k-resid-post-SAEs/resolve/21df74db7b9f690cd2403a20485cf75f46330d0d/v5_32k_layer_4.pt/sae_weights.safetensors)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `gpt2-small` |
| Method | [topk](../../topk.md) |
| Source hook / output | `blocks.4.hook_resid_post` |
| Layer | 4 |
| Activation width | 768 |
| Dictionary features | 32768 |
| Checkpoint license | mit |
| Checkpoint revision | `21df74db7b9f690cd2403a20485cf75f46330d0d` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"normalize_activations": "layer_norm", "context_size": 64, "prepend_bos": false, "apply_b_dec_to_input": true, "k": 32}`

**Weight SHA256:** `621efab60c2e9180a95497ed9c2a8d5300508f992a2758473c65faa7c79b277c`

[Checkpoint configuration](https://huggingface.co/jbloom/GPT2-Small-OAI-v5-32k-resid-post-SAEs/resolve/21df74db7b9f690cd2403a20485cf75f46330d0d/v5_32k_layer_4.pt/cfg.json)

**Published release names:** `gpt2-small-resid-post-v5-32k` / `blocks.4.hook_resid_post`

---

<a id="sae-8ea818798102c6b1d69fa553"></a>

## blocks.5.hook_resid_post on gpt2-small

**Model ID:** `sae-8ea818798102c6b1d69fa553`

[Download weights](https://huggingface.co/jbloom/GPT2-Small-OAI-v5-32k-resid-post-SAEs/resolve/21df74db7b9f690cd2403a20485cf75f46330d0d/v5_32k_layer_5.pt/sae_weights.safetensors)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `gpt2-small` |
| Method | [topk](../../topk.md) |
| Source hook / output | `blocks.5.hook_resid_post` |
| Layer | 5 |
| Activation width | 768 |
| Dictionary features | 32768 |
| Checkpoint license | mit |
| Checkpoint revision | `21df74db7b9f690cd2403a20485cf75f46330d0d` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"normalize_activations": "layer_norm", "context_size": 64, "prepend_bos": false, "apply_b_dec_to_input": true, "k": 32}`

**Weight SHA256:** `08497251e859bef24af937862142af2b3cc3350e891fa2087bfa4d211fff8347`

[Checkpoint configuration](https://huggingface.co/jbloom/GPT2-Small-OAI-v5-32k-resid-post-SAEs/resolve/21df74db7b9f690cd2403a20485cf75f46330d0d/v5_32k_layer_5.pt/cfg.json)

**Published release names:** `gpt2-small-resid-post-v5-32k` / `blocks.5.hook_resid_post`

---

<a id="sae-73b5117230d7eda891666d36"></a>

## blocks.6.hook_resid_post on gpt2-small

**Model ID:** `sae-73b5117230d7eda891666d36`

[Download weights](https://huggingface.co/jbloom/GPT2-Small-OAI-v5-32k-resid-post-SAEs/resolve/21df74db7b9f690cd2403a20485cf75f46330d0d/v5_32k_layer_6.pt/sae_weights.safetensors)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `gpt2-small` |
| Method | [topk](../../topk.md) |
| Source hook / output | `blocks.6.hook_resid_post` |
| Layer | 6 |
| Activation width | 768 |
| Dictionary features | 32768 |
| Checkpoint license | mit |
| Checkpoint revision | `21df74db7b9f690cd2403a20485cf75f46330d0d` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"normalize_activations": "layer_norm", "context_size": 64, "prepend_bos": false, "apply_b_dec_to_input": true, "k": 32}`

**Weight SHA256:** `4b5145b14083285505618247e55c0303ea4065500289fa2be850399933a918e9`

[Checkpoint configuration](https://huggingface.co/jbloom/GPT2-Small-OAI-v5-32k-resid-post-SAEs/resolve/21df74db7b9f690cd2403a20485cf75f46330d0d/v5_32k_layer_6.pt/cfg.json)

**Published release names:** `gpt2-small-resid-post-v5-32k` / `blocks.6.hook_resid_post`

---

<a id="sae-6d433ebcbe57292d055cf959"></a>

## blocks.7.hook_resid_post on gpt2-small

**Model ID:** `sae-6d433ebcbe57292d055cf959`

[Download weights](https://huggingface.co/jbloom/GPT2-Small-OAI-v5-32k-resid-post-SAEs/resolve/21df74db7b9f690cd2403a20485cf75f46330d0d/v5_32k_layer_7.pt/sae_weights.safetensors)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `gpt2-small` |
| Method | [topk](../../topk.md) |
| Source hook / output | `blocks.7.hook_resid_post` |
| Layer | 7 |
| Activation width | 768 |
| Dictionary features | 32768 |
| Checkpoint license | mit |
| Checkpoint revision | `21df74db7b9f690cd2403a20485cf75f46330d0d` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"normalize_activations": "layer_norm", "context_size": 64, "prepend_bos": false, "apply_b_dec_to_input": true, "k": 32}`

**Weight SHA256:** `34a54c2f592d322ff534ca283fba3c5b256573b8813af25c4bb660c3f6b149d5`

[Checkpoint configuration](https://huggingface.co/jbloom/GPT2-Small-OAI-v5-32k-resid-post-SAEs/resolve/21df74db7b9f690cd2403a20485cf75f46330d0d/v5_32k_layer_7.pt/cfg.json)

**Published release names:** `gpt2-small-resid-post-v5-32k` / `blocks.7.hook_resid_post`

---

<a id="sae-40fe01d7c7565e5f61f22dea"></a>

## blocks.8.hook_resid_post on gpt2-small

**Model ID:** `sae-40fe01d7c7565e5f61f22dea`

[Download weights](https://huggingface.co/jbloom/GPT2-Small-OAI-v5-32k-resid-post-SAEs/resolve/21df74db7b9f690cd2403a20485cf75f46330d0d/v5_32k_layer_8.pt/sae_weights.safetensors)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `gpt2-small` |
| Method | [topk](../../topk.md) |
| Source hook / output | `blocks.8.hook_resid_post` |
| Layer | 8 |
| Activation width | 768 |
| Dictionary features | 32768 |
| Checkpoint license | mit |
| Checkpoint revision | `21df74db7b9f690cd2403a20485cf75f46330d0d` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"normalize_activations": "layer_norm", "context_size": 64, "prepend_bos": false, "apply_b_dec_to_input": true, "k": 32}`

**Weight SHA256:** `b56314c681998f6a782c65de9a0969d3634b9ced79021a7ccaa8ec983cae70eb`

[Checkpoint configuration](https://huggingface.co/jbloom/GPT2-Small-OAI-v5-32k-resid-post-SAEs/resolve/21df74db7b9f690cd2403a20485cf75f46330d0d/v5_32k_layer_8.pt/cfg.json)

**Published release names:** `gpt2-small-resid-post-v5-32k` / `blocks.8.hook_resid_post`

---

<a id="sae-4d35450316c733c60c2782ec"></a>

## blocks.9.hook_resid_post on gpt2-small

**Model ID:** `sae-4d35450316c733c60c2782ec`

[Download weights](https://huggingface.co/jbloom/GPT2-Small-OAI-v5-32k-resid-post-SAEs/resolve/21df74db7b9f690cd2403a20485cf75f46330d0d/v5_32k_layer_9.pt/sae_weights.safetensors)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `gpt2-small` |
| Method | [topk](../../topk.md) |
| Source hook / output | `blocks.9.hook_resid_post` |
| Layer | 9 |
| Activation width | 768 |
| Dictionary features | 32768 |
| Checkpoint license | mit |
| Checkpoint revision | `21df74db7b9f690cd2403a20485cf75f46330d0d` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"normalize_activations": "layer_norm", "context_size": 64, "prepend_bos": false, "apply_b_dec_to_input": true, "k": 32}`

**Weight SHA256:** `8794350d4f1022c7d7d4ca85fbd25e2c054e36533233ff5aafe90ae4bcb6342f`

[Checkpoint configuration](https://huggingface.co/jbloom/GPT2-Small-OAI-v5-32k-resid-post-SAEs/resolve/21df74db7b9f690cd2403a20485cf75f46330d0d/v5_32k_layer_9.pt/cfg.json)

**Published release names:** `gpt2-small-resid-post-v5-32k` / `blocks.9.hook_resid_post`

---

<a id="sae-56dd255fcebf8d2d2846c098"></a>

## blocks.10.hook_resid_post on gpt2-small

**Model ID:** `sae-56dd255fcebf8d2d2846c098`

[Download weights](https://huggingface.co/jbloom/GPT2-Small-OAI-v5-32k-resid-post-SAEs/resolve/21df74db7b9f690cd2403a20485cf75f46330d0d/v5_32k_layer_10.pt/sae_weights.safetensors)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `gpt2-small` |
| Method | [topk](../../topk.md) |
| Source hook / output | `blocks.10.hook_resid_post` |
| Layer | 10 |
| Activation width | 768 |
| Dictionary features | 32768 |
| Checkpoint license | mit |
| Checkpoint revision | `21df74db7b9f690cd2403a20485cf75f46330d0d` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"normalize_activations": "layer_norm", "context_size": 64, "prepend_bos": false, "apply_b_dec_to_input": true, "k": 32}`

**Weight SHA256:** `16fff897e0a033ae2d4f169f84dc28fb5ac0d0824238f15c12705761399a4533`

[Checkpoint configuration](https://huggingface.co/jbloom/GPT2-Small-OAI-v5-32k-resid-post-SAEs/resolve/21df74db7b9f690cd2403a20485cf75f46330d0d/v5_32k_layer_10.pt/cfg.json)

**Published release names:** `gpt2-small-resid-post-v5-32k` / `blocks.10.hook_resid_post`

---

<a id="sae-0fb0414f2b3f7fd7a5d615d4"></a>

## blocks.11.hook_resid_post on gpt2-small

**Model ID:** `sae-0fb0414f2b3f7fd7a5d615d4`

[Download weights](https://huggingface.co/jbloom/GPT2-Small-OAI-v5-32k-resid-post-SAEs/resolve/21df74db7b9f690cd2403a20485cf75f46330d0d/v5_32k_layer_11.pt/sae_weights.safetensors)

| Property | Value |
| --- | --- |
| Artifact | SAE dictionary |
| Base model | `gpt2-small` |
| Method | [topk](../../topk.md) |
| Source hook / output | `blocks.11.hook_resid_post` |
| Layer | 11 |
| Activation width | 768 |
| Dictionary features | 32768 |
| Checkpoint license | mit |
| Checkpoint revision | `21df74db7b9f690cd2403a20485cf75f46330d0d` |
| Tensor format | saelens |

**Input / activation conventions:**

`{"normalize_activations": "layer_norm", "context_size": 64, "prepend_bos": false, "apply_b_dec_to_input": true, "k": 32}`

**Weight SHA256:** `a476729ee18b37871b5f5317a7f2c71aa3f0ba329fba823371073152a6a6f6cf`

[Checkpoint configuration](https://huggingface.co/jbloom/GPT2-Small-OAI-v5-32k-resid-post-SAEs/resolve/21df74db7b9f690cd2403a20485cf75f46330d0d/v5_32k_layer_11.pt/cfg.json)

**Published release names:** `gpt2-small-resid-post-v5-32k` / `blocks.11.hook_resid_post`

---

## Metadata sources

- [Pinned published listing 1](https://github.com/decoderesearch/SAELens/blob/30c4502466785dd7809a307f7b705df187978aa3/sae_lens/pretrained_saes.yaml)
