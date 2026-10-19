"""Scientific contracts for algorithm-composed SAEs and training state."""
from dataclasses import asdict
import json

import pytest
import torch
from torch.nn import functional as F

from vlmprobe.sae.models import ARCHITECTURES, SAEConfig, SparseAutoencoder
from vlmprobe.sae.algorithms import JumpReLU, Step
from vlmprobe.sae.registry import get_method, list_methods, method_config


def binding():
    return {"model_id": "toy@sha256:weights", "tokenizer_id": "sha256:tokenizer",
            "preprocessing_id": "identity-v1", "calibration_id": "independent-v1",
            "site": "residual.0", "layer": 0,
            "hook": {"module": "block", "kind": "output", "selector": None, "tensor_slice": None}}


@pytest.fixture(autouse=True)
def threads():
    torch.set_num_threads(1)


def model(architecture="topk", d_in=4, d_sae=8, **kwargs):
    return SparseAutoencoder(SAEConfig(architecture, d_in, d_sae, k=kwargs.pop("k", 2),
        archetypal_candidates=8, **kwargs), binding())


@pytest.mark.parametrize("architecture", ARCHITECTURES)
def test_every_method_has_one_trainable_native_contract_and_validation_is_readonly(architecture):
    instance = model(architecture)
    values = torch.randn(7, 4)
    if instance.config.dictionary == "archetypal":
        with pytest.raises(ValueError, match="TRAIN"):
            instance.encode(values)
        instance.initialize_dictionary_(values)
    optimizer = torch.optim.Adam(instance.parameters(), lr=.001)
    losses = instance.loss(values)
    assert set(losses) == {"loss", "reconstruction", "sparsity", "auxiliary"}
    losses["loss"].backward()
    assert all(parameter.grad is None or torch.isfinite(parameter.grad).all() for parameter in instance.parameters())
    optimizer.step()
    instance.post_optimizer_step_()
    instance.eval()
    state = {name: value.clone() for name, value in instance.state_dict().items()}
    losses = instance.loss(values)
    reconstruction, features = instance(values)
    assert reconstruction.shape == values.shape and features.shape == (7, 8)
    assert torch.isfinite(losses["loss"])
    for name, value in instance.state_dict().items():
        assert torch.equal(value, state[name]), name
    assert type(instance).__module__ == "vlm_probing.sae.models"


@pytest.mark.parametrize("architecture", ["relu", "topk", "gated"])
def test_original_three_kernels_preserve_exact_core_values_and_objectives(architecture):
    instance = model(architecture)
    raw = torch.randn(9, 4)
    instance.set_normalization_(3.)
    instance.initialize_bias_(torch.randn(4))
    normalized = raw / 3
    centered = normalized - instance.decoder.bias
    gate = F.linear(centered, instance.encoder.weight, instance.encoder.bias)
    if architecture == "relu":
        features = gate.relu()
    elif architecture == "topk":
        values, indices = gate.topk(2, dim=-1, sorted=False)
        features = torch.zeros_like(gate).scatter(-1, indices, values.relu())
    else:
        magnitude = F.linear(centered, instance.encoder.weight * instance.log_magnitude_scale.exp()[:, None],
                             instance.magnitude_bias).relu()
        features = (gate > 0).to(magnitude) * magnitude
    reconstructed = instance.decoder(features)
    actual, actual_features = instance(raw)
    assert torch.equal(features, actual_features)
    assert torch.equal(actual, reconstructed * 3)
    losses = instance.loss(raw)
    assert torch.equal(losses["reconstruction"], (reconstructed - normalized).square().sum(-1).mean())
    if architecture == "gated":
        auxiliary_gate = F.linear(normalized - instance.decoder.bias.detach(),
                                 instance.encoder.weight, instance.encoder.bias).relu()
        expected = F.linear(auxiliary_gate, instance.decoder.weight.detach(), instance.decoder.bias.detach())
        assert torch.equal(losses["auxiliary"], (expected - normalized).square().sum(-1).mean())


