# Laboratory and personal repositories

The laboratory repository is [ubc-tea/vlm-probe](https://github.com/ubc-tea/vlm-probe).
The personal mirror is [gexinh/vlm-probing](https://github.com/gexinh/vlm-probing).
Their `main` branches share the same library, version, demos, input images and
current report. Each README displays only its own repository's project page and
navigation links. These README differences require separate commits; every
other file remains identical. Develop and review one change, then publish it to both. Issues,
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

Use the personal checkout as the shared editing source. The tool fetches both
branches and checks for unmerged remote changes before publishing. It renders
the lab README with lab URLs, preserves both histories, and verifies that only
README.md differs between the published trees. It never force-pushes or deletes
refs. If someone edited either GitHub copy, merge that remote's changes locally,
review them, commit, and retry.
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
→ Source: GitHub Actions** in each repository. After enabling it, run
**Actions → Deploy project page → Run workflow** on `main`.

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

The goal is to keep the library and report synchronized while presenting each
repository independently. Compared with the initial synchronization, each
README now contains one project-page button, no cross-repository explanation,
and links to its own documentation. The sync command preserves these URL
differences instead of requiring identical commit hashes. Expected behavior is
identical code, package versions and report hashes; only README URLs differ.
The existing Pages build and single PyPI publishing source continue to apply.
