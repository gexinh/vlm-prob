"""Scientific contracts for native sparse encoders and portable artifacts."""
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest

import torch
from torch import nn

from vlmprobe.sae import SAEConfig, SAELensAdapter, SparseAutoencoder


def binding():
    return {"model_id": "toy@sha256:model", "tokenizer_id": "toy@sha256:tokenizer",
            "preprocessing_id": "identity-v1", "calibration_id": "disjoint-train-sha256",
            "site": "residual.0", "layer": 0,
            "hook": {"module": "blocks.0", "kind": "output", "selector": None, "tensor_slice": None}}


class SAEKernelTests(unittest.TestCase):
    def test_topk_is_per_token_and_nonnegative(self):
        model = SparseAutoencoder(SAEConfig("topk", 5, 12, k=3), binding())
        features = model.encode(torch.randn(2, 7, 5))
        self.assertEqual(features.shape, (2, 7, 12))
        self.assertTrue((features >= 0).all())
        self.assertTrue(((features != 0).sum(-1) <= 3).all())
        one = model.encode(torch.randn(1, 5))
        batch = torch.cat((torch.randn(8, 5), torch.randn(1, 5)))
        self.assertEqual(one.shape[-1], batch.new_zeros(12).shape[-1])
        # An unrelated batch item cannot change another token's TopK budget.
        query = torch.randn(1, 5)
        self.assertTrue(torch.allclose(model.encode(query), model.encode(torch.cat((query, batch)))[0:1]))
        losses = model.loss(query)
        self.assertEqual(float(losses["sparsity"]), 0.)
        self.assertEqual(float(losses["auxiliary"]), 0.)

    def test_decoder_columns_constrained_after_update(self):
        model = SparseAutoencoder(SAEConfig("relu", 5, 12), binding())
        optimizer = torch.optim.Adam(model.parameters(), lr=.01)
        optimizer.zero_grad()
        model.loss(torch.randn(9, 5))["loss"].backward()
        optimizer.step()
        model.normalize_decoder_()
        self.assertTrue(torch.allclose(model.decoder.weight.norm(dim=0), torch.ones(12), atol=1e-6))

    def test_gated_auxiliary_has_no_decoder_gradients(self):
        model = SparseAutoencoder(SAEConfig("gated", 5, 12), binding())
        auxiliary = model.loss(torch.randn(9, 5))["auxiliary"]
        auxiliary.backward()
        self.assertIsNone(model.decoder.weight.grad)
        self.assertIsNone(model.decoder.bias.grad)
        self.assertIsNotNone(model.encoder.weight.grad)
        self.assertTrue(torch.isfinite(model.encoder.weight.grad).all())

    def test_native_coordinate_scaling_and_loss_units(self):
        config = SAEConfig("relu", 5, 12)
        scaled = SparseAutoencoder(config, binding()).set_normalization_(3.)
        normal = SparseAutoencoder(config, binding())
        raw_mean = torch.arange(5).float()
        scaled.initialize_bias_(raw_mean)
        normal.initialize_bias_(raw_mean / 3)
        raw = torch.randn(9, 5) * 3
        scaled_reconstruction, scaled_features = scaled(raw)
        reconstruction, features = normal(raw / 3)
        self.assertTrue(torch.allclose(scaled_features, features))
        self.assertTrue(torch.allclose(scaled_reconstruction, reconstruction * 3))
        self.assertTrue(torch.allclose(scaled.decode(torch.zeros(1, 12))[0], raw_mean))
        self.assertTrue(torch.allclose(scaled.loss(raw)["loss"], normal.loss(raw / 3)["loss"]))
        expected_mse = ((scaled_reconstruction - raw) / 3).square().sum(-1).mean()
        self.assertTrue(torch.allclose(scaled.loss(raw)["reconstruction"], expected_mse))

    def test_seed_is_local_and_repeatable(self):
        torch.manual_seed(91)
        before = torch.get_rng_state().clone()
        first = SparseAutoencoder(SAEConfig("relu", 5, 12, seed=17), binding())
        self.assertTrue(torch.equal(torch.get_rng_state(), before))
        second = SparseAutoencoder(SAEConfig("relu", 5, 12, seed=17), binding())
        self.assertTrue(torch.equal(first.decoder.weight, second.decoder.weight))

    def test_portable_save_restore_and_wrong_binding(self):
        model = SparseAutoencoder(SAEConfig("gated", 5, 12), binding()).set_normalization_(2.)
        model.initialize_bias_(torch.ones(5))
        model.is_fitted = True
        query = torch.randn(3, 5)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "dictionary.pt"
            model.save(path)
            artifact = torch.load(path, weights_only=True)
            self.assertEqual(artifact["implementation_variant"], "gated_frozen_decoder_aux_and_detached_aux_centering")
            restored = SparseAutoencoder.load(path, expected_binding=binding())
            self.assertTrue(restored.is_fitted)
            self.assertTrue(torch.equal(model.encode(query), restored.encode(query)))
            self.assertTrue(torch.equal(model(query)[0], restored(query)[0]))
            wrong = deepcopy(binding())
            wrong["hook"]["module"] = "blocks.1"
            with self.assertRaisesRegex(ValueError, "binding differs"):
                SparseAutoencoder.load(path, expected_binding=wrong)

    def test_binding_and_scale_fail_closed(self):
        bad = binding()
        bad["tokenizer_id"] = "unspecified"
        with self.assertRaisesRegex(ValueError, "tokenizer_id"):
            SparseAutoencoder(SAEConfig("relu", 5, 12), bad)
        model = SparseAutoencoder(SAEConfig("relu", 5, 12), binding())
        for scale in (0, -1, float("nan")):
            with self.assertRaisesRegex(ValueError, "positive scalar"):
                model.set_normalization_(scale)

    def test_external_backend_uses_exact_encode_decode_and_rejects_scaling(self):
        class FakeSAE(nn.Module):
            def __init__(self):
                super().__init__()
                self.weight = nn.Parameter(torch.eye(5))
                self.cfg = SimpleNamespace(d_in=5, d_sae=5, architecture=lambda: "standard",
                    normalize_activations="none", apply_b_dec_to_input=False,
                    reshape_activations="none", metadata=SimpleNamespace(hook_layer=0))

            def encode(self, raw):
                return raw @ self.weight

            def decode(self, features):
                return features @ self.weight.T

        source = FakeSAE()
        wrapped = SAELensAdapter(source, binding(), expected_binding=binding())
        query = torch.randn(3, 5)
        self.assertTrue(torch.equal(wrapped(query)[0], query))
        self.assertFalse(wrapped.source_metadata["apply_b_dec_to_input"])
        source.cfg.normalize_activations = "constant_norm_rescale"
        with self.assertRaisesRegex(ValueError, "normalize_activations='none'"):
            SAELensAdapter(source, binding())
        source.cfg.normalize_activations = "none"
        source.cfg.metadata.model_name = "another-base-model"
        with self.assertRaisesRegex(ValueError, "declared model differs"):
            SAELensAdapter(source, binding())
        source.cfg.metadata.model_name = "toy"
        source.cfg.metadata.hook_name = "blocks.0.hook_resid_post"
        with self.assertRaisesRegex(ValueError, "backend_hook_name"):
            SAELensAdapter(source, binding())
        explicit = {**binding(), "backend_hook_name": "blocks.0.hook_resid_post"}
        self.assertEqual(SAELensAdapter(source, explicit).config.d_in, 5)


if __name__ == "__main__":
    unittest.main()
