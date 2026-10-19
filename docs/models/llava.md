# LLaVA

[Home](../../README.md) / [Models](README.md) / LLaVA

Example checkpoint: [llava-hf/llava-1.5-7b-hf](https://huggingface.co/llava-hf/llava-1.5-7b-hf).
Native class: `LlavaForConditionalGeneration`. Install `python -m pip install "vlmprobe[transformers,visualization]"`. The example uses one GPU; choose float32 for CPU execution.

## Load and probe

```python
from io import BytesIO
from urllib.request import urlopen
import os
import torch
from PIL import Image
from transformers import AutoModelForImageTextToText, AutoProcessor
from vlmprobe import Prober, visualization as viz

model_id = "llava-hf/llava-1.5-7b-hf"
model_id = os.environ.get("VLM_PROBING_MODEL", model_id)
device = os.environ.get("VLM_PROBING_DEVICE", "cuda:0" if torch.cuda.is_available() else "cpu")
dtype = torch.bfloat16 if device.startswith("cuda") else torch.float32
model = AutoModelForImageTextToText.from_pretrained(
    model_id, dtype=dtype, device_map={"": device},
    attn_implementation="eager",
).eval()
processor = AutoProcessor.from_pretrained(model_id, use_fast=False)
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
    messages, tokenize=False, add_generation_prompt=True,
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

Supports the native `LlavaForConditionalGeneration` class with a Llama text backbone. The processor must expand each image placeholder to the actual visual token sequence. Legacy unexpanded input layouts are not inferred or silently remapped.

Lens readouts, observational attention maps, and residual causal methods are available with eager attention. This is the classic LLaVA family; LLaVA-NeXT, OneVision, and original remote-code wrappers have different contracts and are not registered under this adapter.

Transformers 5.3 eager Llama attention exposes audited, weight-free masked-score
and consumed-probability taps. These enable knockout, temperature, probability
reweighting and attention-space integrated attribution. Original input-path EAP-IG
has an audited GPT-2 graph, with VLM graph support requiring further validation.
See the [capability matrix](README.md#capability-matrix).

Grad-CAM, TAM and Beyond Intuition are target-conditioned method transfers at
language-decoder attention sites. They do not constitute full-model DTD/LRP;
the original-rule DTD backend is scoped to the [ViT control](vit.md).

## Validation

Validated with a tiny randomly initialized instance including real image pixels,
the vision tower, projector, and decoder. The pretrained 7B checkpoint was also
run on GQA attribute questions and COCO 2014 captioning examples; those historical
measurements are recorded in the [technical report](../assets/vlmprobe-technical-report.pdf).
The current [Attention Knockout](../../demos/attention_knockout_demo.ipynb)
and [Steering / VSV](../../demos/steering_vsv_demo.ipynb) walkthroughs teach the
same public methods using the smaller SmolVLM-500M default checkpoint.

See the [architecture checks](../../examples/hf_model_matrix.py) and the
[official model implementation](https://github.com/huggingface/transformers/blob/v5.3.0/src/transformers/models/llava/modeling_llava.py).

Next: [method guides](../methods/README.md) and [metrics/calibration](../API.md).
