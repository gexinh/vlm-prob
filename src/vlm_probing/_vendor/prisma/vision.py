"""Selected native HookedViT inference core from ViT-Prisma.

Copyright (c) Sonia Joseph. MIT license: LICENSE. Remote model conversion,
text/video models and broad analysis helpers are deliberately not vendored.
"""
from __future__ import annotations
import torch
from torch import nn
import torch.nn.functional as F
from typing import Dict, Union
from .vision_config import HookedViTConfig
from .hooked_root_module import HookedRootModule
from .hook_point import HookPoint
from .layers.attention import Attention
from .layers.head import Head
from .layers.layer_norm import LayerNorm, LayerNormPre
from .layers.mlp import MLP
from .layers.patch_embedding import PatchEmbedding
from .layers.position_embedding import PosEmbedding
from .layers.transformer_block import TransformerBlock, BertBlock


class HookedViT(HookedRootModule):
    def __init__(
        self,
        cfg: HookedViTConfig,
    ):
        """
        Model initialization
        """

        super().__init__()
        if isinstance(cfg, Dict):
            cfg = HookedViTConfig(**cfg)
        elif isinstance(cfg, str):
            raise ValueError(
                "Please pass in a config dictionary or HookedViT object. If you want to load a "
                "pretrained model, use HookedViT.from_pretrained() instead."
            )
        self.cfg = cfg
        if cfg.is_video_transformer:
            raise ValueError("The selected vendored core supports image ViTs, not video models")

        # ClS token
        self.cls_token = nn.Parameter(torch.randn(1, 1, self.cfg.d_model))

        # Patch embeddings
        self.embed = PatchEmbedding(self.cfg)

        self.hook_embed = HookPoint()

        # Position embeddings
        self.pos_embed = PosEmbedding(self.cfg)
        self.hook_pos_embed = HookPoint()

        self.hook_full_embed = HookPoint()

        if self.cfg.layer_norm_pre:  # Put layernorm after attn/mlp layers, not before
            if self.cfg.normalization_type == "LN":
                self.ln_pre = LayerNorm(self.cfg)
            elif self.cfg.normalization_type == "LNPre":
                self.ln_pre = LayerNormPre(self.cfg)
            elif self.cfg.normalization_type is None:
                self.ln_pre = nn.Identity()
            else:
                raise ValueError(
                    f"Invalid normalization type: {self.cfg.normalization_type}"
                )
            self.hook_ln_pre = HookPoint()
        else:
            print("ln_pre not set")

        # Blocks
        if self.cfg.use_bert_block:
            block = BertBlock
        else:
            block = TransformerBlock

        self.blocks = nn.ModuleList(
            [block(self.cfg, block_index) for block_index in range(self.cfg.n_layers)]
        )
        # Final layer norm
        if self.cfg.normalization_type == "LN":
            self.ln_final = LayerNorm(self.cfg)
        elif self.cfg.normalization_type == "LNPre":
            self.ln_final = LayerNormPre(self.cfg)
        elif self.cfg.normalization_type is None:
            self.ln_final = nn.Identity()
        else:
            raise ValueError(
                f"Invalid normalization type: {self.cfg.normalization_type}"
            )

        self.hook_ln_final = HookPoint()

        # Final classification head
        self.head = Head(self.cfg)

        self.hook_post_head_pre_normalize = HookPoint()

        # Initialize weights
        self.init_weights()

        # Set up HookPoints
        self.setup()


    def forward(
        self,
        input: Union[Float[torch.Tensor, "batch height width channels"],],
        stop_at_layer: Optional[int] = None,
    ):
        """Forward Pass.
        Args:
            stop_at_layer Optional[int]: If not None, stop the forward pass at the specified layer.
                Exclusive - ie, stop_at_layer = 0 will only run the embedding layer, stop_at_layer =
                1 will run the embedding layer and the first transformer block, etc. Supports
                negative indexing. Useful for analysis of intermediate layers, eg finding neuron
                activations in layer 3 of a 24 layer model. Defaults to None (run the full model).
                If not None, we return the last residual stream computed.
        """

        batch_size = input.shape[0]

        embed = self.hook_embed(self.embed(input))

        if self.cfg.use_cls_token:
            cls_tokens = self.cls_token.expand(
                batch_size, -1, -1
            )  # CLS token for each item in the batch
            embed = torch.cat((cls_tokens, embed), dim=1)  # Add to embedding

        pos_embed = self.hook_pos_embed(self.pos_embed(input))

        residual = embed + pos_embed

        self.hook_full_embed(residual)

        if self.cfg.layer_norm_pre:
            residual = self.ln_pre(residual)
            residual = self.hook_ln_pre(residual)

        for block in self.blocks[:stop_at_layer]:
            residual = block(residual)
        if stop_at_layer is not None:
            return residual

        x = self.ln_final(residual)
        self.hook_ln_final(x)

        if self.cfg.classification_type == "gaap":  # GAAP

            x = x.mean(dim=1)
            print(self.cfg.return_type)
        elif self.cfg.classification_type == "cls":  # CLS token
            cls_token = x[:, 0]
            if "dino-vitb" in self.cfg.model_name:
                patches = x[:, 1:]
                patches_pooled = patches.mean(dim=1)
                x = torch.cat(
                    (cls_token.unsqueeze(-1), patches_pooled.unsqueeze(-1)), dim=-1
                )
            else:
                x = cls_token

        x = x if self.cfg.return_type == "pre_logits" else self.head(x)

        self.hook_post_head_pre_normalize(x)

        if self.cfg.normalize_output:
            x = F.normalize(x, dim=-1)

        return x


    def init_weights(self):
        if self.cfg.use_cls_token:
            nn.init.normal_(self.cls_token, std=self.cfg.cls_std)
        # nn.init.trunc_normal_(self.position_embedding, std=self.cfg.pos_std)
        if self.cfg.weight_type == "he":
            for m in self.modules():
                if isinstance(m, PosEmbedding):
                    nn.init.normal_(m.W_pos, std=self.cfg.pos_std)
                elif isinstance(m, Attention):
                    nn.init.xavier_uniform_(m.W_Q)
                    nn.init.xavier_uniform_(m.W_K)
                    nn.init.xavier_uniform_(m.W_V)
                    nn.init.xavier_uniform_(m.W_O)
                elif isinstance(m, MLP):
                    nn.init.kaiming_normal_(m.W_in, nonlinearity="relu")
                    nn.init.kaiming_normal_(m.W_out, nonlinearity="relu")
                    nn.init.zeros_(m.b_out)
                    nn.init.zeros_(m.b_in)
                elif isinstance(m, Head):
                    nn.init.kaiming_normal_(m.W_H, nonlinearity="relu")
                    nn.init.zeros_(m.b_H)
                elif isinstance(m, nn.Linear) or isinstance(m, nn.Conv2d):
                    nn.init.kaiming_normal_(m.weight, nonlinearity="relu")
                    if m.bias is not None:
                        nn.init.constant_(m.bias, 0)
