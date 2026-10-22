"""Native pairwise attention visibility, independent of probability underflow."""
import importlib.util
from importlib.metadata import version
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "examples"))
from hf_model_matrix import make_model
from vlm_probing import ModelSpec, Prober
from vlm_probing.adapters.hf_attention import _attention_support, install_eager_taps, install_support_only

HAS_V5 = (importlib.util.find_spec("transformers") is not None
          and version("transformers").split(".")[:2] == ["5", "3"])


class AttentionSupportContractTests(unittest.TestCase):
    def test_model_spec_requires_declared_site_and_attention_layer(self):
        with self.assertRaisesRegex(ValueError, "unknown hook sites"):
            ModelSpec({0: "res"}, attentions={0: "attn"},
                      attention_supports={0: "support"}).validate({"res": None, "attn": None})
        with self.assertRaisesRegex(ValueError, "support layers"):
            ModelSpec({0: "res"}, attention_supports={0: "support"}).validate(
                {"res": None, "support": None})

    def test_additive_bias_and_probability_underflow_are_not_support(self):
        mask = torch.tensor([[[[0., -1000., float("-inf"), torch.finfo(torch.float32).min]]]])
        actual = _attention_support(mask, batch=1, heads=2, queries=1, keys=4, device=mask.device)
        self.assertEqual(actual.tolist(), [[[[True, True, False, False]]]])
        self.assertEqual(mask.softmax(-1)[0, 0, 0, 1].item(), 0.)

    def test_boolean_per_head_mask_retains_bidirectional_edges(self):
        mask = torch.tensor([[[[True, False], [True, True]], [[True, True], [False, True]]]])
        actual = _attention_support(mask, batch=1, heads=2, queries=2, keys=2, device=mask.device)
        torch.testing.assert_close(actual, mask)