def test_signed_topk_selects_negative_magnitude_instead_of_discarding_it():
    instance = model("abstopk", d_in=4, d_sae=4, normalize_decoder=False)
    with torch.no_grad():
        instance.encoder.weight.copy_(torch.eye(4)); instance.encoder.bias.zero_(); instance.decoder.bias.zero_()
    actual = instance.encode(torch.tensor([[-8., 2., -3., 1.]]))
    assert torch.equal(actual, torch.tensor([[-8., 0., -3., 0.]]))


def test_batch_budget_units_calibration_and_evaluation_batch_independence():
    values = torch.tensor([[1., 2., 3., 4.], [5., 6., 7., 8.], [9., 10., 11., 12.]])
    average = model("batchtopk", d_sae=4, batch_budget="average")
    global_budget = model("batchtopk", d_sae=4, k=5, batch_budget="global")
    for instance in (average, global_budget):
        with torch.no_grad():
            instance.encoder.weight.copy_(torch.eye(4)); instance.encoder.bias.zero_(); instance.decoder.bias.zero_()
    assert int((average.encode(values) != 0).sum()) == 6
    assert int((global_budget.encode(values) != 0).sum()) == 5
    global_budget.eval()
    with pytest.raises(ValueError, match="TRAIN"):
        global_budget.encode(values)
    global_budget.calibrate_(values)
    assert int(global_budget.training_steps) == 0 and int(global_budget.inactive_steps.sum()) == 0
    assert torch.equal(global_budget.encode(values[:1]), global_budget.encode(values)[:1])


def test_jump_rectangle_surrogate_has_distinct_l0_threshold_gradient():
    values = torch.tensor([[.08, .12]], requires_grad=True)
    threshold = torch.tensor([.1, .1], requires_grad=True)
    output = JumpReLU.apply(values, threshold, .1, False)
    output.sum().backward()
    assert torch.equal(output, torch.tensor([[0., .12]]))
    torch.testing.assert_close(threshold.grad, torch.tensor([-1., -1.]))
    assert torch.equal(values.grad, torch.tensor([[0., 1.]]))
    threshold.grad = None
    count = Step.apply(values.detach(), threshold, .1, False)
    count.sum().backward()
    torch.testing.assert_close(threshold.grad, torch.tensor([-10., -10.]))


def test_matryoshka_is_weighted_nested_reconstruction_not_another_trainer():
    instance = model("matryoshka_batchtopk", matryoshka_widths=(2, 8), matryoshka_weights=(.25, 1.5))
    values = torch.randn(5, 4)
    z = instance.encode(values)
    expected = 1.5 * (instance.decoder(z) - values).square().sum(-1).mean()
    inner = F.linear(z[:, :2], instance.decoder.weight[:, :2], instance.decoder.bias)
    expected = expected + .25 * (inner - values).square().sum(-1).mean()
    torch.testing.assert_close(instance.loss(values)["reconstruction"], expected)


def test_archetypal_constraint_and_training_only_anchor_transform():
    instance = model("archetypal_topk", archetypal_delta=.2)
    instance.set_normalization_(2.)
    mean = torch.arange(4).float()
    instance.initialize_bias_(mean)
    anchors = torch.arange(32).reshape(8, 4).float()
    instance.initialize_dictionary_(anchors)
    assert torch.equal(instance.decoder.anchors, (anchors - mean) / 2)
    mixture = instance.decoder.coefficients.softmax(-1)
    assert (mixture >= 0).all()
    torch.testing.assert_close(mixture.sum(-1), torch.ones(8))
    with torch.no_grad():
        instance.decoder.relaxation.fill_(3.)
    instance.post_optimizer_step_()
    assert (instance.decoder.relaxation.norm(dim=0) <= .200001).all()


@pytest.mark.parametrize("architecture,signed", [("matching_pursuit", False), ("signed_matching_pursuit", True),
    ("orthogonal_matching_pursuit", False), ("signed_orthogonal_matching_pursuit", True)])
