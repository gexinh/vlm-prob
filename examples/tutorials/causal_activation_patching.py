"""Live tutorial: run after installing vlmprobe[transformers,visualization]."""
# 1. Install and load a native model
import os
from pathlib import Path
import torch
import matplotlib.pyplot as plt
from transformers import AutoTokenizer, GPT2LMHeadModel
from vlmprobe import Prober, TokenMargin
from vlmprobe.visualization import plot_causal_heatmap, plot_intervention_curves

# First run downloads GPT-2 (~0.5 GB). Use an existing local checkpoint if desired.
model_id = os.environ.get("VLM_PROBING_MODEL", "openai-community/gpt2")
device = os.environ.get("VLM_PROBING_DEVICE", "cuda:0" if torch.cuda.is_available() else "cpu")
model = GPT2LMHeadModel.from_pretrained(model_id, attn_implementation="eager").to(device).eval()
tokenizer = AutoTokenizer.from_pretrained(model_id)
probe = Prober(model, processor=tokenizer)
print({name: info for name, info in probe.describe()["methods"].items()
       if name.startswith("causal.")})
output_dir = Path(os.environ.get("VLM_PROBING_OUTPUT", "outputs/tutorials/causal"))
output_dir.mkdir(parents=True, exist_ok=True)


# 2. Construct raw prompts, aligned inputs, and a one-token answer metric
# An explicit author-published IOI pair (row 826); no result snapshots are used.
# Source: hannamw/eap-ig-faithfulness, data/ioi/gpt2.csv; see docs/REFERENCES.md.
clean_prompt = "When Amy and Laura got a snack at the house, Laura decided to give it to"
reference_prompt = "When Amy and Laura got a snack at the house, Nicholas decided to give it to"

def prepare_text(text):
    # The authors prepend GPT-2's BOS token. Keep the convention explicit.
    ids = [tokenizer.bos_token_id, *tokenizer.encode(text, add_special_tokens=False)]
    input_ids = torch.tensor([ids], device=device)
    return {"input_ids": input_ids, "attention_mask": torch.ones_like(input_ids)}

inputs = prepare_text(clean_prompt)
reference = prepare_text(reference_prompt)
assert inputs["input_ids"].shape == reference["input_ids"].shape, "Pair token lengths must match"
positive_ids = tokenizer.encode(" Amy", add_special_tokens=False)
negative_ids = tokenizer.encode(" Laura", add_special_tokens=False)
assert len(positive_ids) == len(negative_ids) == 1, "TokenMargin requires one-token candidates"
metric = TokenMargin(positive=positive_ids[0], negative=negative_ids[0])
print("Clean:", clean_prompt)
print("Reference:", reference_prompt)
print("Candidates:", tokenizer.decode(positive_ids), tokenizer.decode(negative_ids))
# Check the role alignment, not just the equal length.
for position, (a, b) in enumerate(zip(inputs["input_ids"][0], reference["input_ids"][0])):
    print(position, repr(tokenizer.decode([a.item()])), repr(tokenizer.decode([b.item()])))


# 3. Run measured and first-order patching on identical coordinates
layers = sorted(probe.spec.residuals)
# Both methods replace/estimate the same reference-minus-clean change.
# This is corruption of the clean input, not restoration of the reference.
exact = probe.causal.patch(layers=layers, tokens="last_prompt").run(
    inputs, source=reference, metric=metric, alignment="position",
)
estimated = probe.causal.attribute(layers=layers, tokens="last_prompt").run(
    inputs, source=reference, metric=metric, alignment="position",
)
print("Exact effect [layer,batch]:", exact.tensors["effect"])
print("Estimated effect [layer]:", estimated.tensors["estimated_effect"])
# A separate all-position attribution scan supplies the token heatmap.
token_map = probe.causal.attribute(layers=layers, tokens="all").run(
    inputs, source=reference, metric=metric, alignment="position",
)
print("Token scores [layer,batch,token]:", token_map.tensors["token_scores"].shape)
exact.save(output_dir / "activation_patching")
estimated.save(output_dir / "attribution_patching")
token_map.save(output_dir / "attribution_patching_all_positions")


# 4. Visualize newly computed outputs with the library
fig, axes = plt.subplots(1, 2, figsize=(14, 4.8), constrained_layout=True)
plot_intervention_curves(
    {"Measured patch": exact.tensors["effect"][:, 0],
     "First-order estimate": estimated.tensors["estimated_effect"]},
    x=layers, ax=axes[0], xlabel="Decoder layer", ylabel="Change in Amy-minus-Laura logit margin",
    title="The approximation can differ from the measured effect",
)
labels = ["<BOS>" if i == 0 else tokenizer.decode([token])
          for i, token in enumerate(inputs["input_ids"][0].tolist())]
plot_causal_heatmap(
    token_map, tensor="token_scores", column_labels=labels, ax=axes[1],
    title="Separate attribution scan across all positions",
    value_label="Estimated margin change",
)
axes[1].tick_params(axis="x", labelsize=7)
fig.savefig(output_dir / "causal-patching.png", dpi=150, bbox_inches="tight")
plt.show()
