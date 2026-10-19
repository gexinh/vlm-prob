# Unified SAE training protocol

Every native SAE method trains through `fit_sae` and the same optimizer loop.
The selected method owns its encoder, decoder, sparsity/auxiliary losses and
post-step constraints. There is no dispatch to another library's trainer.

`SAETrainingConfig` describes the shared experiment protocol. `SAEConfig`
describes the method: dictionary width, TopK budget, thresholds, auxiliary
coefficients, dictionary constraints and activation normalization. Both are
retained with the checkpoint. This protocol uses constant-rate Adam and
validation-based checkpoint selection; it does not claim an upstream project's
complete large-scale schedule, resampling system or benchmark reproduction.

## Inputs and independent splits

`fit_sae(model, train_vectors, validation_vectors, output_dir, *, training,
provenance=None)` accepts finite floating `[positions, activation_width]` tensors
or finite activation-cache DataLoaders/batch lists. It never accepts test data.
Extract these vectors from the frozen model using the exact layer, input
preprocessing and token/patch group recorded in the model binding.

Split documents/images/slides/patients before extracting activations. Flatten
only known batch/token axes, exclude padding, and retain native visual-grid
coordinates for later overlays. Splitting patches from one image between
training and validation does not establish image-level generalization.

The engine checks source identity, overlapping tensor views, identical caches,
content/dtype/shape fingerprints and any supplied source-ID/group metadata.
Supply `provenance={"groups": {"train": [...], "validation": [...]}}` when source
groups are known. Tensor values alone cannot establish patient independence.

Cache readers are materialized into CPU activation tensors before fitting;
this version is intended for finite, already extracted activation caches.
Infinite generators and one-shot iterators are rejected. Known tensor loaders
are read without advancing their sampler. Other finite readers retain their
caller Torch/sampler RNG states. The canonical engine creates its own recorded
permutation and minibatch cursor, so all methods use the same batching protocol.

## Configuration

```python
from vlmprobe.sae.training import SAETrainingConfig, fit_sae

training = SAETrainingConfig(
    epochs=20,
    batch_size=1024,       # Activation vectors, not images or documents.
    lr=3e-4,
    patience=4,            # Consecutive completed validation epochs.
    min_delta=1e-4,
    normalization="rms",
    seed=42,
    device="cuda:0",
)
history = fit_sae(
    dictionary, train_vectors, validation_vectors, "outputs/my_sae",
    training=training,
    provenance={"groups": {"train": train_groups, "validation": validation_groups}},
)
```

The model and tensors above are supplied by the corresponding model/data guide;
this function performs no hidden model loading or extraction. Public model-bound
SAE factories prepare the same cache and call this function. The complete
image-to-activation-to-training example is maintained with the library demos.

| Field | Meaning |
|---|---|
| `epochs=10` | Maximum complete passes when no other budget is set. |
| `max_steps=None` | Optional maximum optimizer updates; takes precedence over `epochs`. |
| `max_vectors=None` | Optional maximum activation vectors entering gradient updates; takes precedence over `epochs`. It cannot be combined with `max_steps`. |
| `batch_size=256` | Activation vectors per update; the final cache/budget batch may be shorter. |
| `lr=1e-3` | Finite positive constant Adam learning rate. |
| `patience=3` | Stop after this many completed validation epochs without the required improvement. Budgets are ceilings; early stopping can finish sooner. |
| `min_delta=1e-4` | Minimum validation-objective improvement for committed epoch checkpoint selection. |
| `normalization="rms"` | Fit scalar coordinate RMS on training vectors for scalar-normalized methods; `"none"` uses scale one. Per-input normalization remains method-owned. |
| `seed=0` | Local Torch/permutation seed; caller RNG state is restored afterward. |
| `device="cpu"` | CPU or a specific CUDA device. |
| `resume=True` | Resume a compatible existing canonical training state; otherwise require a fresh output. |
| `grad_clip=5.0` | Finite positive maximum gradient norm before each Adam update. |
| `progress_every=20` | Optimizer-update interval for durable progress and resume checkpoints; epoch ends and budget stops are always saved. |

Unknown constructor options fail rather than disappearing. Epoch, step and
vector budgets have explicit units in `history["budget"]`. The optimizer budget
counts gradient-update vectors. Train-only normalization/initialization reads
the complete training cache beforehand; its observation count is recorded
separately in `history["normalization"]["positions"]`.

## Calibration, objectives and validation

