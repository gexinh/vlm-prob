# Library feedback hotfix 1.0.2

## Goal and baseline

Address the six items in the collaborator's library feedback dated 2026-10-21,
which tested `93e8f3e0`. This branch starts from laboratory main
`6663f0a492c4dea7d96d92b8cacea8f19734825f`, already containing the previous
attention precision and support-mask fixes. The branch is
`fix/library-feedback-1-6`; the package version is 1.0.2.

The goal is clearer calibration contracts, broader audited text-model support,
explicit propagation limits, and conservative input/display diagnostics. The
hotfix preserves the published estimators, attribution formulas and default
preprocessing/display behavior. It does not reproduce or modify technical-report
experiments.

## Changes from the previous version

- Jacobian calibration errors identify failing batch rows, valid/retained source
  and target counts, exclusion settings and selector context. Empty retained
  sets are rejected without silently dropping examples. Replacing an already
  fitted estimate warns before expensive public calibration work and points to
  the existing dataset estimator, `vlmprobe.training.fit_jacobian_lenses`.
  Ordinary `fit` still replaces; the dataset estimator still accumulates.
- Native Transformers 5.3.x Qwen2 and Qwen3 text models gain explicit automatic
  adapters. Qwen3 Q/K sites follow native head normalization before positional
  rotation. Unknown-model errors enumerate supported native classes and retain
  explicit adapter/registration instructions.
- Native adapters explicitly declare causal or bidirectional attention. Causal
  propagation construction warns about possible early-position amplification;
  results record the caveat. Undeclared custom adapters remain unknown. No
  normalization or algorithm is silently substituted, and gradient-weighted
  alternatives are not advertised as universally free of this bias.
- Optional `clip=(lower, upper)` on attention overlays/comparisons sets finite
  display percentiles. The default remains full range; signed maps retain zero
  centering, explicit overlay limits take precedence, shared scales pool finite
  values, and labels identify the display transform. Measured tensors and saved
  results are unchanged.
- Read-only input geometry tools inspect audited native grids, verify declared
  visual-token counts, and summarize preprocessing. Ambiguous tile/crop layouts
  raise an actionable capability error instead of inventing a lattice. Exact
  source-coordinate or bounding-box claims require verified preprocessing;
  geometric retention is not proof that semantic content survives. The LLaVA
  demo retains its strict target-mask guard, with an error clarifying that loss
  of exact-red mask pixels does not establish loss of all visual information.
- Guides distinguish architecture-specific input preparation from the common
  method calls. CPU regression coverage includes the new contracts and tools.
- The main README keeps its method layout, updates the source install command
  to `main`, and links the new Qwen text guide. Mirror synchronization uses the
  current personal repository name while accepting both historical aliases,
  so README project-page and source-install links follow the destination repo.
  Package publication remains an explicit manual workflow operation.

## Expected experimental behavior

- The same valid Jacobian calibration data produces the same estimate. Short or
  selector-incompatible prompts fail with usable diagnostics; repeated one-batch
  fits no longer silently look incremental. Dataset calibration continues to
  equal the prompt-weighted joint estimate.
- Supported Qwen text models bind without custom adapters. Native logits,
  embedding gradients, readout identity, actual consumed attention edits, model
  weights and temporary hook cleanup remain consistent with native execution.
- A causal rollout fixture can still show early-position amplification: the fix
  exposes the interpretation boundary rather than claiming to remove it.
  Bidirectional ViT and unknown custom adapters receive their declared scope.
- A display outlier no longer hides ordinary values when percentile display is
  explicitly requested. Default plots and underlying numeric arrays are stable.
- Native geometry mismatches remain errors. Preprocessing diagnostics distinguish
  known geometry from unavailable mappings, and do not equate loss of a pure
  color with absence of visual information.

## Validation and limits

Completed checks:

- Complete source suite: **329 tests passed**, including 47 new regressions.
- Installed-wheel checks: **79 tests passed** in a separate environment; imports
  resolve to the installed package, and all 16 changed/new implementation files
  match the reviewed source hashes.
- Wheel and source distribution build, `twine check --strict`, and
  `git diff --check` passed.
- Documentation checks passed for 20 method guides, 12 model guides, 33 Python
  blocks, 19 scripts, nine notebooks and 89 factory parameters. Both new input
  geometry examples executed offline through the public import name.
- Independent reviews checked display provenance and native geometry ordering;
  explicit color-limit labels, channels-last ambiguity, config-less custom
  models and InternVL pixel-shuffle version handling have regression coverage.

These regressions use controlled fixtures and small native CPU models with
downloads disabled; they do not establish pretrained accuracy or repeat the
collaborator's large GPU sweep.

Python 3.10 and 3.12 are configured in the library regression workflow. Local
validation uses Python 3.12, PyTorch 2.6.0 and Transformers 5.3.0. Qwen text
support added here targets Transformers 5.3.x, not an untested extension of the
legacy 4.57 adapter branches.

Automatic grids currently cover fixed ViT/LLaVA, Qwen still-image mergers and
InternVL v2 tile-local grids. Idefics3 tiled/padded inputs, video, unknown models,
and ambiguous layouts still require caller-provided explicit geometry. InternVL
tile grouping and original-image placement are not inferred. Exact bbox traces
are limited to supported slow CLIP/ViT image processors with matching replay;
other paths report unavailable geometry rather than inventing a mapping.

Audit inputs, generated figures, build artifacts, installation environments and
validation logs live outside the source tree. No copied model implementations,
downloaded checkpoints, cached experiment outputs or obsolete alternative
estimators are introduced. Existing compatibility paths remain in place.
The previous duplicate streaming exclusion helper was removed in favor of the
same calibration preflight used by the one-batch estimator.

This development branch does not itself publish a PyPI release, create a tag,
update Hugging Face, or modify report repositories/assets.
