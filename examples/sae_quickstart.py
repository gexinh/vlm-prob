"""CPU image-to-SAE workflow; random ViT features are not named concepts."""
import argparse
import hashlib
import json
from pathlib import Path
import tempfile

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image
import torch
from vlmprobe import Prober, visualization as viz
from vlmprobe.sae import SAEConfig, SparseAutoencoder, build_sae_binding
from vlmprobe.sae.training import train_sae
from vlmprobe.sae.backends import prisma
from vlmprobe.sae.backends.prisma import HookedViT, HookedViTConfig

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--output-dir", type=Path, default=Path("runs/readme_sae_quickstart"))
base = parser.parse_args().output_dir
base.mkdir(parents=True, exist_ok=True)
output = Path(tempfile.mkdtemp(prefix="run-", dir=base))  # Every run is fresh.
torch.manual_seed(42)
torch.set_num_threads(1)
model = HookedViT(HookedViTConfig(
    n_layers=2, d_model=16, d_head=4, d_mlp=32, n_heads=4, n_channels=3,
    patch_size=8, image_size=32, device="cpu", model_name="tiny-image-demo",
    return_type="pre_logits",
)).eval().requires_grad_(False)
# Independent image splits; these exact RGB tensors are the model inputs.
def images(seed, count):
    generator = torch.Generator().manual_seed(seed)
    pixels = torch.randint(0, 64, (count, 3, 32, 32), generator=generator)
    pixels[:, :, 8:24, 8:24] += torch.randint(64, 192, (count, 3, 1, 1), generator=generator)
    return pixels.float() / 255
train_images, validation_images, test_images = images(11, 32), images(22, 8), images(33, 2)
digest = hashlib.sha256()
for name, value in sorted(model.state_dict().items()):
    digest.update(name.encode() + value.detach().numpy().tobytes())
model_id = "tiny-image-demo@" + digest.hexdigest()
probe = Prober(model, adapter=prisma.make_model_adapter(model, model_id=model_id, layers=[1]))
binding = build_sae_binding(probe, 1, model_id=model_id, tokenizer_id="none:vision-only",
    preprocessing_id="RGB32-unit-interval-patch8", calibration_id="independent-image-seeds11-22")
@torch.no_grad()
def capture(batch):
    site = binding["site"]
    hidden = probe.adapter.run({"input": batch}, capture=[site]).activations[site]
    return hidden[:, 1:].flatten(0, 1).detach()  # Exclude CLS; keep spatial patches.
train_vectors, validation_vectors = capture(train_images), capture(validation_images)
# Fourfold dictionary expansion; TopK keeps at most four active features per patch.
sae = SparseAutoencoder(SAEConfig(architecture="topk", d_in=16, d_sae=64, k=4, seed=42), binding=binding)
history = train_sae(sae, list(train_vectors.split(64)), list(validation_vectors.split(64)),
    output / "sae", epochs=8, lr=1e-3, patience=4, seed=42,
    provenance={"train_image_ids": list(range(32)), "validation_image_ids": list(range(32, 40))})
sae = SparseAutoencoder.load(history["checkpoint"], expected_binding=binding)
common = dict(layer=1, sae=sae, binding=binding, tokens="visual")
inputs = {"input": test_images}
features = probe.sae.features(**common).run(inputs)
profile = probe.sae.profile(**common, top_k=3).run(inputs)
reconstruction = probe.sae.reconstruct(**common).run(inputs)
feature_id = int(sae.encode(validation_vectors).detach().abs().mean(0).argmax())
edited = probe.sae.edit(**common, feature_ids=[feature_id], scale=0).run(inputs)
for name, result in {"features": features, "profile": profile,
                     "reconstruction": reconstruction, "ablation": edited}.items():
    result.save(output / name)
image = Image.fromarray((test_images[0].permute(1, 2, 0) * 255).round().byte().numpy())
figure, axes = plt.subplots(1, 2, figsize=(10, 4))
viz.plot_sae_feature_overlay(image, features, feature_id=feature_id, grid_shape=(4, 4),
    image_alpha=.2, alpha=1., ax=axes[0])
viz.plot_sae_activity(features, top_k=12, ax=axes[1])
figure.suptitle("Random ViT workflow demonstration: feature IDs are not named concepts")
figure.savefig(output / "sae_visualization.png", dpi=160, bbox_inches="tight")
plt.close(figure)
summary = {"features_shape": list(features.tensors["features"].shape),
    "positions_shape": list(features.tensors["positions"].shape), "selected_feature": feature_id,
    "best_validation_loss": history["best_validation_loss"], "output": str(output)}
(output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps(summary, indent=2))
