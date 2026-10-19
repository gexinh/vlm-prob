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


# 3. Execute independent sender-to-receiver paths
# A short scan: all heads in the first, middle, and last decoder layer.
# Other layers are genuinely unmeasured and remain gray in the plot.
available = sorted(probe.spec.path_heads)
selected_layers = sorted({available[0], available[len(available) // 2], available[-1]})
senders = [(layer, head) for layer in selected_layers
           for head in range(probe.spec.path_heads[layer].heads)]
method = probe.causal.path(
    senders=senders, receivers="residual", sender_tokens="last_prompt",
    donor_tokens="last_prompt", receiver_tokens="last_prompt",
)
result = method.sweep(inputs, donor=reference, metric=metric, alignment="position")
print("Baseline margin:", result.tensors["baseline_score"])
print("Reference margin:", result.tensors["donor_score"])
print("Measured effects [sender,batch]:", result.tensors["effect"].shape)
print("Actual forward passes:", result.metadata["actual_forward_passes"])
result.save(output_dir / "path_patching")
# A no-change control executes the same four-stage intervention with identical inputs.
identity = probe.causal.path(senders=[senders[0]], receivers="residual").run(
    inputs, donor=inputs, metric=metric,
)
print("Identity-donor effect (should be near zero):", identity.tensors["effect"])


# 4. Plot actual coordinates and inspect the sign
ax = plot_causal_heatmap(
    result, layer_labels=available,
    column_labels=list(range(model.config.n_head)),
    title="Independent head-to-final-residual path interventions",
    value_label="Measured Amy-minus-Laura margin change", highlight_count=3,
)
ax.figure.set_size_inches(8, 5)
ax.figure.savefig(output_dir / "causal-path-patching.png", dpi=150, bbox_inches="tight")
plt.show()


# 5. Optional: change the receiver, keeping the public input contract
# Optional receiver-specific experiment: one early sender to a later physical V head.
# This runs four fresh forwards; it is not an attribution graph or a new training step.
receiver_result = probe.causal.path(
    senders=[(available[0], 0)], receivers=[(available[-1], 0, "v")],
    sender_tokens="last_prompt", receiver_tokens="last_prompt",
).run(inputs, donor=reference, metric=metric, alignment="position")
print("Sender -> receiver V-head effect:", receiver_result.tensors["effect"])
