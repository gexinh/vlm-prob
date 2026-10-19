# Method API examples and main-branch integration (v4.3)

## Objective

Make the object lifecycle explicit in every method's API reference, then merge
the reviewed SAE implementation into main. Extend the approved four-stage
library diagram with SAE while preserving the previous figure files.
Previous version: `25420c7` on `dev/sae-v4`.

## Differences from v4.2

- Define each returned method object before calling its fitting, running or
  generation operations. Label argument signatures as API notation and link
  them to complete model/input/output examples.
- Add a valid configure/fit/run snippet to each of the 14 SAE method pages.
  Explain where its model and input variables are constructed. Keep the full
  independent scripts and their training/visualization workflow intact.
- Give grouped attention methods separate named objects. Define the activation
  EAP alternative explicitly and construct joint intervention methods before
  their forward/generate operations.
- Point Git installation instructions and generated model-card navigation at
  main. Update the renamed personal repository's project-page URL, shared
  synchronization tooling and release-workflow repository condition.
- Present all four method families on the project page. Keep the archived
  experiment controls and measurements unchanged.
- Create a new editable SVG, PNG and vector PDF overview with a fourth SAE
  Tools card, matching fit/load and feature outputs. Keep both original SVGs.

## Expected results

Readers can identify where `method` comes from and follow factory, fit/load and
run operations without an undefined object appearing. Every complete tutorial
remains executable. Personal and lab repositories retain the same code and
report, with their own README and deployed navigation links. Ordinary pushes
build and deploy documentation without publishing a new PyPI distribution.

The new figure should retain the existing Input, Configure, Tools and Output
structure and visual style, make all four branches legible, and export without
overlapping or clipped text. Its miniature plots are schematic, not new
experimental measurements.

## Validation

- CPU regression: **452 passed, 2 optional author-checkpoint tests skipped,
  179 subtests passed**.
- All 14 new SAE API usage snippets executed with their displayed complete
  example's model/input setup: each returned `[16,32]` held-out features after
  24 SAE training updates. The model remains frozen.
- All 20 non-SAE guide revisions passed syntax, object-lifecycle and anchored
  complete-example checks. Their complete executable examples are unchanged.
- All 11 repository synchronization tests pass, including actual disposable
  bare remotes, renamed repository links and preserved lab history.
- Browser validation covers the four-family page, small-screen layout,
  catalog navigation and the existing archived Attention Knockout controls.
- The new diagram's four branch connections, actual text bounds and vector/
  raster exports were checked. Original figure files remain byte-identical.

## Scope

This revision changes documentation, publication tooling and presentation. SAE
mathematics, weights, training defaults and inference contracts are unchanged.
The existing package version remains `0.9.4.dev2`; merging main does not publish
it to PyPI. The technical report's PDF and authoring source are unchanged.
