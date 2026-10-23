# Qwen2 and Qwen3 (text-only controls)

[Home](../../README.md) / [Models](README.md)

The exact native `Qwen2ForCausalLM` and `Qwen3ForCausalLM` classes have automatic
adapters in Transformers **5.3.x**. Install
`python -m pip install "vlmprobe[transformers,visualization]"`.
These are text-only models, distinct from Qwen-VL and Qwen3.5 hybrid models.

## Load, prepare and probe

```python
import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from vlmprobe import Prober, TokenMargin, visualization as viz

# For Qwen2, use e.g. Qwen/Qwen2.5-0.5B-Instruct (native Qwen2ForCausalLM).
model_id = os.environ.get("VLM_PROBING_MODEL", "Qwen/Qwen3-0.6B")
device = "cuda:0" if torch.cuda.is_available() else "cpu"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id, attn_implementation="eager",
).to(device).eval()
probe = Prober(model, tokenizer)
prompt = "The capital of France is"
inputs = {key: value.to(device) for key, value in tokenizer(
    prompt, return_tensors="pt"
).items()}
print(type(model).__name__)
print(probe.describe())
layers = probe.describe()["methods"]["lens.logit"]["sites"]
selected = list(dict.fromkeys([layers[0], layers[len(layers) // 2], layers[-1]]))
result = probe.lens.logit(layers=selected, tokens="last_prompt").run(inputs)
target_id = int(result.tensors["logits"][-1, 0].argmax())
print("Next token:", repr(tokenizer.decode([target_id])))
ax = viz.plot_lens_heatmap(result, target_token_id=target_id)
ax.figure.savefig("qwen-text-logit-lens.png", bbox_inches="tight")
result.save("qwen-text-logit-lens")

# The entire vocabulary is searched; no image tokens exist in these inputs.
neighbors = probe.lens.embed(tokens="all").run(inputs, top_k=3)
print(neighbors.tensors["token_ids"])

# Build a fixed answer contrast from token IDs present in this tokenizer.
ranked = result.tensors["logits"][-1, 0].topk(2).indices.tolist()
metric = TokenMargin(positive=ranked[0], negative=ranked[1])
map_result = probe.attention.grad_cam(layers=[layers[-1]], queries="last_prompt", keys="all").run(
    inputs, metric=metric,
)
print(map_result.tensors["cam"].shape)
map_result.save("qwen-text-grad-cam")
```

## Capabilities and boundaries

Residual and embedding lenses, projected heads, activation interventions and
IOI-style path controls use the same method APIs as the VLM adapters. With
`attn_implementation="eager"`, the audited attention taps additionally expose
actual consumed probabilities and pre-softmax scores for profile, Grad-CAM,
ATTATTR, reweighting, temperature and knockout. SDPA retains residual and path
controls but does not expose attention matrices. Inspect `probe.describe()`
for the exact instance before selecting layers.

Qwen3 Q/K path receiver hooks are **after per-head Q/K normalization and before
rotary position encoding**; Qwen2 hooks are at the Q/K projections before
rotation. Query heads and physical K/V heads are declared separately for GQA.
The output head capture excludes output-projection bias.

No input positions are visual. Use explicit text positions or `"all"`; default
`tokens="visual"` for EmbedLens is empty. Tuned, Jacobian and Attention Lens
require calibration or artifacts for this exact checkpoint. Input-path TAM and
Beyond Intuition require an explicit floating input and matching token layout;
integer token IDs cannot be interpolated. Their `pixel_values` default is not a
text-model input. Rollout/relevance and these propagation methods carry the
[causal-mask caveat](../methods/attention_rollout.md#causal-decoder-applicability).

Validation uses small random-weight native models on CPU with float32 and BF16:
forward/embedding-gradient parity, final readout agreement, padding and embedding
coordinates, Q/K normalization stage, projected-head reconstruction, consumed
attention edits, identity/nontrivial path edits and cleanup after failure.
The checkpoint names above are loading examples, not new pretrained evaluations.
Qwen2/Qwen3 text automatic adapters are not claimed for Transformers 4.57.x;
unknown wrappers require an [explicit adapter](../ADAPTERS.md).
