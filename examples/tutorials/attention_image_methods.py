from pathlib import Path
import os
from io import BytesIO
from urllib.request import urlopen
import numpy as np
import torch
from PIL import Image
from transformers import AutoImageProcessor, ViTForImageClassification
from vlmprobe import Prober, ClassScore
from vlmprobe import visualization as viz
import matplotlib.pyplot as plt

# Install: pip install "vlmprobe[transformers,visualization]"
# Set VLM_PROBING_MODEL to a local directory to avoid downloading this checkpoint.
model_id = os.environ.get("VLM_PROBING_MODEL", "google/vit-base-patch16-224")
device = os.environ.get("VLM_PROBING_DEVICE", "cuda:0" if torch.cuda.is_available() else "cpu")
model = ViTForImageClassification.from_pretrained(model_id, attn_implementation="eager").to(device).eval()
processor = AutoImageProcessor.from_pretrained(os.environ.get("VLM_PROBING_PROCESSOR", model_id))
probe = Prober(model, processor)

# A raw COCO image, not a saved attention map or a previous model result.
image_path = os.environ.get("VLM_PROBING_IMAGE")
image = (Image.open(image_path) if image_path else Image.open(BytesIO(urlopen(
    "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/coco_sample.png"
).read()))).convert("RGB")
inputs = {k: v.to(device) for k, v in processor(images=image, return_tensors="pt").items()}
with torch.no_grad():
    logits = model(**inputs).logits
    target_id = int(logits[0].argmax())  # Choose once; keep fixed during attribution.
metric = ClassScore(target_id, kind="logit")
print("Fixed target:", target_id, model.config.id2label.get(target_id))

# Plot the actual processed image; its crop/resize aligns with the patch tokens.
mean = torch.tensor(processor.image_mean)[:, None, None]
std = torch.tensor(processor.image_std)[:, None, None]
rgb = (inputs["pixel_values"][0].detach().cpu() * std + mean).clamp(0, 1)
processed_image = Image.fromarray((rgb.permute(1, 2, 0).numpy() * 255).astype("uint8"))
patch = model.config.patch_size
grid_shape = tuple(int(n // patch) for n in inputs["pixel_values"].shape[-2:])
visual_positions = list(range(1, 1 + grid_shape[0] * grid_shape[1]))  # CLS is 0.
last = probe.describe()["methods"]["attention.profile"]["sites"][-1]
output_dir = Path(os.environ.get("VLM_PROBING_OUTPUT", "outputs/attention-tutorial"))
output_dir.mkdir(parents=True, exist_ok=True)
steps = int(os.environ.get("VLM_PROBING_STEPS", "8"))
# 8 samples keep the walkthrough short; use 20+ and check convergence for analysis.
results = {
    "Grad-CAM": probe.attention.grad_cam(layers=[last], queries=[0], keys="visual").run(inputs, metric=metric),
    "ATTATTR": probe.attention.attribution(layers=[last], queries=[0], keys="visual", steps=steps).run(inputs, metric=metric),
    "TAM": probe.attention.tam(queries=[0], keys="visual", steps=steps, residual_normalize=True).run(inputs, metric=metric),
    "Beyond-H": probe.attention.beyond_intuition(variant="head", queries=[0], keys="visual", steps=steps).run(inputs, metric=metric),
    "Beyond-C": probe.attention.beyond_intuition(variant="token", queries=[0], keys="visual", steps=steps).run(inputs, metric=metric),
}
for name, result in results.items():
    print(name, {key: tuple(value.shape) for key, value in result.tensors.items()})
    result.save(output_dir / name.lower())
fig, axes = viz.plot_attention_comparison(
    processed_image, results, grid_shape=grid_shape,
    visual_positions=visual_positions, query_positions=[0], columns=3,
    signed={name: name == "ATTATTR" for name in results},
    shared_scale=False, image_alpha=0.25, alpha=1.0,
)
fig.savefig(output_dir / "attention-maps.png", dpi=160, bbox_inches="tight")
plt.show()
