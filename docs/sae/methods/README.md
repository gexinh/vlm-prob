# Sparse autoencoder methods

SAE is one of VLMProbe's four method families, alongside Lens, Attention and
Causal. Methods are organized by algorithms. Model-card provenance identifies
where imported weights came from; it never chooses a different training engine
or mathematical implementation.

Every method consumes floating activation vectors `x[..., D]` from one bound
model and hook, produces dictionary coefficients `z[..., F]`, and reconstructs
the original activation coordinates. The backbone remains frozen. A feature ID
is a dictionary coordinate, not automatically a named concept or causal unit.

```python
from vlmprobe.sae.registry import list_methods, get_method, method_config

print([method["name"] for method in list_methods()])
config = method_config("topk", d_in=768, d_sae=3072, k=32)
print(get_method("topk")["sources"])
```

Each method has the same fit, save/load, feature/profile, reconstruction-control
and feature-edit workflow. All use the same native `SparseAutoencoder`, shared
trainer and artifact format. Core computation imports only PyTorch and local
mathematical primitives, never a source toolkit or a provider-selected SAE class.

## Encoders and dictionary components

Let `u` be the declared normalized activation, `b` the decoder bias and
`a = W_enc (u - b) + b_enc`. Input centering can be disabled explicitly with
`apply_b_dec_to_input=False`; output bias is independently controlled by
`use_decoder_bias`. Unless otherwise configured, decoder columns are projected
to unit L2 norm after each optimizer step.

| Method | Mathematical operation | Training recipe and scope |
|---|---|---|
| ReLU + L1 | `z = relu(a)` | Summed squared reconstruction error plus `l1_coefficient * sum(abs(z))`. |
| TopK | Keep at most `k` positive entries of each `a` | Reconstruction objective; optional explicit dead-feature AuxK. The original native default keeps AuxK disabled. |
| AbsTopK | Keep the `k` largest magnitudes and preserve their signs | Same decoder and optional dead-feature auxiliary path; negative coefficients are valid. |
| Gated | Hard positive gate selects features; separately scaled encoder directions predict magnitudes | L1 on rectified gate logits and a gate-reconstruction auxiliary whose decoder and centering bias are detached. |
| JumpReLU | `z_i = a_i` when `a_i > threshold_i`, otherwise zero | Nonnegative learned thresholds; rectangle surrogate, explicit bandwidth, L0 step penalty by default or an explicitly selected L1 variant. |
| BatchTopK | Keep the largest positive values across the training batch | `batch_budget="average"` means `k * number_of_vectors`; `"global"` means `k` total. Evaluation uses the saved training threshold independently for each input. |
| Matryoshka BatchTopK | BatchTopK with nested dictionary prefixes | Weighted sum of prefix reconstruction losses. Widths increase strictly and end at `d_sae`; the full-width loss occurs once. |
| Archetypal TopK | The same TopK encoder with an archetypal dictionary | Convex combinations of training anchors plus bounded relaxation; shares the same trainer. |
| Archetypal JumpReLU | The same JumpReLU encoder with that dictionary | Same threshold/loss options and training-only anchor requirement. |
| Matching Pursuit | Repeatedly select the positive atom most correlated with the residual | Tied decoder directions; discrete choices with gradients through selected coefficients and atoms. |
| Signed Matching Pursuit | Select by absolute correlation, retaining the sign | Experimental signed extension; iteration budget, residual tolerance and repeated-support stopping are explicit. |
| Nonnegative OMP | Unique greedy support followed by joint nonnegative coefficient refits | Experimental: projected-gradient NNLS with `omp_nnls_iterations`, a finite approximate solver budget. |
| Signed OMP | Unique greedy support followed by joint least-squares refits | Experimental signed extension; uses differentiable least squares on the selected atoms. |
| Quantized SAE | Learned scalar codebook with soft or hard quantization and a straight-through path | Experimental and unpublished in the reference toolbox. Quantization alone does not ensure sparse coefficients. |

ReLU, TopK and Gated preserve the earlier native core's values, objectives and
raw-coordinate scaling. These are declared implementation recipes rather than
claims of full paper-scale reproduction. The registry exposes `status`, defaults,
input contracts and primary references.

## Explicit training state

`model.loss(raw)` returns `loss`, `reconstruction`, `sparsity` and `auxiliary`.
The shared trainer owns optimization, validation, budget handling, snapshots and
resume. `model.post_optimizer_step_()` enforces dictionary/threshold constraints.
Model state contains all method-specific training buffers; source-specific
trainers are not called.

