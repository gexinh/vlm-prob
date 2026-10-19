# SAE v2: native toolkits for language and vision

## Goal

Integrate SAELens, ViT-Prisma and Overcomplete as optional providers of trained
dictionaries, training protocols and probing methods. Keep a shared model-bound
analysis interface and preserve each toolkit's native mathematical conventions.

Development remains in `/data/gexinh/project/gexin/vlmprobe_sae`, now on
`dev/sae-v2`. The preceding version is local commit
`95a015e8bfe9cadc579dc6b514fa1f6bdbc6845b` on `dev/sae-v1`. The original library
checkout and published package are not the development targets.

## Differences from v1

- Add three optional native providers, checkpoint loading/wrapping, architecture
  discovery and native training dispatch. Preserve the v1 native implementations.
- Package a compressed author-resource catalog with model, hook, normalization,
  revision, source and verification metadata; provide CLI and offline HTML search.
- Add `probe.sae.profile`, `probe.sae.reconstruct` and runtime-checked provider
  loading alongside the existing feature and edit methods.
- Preserve input-specific normalization contexts during original and edited
  decodes, including Prisma's layer norm and constant-norm state.
- Support explicitly bound native HookedViT residual and MLP hooks. Representation
  vectors are identified as representation outputs rather than fake logits.
- Add full provider guides, native training examples and README credits.
- Reject incompatible training resumes: preserve source/configuration/optimizer
  contracts, fingerprint supported activation tensors, and record limits for
  caller-managed data streams and schedules.
- Move the v1 SAELens adapter to the provider module and retain its original
  import as a compatibility reexport. Keep one compressed catalog rather than a
  duplicate multi-megabyte raw registry in the source tree.

## Expected behavior

1. Adapted feature and reconstruction tensors should match the original toolkit
   on identical activation vectors, including saved normalization state.
2. User-data training should use the stated upstream objective, preserve
   frozen-model independence and produce loadable provenance-bound dictionaries.
3. Native identity edits must remain exact no-ops; reconstruction replacement
   and feature ablation remain separate controls.
4. Catalog search should work offline without importing optional toolkits.
   Listed resources must not be advertised as completed compatibility tests.
5. Vision and language feature IDs require independent semantic and behavioral
   evaluation; a working integration does not establish named concepts.

## Source audit

| Toolkit | Audited source | Installation / protocol detail |
| --- | --- | --- |
| SAELens | `30c4502466785dd7809a307f7b705df187978aa3`, 6.54.6 | Core SAETrainer supports custom/vision activations; the high-level LM runner is not the only training abstraction |
| ViT-Prisma | `64daf1425f7e5311844213fd0fb6f4127a30cd16`, source version 2.0.0 | PyPI currently has 0.1.4; use the pinned source and avoid its legacy SAELens 2.1.3 extra |
| Overcomplete | `a1781af49c6e4bbfdbfd763b9757bcf6c5dd6403`, 0.3.0 | Python <3.13; Matplotlib <3.9; pointwise SAE adapters preserve native training conventions |

SAELens snapshot source YAML SHA256 is
`bea73bf39c2a345ce03fca3d9d44e133085e9ff2aea74c8ae5b26de0819c96d2`.
The catalog contains 13,857 SAELens entries and 82 Prisma table entries (71 SAEs,
11 transcoders). Overcomplete has no central pretrained SAE registry; its
pretrained vision backbones are not presented as pretrained dictionaries.

## Measured verification

The default environment passes **288 tests and 182 subtests**, with 39 optional
integration cases skipped because their backend is absent or incompatible with
that environment. Separate compatible environments exercise the actual toolkits:
SAELens 22 tests, Prisma 26 tests and Overcomplete 15 tests pass. All eight
advertised SAELens training architectures and all six integrated Overcomplete
architectures complete small CPU training runs. The Prisma guide's full image
input, training, feature-overlay and intervention workflow was executed.

One official SAELens checkpoint (4.7 MB) and one official Prisma CLIP dictionary
(302 MB) were actually loaded and used for finite encode/decode checks. This
verifies dictionary numerics on test vectors; it does not establish transfer to
a different backbone, clinical interpretation or complete registry coverage.

Artifacts are consolidated under `runs/sae_backends_v2/`; the catalog can be
inspected in `catalog.html`. Provider-specific guides preserve training objectives,
validation policy, resume limits and exact implementation variants. No pathology
semantic performance claim is inferred from synthetic integration runs.

Wheel and source distribution `0.9.2.dev0` were built locally. Installing the
wheel into an independent target directory verifies the public imports, all
13,939 bundled records and discovery without importing optional upstream
packages. The catalog marks the two numerical checks separately and keeps
unknown compatibility fields unknown. The original checkout and remote branches
remain unchanged; this development branch is for local review.
