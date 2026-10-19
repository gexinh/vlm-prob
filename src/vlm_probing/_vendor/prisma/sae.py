# Vendored from ViT-Prisma; MIT license and exact provenance: ../LICENSE / SOURCE.json.
"""Most of this is just copied over from Arthur's code and slightly simplified:
https://github.com/ArthurConmy/sae/blob/main/sae/model.py
"""

from __future__ import annotations


import logging
import math
from abc import ABC, abstractmethod

# import fields
from typing import Any, Callable

import einops
import torch
from torch import nn

from .hook_point import HookPoint
from .hooked_root_module import HookedRootModule
from .config import VisionModelSAERunnerConfig


class SparseAutoencoder(HookedRootModule, ABC):
    """ """

    def __init__(
        self,
        cfg: VisionModelSAERunnerConfig,
    ):
        super().__init__()
        self.cfg = cfg
        self.d_in = cfg.d_in
        if not isinstance(self.d_in, int):
            raise ValueError(
                f"d_in must be an int but was {self.d_in}; {type(self.d_in)}"
            )
        assert cfg.d_sae is not None  # keep pyright happy
        self.d_sae = cfg.d_sae
        self.l1_coefficient = cfg.l1_coefficient
        self.lp_norm = cfg.lp_norm
        self.dtype = cfg.dtype
        self.device = cfg.device
        self.initialization_method = cfg.initialization_method
        self.zero_loss = torch.tensor(0.0, dtype=self.dtype, device=self.device)

        self.initialize_sae_weights()

        self.hook_sae_in = HookPoint()
        self.hook_hidden_pre = HookPoint()
        self.hook_hidden_post = HookPoint()
        self.hook_sae_out = HookPoint()

        # handle run time activation normalization if needed:
        if self.cfg.normalize_activations == "constant_norm_rescale":

            #  we need to scale the norm of the input and store the scaling factor
            def run_time_activation_norm_fn_in(x: torch.Tensor) -> torch.Tensor:
                self.x_norm_coeff = (self.cfg.d_in**0.5) / x.norm(dim=-1, keepdim=True)
                x = x * self.x_norm_coeff
                return x

            def run_time_activation_norm_fn_out(x: torch.Tensor) -> torch.Tensor:  #
                x = x / self.x_norm_coeff
                del self.x_norm_coeff  # prevents reusing
                return x

            self.run_time_activation_norm_fn_in = run_time_activation_norm_fn_in
            self.run_time_activation_norm_fn_out = run_time_activation_norm_fn_out
        elif self.cfg.normalize_activations == "layer_norm":

            #  we need to scale the norm of the input and store the scaling factor
            def run_time_activation_ln_in(
                x: torch.Tensor, eps: float = 1e-5
            ) -> torch.Tensor:
                mu = x.mean(dim=-1, keepdim=True)
                x = x - mu
                std = x.std(dim=-1, keepdim=True)
                x = x / (std + eps)
                self.ln_mu = mu
                self.ln_std = std
                return x

            def run_time_activation_ln_out(x: torch.Tensor, eps: float = 1e-5):
                return x * self.ln_std + self.ln_mu

            self.run_time_activation_norm_fn_in = run_time_activation_ln_in
            self.run_time_activation_norm_fn_out = run_time_activation_ln_out
        else:
            self.run_time_activation_norm_fn_in = lambda x: x
            self.run_time_activation_norm_fn_out = lambda x: x

        self.activation_fn = get_activation_fn(
            self.cfg.activation_fn_str, **self.cfg.activation_fn_kwargs
        )

        self.setup()  # Required for `HookedRootModule`s

    def initialize_weights(self, out_features, in_features):
        """
        Initialize weights for the Sparse Autoencoder.

        This function uses Kaiming uniform initialization and then normalizes
        the weights to have unit normls
         along the output dimension.

        Args:
        out_features (int): Number of output features
        in_features (int): Number of input features

        Returns:
        torch.Tensor: Initialized weight matrix
        """
        weight = torch.empty(
            out_features, in_features, dtype=self.dtype, device=self.device
        )

        # Kaiming uniform initialization
        nn.init.kaiming_uniform_(weight, a=math.sqrt(5))

        # Normalize to unit norm along output dimension
        with torch.no_grad():
            weight /= torch.norm(weight, dim=1, keepdim=True)

        return weight

    @abstractmethod
    def encode(self, x: torch.Tensor): ...

    @abstractmethod
    def decode(self, features: torch.Tensor): ...

    @abstractmethod
    def initialize_sae_weights(self): ...

    @abstractmethod
    def forward(self, x: torch.Tensor, dead_neuron_mask: torch.Tensor = None): ...

    def _compute_mse_loss(self, x: torch.Tensor, sae_out: torch.Tensor) -> torch.Tensor:
        x_centred = x - x.mean(dim=0, keepdim=True)
        mse_loss = torch.nn.functional.mse_loss(sae_out, x.detach(), reduction="none")
        norm_factor = torch.norm(x_centred, p=2, dim=-1, keepdim=True)
        mse_loss = (mse_loss / norm_factor).mean()
        return mse_loss

    def _compute_ghost_residual_loss(
        self,
        x: torch.Tensor,
        sae_out: torch.Tensor,
        hidden_pre: torch.Tensor,
        dead_neuron_mask: torch.Tensor,
    ) -> torch.Tensor:
        # Compute residuals
        residual = x - sae_out
        residual_centred = residual - residual.mean(dim=0, keepdim=True)
        l2_norm_residual = torch.norm(residual, dim=-1)

        # Compute ghost output from dead neurons
        feature_acts_dead_neurons_only = torch.exp(hidden_pre[:, dead_neuron_mask])
        ghost_out = feature_acts_dead_neurons_only @ self.W_dec[dead_neuron_mask, :]
        l2_norm_ghost_out = torch.norm(ghost_out, dim=-1)
        norm_scaling_factor = l2_norm_residual / (1e-6 + l2_norm_ghost_out * 2)
        ghost_out = ghost_out * norm_scaling_factor[:, None].detach()

        # Compute ghost residual loss
        mse_loss_ghost_resid = (
            torch.pow((ghost_out - residual.detach().float()), 2)
            / (residual_centred.detach() ** 2).sum(dim=-1, keepdim=True).sqrt()
        )
        mse_rescaling_factor = (
            self._compute_mse_loss(x, sae_out) / (mse_loss_ghost_resid + 1e-6)
        ).detach()
        mse_loss_ghost_resid = (mse_rescaling_factor * mse_loss_ghost_resid).mean()
        return mse_loss_ghost_resid






    @torch.no_grad()
    def set_decoder_norm_to_unit_norm(self):
        self.W_dec.data /= torch.norm(self.W_dec.data, dim=1, keepdim=True)

    @torch.no_grad()
    def remove_gradient_parallel_to_decoder_directions(self):
        """
        Update grads so that they remove the parallel component
            (d_sae, d_in) shape
        """

        parallel_component = einops.einsum(
            self.W_dec.grad,
            self.W_dec.data,
            "d_sae d_in, d_sae d_in -> d_sae",
        )
        assert parallel_component is not None  # keep pyright happy

        self.W_dec.grad -= einops.einsum(
            parallel_component,
            self.W_dec.data,
            "d_sae, d_sae d_in -> d_sae d_in",
        )




    def get_name(self):
        sae_name = f"sparse_autoencoder_{self.cfg.model_name}_{self.cfg.hook_point}_{self.cfg.d_sae}"
        return sae_name


