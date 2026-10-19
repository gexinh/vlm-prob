"""The one-page directory preserves backbone and checkpoint discovery."""
import gzip
import importlib.util
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("sae_directory", ROOT / "tools/build_sae_model_pages.py")
PAGES = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PAGES)


def test_directory_groups_every_backbone_on_the_same_page_without_losing_repositories():
    payload = json.loads(gzip.decompress(PAGES.RESOURCE.read_bytes()))
    cards = [card for card in payload["models"] if card["artifact_kind"] == "sae"]
    rendered = PAGES.repository_index(payload["models"])
    assert rendered == (PAGES.DESTINATION / "published/README.md").read_text()
    models = {card["base_model"] for card in cards}
    anchors = re.findall(r'<a id="([^"]+)"></a>', rendered)
    assert len(anchors) == len(set(anchors)) == len(models)
    for model in models:
        assert f'[{model}](#{PAGES.model_anchor(model)})' in rendered
        assert f'#### {model}\n' in rendered
    for repo in {card["download"]["repo_id"] for card in cards}:
        assert f'https://huggingface.co/{repo}' in rendered
    for relative in re.findall(r'\]\(([^\s)]+\.md#[^\s)]+)\)', rendered):
        path, anchor = relative.split("#", 1)
        destination = PAGES.DESTINATION / "published" / path
        assert destination.exists(), relative
        assert f'<a id="{anchor}"></a>' in destination.read_text(), relative
    assert "### CLIP\n" in rendered and "### DINO\n" in rendered
    assert "**Vanilla SAEs (All Patches)**" in rendered
    assert "**Top K SAEs (CLS only, k = 64)**" in rendered
    assert "unclassified" not in rendered and "Pages |" not in rendered


def test_directory_layer_ranges_do_not_fill_missing_layers():
    assert PAGES.layer_summary([{"layer": index} for index in (0, 1, 2, 4, 6, 7, 8)]) == "0–2, 4, 6–8"
    assert PAGES.layer_summary([{"layer": None}]) == "—"
    assert PAGES.layer_summary([{"layer": 0}, {"layer": None}]) == "0, unspecified"


def test_vision_directory_does_not_invent_missing_features_or_method():
    card = {
        "id": "test-card", "artifact_kind": "sae", "base_model": "facebook/dino-vitb16",
        "layer": 0, "hook": "blocks.0.hook_resid_post", "method": "unknown",
        "dimensions": {"features": None}, "input_conventions": {},
        "download": {"repo_id": "author/test"},
        "links": {"card": "docs/methods/sae/models/published/test-p1.md#test-card",
                  "checkpoint": "https://huggingface.co/author/test/resolve/main/weights.pt"},
    }
    rendered = PAGES.repository_index([card])
    assert "| 0 | `resid_post` | — | — | [Model card]" in rendered
    assert "https://huggingface.co/author/test/resolve/main/weights.pt" in rendered
