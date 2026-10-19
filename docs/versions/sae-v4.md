# SAE v4: native methods, one trainer and first-party model cards

## Objective

Make SAE a peer of Lens, Attention and Causal inside VLMProbe. Users choose an
algorithm and use one fit/load/run interface. Implementation sources must not
be public backend choices. The previous version is `dev/sae-v3`, commit
`3a963b7f843a9f371d98c61248a48f910508d95c`.

## Changes from v3

- Replace provider dispatch with native method configurations and a deduplicated
  algorithm registry, preserving explicit mathematical/training variants.
- Route every trainable dictionary through one trainer, normalizer, evaluation
  and checkpoint path; retain method-owned losses and state updates.
- Add model-bound method factories, fitting on caller inputs and bound loading,
  with automatic exact model-weight fingerprints and explicit data provenance.
- Introduce one artifact schema and our own model cards. Source checkpoints
  enter through one-time importers rather than runtime upstream classes.
- Exclude unverified pretrained cards and candidate resource lists from the
  distributed package. Published model cards require completed end-to-end validation.
- Restore a balanced README and move SAE methods/models/training/examples/API
  to the SAE documentation subtree.
- Remove superseded backend modules, duplicate training loops and source-first
  examples/docs once the native replacement is verified.

## Expected behavior

1. Identical algorithms use identical public calls for language, vision and VLM
   inputs, subject to explicit adapter and activation-shape compatibility.
2. Native migration matches mathematical reference computations and supported
   source checkpoints without silently equating different recipes.
3. Fit freezes backbone computation, fits preprocessing only on training data,
   validates independently and supports provenance-checked resumable training.
4. All algorithms save/load one native format; imported feature ordering,
   normalizers and precise model/module bindings remain explicit.
5. Public pretrained model cards require completed end-to-end validation. Local
   experiment artifacts retain their own provenance and measured evidence.
6. Public workflows never import `sae.backends` or select an upstream toolkit.

## Measured validation

- Full CPU regression suite: **430 passed, 2 optional real-checkpoint tests
  skipped, 178 subtests passed**. The two pinned author-checkpoint conversions
  were run separately and passed their numerical parity checks (GPT-2 and CLIP).
- The same fit/run/profile/control/save/load contract was exercised on actual
  tiny GPT-2, HF ViT and Qwen3-VL forwards, across TopK, Gated and BatchTopK.
- All fourteen dictionary recipes train and round-trip through the single
  engine/artifact contract. Signed activity, constraints, train-only state,
  strict content/provenance resume, precise step/vector budgets, normalization
  contexts and BF16 JumpReLU thresholds have regression coverage.
- Identity tests reject equal-shaped weights with different activations,
  normalization epsilon or tokenizer behavior. Automatic loading verifies
  model tensors, architecture/configuration, numerical versions and processor
  identity. Explicitly declared source bindings cannot bypass the native card
  gate merely by being embedded in a card.
- Inference-method fitting fails explicitly rather than silently discarding a
  loaded recipe/weights. Changed dictionary tensors invalidate inherited
  numerical evidence and mark previous training metrics stale on re-save.
- Source distribution and wheel build successfully; `twine check --strict`
  passes. A separately installed wheel runs all fourteen native mathematical
  paths, resolves the validated registry and packaged licenses, and completes live ViT fitting,
  feature readout, save/load and an exact no-op control while official SAE
  package imports are blocked **in the verification process only**.
- The balanced README, SAE hub, full parameter tables, method inventory,
  training protocol, native model cards and full input-to-plot tutorial are
  included. Deprecated provider APIs, duplicated SDKs/trainers, source-first
  guides and obsolete provider tests were removed; relevant shared operation
  tests and original licenses were retained.

### Image workflow

`examples/sae_quickstart.py` creates procedural RGB images and a random tiny
ViT; it uses 24 train and eight held-out images, a 4 by 4 patch grid, a 64-feature
TopK dictionary (`k=4`), and four training epochs. The selected held-out feature
is 48. The measured best validation objective is `4.4014503955841064`;
reconstruction changes class-0 logit by `0.0013364032`, feature removal by
`-0.0053254217`. `scale=1` is an exact no-op. These demonstrate an executed
workflow, not useful semantic concepts or improved accuracy.

The local run is `runs/sae-v4-quickstart-final/`; the published compact figure is
`docs/assets/sae/native-v4-quickstart.png`. Fitted weights, full runs, downloaded
models, paper/report/slides source trees and old experiment outputs are not
added to this review branch. The imported checkpoint audit is retained locally
at `runs/sae_native_v4/imported/verification.json`.

## Model catalog and current limits

The native method registry contains fourteen algorithm recipes, four explicitly
experimental. The published pretrained-model registry is currently empty:
existing source checkpoint checks establish dictionary numerical parity, while
complete source-backbone execution and hook/preprocessing compatibility still
need validation. Those records and resource lists are retained only in ignored
local audit storage and are not distributed or exposed as public model cards.
Native dictionaries trained by a user remain savable, locally registrable and
loadable through the unified model-card workflow.

This version uses constant-rate Adam and finite in-memory activation caches.
It does not reproduce every upstream optimizer schedule, resampling subsystem,
spatial encoder or training-scale benchmark. Nonnegative OMP uses a recorded
finite projected-gradient NNLS approximation; archetypal training uses our
explicit constraint parameterization; QSAE is experimental and quantization is
not guaranteed sparsity. Cross-space transcoders and temporal dictionaries
require separate contracts and remain deferred.

The collection limit is a per-split tensor payload cap, not a hard total-RAM
cap; joining chunks can temporarily duplicate a split. Torch and explicit
loader/sampler RNG states are restored, but arbitrary Python/NumPy transforms
and worker-process randomness need their own deterministic caching protocol.
Backbone fingerprints are checked at fit/load; callers must keep that backbone
frozen during subsequent probe calls. Inference loading is supported; implicit
warm-start fine-tuning on a loaded method is deliberately rejected.

The original `/data/gexinh/project/vlm_probing` checkout and its main branch are
unchanged. Review work is isolated in `/data/gexinh/project/gexin/vlmprobe_sae`,
branch `dev/sae-v4`; v3 remains available for comparison.
