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

source_text = "The capital of France is Paris"
target_text = "Apple: Apple\nOrange: Orange\nBanana:"
source_inputs, target_inputs = prepare(source_text), prepare(target_text)
source_position = source_inputs.kwargs["input_ids"].shape[1] - 1
target_position = target_inputs.kwargs["input_ids"].shape[1] - 1
layers = [0, model.config.n_layer // 2, model.config.n_layer - 1]
scope = probe.lens.patchscope(layers=layers, source_position=source_position,
                              target_layer=0, target_position=target_position)
result = scope.run(source_inputs, target_inputs=target_inputs)
print("teacher-forced logits [source layer, batch, target position, vocabulary]:", result.tensors["logits"].shape)
# Last target-position logits measure one next-token readout, not generated text.
paris_ids = tokenizer.encode(" Paris", add_special_tokens=False)
assert len(paris_ids) == 1
logits = result.tensors["logits"][:, 0, -1:, :]
for layer, row in zip(layers, logits[:, 0]):
    print(layer, "top next subword:", repr(tokenizer.decode([int(row.argmax())])))
ax = plot_lens_heatmap(logits, target_token_id=paris_ids[0], layer_labels=layers,
                       token_labels=["Target prompt end"], tokenizer=tokenizer,
                       title="Patchscope: next-subword rank after residual replacement")
ax.figure.savefig(OUT / "patchscope.png", dpi=160, bbox_inches="tight")
plt.show()
