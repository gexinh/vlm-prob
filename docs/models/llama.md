# Llama (text-only control)

[Home](../../README.md) / [Models](README.md)

The native `LlamaForCausalLM` adapter provides text-only controls. Method APIs
are the same as the VLM APIs; image-specific selectors do not apply. Install
`python -m pip install "vlmprobe[transformers,visualization]"`.

The example uses the public SmolLM2-135M-Instruct checkpoint, whose native class
is `LlamaForCausalLM`. To use a Meta Llama checkpoint, change `model_id` and
obtain any required Hugging Face access before downloading weights.

## Load and prepare text

```python
import os
import torch
from transformers import AutoTokenizer, LlamaForCausalLM
from vlmprobe import Prober, visualization as viz

model_id = os.environ.get("VLM_PROBING_MODEL", "HuggingFaceTB/SmolLM2-135M-Instruct")
device = os.environ.get("VLM_PROBING_DEVICE", "cuda:0" if torch.cuda.is_available() else "cpu")
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = LlamaForCausalLM.from_pretrained(
    model_id, attn_implementation="eager",
).to(device).eval()
probe = Prober(model, tokenizer)
prompt = tokenizer.apply_chat_template(
    [{"role": "user", "content": "What is the capital of France?"}],
    tokenize=False, add_generation_prompt=True,
)
inputs = {key: value.to(device) for key, value in tokenizer(
    prompt, add_special_tokens=False, return_tensors="pt"
).items()}
capabilities = probe.describe()["methods"]
for name, item in capabilities.items():
    print(name, item["available"], item["sites"], item["missing"])
layers = capabilities["lens.logit"]["sites"]
selected = list(dict.fromkeys([layers[0], layers[len(layers) // 2], layers[-1]]))
result = probe.lens.logit(layers=selected).run(inputs)
target_id = int(result.tensors["logits"][-1, 0].argmax())
print("Target token:", target_id, repr(tokenizer.decode([target_id])))
ax = viz.plot_lens_heatmap(result, target_token_id=target_id)
ax.figure.savefig("llama-logit-lens.png", bbox_inches="tight")
result.save("llama-logit-lens-result")
```

Continue with any supported [method guide](../methods/README.md), retaining this
model/tokenizer/input block. Calibrated lenses need new model-specific artifacts;
GPT-2 artifacts cannot be transferred by renaming files. The example checkpoint
is a loading recipe, not a claim of a new evaluation in the technical report.
See the [shared workflow](README.md#use-any-supported-method).

Use `tokens="all"` or `"last_prompt"` for residual causal methods, and
`tokens="all"` for EmbedLens; the default visual selection is empty.
The same class can be loaded with `LlamaForCausalLM.from_pretrained(...)`.
Tested on random configurations in Transformers 4.57.6 and 5.3.0, including
padding, grouped-query attention, and frozen-parameter gradient relevance.

Transformers 5.3 eager attention additionally supports real pre-softmax knockout
and temperature interventions through weight-free score taps. Select explicit
text token positions as keys; a text-only model has no visual token selection.
Consumed-probability taps also support reweighting and Hao attention attribution.
Input-path TAM/Beyond Intuition require an explicit floating embedding input;
the default `pixel_values` path does not apply to a text-only model.
