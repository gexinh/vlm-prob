from pathlib import Path
import os
import torch
from transformers import AutoModelForImageTextToText, AutoProcessor
from vlmprobe import Prober
from vlmprobe import visualization as viz
import matplotlib.pyplot as plt

# Install: pip install "vlmprobe[transformers,visualization]"
model_id = os.environ.get("VLM_PROBING_MODEL", "HuggingFaceTB/SmolVLM-500M-Instruct")
device = os.environ.get("VLM_PROBING_DEVICE", "cuda:0" if torch.cuda.is_available() else "cpu")
model = AutoModelForImageTextToText.from_pretrained(
    model_id, dtype=torch.float32, attn_implementation="eager",
).to(device).eval()
processor = AutoProcessor.from_pretrained(model_id)
probe = Prober(model, processor)
prompt = "The capital of France is"
inputs = probe.prepare(prompt=prompt, device=device)  # This VLM also accepts text-only inputs.
capability = probe.describe()["methods"]["attention.head_logits"]
assert capability["available"], capability["missing"]
layer = capability["sites"][-1]
result = probe.attention.head_logits(layers=[layer]).run(inputs)
print("Head logits [L,B,H,T,V]:", result.tensors["head_logits"].shape)
last_position = int(inputs.kwargs["attention_mask"][0].nonzero()[-1])
# Show each head's top direct vocabulary contributions at one prediction row.
head_scores = result.tensors["head_logits"][0, 0, :, last_position, :]
for head, scores in enumerate(head_scores):
    token_ids = scores.topk(3).indices.tolist()
    print(head, [(processor.tokenizer.decode([i]), float(scores[i])) for i in token_ids])
with torch.no_grad():
    target_id = int(model(**inputs.kwargs).logits[0, last_position].argmax())
curves = {"Fixed next-token contribution": {
    "x": list(range(head_scores.shape[0])), "y": head_scores[:, target_id].numpy(),
}}
ax = viz.plot_intervention_curves(curves, baseline=0, xlabel="Attention head",
    ylabel="Direct logit contribution (fixed final RMSNorm scale)",
    title=f"Layer {layer}: {processor.tokenizer.decode([target_id])!r}")
# Only the plot function is reused: these are observational contributions, not interventions.
output_dir = Path(os.environ.get("VLM_PROBING_OUTPUT", "outputs/attention-head-logits"))
output_dir.mkdir(parents=True, exist_ok=True)
result.save(output_dir / "head-logits")
ax.figure.savefig(output_dir / "attention-head-logits.png", dpi=160, bbox_inches="tight")
plt.show()
