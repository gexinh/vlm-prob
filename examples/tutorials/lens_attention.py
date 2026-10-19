"""Live pretrained GPT-2 tutorial; see docs/methods. No result cache is loaded."""
import hashlib
import json
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

# Disjoint strings illustrate the protocol; this tiny split is not a quality benchmark.
train_texts = [
    "The child opened a book and began to read.",
    "A red boat crossed the lake before sunset.",
    "The baker placed fresh bread beside the window.",
    "Two friends walked through a quiet garden.",
]
validation_texts = [
    "A musician carried a violin onto the stage.",
    "The train arrived at the station after midnight.",
]
assert not (set(train_texts) & set(validation_texts))
assert prompt not in train_texts + validation_texts
train_inputs = [prepare(text) for text in train_texts]
validation_inputs = [prepare(text) for text in validation_texts]
split_hash = hashlib.sha256(json.dumps([train_texts, validation_texts]).encode()).hexdigest()
binding = {
    "model_id": MODEL_ID + "@" + str(getattr(model.config, "_commit_hash", None) or "local-checkpoint"),
    "tokenizer_id": tokenizer.name_or_path,
    "readout_id": "transformer.ln_f+lm_head",
    "calibration_id": "tutorial-distinct-texts-sha256:" + split_hash,
}
# For a release, pin the model/tokenizer revision and hash the local checkpoint
# if config._commit_hash is unavailable. This binding is caller-declared identity.

# GPT-2: 12 * 768 * 50,257 = 463,168,512 decoder weights per layer.
# Adam/gradients need several times the weight memory; prefer a GPU with ample RAM.
layer = int(os.environ.get("VLM_PROBING_ATTENTION_LAYER", "7"))
assert layer in probe.describe()["methods"]["lens.attention"]["sites"]
lens = probe.lens.attention(layers=[layer], tokens="last_prompt", binding=binding)
head = model.get_output_embeddings()
lens.fit_batches(train_inputs, validation_inputs, OUT / "attention-artifact",
                 initial_unembedding=head.weight, initial_bias=getattr(head, "bias", None),
                 batch_size=4, epochs=2, lr=1e-4, patience=2, seed=0,
                 resume=False)
result = lens.run(inputs)
print("head logits [layer, packed position, head, vocabulary]:", result.tensors["head_logits"].shape)
print("summed logits:", result.tensors["logits"].shape)
# Put the measured heads on rows; this is not a layer axis.
head_logits = result.tensors["head_logits"][0].permute(1, 0, 2)
fig, ax = plt.subplots(figsize=(7, 5), layout="constrained")
ax = plot_lens_heatmap(head_logits, ax=ax, target_token_id=answer_id,
                       layer_labels=[f"Head {i}" for i in range(head_logits.shape[0])],
                       token_labels=["Final prompt position"], tokenizer=tokenizer,
                       title=f"Attention Lens: GPT-2 layer {layer}")
ax.set_ylabel("Attention head")
ax.tick_params(axis="y", labelsize=9)
ax.tick_params(axis="x", labelrotation=0)
ax.set_xlabel("")
ax.figure.savefig(OUT / "attention.png", dpi=160, bbox_inches="tight")
plt.show()
print("best held-out KL:", lens.training_history[layer]["best_validation_kl"])
restored = probe.lens.attention(layers=[layer], binding=binding).load(OUT / "attention-artifact")
