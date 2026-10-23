"""Native Qwen text bindings: actual readouts, normalized receivers and edits."""
import importlib.util
from importlib.metadata import version
import unittest
from unittest.mock import patch

import torch
from torch import nn

from vlmprobe import CapabilityError, Prober, TokenMargin

HAS_V5 = (importlib.util.find_spec("transformers") is not None
          and version("transformers").split(".")[:2] == ["5", "3"])


def make_qwen(family, dtype=torch.float32, backend="eager"):
    from transformers import Qwen2Config, Qwen2ForCausalLM, Qwen3Config, Qwen3ForCausalLM
    config_class, model_class = {"qwen2": (Qwen2Config, Qwen2ForCausalLM),
                                 "qwen3": (Qwen3Config, Qwen3ForCausalLM)}[family]
    config = config_class(vocab_size=32, hidden_size=16, intermediate_size=24,
                          num_hidden_layers=2, num_attention_heads=2,
                          num_key_value_heads=1, head_dim=8, max_position_embeddings=32,
                          attention_dropout=0.0, use_cache=False,
                          attn_implementation=backend)
    model = model_class(config).to(dtype=dtype).eval()
    inputs = {"input_ids": torch.tensor([[1, 2, 3, 4], [0, 1, 2, 5]]),
              "attention_mask": torch.tensor([[1, 1, 1, 1], [0, 1, 1, 1]])}
    return model, inputs


