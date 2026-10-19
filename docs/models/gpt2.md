# GPT-2 (IOI reference architecture)

[Home](../../README.md) / [Models](README.md)

The native `GPT2LMHeadModel` adapter supports the text decoder used in the
IOI circuit study. Install `python -m pip install "vlmprobe[transformers,visualization]"`.
This example downloads pretrained GPT-2 small (about 124M parameters), tokenizes
an actual prompt and plots a live vocabulary readout.

## Load and prepare text

```python
import os
import torch
from transformers import AutoTokenizer, GPT2LMHeadModel
from vlmprobe import Prober, visualization as viz

model_id = os.environ.get("VLM_PROBING_MODEL", "openai-community/gpt2")
device = os.environ.get("VLM_PROBING_DEVICE", "cpu")
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = GPT2LMHeadModel.from_pretrained(
    model_id, attn_implementation="eager",
).to(device).eval()
probe = Prober(model, tokenizer)
inputs = {key: value.to(device) for key, value in tokenizer(
    "When Mary and John went to the store, John gave a drink to", return_tensors="pt"
).items()}
capabilities = probe.describe()["methods"]
for name, item in capabilities.items():
    print(name, item["available"], item["sites"], item["missing"])

layers = capabilities["lens.logit"]["sites"]
result = probe.lens.logit(layers=layers, tokens="last_prompt").run(inputs)
answer_ids = tokenizer.encode(" Mary", add_special_tokens=False)
assert len(answer_ids) == 1
ax = viz.plot_lens_heatmap(result, target_token_id=answer_ids[0], tokenizer=tokenizer)
ax.figure.savefig("gpt2-logit-lens.png", bbox_inches="tight")
result.save("gpt2-logit-lens-result")
```

This single example does not establish the model's IOI circuit. The same model
binding supports the [method guides](../methods/README.md), including complete
training examples for calibrated lenses and clean/reference construction for
[activation](../methods/activation_patching.md), [path](../methods/path_patching.md)
and [EAP-IG](../methods/eap_ig.md) analyses. Method calls retain their common
syntax; valid layers and capabilities come from the bound model. See the
[shared workflow](README.md#use-any-supported-method).

## Adapter behavior

The adapter captures each attention head's message at the input to `c_proj`.
Freezing that message freezes its contribution after the fixed output matrix;
the shared projection bias remains unchanged. Q/K/V receivers are separate
slices of the packed `c_attn` output, so replacing Q leaves K and V intact. Final
residual receivers are measured before `transformer.ln_f`.

Logit lenses use the model's final LayerNorm and language head. The adapter does
not expose fixed-scale head logit attribution for GPT-2's affine LayerNorm.
Attention observation requires eager attention; path patching operates on
projection sites and does not require attention probabilities. Cross-attention
configurations require an explicit adapter.

## Validation

Random GPT-2 configurations were tested with Transformers 5.3.0. Validation
checks the packed Q/K/V shapes, the reconstruction of the attention output from
per-head contributions, and equality between final-residual decoding and the
unmodified full forward pass. Four-stage forwards also cover joint Q/K/V and
final-residual receivers in padded batches, including a zero-effect check with
identical base and donor inputs. These checks validate the implementation; they
are not a reproduction of the pretrained IOI circuit.

See [IOI-style path patching](../methods/path_patching.md) and the
[official GPT-2 implementation](https://github.com/huggingface/transformers/blob/v5.3.0/src/transformers/models/gpt2/modeling_gpt2.py).

The [live EAP-IG notebook](../../demos/eap_ig_demo.ipynb) additionally runs
pretrained GPT-2 small on two author-published IOI pairs. Configure
`probe.causal.eap_ig(graph="transformer", steps=5)` for original input-embedding
integration over independent pre-LayerNorm Q/K/V, MLP, and readout messages.
Its 32,491-edge graph supports actual complement-edge replacement to evaluate
retained circuits. This graph currently covers native GPT-2 self-attention;
cross-attention and reordered/upcast attention are rejected.
