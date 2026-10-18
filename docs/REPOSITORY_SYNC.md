# Laboratory and personal repositories

The laboratory repository is [ubc-tea/vlm-probe](https://github.com/ubc-tea/vlm-probe).
The personal mirror is [gexinh/vlm-probing](https://github.com/gexinh/vlm-probing).
Their `main` branches share the same commits, library, demos, input images and
current report. Develop and review one change, then publish it to both. Issues,
pull requests, GitHub Releases and repository settings are separate GitHub
objects; they are not duplicated by pushing commits.

## Synchronize an update

In a new checkout, configure these aliases once, preserving its existing `origin`:

```bash
git remote add personal git@github.com:gexinh/vlm-probing.git
git remote add lab git@github.com:ubc-tea/vlm-probe.git
```

If an alias already exists, inspect it with `git remote -v` rather than adding it
again. From the repository root on `main`, inspect or publish with:

```bash
python tools/sync_repositories.py
python tools/sync_repositories.py --push
```

The tool fetches both branches, checks that neither contains changes missing
locally, then fast-forwards both to one exact commit and verifies the remote
hashes. It never force-pushes or deletes refs. If someone edited either GitHub
copy, merge that remote's changes locally, review them, commit, and retry.
Publishing requires a clean working tree. Release tags can be pushed to both
remotes separately after reviewing the release.

This is an explicit synchronization command, not a background service. Two
remote writes cannot be atomic: a network failure or concurrent update can leave
one ahead. Fetch, inspect, and rerun after resolving the cause. Automatic GitHub
mirroring would additionally require a scoped GitHub App or another authorized
credential; a repository's default `GITHUB_TOKEN` cannot write to the other
repository. Do not copy an interactive login token into workflow secrets.

## One page per repository

- Lab: https://ubc-tea.github.io/vlm-probe/
- Personal: https://gexinh.github.io/vlm-probing/

The same Pages workflow renders repository links from `GITHUB_REPOSITORY` at
build time. Each deployed website links to its own code and documentation.
Recorded experimental measurements retain their original provenance. Both
websites include the same report PDF under `assets/vlmprobe-technical-report.pdf`.

A repository administrator must enable **Settings → Pages → Build and deployment
→ Source: GitHub Actions** in each repository. The personal repository already
uses this setting. The laboratory repository had Pages disabled when this
integration was prepared; the available account has push permission but no
administrator permission there. After enabling it, run **Actions → Deploy
project page → Run workflow** on `main`.

For a local build:

```bash
python tools/build_project_page.py --repository ubc-tea/vlm-probe --output /tmp/vlmprobe-lab-site
python tools/build_project_page.py --repository gexinh/vlm-probing --output /tmp/vlmprobe-personal-site
```

## One report and one PyPI package

The current reviewed PDF is [docs/assets/vlmprobe-technical-report.pdf](assets/vlmprobe-technical-report.pdf).
Its source commit and checksum are recorded in [report provenance](assets/report-provenance.json).
The standalone [LaTeX repository](https://github.com/gexinh/vlm-probing-report)
remains the report authoring source. Update and compile it first, then replace
the tracked PDF and provenance record. Local report sources and historical
experiments under `docs/report/` remain excluded from this library repository.

`pip install vlmprobe` downloads the published distribution from PyPI. It does
not read either GitHub `main` branch. One PyPI project suffices for both mirrors;
the release workflow remains bound to **gexinh/vlm-probing**, `package.yml`,
environment `pypi`. Only that repository can run the publish job. Ordinary pushes
build and test but do not publish. Before publishing a new release, increment
the package version and synchronize the reviewed source. A published PyPI file
cannot be replaced with a different file under the same version/filename.

## This integration

The goal is to place the library under the laboratory while preserving the
personal mirror, current report and existing installation name. Compared with
the previous version, this adds dual-remote synchronization, mirror-specific
Pages builds, a checked-in current PDF, and a single-publisher guard. It also
includes the already prepared attention-overlay improvement: the original image
is dimmed over an opaque heatmap. Probe values and model execution are unchanged.
Expected behavior is identical library commits and report hashes in both
repositories, working links to each site's own repository, and one shared PyPI
release stream.
