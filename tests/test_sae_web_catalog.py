"""Published web catalog coverage and deployment-context checks, stdlib only."""
import gzip
import importlib.util
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "docs/methods/sae/models/web"


def test_web_cards_preserve_every_published_model_and_exact_download():
    source = json.loads(gzip.decompress(
        (ROOT / "src/vlm_probing/sae/resources/published_model_cards.json.gz").read_bytes()))
    index = json.loads((WEB / "catalog-index.json").read_text())
    rows = {row[0]: row for row in index["rows"]}
    assert set(rows) == {card["id"] for card in source["models"]}
    shards = {path.stem: json.loads(path.read_text()) for path in (WEB / "cards").glob("*.json")}
    assert set().union(*(set(cards) for cards in shards.values())) == set(rows)
    for card in source["models"]:
        row = rows[card["id"]]
        assert index["base_models"][row[1]] == card["base_model"]
        assert index["methods"][row[2]] == card["method"]
        # This includes full source conventions, alias names, revisions and
        # direct file/config URLs, not just the fields shown in search results.
        assert shards[row[12]][card["id"]] == card


def test_html_shell_remains_small_and_metadata_is_loaded_on_demand():
    document = (WEB / "index.html").read_text()
    assert len(document.encode()) < 25_000
    assert "model-data" not in document
    assert "getJSON('catalog-index.json')" in document
    assert "getJSON('cards/'+model.shard+'.json')" in document
    assert len((WEB.parent / "catalog.html").read_bytes()) < 4_000
    assert max(path.stat().st_size for path in (WEB / "cards").glob("*.json")) < 600_000


def test_generation_context_can_target_the_lab_repository(tmp_path, monkeypatch):
    spec = importlib.util.spec_from_file_location("sae_model_pages", ROOT / "tools/build_sae_model_pages.py")
    generator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(generator)
    monkeypatch.setattr(generator, "DESTINATION", tmp_path)
    payload = json.loads(gzip.decompress(generator.RESOURCE.read_bytes()))
    sample = payload["models"][:2]
    generator.build_web(sample, {"sae_dictionaries": 2, "backbones": 0},
                        repository="ubc-tea/vlm-probe", ref="main",
                        site_url="https://ubc-tea.github.io/vlm-probe/sae-models/")
    document = (tmp_path / "web/index.html").read_text()
    assert "https://github.com/ubc-tea/vlm-probe/blob/main/" in document
    assert "gexinh/vlm-prob" not in document
    assert "https://ubc-tea.github.io/vlm-probe/sae-models/" in (tmp_path / "catalog.html").read_text()
    launcher_before = (tmp_path / "catalog.html").read_bytes()
    export = tmp_path / "deployment" / "sae-models"
    generator.build_web(sample, {"sae_dictionaries": 2, "backbones": 0},
                        repository="gexinh/vlm-prob", ref="main", output=export,
                        site_url="https://gexinh.github.io/vlm-prob/sae-models/")
    assert "https://github.com/gexinh/vlm-prob/blob/main/" in (export / "index.html").read_text()
    assert (export / "README.md").is_file()
    assert (tmp_path / "catalog.html").read_bytes() == launcher_before
    with pytest.raises(ValueError, match="owner/name"):
        generator.build_web(sample, {"sae_dictionaries": 2, "backbones": 0},
                            repository='bad/owner" onclick="oops', ref="main", site_url="https://example.org")
