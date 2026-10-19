# Vendored from ViT-Prisma; MIT license and exact provenance: ../LICENSE / SOURCE.json.

from __future__ import annotations

import torch.nn as nn
import torch

import logging
from ..hook_point import HookPoint
from ..vision_config import HookedViTConfig

from typing import Union, Dict, Optional, List, Tuple


import numpy as np

import einops

from .._ops import einsum

import torch.nn.functional as F



class Attention(nn.Module):

    def __init__(
            self,
            cfg: Union[Dict, HookedViTConfig],
            layer_id: Optional[int] = None,
    ):
        super().__init__()
        if isinstance(cfg, Dict):
            cfg = HookedViTConfig.from_dict(cfg)

        self.cfg = cfg

        # Initialize parameters
        self.W_Q = nn.Parameter(
            torch.empty(
                self.cfg.n_heads,
                self.cfg.d_model,
                self.cfg.d_head,
                dtype = self.cfg.dtype
            )
        )
        self.W_K = nn.Parameter(
            torch.empty(
                self.cfg.n_heads,
                self.cfg.d_model,
                self.cfg.d_head,
                dtype = self.cfg.dtype
            )
        )
        self.W_V = nn.Parameter(
            torch.empty(
                self.cfg.n_heads,
                self.cfg.d_model,
                self.cfg.d_head,
                dtype = self.cfg.dtype
            )
        )
        self.W_O = nn.Parameter(
            torch.empty(
                self.cfg.n_heads,
                self.cfg.d_head,
                self.cfg.d_model,
                dtype = self.cfg.dtype
            )
        )

        # Initialize biases
        self.b_Q = nn.Parameter(
            torch.zeros(self.cfg.n_heads, self.cfg.d_head, dtype=self.cfg.dtype)
        )
        self.b_K = nn.Parameter(
            torch.zeros(self.cfg.n_heads, self.cfg.d_head, dtype=self.cfg.dtype)
        )
        self.b_V = nn.Parameter(
            torch.zeros(self.cfg.n_heads, self.cfg.d_head, dtype=self.cfg.dtype)
        )
        self.b_O = nn.Parameter(torch.zeros(self.cfg.d_model, dtype=self.cfg.dtype))


        # Add hook points
        self.hook_k = HookPoint()  # [batch, pos, head_index, d_head]
        self.hook_q = HookPoint()  # [batch, pos, head_index, d_head]
        self.hook_v = HookPoint()  # [batch, pos, head_index, d_head]
        self.hook_z = HookPoint()  # [batch, pos, head_index, d_head]
        self.hook_attn_scores = HookPoint()  # [batch, head_index, query_pos, key_pos]
        self.hook_pattern = HookPoint()  # [batch, head_index, query_pos, key_pos]
        self.hook_result = HookPoint()  # [batch, pos, head_index, d_model]

        self.layer_id = layer_id

        # Note to Sonia: check this.
        # attn_scale is a constant that we divide the attention scores by pre-softmax. I'm not entirely sure why it matters, but it's probably a mix of softmax not being scale invariant and numerical stability?
        if self.cfg.use_attn_scale:
            self.attn_scale = np.sqrt(self.cfg.d_head)
        else:
            self.attn_scale = 1.0



    def forward(
            self,
            query_input: Union[
                Float[torch.Tensor, "batch pos d_model"],
                Float[torch.Tensor, "batch pos head_index d_model"],
            ],
            key_input: Union[
                Float[torch.Tensor, "batch pos d_model"],
                Float[torch.Tensor, "batch pos head_index d_model"],
            ],
            value_input: Union[
                Float[torch.Tensor, "batch pos d_model"],
                Float[torch.Tensor, "batch pos head_index d_model"],
            ],
            attention_mask: Optional[Float[torch.Tensor, "batch pos pos"]] = None,
    ) -> Float[torch.Tensor, "batch pos d_model"]:

        q, k, v  = self.calculate_qkv_matrices(query_input, key_input, value_input)

        attn_scores = self.calculate_attn_scores(q, k, attention_mask)
        attn_scores = self.hook_attn_scores(attn_scores)

        pattern = F.softmax(attn_scores, dim=-1) # where do I do normalization?
        pattern = torch.where(torch.isnan(pattern), torch.zeros_like(pattern), pattern)
        pattern = self.hook_pattern(pattern)

        pattern = pattern.to(self.cfg.dtype)
        z = self.calculate_z_scores(v, pattern)

        if not self.cfg.use_attn_result:
            out = (
                (
                    einsum(
                        "batch pos head_index d_head, \
                        head_index d_head d_model -> \
                        batch pos d_model",
                        z,
                        self.W_O,
                    )
                )
                + self.b_O
            )
        else:
            # Explicitly calculate the attention result so it can be accessed by a hook.
            # Off by default to not eat through GPU memory.
            result = self.hook_result(
                einsum(
                    "batch pos head_index d_head, \
                    head_index d_head d_model -> \
                    batch pos head_index d_model",
                    z,
                    self.W_O,
                )
            )
            out = (
                einops.reduce(result, "batch pos head_index d_model -> batch pos d_model", "sum")
                + self.b_O
            )
        return out

    def calculate_qkv_matrices(
            self,
            query_input: Union[
                Float[torch.Tensor, "batch pos d_model"],
                Float[torch.Tensor, "batch pos head_index d_model"],
            ],
            key_input: Union[
                Float[torch.Tensor, "batch pos d_model"],
                Float[torch.Tensor, "batch pos head_index d_model"],
            ],
            value_input: Union[
                Float[torch.Tensor, "batch pos d_model"],
                Float[torch.Tensor, "batch pos head_index d_model"],
            ]
    ) -> Tuple[
        Float[torch.Tensor, "batch pos head_index d_head"],
        Float[torch.Tensor, "batch pos head_index d_head"],
        Float[torch.Tensor, "batch pos head_index d_head"],
    ]:
        """
        Calculate the Q, K, V matrices for the attention layer. This is done by multiplying the input by the weight matrices and adding the biases.

        Returns a tuple of (Q, K, V) matrices, each of shape [batch, pos, head_index, d_head]
        """

        if self.cfg.use_split_qkv_input or self.cfg.use_attn_in:
            qkv_einops_string = "batch pos head_index d_model"
        else:
            qkv_einops_string = "batch pos d_model"


        q = self.hook_q(
            einsum(
                f"{qkv_einops_string}, head_index d_model d_head \
                -> batch pos head_index d_head",
                query_input,
                self.W_Q,
            )
            + self.b_Q
        )  # [batch, pos, head_index, d_head]
        k = self.hook_k(
            einsum(
                f"{qkv_einops_string}, head_index d_model d_head \
                -> batch pos head_index d_head",
                key_input,
                self.W_K,
            )
            + self.b_K
        )  # [batch, pos, head_index, d_head]
        v = self.hook_v(
            einsum(
                f"{qkv_einops_string}, head_index d_model d_head \
                -> batch pos head_index d_head",
                value_input,
                self.W_V,
            )
            + self.b_V
        )  # [batch, pos, head_index, d_head]
        return q, k, v

    def calculate_attn_scores(
            self,
            q: Float[torch.Tensor, "batch pos head_index d_head"],
            k: Float[torch.Tensor, "batch pos head_index d_head"],
            attention_mask: Optional[Float[torch.Tensor, "batch pos pos"]] = None,
    ) -> Float[torch.Tensor, "batch head_index query_pos key_pos"]:
        """
        Calculate the attention scores for the attention layer. This is done by multiplying the Q and K matrices together, and dividing by the square root of the dimension of the key vectors.

        Returns a tensor of shape [batch, head_index, query_pos, key_pos]
        """
        attn_scores = einsum(
            "batch query_pos head_index d_head, batch key_pos head_index d_head -> batch head_index query_pos key_pos",
            q,
            k,
        )
        attn_scores = attn_scores / self.attn_scale
        if attention_mask is not None:
            attn_scores = attn_scores + attention_mask
        return attn_scores

    def calculate_z_scores(
            self,
            v: Float[torch.Tensor, "batch key_pos head_index d_head"],
            pattern: Float[torch.Tensor, "batch head_index query_pos key_pos"],
    ) -> Float[torch.Tensor, "batch query_pos head_index d_head"]:
        z = self.hook_z(
            einsum(
                "batch key_pos head_index d_head, \
                batch head_index query_pos key_pos -> \
                batch query_pos head_index d_head",
                v,
                pattern,
            )
        )
        return z
