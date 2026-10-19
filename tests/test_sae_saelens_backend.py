"""Optional SAELens v6 interoperability, source identity and native training."""
from copy import deepcopy
from importlib.util import find_spec
import itertools
import json
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest
from unittest.mock import patch

import torch
from torch import nn

from vlm_probing.sae.backends import saelens


def binding():
    return {"model_id": "toy@model-sha", "tokenizer_id": "none@image-input",
            "preprocessing_id": "identity-v1", "calibration_id": "train-only@manifest-sha",
            "site": "residual.0", "layer": 0,
            "hook": {"module": "blocks.0", "kind": "output", "selector": None, "tensor_slice": None}}


class FakeSAE(nn.Module):
    def __init__(self):
        super().__init__()
        self.weight = nn.Parameter(torch.eye(4))
        self.cfg = SimpleNamespace(d_in=4, d_sae=4, architecture=lambda: "standard",
            normalize_activations="none", apply_b_dec_to_input=False,
            reshape_activations="none", metadata=SimpleNamespace(hook_layer=0))

    def encode(self, x):
        return x @ self.weight

    def decode(self, z):
        return z @ self.weight.T


class SAELensContractTests(unittest.TestCase):
    def test_backend_info_does_not_import_optional_backend(self):
        with patch.object(saelens, "version", return_value="7.0.0"):
            self.assertEqual(saelens.backend_info()["version"], "7.0.0")
            with self.assertRaisesRegex(ValueError, "v6"):
                saelens._version()
        self.assertIn("vision", saelens.backend_info()["modalities"])

    def test_raw_coordinates_and_geometry_are_preserved(self):
        adapter = saelens.wrap(FakeSAE(), binding=binding())
        x = torch.randn(2, 3, 4)
        reconstruction, z = adapter(x)
        self.assertTrue(torch.equal(reconstruction, x))
        self.assertTrue(torch.equal(z, x))
        for invalid in [torch.ones(4, dtype=torch.long), torch.empty(0, 4), torch.full((2, 4), float("nan"))]:
            with self.assertRaises(ValueError):
                adapter.encode(invalid)

    def test_rejects_context_cross_hook_and_head_dictionary_even_when_widths_match(self):
        for architecture in ["transcoder", "skip_transcoder", "temporal"]:
            source = FakeSAE()
            source.cfg.architecture = lambda name=architecture: name
            with self.assertRaisesRegex(ValueError, "same-space architecture"):
                saelens.wrap(source, binding=binding())
        for normalization in ["layer_norm", "constant_norm_rescale", "covariance_whitening", "expected_average_only_in"]:
            source = FakeSAE()
            source.cfg.normalize_activations = normalization
            with self.assertRaisesRegex(ValueError, "normalize_activations='none'"):
                saelens.wrap(source, binding=binding())
        source = FakeSAE()
        source.cfg.metadata.hook_head_index = 0
        with self.assertRaisesRegex(ValueError, "head-specific"):
            saelens.wrap(source, binding=binding())

    def test_upstream_model_processing_requires_explicit_declaration(self):
        source = FakeSAE()
        source.cfg.metadata.model_from_pretrained_kwargs = {"center_writing_weights": False}
        with self.assertRaisesRegex(ValueError, "backend_model_from_pretrained_kwargs"):
            saelens.wrap(source, binding=binding())
        declared = {**binding(), "backend_model_from_pretrained_kwargs": {"center_writing_weights": False}}
        self.assertEqual(saelens.wrap(source, binding=declared).config.d_in, 4)

    def test_local_binding_is_checked_before_any_optional_import(self):
        with tempfile.TemporaryDirectory() as directory:
            wrong = {**binding(), "calibration_id": "other-data"}
            (Path(directory) / "vlmprobe_binding.json").write_text(json.dumps(wrong))
            with self.assertRaisesRegex(ValueError, "binding differs"):
                saelens.load(path=directory, binding=binding())