@unittest.skipUnless(HAS_V5, "Qwen text automatic adapters are audited for Transformers 5.3.x")
class QwenTextAdapterTests(unittest.TestCase):
    def setUp(self):
        torch.manual_seed(71)
        torch.set_num_threads(1)

    def test_native_forward_gradient_embedding_and_final_readout(self):
        for family in ("qwen2", "qwen3"):
            for dtype in (torch.float32, torch.bfloat16):
                with self.subTest(family=family, dtype=dtype):
                    model, inputs = make_qwen(family, dtype)
                    native = model(**inputs).logits
                    embedding = model.get_input_embeddings().weight
                    native_gradient, = torch.autograd.grad(native[:, -1, 4].sum(), embedding)
                    state = {name: value.detach().clone() for name, value in model.state_dict().items()}
                    probe = Prober(model)
                    actual = model(**inputs).logits
                    gradient, = torch.autograd.grad(actual[:, -1, 4].sum(), embedding)
                    torch.testing.assert_close(actual, native, rtol=0, atol=0)
                    torch.testing.assert_close(gradient, native_gradient, rtol=0, atol=0)
                    self.assertTrue(probe.spec.causal_attention)
                    last = max(probe.spec.residuals)
                    lens = probe.lens.logit(layers=[last], tokens="all").run(inputs)
                    valid = inputs["attention_mask"].bool()
                    torch.testing.assert_close(lens.tensors["logits"][0], native.detach()[valid], rtol=0, atol=0)
                    nearest = probe.lens.embed(tokens="all").run(inputs, top_k=1)
                    torch.testing.assert_close(nearest.tensors["token_ids"][0, :, 0], inputs["input_ids"][valid])
                    layout = probe._layout(inputs, actual)
                    torch.testing.assert_close(layout.valid, valid)
                    self.assertFalse(layout.visual.any())
                    self.assertEqual(state.keys(), model.state_dict().keys())
                    for name, value in model.state_dict().items():
                        torch.testing.assert_close(value, state[name], rtol=0, atol=0)
                    self.assertTrue(all(value.grad is None for value in model.parameters()))

    def test_qk_receiver_stage_and_head_projection(self):
        for family in ("qwen2", "qwen3"):
            with self.subTest(family=family):
                model, inputs = make_qwen(family)
                probe = Prober(model)
                attention = model.model.layers[0].self_attn
                expected = {}
                handles = []
                for kind in ("q", "k"):
                    component = getattr(attention, f"{kind}_norm" if family == "qwen3" else f"{kind}_proj")
                    def capture(_module, _args, output, kind=kind):
                        expected[kind] = output.detach().clone()
                    handles.append(component.register_forward_hook(capture))
                try:
                    sites = [probe.spec.path_qkv[0][kind].site for kind in ("q", "k")]
                    sites.append(probe.spec.heads[0])
                    trace = probe._run(inputs, capture=sites)
                finally:
                    for handle in handles:
                        handle.remove()
                for kind in ("q", "k"):
                    declared = probe.spec.path_qkv[0][kind]
                    self.assertEqual(declared.heads, 2 if kind == "q" else 1)
                    torch.testing.assert_close(trace.activations[declared.site], expected[kind], rtol=0, atol=0)
                    self.assertEqual(declared.view(expected[kind]).shape[-2:], (declared.heads, 8))
                heads = trace.activations[probe.spec.heads[0]]
                projected = probe.spec.project_heads(0, heads).sum(-2)
                torch.testing.assert_close(projected, nn.functional.linear(heads, attention.o_proj.weight),
                                           rtol=1e-5, atol=1e-7)
                scores = probe.attention.head_logits(layers=[0]).run(inputs)
                self.assertTrue(torch.isfinite(scores.tensors["head_logits"]).all())

    def test_consumed_edits_path_intervention_and_cleanup(self):
        for family in ("qwen2", "qwen3"):
            with self.subTest(family=family):
                model, inputs = make_qwen(family)
                model.requires_grad_(False)
                probe = Prober(model)
                model.train()
                model.model.layers[0].eval()  # Restore mixed module flags as well.
                flags = [(module, module.training) for module in model.modules()]
                sites = [probe.spec.attentions[0], probe.spec.attention_supports[0]]
                native = probe._run(inputs, capture=sites)
                support = native.activations[sites[1]]
                expected = torch.ones(4, 4, dtype=torch.bool).tril()[None, None] & inputs["attention_mask"][:, None, None].bool()
                torch.testing.assert_close(support, expected)
                edited = probe._run(inputs, interventions={sites[0]: lambda value: value * 0})
                self.assertGreater((edited.logits - native.logits).abs().max().item(), 1e-7)
                attribution = probe.attention.attribution(layers=[0], steps=2).run(inputs, metric=TokenMargin(4, 5))
                self.assertTrue(all(torch.isfinite(value).all() for value in attribution.tensors.values()))
                path = probe.causal.path(senders=[(0, 0)], receivers=[(1, 0, "k")],
                                         sender_tokens=[1], receiver_tokens=[1])
                identity = path.run(inputs, donor=inputs, metric=TokenMargin(4, 5))
                torch.testing.assert_close(identity.tensors["effect"], torch.zeros(2), atol=1e-7, rtol=0)
                donor = {**inputs, "input_ids": torch.tensor([[5, 6, 7, 8], [0, 6, 7, 8]])}
                changed = path.run(inputs, donor=donor, metric=TokenMargin(4, 5), alignment="position")
                self.assertGreater(changed.tensors["effect"].abs().max().item(), 1e-8)
                with self.assertRaisesRegex(RuntimeError, "controlled failure"):
                    probe._run(inputs, interventions={sites[0]: lambda _: (_ for _ in ()).throw(RuntimeError("controlled failure"))})
                for module, training in flags:
                    self.assertEqual(module.training, training)
                    self.assertFalse(module._forward_hooks)
                    self.assertFalse(module._forward_pre_hooks)
                self.assertEqual(model.config._attn_implementation, "eager")
                self.assertTrue(all(parameter.grad is None for parameter in model.parameters()))
                torch.testing.assert_close(probe._run(inputs).logits, native.logits, rtol=0, atol=0)

    def test_training_dropout_parity_after_tap_installation(self):
        for family in ("qwen2", "qwen3"):
            with self.subTest(family=family):
                model, inputs = make_qwen(family)
                for layer in model.model.layers:
                    layer.self_attn.attention_dropout = 0.25
                model.train()
                torch.manual_seed(39)
                native = model(**inputs).logits
                Prober(model)
                torch.manual_seed(39)
                actual = model(**inputs).logits
                torch.testing.assert_close(actual, native, rtol=0, atol=0)
                self.assertTrue(model.training)

    def test_bf16_consumed_edits_keep_native_dtype(self):
        for family in ("qwen2", "qwen3"):
            with self.subTest(family=family):
                model, inputs = make_qwen(family, torch.bfloat16)
                model.requires_grad_(False)
                probe = Prober(model)
                site = probe.spec.attentions[0]
                native = probe._run(inputs, capture=[site])
                seen = []
                def suppress(value):
                    seen.append(value.dtype)
                    return value * 0
                edited = probe._run(inputs, capture=[site], interventions={site: suppress})
                self.assertEqual(seen, [torch.bfloat16])
                self.assertEqual(edited.activations[site].dtype, torch.bfloat16)
                self.assertEqual(edited.logits.dtype, native.logits.dtype)
                self.assertGreater((edited.logits - native.logits).abs().max().item(), 1e-5)
                result = probe.attention.attribution(layers=[0], steps=2).run(inputs, metric=TokenMargin(4, 5))
                self.assertEqual(result.tensors["attribution"].dtype, torch.float32)
                self.assertTrue(torch.isfinite(result.tensors["attribution"]).all())
                self.assertTrue(all(parameter.grad is None for parameter in model.parameters()))

    def test_sdpa_residual_and_path_capability_remains_available(self):
        for family in ("qwen2", "qwen3"):
            with self.subTest(family=family):
                model, inputs = make_qwen(family, backend="sdpa")
                probe = Prober(model)
                capabilities = probe.describe()["methods"]
                self.assertTrue(capabilities["lens.logit"]["available"])
                self.assertTrue(capabilities["causal.path"]["available"])
                self.assertFalse(capabilities["attention.profile"]["available"])
                final = probe.lens.logit(layers=[1]).run(inputs).tensors["logits"][0]
                torch.testing.assert_close(final, model(**inputs).logits[:, -1], rtol=1e-5, atol=1e-7)

    def test_new_text_contract_does_not_claim_legacy_transformers_support(self):
        for family in ("qwen2", "qwen3"):
            with self.subTest(family=family):
                model, _ = make_qwen(family)
                with patch("vlm_probing.adapters.huggingface.version", return_value="4.57.6"):
                    with self.assertRaisesRegex(CapabilityError, "require transformers 5.3.x"):
                        Prober(model)


class AutomaticAdapterErrorTests(unittest.TestCase):
    def test_error_lists_exact_supported_classes_and_custom_escape_hatch(self):
        with self.assertRaises(CapabilityError) as caught:
            Prober(nn.Linear(2, 2))
        message = str(caught.exception)
        for fragment in ("Qwen2ForCausalLM", "Qwen3ForCausalLM", "ViTForImageClassification",
                         "adapter=TorchModelAdapter", "register_adapter", "probing_adapter"):
            self.assertIn(fragment, message)


if __name__ == "__main__":
    unittest.main()
