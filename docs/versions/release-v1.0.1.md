# Release 1.0.1

## Objective

Publish the current library to PyPI and synchronize its source, documentation,
project page and latest technical report to Hugging Face.

## Differences from the previous version

- Advance the package version from 1.0.0 to 1.0.1, preserving the published
  1.0.0 tags and artifacts.
- Include the method-formula fixes, backbone-grouped model directory and
  author-configuration metadata corrections committed after 1.0.0.
- Update the README installation version and add patch-release notes.
- Use the same reviewed source commit for PyPI publication and the Hugging
  Face export; retain the personal/laboratory repository synchronization.

## Expected results

Both import names and installed distribution metadata report 1.0.1. The PyPI
distribution includes all 14 SAE algorithms and 9,660 checkpoint records. The
Hugging Face source and static catalog match the reviewed release and retain
the current report PDF. Numerical methods and training defaults remain those
of the reviewed implementation.

## Validation

The complete CPU suite passes 459 tests and 179 subtests, with two optional
author-checkpoint tests skipped. Distribution builds, installed-package checks
and remote artifact verification are performed during publication.