class StandardSparseAutoencoder(SparseAutoencoder):

    def initialize_sae_weights(self):
        self.W_dec = nn.Parameter(self.initialize_weights(self.d_sae, self.d_in))

        if self.initialization_method == "independent":
            self.W_enc = nn.Parameter(self.initialize_weights(self.d_in, self.d_sae))
        elif self.initialization_method == "encoder_transpose_decoder":
            self.W_enc = nn.Parameter(self.W_dec.data.t().clone())
        else:
            raise ValueError(
                f"Unknown initialization method: {self.initialization_method}"
            )

        self.b_enc = nn.Parameter(
            torch.zeros(self.d_sae, dtype=self.dtype, device=self.device)
        )

        self.b_dec = nn.Parameter(
            torch.zeros(self.d_in, dtype=self.dtype, device=self.device)
        )

    def encode(self, x: torch.Tensor, return_hidden_pre: bool = False):
        # move x to correct dtype
        x = x.to(self.dtype)

        sae_in = self.run_time_activation_norm_fn_in(x)

        sae_in = self.hook_sae_in(
            sae_in - self.b_dec
        )  # Remove decoder bias as per Anthropic

        hidden_pre = self.hook_hidden_pre(
            einops.einsum(
                sae_in,
                self.W_enc,
                "... d_in, d_in d_sae -> ... d_sae",
            )
            + self.b_enc
        )

        feature_acts = self.hook_hidden_post(self.activation_fn(hidden_pre))

        if return_hidden_pre:
            return sae_in, feature_acts, hidden_pre

        return sae_in, feature_acts

    def decode(self, features: torch.Tensor):
        sae_out = self.hook_sae_out(
            einops.einsum(
                features,
                self.W_dec,
                "... d_sae, d_sae d_in -> ... d_in",
            )
            + self.b_dec
        )

        sae_out = self.run_time_activation_norm_fn_out(sae_out)

        return sae_out

    def forward(
        self, x: torch.Tensor, dead_neuron_mask: torch.Tensor = None, *args, **kwargs
    ):

        # Encode input and get feature activations and pre-activation hidden state
        _, feature_acts, hidden_pre = self.encode(x, return_hidden_pre=True)
        sae_out = self.decode(feature_acts)

        # Compute MSE loss, normalized by input centering
        mse_loss = self._compute_mse_loss(x, sae_out)

        # Compute ghost residual loss if required
        if self.cfg.use_ghost_grads and self.training and dead_neuron_mask is not None:
            mse_loss_ghost_resid = self._compute_ghost_residual_loss(
                x, sae_out, hidden_pre, dead_neuron_mask
            )
        else:
            mse_loss_ghost_resid = self.zero_loss

        # Compute sparsity loss
        sparsity = feature_acts.norm(p=self.lp_norm, dim=1).mean(dim=(0,))

        # Combine losses based on activation function type
        l1_loss = (
            self.l1_coefficient * sparsity
            if self.cfg.activation_fn_str != "topk"
            else None
        )

        loss = mse_loss + (l1_loss if l1_loss is not None else 0) + mse_loss_ghost_resid

        # Placeholder for auxiliary reconstruction loss
        aux_reconstruction_loss = torch.tensor(0.0)

        if hasattr(
            self.cfg, "return_out_only"
        ):  # to work with HookedSAEViT efficiently
            if self.cfg.return_out_only:
                return sae_out

        return (
            sae_out,
            feature_acts,
            loss,
            mse_loss,
            l1_loss,
            mse_loss_ghost_resid,
            aux_reconstruction_loss,
        )


