"""Architecture and tokenization identities must describe the actual IO contract."""
import copy
import json
from pathlib import Path
import sys
from types import SimpleNamespace

import pytest
import torch
from torch import nn

from vlmprobe.sae.data import ActivationCollector, model_identity, processor_identity


class Model(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = nn.Linear(3, 3)
        self.activation = nn.GELU()
        self.norm = nn.LayerNorm(3, eps=1e-5)
        self.config = SimpleNamespace(hidden_size=3, epsilon=1e-5, _name_or_path="/cache/one")

    def forward(self, value):
        return self.norm(self.activation(self.linear(value)))


def test_same_tensors_with_different_activation_or_epsilon_do_not_share_identity():
    original = Model()
    changed = copy.deepcopy(original)
    changed.activation = nn.ReLU()
    assert all(torch.equal(value, changed.state_dict()[name]) for name, value in original.state_dict().items())
    assert model_identity(original) != model_identity(changed)
    changed = copy.deepcopy(original)
    changed.norm.eps = .1
    assert model_identity(original) != model_identity(changed)
    changed = copy.deepcopy(original)
    changed.config.epsilon = .2
    assert model_identity(original) != model_identity(changed)


def test_identity_ignores_training_flags_cache_paths_and_device_map_but_hashes_weights():
    original = Model()
    changed = copy.deepcopy(original)
    original.train(); changed.eval()
    changed.config._name_or_path = "/different/cache"
    changed.hf_device_map = {"": "cuda:3"}
    changed.warnings_issued = {"already_warned": True}
    assert model_identity(original) == model_identity(changed)
    with torch.no_grad():
        changed.linear.weight[0, 0] += .1
    assert model_identity(original) != model_identity(changed)


class Backend:
    def __init__(self, lowercase=False):
        self.lowercase, self.padding = lowercase, None

    def to_str(self):
        return json.dumps({"normalizer": {"type": "Lowercase"} if self.lowercase else None,
                           "model": {"type": "WordLevel", "vocab": {"hello": 1}},
                           "padding": self.padding, "truncation": None})


class Tokenizer:
    def __init__(self, lowercase=False):
        self.backend_tokenizer = Backend(lowercase)
        self.special_tokens_map = {"unk_token": "[UNK]"}
        self.chat_template = None

    def get_vocab(self):
        return {"[UNK]": 0, "hello": 1}


def test_tokenizer_backend_normalizer_is_not_replaced_by_vocabulary_only_identity():
    first, second = Tokenizer(), Tokenizer(True)
    assert first.get_vocab() == second.get_vocab()
    assert processor_identity(first) != processor_identity(second)
    before = processor_identity(first)
    first.backend_tokenizer.padding = {"length": 32}
    assert processor_identity(first) == before  # per-call HF padding is recorded by prepared inputs instead.


def test_slow_bpe_merges_and_explicit_image_processor_are_part_of_identity():
    first, second = Tokenizer(), Tokenizer()
    first.bpe_ranks = {("a", "b"): 0, ("b", "c"): 1}
    second.bpe_ranks = {("a", "b"): 1, ("b", "c"): 0}
    assert processor_identity(first) != processor_identity(second)

    class ImageProcessor:
        def __init__(self, mean):
            self.mean = mean

        def to_dict(self):
            return {"image_mean": self.mean, "crop_size": [224, 224]}

    class Processor:
        def __init__(self, mean):
            self.tokenizer, self.image_processor = Tokenizer(), ImageProcessor(mean)

        def to_dict(self):
            return {"processor_class": "custom"}  # deliberately omits the image transform.

    assert processor_identity(Processor([.5] * 3)) != processor_identity(Processor([.4] * 3))


def test_real_fast_tokenizer_collision_regression():
    tokenizers = pytest.importorskip("tokenizers")
    transformers = pytest.importorskip("transformers")
    def tokenizer(lowercase):
        backend = tokenizers.Tokenizer(tokenizers.models.WordLevel({"[UNK]": 0, "hello": 1}, unk_token="[UNK]"))
        backend.pre_tokenizer = tokenizers.pre_tokenizers.Whitespace()
        if lowercase:
            backend.normalizer = tokenizers.normalizers.Lowercase()
        return transformers.PreTrainedTokenizerFast(tokenizer_object=backend, unk_token="[UNK]")
    first, second = tokenizer(False), tokenizer(True)
    assert first("HELLO")["input_ids"] != second("HELLO")["input_ids"]
    assert processor_identity(first) != processor_identity(second)


def test_activation_collection_restores_distinct_loader_sampler_and_global_rng_even_on_error():
    from torch.utils.data import DataLoader, RandomSampler
    from vlmprobe import Prober
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "examples"))
    from tiny_model import TinyModel
    torch.manual_seed(16)
    torch.set_num_threads(1)
    probe = Prober(TinyModel())
    rows = [{"input_ids": torch.tensor([i, 2, 3]), "image_tokens": torch.randn(2, 6)} for i in range(1, 6)]
    loader_rng = torch.Generator().manual_seed(41)
    sampler_rng = torch.Generator().manual_seed(53)
    loader = DataLoader(rows, batch_size=1,
        sampler=RandomSampler(rows, generator=sampler_rng), generator=loader_rng)
    global_before = torch.get_rng_state().clone()
    loader_before, sampler_before = loader_rng.get_state().clone(), sampler_rng.get_state().clone()
    collector = ActivationCollector(probe, 0, "all")
    first, first_meta = collector.collect(loader)
    second, second_meta = collector.collect(loader)
    assert torch.equal(first, second)
    assert first_meta["input_hashes"] == second_meta["input_hashes"]
    assert torch.equal(torch.get_rng_state(), global_before)
    assert torch.equal(loader_rng.get_state(), loader_before)
    assert torch.equal(sampler_rng.get_state(), sampler_before)
    with pytest.raises(ValueError, match="max_cache_bytes"):
        ActivationCollector(probe, 0, "all", max_cache_bytes=1).collect(loader)
    assert torch.equal(torch.get_rng_state(), global_before)
    assert torch.equal(loader_rng.get_state(), loader_before)
    assert torch.equal(sampler_rng.get_state(), sampler_before)
