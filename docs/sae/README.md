# Sparse autoencoders

[Home](../../README.md) · [All method families](../methods/README.md)

SAE is a peer of Lens, Attention and Causal. It learns sparse feature directions
from frozen-model activations, then measures their activity and controlled
interventions. The same method interface works on native language, image and
multimodal residuals with explicit layer and token coordinates.

| Task | Guide |
| --- | --- |
| Choose an algorithm and understand the upstream union | [Methods and scope](methods/README.md) |
| Inspect parameters and outputs | [API reference](API.md) |
| Train on your model and data, validate and resume | [Training protocol](training/README.md) |
| Browse our model cards or convert source checkpoints | [Models and imports](models/README.md) |
| Run an actual input → frozen forward → training → probe → visualization workflow | [Complete examples](examples/README.md) |
| Inspect pinned sources and licensing | [Credits and provenance](SOURCES.md) |

```python
from vlmprobe.sae import SAETrainingConfig

method = probe.sae.topk(layer=0, tokens="visual", d_sae=1024, k=32)
method.fit(train_inputs, validation_inputs, output_dir="outputs/my_sae",
           train_ids=train_slide_ids, validation_ids=held_out_slide_ids,
           preprocessing_id="my-resize-and-normalization-v1",
           training=SAETrainingConfig(epochs=10, batch_size=256))
features = method.run(inputs)
profile = method.profile(top_k=5).run(inputs)
control = method.reconstruct().run(inputs, metric=score)
intervention = method.edit(feature_ids=[7], scale=0).run(inputs, metric=score)
method.save("outputs/my_dictionary")
loaded = probe.sae.load("outputs/my_dictionary")
```

The example above shows the contract; the [runnable tutorial](examples/README.md)
defines every input and plotting call. Source toolkits are credited as sources,
not selected as runtime backends. Training, inference, artifacts and feature
operations are implemented in this project. One-time converters accept supported
source tensor formats without importing official SAE packages.

## Interpretation and current scope

- Dictionary features are learned directions, not automatically named concepts.
- A feature overlay shows feature activity at native token positions. It does
  not establish attention, semantic grounding or causal relevance.
- Reconstruction is a separate intervention control. The default feature edit
  preserves the SAE reconstruction error: `x + decode(z_edited) - decode(z)`.
- The current collector caches finite train/validation activations in bounded
  CPU memory. It is not yet a distributed, streaming billion-token trainer.
- Published pretrained model cards require completed end-to-end validation.
  Your own training runs can save and register local cards with full provenance.
  Unverified models and resource lists are excluded from the distributed catalog.

## Changes from the earlier SAE preview

The v4 preview replaces provider-specific constructors and trainers with native
algorithm factories and a single training engine. Source-format names are only
used for one-time checkpoint import. The published model registry contains only
models that have completed end-to-end validation; this version does not bundle
pretrained model cards. Local fitted dictionaries can be saved, registered and
reloaded through the same interface.
