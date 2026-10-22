"""Grad-CAM respects structural support, including zero-probability allowed keys."""
import importlib.util
from importlib.metadata import version
import unittest

import torch

from vlm_probing.attention import AttentionGradCAM


HAS_V5 = (importlib.util.find_spec("transformers") is not None
          and version("transformers").split(".")[:2] == ["5", "3"])


class GradCAMSupportTests(unittest.TestCase):
    def test_causal_per_query_pooling_excludes_forbidden_gradients(self):
        attention = torch.tensor([[[[1., 0., 0.], [.25, .75, 0.], [.2, .3, .5]]]], dtype=torch.float64)
        gradient = torch.tensor([[[[2., 1000., 2000.], [2., 4., 3000.], [1., 2., 3.]]]], dtype=torch.float64)
        support = torch.ones(1, 1, 3, 3, dtype=torch.bool).tril()
        result = AttentionGradCAM().run(attention, gradient, support_mask=support)
        torch.testing.assert_close(result.tensors["head_weights"], torch.tensor([[[2., 3., 2.]]], dtype=torch.float64))
        torch.testing.assert_close(result.tensors["cam"], attention[:, 0] * torch.tensor([[[2.], [3.], [2.]]]))
        self.assertTrue(result.metadata["structural_support_supplied"])

    def test_allowed_underflowed_probabilities_still_participate_in_pooling(self):
        attention = torch.tensor([[[[1., 0., 0.]]]], dtype=torch.float64)
        gradient = torch.tensor([[[[0., 3., 6.]]]], dtype=torch.float64)
        support = torch.ones_like(attention, dtype=torch.bool)
        result = AttentionGradCAM().run(attention, gradient, support_mask=support)
        torch.testing.assert_close(result.tensors["head_weights"], torch.tensor([[[3.]]], dtype=torch.float64))
        torch.testing.assert_close(result.tensors["cam"], torch.tensor([[[3., 0., 0.]]], dtype=torch.float64))

    def test_normalization_ignores_forbidden_keys_and_handles_empty_rows(self):
        attention = torch.tensor([[[[.25, .75, 0.], [0., 0., 1.]]]], dtype=torch.float64)
        gradient = torch.tensor([[[[2., 2., 1000.], [9., 8., 7.]]]], dtype=torch.float64)
        support = torch.tensor([[[[True, True, False], [False, False, True]]]])
        keys = torch.tensor([[True, True, False]])
        result = AttentionGradCAM().run(attention, gradient, key_mask=keys, support_mask=support, normalize=True)
        torch.testing.assert_close(result.tensors["cam"], torch.tensor([[[0., 1., 0.], [0., 0., 0.]]], dtype=torch.float64))
        self.assertTrue(torch.isfinite(result.tensors["head_weights"]).all())

    def test_unrestricted_support_preserves_bidirectional_rule(self):
        generator = torch.Generator().manual_seed(9)
        attention = torch.rand(2, 3, 4, 4, generator=generator, dtype=torch.float64).softmax(-1)
        gradients = torch.rand(attention.shape, generator=generator, dtype=torch.float64)
        kernel = AttentionGradCAM()
        original = kernel.run(attention, gradients)
        supported = kernel.run(attention, gradients, support_mask=torch.ones(1, 1, 4, 4, dtype=torch.bool))
        for name in original.tensors:
            torch.testing.assert_close(original.tensors[name], supported.tensors[name], rtol=0, atol=0)

    def test_head_specific_support_and_selection_intersection(self):
        attention = torch.tensor([[[[.25, .75, 0.]], [[0., .4, .6]]]], dtype=torch.float64)
        gradient = torch.tensor([[[[100., 2., 999.]], [[999., 4., 8.]]]], dtype=torch.float64)
        support = torch.tensor([[[[True, True, False]], [[False, True, True]]]])
        keys = torch.tensor([[False, True, True]])
        result = AttentionGradCAM().run(attention, gradient, support_mask=support, key_mask=keys)
        torch.testing.assert_close(result.tensors["head_weights"], torch.tensor([[[2.], [6.]]], dtype=torch.float64))
        torch.testing.assert_close(result.tensors["cam"], torch.tensor([[[0., 1.95, 1.8]]], dtype=torch.float64))

    def test_invalid_support_masks_fail_before_broadcast(self):
        attention = torch.ones(1, 2, 3, 3, dtype=torch.float64) / 3
        invalid = [torch.ones(1, 1, 3, 3), torch.ones(3, 3, dtype=torch.bool),
                   torch.ones(2, 1, 3, 3, dtype=torch.bool), torch.ones(1, 3, 3, 3, dtype=torch.bool)]
        for mask in invalid:
            with self.subTest(shape=mask.shape, dtype=mask.dtype):
                with self.assertRaisesRegex(ValueError, "support_mask"):
                    AttentionGradCAM().run(attention, attention, support_mask=mask)


@unittest.skipUnless(HAS_V5, "native adapter regression requires Transformers 5.3.x")
class NativeCausalGradCAMTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from transformers import GPT2Config, GPT2LMHeadModel
        from vlm_probing import Prober
        torch.manual_seed(3)
        torch.set_num_threads(1)
        cls.model = GPT2LMHeadModel(GPT2Config(
            vocab_size=20, n_positions=16, n_ctx=16, n_embd=16, n_layer=2,
            n_head=2, attn_implementation="eager", initializer_range=.2,
        )).eval().double().requires_grad_(False)
        cls.probe = Prober(cls.model)

    @staticmethod
    def inputs(tokens):
        return {"input_ids": torch.tensor([tokens]), "attention_mask": torch.ones(1, len(tokens), dtype=torch.long)}

    def test_future_tokens_leave_single_and_multiple_query_prefix_maps_invariant(self):
        from vlm_probing import TokenMargin
        short = self.inputs([1, 2, 3])
        long = self.inputs([1, 2, 3, 7, 8, 9])
        metric = TokenMargin(4, 5, position=[2])
        with torch.no_grad():
            torch.testing.assert_close(self.model(**short).logits[0, 2], self.model(**long).logits[0, 2], rtol=1e-12, atol=1e-12)
        for layer, queries in [(1, [2]), (0, [1, 2])]:
            for normalize in [False, True]:
                with self.subTest(layer=layer, queries=queries, normalize=normalize):
                    method = self.probe.attention.grad_cam(layers=[layer], queries=queries, keys="all", normalize=normalize)
                    before = method.run(short, metric=metric)
                    after = method.run(long, metric=metric)
                    torch.testing.assert_close(before.tensors["cam"][..., :3, :3], after.tensors["cam"][..., :3, :3], rtol=1e-12, atol=1e-12)
                    torch.testing.assert_close(before.tensors["head_weights"][..., :3], after.tensors["head_weights"][..., :3], rtol=1e-12, atol=1e-12)
                    self.assertEqual(after.tensors["cam"][..., :3, 3:].abs().max().item(), 0)
                    self.assertTrue(after.metadata["layer_results"][0]["structural_support_supplied"])


if __name__ == "__main__":
    unittest.main()
