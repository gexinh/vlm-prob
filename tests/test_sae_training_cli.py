"""The portable-cache CLI exposes every native method and the same protocol."""
import importlib.util
import json
from pathlib import Path

import pytest
import torch

from vlmprobe.sae.models import ARCHITECTURES


@pytest.fixture
def cli(monkeypatch):
    path = Path(__file__).resolve().parents[1] / "examples" / "train_sae.py"
    spec = importlib.util.spec_from_file_location("native_sae_training_cli", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    monkeypatch.setattr(torch, "set_num_threads", lambda count: None)
    return module


def bundle(tmp_path):
    generator = torch.Generator().manual_seed(31)
    values = {split: torch.randn(count, 4, generator=generator)
              for split, count in (("train", 32), ("validation", 12), ("test", 12))}
    path = tmp_path / "activations.pt"
    torch.save({"binding": {"model_id": "random-tiny-cli@1", "tokenizer_id": "none@vectors",
                            "preprocessing_id": "raw-v1", "calibration_id": "split-v1",
                            "site": "residual.0", "layer": 0,
                            "hook": {"module": "layers.0", "kind": "output",
                                     "selector": None, "tensor_slice": None}},
                "groups": {split: [split + "-source"] * len(raw) for split, raw in values.items()},
                **values}, path)
    return path


@pytest.mark.parametrize("architecture", ARCHITECTURES)
def test_cli_all_methods_use_native_config_and_precise_vector_budget(cli, tmp_path, architecture, capsys):
    activation_path = bundle(tmp_path)
    recipe = tmp_path / "recipe.json"
    recipe.write_text(json.dumps({"auxk_coefficient": 0., "k": 2}))
    output = tmp_path / "fit"
    cli.main(["--activations", str(activation_path), "--output-dir", str(output),
              "--method", architecture, "--d-sae", "12", "--k", "3",
              "--method-config", str(recipe), "--batch-size", "16", "--max-vectors", "19",
              "--device", "cpu", "--progress-every", "1"])
    assert json.loads(capsys.readouterr().out)["state"] == "complete"
    metrics = json.loads((output / "metrics.json").read_text())
    assert metrics["configuration"]["architecture"] == architecture
    assert metrics["configuration"]["k"] == 2
    assert metrics["budget"] == {"unit": "vectors", "target": 19}
    assert metrics["test"]["positions"] == 12
    history = json.loads((output / "history.json").read_text())
    assert history["training_vectors"] == 19
    assert history["completed_steps"] == 2
    assert history["normalization"]["positions"] == 32


def test_cli_rejects_identity_replacement_and_unknown_recipe_fields(cli, tmp_path):
    activation_path = bundle(tmp_path)
    recipe = tmp_path / "recipe.json"
    arguments = ["--activations", str(activation_path), "--output-dir", str(tmp_path / "fit"),
                 "--method", "topk", "--d-sae", "12", "--k", "3",
                 "--method-config", str(recipe), "--max-steps", "1", "--device", "cpu"]
    recipe.write_text(json.dumps({"d_in": 300}))
    with pytest.raises(SystemExit):
        cli.main(arguments)
    recipe.write_text(json.dumps({"not_an_sae_option": 3}))
    with pytest.raises(TypeError, match="unexpected keyword"):
        cli.main(arguments)
    assert not (tmp_path / "fit").exists()
