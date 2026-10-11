# Installation and package releases

[Home](../README.md) / [Documentation](README.md)

The installable distribution and recommended Python import are **`vlmprobe`**.
The project and repository remain **VLM Probing** and **`gexinh/vlm-probing`**.

## Install and import

Install from GitHub without cloning the repository yourself:

```bash
python -m pip install "vlmprobe[transformers,visualization] @ git+https://github.com/gexinh/vlm-probing.git"
```

```python
import vlmprobe
from vlmprobe import Prober, TokenMargin, visualization as viz

probe = Prober(model, processor)  # caller-owned model and native processor
result = probe.lens.logit(tokens="last_prompt").run(inputs)
```

Native model inputs, adapter checks, metrics, fitting, and visualization retain
the [common API](API.md). Importing the base package requires PyTorch; plotting
and Hugging Face dependencies are loaded only when those features are used.

| Extra | Adds |
| --- | --- |
| `visualization` | Matplotlib, NumPy, and Pillow for built-in plots. |
| `transformers` | Supported Transformers 5.3.x, Accelerate, Torchvision, and Pillow. |
| `notebooks` | Jupyter and the plotting/tokenizer tools used by demos. |

For a pinned experiment, append a commit or release tag to the Git URL, using
[pip's VCS syntax](https://pip.pypa.io/en/stable/topics/vcs-support/).

## Compatibility

`vlm_probing` remains an import alias to the same implementation. Both import
names share the exact classes, submodules, adapter registry, and serialized
types; there are no separate copies of the algorithms. Advanced imports work
under either spelling, for example `vlmprobe.adapters` or
`vlmprobe.training.jacobian`.

The old distribution was called `vlm-probing`. If it is already installed,
remove that distribution before installing `vlmprobe`, because both releases
contain the compatibility namespace:

```bash
python -m pip uninstall vlm-probing
```

Existing source imports and saved results do not need to be rewritten.

## Build a release

From the repository root:

```bash
python -m pip install build twine
python -m build
python -m twine check --strict dist/*
```

`dist/` contains a wheel and source distribution. The wheel installs the
library and third-party notices. Model weights, datasets, report/slides,
experiment archives, and notebook outputs are excluded. Demos and their input
images remain available in the GitHub repository.

The version has one source: `vlm_probing.__version__`. Setuptools reads that
constant to create distribution metadata; `vlmprobe.__version__` exposes the
same value. The source distribution is sufficient to rebuild the wheel.

## First PyPI publication

Until the first publication completes, use the GitHub install command above.
After publication, users can install with:

```bash
python -m pip install "vlmprobe[transformers,visualization]"
```

The repository includes a GitHub Actions workflow named **Build and publish
Python package** (`.github/workflows/package.yml`). Pushes and pull requests
only build and test the package on Python 3.10 and 3.12. Publishing is a manual
workflow action, using PyPI's token-free trusted publishing.

For a new project, a maintainer must first create a
[pending trusted publisher](https://docs.pypi.org/trusted-publishers/creating-a-project-through-oidc/)
in their PyPI account with these values:

| Field | Value |
| --- | --- |
| PyPI project name | `vlmprobe` |
| GitHub owner | `gexinh` |
| Repository | `vlm-probing` |
| Workflow filename | `package.yml` |
| Environment | `pypi` |

Create the matching GitHub repository environment `pypi`. In **Actions → Build
and publish Python package → Run workflow**, choose `main` and set
`publish_target` to `pypi`. The workflow publishes only after both build/test
jobs succeed. Its OIDC permission belongs only to the publish job; no PyPI API
token is stored in the repository.

To test publication first, repeat the trusted-publisher setup on **TestPyPI**
with environment `testpypi`, then select `testpypi` in the workflow. TestPyPI
accounts and projects are separate from PyPI. An index refuses overwriting an
already published version; increment the version for later releases.
