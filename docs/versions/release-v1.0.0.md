# Release 1.0.0

## Objective

Publish the reviewed four-family library as GitHub release `v1.0.0`, using one
version for the public import and installable wheel/source distribution.
Previous main commit: `967e2dd`; previous package version: `0.9.4.dev2`.

## Differences from the previous version

- Set the single package version source to `1.0.0` and align the personal
  repository metadata with its current `gexinh/vlm-prob` name.
- Pin the README Git installation command to the reviewed `v1.0.0` tag.
- Add reader-facing release notes summarizing changes since the previous
  public `0.9.0` release. Preserve earlier release/version records as history.
- Build one wheel and source distribution for the personal and lab releases;
  attach the current report without modifying its contents.

## Expected results

Both import names and installed distribution metadata report `1.0.0`. The
existing methods, numerical outputs, training defaults and saved artifacts
remain unchanged. Both GitHub repositories expose `v1.0.0` as their latest
release, with matching package/report assets and preserved repository histories.
PyPI publication and Hugging Face synchronization remain separate operations;
creating this GitHub release does not silently perform either upload.

## Validation

- Complete CPU suite: **452 passed, 2 optional author-checkpoint tests skipped,
  179 subtests passed**.
- Wheel and source distribution build successfully and pass strict Twine checks.
- An installed-wheel check outside the repository confirms both imports report
  `1.0.0`, all 14 native SAE methods and 9,660 dictionary cards are packaged,
  and a live ViT fit/run/save/load workflow succeeds. All five installed-wheel
  namespace, serialization and computation-compatibility tests also pass.
- Remote tags, latest-release metadata and asset checksums are checked after
  publication; GitHub main and lab trees remain identical except README links.
