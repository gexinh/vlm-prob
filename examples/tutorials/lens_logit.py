"""Live pretrained GPT-2 tutorial; see docs/methods. No result cache is loaded."""
import os
from pathlib import Path

import matplotlib.pyplot as plt
import torch
from transformers import AutoTokenizer, GPT2LMHeadModel
from vlmprobe import Prober
from vlmprobe.visualization import plot_lens_heatmap

# A pretrained text model, not a random architecture or cached probe result.
MODEL_ID = os.environ.get("VLM_PROBING_MODEL", "openai-community/gpt2")
DEVICE = os.environ.get("VLM_PROBING_DEVICE", "cuda:0" if torch.cuda.is_available() else "cpu")
OUT = Path(os.environ.get("VLM_PROBING_OUTPUT", "outputs/lens_tutorial"))
OUT.mkdir(parents=True, exist_ok=True)
torch.manual_seed(0)
model = GPT2LMHeadModel.from_pretrained(MODEL_ID, attn_implementation="eager").to(DEVICE).eval()
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
probe = Prober(model, tokenizer)
print(probe.describe())

def prepare(text):
    return probe.prepare(prompt=text, device=DEVICE)

prompt = "When Amy and Laura got a snack at the house, Laura decided to give it to"
inputs = prepare(prompt)
answer_ids = tokenizer.encode(" Amy", add_special_tokens=False)
assert len(answer_ids) == 1, "Choose a single target subword for this rank plot."
answer_id = answer_ids[0]

layers = sorted(probe.describe()["methods"]["lens.logit"]["sites"])
result = probe.lens.logit(layers=layers, tokens="text").run(inputs)
print("logits [layers, packed positions, vocabulary]:", result.tensors["logits"].shape)
print("[batch, expanded-token position]:", result.tensors["positions"])
result.save(OUT / "logit-result")
ax = plot_lens_heatmap(result, target_token_id=answer_id, tokenizer=tokenizer,
                       title="Logit Lens: rank of the subword ' Amy'")
ax.figure.savefig(OUT / "logit.png", dpi=160, bbox_inches="tight")
plt.show()
