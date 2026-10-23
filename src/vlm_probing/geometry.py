"""Read-only, model-specific input geometry; no grids are guessed from token counts."""
from collections.abc import Mapping
from copy import deepcopy
from numbers import Integral

import torch

from .adapters import CapabilityError, TokenLayout
from .api.common import unpack


def _pair(value, name):
    try:
        values = (value, value) if isinstance(value, Integral) else tuple(value)
    except TypeError as error:
        raise CapabilityError(f"{name} must declare positive height and width") from error
    if len(values) != 2 or any(not isinstance(n, Integral) or n <= 0 for n in values):
        raise CapabilityError(f"{name} must declare positive height and width")
    return tuple(int(n) for n in values)


def _layout(probe, values, explicit):
    provider = probe.spec.layout
    layout = explicit if explicit is not None else provider(values) if provider else None
    if not isinstance(layout, TokenLayout):
        raise CapabilityError("visual_grid requires an adapter layout or explicit ProbeInputs.layout")
    layout = layout.checked(layout.valid.shape, layout.valid.device)
    if layout.visual is None or not layout.visual.any():
        raise CapabilityError("visual_grid requires nonempty declared visual token positions")
    return layout


def _chunks(positions, counts):
    if sum(counts) != len(positions):
        raise CapabilityError(
            f"native geometry describes {sum(counts)} visual tokens but layout selects {len(positions)}; "
            "check expanded image placeholders, merger settings and native processor metadata"
        )
    result, offset = [], 0
    for count in counts:
        chunk = positions[offset:offset + count]
        if any(p[0] != chunk[0][0] or p[1] != chunk[0][1] + i for i, p in enumerate(chunk)):
            raise CapabilityError("each native image/tile grid must occupy consecutive visual positions in one sequence")
        result.append(chunk)
        offset += count
    return result


