"""Local activation-vector training configuration, derived from SAELens v6.54.6."""
from dataclasses import dataclass,field

@dataclass
class LoggingConfig:
    log_to_wandb: bool = False
    log_activations_store_to_wandb: bool = False
    log_optimizer_state_to_wandb: bool = False
    log_weights_to_wandb: bool = True
    wandb_project: str = "sae_lens_training"
    wandb_id: str | None = None
    run_name: str | None = None
    wandb_entity: str | None = None
    wandb_log_frequency: int = 10
    eval_every_n_wandb_logs: int = 100

    def __post_init__(self):
        if self.log_to_wandb:
            raise ValueError("Remote WandB logging is not part of the vendored SAE core; use local protocol and checkpoint artifacts")

    def log(self,*args,**kwargs):
        raise NotImplementedError("Remote logging is not part of the vendored SAE core")

@dataclass
class SAETrainerConfig:
    total_training_samples: int
    train_batch_size_samples: int
    lr: float = 3e-4
    lr_end: float | None = None
    lr_scheduler_name: str = "constant"
    lr_warm_up_steps: int = 0
    lr_decay_steps: int = 0
    n_restart_cycles: int = 1
    adam_beta1: float = 0.9
    adam_beta2: float = 0.999
    device: str = "cpu"
    autocast: bool = False
    dead_feature_window: int = 1000
    feature_sampling_window: int = 2000
    n_checkpoints: int = 0
    checkpoint_path: str | None = None
    save_final_checkpoint: bool = False
    logger: LoggingConfig = field(
        default_factory=lambda: LoggingConfig(log_to_wandb=False)
    )
    n_batches_for_norm_estimate: int = 1000

    @property
    def total_training_steps(self) -> int:
        return self.total_training_samples // self.train_batch_size_samples
