"""Analytic integration regressions through the public API; no model downloads."""
import importlib.util
import unittest

import torch
from torch import nn

from vlmprobe import HookPoint, ModelSpec, Prober, TokenLayout, TokenMargin, TorchModelAdapter


class LinearAttentionScore(nn.Module):
    """Constant dF/dA isolates accumulation from quadrature/model error."""

    def __init__(self, dtype):
        super().__init__()
        self.register_buffer("attention", torch.full((1, 1, 2, 2), .5, dtype=dtype))
        self.emb = nn.Identity()
        self.input_tap = nn.Identity()
        self.value_tap = nn.Identity()
        self.tap = nn.Identity()
        self.res = nn.Identity()
        self.input_dtypes = []
        self.probability_dtypes = []

    def forward(self, pixel_values):
        self.input_dtypes.append(pixel_values.dtype)
        x = self.emb(pixel_values)
        raw = self.input_tap(x.reshape(1, 1, 1).expand(1, 2, 2) + 1)
        self.value_tap(torch.ones_like(raw))
        attention = self.tap(self.attention + 0 * raw.sum())
        self.probability_dtypes.append(attention.dtype)
        score = attention.sum((1, 3))
        return {"logits": self.res(torch.stack((score, score * 0), -1))}

    def probing_adapter(self):
        spec = ModelSpec(
            {0: "res"}, attentions={0: "attention"}, editable_attention={0},
            embeddings="emb", attention_inputs={0: "input"},
            attention_values={0: "value"}, project_values=lambda _, value: value,
            layout=lambda _: TokenLayout(torch.ones(1, 2, dtype=torch.bool)),
        )
        return TorchModelAdapter(self, {
            "res": HookPoint("res"), "attention": HookPoint("tap"),
            "emb": HookPoint("emb"), "input": HookPoint("input_tap"),
            "value": HookPoint("value_tap"),
        }, spec=spec)