class GatedSparseAutoencoder(SparseAutoencoder):

    def __init__(
        self,
        cfg: VisionModelSAERunnerConfig,
    ):
        super().__init__(cfg)
        assert (
            self.cfg.use_ghost_grads == False
        ), "Gated SAE does not support ghost grads"

    def initialize_sae_weights(self):
        self.W_enc = nn.Parameter(
            torch.nn.init.kaiming_uniform_(
                torch.empty(
                    self.cfg.d_in, self.cfg.d_sae, dtype=self.dtype, device=self.device
                )
            )
        )

        self.b_gate = nn.Parameter(
            torch.zeros(self.cfg.d_sae, dtype=self.dtype, device=self.device)
        )

        self.r_mag = nn.Parameter(
            torch.zeros(self.cfg.d_sae, dtype=self.dtype, device=self.device)
        )

        self.b_mag = nn.Parameter(
            torch.zeros(self.cfg.d_sae, dtype=self.dtype, device=self.device)
        )

        self.W_dec = nn.Parameter(
            torch.nn.init.kaiming_uniform_(
                torch.empty(
                    self.cfg.d_sae, self.cfg.d_in, dtype=self.dtype, device=self.device
                )
            )
        )

        self.b_enc = nn.Parameter(
            torch.zeros(self.d_sae, dtype=self.dtype, device=self.device)
        )

        self.b_dec = nn.Parameter(
            torch.zeros(self.d_in, dtype=self.dtype, device=self.device)
        )

    def encode(self, x: torch.Tensor):
        x = x.to(self.dtype)
        x = self.run_time_activation_norm_fn_in(x)

        sae_in = self.hook_sae_in(x - self.b_dec)

        # Gating path
        gating_pre_activation = sae_in @ self.W_enc + self.b_gate
        active_features = (gating_pre_activation > 0).to(self.dtype)

        # Magnitude path with weight sharing
        magnitude_pre_activation = sae_in @ (self.W_enc * self.r_mag.exp()) + self.b_mag

        feature_magnitudes = self.activation_fn(magnitude_pre_activation)

        feature_acts = self.hook_hidden_post(active_features * feature_magnitudes)

        return sae_in, feature_acts

    def decode(self, features: torch.Tensor):
        sae_out = self.hook_sae_out(
            einops.einsum(
                features,
                self.W_dec,
                "... d_sae, d_sae d_in -> ... d_in",
            )
            + self.b_dec
        )

        sae_out = self.run_time_activation_norm_fn_out(sae_out)

        return sae_out

    def forward(self, x: torch.Tensor, *args, **kwargs):

        sae_in, feature_acts = self.encode(x)
        sae_out = self.decode(feature_acts)

        # Compute MSE loss, normalized by input centering
        mse_loss = self._compute_mse_loss(x, sae_out)

        # Compute gate activations
        pi_gate_act = self._compute_gate_activation(sae_in)

        # Compute sparsity (L1) loss
        l1_loss = (
            self._compute_l1_loss(pi_gate_act)
            if self.cfg.activation_fn_str != "topk"
            else self.zero_loss
        )

        # Compute auxiliary reconstruction loss
        aux_reconstruction_loss = self._compute_aux_reconstruction_loss(
            pi_gate_act, sae_in
        )

        loss = mse_loss + l1_loss + aux_reconstruction_loss

        # Initialize ghost residual loss (not used for gated SAEs)
        mse_loss_ghost_resid = self.zero_loss

        if hasattr(
            self.cfg, "return_out_only"
        ):  # to work with HookedSAEViT efficiently
            if self.cfg.return_out_only:
                return sae_out

        return (
            sae_out,
            feature_acts,
            loss,
            mse_loss,
            l1_loss,
            mse_loss_ghost_resid,
            aux_reconstruction_loss,
        )

    def _compute_gate_activation(self, sae_in: torch.Tensor) -> torch.Tensor:
        """Compute gate activations based on configuration."""
        pi_gate = sae_in @ self.W_enc + self.b_gate
        if self.cfg.activation_fn_str == "topk":
            return self.activation_fn(pi_gate)
        return torch.relu(pi_gate)

    def _compute_l1_loss(self, pi_gate_act: torch.Tensor) -> torch.Tensor:
        """Compute sparsity (L1) loss."""
        return (
            self.l1_coefficient
            * torch.sum(pi_gate_act * self.W_dec.norm(dim=1), dim=-1).mean()
        )

    def _compute_aux_reconstruction_loss(
        self, pi_gate_act: torch.Tensor, sae_in: torch.Tensor
    ) -> torch.Tensor:
        """Compute auxiliary reconstruction loss."""
        via_gate_reconstruction = pi_gate_act @ self.W_dec + self.b_dec
        return torch.sum((via_gate_reconstruction - sae_in) ** 2, dim=-1).mean()


