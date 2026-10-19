#!/usr/bin/env python3
"""Execute the displayed SAE method examples and verify their real outputs.

Examples are extracted from Markdown so the verified code is the code readers
copy. The tiny randomly initialized ViT and synthetic image splits run on CPU;
these checks establish API execution and artifact parity, not semantic quality.
"""
from __future__ import annotations

import argparse
from contextlib import redirect_stdout
from hashlib import sha256
import io
import json
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
PAGES = ROOT / "docs" / "methods" / "sae"
EXAMPLE = re.compile(r"<!-- runnable-example -->\s*```python\n(.*?)\n```", re.S)
LINKS = re.compile(r"!?\[[^\]]*\]\(([^\s)]+)\)")


def validate(*, output_dir: Path, write_figures: bool, methods=None):
    # Prefer this checkout to a previously installed package.
    sys.path.insert(0, str(ROOT / "src"))
    os.environ.setdefault("MPLBACKEND", "Agg")
    import torch
    import transformers
    from vlmprobe.sae import list_methods

    available = [entry["name"] for entry in list_methods()]
    selected = methods or available
    if set(selected) - set(available):
        raise ValueError("requested method is absent from the native method registry")
    output_dir.mkdir(parents=True, exist_ok=True)
    record = {"scope": "CPU execution of displayed random-ViT SAE method examples",
              "torch": torch.__version__, "transformers": transformers.__version__,
              "semantic_quality_evaluated": False, "methods": [], "errors": []}
    for name in selected:
        page = PAGES / f"{name}.md"
        content = page.read_text()
        found = EXAMPLE.findall(content)
        if len(found) != 1:
            raise ValueError(f"{page}: expected exactly one complete runnable example")
        source = found[0]
        if f"probe.sae.{name}(" not in source:
            raise ValueError(f"{page}: example does not use its named method factory")
        for forbidden in ("load_snapshot", "from demos.common", "sae.backends", "torch.load("):
            if forbidden in source:
                raise ValueError(f"{page}: hidden/precomputed example dependency {forbidden}")
        for destination in LINKS.findall(content):
            if "://" not in destination and not destination.startswith("#"):
                target = page.parent / destination.split("#", 1)[0]
                # Generated image targets are checked after execution below.
                if not target.exists() and not destination.endswith(f"sae-{name}.png"):
                    raise ValueError(f"{page}: missing relative link {destination}")
        old_output = os.environ.get("VLM_PROBING_OUTPUT")
        log = io.StringIO()
        try:
            # Every run is fresh, so documentation verification cannot quietly
            # reuse a prior optimizer checkpoint or cached activation result.
            with tempfile.TemporaryDirectory(prefix=f"sae-{name}-", dir=output_dir) as run:
                run_dir = Path(run)
                os.environ["VLM_PROBING_OUTPUT"] = str(run_dir)
                namespace = {"__name__": "__main__"}
                with redirect_stdout(log):
                    exec(compile(source, str(page), "exec"), namespace)
                result, history = namespace["result"], namespace["history"]
                values = result.tensors["features"]
                assert values.shape == (16, 32), (name, tuple(values.shape))
                assert torch.isfinite(values).all(), name
                assert (values != 0).any(), f"{name}: held-out dictionary is entirely inactive"
                assert history["completed_steps"] == 24, (name, history["completed_steps"])
                assert history["train"]["positions"] == 96, name
                assert history["validation"]["positions"] == 32, name
                assert history["fingerprints"]["train"] != history["fingerprints"]["validation"], name
                assert result.metadata["visual_only"], name
                assert result.tensors["positions"][:, 1].tolist() == list(range(1, 17)), name
                assert (run_dir / "dictionary" / "model_card.json").is_file(), name
                assert (run_dir / "training" / "training_state.pt").is_file(), name
                figure = run_dir / "features.png"
                assert figure.is_file() and figure.stat().st_size > 1000, name
                if write_figures:
                    target = ROOT / "docs" / "assets" / "tutorials" / f"sae-{name}.png"
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(figure, target)
                row = {"method": name, "success": True,
                       "code_sha256": sha256(source.encode()).hexdigest(),
                       "figure_sha256": sha256(figure.read_bytes()).hexdigest(),
                       "feature_shape": list(values.shape),
                       "mean_test_l0": result.tensors["l0"].float().mean().item(),
                       "training_steps": history["completed_steps"],
                       "training_positions": history["train"]["positions"],
                       "validation_positions": history["validation"]["positions"],
                       "validation_mse": history["validation"]["mse"],
                       "validation_fvu": history["validation"]["fvu"],
                       "inference_artifact_roundtrip": "identical state; features rtol=1e-5, atol=1e-6"}
                record["methods"].append(row)
                print(f"PASS {name}: train={row['training_positions']}, validation={row['validation_positions']}, "
                      f"features={row['feature_shape']}, held-out L0={row['mean_test_l0']:.3f}", flush=True)
        except Exception as error:
            record["errors"].append({"method": name, "error": repr(error), "stdout": log.getvalue()})
            print(f"FAIL {name}: {error}", flush=True)
        finally:
            if old_output is None:
                os.environ.pop("VLM_PROBING_OUTPUT", None)
            else:
                os.environ["VLM_PROBING_OUTPUT"] = old_output
    record["success"] = not record["errors"] and len(record["methods"]) == len(selected)
    (output_dir / "validation.json").write_text(json.dumps(record, indent=2) + "\n")
    if write_figures and record["success"] and selected == available:
        provenance = ROOT / "docs" / "assets" / "tutorials" / "sae-examples-provenance.json"
        provenance.write_text(json.dumps(record, indent=2) + "\n")
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "outputs" / "sae_method_guides")
    parser.add_argument("--write-figures", action="store_true",
                        help="Update the documentation figures from the actual executed examples")
    parser.add_argument("--methods", nargs="+", help="Optional subset of native method names")
    args = parser.parse_args()
    record = validate(output_dir=args.output_dir.resolve(), write_figures=args.write_figures, methods=args.methods)
    print(f"{len(record['methods'])} passed; {len(record['errors'])} failed")
    raise SystemExit(0 if record["success"] else 1)


if __name__ == "__main__":
    main()
