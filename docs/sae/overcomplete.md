# Overcomplete: vision dictionary learning through the same probing interface

[Overcomplete](https://github.com/KempnerInstitute/overcomplete) provides sparse
autoencoders and other dictionary-learning algorithms for vision activations.
VLMProbe uses its actual Python implementations; it does not copy their source
or rename NMF, PCA or ICA as sparse autoencoders. The same pointwise adapter also
accepts language and multimodal residual vectors with a verified model binding.

## Installation and compatibility

```bash
python -m venv .venv-overcomplete
source .venv-overcomplete/bin/activate
pip install -e '.[overcomplete,visualization]'
```

Run these commands from the development checkout; these additions have not
been released on PyPI. The bridge is audited against
Overcomplete **0.3.x**. Upstream requires Python below 3.13. Overcomplete 0.3 imports
`matplotlib.cm.get_cmap`, which was removed in Matplotlib 3.9; its optional extra
therefore selects Matplotlib 3.8.x. Use a separate environment if another
application requires newer Matplotlib. No optional backend imports at
`import vlmprobe` time.

## Architectures and native parameters

```python
from vlmprobe.sae.backends import overcomplete

sae = overcomplete.create(
    "topk", d_in=768, d_sae=3072, binding=binding,
    top_k=32, encoder_module="linear", device="cpu",
)
```

| Architecture | Native class | Native parameters and interpretation |
|---|---|---|
| `relu` | `SAE` | ReLU encoder; training defaults to the native `mse_l1` objective. |
| `topk` | `TopKSAE` | `top_k`: retained nonnegative features per activation vector. |
| `batchtopk` | `BatchTopKSAE` | `top_k`: **global number** of retained activations across the native training batch; `threshold_momentum=0.9`. Evaluation uses its saved running threshold. |
| `jumprelu` | `JumpSAE` | `kernel="silverman"`, `bandwidth=1e-3`; learns positive thresholds with the native surrogate gradient. |
| `archetypal_topk` | `RATopKSAE` | `points`: candidate vectors from training activations only; `top_k`, `delta=1.0`, `use_multiplier=True`. |
| `archetypal_jumprelu` | `RAJumpSAE` | Training-only `points`, `bandwidth=1e-3`, `delta=1.0`, `use_multiplier=True`. |

All architectures take `d_in`, `d_sae`, `binding` and `device`. The named
pointwise encoders are `linear`, `mlp_ln_1`, `mlp_ln_3`, `mlp_bn_1` and
`mlp_bn_3`. Their input is `[positions, hidden]`; evaluation-mode BatchNorm
statistics are preserved. Native `dictionary_params` controls dictionary
normalization and its optional learned multiplier. The archetypal dictionary
uses its own constraints instead. Additional keyword arguments go directly to
the native constructor, so an unsupported argument raises an error.

Attention and convolutional encoders are **not** flattened into independent
tokens: their original geometry matters. The bridge rejects those encoders.
Upstream experimental QSAE, matching pursuit and orthogonal matching pursuit are
outside the initial supported bridge.

The optional `input_mean` and `input_scale` are explicit scalars or `[d_in]`
vectors; they default to zero and one. The bridge computes
`u = (raw - input_mean) / input_scale` and returns raw-space reconstructions as
`decode(z) = native_decode(z) * input_scale + input_mean`. It does not fit or
guess normalization. Estimate these quantities on the **training split only**
if your selected upstream recipe requires standardization.

## Training on your own activations

The following standalone CPU example trains on synthetic activation vectors,
evaluates an independent validation set, reloads the portable dictionary and
plots held-out features. This validates the workflow rather than demonstrating
semantic visual concepts. In a real experiment, replace the synthetic vectors
with non-padding activations extracted from your loaded model at the **same
layer and preprocessing settings** as the binding.

```python
from pathlib import Path
import torch
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt
from vlmprobe import ProbeResult, visualization as viz
from vlmprobe.sae.backends import overcomplete

torch.manual_seed(42)
torch.set_num_threads(1)
output = Path("outputs/overcomplete_cpu")

binding = {
    "model_id": "synthetic-frozen-vectors-seed42-v1",
    "tokenizer_id": "no-tokenizer-synthetic-vectors-v1",
    "preprocessing_id": "identity-v1",
    "calibration_id": "synthetic-independent-train-validation-test-seed42-v1",
    "site": "residual.0", "layer": 0,
    "hook": {"module": "blocks.0", "kind": "output",
             "selector": None, "tensor_slice": None},
}
generator = torch.Generator().manual_seed(42)
basis = torch.randn(3, 16, generator=generator)
train = torch.rand(256, 3, generator=generator) @ basis
validation = torch.rand(64, 3, generator=generator) @ basis
test = torch.rand(64, 3, generator=generator) @ basis

sae = overcomplete.create(
    "topk", d_in=16, d_sae=64, top_k=8, binding=binding,
    encoder_module="linear", device="cpu",
)
report = overcomplete.train(
    model=sae,
    train_data=DataLoader(train, batch_size=32, shuffle=True,
        generator=torch.Generator().manual_seed(42)),
    validation_data=DataLoader(validation, batch_size=32),
    output_dir=output, binding=binding, nb_epochs=20, lr=1e-3,
    objective="mse", patience=5, seed=42,
    provenance={"corpus": "synthetic-seed42-v1", "split_unit": "independent-vector"},
)
loaded = overcomplete.load(output / "best.pt", binding=binding)
with torch.no_grad():
    features = loaded.encode(test)
    reconstruction = loaded.decode(features)
print(report["validation"])
print("held-out raw MSE:", (test - reconstruction).square().mean().item())

fig, ax = plt.subplots(figsize=(8, 4))
image = ax.imshow(features.numpy().T, aspect="auto", interpolation="nearest")
ax.set(xlabel="Held-out position", ylabel="Dictionary feature")
fig.colorbar(image, ax=ax, label="Feature activation")
fig.tight_layout()
fig.savefig(output / "heldout_features.png", dpi=160)
activity = ProbeResult("sae.features", {"features": features},
    {"source": "synthetic held-out activations"})
ax = viz.plot_sae_activity(activity, top_k=16)
ax.figure.tight_layout()
ax.figure.savefig(output / "feature_firing_frequency.png", dpi=160)
```

The training implementation calls the actual upstream `train_sae` each epoch
while preserving one Adam optimizer. It selects `best.pt` by independent
validation objective. `latest.pt` and `training_state.pt` preserve the final
model, optimizer, RNG and explicitly supplied DataLoader generator states for
resume. Increasing `nb_epochs` continues that run; altered hyperparameters,
binding, normalization or `provenance` are rejected. Supply accurate data hashes
and split IDs in `provenance`: tensor widths alone cannot establish independence.
Raw tensors and DataLoaders backed by tensors or `TensorDataset` are also
automatically fingerprinted from their shapes, dtypes and bytes; changed content
is rejected on resume even when manual provenance was omitted. The same stored
activation tensor in both splits is rejected even if it was cloned. Fingerprinting
reads the stored dataset tensors directly, without constructing a DataLoader
iterator, consuming shuffle RNG or running dataset transforms. Arbitrary datasets
and iterables are deliberately not traversed for hashing; their exact content
identity remains the caller's responsibility in `provenance` and is recorded as
unverified by the automatic fingerprint. This guard detects identical complete
splits, not partial overlap or common source specimens.
Keep training/validation/test split membership at the image or specimen level
when multiple correlated visual tokens come from the same source.

| Training parameter | Meaning |
|---|---|
| `nb_epochs=20` | Cumulative maximum epochs, including resumed epochs. |
| `lr=1e-3` | Persistent Adam learning rate. |
| `objective` | `mse`, `mse_l1` or `topk_auxiliary`; default is MSE for TopK variants and native MSE+L1 otherwise. |
| `l1_coefficient=0.01` | Native `mse_l1` penalty; coordinate-mean reconstruction and native penalty reductions are retained. |
| `auxiliary_coefficient=0.1` | Penalty passed to the upstream optional TopK auxiliary objective. |
| `clip_grad=1.0` | Native gradient clipping bound; zero disables clipping. |
| `patience=5`, `min_delta=0.0` | Early stopping on held-out objective. |
| `seed=0`, `resume=True` | Training RNG initialization and compatible checkpoint resume. |
| `monitoring=0` | Native monitoring level; 1–2 include upstream training statistics. |
| `device` | Optional device move; otherwise retain the adapter's current device. |

Overcomplete's generic JumpReLU training with `mse_l1` is not the JumpReLU
paper's full L0 recipe. Its native optional auxiliary TopK loss is reported by
name rather than claimed as a full paper-scale reproduction. BatchTopK's global
training count and running evaluation threshold retain upstream 0.3 semantics;
do not compare it as if `top_k` meant an average count per token.

## Existing dictionaries and model-bound probing

There is no central pretrained SAE release catalog in Overcomplete 0.3:
`overcomplete.list_pretrained()` returns `[]`. DINOv2/SigLIP/ViT/ResNet/ConvNeXt
backbone weights exposed upstream are pretrained **models**, not pretrained
SAE dictionaries. Train a dictionary or load one from a documented third-party
release, then wrap its already loaded native module:

```python
adapter = overcomplete.wrap(
    native_sae, binding=binding, is_fitted=True,
    input_mean=training_mean, input_scale=training_scale,
    source_metadata={"checkpoint": "actual-release-and-revision"},
)
result = probe.sae.features(
    layer=7, sae=adapter, binding=binding, tokens="visual",
).run(inputs)
edited = probe.sae.edit(
    layer=7, sae=adapter, binding=binding, tokens="visual",
    feature_ids=[15], scale=0.0, mode="error_preserving",
).run(inputs, metric=metric)
```

Here `probe`, `inputs`, `binding` and `metric` come from the model-bound workflow
in the [SAE guide](../sae.md). A runtime binding must come from
`build_sae_binding` for the actual loaded model; the synthetic example binding
above is not a substitute. Native trained BatchTopK requires its real
`running_threshold`; a bare upstream `state_dict` omits it and is insufficient.

The bridge saves tensor-only artifacts and never unpickles arbitrary upstream
model objects. Portable saving of a caller-loaded custom module additionally
requires its exact `init_config`; `create()` supplies this automatically. The
artifact also retains native non-buffer thresholds, JumpReLU bandwidth, fused
evaluation dictionary and explicit preprocessing. `decode` always returns native
activation units, so the common error-preserving intervention remains
`x_edit = x + D(z_edit) - D(z)`.

Use [VLMProbe's SAE visualization tools](../sae.md) with these shared
`ProbeResult` tensors. Features have no names until empirically interpreted:
activation association alone does not establish a diagnosis or causal mechanism.

## Sources and credit

This optional backend depends on Thomas Fel and collaborators'
[Overcomplete](https://github.com/KempnerInstitute/overcomplete), licensed under
MIT. The upstream architecture implementations, native losses and training loop
remain upstream. Relevant method papers include
[Scaling and evaluating sparse autoencoders](https://arxiv.org/abs/2406.04093),
[BatchTopK sparse autoencoders](https://arxiv.org/abs/2412.06410),
[Jumping Ahead](https://arxiv.org/abs/2407.14435), and
[Archetypal SAE](https://arxiv.org/abs/2502.12892).
