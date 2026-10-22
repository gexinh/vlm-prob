"""Target-independent attention methods must not silently accept target scores."""
import importlib.util
import unittest
from unittest.mock import patch

import torch

from vlmprobe import Prober, TokenMargin


class UnexpectedMetric:
    def __init__(self):
        self.calls = 0

    def score(self, logits, layout):
        self.calls += 1
        raise AssertionError("an observational method evaluated its unused metric")


class CountingMargin:
    def __init__(self):
        self.calls = 0

    def score(self, logits, layout):
        self.calls += 1
        return TokenMargin(4, 5).score(logits, layout)


@unittest.skipUnless(importlib.util.find_spec("transformers"), "optional transformers extra")
class AttentionObservationContractTests(unittest.TestCase):
    def setUp(self):
        from transformers import LlamaConfig, LlamaForCausalLM

        torch.manual_seed(7)
        torch.set_num_threads(1)
        model = LlamaForCausalLM(LlamaConfig(
            vocab_size=16, hidden_size=16, intermediate_size=32,
            num_hidden_layers=1, num_attention_heads=2, num_key_value_heads=2,
            max_position_embeddings=16, attn_implementation="eager",
        )).eval().requires_grad_(False)
        self.probe = Prober(model)
        self.inputs = {
            "input_ids": torch.tensor([[1, 2, 3]]),
            "attention_mask": torch.ones(1, 3, dtype=torch.long),
        }

    def observations(self):
        return {
            "profile": self.probe.attention.profile(layers=[0], queries="last_prompt"),
            "rollout": self.probe.attention.rollout(layers=[0]),
            "head_logits": self.probe.attention.head_logits(layers=[0]),
        }

    def targeted(self):
        return {
            "relevance": self.probe.attention.relevance(layers=[0]),
            "reweight": self.probe.attention.reweight(layers=[0], queries="last_prompt", keys="all", weight=0.5),
            "temperature": self.probe.attention.temperature(layers=[0], queries="last_prompt", temperature=2.0),
        }

    def test_observations_reject_metrics_before_any_model_forward(self):
        for name, method in self.observations().items():
            with self.subTest(method=name):
                metric = UnexpectedMetric()
                with patch.object(self.probe, "_run", side_effect=AssertionError("forward was executed")) as forward:
                    with self.assertRaisesRegex(ValueError, f"{name} is target-independent"):
                        method.run(self.inputs, metric=metric)
                forward.assert_not_called()
                self.assertEqual(metric.calls, 0)

    def test_observations_run_without_target_and_record_none(self):
        fields = {"profile": "entropy", "rollout": "rollout", "head_logits": "head_logits"}
        for name, method in self.observations().items():
            with self.subTest(method=name):
                result = method.run(self.inputs)
                repeated = method.run(self.inputs, metric=None)
                self.assertIsNone(result.metadata["metric"])
                self.assertIsNone(repeated.metadata["metric"])
                self.assertIn(fields[name], result.tensors)
                for key, value in result.tensors.items():
                    self.assertTrue(torch.isfinite(value).all())
                    torch.testing.assert_close(value, repeated.tensors[key], rtol=0, atol=0)

    def test_targeted_methods_still_require_target_before_forward(self):
        for name, method in self.targeted().items():
            with self.subTest(method=name):
                with patch.object(self.probe, "_run", side_effect=AssertionError("forward was executed")) as forward:
                    with self.assertRaisesRegex(ValueError, "requires a target metric"):
                        method.run(self.inputs)
                forward.assert_not_called()

    def test_targeted_methods_evaluate_target_and_record_it(self):
        for name, method in self.targeted().items():
            with self.subTest(method=name):
                metric = CountingMargin()
                result = method.run(self.inputs, metric=metric)
                self.assertGreater(metric.calls, 0)
                self.assertEqual(result.metadata["metric"]["name"], "CountingMargin")
                self.assertEqual(result.metadata["metric"]["parameters"]["calls"], metric.calls)
                self.assertTrue(all(torch.isfinite(value).all() for value in result.tensors.values()))


if __name__ == "__main__":
    unittest.main()
