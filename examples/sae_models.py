"""Browse VLMProbe's native model cards; no weights are downloaded."""
from argparse import ArgumentParser
import json
from vlmprobe.sae import list_models

if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--modality", choices=["language", "vision", "multimodal", "activation"])
    parser.add_argument("--method")
    parser.add_argument("--status")
    parser.add_argument("--registry-dir")
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args()
    print(json.dumps(list_models(**vars(args)), indent=2))