def visual_grid(probe, inputs):
    """Return verified processed-image grids and ordered ``[batch, token]`` positions.

    Supported: native fixed-grid ViT/LLaVA and Qwen VL image patch mergers.
    InternVL exposes tile-local grids, without inferring original-image placement.
    Videos, Idefics3 tiled/padded layouts and unknown architectures raise
    :class:`CapabilityError`. This function runs neither the model nor processor.
    ``grid_shape`` is ``[rows, columns]``; each position list is row-major.
    No returned grid promises a mapping back to an uncropped original image.
    """
    values, explicit = unpack(inputs)
    config = getattr(probe.model, "config", None)
    family = getattr(config, "model_type", "unknown")
    supported = {"vit", "llava", "internvl", "qwen2_vl", "qwen2_5_vl", "qwen3_vl", "qwen3_5"}
    if family not in supported:
        raise CapabilityError(
            f"visual_grid has no audited geometry contract for {family!r}; supply an explicit "
            "native grid and token mapping to visualization. Idefics3 padded/tiled layouts are not inferred."
        )
    if values.get("video_grid_thw") is not None or values.get("pixel_values_videos") is not None:
        raise CapabilityError("visual_grid currently supports still images only, not video grids")
    layout = _layout(probe, values, explicit)
    positions = layout.visual.nonzero().detach().cpu().tolist()
    pixels = values.get("pixel_values")
    if family == "vit":
        if not isinstance(pixels, torch.Tensor) or pixels.ndim != 4:
            raise CapabilityError("ViT geometry requires pixel_values[B,C,H,W]")
        patch = _pair(config.patch_size, "config.patch_size")
        height, width = map(int, pixels.shape[-2:])
        if values.get("interpolate_pos_encoding", False) or (height, width) != _pair(config.image_size, "config.image_size"):
            raise CapabilityError("native fixed-grid ViT geometry requires config.image_size without positional interpolation")
        if height % patch[0] or width % patch[1]:
            raise CapabilityError("processed image dimensions must be divisible by the native patch size")
        rows, columns = height // patch[0], width // patch[1]
        shapes = [(rows, columns)] * int(pixels.shape[0])
        expected = torch.zeros_like(layout.valid)
        if expected.shape != (pixels.shape[0], rows * columns + 1):
            raise CapabilityError("native ViT requires one CLS token followed by the complete patch grid")
        expected[:, 1:] = True
        if not torch.equal(layout.visual, expected) or not layout.valid.all():
            raise CapabilityError("declared ViT layout disagrees with native CLS/patch order")
    else:
        ids = values.get("input_ids")
        if not isinstance(ids, torch.Tensor) or ids.ndim != 2 or ids.shape != layout.valid.shape:
            raise CapabilityError("native VLM geometry requires input_ids aligned with the expanded layout")
        field = "image_token_index" if family == "llava" else "image_token_id"
        native_visual = (ids.to(layout.valid.device) == getattr(config, field)) & layout.valid
        if not torch.equal(native_visual, layout.visual):
            raise CapabilityError("declared visual layout disagrees with native image-token IDs")
        if family.startswith("qwen"):
            grid = values.get("image_grid_thw")
            if not isinstance(grid, torch.Tensor) or grid.ndim != 2 or grid.shape[1] != 3:
                raise CapabilityError("Qwen image geometry requires native image_grid_thw[num_images,3]")
            if grid.dtype not in (torch.int32, torch.int64) or not (grid > 0).all():
                raise CapabilityError("image_grid_thw must contain positive integer temporal/height/width counts")
            merge = getattr(config.vision_config, "spatial_merge_size", None)
            if not isinstance(merge, Integral) or merge <= 0:
                raise CapabilityError("Qwen geometry requires vision_config.spatial_merge_size")
            raw = grid.detach().cpu().tolist()
            if any(t != 1 or h % merge or w % merge for t, h, w in raw):
                raise CapabilityError("still-image grids require temporal count 1 and dimensions divisible by spatial_merge_size")
            if isinstance(pixels, torch.Tensor) and (pixels.ndim != 2 or len(pixels) != sum(t*h*w for t, h, w in raw)):
                raise CapabilityError("packed Qwen pixel_values patch count disagrees with image_grid_thw")
            shapes = [(h // merge, w // merge) for _, h, w in raw]
        else:
            if not isinstance(pixels, torch.Tensor) or pixels.ndim != 4:
                raise CapabilityError(f"{family} geometry requires pixel_values[num_images_or_tiles,C,H,W]")
            strategy = values.get("vision_feature_select_strategy", getattr(config, "vision_feature_select_strategy", "default"))
            if strategy != "default":
                raise CapabilityError("visual_grid supports default patch-only vision selection; CLS/full selection requires an explicit mapping")
            if family == "llava" and values.get("image_sizes") is not None:
                raise CapabilityError("LLaVA packed image_sizes layouts require an explicit mapping; this helper covers fixed single-grid images")
            patch = _pair(config.vision_config.patch_size, "vision_config.patch_size")
            height, width = map(int, pixels.shape[-2:])
            if height % patch[0] or width % patch[1]:
                raise CapabilityError("processed image/tile dimensions must be divisible by native patch size")
            rows, columns = height // patch[0], width // patch[1]
            if family == "internvl":
                if getattr(config, "ps_version", "v2") != "v2":
                    raise CapabilityError("InternVL geometry supports native v2 pixel-shuffle order only; v1 requires an explicit axis mapping")
                ratio = getattr(config, "downsample_ratio", None)
                if ratio is None or not 0 < ratio <= 1:
                    raise CapabilityError("InternVL geometry requires a valid config.downsample_ratio")
                reduced = (rows * ratio, columns * ratio)
                if rows != columns or any(n != int(n) for n in reduced):
                    raise CapabilityError("native InternVL pixel shuffle requires a square, exactly divisible patch grid")
                rows, columns = map(int, reduced)
            shapes = [(rows, columns)] * int(pixels.shape[0])
    chunks = _chunks(positions, [h*w for h, w in shapes])
    grids = []
    for i, ((rows, columns), chunk) in enumerate(zip(shapes, chunks)):
        grids.append({"batch_index": chunk[0][0], "image_index": None if family == "internvl" else i,
                      "tile_index": i if family == "internvl" else 0,
                      "grid_shape": [rows, columns], "positions": chunk})
    return {"family": family, "coordinate_space": "processed_tile" if family == "internvl" else "processed_image",
            "order": "row-major", "grids": grids, "visual_token_count": len(positions),
            "source_mapping": None,
            "notes": ["Original-image crop/pad coordinates are not inferred."] +
                     (["InternVL tile order follows native pixel_values; image grouping, tile placement and thumbnail identity are unavailable."]
                      if family == "internvl" else [])}


def _image_size(image):
    size = getattr(image, "size", None)
    if not isinstance(size, tuple) or len(size) != 2 or any(not isinstance(n, Integral) or n <= 0 for n in size):
        raise TypeError("image must be one PIL image with positive width and height")
    return [int(n) for n in size]


def _simple_trace(processor, size, overrides):
    """Exact slow HF CLIP/ViT resize and crop rounding, with no tensor guessing."""
    identity = (type(processor).__module__, type(processor).__name__)
    allowed = {("transformers.models.clip.image_processing_clip", "CLIPImageProcessor"),
               ("transformers.models.vit.image_processing_vit", "ViTImageProcessor")}
    if identity not in allowed:
        return None
    if overrides.get("data_format", "channels_first") != "channels_first":
        return None
    # Native slow processors infer channel order from array dimensions. A PIL
    # RGB image with height 1 or 3 can be misread as channels-first unless the
    # original caller explicitly supplied channels_last. Do not invent geometry.
    channel_order = overrides.get("input_data_format")
    if channel_order not in (None, "channels_last") or (size[1] in (1, 3) and channel_order is None):
        return None
    def option(key, default=None):
        return overrides.get(key, getattr(processor, key, default))
    width, height = size
    trace = []
    if option("do_resize", False):
        target = option("size")
        if not isinstance(target, Mapping):
            return None
        if "height" in target and "width" in target:
            new_width, new_height = int(target["width"]), int(target["height"])
        elif "shortest_edge" in target and identity[1] == "CLIPImageProcessor":
            edge = int(target["shortest_edge"])
            if width <= height:
                new_width, new_height = edge, int(edge * height / width)
            else:
                new_width, new_height = int(edge * width / height), edge
        else:
            return None
        trace.append({"operation": "resize", "input_size": [width, height], "output_size": [new_width, new_height]})
        width, height = new_width, new_height
    if option("do_center_crop", False):
        crop = option("crop_size")
        if not isinstance(crop, Mapping) or not {"height", "width"} <= crop.keys():
            return None
        crop_width, crop_height = int(crop["width"]), int(crop["height"])
        # HF slow center_crop pads with ceil(remaining / 2) for an undersized axis.
        pad_left = (max(0, crop_width - width) + 1) // 2
        pad_top = (max(0, crop_height - height) + 1) // 2
        left, top = (width - crop_width) // 2, (height - crop_height) // 2
        shift_x = pad_left - max(0, left + pad_left)
        shift_y = pad_top - max(0, top + pad_top)
        trace.append({"operation": "center_crop", "input_size": [width, height],
                      "output_size": [crop_width, crop_height], "shift_xy": [shift_x, shift_y]})
        width, height = crop_width, crop_height
    return trace, [width, height]


def preprocessing_report(probe, inputs, *, image=None, bbox_xywh=None,
                         explicit_padding=None, processor_kwargs=None):
    """Inspect inputs without modifying model kwargs, preprocessing or global state.

    ``image`` is the original single PIL image. ``explicit_padding`` optionally
    records caller-applied ``left, top, right, bottom, fill`` (PIL RGB fill).
    Exact bbox geometry is limited to audited slow HF CLIP/ViT processors and
    requires replay matching supplied pixels. Pass the original image-processor
    call overrides in ``processor_kwargs``; unknown paths remain unavailable.
    Geometric retention does not measure information or semantic object presence.
    """
    values, _ = unpack(inputs)
    processor = getattr(probe, "processor", None)
    processor = getattr(processor, "image_processor", processor)
    pixels = values.get("pixel_values")
    report = {"source_size": _image_size(image) if image is not None else None,
              "pixel_values_shape": list(pixels.shape) if isinstance(pixels, torch.Tensor) else None,
              "processed_size": list(reversed(pixels.shape[-2:])) if isinstance(pixels, torch.Tensor) and pixels.ndim in (4, 5) else None,
              "processor": type(processor).__name__ if processor is not None else None,
              "declared_processor_settings": {}, "explicit_padding": deepcopy(explicit_padding),
              "geometry_status": "unavailable", "operations": None, "bbox": None,
              "notes": ["Sizes are width,height; grid dimensions use rows,columns.",
                        "Processor settings describe configuration; source geometry is unavailable unless a supported replay matches pixels.",
                        "Geometric bbox retention does not establish semantic object presence or preserved visual information."]}
    for name in ("do_resize", "size", "do_center_crop", "crop_size", "do_pad", "patch_size", "merge_size", "do_image_splitting"):
        value = getattr(processor, name, None)
        if isinstance(value, (str, int, float, bool, dict, list, tuple)):
            report["declared_processor_settings"][name] = deepcopy(value)
    overrides = dict(processor_kwargs or {})
    if image is None or processor is None or not isinstance(pixels, torch.Tensor) or pixels.ndim != 4 or len(pixels) != 1:
        return report
    prepared = image
    operations = []
    if explicit_padding is not None:
        if not isinstance(explicit_padding, Mapping) or not {"left", "top", "right", "bottom", "fill"} <= explicit_padding.keys():
            raise ValueError("explicit_padding requires left, top, right, bottom and fill")
        pad = [explicit_padding[k] for k in ("left", "top", "right", "bottom")]
        if any(not isinstance(n, Integral) or n < 0 for n in pad):
            raise ValueError("explicit padding sizes must be nonnegative integers")
        from PIL import Image
        left, top, right, bottom = map(int, pad)
        prepared = Image.new("RGB", (image.width + left + right, image.height + top + bottom), explicit_padding["fill"])
        prepared.paste(image.convert("RGB"), (left, top))
        operations.append({"operation": "caller_padding", "input_size": list(image.size),
                           "output_size": list(prepared.size), "shift_xy": [left, top]})
    traced = _simple_trace(processor, list(prepared.size), overrides)
    if traced is None:
        report["notes"].append("Exact replay geometry requires a native slow CLIP/ViT processor and unambiguous channels-last PIL image handling.")
        return report
    trace, endpoint = traced
    replay = processor(images=prepared, **{**overrides, "return_tensors": "pt"})["pixel_values"]
    if replay.shape != pixels.shape or not torch.equal(replay.to(device=pixels.device, dtype=pixels.dtype), pixels):
        report["notes"].append("Processor replay does not match supplied pixels; pass exact image preprocessing overrides/padding, not inferred geometry.")
        return report
    if endpoint != report["processed_size"]:
        report["notes"].append("Computed resize/crop endpoint disagrees with native output; no source mapping is returned.")
        return report
    operations.extend(trace)
    report.update(geometry_status="supported_processor_replay_matches", operations=operations)
    if bbox_xywh is not None:
        if len(bbox_xywh) != 4:
            raise ValueError("bbox_xywh must contain x,y,width,height in source pixels")
        x, y, width, height = map(float, bbox_xywh)
        if not all(torch.isfinite(torch.tensor(n)).item() for n in (x, y, width, height)) or not (width > 0 and height > 0 and x >= 0 and y >= 0 and x+width <= image.width and y+height <= image.height):
            raise ValueError("bbox_xywh must be finite, nonempty and within the original image")
        box = [x, y, x+width, y+height]
        retained = 1.0
        for op in operations:
            if op["operation"] == "resize":
                sx, sy = (op["output_size"][i] / op["input_size"][i] for i in (0, 1))
                box = [box[0]*sx, box[1]*sy, box[2]*sx, box[3]*sy]
            else:
                dx, dy = op["shift_xy"]
                box = [box[0]+dx, box[1]+dy, box[2]+dx, box[3]+dy]
                if op["operation"] == "center_crop":
                    before = max(0, box[2]-box[0]) * max(0, box[3]-box[1])
                    w, h = op["output_size"]
                    box = [min(w, max(0, box[0])), min(h, max(0, box[1])), min(w, max(0, box[2])), min(h, max(0, box[3]))]
                    after = max(0, box[2]-box[0]) * max(0, box[3]-box[1])
                    retained *= after/before if before else 0.0
        report["bbox"] = {"source_xywh": [x, y, width, height], "processed_xyxy": box,
                          "retained_area_fraction": retained,
                          "processed_extent": [max(0, box[2]-box[0]), max(0, box[3]-box[1])]}
    return report
