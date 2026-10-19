# Selected SAELens core maintained inside VLMProbe

Source: https://github.com/decoderesearch/SAELens
Pinned commit: `30c4502466785dd7809a307f7b705df187978aa3`
Upstream version: `6.54.6`; local revision: `1`.
License: MIT; original copyright notice is retained in `LICENSE`.

This directory is a selected source copy, not a wrapper around an installed
`sae_lens` distribution. Its code is maintained and shipped by VLMProbe.
`PROVENANCE.json` records source paths, upstream SHA256 values, local SHA256
values, and changes. Checkpoint/model licenses remain publisher-specific.

Included:

- Standard/ReLU, Gated, TopK, JumpReLU, AbsTopK and Matching Pursuit inference.
- Those six training architectures plus BatchTopK and Matryoshka BatchTopK.
- Original architecture-specific losses, optimizer/schedule, activation scaling
  and whitening, safetensors serialization, native training-state persistence.
- Complete pinned pretrained registry and selected native/Gemma/Llama/Goodfire/
  dictionary-learning/DeepSeek/Qwen/sparsify checkpoint converters.

Local integration changes:

- Imports point to this package. Generic utility dependencies remain external;
  official SAELens, TransformerLens and transformers are not dependencies.
- TransformerLens hook containers are replaced with small local PyTorch identity
  points plus module-name registration. Ordinary PyTorch forward hooks remain
  available; TransformerLens model/cache/context APIs are not implemented.
- Language-model runners, datasets and CLI helpers are omitted. Activation-vector
  sources come from VLMProbe or the caller's frozen model/data pipeline.
- Remote WandB logging and its callback path are omitted and rejected explicitly.
  Local statistics, protocol artifacts and independent held-out evaluation remain.
- Transcoder and temporal converters are omitted because their multi-hook/context
  contracts are outside the current same-space SAE probing API.
- The identical registry YAML is losslessly gzip-compressed. Tensor-only PyTorch
  checkpoint loads explicitly request `weights_only=True`.

No architecture's selected encode/decode, sparsity penalty, auxiliary loss,
threshold update, whitening or optimizer equation was replaced by a simplified
reimplementation. Optional pinned-upstream differential tests cover exact
inference outputs/gradients for six architectures and training outputs/losses/
gradients for all eight. Ordinary tests execute this copy without official
packages installed and with their imports actively blocked.
