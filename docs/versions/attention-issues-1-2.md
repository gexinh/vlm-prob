# Attention API and attribution fixes

## Goal and baseline

Address [issue #1](https://github.com/ubc-tea/vlm-probe/issues/1) and
[issue #2](https://github.com/ubc-tea/vlm-probe/issues/2) against library version
1.0.1, laboratory main commit `81d7b2e9ccf16acc25b2d2bceb3ce056397fca3c`.
The implementation is developed in `fix/attention-issues-1-2`.

## Changes from the previous version

- `profile`, `rollout` and `head_logits` reject a non-`None` metric before model
  execution. Their normal results retain `metric=None`. Target-conditioned
  attribution and intervention methods continue to require and evaluate a metric.
- ATTATTR and input-path integration accumulate gradients in at least FP32,
  promoting before division; FP64 remains FP64. Inputs and probabilities injected
  into the frozen model retain their native dtype. Native probability validation
  happens before wider analysis arithmetic, so rounded BF16 rows remain valid.
- Grad-CAM pools gradients over the intersection of selected keys and each
  head/query's actual attention support. Display masking and normalization use
  the same support. Empty selected intersections produce finite zero maps.
- Native adapters expose structural support for causal, padding, sliding-window
  and bidirectional attention. Support is captured only when requested; ordinary
  forwards keep their numerical operations and weights. Custom adapters can
  declare `ModelSpec.attention_supports`; absent a declaration, the standalone
  kernel retains unrestricted-support behavior. Probability underflow is not
  used to infer structural masking.
- Qwen3.5 loading guidance separates vision SDPA from decoder eager attention.
  The guides explain that query/key selection does not make attention sparse,
  and integration steps primarily affect runtime rather than per-step dense
  attention storage. Unused target setup is removed from observation tutorials.
- Add analytic and native-model regression tests, with a CPU attention workflow
  for Python 3.10 and 3.12.

## Expected experimental behavior

- On the constant-gradient fixture, the ATTATTR sum stays approximately one at
  20, 64, 256, 512 and 1,024 steps for BF16/FP32/FP64, instead of BF16 sums
  shrinking to 0.5 and 0.25 at 512 and 1,024 steps.
- Appending causally inaccessible future tokens leaves earlier-query prefix
  Grad-CAM maps and head weights unchanged, including multi-query and normalized
  displays. Allowed keys whose probabilities underflow to zero still participate
  in gradient pooling.
- Unrestricted bidirectional Grad-CAM preserves its previous formula. Native
  forward logits, embedding gradients, model weights and hook cleanup remain
  unchanged by support capture.
- These controlled regressions do not establish the error magnitude in existing
  pretrained maps or technical-report figures. No pretrained benchmark or report
  experiment is rerun as part of this fix.

## Compatibility

Passing a metric to a descriptive observation now raises `ValueError`; omit it.
Model-bound BF16 integration results use FP32 analysis tensors, and FP64 results
remain FP64. The package version is not changed or published by this development
branch. No official SAE packages are introduced as dependencies.

## Validation

Validation uses Python 3.12, PyTorch 2.6.0 and Transformers 5.3.0 on CPU, with
downloads disabled. The issue author used PyTorch 2.10.0; the original BF16
counterexample was reproduced on 2.6.0 before applying this fix.

- Complete source suite: **282 tests passed**, including the 25 new regressions.
- Installed-wheel regressions: **25 tests passed**, with imports verified to
  resolve to the installed wheel rather than the source checkout.
- Installed package/import compatibility: **5 tests passed**.
- Wheel and source distribution builds and `twine check --strict` passed.
- Documentation validation passed: 20 method guides, 11 model guides,
  32 Python blocks, 19 scripts, nine notebooks and 89 factory parameters.
- The profile and rollout tutorials executed offline using a tiny local ViT;
  both saved fresh results and plots with `metric=None` metadata.
- Native support tests check exact forward logits, embedding gradients, model
  weights and hook cleanup for GPT-2, Mistral, Qwen3.5 and bidirectional ViT.
  The legacy adapter branch was checked using current native Llama/Qwen2.5 models
  with mocked version selection; a separate Transformers 4.57 installation was
  not executed. Python 3.10 is configured in CI but was not run locally.

The new regressions cover constant-gradient completeness across dtypes and step
counts, native BF16 probability rounding, signed targets, native intervention
dtypes, single/multi-query future-token invariance, normalization, empty support
intersections, padding, sliding windows, per-head masks and allowed probabilities
that underflow to zero. Custom support declarations and invalid mask shapes are
also checked.

From a checkout with the optional model dependencies installed:

```bash
CUDA_VISIBLE_DEVICES='' HF_HUB_OFFLINE=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
PYTHONPATH=src:examples python -m unittest discover -s tests -v
```

Audit fixtures, transient environments, distributions and validation logs are
kept outside the source tree. No cached experiment outputs or duplicate model
implementations are added to the library.
