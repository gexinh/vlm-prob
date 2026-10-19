# Tuned Lens

[Home](../../README.md) / [Methods](README.md) / Tuned Lens

Learn a separate affine translator at each residual layer while leaving the supplied model frozen.

## API and parameters

`probe` is a `Prober` bound to a loaded model; `inputs` contains prepared model inputs. The blocks below are API signatures: `*` marks keyword-only parameters, not an argument to copy. The [complete example](#complete-live-example) defines the model, inputs, and all other variables before running the method.

```text
method = probe.lens.tuned(*, layers=None, tokens="last_prompt", binding=None)
method.fit(inputs, *, steps=100, lr=1e-3)
result = method.run(inputs)
```

| Parameter | Default | Meaning and constraints |
| --- | --- | --- |
| `layers` | `None` | Residual layers to calibrate separately; storage scales roughly as `L × D²`. |
| `tokens` | `"last_prompt"` | The same selector is used for calibration and evaluation. |
| `binding` | `None` | Checkpoint/tokenizer/readout/data identities required for dataset training and artifact persistence. |
| `inputs` | Required | Calibration input for `fit`, independent showcase input for `run`. |
| `steps` | `100` | Positive Adam steps for one-batch `fit` only. |
| `lr` | `1e-3` | Positive learning rate for one-batch `fit`. |

The translator is `h + A_layer @ h + b_layer`, initialized to identity, followed
by the frozen model readout. Calibration minimizes `KL(model || lens)` at the
same prediction positions, with no next-token label shift. Returns
`logits[L,N,V]` and `positions[N,2]`. `method.losses[layer]` describes one-batch
`fit`; use `training_history` for dataset training.

### Dataset training and artifacts

```text
method.fit_batches(train_inputs, validation_inputs, directory,
                   batch_size=64, epochs=10, lr=1e-3, patience=3, min_delta=1e-4,
                   seed=0, resume=True, provenance=None, progress_every=16)
method.save(directory)
method.load(directory)
```

| Parameter | Default | Meaning and constraints |
| --- | --- | --- |
| `train_inputs` | Required | Re-iterable prepared training examples; selected activations/teacher logits are captured once into CPU RAM. |
| `validation_inputs` | Required | Independent examples; split by document/image before tokenization. The library does not deduplicate your dataset. |
| `directory` | Required | Writable artifact/checkpoint directory. Use a fresh directory to start a different experiment. |
| `batch_size` | `64` | Positive number of **selected positions** per decoder minibatch, not input images/prompts. |
| `epochs` | `10` | Positive maximum epochs. |
| `lr` | `1e-3` | Positive Adam learning rate. |
| `patience` | `3` | Positive epochs without sufficient validation improvement before stopping. |
| `min_delta` | `1e-4` | Nonnegative minimum KL improvement; the initial decoder is also a best-checkpoint candidate. |
| `seed` | `0` | Shuffle/training RNG seed. |
| `resume` | `True` | Restore optimizer/RNG/history when matching state exists; identities, data order and configuration must match. |
| `provenance` | `None` | Optional JSON-compatible experiment metadata checked on resume. |
| `progress_every` | `16` | Positive interval (at least `1`) for saving minibatch progress status; epoch summaries are also printed. |

The simpler `fit(inputs, steps=100, lr=1e-3)` repeatedly optimizes one batch.
`steps` must be positive; it restarts Adam on every call, whereas `fit_batches`
keeps Adam across minibatches and validates each epoch. Model parameters are not
updated. Neither fitting entry point may run under `torch.inference_mode()`.

`binding` is a caller-declared dictionary with nonempty string `model_id`,
`tokenizer_id`, `readout_id` and `calibration_id`; the adapter adds the capture
`site`. Loading checks these identities and dimensions. Save/load requires
explicit identities; use pinned revisions and dataset-manifest hashes for real
experiments. Bindings are not an automatic hash of checkpoint contents.
`training_history[layer]` includes initial/epoch validation KL, top-1 agreement,
best epoch and `best_validation_kl`. See [training protocol](../TRAINING.md) for
disk-backed caches, author weights and larger datasets.

## Input and coordinate conventions

`inputs` is a native model-input dictionary or `ProbeInputs` from `probe.prepare(...)`.
All examples below are complete scripts; they do not depend on variables from a
model guide. Install `pip install "vlmprobe[transformers,visualization]"` first.
`VLM_PROBING_MODEL` may select a compatible local checkpoint; public defaults use
Hugging Face model IDs. For a VLM, replace only model/processor loading and input
preparation with its [model guide](../models/README.md); the method call and result
contract remain the same wherever `probe.describe()` reports support.

Layer indices are zero-based blocks, measured **after** each block. `None` selects
all available layers; an integer or nonempty list of unique available integers
selects a subset. Shared `tokens` selectors are `"last_prompt"`, `"all"`, `"visual"`,
`"text"`, `"prediction"`, a single expanded position, a sequence of positions, or a boolean
`[batch, expanded_sequence]` mask. `"prediction"` selects the final prompt position and subsequent teacher-forced/generated positions when an explicit prompt mask is supplied. String selectors exclude padding; explicit positions/masks must not select padding. Packed outputs carry
`positions[N,2] = [batch index, expanded token index]`; `N` is not the original
unpadded text length when images add tokens.

## Complete live example

This example trains fresh decoders on independent strings. It downloads GPT-2 if not cached; increase the corpus before treating it as an analysis artifact.

```python
import hashlib
import json
import os
from pathlib import Path

import matplotlib.pyplot as plt
import torch
from transformers import AutoTokenizer, GPT2LMHeadModel
from vlmprobe import Prober
from vlmprobe.visualization import plot_lens_heatmap

# A pretrained text model, not a random architecture or cached probe result.
MODEL_ID = os.environ.get("VLM_PROBING_MODEL", "openai-community/gpt2")
DEVICE = os.environ.get("VLM_PROBING_DEVICE", "cuda:0" if torch.cuda.is_available() else "cpu")
OUT = Path(os.environ.get("VLM_PROBING_OUTPUT", "outputs/lens_tutorial"))
OUT.mkdir(parents=True, exist_ok=True)
torch.manual_seed(0)
model = GPT2LMHeadModel.from_pretrained(MODEL_ID, attn_implementation="eager").to(DEVICE).eval()
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
probe = Prober(model, tokenizer)
print(probe.describe())

def prepare(text):
    return probe.prepare(prompt=text, device=DEVICE)

prompt = "When Amy and Laura got a snack at the house, Laura decided to give it to"
inputs = prepare(prompt)
answer_ids = tokenizer.encode(" Amy", add_special_tokens=False)
assert len(answer_ids) == 1, "Choose a single target subword for this rank plot."
answer_id = answer_ids[0]
# Disjoint strings illustrate the protocol; this tiny split is not a quality benchmark.
train_texts = [
    "The child opened a book and began to read.",
    "A red boat crossed the lake before sunset.",
    "The baker placed fresh bread beside the window.",
    "Two friends walked through a quiet garden.",
]
validation_texts = [
    "A musician carried a violin onto the stage.",
    "The train arrived at the station after midnight.",
]
assert not (set(train_texts) & set(validation_texts))
assert prompt not in train_texts + validation_texts
train_inputs = [prepare(text) for text in train_texts]
validation_inputs = [prepare(text) for text in validation_texts]
split_hash = hashlib.sha256(json.dumps([train_texts, validation_texts]).encode()).hexdigest()
binding = {
    "model_id": MODEL_ID + "@" + str(getattr(model.config, "_commit_hash", None) or "local-checkpoint"),
    "tokenizer_id": tokenizer.name_or_path,
    "readout_id": "transformer.ln_f+lm_head",
    "calibration_id": "tutorial-distinct-texts-sha256:" + split_hash,
}
# For a release, pin the model/tokenizer revision and hash the local checkpoint
# if config._commit_hash is unavailable. This binding is caller-declared identity.
layers = [0, model.config.n_layer // 2, model.config.n_layer - 1]
lens = probe.lens.tuned(layers=layers, tokens="text", binding=binding)
lens.fit_batches(train_inputs, validation_inputs, OUT / "tuned-artifact",
                 batch_size=16, epochs=2, lr=1e-3, patience=2, seed=0,
                 resume=False)
for layer, history in lens.training_history.items():
    print(layer, "best held-out KL:", history["best_validation_kl"])
result = lens.run(inputs)
print("logits:", result.tensors["logits"].shape)
ax = plot_lens_heatmap(result, target_token_id=answer_id, tokenizer=tokenizer,
                       title="Tuned Lens: two-epoch protocol demonstration")
ax.figure.savefig(OUT / "tuned.png", dpi=160, bbox_inches="tight")
plt.show()
# Artifact restoration uses the same checkpoint/tokenizer/calibration identities.
restored = probe.lens.tuned(layers=layers, tokens="text", binding=binding).load(OUT / "tuned-artifact")
```

Run the same code as a script: [lens_tuned.py](../../examples/tutorials/lens_tuned.py).

## Output and visualization

Compare held-out KL before/after fitting, then inspect the independent IOI prompt. A lower teacher KL means closer agreement with the frozen model, not higher factual accuracy. Two epochs on four strings are an engineering demonstration, not a calibrated scientific comparison.

![Actual pretrained GPT-2 tutorial output](../assets/tutorials/lens-tuned.png)

The preview is generated by the live tutorial, not a loaded measurement snapshot.
[Checkpoint hashes, data split and run provenance](../assets/tutorials/lens-provenance.json).
[Source/reference](../REFERENCES.md#lens-methods) · [Training and artifact protocol](../TRAINING.md).