class TopK(nn.Module):
    def __init__(
        self, k: int, postact_fn: Callable[[torch.Tensor], torch.Tensor] = nn.ReLU()
    ):
        super().__init__()
        self.k = k
        self.postact_fn = postact_fn

    def forward(self, x: torch.Tensor) -> torch.Tensor:

        topk = torch.topk(x, k=self.k, dim=-1)
        values = self.postact_fn(topk.values)
        result = torch.zeros_like(x)
        result.scatter_(-1, topk.indices, values)

        return result


def get_activation_fn(
    activation_fn: str, **kwargs: Any
) -> Callable[[torch.Tensor], torch.Tensor]:

    logging.info(
        f"get_activation_fn received: activation_fn={activation_fn}, kwargs={kwargs}"
    )

    if activation_fn == "relu":
        return torch.nn.ReLU()
    elif activation_fn == "tanh-relu":

        def tanh_relu(input: torch.Tensor) -> torch.Tensor:
            input = torch.relu(input)
            input = torch.tanh(input)
            return input

        return tanh_relu
    elif activation_fn == "topk":
        assert "k" in kwargs, "TopK activation function requires a k value."
        k = kwargs.get("k", 64)  # Default k to 1 if not provided
        postact_fn = kwargs.get(
            "postact_fn", nn.ReLU()
        )  # Default post-activation to ReLU if not provided
        return TopK(k, postact_fn)
    else:
        raise ValueError(f"Unknown activation function: {activation_fn}")
