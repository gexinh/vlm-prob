# SAE v1 development version

## Goal

Introduce a fourth method family for learned sparse features while retaining the
existing model adapter, token selectors, structured results and visualization
contracts. Users must be able to train their own dictionary and test individual
feature interventions, rather than depend only on third-party checkpoints.

Development is isolated in `/data/gexinh/project/gexin/vlmprobe_sae`, branch
`dev/sae-v1`, based on commit `d912a4edb9c6b61d9d92bb499a050007d12813e7`.
The original `/data/gexinh/project/vlm_probing` checkout is not the development
target. No push or merge is part of this version's authorization.

## Differences from the previous version

- Add ReLU + L1, TopK and Gated SAE core architectures with explicit input
  normalization and native-unit reconstruction.
- Add training on user activation batches, train-only initialization, independent
  validation, early stopping, portable best artifacts and resumable optimizer/RNG
  state. Test examples are evaluated only after checkpoint selection.
- Add `probe.sae.features` and `probe.sae.edit` using actual residual hooks and
  common token selections. Reject unfitted or mismatched dictionaries.
- Bind artifacts to layer/module/selector/representation and explicit
  model/tokenizer/preprocessing/calibration identities.
- Retain the original reconstruction error during default feature edits;
  expose reconstruction replacement as a separate control.
- Add sparse-feature activity plots and visual-region overlays, using native
  token positions and caller-supplied image geometry.
- Document complete input-to-training-to-output usage in `docs/sae.md`.

This version does not replace the existing Tuned Lens objective or relabel a
dictionary feature as a named pathology concept. SAE training reconstructs native
activations; it does not automatically teach the frozen model a new vocabulary.

## Expected experimental behavior

- ReLU dictionaries should trade reconstruction error against mean L0 as the L1
  coefficient changes. TopK should activate at most `k` positive features per
  vector. Gated dictionaries should separate feature selection and magnitude.
- A trained dictionary should be evaluated against its initialization on
  independent inputs; improved reconstruction is expected but is not guaranteed
  for every architecture or small pilot dataset.
- Error-preserving edits at scale one must be bitwise native no-ops. At scale
  zero, only the selected features' decoded contribution is removed. Replacing
  the entire activation by a reconstruction can change behavior even at scale one.
- Feature IDs require high-activation examples and controlled edits before any
  semantic interpretation. Architecture comparisons must preserve measured
  reconstruction/sparsity tradeoffs, data scope and run size.

## Verification status

The full library suite passes **263 tests and 177 subtests**. A wheel for
`vlmprobe 0.9.1.dev0` builds successfully; this development version is local and
has not been published to PyPI or pushed to GitHub.

The generic cache and training CLIs were additionally executed offline on a
locally saved tiny GPT-2 checkpoint and six custom JSONL records. They computed
new native activations, trained a TopK dictionary and restored the best epoch;
held-out FVU was 0.6859 with mean L0 4.0. These are workflow checks on a random
model, separate from the pretrained pathology pilot below.

Fourteen model-bound SAE API tests pass on CPU. They cover actual small-model
forwards, independent SAE fitting, padding coordinates, mismatched hook and
checkpoint identities, training-flag/parameter preservation, exact no-op
controls, mixed-precision inactive-feature no-ops and native-plus-decoded-delta
hook equivalence, and both built-in visualizations. Nonvisual overlays are
rejected even when their token count happens to match a declared image grid.

The complete example in `docs/sae.md` was executed directly: a random GPT-2
configuration, explicit input vocabulary and independent example-text splits
produce real activations, train a TopK dictionary, reload its validation-selected
checkpoint, evaluate held-out inputs, save `outputs/sae_cpu/feature_activity.png`,
and measure a feature edit. The output is an `[11, 64]` held-out feature matrix
with exactly four active features per token. It verifies plumbing on a tiny
random model, not pathology interpretation or pretrained-model performance.

Architecture-specific kernel/training checks and any larger-domain pilot should
be reported separately from this API verification. External checkpoint loading
is restricted to the supported format/backend contracts; no public external
dictionary is represented as verified merely because the bridge exists.

## Measured pathology functional pilot

Three native dictionaries were trained on the same frozen Qwen2.5-VL-3B-Instruct
post-block-7 visual activations: input width 2,048, dictionary width 4,096. The
source-slide-disjoint PathVG pilot supplies 98,756 training, 24,850 validation
and 24,836 test visual positions from 512 / 128 / 128 images and 34 / 6 / 6
reconstructed source-slide groups. Patient independence is not verified.
Normalization uses the training split and test FVU uses the fixed training mean.

All runs use seed 42, batch size 512, Adam learning rate 0.001, a maximum of ten
epochs and patience three. ReLU and Gated use L1 coefficient 1.0 after initial
validation density checks found their 0.01 setting too dense. TopK uses `k=32`;
its supplied L1 coefficient is inactive in the core TopK objective. Earlier
calibration outputs remain in ignored run directories and are not presented as
additional selected results.

| Dictionary | Test FVU | Mean test L0 | Zero-firing features on test | Selected epoch |
|---|---:|---:|---:|---:|
| ReLU + L1 | 0.1437 | 103.34 | 2.08% | 8 |
| TopK, k=32 | 0.1656 | 32.00 | 74.46% | 10 |
| Gated | 0.0828 | 272.00 | 8.54% | 5 |

This is a **functional pilot, not a comparison at matched L0**. The dictionaries
operate at different sparsity levels; smaller FVU does not establish a better
architecture or more interpretable features. TopK's high zero-firing fraction on
this test split is a measured limitation. The current TopK implementation does
not include AuxK; no claim of reproducing the complete original training recipe
is made. Zero firing here means no positive activation on this evaluation split,
not a proof of a globally dead feature. Reconstruction and sparsity measurements
do not automatically validate named pathology concepts.

Measured artifacts are in [ReLU metrics](../../runs/sae_pathvg_v1/relu/metrics.json),
[TopK metrics](../../runs/sae_pathvg_v1/topk/metrics.json) and
[Gated metrics](../../runs/sae_pathvg_v1/gated/metrics.json). The matching
`best.pt` files contain the fitted dictionaries and their exact model/hook/data
bindings. `examples/visualize_sae_pathology.py` renders feature maps and measures
native feature-edit controls on held-out images. Generated domain results stay
under `runs/sae_pathvg_v1/results/` rather than becoming source-tree inputs.

## Scope and cleanup

Keep generated training caches, checkpoints, figures and temporary runs under
ignored output directories. Retain one current example per workflow and avoid
copying old report, slide or research-output trees into this development checkout.
External checkpoint support must name the supported source architecture and
normalization; unsupported layouts should fail explicitly.
