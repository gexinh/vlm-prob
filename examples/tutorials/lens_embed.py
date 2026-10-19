"""Live projected visual-token nearest-neighbor tutorial. No result cache."""
import hashlib
import os
from pathlib import Path
from urllib.request import urlretrieve

import matplotlib.pyplot as plt
import torch
from PIL import Image
from transformers import AutoModelForImageTextToText, AutoProcessor
from vlmprobe import Prober
from vlmprobe.visualization import plot_input, plot_lens_heatmap

MODEL_ID = os.environ.get("VLM_PROBING_MODEL", "HuggingFaceTB/SmolVLM-500M-Instruct")
DEVICE = os.environ.get("VLM_PROBING_DEVICE", "cuda:0" if torch.cuda.is_available() else "cpu")
OUT = Path(os.environ.get("VLM_PROBING_OUTPUT", "outputs/embed_tutorial"))
OUT.mkdir(parents=True, exist_ok=True)
custom_image = os.environ.get("VLM_PROBING_IMAGE")
image_path = Path(custom_image) if custom_image else OUT / "2341576.jpg"
if custom_image and not image_path.is_file():
    raise FileNotFoundError(image_path)
if not image_path.is_file():
    urlretrieve("https://raw.githubusercontent.com/gexinh/vlm-probing/main/demos/assets/images/2341576.jpg", image_path)
if not custom_image:
    assert hashlib.sha256(image_path.read_bytes()).hexdigest() == "f2f5880022dce631fd23240b2d690a56dd1fa551205c48b16db210b147d2f968"
image = Image.open(image_path).convert("RGB")
question = "Is the shirt black or yellow?"
model = AutoModelForImageTextToText.from_pretrained(
    MODEL_ID, dtype=torch.float32, attn_implementation="eager",
).to(DEVICE).eval()
processor = AutoProcessor.from_pretrained(MODEL_ID)
probe = Prober(model, processor)
print(probe.describe())
messages = [{"role": "user", "content": [
    {"type": "image"}, {"type": "text", "text": question},
]}]
prompt = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
inputs = probe.prepare(prompt=prompt, image=image, device=DEVICE)
result = probe.lens.embed(tokens="visual").run(inputs, top_k=5, vocabulary_chunk_size=4096)
print("neighbors / cosine:", result.tensors["token_ids"].shape, result.tensors["similarities"].shape)
print("coordinates:", result.tensors["positions"].shape)
for position, ids, cosine in zip(result.tensors["positions"][:8],
                                result.tensors["token_ids"][0, :8],
                                result.tensors["similarities"][0, :8]):
    print(position.tolist(), [(processor.tokenizer.decode([int(i)]), round(float(s), 3))
                              for i, s in zip(ids, cosine)])
# Geometry is not guessed: crops/tiles are model-specific. Display exact token
# coordinates rather than stretching a multi-crop sequence over the raw image.
count = min(32, result.tensors["positions"].shape[0])
fig, axes = plt.subplots(2, 1, figsize=(12, 6), height_ratios=[4, 1], constrained_layout=True)
plot_input(image, prompt=question, answer="yellow" if not custom_image else None, ax=axes[0])
plot_lens_heatmap(result.tensors["similarities"][0, :count, 0][None],
                  value_kind="logit", log_scale=False, vmin=-1, vmax=1,
                  layer_labels=["Decoder input"],
                  token_labels=result.tensors["positions"][:count, 1].tolist(),
                  ax=axes[1], value_label="Nearest vocabulary cosine similarity",
                  title="First 32 visual-token positions (not image pixel coordinates)")
fig.savefig(OUT / "embed.png", dpi=160, bbox_inches="tight")
plt.show()
result.save(OUT / "embed-result")
