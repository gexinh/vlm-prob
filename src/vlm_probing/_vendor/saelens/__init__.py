"""Pinned and locally controlled SAELens activation-vector core.

MIT-licensed selected source from decoderesearch/SAELens. No official package,
TransformerLens model stack, datasets runner or remote logging is imported.
"""
import logging
__version__ = "6.54.6"
VENDORED_REVISION = 1
logger = logging.getLogger(__name__)

from .saes import *
from .registry import register_sae_class, register_sae_training_class

register_sae_class('standard', StandardSAE, StandardSAEConfig)
register_sae_training_class('standard', StandardTrainingSAE, StandardTrainingSAEConfig)
register_sae_class('gated', GatedSAE, GatedSAEConfig)
register_sae_training_class('gated', GatedTrainingSAE, GatedTrainingSAEConfig)
register_sae_class('topk', TopKSAE, TopKSAEConfig)
register_sae_training_class('topk', TopKTrainingSAE, TopKTrainingSAEConfig)
register_sae_class('abstopk', AbsTopKSAE, AbsTopKSAEConfig)
register_sae_training_class('abstopk', AbsTopKTrainingSAE, AbsTopKTrainingSAEConfig)
register_sae_class('jumprelu', JumpReLUSAE, JumpReLUSAEConfig)
register_sae_training_class('jumprelu', JumpReLUTrainingSAE, JumpReLUTrainingSAEConfig)
register_sae_class('matching_pursuit', MatchingPursuitSAE, MatchingPursuitSAEConfig)
register_sae_training_class('matching_pursuit', MatchingPursuitTrainingSAE, MatchingPursuitTrainingSAEConfig)
register_sae_training_class('batchtopk', BatchTopKTrainingSAE, BatchTopKTrainingSAEConfig)
register_sae_training_class('matryoshka_batchtopk', MatryoshkaBatchTopKTrainingSAE, MatryoshkaBatchTopKTrainingSAEConfig)

from .config import SAETrainerConfig, LoggingConfig
from .training.sae_trainer import SAETrainer
