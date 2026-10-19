# ViT vision-classification control

[Home](../../README.md) / [Models](README.md)

Native `transformers.ViTForImageClassification` is supported on Transformers
5.3.x with eager attention. This is a pure-vision control for spatial
attribution comparisons; it has no language vocabulary lens.

Install `python -m pip install "vlmprobe[transformers,visualization]"`.
This complete example downloads ViT-B/16 and an input photo, then computes a
class-conditioned map. The displayed image is explicitly resized to the same
224×224 frame used by the processor.

```python
from io import BytesIO
from urllib.request import urlopen
import os
import torch
from PIL import Image
from transformers import AutoImageProcessor, ViTForImageClassification
from vlmprobe import ClassScore, Prober, visualization as viz

checkpoint = os.environ.get("VLM_PROBING_VIT_MODEL", "google/vit-base-patch16-224")
device = os.environ.get("VLM_PROBING_DEVICE", "cpu")
processor = AutoImageProcessor.from_pretrained(checkpoint)
model = ViTForImageClassification.from_pretrained(
    checkpoint, attn_implementation="eager",
).to(device).eval()
url = "https://raw.githubusercontent.com/gexinh/vlm-probing/main/demos/assets/images/2341576.jpg"
with urlopen(url, timeout=30) as response:
    image = Image.open(BytesIO(response.read())).convert("RGB").resize((224, 224))
inputs = {key: value.to(device) for key, value in processor(
    images=image, return_tensors="pt"
).items()}
probe = Prober(model)
with torch.no_grad():
    target = int(model(**inputs).logits.argmax(-1).item())
print("Target:", target, model.config.id2label[target])
print(probe.describe())
last = probe.describe()["methods"]["attention.grad_cam"]["sites"][-1]
cam = probe.attention.grad_cam(layers=[last]).run(inputs, metric=ClassScore(target))
patch = model.config.patch_size
grid = (inputs["pixel_values"].shape[-2] // patch,
        inputs["pixel_values"].shape[-1] // patch)
ax = viz.plot_attention_overlay(
    image, cam, tensor="cam", grid_shape=grid,
    visual_positions=list(range(1, 1 + grid[0] * grid[1])), query_positions=[0],
    image_alpha=0.2, title=model.config.id2label[target],
)
ax.figure.savefig("vit-grad-cam.png", bbox_inches="tight")
cam.save("vit-grad-cam-result")
```

Follow the [attention method guides](../methods/README.md#attention) for complete
API/parameter examples for ATTATTR, TAM, Beyond Intuition and DTD/LRP. Their
factory/run structure is shared; this model's metric is `ClassScore` instead
of a language token or sequence score. See the
[shared workflow](README.md#use-any-supported-method).

Map factories default to CLS query `[0]` and spatial keys `"visual"` for this
adapter. Native logits remain `[B,C]`; `ClassScore(kind="logit")` names the
selected class explicitly. The adapter exposes consumed probabilities and
masked scores without changing weights; no-op forwards are bit-for-bit equal
in the CPU check. Patch coordinates are row-major after CLS and refer to the
processor's fixed resized/cropped image, not automatically to the source image.
Interpolated position grids and distilled DeiT variants are not declared native
support in this adapter.

DTD requires the eligible author architecture; unsupported activation/config
variants raise an error rather than substituting a gradient recurrence. Its
factory creates a separate weight copy, so account for that memory. Both architecture tests and pretrained author-checkpoint demonstrations are
available. The [live ViT attention notebook](../../demos/attention_comparison_demo.ipynb)
computes maps from the public Google checkpoint and a raw COCO image, including
genuine DTD/LRP on a copy of the same classifier weights. Historical author-image
measurements remain in the report archive.
