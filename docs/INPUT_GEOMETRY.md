# Visual token geometry and preprocessing

`visual_grid` reports the native processed-image grid and its exact expanded
token positions. `preprocessing_report` inspects resolution, preprocessing
configuration and, for supported processors, geometric bbox retention. Neither
tool changes inputs, overrides processor defaults or runs the model.

## API

```python
geometry = visual_grid(probe, inputs)
report = preprocessing_report(
    probe, inputs, image=None, bbox_xywh=None,
    explicit_padding=None, processor_kwargs=None,
)
```

| Argument | Meaning |
| --- | --- |
| `probe` | A `Prober` bound to the model and, for preprocessing diagnostics, its processor. |
| `inputs` | The native processor dictionary or `ProbeInputs` used for the forward. |
| `image` | One original PIL image, before any caller-applied padding. Optional for a size/configuration report; required for replay and bbox geometry. |
| `bbox_xywh` | Optional source-image box `(x, y, width, height)` in pixels. Bounds must lie inside the image. |
| `explicit_padding` | Optional caller-applied padding with `left`, `top`, `right`, `bottom` and RGB `fill`. It is recorded separately from processor cropping. |
| `processor_kwargs` | The exact image-processor overrides used to construct `pixel_values`, such as `{"do_center_crop": False}`. No overrides are inferred. |

Grid entries contain `grid_shape=[rows, columns]` and ordered
`positions=[[batch, expanded_token], ...]`. They describe processed images or
tiles, **not uncropped original-image coordinates**. Never infer a square grid
by taking the square root of the visual token count.

| Native input family | Geometry returned |
| --- | --- |
| ViT classification | Fixed patch grid, excluding CLS; positional interpolation is unsupported. |
| LLaVA | Fixed patch-only images, using actual pixel dimensions and the configured patch size. Packed `image_sizes` and `full`/CLS selection need an explicit mapping. |
| Qwen2-VL, Qwen2.5-VL, Qwen3-VL, Qwen3.5 | Per-image merged grids from `image_grid_thw` and `vision_config.spatial_merge_size`; packed pixel counts and expanded visual positions must agree. Still images only. |
| InternVL | Per-tile grids after native v2 pixel shuffle. Tile grouping, original-image placement and thumbnail identity are unavailable; these grids must not be combined into an original-image overlay. |
| Idefics3 and other layouts | `CapabilityError` with guidance to provide explicit native geometry. Tiling, pixel shuffle and padding are not guessed. |

The tools validate declared layout/count contracts; they do not establish that
the supplied model inputs can successfully complete a forward pass.

## Complete CPU example

This example needs `vlmprobe[transformers]`, Pillow and no downloaded weights.
It constructs a small native ViT, preprocesses an image, checks its grid and
prints bbox diagnostics. In a real application, retain the original image and
the exact processor overrides alongside the processor outputs.

```python
import json
from PIL import Image, ImageDraw
from transformers import ViTConfig, ViTForImageClassification, ViTImageProcessor
from vlmprobe import Prober, preprocessing_report, visual_grid

image = Image.new("RGB", (96, 48), "white")
ImageDraw.Draw(image).rectangle((60, 12, 83, 35), fill="red")
model = ViTForImageClassification(ViTConfig(
    image_size=32, patch_size=8, hidden_size=16,
    num_hidden_layers=1, num_attention_heads=2, intermediate_size=32,
    num_labels=2, attn_implementation="eager",
)).eval()
processor = ViTImageProcessor(size={"height": 32, "width": 32})
probe = Prober(model, processor)
inputs = processor(images=image, return_tensors="pt")

geometry = visual_grid(probe, inputs)
print(geometry["grids"][0]["grid_shape"])       # [4, 4]
print(geometry["grids"][0]["positions"][0])    # [0, 1]: CLS is excluded
report = preprocessing_report(
    probe, inputs, image=image, bbox_xywh=(60, 12, 24, 24),
)
print(json.dumps(report, indent=2))
```

`processed_size` and `source_size` use `[width, height]`; `grid_shape` uses
`[rows, columns]`. This avoids silently swapping image and matrix conventions.

## Reading preprocessing diagnostics

Every report separates declared processor settings from effective source
geometry. Exact resize/crop geometry currently supports the native **slow**
`CLIPImageProcessor` and `ViTImageProcessor`. The helper replays the original
image, caller-declared padding and supplied overrides through that processor,
then requires equality with the supplied pixels (after matching their dtype).
The replay does not call the text tokenizer or modify the supplied tensors.

When this check passes, `geometry_status` is
`"supported_processor_replay_matches"`, `operations` contains the resize/crop
trace, and an optional bbox has its projected extent and retained-area
fraction. This is a configuration-based geometric diagnostic with a pixel
replay check, not an execution trace captured during the original call.

For other processors, multiple images, tiles, unknown overrides or replay
mismatches, geometry remains `"unavailable"` and `bbox=None`. A reported tensor
shape or declared center-crop setting alone does not establish original-image
coordinates. Fast processors may round differently and are not substituted for
the audited slow processors.

A retained-area fraction of zero means the geometric box lies outside the
reported crop. A fraction of one can still correspond to a very small processed
extent. Neither value determines whether a concept remains recognizable:
interpolation can remove pure-color pixels while retaining weaker visual
information. Without a bbox or other annotation, the tool cannot determine
whether the subject survived preprocessing.

The fixed LLaVA notebooks explicitly pad images to a square before calling the
HF processor. This is a demo recipe, not the default behavior of
`Prober.prepare`. To describe it, supply the actual padding offsets and fill:

```python
padding = {
    "left": 0, "top": 24, "right": 0, "bottom": 24,
    "fill": (122, 116, 104),
}
padded = Image.new("RGB", (96, 96), padding["fill"])
padded.paste(image, (padding["left"], padding["top"]))
padded_inputs = processor(images=padded, return_tensors="pt")
report = preprocessing_report(
    probe, padded_inputs, image=image, bbox_xywh=(60, 12, 24, 24),
    explicit_padding=padding,
)
```

The supplied `inputs` must actually have been generated from that padded image;
otherwise the replay check leaves source geometry unavailable.
