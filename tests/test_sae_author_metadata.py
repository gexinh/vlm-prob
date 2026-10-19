"""Published cards retain the algorithm and activation site in author configs."""
import gzip
import hashlib
import json
from pathlib import Path

import pytest

from vlmprobe.sae import get_model_card, list_models


ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("card_id,method,model,layer,width,features", [
    ("sae-21911514d66bc703e7143b75", "gated", "pythia-70m-deduped", 3, 512, 4096),
    ("sae-2c2c35702492e87a6b39f81e", "batchtopk", "meta-llama/Llama-3.1-8B-Instruct", 11, 4096, 131072),
    ("sae-cbd3b7eaf315451abbf902c4", "matryoshka_batchtopk", "gemma-2-2b", 12, 2304, 4096),
])
def test_featured_cards_report_author_algorithm_and_activation_site(card_id, method, model, layer, width, features):
    card = get_model_card(card_id)
    assert card["method"] == method
    assert card["base_model"] == model
    assert card["layer"] == layer
    assert card["hook"] == f"resid_post_layer_{layer}"
    assert card["dimensions"] == {"activation": width, "features": features}
    assert card["id"] in {row["id"] for row in list_models(method=method)}
    assert card["loading"]["mode"] == "download_and_convert"
    revision = card["download"]["revision"]
    assert len(revision) == 40
    assert f"/resolve/{revision}/" in card["links"]["config"]


def test_published_config_evidence_preserves_verbatim_source_and_exact_dictionary_identity():
    evidence = json.loads(gzip.decompress((ROOT / "tools/data/sae_author_configs.json.gz").read_bytes()))
    for record in evidence["records"]:
        content = record["content"].encode()
        assert hashlib.sha256(content).hexdigest() == record["sha256"]
        card = get_model_card(record["id"])
        assert card["source_configuration"] == json.loads(content)
        assert card["origin"]["source_model_id"] == json.loads(content)["trainer"]["lm_name"]
        assert card["download"]["repo_id"] == record["repo_id"]
        assert card["download"]["path"] + "/config.json" == record["path"]
        assert card["download"]["revision"] == record["revision"]
        assert card["links"]["config"] == record["url"]
        assert card["evidence"]["author_config"]["sha256"] == record["sha256"]
