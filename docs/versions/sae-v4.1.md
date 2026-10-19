# SAE documentation and published model catalog (v4.1)

## Objective

Present SAE through the same reader-facing method documentation as Lens,
Attention and Causal. Aggregate published checkpoint information into VLMProbe
model-card pages with direct model/weight links. Previous version: `cc72ff2`
on `dev/sae-v4`.

## Differences from v4

- Move SAE documentation from `docs/sae/` into `docs/methods/sae/`.
- Link each SAE algorithm directly from the README method table; remove the
  standalone SAE preview, family-order explanations and development narrative.
- Give each method its own API/default/parameter guide and executable input-to-
  training-to-visualization example, linked to shared models/training guides.
- Publish our own model-card pages for released author weights. Source provenance
  and actual download links remain explicit; inclusion is not represented as a
  new end-to-end reproduction or arbitrary-backbone compatibility claim.
- Keep pretrained SAE dictionaries distinct from vision backbones used to train
  dictionaries. Checkpoint formats still enter the native runtime through
  explicit import, with exact model/hook/preprocessing binding.
- Remove the empty-public-registry policy and the candidate/validated split from
  reader-facing discovery. Keep native training/feature/edit behavior unchanged.

## Expected results

Readers can choose a method in one click, find every argument and run a complete
example. They can browse model cards hosted in this repository and follow direct
checkpoint links, or use the common training protocol on their own data.
Documentation links must resolve after moving the subtree. All displayed SAE
examples must execute and produce saved results and plots. Existing numerical,
training, intervention and artifact checks must continue to pass.

## Validation

- Full CPU regression suite: **430 passed, 2 optional author-checkpoint tests
  skipped, 178 subtests passed**. Numerical training/intervention/artifact
  behavior remains unchanged by this revision.
- All **14 displayed method examples** were extracted from their Markdown and
  executed: each performs 24 native training steps on 96 captured training
  positions, validates on 32 independent positions, computes held-out `[16,32]`
  features, saves plots and checks exact saved-state equality plus explicit
  numerical feature tolerances after reload. Code/image hashes are recorded in
  `docs/assets/tutorials/sae-examples-provenance.json`.
- Navigation checks cover every README method link, API/example/shared-resource
  links, the new hierarchy, and all local documentation/image destinations.
- Catalog checks cover **9,660 distinct SAE checkpoints** across **151 weight
  repositories**, merging 429 aliases from 10,089 published listing rows.
  Every card has our own page/anchor and a direct checkpoint repository/file
  link. Five separately typed pretrained vision backbones are also included.
- Model pages are reproducible with `tools/build_sae_model_pages.py`: 307
  paginated repository pages, an index, backbone cards and a standalone search
  page. JSON/rendering/search/method/modality/resource filters were executed
  successfully. The generator removes obsolete generated pages on refresh.
- Source distribution/wheel build and strict Twine metadata checks pass. A
  separately installed wheel exposes the complete packaged catalog and all 14
  native methods, and performs live ViT fitting, feature readout, save/load and
  an exact no-op edit while official SAE library imports are blocked in the
  verification process.
- A final documentation/catalog check passes 12 tests after page regeneration.
  Shared model/training pages contain reader-facing usage rather than version
  history or an empty-registry policy.

## Scope

The catalog aggregates author-published weight information; it does not claim
newly trained weights or automatic conversion of every external format.
Reported model, hook, image/normalization settings, licenses and available
revisions/checksums are retained. Unreported fields remain unspecified.
Transcoders/temporal dictionaries have different activation contracts and are
outside this same-space catalog. Overcomplete supplies five documented
activation-extraction backbone resources in the audited source, alongside its
training methods; these are explicitly typed separately from SAE weights.

The method examples use random tiny ViT weights and synthetic images to teach
the complete API. They establish executable workflows, not semantic concept
quality or benchmark performance. The original checkout and main branch remain
unchanged; the review continues on `dev/sae-v4`.