Optional AuxK uses `inactive_steps` counted in **training steps**, with
`dead_feature_steps`, `auxk_k` and `auxk_coefficient` recorded in the configuration.
Inactive features reconstruct the detached current residual. This is an explicit
core auxiliary recipe; it does not silently enable a paper's full dead-feature
schedule, loss normalization or data curriculum.

Batch thresholds are updated only by training loss calls. Before initial
validation, `calibrate_(raw_training_batch)` may initialize the threshold without
updating step/dead-feature counters. `threshold_init` distinguishes first-batch
initialization from a zero-start EMA; `threshold_ema` is the retained-old-value
weight. Evaluation never updates thresholds, counters or anchors. Evaluation
thresholding can yield a different realized L0 than the training selection
budget; both should be reported.

The archetypal component is
`D = (softmax(coefficients) @ TRAIN_anchors).T + relaxation`, with each relaxation
column bounded by `archetypal_delta`. Candidates are selected deterministically
from supplied training vectors after normalization and declared centering.
This native softmax parameterization preserves the stated convex-combination
constraint; it does not claim the same optimizer trajectory as a projected
coefficient implementation. Validation/test vectors must never supply anchors.

## Normalization and imported checkpoints

`normalization="rms"` fits a scalar on training vectors only. The encoder receives
`x / input_scale`, and decoding multiplies by the same saved scalar. `"none"`
uses identity preprocessing for imported/folded weights and skips automatic RMS
fitting. Native recipe flags preserve decoder norms, input centering and the
optional TopK decoder-norm rescaling used by certain checkpoints.

`"layer_norm"` and `"constant_norm_rescale"` need per-input context. They are
handled through paired `encode_with_context` / `decode_with_context` calls. The
same context is reused for baseline and edited decoding, so an edit cannot
accidentally normalize against a different input. Plain `decode(z)` refuses
these modes because the required context is absent.

Layer normalization records mean, standard deviation, epsilon and correction
convention. The supported context recipe divides by `std + eps` and restores
`decoded * std + mean`, matching the visual reference convention; epsilon is not
added a second time on output. Constant-norm rescaling divides by the original
norm and rejects zero vectors instead of inventing a scale.

Any imported checkpoint must first convert to the same canonical architecture,
raw-space contract and artifact schema. Matching a hidden width is insufficient;
the exact backbone, hook, tokenizer/image preprocessing and calibration identity
remain required. Unsupported normalization or cross-space transcoders are
rejected rather than guessed.

## Sources and mathematical credit

The mathematical conventions were checked against the following primary works
and MIT-licensed reference implementations. Source projects supply provenance and
numerical oracles, not runtime selection or public method names.

- ReLU dictionary learning: [Towards Monosemanticity](https://transformer-circuits.pub/2023/monosemantic-features/index.html).
- TopK: [Scaling and evaluating sparse autoencoders](https://arxiv.org/abs/2406.04093).
- Gated: [Improving Dictionary Learning with Gated Sparse Autoencoders](https://arxiv.org/abs/2404.16014).
- JumpReLU: [Jumping Ahead](https://arxiv.org/abs/2407.14435).
- BatchTopK: [BatchTopK Sparse Autoencoders](https://arxiv.org/abs/2412.06410).
- Matryoshka: [Matryoshka Sparse Autoencoders](https://arxiv.org/abs/2503.17547).
- Archetypal dictionaries: [Archetypal SAE](https://arxiv.org/abs/2502.12892).
- Signed TopK: [AbsTopK](https://arxiv.org/abs/2510.00404),
  [MIT-licensed author implementation](https://github.com/GoXzascc/AbsTopK-SAE).
- Matching pursuit: [Matching pursuits with time-frequency dictionaries](https://doi.org/10.1109/78.258082).

Reference-code provenance includes
[SAELens](https://github.com/decoderesearch/SAELens) at
`30c4502466785dd7809a307f7b705df187978aa3`,
[ViT-Prisma](https://github.com/Prisma-Multimodal/ViT-Prisma) at
`64daf1425f7e5311844213fd0fb6f4127a30cd16`, and
[Overcomplete](https://github.com/KempnerInstitute/overcomplete) at
`a1781af49c6e4bbfdbfd763b9757bcf6c5dd6403`. The JumpReLU/Step surrogate conventions
follow the SAELens reference; signed selection credits GoXzascc; the experimental
quantized recipe credits Thomas Fel's reference toolbox. Original license and
copyright notices are retained; algorithm credit is not reassigned to VLMProbe.
