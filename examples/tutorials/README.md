# Runnable method tutorials

These scripts contain the same complete workflows shown in the
[method guides](../../docs/methods/README.md): load a model, prepare raw inputs,
configure a probe, compute results, inspect tensors and draw built-in plots.
They do not load archived probe measurements.

From the repository root:

```bash
python -m pip install -e ".[transformers,visualization]"
python examples/tutorials/lens_logit.py
```

| Family | Scripts |
| --- | --- |
| Lens | [Logit](lens_logit.py), [Tuned](lens_tuned.py), [Attention Lens](lens_attention.py), [Jacobian](lens_jacobian.py), [EmbedLens](lens_embed.py), [Patchscope](lens_patchscope.py) |
| Attention | [Profile](attention_profile.py), [Rollout](attention_rollout.py), [Relevance](attention_relevance.py), [Grad-CAM / ATTATTR / TAM / Beyond Intuition](attention_image_methods.py), [DTD/LRP](attention_chefer.py), [Head logit contributions](attention_head_logits.py), [Reweighting](attention_reweight.py), [Temperature](attention_temperature.py) |
| Causal | [Activation / attribution patching](causal_activation_patching.py), [Path patching](causal_path_patching.py), [EAP / EAP-IG](causal_eap_ig.py), [Attention knockout](causal_attention_knockout.py), [Steering / VSV](causal_steering_vsv.py) |

`VLM_PROBING_DEVICE` selects a device and `VLM_PROBING_OUTPUT` selects an output
directory. `VLM_PROBING_MODEL` optionally supplies a compatible local checkpoint;
otherwise each script uses its stated public model. Keep overrides within the
script's supported model family. Image examples expose their input URL/path and
prompt directly; some also accept `VLM_PROBING_IMAGE`.

GPT-2 is the text default, SmolVLM-500M the VLM default, and Google ViT-B/16 the
vision-classifier default. First use downloads weights. Dense Attention Lens
fitting can use several gigabytes of memory and checkpoints even for GPT-2;
exact Jacobians and integrated attribution require repeated backwards/forwards.
Read the method's cost and calibration notes before starting those scripts.

For a guided sequence and inline outputs, use the
[live notebooks](../../demos/README.md). Raw sample provenance and image rights
are documented there. Short training splits demonstrate the protocol; use
independent representative data before interpreting a fitted decoder.
