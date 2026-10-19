# Method Guides

[Home](../../README.md) / [Documentation](../README.md)

Each guide presents the API and parameter defaults first, followed by a complete
example: imports, model loading, input/prompt preparation, calibration or target
construction when needed, method execution, result inspection and visualization.
Examples can be copied without first running a hidden shared setup cell.
Availability depends on the model adapter;
check `probe.describe()` or the [model matrix](../models/README.md).

Residual and head lenses support language-model and VLM representations;
EmbedLens uses the input-embedding space; its visual-analysis mode needs projected
visual tokens, while `tokens="all"` also permits text-only inputs. Spatial attention maps
can analyze vision classifiers or decoder visual tokens when the adapter
exposes the required sites. Original EAP-IG currently uses a text-only GPT-2
graph. These modality boundaries are documented on each method page.

## Lens

| Method | Public factory | What it does |
| --- | --- | --- |
| [Logit Lens](logit_lens.md) | `probe.lens.logit(...)` | Decode intermediate residuals with the model's final normalization and vocabulary head. |
| [Tuned Lens](tuned_lens.md) | `probe.lens.tuned(...)` | Fit one affine translator per residual layer before applying the model's frozen readout. |
| [Attention Lens](attention_lens.md) | `probe.lens.attention(...)` | Train separate vocabulary decoders for individual attention heads. |
| [Jacobian Lens](jacobian_lens.md) | `probe.lens.jacobian(...)` | Estimate a layer-to-final-residual Jacobian, transport representations, and decode them. |
| [EmbedLens](embed_lens.md) | `probe.lens.embed(...)` | Find vocabulary embeddings nearest to projected visual tokens. |
| [Patchscope](patchscope.md) | `probe.lens.patchscope(...)` | Insert a source representation into a target prompt and inspect its output logits. |

## Attention

| Method | Public factory | What it does |
| --- | --- | --- |
| [Attention Profile](attention_profile.md) | `probe.attention.profile(...)` | Measure attention entropy, concentration, and mass assigned to token groups. |
| [Head Logit Attribution](head_logit_attribution.md) | `probe.attention.head_logits(...)` | Project head contributions to vocabulary logits with a fixed final normalization scale. |
| [Attention Rollout](attention_rollout.md) | `probe.attention.rollout(...)` | Compose normalized self-attention transitions across consecutive layers. |
| [Attention Relevance](attention_relevance.md) | `probe.attention.relevance(...)` | Propagate positive gradient-weighted self-attention for a selected output score. |
| [Attention Reweighting](attention_reweight.md) | `probe.attention.reweight(...)` | Rescale attention on selected key tokens and measure the output change. |
| [Attention Temperature](attention_temperature.md) | `probe.attention.temperature(...)` | Change the sharpness of attention at selected query rows. |
| [Attention Grad-CAM](attention_maps.md) | `probe.attention.grad_cam(...)` | Target-conditioned CAM using attention heads as channels. |
| [Self-Attention Attribution](attention_maps.md) | `probe.attention.attribution(...)` | Integrate gradients along a single layer's zero-to-original probability path. |
| [TAM](attention_maps.md) | `probe.attention.tam(...)` | Combine backward Markov transitions with input-path final-attention feedback. |
| [Beyond Intuition](attention_maps.md) | `probe.attention.beyond_intuition(...)` | Headwise or tokenwise perception with integrated reasoning feedback. |
| [Chefer DTD/LRP](chefer_lrp.md) | `probe.attention.dtd_lrp(...)` | Copy native ViT weights into the pinned author's actual relevance-propagation backend. |

Profile, head logit attribution, reweighting, and temperature are reusable
statistics/readout/intervention tools. They do not reproduce VAR, OPERA, or PAI.
The [source index](../REFERENCES.md) identifies the paper-backed attribution
algorithms and their implemented scope.

## Causal

| Method | Public factory | What it does |
| --- | --- | --- |
| [Activation Patching](activation_patching.md) | `probe.causal.patch(...)` | Replace selected receiver residuals with source residuals and measure the causal effect. |
| [Path Patching](path_patching.md) | `probe.causal.path(...)` | Freeze other head outputs, transfer sender outputs, then replay only recomputed receiver Q/K/V or final residual. |
| [Attribution Patching](attribution_patching.md) | `probe.causal.attribute(...)` | Approximate a patch effect using activation differences and a receiver-side gradient. |
| [Attention Knockout](attention_knockout.md) | `probe.causal.knockout(...)` | Block selected query-to-key attention paths before softmax. |
| [EAP / EAP-IG](eap_ig.md) | `probe.causal.eap_ig(graph="transformer", ...)` | Attribute independently replaceable GPT-2 edges along an input-embedding path, then evaluate retained circuits with actual forwards. |
| [Residual Steering](steering.md) | `probe.causal.steer(...)` | Add a supplied direction to selected residuals and measure the output change. |
| [Visual Steering Vector (VSV)](steering.md#per-image-visual-steering-vsv) | `probe.causal.vsv(positive, negative, ...)` | Build per-image residual directions from image and text-only inputs; configure a joint steering run. |

## Running the examples

Install `python -m pip install "vlmprobe[transformers,visualization]"` for the
pretrained examples. For notebooks, clone the repository and install
`python -m pip install -e ".[transformers,visualization,notebooks]"`.
Model downloads and compute requirements are stated on each page. Example
calibrations teach the workflow; they are not validated research checkpoints.

The [notebooks](../../demos/README.md) walk through raw input preparation and
compute results before plotting them. The [model guides](../models/README.md#use-any-supported-method)
explain how to switch the loading and input block while retaining the common
method API. The optional [TinyModel example](../../examples/prober_quickstart.py)
is an architecture/API smoke test with synthetic IDs, not a pretrained semantic
demonstration or a prerequisite for these method pages.

## Shared conventions

`layers=None` selects available method sites; indices are zero-based. Tokens may
be `"all"`, `"visual"`, `"text"`, `"last_prompt"`, a position/list, or a boolean
`[B,T]` mask. Positions refer to the expanded language sequence. `"last_prompt"`
means the last valid token unless an explicit prompt mask is supplied.

In output shapes, `L` is the number of selected layers, `B` batch size, `T/Q`
sequence/query length, `H` heads, `V` vocabulary size, and `N` packed selected
positions. Lens `positions[N,2]` maps packed rows to batch/token coordinates.
Layer metadata preserves the chosen order. Results default to detached CPU tensors;
`result.save(directory)` writes tensors and JSON metadata.

See [the full API](../API.md), [custom adapters](../ADAPTERS.md), and the
[paper index](../REFERENCES.md) for shared contracts and sources.