Training-only initialization computes a position-weighted raw mean and coordinate
RMS. Scalar normalization stores its scale in the model; decoding returns raw
activation coordinates. Layer normalization and constant-norm methods retain
their matching per-input decoding context and do not fit a second global scale.
Their decoder bias is initialized to zero. Archetypal candidates and initial
BatchTopK/Matryoshka inference thresholds are calibrated exclusively from train
vectors before the first validation pass.

Each training step calls the method's `loss`, clips gradients, updates Adam and
applies its `post_optimizer_step_` constraints. Threshold EMA, inactive-feature
counters and other method state are registered buffers saved with the model.
Validation runs in evaluation mode, checks that buffers remain unchanged and
restores the original module flags. It never updates training counters or
thresholds.

Validation reports the method's total/reconstruction/sparsity/auxiliary
objectives, raw-coordinate MSE, FVU relative to the fixed training mean, L0 and
feature frequencies. Signed methods count nonzero activations, including negative
ones. An inactive feature means inactive on this evaluation cache, rather than
a claim that the feature is universally dead. Degenerate FVU denominators are
reported as `None` with an explicit flag.

Checkpoint selection uses the total validation objective and never a test-set
score. A budget that stops inside an epoch also reports terminal validation.
This provisional measurement can select the returned inference artifact, but
it does not alter persistent epoch-based early stopping when the budget is
later extended.

## Artifacts and exact continuation

- `best.pt`: portable native inference artifact selected by validation.
- `training_state.pt`: last training weights, optimizer, method buffers,
  normalizer, committed best weights, local RNG, cache permutation and cursor.
- `history.json`: configuration, source fingerprints, train-only statistics,
  validation history, selected artifact and final metrics.
- `status.json`: current phase, completed epochs/updates/vectors and errors.

Inference export and resumable training state remain separate. The trainer does
not fold normalization into the live weights and then resume with an optimizer
from another coordinate system.

Resume requires identical method/objective settings, optimizer settings,
minibatch size, seed, normalization, source binding, provenance, dtype, Torch
version and cache fingerprints. Device moves are allowed; numerical equivalence
across different hardware is not guaranteed. A budget may increase within the same
unit; it cannot shrink or silently switch from epochs to vectors/steps.

For a vector budget cutting a minibatch, the checkpoint additionally retains the
state before that partial update. Extending the budget restores this boundary
and replays the full minibatch, producing the same trajectory as uninterrupted
training with the larger budget. Replayed partial vectors are explicitly
reported as `resume_rolled_back_partial_vectors`. This prevents a short terminal
batch from silently changing all subsequent optimizer updates.

`train_sae(model, train_batches, validation_batches, checkpoint_dir, ...)` remains
as a compatibility spelling. It constructs `SAETrainingConfig` and invokes the
same engine; it contains no second training loop.

## Command-line training on your activation cache

The repository's [cache extractor](../../../examples/cache_sae_activations.py)
starts from a user-supplied dataset manifest and a frozen model. The
[training command](../../../examples/train_sae.py) accepts its portable `.pt`
bundle: raw `train`, `validation` and `test` matrices, the exact model/hook
`binding`, and `groups[split]` with one source-group string per activation row.
All three split groups must be disjoint. Test positions are evaluated only after
training and validation-based checkpoint selection; they never enter fitting.
The Python `fit_sae` API requires only train and validation caches.

```bash
python examples/train_sae.py \
  --activations my_activations.pt --output-dir outputs/topk \
  --method topk --d-sae 4096 --k 32 \
  --epochs 20 --batch-size 1024 --lr 0.0003 --device cuda:0
```

`--method` and the older `--architecture` are aliases. Their choices come from
`list_methods()` and include every supported and experimental native method.
For method-specific settings, save a JSON object such as:

```json
{
  "jumprelu_threshold": 0.15,
  "jumprelu_bandwidth": 0.05,
  "jumprelu_sparsity": "l0",
  "l0_coefficient": 0.01,
  "input_normalization": "layer_norm"
}
```

Pass it with `--method jumprelu --method-config jumprelu.json`. JSON values
override `--k` and `--l1-coefficient`; identity, widths and random seed remain
explicit CLI arguments. Unrecognized fields raise an error. Every resolved
method and training option is saved in `metrics.json`.

Use `--max-steps 1000` or `--max-vectors 1000000` instead of the epoch budget;
they are mutually exclusive and have the same exact budget/resume semantics as
the Python API. Other shared options include `--patience`, `--min-delta`,
`--normalization rms|none`, `--grad-clip`, `--progress-every` and `--seed`.
Resume is enabled by default. `--no-resume` requires a fresh output directory.
