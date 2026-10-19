# Source audit and credits

[SAE hub](README.md) · [Methods](ALGORITHMS.md) · [Model-card workflows](models/README.md)

SAE methods share configuration, training, artifact and model-bound analysis
interfaces. Source checkpoint formats are read by explicit tensor converters.
The table records the implementation sources and their contributions.

| Source | Audited revision | What informed this integration |
| --- | --- | --- |
| [SAELens](https://github.com/decoderesearch/SAELens/tree/30c4502466785dd7809a307f7b705df187978aa3) | `30c4502466785dd7809a307f7b705df187978aa3` (6.54.6) | Language dictionaries; ReLU, Gated, TopK/AuxK, AbsTopK, JumpReLU, BatchTopK, Matryoshka and pursuit recipes; saved threshold/dead-feature state; checkpoint formats. |
| [ViT-Prisma](https://github.com/Prisma-Multimodal/ViT-Prisma/tree/64daf1425f7e5311844213fd0fb6f4127a30cd16) | `64daf1425f7e5311844213fd0fb6f4127a30cd16` | Vision dictionary use; ReLU/TopK/Gated; per-input normalization contexts; native image coordinates; author CLIP dictionary conversion. VLMProbe uses its own HF ViT adapter. |
| [Overcomplete](https://github.com/KempnerInstitute/overcomplete/tree/a1781af49c6e4bbfdbfd763b9757bcf6c5dd6403) | `a1781af49c6e4bbfdbfd763b9757bcf6c5dd6403` (0.3.0) | Vision dictionary methods; global-batch TopK, archetypal dictionary constraints, matching/orthogonal pursuit and experimental quantized codes. |
| [AbsTopK-SAE](https://github.com/GoXzascc/AbsTopK-SAE) | Author credit retained by SAELens's AbsTopK implementation | Absolute-magnitude selection and signed activations. |

Original MIT notices are distributed with the package:
[SAELens](../../../src/vlm_probing/sae/licenses/saelens-MIT.txt),
[ViT-Prisma](../../../src/vlm_probing/sae/licenses/prisma-MIT.txt),
[Overcomplete](../../../src/vlm_probing/sae/licenses/overcomplete-MIT.txt),
[AbsTopK](../../../src/vlm_probing/sae/licenses/abstopk-MIT.txt).
These notices do not relicense unrelated code or third-party checkpoints.
Model cards retain author checkpoint identifiers, source configurations,
licensing information and direct model/weight links.

The method audit records explicit departures from source recipes. In particular,
finite projected-gradient nonnegative pursuit, our archetypal parameterization,
normalization choices, and optional auxiliary objectives must not be represented
as identical reproductions of every upstream optimizer or paper result.
Temporal SAEs, transcoders, spatial nonlinear encoders, and classical NMF/PCA/ICA
have different contracts and are not advertised as supported same-hook SAEs.

## What is tested

Tests cover equations/gradients, saved method state, train-only normalization,
held-out evaluation, exact budget/resume behavior, artifact corruption and
binding rejection, context-preserving feature edits and actual LM/ViT/VLM
forwards. Optional direct checkpoint tests compare native inference with source
tensor equations for a pinned GPT-2 dictionary and a pinned CLIP dictionary.
They establish dictionary conversion numerics, not end-to-end backbone parity,
named concepts or a paper-scale benchmark.
