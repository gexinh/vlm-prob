# ViT-Prisma: native vision dictionaries and training

[ViT-Prisma](https://github.com/Prisma-Multimodal/ViT-Prisma) provides HookedViT
models, pretrained CLIP/DINO dictionaries, image activation stores and SAE
training/evaluation. This library maintains a selected, pinned copy of its
MIT-licensed `StandardSparseAutoencoder`, `GatedSparseAutoencoder`, normalization
and image-transformer forward core. It preserves their objectives and TopK
operation instead of converting their weights into different SAE kernels.
Installing or importing the official `vit_prisma` package is unnecessary.

## Installation

```bash
python -m venv .venv-prisma
source .venv-prisma/bin/activate
pip install -e '.[sae,visualization]'
```

Run these commands from the development checkout; these additions have not
been released on PyPI. Only generic tensor/plot dependencies are needed.
The selected implementation comes from ViT-Prisma 2.0 source revision
`64daf1425f7e5311844213fd0fb6f4127a30cd16` and remains fixed until deliberately
updated here. The internal `SOURCE.json` records upstream file hashes, local
file hashes and modifications, and the accompanying `LICENSE` retains the MIT
copyright notice. Remote backbone conversion, the full image trainer, dataset
loaders and text/video models are outside this selected copy.

## Pretrained discovery and loading

```python
from vlmprobe.sae import list_pretrained

rows = list_pretrained("prisma", model="CLIP", query="hook_resid_post")
print(rows[0])
```

The snapshot records the official CLIP all-patch, CLS-only, spatial-only,
TopK and DINO releases. The linked upstream table also contains **transcoders**,
which map different input/output representations; they are identified in the
catalog and are not accepted as same-hook SAEs.

Every pretrained dictionary belongs to an exact native model, hook and
preprocessing contract. `HookedViT` residuals can differ from raw Hugging Face
or OpenCLIP residuals because of weight processing such as layer-norm folding
and centering. A matching hidden width does not establish compatibility.
The selected vision core does not download or convert pretrained backbones.
For a released dictionary, supply verified native HookedViT weights/config and
the matching preprocessing; do not attach it to an unrelated encoder. Safe
dictionary loading and its vector-level checks do not imply an end-to-end
backbone conversion has been verified.

```python
from vlmprobe.sae.backends import prisma

starter = prisma.list_pretrained()[0]
print(starter["release"], starter["revision"], starter["hook"])

# Supply a binding constructed from the matching native HookedViT adapter;
# the complete executable example below shows how to construct that binding.
sae = prisma.load(
    release=starter["release"], revision=starter["revision"],
    sae_id=starter["sae_id"], binding=binding, device="cpu",
)
```

The starter is the authors' recommended CLIP-B/32 layer-11 post-residual,
all-patch ReLU SAE: `d_in=768`, `d_sae=49152`, 224-pixel input and 50 tokens
(CLS plus 49 spatial patches). Its separate `config.json` and `weights.pt`
were loaded and encoded/decoded on CPU. This checks the checkpoint numerics;
it does not constitute a reproduction of the authors' downstream scores.

`load` accepts either `release` and an immutable 40-character Hub `revision`,
or `weights_path` and an optional `config_path` (defaults to the adjacent
`config.json`). `sae_id`/`filename` selects the actual weight filename.
`device="cpu"`, `dtype=torch.float32`, `expected_binding` and
`local_files_only=False` are optional. The checkpoint loader uses
`torch.load(weights_only=True)` and never enables unrestricted pickle loading.
Some early upstream `n_images_*.pt` files contain pickled configuration
objects; these are listed for discovery but require an explicitly reviewed
conversion into tensor-only weights and JSON configuration. An already-loaded
trusted native dictionary can also be passed to `prisma.wrap`.

## Complete CPU image-to-training-to-visualization example

This example needs no downloaded backbone or dataset. It constructs a tiny
native HookedViT, freezes it, extracts native activations from independent
synthetic image splits, trains a real Prisma SAE, reloads it and overlays a
held-out feature using the library's visualization tools. It validates the
workflow; random-backbone features should not be interpreted as named visual
concepts. Replace the tiny backbone and synthetic images with a matching
pretrained HookedViT and your own correctly preprocessed images for research.

```python
from pathlib import Path
import hashlib
import torch
import matplotlib.pyplot as plt
from PIL import Image

from vlmprobe import Prober, visualization as viz
from vlmprobe.sae import build_sae_binding
from vlmprobe.sae.backends import prisma
from vlmprobe.sae.backends.prisma import (
    HookedViT, HookedViTConfig, VisionModelSAERunnerConfig,
)

torch.manual_seed(42)
torch.set_num_threads(1)
output = Path("outputs/prisma_cpu_v3")
output.mkdir(parents=True, exist_ok=True)

model = HookedViT(HookedViTConfig(
    n_layers=2, d_model=16, d_head=4, d_mlp=32, n_heads=4,
    n_channels=3, patch_size=8, image_size=32, device="cpu",
    model_name="tiny-prisma-image-demo", return_type="pre_logits",
))
model.eval().requires_grad_(False)

# These are the exact processed RGB tensors used by the model: no hidden crop
# or resize occurs. A real checkpoint requires its own upstream transform.
generator = torch.Generator().manual_seed(123)
train_images = torch.rand(32, 3, 32, 32, generator=generator)
validation_images = torch.rand(8, 3, 32, 32, generator=generator)
test_images = torch.rand(2, 3, 32, 32, generator=generator)

digest = hashlib.sha256()
for name, tensor in sorted(model.state_dict().items()):
    digest.update(name.encode())
    digest.update(tensor.detach().cpu().contiguous().numpy().tobytes())
model_id = "tiny-prisma-image-demo@" + digest.hexdigest()

adapter = prisma.make_model_adapter(model, model_id=model_id, layers=[1])
probe = Prober(model, adapter=adapter)
binding = build_sae_binding(
    probe, 1, model_id=model_id,
    tokenizer_id="not-applicable:vision-only",
    preprocessing_id="identity-RGB-unit-interval-32x32-v1",
    calibration_id="synthetic-disjoint-splits-generator123-v1",
)
binding.update(
    backend_model_name="tiny-prisma-image-demo",
    backend_hook_name="blocks.1.hook_resid_post",
)

config = VisionModelSAERunnerConfig(
    _device="cpu", d_in=16, expansion_factor=4,
    model_name="tiny-prisma-image-demo", hook_point_layer=1,
    layer_subtype="hook_resid_post", architecture="standard",
    activation_fn_str="relu", activation_fn_kwargs={},
    normalize_activations=None, l1_coefficient=1e-3,
    context_size=17, image_size=32, log_to_wandb=False,
)
report = prisma.train(
    config=config, model=model, input_kind="images",
    dataset=train_images, eval_dataset=validation_images,
    output_dir=output / "sae", binding=binding,
    epochs=5, batch_size=32, lr=1e-3, patience=3, seed=42,
    train_ids=["independent-training-images"],
    eval_ids=["independent-validation-images"],
)
print(report["best_validation_objective"])

sae = prisma.load(weights_path=report["checkpoint"], binding=binding)
result = probe.sae.features(
    layer=1, sae=sae, binding=binding, tokens="visual",
).run({"input": test_images})
print(result.tensors["features"].shape)  # [2 * 16 spatial patches, 64 features]
print(result.tensors["positions"].shape)  # [32, 2]: batch index, native token index
result.save(output / "held_out_features")

feature_id = int(result.tensors["features"].abs().mean(0).argmax())
image = Image.fromarray((test_images[0].permute(1, 2, 0).numpy() * 255).astype("uint8"))
ax = viz.plot_sae_feature_overlay(
    image, result, feature_id=feature_id, batch_index=0,
    grid_shape=(4, 4), image_alpha=0.2, alpha=1.0,
)
ax.figure.savefig(output / "feature_overlay.png", dpi=180, bbox_inches="tight")
plt.close(ax.figure)

# A feature intervention changes the native representation. No class/vocabulary
# logits are fabricated for a model that returns an embedding.
edited = probe.sae.edit(
    layer=1, sae=sae, binding=binding, tokens="visual",
    feature_ids=[feature_id], scale=0.0, mode="error_preserving",
).run({"input": test_images})
print(edited.tensors["baseline_output"].shape)
print(edited.tensors["edited_output"].shape)
edited.save(output / "feature_ablation")
```

`make_model_adapter` also accepts `layer_subtype="hook_mlp_out"` for native
MLP-output dictionaries. The artifact binding records `native_mlp_output`
separately from `native_residual_output`. `layers` selects the native block
indices. The default output kind is `representation`; explicitly choose
`output_kind="classification"` only for a genuine classifier output. The
adapter exposes only verified native hooks and the exact configured image grid;
visual selection excludes CLS.

## Architectures and parameters

| Parameter | Meaning |
|---|---|
| `architecture` | Native `standard`/`vanilla` or `gated`; same-hook transcoders are rejected. |
| `d_in` | Exact activation width of the bound native hook. |
| `expansion_factor` | Dictionary width is `d_sae = d_in * expansion_factor`. |
| `activation_fn_str` | Native `relu` or `topk`. TopK requires explicit `activation_fn_kwargs={"k": ...}`. |
| `normalize_activations` | Explicit `None`/`"none"`, `"layer_norm"` or `"constant_norm_rescale"`; unknown modes are rejected. |
| `model_name`, `hook_point_layer`, `layer_subtype` | Exact source model and native hook identity, checked against the artifact binding. |
| `cls_token_only`, `use_patches_only` | Native image token scope; these options are mutually exclusive. |
| `l1_coefficient`, `lp_norm` | Native feature sparsity penalty; standard TopK omits its L1 term. |
| `use_ghost_grads` | Upstream ghost-gradient option. The activation bridge does not supply a dead-feature mask, so the ghost path is inactive. |
| `max_grad_norm` | Native-config gradient clipping used by the bridge. |

Gated SAE retains the native gating/magnitude parameters and native auxiliary
reconstruction objective. This bridge does not assert that every upstream
objective matches every later SAE paper revision.

`train` takes native configuration as a `VisionModelSAERunnerConfig` or an
explicit equivalent dictionary. `input_kind="activations"` accepts finite
`[positions, d_in]` training and validation tensors. `input_kind="images"`
captures the configured native hook from already preprocessed BCHW tensors
using the supplied model. The default training wrapper preserves the upstream
SAE forward objective, uses Adam and per-epoch held-out validation, and saves
the best tensor-only weights. It does not use the upstream ImageNet-size
schedule. At least two activation rows per split are required because the
native reconstruction objective uses batch-centered normalization.

This activation bridge uses the native dictionary constructor's initialization.
It does not run the image trainer's `b_dec_init_method` mean/geometric-median
initialization routine. The broad image runner is outside the selected copy.

| Training option | Default and meaning |
|---|---|
| `epochs` | `10`, maximum completed training epochs. |
| `batch_size` | `256`, activation rows per update; a final singleton is merged into the preceding batch. |
| `lr` | `None`, uses `config.lr`; an explicit positive value overrides it. |
| `patience` | `5`, consecutive non-improving validation epochs before stopping. |
| `seed` | `0`, isolated initialization and deterministic per-epoch shuffling. |
| `device`, `dtype` | `"cpu"`, `torch.float32`; config construction uses the requested device explicitly. |
| `resume` | `True`, restores weights, Adam state and completed epoch from `training_state.pt`; different data/config/binding is rejected. |
| `train_ids`, `eval_ids` | Optional source identifiers; when supplied, overlap is rejected and provenance records that check. Split tensors alone cannot establish patient/slide independence. |

Artifacts include `config.json`, `binding.json`, `protocol.json`, `weights.pt`,
`training_state.pt`, `history.json` and `report.json`. Preprocessing, model
identity and calibration split belong in the saved binding. Calibration and
training must be separate from your final evaluation data.

The broad upstream `VisionSAETrainer` is not included. Its audited configuration
hardcodes 1,300,000 images per epoch when deriving its schedule. This library
uses its own bounded activation/image training loop with the selected native
SAE objectives; `native_runner=True` raises an explicit unsupported error.
Dead-feature and ghost-gradient schedules are not part of this maintained
training protocol.

## Normalization and feature interventions

Native Prisma `encode` returns `(normalized_centered_input, features)`, not a
feature tensor alone. The adapter returns features and retains the native
decode operation. For per-input normalization it exposes an explicit context:

```python
features, context = sae.encode_with_context(raw_activations)
baseline = sae.decode_with_context(features, context)
changed = features.clone()
changed[:, feature_id] = 0
ablated = sae.decode_with_context(changed, context)
replacement = raw_activations + (ablated - baseline)
```

This preserves each input's mean/std or norm-rescaling coefficient across
interleaved inputs and repeated decodes. The public `probe.sae` methods use
this protocol automatically. Plain `encode`/`decode` preserve upstream's
single-chain behavior and should not be interleaved for stateful
normalization. Feature IDs are learned coordinates requiring empirical
interpretation; reconstruction and visual overlays alone do not establish a
named concept or causal relevance.

## Sources and licenses

The integration includes selected upstream source under
`src/vlm_probing/_vendor/prisma`; that directory's `SOURCE.json` describes
the selection and local modifications. ViT-Prisma code is MIT licensed.
Checkpoint licenses remain those of their
authors; the verified starter model card specifies Apache-2.0. See the
[official checkpoint table](https://github.com/Prisma-Multimodal/ViT-Prisma/blob/main/docs/sae_table.md),
[configuration](https://github.com/Prisma-Multimodal/ViT-Prisma/blob/main/src/vit_prisma/sae/config.py),
[native SAE classes](https://github.com/Prisma-Multimodal/ViT-Prisma/blob/main/src/vit_prisma/sae/sae.py)
and [training runner](https://github.com/Prisma-Multimodal/ViT-Prisma/blob/main/src/vit_prisma/sae/train_sae.py).
