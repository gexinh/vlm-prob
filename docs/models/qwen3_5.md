# Qwen3.5

[Home](../../README.md) / [Models](README.md) / Qwen3.5

Example checkpoint: [Qwen/Qwen3.5-4B](https://huggingface.co/Qwen/Qwen3.5-4B).
Native class: `Qwen3_5ForConditionalGeneration`. Install `python -m pip install "vlmprobe[transformers,visualization]"`. The example uses one GPU; choose float32 for CPU execution.

## Load and probe

```python
from io import BytesIO
from urllib.request import urlopen
import os
import torch
from PIL import Image
from transformers import AutoModelForImageTextToText, AutoProcessor
from vlmprobe import Prober, visualization as viz

model_id = "Qwen/Qwen3.5-4B"
model_id = os.environ.get("VLM_PROBING_MODEL", model_id)
device = os.environ.get("VLM_PROBING_DEVICE", "cuda:0" if torch.cuda.is_available() else "cpu")
dtype = torch.bfloat16 if device.startswith("cuda") else torch.float32
model = AutoModelForImageTextToText.from_pretrained(
    model_id, dtype=dtype, device_map={"": device},
    attn_implementation="eager",
).eval()
processor = AutoProcessor.from_pretrained(model_id)
probe = Prober(model, processor)

# A bundled GQA input photo; replace this URL with your own image.
image_url = "https://raw.githubusercontent.com/gexinh/vlm-probing/main/demos/assets/images/2341576.jpg"
with urlopen(image_url, timeout=30) as response:
    image = Image.open(BytesIO(response.read())).convert("RGB")

messages = [{"role": "user", "content": [
    {"type": "image"},
    {"type": "text", "text": "What is in this image?"},
]}]
prompt = processor.apply_chat_template(
    messages, tokenize=False, add_generation_prompt=True, enable_thinking=False,
)
inputs = probe.prepare(
    prompt=prompt, image=image, device=device,
)
# Keep integer token/grid fields intact; match floating image tensors to the model.
for key, value in inputs.kwargs.items():
    if isinstance(value, torch.Tensor) and value.is_floating_point():
        inputs.kwargs[key] = value.to(dtype=dtype)

capabilities = probe.describe()["methods"]
for name, capability in capabilities.items():
    print(name, capability["available"], capability["sites"], capability["missing"])

# This is one method example, not the list of methods supported by this model.
available = capabilities["lens.logit"]["sites"]
layers = list(dict.fromkeys([available[0], available[len(available) // 2], available[-1]]))
result = probe.lens.logit(layers=layers, tokens="last_prompt").run(inputs)
print(result.tensors["positions"], result.tensors["logits"].shape)
# Inspect the final readout's top token across these layers, without assuming a label.
target_id = int(result.tensors["logits"][-1, 0].argmax())
print("Target token:", target_id, repr(processor.tokenizer.decode([target_id])))
ax = viz.plot_lens_heatmap(result, target_token_id=target_id)
ax.figure.savefig("model-lens.png", bbox_inches="tight")
result.save("model-lens-result")
```

The same `probe.lens`, `probe.attention`, and `probe.causal` factories apply to
this model. The single Logit Lens call above only verifies the loaded binding;
it does not limit the model to that method. Follow the [method guides](../methods/README.md)
for complete training, target-score, paired-input and plotting examples, or the
[shared model workflow](README.md#use-any-supported-method) to switch methods.
`describe()` reports supported operations, not the presence of trained lens artifacts.
Pass the complete native processor dictionary to `.run(...)` if inputs are already prepared.
The downloaded photo is an illustrative input, not a benchmark evaluation.

## Adapter behavior

Qwen3.5-4B has 32 language layers. Residual lenses and interventions cover all 32. Attention Lens, attention profiles, and head logit attribution cover full-attention layers **3, 7, 11, 15, 19, 23, 27, 31**. Linear-attention layers do not expose a token-by-token softmax matrix, so rollout and relevance are unavailable on this checkpoint.

The adapter captures gated values immediately before the attention output projection and handles the final RMSNorm's `1 + weight` gain. `H * head_dim` need not equal the residual width. Transformers' PyTorch fallback works without the optional fast linear-attention kernels.

The eager adapter exposes editable pre-softmax scores and consumed attention
probabilities at standard-attention layers. Knockout, temperature, reweighting,
and ATTATTR operate on these sites; hybrid linear-attention blocks have no
softmax-probability counterpart. Original EAP-IG remains a GPT-2 graph method.

## Validation

Both the tiny architecture and the named local pretrained checkpoint were run. Pretrained checks cover an image prompt, selected Logit Lens layers, EmbedLens, an attention profile, self-patching, and an image intervention.

See the [architecture checks](../../examples/hf_model_matrix.py) and the
[official model implementation](https://github.com/huggingface/transformers/blob/v5.3.0/src/transformers/models/qwen3_5/modeling_qwen3_5.py).

Next: [method guides](../methods/README.md) and [metrics/calibration](../API.md).
