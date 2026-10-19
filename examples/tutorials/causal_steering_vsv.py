"""Live tutorial: run after installing vlmprobe[transformers,visualization]."""
# 1. Install and load the native VLM
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


# 2. Read the original image and verify its source identity
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


# 3. Prepare a native image prompt and an exact text-only reference
question = "Please help me describe the image in detail."
messages = [{"role": "user", "content": [
    {"type": "image"}, {"type": "text", "text": question},
]}]
prompt = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
values = dict(processor(text=prompt, images=image, return_tensors="pt"))
positive = {key: value.to(device=device, dtype=dtype if value.is_floating_point() else value.dtype)
            if isinstance(value, torch.Tensor) else value for key, value in values.items()}
# SmolVLM surrounds all image crops/global image tokens with a contiguous wrapper span.
# Remove that entire span; preserve the exact tokenized text on either side.
wrapper_id = processor.fake_image_token_id
wrappers = (positive["input_ids"][0] == wrapper_id).nonzero().flatten()
assert wrappers.numel() >= 2, "Expected SmolVLM image wrapper tokens"
keep = torch.ones(positive["input_ids"].shape[1], dtype=torch.bool, device=device)
keep[int(wrappers[0]):int(wrappers[-1]) + 1] = False
negative = {"input_ids": positive["input_ids"][:, keep].clone(),
            "attention_mask": positive["attention_mask"][:, keep].clone()}
assert torch.equal(negative["input_ids"], positive["input_ids"][:, keep])
print("Positive prompt:", prompt)
print("Text-only reference:", processor.tokenizer.decode(negative["input_ids"][0]))
print("Positive/reference token counts:", positive["input_ids"].shape[1], negative["input_ids"].shape[1])
ax = plot_input(image, prompt=question, title="Raw COCO input")
ax.figure.savefig(output_dir / "causal-vsv-input.png", dpi=150, bbox_inches="tight")
plt.show()


# 4. Construct directions, intervene, and generate fresh continuations
# No training: directions are positive-minus-negative last-context residuals.
vectors = probe.causal.vsv(positive, negative, layers=None)
print("Direction construction:", vectors.metadata)
strengths = [0.0, 0.02, 0.05]
max_new_tokens = int(os.environ.get("VLM_PROBING_MAX_NEW_TOKENS", "32"))
# These are exact vocabulary-token logits, not complete word probabilities.
candidates = {word: processor.tokenizer.encode(word, add_special_tokens=False)[0]
              for word in ("person", "car")}
print("Fixed-prefix subwords:", {word: processor.tokenizer.decode([token])
                                  for word, token in candidates.items()})
responses = {word: [] for word in candidates}
captions = {}
for strength in strengths:
    method = vectors.configure(strength=strength, tokens="prediction")
    # All strengths see this same original prompt in this diagnostic.
    trace = method.forward(positive, direction=vectors.directions)
    for word, token in candidates.items():
        responses[word].append(float(trace.logits[0, -1, token]))
    del trace
    output = method.generate(positive, direction=vectors.directions,
                             max_new_tokens=max_new_tokens, do_sample=False)
    captions[strength] = output.metadata["decoded_text"][0]
    print(f"Strength {strength}: {captions[strength]}")
    output.save(output_dir / f"vsv_strength_{strength:g}")


# 5. Visualize the fixed-prefix response and retain full generated text
ax = plot_intervention_curves(
    {word: {"x": strengths, "y": values} for word, values in responses.items()},
    xlabel="Raw residual steering strength", ylabel="First-subword logit",
    title="Same input prefix; per-image VSV strength sweep",
)
ax.figure.savefig(output_dir / "causal-vsv.png", dpi=150, bbox_inches="tight")
plt.show()
# Persist the complete generated continuations, not selected favorable excerpts.
import json
(output_dir / "vsv_captions.json").write_text(json.dumps({
    "model": model_id, "prompt": prompt, "construction": vectors.metadata,
    "max_new_tokens": max_new_tokens, "captions": captions,
    "candidate_ids": candidates, "fixed_prefix_logits": responses,
}, indent=2) + "\n")
