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


# 3. Integrate gradients along input embeddings
# Choose the original input-embedding-path algorithm explicitly.
method = probe.causal.eap_ig(graph="transformer", steps=5, quadrature="left")
attribution = method.run(inputs, donor=reference, metric=metric, alignment="position")
print("Graph edges:", len(method.graph.edge_names))
print("EAP-IG scores:", attribution.tensors["edge_scores"].shape)
print("EAP scores:", attribution.tensors["eap_scores"].shape)
print("Clean / reference margins:", attribution.tensors["baseline_score"],
      attribution.tensors["donor_score"])
attribution.save(output_dir / "eap_ig")


# 4. Evaluate ranked circuits and actual single-edge replacements
# Every plotted circuit value comes from a fresh forward intervention.
# Use separate attribution/evaluation pairs for a generalization experiment.
budgets = [0, 100, 1000, len(method.graph.edge_names)]
evaluation = method.evaluate(
    inputs, donor=reference, metric=metric, attribution=attribution,
    budgets=budgets, rankings=("eap", "eap_ig"), strategy="greedy",
    alignment="position", epsilon=1e-6,
)
print("Eligible nonzero denominator:", evaluation.tensors["eligible"])
print("All-retained endpoint error:", evaluation.tensors["all_retained_error"])
print("None-retained endpoint error:", evaluation.tensors["none_retained_error"])
evaluation.save(output_dir / "eap_ig_faithfulness")
# Corrupt three high-scoring edges individually and compare to the estimate.
edge_ids = attribution.tensors["edge_scores"].abs().topk(3).indices.tolist()
exact_edges = method.patch_edges(inputs, donor=reference, metric=metric,
                                 excluded_edges=edge_ids, alignment="position")
for row, edge in enumerate(edge_ids):
    print(method.graph.edge_names[edge],
          "estimated loss increase:", float(attribution.tensors["edge_scores"][edge]),
          "actual loss increase:", float(exact_edges.tensors["loss_increase"][row, 0]))


# 5. Draw newly measured circuit curves and estimated connections
from vlmprobe.visualization import plot_connections

fig, axes = plt.subplots(1, 2, figsize=(16, 4.8), constrained_layout=True,
                         gridspec_kw={"width_ratios": [1, 1.4]})
curves = {}
for index, name in enumerate(evaluation.metadata["rankings"]):
    # Never plot a zero placeholder from an ineligible denominator as a failure.
    values = evaluation.tensors["faithfulness"][index, :, 0].clone()
    if not bool(evaluation.tensors["eligible"][0]):
        values[:] = float("nan")
    curves[name.upper().replace("_", "-")] = {
        "x": evaluation.tensors["retained_edges"][index], "y": values,
    }
if bool(evaluation.tensors["eligible"][0]):
    plot_intervention_curves(
        curves, ax=axes[0], baseline=1.0, xlabel="Actual retained edges",
        ylabel="Recovered clean-vs-reference margin", title="Circuit intervention, not a score sum",
    )
    axes[0].set_xscale("symlog", linthresh=100)
    axes[0].set_xlim(0, len(method.graph.edge_names))
else:
    axes[0].text(.5, .5, "Clean/reference margin too similar to normalize", ha="center")
    axes[0].set_axis_off()
# The graph draws only supplied high-scoring edges; it does not discover roles.
indices = attribution.tensors["edge_scores"].abs().topk(8).indices.tolist()
edges = []
for index in indices:
    u, v = method.graph.edge_indices[index].tolist()
    edges.append((method.graph.source_names[u], method.graph.destination_names[v],
                  float(attribution.tensors["edge_scores"][index])))
nodes = {node for source, receiver, _ in edges for node in (source, receiver)}
def layer_coordinate(node):
    if node == "input": return -1
    if node == "readout": return model.config.n_layer
    return int(node.split(".")[0][1:])
plot_connections(edges, node_layers={node: layer_coordinate(node) for node in nodes},
                 top_k=8, ax=axes[1], title="Candidate edges ranked by EAP-IG",
                 value_label="Estimated corrupted-edge loss increase")
for label in axes[1].texts:
    label.set_fontsize(7)
fig.savefig(output_dir / "causal-eap-ig.png", dpi=150, bbox_inches="tight")
plt.show()