@unittest.skipUnless(find_spec("sae_lens") is not None, "optional sae-lens not installed")
class SAELensNativeTests(unittest.TestCase):
    @staticmethod
    def config(samples=64, architecture="standard"):
        sae = {"architecture": architecture, "d_in": 8, "d_sae": 16}
        if architecture == "topk":
            sae["k"] = 3
        elif architecture in {"standard", "gated"}:
            sae["l1_coefficient"] = .01
        return {"sae": sae, "trainer": {"total_training_samples": samples,
                "train_batch_size_samples": 16, "lr": .001,
                "feature_sampling_window": 100, "dead_feature_window": 100}, "seed": 42}

    def test_exact_upstream_encode_decode_on_supported_classic_architectures(self):
        from sae_lens import StandardSAE, StandardSAEConfig, GatedSAE, GatedSAEConfig, TopKSAE, TopKSAEConfig, JumpReLUSAE, JumpReLUSAEConfig
        pairs = [(StandardSAE, StandardSAEConfig, {}), (GatedSAE, GatedSAEConfig, {}),
                 (TopKSAE, TopKSAEConfig, {"k": 3}), (JumpReLUSAE, JumpReLUSAEConfig, {})]
        x = torch.randn(7, 8)
        for cls, cfg, extra in pairs:
            with self.subTest(architecture=cls.__name__):
                source = cls(cfg(d_in=8, d_sae=16, **extra))
                adapter = saelens.wrap(source, binding=binding())
                z = adapter.encode(x)
                self.assertTrue(torch.equal(z, source.encode(x)))
                self.assertTrue(torch.equal(adapter.decode(z), source.decode(z)))

    def test_registry_returns_real_upstream_ids_without_downloading_weights(self):
        rows = saelens.list_pretrained(release="goodfire-llama-3.1-8b-instruct")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["repo_id"], "Goodfire/Llama-3.1-8B-Instruct-SAE-l19")
        self.assertEqual(rows[0]["sae_id"], "layer_19")
        self.assertIsNone(rows[0]["architecture"])
        self.assertIsNone(rows[0]["hook"])

    def test_native_training_exports_reloadable_dictionary_and_rejects_wrong_identity(self):
        x = torch.randn(16, 8, generator=torch.Generator().manual_seed(14), requires_grad=True)
        for architecture in ("standard", "gated", "topk"):
            with self.subTest(architecture=architecture), tempfile.TemporaryDirectory() as directory:
                report = saelens.train(config=self.config(architecture=architecture),
                    activation_source=itertools.repeat(x), validation_source=[x * 2],
                    output_dir=directory, binding=binding())
                self.assertEqual(report["status"], "complete")
                self.assertEqual(report["training_steps"], 4)
                self.assertIsNone(x.grad)
                self.assertEqual(report["validation"]["samples"], 16)
                self.assertGreaterEqual(report["validation"]["mse_per_vector"], 0)
                trained = saelens.load(path=report["artifacts"]["inference_dir"], binding=binding())
                self.assertEqual(trained.encode(x).shape, (16, 16))
                self.assertTrue(torch.isfinite(trained(x)[0]).all())
                wrong = {**binding(), "calibration_id": "different-source"}
                with self.assertRaisesRegex(ValueError, "binding differs"):
                    saelens.load(path=report["artifacts"]["inference_dir"], binding=wrong)
                with self.assertRaisesRegex(ValueError, "earlier run"):
                    saelens.train(config=self.config(), activation_source=itertools.repeat(x), output_dir=directory, binding=binding())

    def test_same_data_constant_lr_resume_reproduces_uninterrupted_weights(self):
        x = torch.randn(16, 8, generator=torch.Generator().manual_seed(14))
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            full = saelens.train(config=self.config(128), activation_source=itertools.repeat(x), output_dir=root / "full", binding=binding())
            part = saelens.train(config=self.config(64), activation_source=itertools.repeat(x), output_dir=root / "part", binding=binding())
            resumed = saelens.train(config=self.config(128), activation_source=itertools.repeat(x), output_dir=root / "resume", binding=binding(), resume_from=part["artifacts"]["training_state"])
            one = saelens.load(path=full["artifacts"]["inference_dir"], binding=binding())
            two = saelens.load(path=resumed["artifacts"]["inference_dir"], binding=binding())
            self.assertEqual(resumed["training_steps"], 8)
            self.assertEqual(resumed["resume_validation"]["previous_target_samples"], 64)
            self.assertEqual(resumed["resume_validation"]["requested_target_samples"], 128)
            self.assertEqual(resumed["resume_validation"]["budget_extension"], "constant_learning_rate_only")
            for key, value in one.sae.state_dict().items():
                self.assertTrue(torch.equal(value, two.sae.state_dict()[key]), key)

    def test_resume_rejects_changed_dictionary_and_optimizer_protocol(self):
        x = torch.randn(16, 8, generator=torch.Generator().manual_seed(14))
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            original = self.config(64, "topk")
            part = saelens.train(config=original, activation_source=itertools.repeat(x), output_dir=root / "part", binding=binding())
            checkpoint = part["artifacts"]["training_state"]
            changes = [("sae", "k", 4), ("trainer", "lr", .002),
                       ("trainer", "adam_beta1", .8), ("trainer", "train_batch_size_samples", 8),
                       ("sae", "normalize_activations", "expected_average_only_in")]
            for family, key, value in changes:
                changed = deepcopy(original)
                changed[family][key] = value
                changed["trainer"]["total_training_samples"] = 128
                with self.subTest(key=key), self.assertRaisesRegex(ValueError, "configuration differs|normalization|normalize_activations"):
                    saelens.train(config=changed, activation_source=itertools.repeat(x), output_dir=root / key, binding=binding(), resume_from=checkpoint)
            # Even if a protocol file still claims the old config, the native
            # dictionary config is checked independently before weights load.
            native_config = Path(checkpoint) / "cfg.json"
            original_text = native_config.read_text()
            tampered = json.loads(original_text)
            tampered["k"] = 4
            native_config.write_text(json.dumps(tampered))
            with self.assertRaisesRegex(ValueError, "native SAE configuration differs"):
                saelens.train(config=self.config(128, "topk"), activation_source=itertools.repeat(x), output_dir=root / "native_tamper", binding=binding(), resume_from=checkpoint)
            native_config.write_text(original_text)
            state_path = Path(checkpoint) / "trainer_state.pt"
            state = torch.load(state_path, map_location="cpu", weights_only=True)
            state["optimizer"]["param_groups"][0]["lr"] = .002
            torch.save(state, state_path)
            with self.assertRaisesRegex(ValueError, "native optimizer learning rate differs"):
                saelens.train(config=self.config(128, "topk"), activation_source=itertools.repeat(x), output_dir=root / "optimizer_tamper", binding=binding(), resume_from=checkpoint)
            state["optimizer"]["param_groups"][0]["lr"] = .001
            torch.save(state, state_path)
            saved_protocol = Path(checkpoint) / "vlmprobe_training_protocol.json"
            protocol = json.loads(saved_protocol.read_text())
            protocol["trainer_config"]["lr"] = .002
            saved_protocol.write_text(json.dumps(protocol))
            with self.assertRaisesRegex(ValueError, "trainer configuration differs"):
                saelens.train(config=self.config(128, "topk"), activation_source=itertools.repeat(x), output_dir=root / "protocol_tamper", binding=binding(), resume_from=checkpoint)

    def test_resume_rejects_changed_l1_and_nonconstant_budget_extension(self):
        x = torch.randn(16, 8, generator=torch.Generator().manual_seed(14))
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            original = self.config(64)
            original["trainer"].update(lr_scheduler_name="cosineannealing", lr_end=.0001)
            part = saelens.train(config=original, activation_source=itertools.repeat(x), output_dir=root / "part", binding=binding())
            changed = deepcopy(original)
            changed["sae"]["l1_coefficient"] = .02
            with self.assertRaisesRegex(ValueError, "SAE configuration differs"):
                saelens.train(config=changed, activation_source=itertools.repeat(x), output_dir=root / "l1", binding=binding(), resume_from=part["artifacts"]["training_state"])
            changed = deepcopy(original)
            changed["trainer"]["total_training_samples"] = 128
            with self.assertRaisesRegex(ValueError, "budget extension requires constant"):
                saelens.train(config=changed, activation_source=itertools.repeat(x), output_dir=root / "budget", binding=binding(), resume_from=part["artifacts"]["training_state"])

    def test_nonfinite_optimizer_hyperparameters_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            for key, value in [("lr", float("inf")), ("lr_end", float("nan")), ("adam_beta1", float("inf"))]:
                config = self.config()
                config["trainer"][key] = value
                with self.subTest(key=key), self.assertRaisesRegex(ValueError, "finite"):
                    saelens.train(config=config, activation_source=iter(()), output_dir=directory, binding=binding())

    def test_unknown_hyperparameters_raise_instead_of_silently_disappearing(self):
        with self.assertRaises(TypeError):
            saelens.create_training_sae(d_in=8, d_sae=16, not_a_parameter=3)

    def test_trained_dictionary_uses_same_native_model_feature_and_intervention_workflow(self):
        import sys
        sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "examples"))
        from tiny_model import TinyModel
        from vlmprobe import Prober
        from vlmprobe.sae import build_sae_binding
        with torch.random.fork_rng(devices=[]):
            torch.random.default_generator.manual_seed(23)
            model = TinyModel()
            inputs = {"input_ids": torch.tensor([[1, 2, 3]]), "image_tokens": torch.randn(1, 2, 6)}
        probe = Prober(model)
        bound = build_sae_binding(probe, 0, model_id="tiny@seed23", tokenizer_id="integer-ids-v1",
            preprocessing_id="two-visual-three-text-v1", calibration_id="tiny-activation-smoke-only")
        raw = probe.adapter.run(inputs, capture=["residual.0"]).activations["residual.0"].detach().flatten(0, 1)
        config = self.config(20)
        config["sae"]["d_in"] = 6
        config["trainer"]["train_batch_size_samples"] = 5
        with tempfile.TemporaryDirectory() as directory:
            report = saelens.train(config=config, activation_source=itertools.repeat(raw), output_dir=directory, binding=bound)
            adapter = saelens.load(path=report["artifacts"]["inference_dir"], binding=bound)
            result = probe.sae.features(layer=0, sae=adapter, binding=bound).run(inputs)
            torch.testing.assert_close(result.tensors["features"], adapter.encode(raw))
            edited = probe.sae.edit(layer=0, sae=adapter, binding=bound, feature_ids=[0], scale=1).run(inputs)
            self.assertTrue(torch.equal(edited.tensors["baseline_logits"], edited.tensors["edited_logits"]))


if __name__ == "__main__":
    unittest.main()
