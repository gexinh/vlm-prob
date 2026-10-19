# SAE v3: locally controlled, bundled research cores

## Goal

Make all three SAE integrations independent of installed official SAELens,
ViT-Prisma and Overcomplete distributions. Maintain selected source internally,
preserve native numerical conventions, and expose VLMProbe-owned public loading,
training, probing and visualization interfaces.

## Difference from v2

The previous version, commit `c3f9006` on `dev/sae-v2`, wrapped installed upstream
packages with version-range checks. It unified our API but did not own the
implementation or isolate it from upstream dependency changes.

This version, `dev/sae-v3` / `0.9.3.dev0`, bundles the selected cores under
`src/vlm_probing/_vendor/{saelens,prisma,overcomplete}` at the same audited source
commits as v2. Each selection retains its original MIT LICENSE, upstream file
hashes, local hashes and modification notes. No runtime imports or distribution
checks select an official SAE package. Upstream changes enter only through an
explicit local source update and regression review.

- Keep the `sae.backends` names, loading/training entry points and `probe.sae`
  feature/profile/reconstruction/edit interface.
- Preserve eight SAELens training architectures, six Overcomplete architectures,
  Prisma Standard/TopK/Gated dictionaries, per-input normalization contexts and
  model/hook/preprocessing binding checks.
- Retain the compressed checkpoint catalog; inference and training use bundled
  source. Checkpoint downloads remain separate from code installation.
- Keep generic numerical/download dependencies in our own `sae` extra. Remove
  official toolkit dependencies, Prisma Git installs and the inherited
  Overcomplete Matplotlib upper bound. The base package remains PyTorch-only.
- Do not bundle unrelated model download/conversion stacks, dataset runners,
  dashboards or tracking services. Prisma's broad ImageNet-size native runner
  is explicitly outside this selection; our activation/image training path
  remains available with user-defined budgets.
- Skip the private vendor tree during public namespace alias discovery, so
  importing VLMProbe does not eagerly import SAE dependencies.
- Keep v2 as a separate local branch; do not modify the original checkout or
  publish these experimental changes.

## Expected results

1. Without the three official packages or TransformerLens, users can construct,
   train, save/reload and probe the integrated dictionaries.
2. Installing/upgrading those official packages must not affect selected code,
   output shapes, training options or checkpoint interpretation.
3. Bundled math should match the audited upstream implementation on identical
   weights and inputs, including gradients and normalization context.
4. Supported pre-trained dictionaries should remain loadable without their
   original Python toolkit; exact backbone/preprocessing compatibility remains
   independently verified rather than inferred from hidden width.
5. Original licensing and source provenance must ship in both wheels and source
   distributions. No downloaded weights or generated run outputs belong in the
   source package.

## Source scope and maintenance

| Core | Audited source commit | Internal provenance |
| --- | --- | --- |
| SAELens | `30c4502466785dd7809a307f7b705df187978aa3` | `_vendor/saelens/PROVENANCE.json` |
| ViT-Prisma | `64daf1425f7e5311844213fd0fb6f4127a30cd16` | `_vendor/prisma/SOURCE.json` |
| Overcomplete | `a1781af49c6e4bbfdbfd763b9757bcf6c5dd6403` | `_vendor/overcomplete/VENDOR_MANIFEST.json` |

The public backend is the compatibility boundary. Vendor paths are private.
Original architecture names and references remain credited; bundling does not
claim authorship of their algorithms. Generic PyTorch/numerical dependencies
still require a supported environment; owning SAE source specifically removes
runtime coupling to the three upstream toolkit APIs.

## Verification

The full default regression suite passes **338 tests and 191 subtests**, with
13 optional pinned-upstream oracle comparisons skipped in that environment.
The separate oracle environments pass those comparisons: SAELens six inference
and eight training architectures match exact outputs/gradients; Overcomplete's
six architectures match exact forward/gradient/evaluation results; Prisma's
nine SAE/normalization variants and four tiny vision variants match the pinned
upstream numerical contracts.

All eight SAELens architectures and all six Overcomplete architectures complete
small CPU training/export/reload runs without official packages. Prisma's full
image-to-training-to-feature-overlay example executes using the bundled core.
The previously checked official GPT-2 and CLIP dictionary weights also load
through the vendored implementations with official imports absent or blocked.

The wheel and source distribution are built as `0.9.3.dev0`; their original
licenses, manifests and pinned registry are included. Installing the wheel into
an independent target and actively blocking all three official toolkits plus
TransformerLens still permits construction and encode/decode through all three
backends. Installed-wheel catalog search also works offline.

Measured evidence is recorded in `runs/sae_backends_v3/verification_summary.json`
and the local run index. Source/import guards and license/file-hash checks are
part of the normal suite. Synthetic integration checks are not evidence of
semantic concept quality.
