# SmolVLM

[Home](../../README.md) / [Models](README.md) / SmolVLM

Example checkpoint: [HuggingFaceTB/SmolVLM-256M-Instruct](https://huggingface.co/HuggingFaceTB/SmolVLM-256M-Instruct).
Native class: `Idefics3ForConditionalGeneration`. Install `python -m pip install "vlmprobe[transformers,visualization]"`. The example uses one GPU; choose float32 for CPU execution.

## Load and probe

```python
from io import BytesIO
from urllib.request import urlopen
import os
import torch
from PIL import Image
from transformers import AutoModelForImageTextToText, AutoProcessor
from vlmprobe import Prober, visualization as viz

model_id = "HuggingFaceTB/SmolVLM-256M-Instruct"
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

SmolVLM-256M-Instruct is registered by its actual checkpoint class, `Idefics3ForConditionalGeneration`, with a Llama text backbone at `model.text_model`. The processor handles image crops, visual placeholders, and pixel masks; pass all returned fields to the model. Layouts mark only the image-content slots, excluding image boundary tokens. SmolVLM2 checkpoints using the separate `SmolVLMForConditionalGeneration` class are not part of this adapter.

SmolVLM treats an all-zero image tile as padding. For a blank-image control, process a real blank PIL image through the same processor rather than zeroing `pixel_values`. The same constraint applies to input-path integration: endpoint-inclusive sampling needs a baseline that preserves the valid tile layout. Lens readouts, observational attention maps, and residual causal methods are available with eager attention.

Its native Llama backbone exposes audited score and consumed-probability taps
with Transformers 5.3 eager attention. These enable knockout, temperature,
reweighting and attention-space attribution. EAP-IG requires an explicit
validated edge graph. See the
[capability matrix](README.md#capability-matrix).

## Validation

SmolVLM-500M-Instruct also runs all eight fixed report cases with actual
residual replacements, editable attention and a full paired-image path sweep.
Three Tuned Lens translators are independently calibrated on COCO captions.
See the [technical report](https://github.com/gexinh/vlm-probing-report/blob/main/technical-report.pdf) and
[VLM lens notebook](../../demos/vlm_lens_demo.ipynb).

Both the tiny architecture and the named pretrained checkpoint were run. Pretrained checks cover an image prompt, selected Logit Lens layers, EmbedLens, an attention profile, self-patching, and an image intervention. The processor expanded the image to 1,088 visual slots, all correctly identified by the adapter.

See the [architecture checks](../../examples/hf_model_matrix.py) and the
[official model implementation](https://github.com/huggingface/transformers/blob/v5.3.0/src/transformers/models/idefics3/modeling_idefics3.py).

Next: [method guides](../methods/README.md) and [metrics/calibration](../API.md).