@unittest.skipUnless(HAS_V5, "native attention support is audited for Transformers 5.3.x")
class NativeAttentionSupportTests(unittest.TestCase):
    def setUp(self):
        torch.manual_seed(73)
        torch.set_num_threads(1)

    def check_native(self, model, inputs, expected):
        model.eval().requires_grad_(True)
        embedding = (model.get_input_embeddings().weight if hasattr(model.get_input_embeddings(), "weight")
                     else next(model.get_input_embeddings().parameters()))
        native = model(**inputs, use_cache=False).logits if model.config.model_type != "vit" else model(**inputs).logits
        native_gradient, = torch.autograd.grad(native[..., -1].sum(), embedding)
        state = {name: value.detach().clone() for name, value in model.state_dict().items()}
        probe = Prober(model)
        tapped = model(**inputs, use_cache=False).logits if model.config.model_type != "vit" else model(**inputs).logits
        actual_gradient, = torch.autograd.grad(tapped[..., -1].sum(), embedding)
        torch.testing.assert_close(tapped, native, rtol=0, atol=0)
        torch.testing.assert_close(actual_gradient, native_gradient, rtol=0, atol=0)
        self.assertEqual(set(model.state_dict()), set(state))
        for name, value in model.state_dict().items():
            torch.testing.assert_close(value, state[name], rtol=0, atol=0)
        before = [(tuple(module._forward_hooks), tuple(module._forward_pre_hooks)) for module in model.modules()]
        support_sites = list(probe.spec.attention_supports.values())
        self.assertTrue(support_sites)
        trace = probe._run(inputs, capture=support_sites)
        for layer, site in probe.spec.attention_supports.items():
            actual = trace.activations[site]
            self.assertEqual(actual.dtype, torch.bool)
            torch.testing.assert_close(actual, expected[layer])
        self.assertEqual(before, [(tuple(module._forward_hooks), tuple(module._forward_pre_hooks))
                                  for module in model.modules()])
        return probe

    def test_gpt2_causal_and_padding_and_native_parity(self):
        from transformers import GPT2Config, GPT2LMHeadModel
        model = GPT2LMHeadModel(GPT2Config(
            vocab_size=20, n_positions=16, n_embd=16, n_layer=2, n_head=2,
            attn_implementation="eager",
        ))
        inputs = {"input_ids": torch.tensor([[1, 2, 3, 0], [0, 1, 2, 3]]),
                  "attention_mask": torch.tensor([[1, 1, 1, 0], [0, 1, 1, 1]])}
        expected = torch.ones(4, 4, dtype=torch.bool).tril()[None, None] & inputs["attention_mask"][:, None, None].bool()
        self.check_native(model, inputs, {0: expected, 1: expected})

    def test_support_only_llama_wrapper_and_later_taps_emit_once(self):
        # Exercise the legacy adapter's wrapper mechanism on the installed 5.3
        # native class. This is not a claim that the 4.57 environment was run.
        from transformers import LlamaConfig, LlamaForCausalLM
        model = LlamaForCausalLM(LlamaConfig(
            vocab_size=20, hidden_size=16, intermediate_size=24, num_hidden_layers=1,
            num_attention_heads=2, num_key_value_heads=1, head_dim=8,
            attn_implementation="eager",
        )).eval()
        inputs = {"input_ids": torch.tensor([[1, 2, 3, 0]]),
                  "attention_mask": torch.tensor([[1, 1, 1, 0]])}
        embedding = model.get_input_embeddings().weight
        original = model(**inputs, use_cache=False).logits
        original_gradient, = torch.autograd.grad(original[..., -1].sum(), embedding)
        attention = model.model.layers[0].self_attn
        state_keys = set(model.state_dict())
        self.assertTrue(install_support_only(attention))
        wrapped_forward = attention.forward
        self.assertTrue(install_support_only(attention))
        self.assertIs(attention.forward, wrapped_forward)
        captured = []
        handle = attention._probe_support.register_forward_hook(
            lambda _module, _args, output: captured.append(output.detach().clone()))
        try:
            wrapped = model(**inputs, use_cache=False).logits
        finally:
            handle.remove()
        wrapped_gradient, = torch.autograd.grad(wrapped[..., -1].sum(), embedding)
        torch.testing.assert_close(wrapped, original, rtol=0, atol=0)
        torch.testing.assert_close(wrapped_gradient, original_gradient, rtol=0, atol=0)
        self.assertEqual(set(model.state_dict()), state_keys)
        expected = torch.ones(4, 4, dtype=torch.bool).tril()[None, None] & inputs["attention_mask"][:, None, None].bool()
        self.assertEqual(len(captured), 1)
        torch.testing.assert_close(captured[0], expected)
        # Prober installs the later consumed-probability backend. The original
        # support-only wrapper must defer to it rather than emit a second time.
        probe = self.check_native(model, inputs, {0: expected})
        wrapped_forward = attention.forward
        self.assertTrue(install_eager_taps(attention))
        self.assertTrue(install_support_only(attention))
        self.assertIs(attention.forward, wrapped_forward)
        site = probe.spec.attention_supports[0]
        torch.testing.assert_close(probe._run(inputs, capture=[site]).activations[site], expected)

    def test_legacy_adapter_branch_registers_llama_and_qwen_support(self):
        # Select the adapter's 4.57 compatibility branch while running actual
        # installed 5.3 native models; no old runtime is installed or implied.
        from hf_smoke import make_llama, make_qwen
        for factory in (make_llama, make_qwen):
            with self.subTest(factory=factory.__name__):
                model, inputs = factory()
                size = inputs["input_ids"].shape[1]
                expected = (torch.ones(size, size, dtype=torch.bool).tril()[None, None]
                            & inputs["attention_mask"][:, None, None].bool())
                with patch("vlm_probing.adapters.huggingface.version", return_value="4.57.6"):
                    probe = self.check_native(model, inputs, {0: expected, 1: expected})
                self.assertEqual(set(probe.spec.attention_supports), set(probe.spec.attentions))
                self.assertFalse(probe.spec.editable_attention)

    def test_mistral_uses_effective_sliding_window(self):
        from transformers import LlavaConfig, LlavaForConditionalGeneration
        text = dict(model_type="mistral", vocab_size=40, hidden_size=16, intermediate_size=24,
                    num_hidden_layers=2, num_attention_heads=2, num_key_value_heads=1,
                    head_dim=8, pad_token_id=0, sliding_window=4)
        vision = dict(model_type="pixtral", hidden_size=16, intermediate_size=24,
                      num_hidden_layers=2, num_attention_heads=2, image_size=4, patch_size=2)
        config = LlavaConfig(text_config=text, vision_config=vision, image_token_index=28,
                             image_seq_length=4, vision_feature_select_strategy="full", vision_feature_layer=-1)
        config._attn_implementation = "eager"
        model = LlavaForConditionalGeneration(config)
        inputs = {"input_ids": torch.tensor([[1, 28, 28, 28, 28, 3]]),
                  "attention_mask": torch.ones(1, 6, dtype=torch.long),
                  "pixel_values": torch.randn(1, 3, 4, 4), "image_sizes": torch.tensor([[4, 4]])}
        q, k = torch.arange(6)[:, None], torch.arange(6)[None]
        expected = ((k <= q) & (k > q-4))[None, None]
        self.check_native(model, inputs, {0: expected, 1: expected})

    def test_qwen3_5_full_attention_uses_causal_and_padding_mask(self):
        model, inputs = make_model("qwen3_5")
        expected = torch.ones(6, 6, dtype=torch.bool).tril()[None, None] & inputs["attention_mask"][:, None, None].bool()
        probe = self.check_native(model, inputs, {3: expected})
        self.assertEqual(set(probe.spec.attention_supports), {3})

    def test_vit_support_is_bidirectional(self):
        from transformers import ViTConfig, ViTForImageClassification
        model = ViTForImageClassification(ViTConfig(
            image_size=8, patch_size=4, hidden_size=16, num_hidden_layers=1,
            num_attention_heads=2, intermediate_size=24, num_labels=3,
            attn_implementation="eager",
        ))
        inputs = {"pixel_values": torch.randn(2, 3, 8, 8)}
        expected = torch.ones(2, 1, 5, 5, dtype=torch.bool)
        self.check_native(model, inputs, {0: expected})


if __name__ == "__main__":
    unittest.main()
