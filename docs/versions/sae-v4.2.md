# SAE inference and model browsing (v4.2)

## Objective

Make the distinction between training a dictionary and using an existing one
clear in every SAE method guide. Provide a complete inference-only path and
replace the oversized GitHub HTML catalog with usable model discovery.
Previous version: `388e7af` on `dev/sae-v4`; package version: `0.9.4.dev2`.

## Differences from v4.1

- Link every method guide to a shared pretrained loading guide. Explain that
  `.fit(...)` trains the SAE on frozen backbone activations, while loading and
  `.run(...)` perform inference. The tiny random ViT examples remain explicitly
  labeled API demonstrations rather than pretrained semantic analyses.
- Add a bounded automatic published-checkpoint loading path. Preserve the
  checkpoint's exact recipe, activation hook, backbone and tokenizer; reject
  unsupported conversion recipes and mismatches rather than infer compatibility
  from vector dimensions alone.
- Correct legacy TopK/normalization conversion and the directory links in the
  GPT-2 OAI v5 collection. Keep author weight provenance and pinned revisions.
- Make tokenizer identities portable across cache directories while retaining
  vocabulary, merge/normalization rules and behavior-affecting options. Keep
  complete recipe and converted-state checks on reusable pretrained artifacts.
- Keep the GitHub-readable repository index and paginated Markdown model cards
  as the immediate browsing path. Retire the 4 MB embedded-data HTML file.
- Generate a small searchable web interface, a separate search index and
  on-demand detail shards. Include it at `/sae-models/` in each repository's
  normal Pages build, with repository-specific navigation and Markdown links.
- Provide local HTTP browsing instructions. Publishing the hosted catalog
  follows the existing main-branch deployment policy; this review branch does
  not change that policy or update main.

## Expected results

A reader with a compatible trained SAE can analyze new inputs without calling
`.fit(...)`. A supported author recipe can be downloaded and converted through
the same model-bound interface with no upstream SAE toolkit dependency. Saved
features, reconstruction and feature editing retain existing native contracts.
Invalid source/model/tokenizer combinations must fail explicitly.

Model cards must be readable on GitHub and searchable in an ordinary browser.
Selecting a card should fetch only its detail shard. Both personal and lab
Pages builds should point back to their own repository without mutating source
documentation. Existing numerical, artifact, training and integration checks
must continue to pass.

## Validation

- Complete CPU regression suite: **449 passed, 2 optional author-checkpoint
  tests skipped, 179 subtests passed**. New checks cover inference-only loading,
  source checksums, backbone/tokenizer mismatch, cache reuse and invalidation,
  edited-dictionary integrity, and cache-directory portability.
- Both exact Python examples in the loading guide ran against published GPT-2
  and OAI TopK SAE weights. The first produced `[10,32768]` features and exactly
  32 active features per token, with raw reconstruction MSE `0.0619781`; the
  saved native dictionary also ran reconstruction and feature ablation on fresh
  input. Both used zero training updates. Actual figure and pinned-weight/code/
  figure checksums are recorded under `docs/assets/tutorials/`.
- The independent native block-0 capture check and source dictionary equations
  agree within explicit FP32 tolerances on actual activations. These are source
  formula/native-hook checks; no execution of TransformerLens or an upstream
  SAE SDK is claimed. Cached repeat inference is bitwise equal.
- All 9,660 dictionary cards and five separately typed backbone records are
  preserved in the Markdown pages, search index and 64 detail shards. Browser
  checks exercise search, combined filters, direct card fragments, missing IDs,
  lazy detail requests and correct per-repository links. The HTML shell is
  about 13 KB and the old 4 MB file is an approximately 1 KB launcher.
- Personal and lab project-page builds succeed with repository-specific links
  and without rewriting source documentation. The catalog is prepared for the
  existing main-branch Pages workflow; it is not deployed from this branch.
- Wheel/source distribution build and strict Twine metadata checks pass. The
  installed wheel exposes the complete catalog, all 14 native methods and the
  pretrained recipe, and runs fitting/loading/inference without importing an
  official SAE toolkit. Published-weight inference is also checked from the
  installed wheel.

## Scope

The published model catalog aggregates author metadata and weight links; it is
not a promise of automatic conversion for every checkpoint format. Automatic
loading only accepts implemented source recipes. A successful frozen-model
inference example and numerical conversion checks do not establish semantic
feature quality, pathology-domain performance or a new SAE training result.
The original checkout, personal main, lab main and PyPI release are unchanged.