class AttentionIntegrationPrecisionTests(unittest.TestCase):
    def setUp(self):
        self.old_threads = torch.get_num_threads()
        torch.set_num_threads(1)

    def tearDown(self):
        torch.set_num_threads(self.old_threads)

    @staticmethod
    def setup_case(dtype):
        model = LinearAttentionScore(dtype).eval().requires_grad_(False)
        return model, Prober(model), {"pixel_values": torch.ones(1, 1, 1, 1, dtype=dtype)}

    def assert_native_forward(self, model, dtype):
        self.assertEqual(set(model.input_dtypes), {dtype})
        self.assertEqual(set(model.probability_dtypes), {dtype})
        self.assertTrue(all(parameter.grad is None for parameter in model.parameters()))

    def test_attention_integral_completeness_dtypes_and_native_interventions(self):
        for dtype in (torch.bfloat16, torch.float32, torch.float64):
            model, probe, inputs = self.setup_case(dtype)
            output_dtype = torch.float64 if dtype == torch.float64 else torch.float32
            for steps in (20, 64, 256, 512, 1024):
                with self.subTest(dtype=dtype, steps=steps):
                    result = probe.attention.attribution(
                        layers=[0], queries="all", keys="all", steps=steps,
                    ).run(inputs, metric=TokenMargin(0, 1))
                    attribution = result.tensors["attribution"]
                    expected = torch.tensor([[[[[0., 0.], [.5, .5]]]]], dtype=output_dtype)
                    tolerance = 1e-12 if dtype == torch.float64 else 2e-6
                    torch.testing.assert_close(attribution, expected, rtol=tolerance, atol=tolerance)
                    torch.testing.assert_close(attribution.sum(), torch.tensor(1., dtype=output_dtype),
                                               rtol=tolerance, atol=tolerance)
                    for key in ("attribution", "head_attribution", "token_attribution"):
                        self.assertEqual(result.tensors[key].dtype, output_dtype)
                    self.assert_native_forward(model, dtype)

    def test_input_integrals_promote_feedback_and_all_kernel_auxiliaries(self):
        for dtype in (torch.bfloat16, torch.float32, torch.float64):
            model, probe, inputs = self.setup_case(dtype)
            output_dtype = torch.float64 if dtype == torch.float64 else torch.float32
            methods = (
                ("tam", probe.attention.tam, {}),
                ("beyond_head", probe.attention.beyond_intuition, {"variant": "head"}),
                ("beyond_token", probe.attention.beyond_intuition, {"variant": "token"}),
            )
            for name, factory, kwargs in methods:
                for steps in (20, 64, 256, 512, 1024):
                    with self.subTest(dtype=dtype, method=name, steps=steps):
                        result = factory(layers=[0], queries="all", keys="all", steps=steps, **kwargs).run(
                            inputs, metric=TokenMargin(0, 1))
                        expected = torch.tensor([[[0., 0.], [1., 1.]]], dtype=output_dtype)
                        tolerance = 1e-12 if dtype == torch.float64 else 2e-6
                        torch.testing.assert_close(result.tensors["feedback"], expected,
                                                   rtol=tolerance, atol=tolerance)
                        for key in ("relevance", "feedback", "map"):
                            self.assertEqual(result.tensors[key].dtype, output_dtype)
                        self.assert_native_forward(model, dtype)

    def test_signed_attribution_and_supported_quadratures(self):
        model, probe, inputs = self.setup_case(torch.bfloat16)
        for quadrature in ("left", "right", "endpoints"):
            with self.subTest(quadrature=quadrature):
                method = probe.attention.attribution(layers=[0], queries="all", keys="all",
                                                      steps=20, quadrature=quadrature)
                forward = method.run(inputs, metric=TokenMargin(0, 1))
                reverse = method.run(inputs, metric=TokenMargin(1, 0))
                torch.testing.assert_close(forward.tensors["attribution"],
                                           -reverse.tensors["attribution"], rtol=0, atol=0)
                torch.testing.assert_close(forward.tensors["attribution"].sum(), torch.tensor(1.),
                                           rtol=2e-6, atol=2e-6)
        self.assert_native_forward(model, torch.bfloat16)

    def test_integral_kernel_contract_keeps_native_probability_tolerance(self):
        from vlm_probing.attention import AttentionAttribution, BeyondIntuition, TransitionAttentionMaps

        # 1/3 is valid at BF16 precision but its FP32 row sum is not exactly 1.
        attention = torch.full((1, 1, 3, 3), 1 / 3, dtype=torch.bfloat16)
        self.assertGreater((attention.float().sum(-1) - 1).abs().max().item(), 1e-5)
        integrated = torch.ones_like(attention, dtype=torch.float32)
        result = AttentionAttribution().run(attention, integrated)
        torch.testing.assert_close(result.tensors["attribution"], attention.float(), rtol=0, atol=0)
        for result in (
            TransitionAttentionMaps().run(attention[None], integrated),
            BeyondIntuition().run(attention[None], integrated, gradients=torch.ones_like(attention[None])),
        ):
            self.assertEqual(result.tensors["relevance"].dtype, torch.float32)
            self.assertEqual(result.tensors["feedback"].dtype, torch.float32)
        with self.assertRaisesRegex(ValueError, "dtype"):
            AttentionAttribution().run(torch.full_like(attention, 1 / 3, dtype=torch.float64), integrated)
        # Original-forward gradients keep their existing strict dtype contract.
        with self.assertRaisesRegex(ValueError, "dtype"):
            BeyondIntuition().run(attention[None], integrated,
                                  gradients=torch.ones_like(attention[None], dtype=torch.float32))
        with self.assertRaisesRegex(ValueError, "sum to one"):
            AttentionAttribution().run(attention * 2, integrated)

    @unittest.skipUnless(importlib.util.find_spec("transformers"), "optional transformers extra")
    def test_native_bf16_vit_integrated_maps_accept_rounded_probability_rows(self):
        from transformers import ViTConfig, ViTForImageClassification
        from vlmprobe import ClassScore

        torch.manual_seed(7)
        model = ViTForImageClassification(ViTConfig(
            image_size=16, patch_size=8, hidden_size=16, num_hidden_layers=1,
            num_attention_heads=2, intermediate_size=32, num_labels=3,
            attn_implementation="eager",
        )).eval().bfloat16().requires_grad_(False)
        probe = Prober(model)
        inputs = {"pixel_values": torch.randn(1, 3, 16, 16, dtype=torch.bfloat16)}
        attention = probe.attention.profile(include_attention=True).run(inputs).tensors["attention"]
        self.assertGreater((attention.float().sum(-1) - 1).abs().max().item(), 1e-5)
        for method in (
            probe.attention.attribution(layers=[0], steps=2),
            probe.attention.tam(layers=[0], steps=2),
            probe.attention.beyond_intuition(layers=[0], steps=2),
            probe.attention.beyond_intuition(layers=[0], variant="token", steps=2),
        ):
            with self.subTest(method=method.name, variant=method.options.get("variant")):
                result = method.run(inputs, metric=ClassScore(1))
                key = "attribution" if method.name == "attribution" else "map"
                self.assertEqual(result.tensors[key].dtype, torch.float32)
                self.assertTrue(torch.isfinite(result.tensors[key]).all())


if __name__ == "__main__":
    unittest.main()