def test_pursuit_variants_refit_known_identity_dictionary(architecture, signed):
    instance = model(architecture, d_in=3, d_sae=3, k=3, pursuit_iterations=3, residual_tolerance=0., normalize_decoder=False)
    with torch.no_grad():
        instance.decoder.weight.copy_(torch.eye(3)); instance.decoder.bias.zero_()
    raw = torch.tensor([[-2., 1., 3.]])
    expected = raw if signed else raw.relu()
    torch.testing.assert_close(instance.encode(raw), expected, atol=1e-5, rtol=1e-5)


def test_signed_omp_joint_refit_removes_error_left_by_greedy_coefficients():
    greedy = model("signed_matching_pursuit", d_in=2, d_sae=2, k=2,
                   pursuit_iterations=2, residual_tolerance=0., normalize_decoder=False)
    orthogonal = model("signed_orthogonal_matching_pursuit", d_in=2, d_sae=2, k=2,
                       pursuit_iterations=2, residual_tolerance=0., normalize_decoder=False)
    dictionary = torch.tensor([[1., 2 ** -.5], [0., 2 ** -.5]])
    for instance in (greedy, orthogonal):
        with torch.no_grad():
            instance.decoder.weight.copy_(dictionary); instance.decoder.bias.zero_()
    raw = torch.tensor([[0., 1.]])
    assert (greedy(raw)[0] - raw).norm() > .1
    torch.testing.assert_close(orthogonal(raw)[0], raw, atol=1e-6, rtol=1e-6)


def test_auxk_trains_inactive_encoder_directions_and_jump_threshold_keeps_fp32():
    instance = model("topk", d_in=4, d_sae=4, k=1, auxk_coefficient=.1,
                     auxk_k=2, dead_feature_steps=1)
    with torch.no_grad():
        instance.encoder.weight.copy_(torch.eye(4) * .5); instance.encoder.bias.zero_()
        instance.decoder.weight.copy_(torch.eye(4)); instance.decoder.bias.zero_()
        instance.inactive_steps.fill_(2)
    auxiliary = instance.loss(torch.tensor([[4., 3., 2., 1.]]))["auxiliary"]
    auxiliary.backward()
    assert torch.isfinite(auxiliary) and auxiliary > 0
    assert instance.encoder.weight.grad[1].abs().sum() > 0
    jump = model("jumprelu").to(dtype=torch.bfloat16)
    assert jump.encoder.weight.dtype == torch.bfloat16
    assert jump.threshold.dtype == torch.float32


@pytest.mark.parametrize("normalization,correction", [("layer_norm", 0), ("layer_norm", 1), ("constant_norm_rescale", 0)])
def test_normalization_context_is_explicit_reusable_and_in_raw_units(normalization, correction):
    instance = model("relu", normalization=normalization, normalization_std_correction=correction)
    raw = torch.randn(5, 4) * 3 + 8
    z, context = instance.encode_with_context(raw)
    reconstruction = instance.decode_with_context(z, context)
    with pytest.raises(ValueError, match="context"):
        instance.decode(z)
    if normalization == "layer_norm":
        expected = instance.decoder(z) * raw.std(-1, correction=correction, keepdim=True) + raw.mean(-1, keepdim=True)
    else:
        expected = instance.decoder(z) * raw.norm(dim=-1, keepdim=True) / 2
    torch.testing.assert_close(reconstruction, expected)
    assert torch.equal(instance.decode_with_context(z, context), reconstruction)


def test_registry_is_algorithm_first_and_experimental_scope_is_explicit():
    rows = list_methods()
    assert {row["name"] for row in rows} == set(ARCHITECTURES)
    assert all(row["family"] == "sae" and row["sources"] for row in rows)
    assert get_method("qsae")["status"] == "experimental"
    assert "approximate" in get_method("omp")["math_notes"]
    assert "provider" not in method_config("topk", d_in=4, d_sae=8, k=2).__dict__
    json.dumps(asdict(method_config("jumprelu", d_in=4, d_sae=8)))
