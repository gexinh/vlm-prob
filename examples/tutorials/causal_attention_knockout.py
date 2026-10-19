"""Live tutorial: run after installing vlmprobe[transformers,visualization]."""
# 1. Load an eager-attention native model
import os
import hashlib
import urllib.request
from pathlib import Path
import torch
import matplotlib.pyplot as plt
from PIL import Image
from transformers import AutoModelForImageTextToText, AutoProcessor
from vlmprobe import Prober, TokenMargin
from vlmprobe.visualization import plot_input, plot_intervention_curves

# This recipe targets the SmolVLM/Idefics3 image/chat contract.
# First run downloads the 500M model (~1 GB); CUDA is recommended.
model_id = os.environ.get("VLM_PROBING_MODEL", "HuggingFaceTB/SmolVLM-500M-Instruct")
device = os.environ.get("VLM_PROBING_DEVICE", "cuda:0" if torch.cuda.is_available() else "cpu")
dtype = torch.bfloat16 if device.startswith("cuda") else torch.float32
model = AutoModelForImageTextToText.from_pretrained(
    model_id, dtype=dtype, attn_implementation="eager",
).to(device).eval()
processor = AutoProcessor.from_pretrained(model_id)
probe = Prober(model, processor=processor)
assert model.config.model_type == "idefics3", "Use this recipe with SmolVLM; other models need their native input guide"
print({name: info for name, info in probe.describe()["methods"].items()
       if name.startswith("causal.")})
output_dir = Path(os.environ.get("VLM_PROBING_OUTPUT", "outputs/tutorials/causal"))
output_dir.mkdir(parents=True, exist_ok=True)


# 2. Read the raw COCO input
# A raw COCO image, not an attribution asset or cached model output.
filename = "COCO_val2014_000000310196.jpg"
expected_sha256 = "0dcc39d91764e59e0e01c11b92ec31320f094a87ca2dce5e0c56c4f1a361daf4"
custom_image = os.environ.get("VLM_PROBING_IMAGE")
root = next((p for p in [Path.cwd(), *Path.cwd().parents]
             if (p / "demos/assets/images" / filename).is_file()), None)
image_path = Path(custom_image) if custom_image else (root / "demos/assets/images" / filename if root else output_dir / filename)
if custom_image and not image_path.is_file():
    raise FileNotFoundError(image_path)
if not image_path.is_file():
    url = "https://s3.amazonaws.com/images.cocodataset.org/val2014/" + filename
    with urllib.request.urlopen(url, timeout=60) as response:
        image_path.write_bytes(response.read())
if not custom_image:
    assert hashlib.sha256(image_path.read_bytes()).hexdigest() == expected_sha256
image = Image.open(image_path).convert("RGB")


# 3. Prepare the prompt and a fixed answer score
question = "Is there a person in this image? Answer yes or no."
messages = [{"role": "user", "content": [
    {"type": "image"}, {"type": "text", "text": question},
]}]
prompt = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
prepared = probe.prepare(prompt=prompt, image=image, device=device)
# prepare preserves integer fields; cast only floating image inputs for this model.
inputs = {key: value.to(dtype=dtype) if isinstance(value, torch.Tensor) and value.is_floating_point()
          else value for key, value in prepared.kwargs.items()}
positive_ids = processor.tokenizer.encode("Yes", add_special_tokens=False)
negative_ids = processor.tokenizer.encode("No", add_special_tokens=False)
print("Answer subwords:", processor.tokenizer.decode([positive_ids[0]]),
      processor.tokenizer.decode([negative_ids[0]]))
metric = TokenMargin(positive_ids[0], negative_ids[0])
# This targets the first vocabulary subword; it is not complete-answer scoring.
available = sorted(probe.spec.attention_scores)
assert available, "Use an audited eager-attention model for knockout"
layers = sorted({available[0], available[len(available)//2], available[-1]})


# 4. Measure independent and joint route blocks
curves = {}
for label, queries in [("Visual keys to last prompt token", "last_prompt"),
                       ("Visual keys to all text tokens", "text")]:
    result = probe.causal.knockout(layers=layers, queries=queries,
                                  keys="visual", joint=False).run(inputs, metric=metric)
    curves[label] = result
    print(label, "measured effect:", result.tensors["effect"])
    result.save(output_dir / ("knockout_prediction" if queries == "last_prompt" else "knockout_text"))
ax = plot_intervention_curves(curves, tensor="effect", xlabel="Independently blocked layer",
                              ylabel="Change in Yes-minus-No first-subword margin",
                              title="Block visual attention routes before softmax")
ax.figure.savefig(output_dir / "causal-attention-knockout.png", dpi=150, bbox_inches="tight")
plt.show()
# For a simultaneous multi-layer intervention, configure joint=True explicitly.
joint = probe.causal.knockout(layers=layers, queries="last_prompt", keys="visual", joint=True)
joint_result = joint.run(inputs, metric=metric)
print("Joint effect (not the sum of independent effects):", joint_result.tensors["effect"])
