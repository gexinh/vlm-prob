"""Geometry must follow declared native token layouts, not sqrt(token_count)."""
from types import SimpleNamespace
import importlib.util
from importlib.metadata import version
import unittest

import torch

from vlm_probing import CapabilityError, ProbeInputs, TokenLayout
from vlm_probing.geometry import preprocessing_report, visual_grid

HAS_V5 = (importlib.util.find_spec("transformers") is not None
          and version("transformers").split(".")[:2] == ["5", "3"])


def fixture(family, visual_counts, *, patch_size=2, processor=None, **config):
    ids = torch.tensor([[3] + [9]*n + [4] for n in visual_counts])
    valid = torch.ones_like(ids, dtype=torch.bool)
    layout = TokenLayout(valid, ids == 9, token_ids=ids)
    config = SimpleNamespace(model_type=family, image_token_id=9, image_token_index=9,
                             patch_size=patch_size, image_size=4,
                             vision_config=SimpleNamespace(patch_size=patch_size, spatial_merge_size=2),
                             **config)
    probe = SimpleNamespace(model=SimpleNamespace(config=config), processor=processor,
                            spec=SimpleNamespace(layout=lambda _: layout))
    return probe, {"input_ids": ids}, layout


class VisualGridTests(unittest.TestCase):
    def test_llava_count_and_positions_match_native_flatten_order(self):
        probe, values, _ = fixture("llava", [12])
        values["pixel_values"] = torch.ones(2, 3, 4, 6)
        grid = visual_grid(probe, values)
        self.assertEqual([g["grid_shape"] for g in grid["grids"]], [[2, 3], [2, 3]])
        self.assertEqual(grid["grids"][1]["positions"], [[0, n] for n in range(7, 13)])
        self.assertIsNone(grid["source_mapping"])
        values["pixel_values"] = values["pixel_values"][:1]
        with self.assertRaisesRegex(CapabilityError, "describes 6.*selects 12"):
            visual_grid(probe, values)

    def test_qwen_merger_and_packed_count(self):
        probe, values, _ = fixture("qwen2_5_vl", [6])
        values.update(image_grid_thw=torch.tensor([[1, 4, 6]]), pixel_values=torch.zeros(24, 12))
        grid = visual_grid(probe, values)
        self.assertEqual(grid["grids"][0]["grid_shape"], [2, 3])
        self.assertEqual(grid["grids"][0]["positions"], [[0, n] for n in range(1, 7)])
        values["pixel_values"] = torch.zeros(6, 12)
        with self.assertRaisesRegex(CapabilityError, "packed Qwen"):
            visual_grid(probe, values)

    def test_qwen_multibatch_and_ambiguous_cross_batch_image(self):
        probe, values, _ = fixture("qwen3_vl", [6, 6])
        values["image_grid_thw"] = torch.tensor([[1, 4, 6], [1, 4, 6]])
        grids = visual_grid(probe, values)["grids"]
        self.assertEqual([g["batch_index"] for g in grids], [0, 1])
        values["image_grid_thw"] = torch.tensor([[1, 4, 12]])
        with self.assertRaisesRegex(CapabilityError, "consecutive"):
            visual_grid(probe, values)

    def test_native_ids_and_layout_must_agree(self):
        probe, values, layout = fixture("llava", [4])
        values["pixel_values"] = torch.zeros(1, 3, 4, 4)
        wrong = layout.visual.clone()
        wrong[0, 0], wrong[0, 1] = True, False
        with self.assertRaisesRegex(CapabilityError, "native image-token"):
            visual_grid(probe, ProbeInputs(values, TokenLayout(layout.valid, wrong)))

    def test_internvl_tile_local_only_and_shuffle(self):
        probe, values, _ = fixture("internvl", [8], downsample_ratio=0.5)
        values["pixel_values"] = torch.zeros(2, 3, 8, 8)
        result = visual_grid(probe, values)
        self.assertEqual(result["coordinate_space"], "processed_tile")
        self.assertEqual([g["grid_shape"] for g in result["grids"]], [[2, 2], [2, 2]])
        self.assertTrue(all(g["image_index"] is None for g in result["grids"]))
        probe.model.config.ps_version = "v1"
        with self.assertRaisesRegex(CapabilityError, "v2 pixel-shuffle"):
            visual_grid(probe, values)

    def test_unsupported_or_nonspatial_paths_fail_clearly(self):
        for family in ("idefics3", "clip", "custom"):
            probe, values, _ = fixture(family, [4])
            with self.subTest(family=family), self.assertRaisesRegex(CapabilityError, "no audited geometry"):
                visual_grid(probe, values)
        probe, values, _ = fixture("llava", [4])
        values.update(pixel_values=torch.zeros(1, 3, 4, 4), vision_feature_select_strategy="full")
        with self.assertRaisesRegex(CapabilityError, "patch-only"):
            visual_grid(probe, values)
        values.pop("vision_feature_select_strategy")
        values["image_sizes"] = torch.tensor([[4, 4]])
        with self.assertRaisesRegex(CapabilityError, "packed image_sizes"):
            visual_grid(probe, values)

    def test_custom_model_without_config_fails_with_capability_error(self):
        probe = SimpleNamespace(model=torch.nn.Linear(2, 2))
        with self.assertRaisesRegex(CapabilityError, "no audited geometry.*unknown"):
            visual_grid(probe, {})

    def test_missing_merger_metadata_and_video_fail(self):
        probe, values, _ = fixture("qwen3_5", [4])
        with self.assertRaisesRegex(CapabilityError, "image_grid_thw"):
            visual_grid(probe, values)
        values["image_grid_thw"] = torch.tensor([[1, 3, 3]])
        with self.assertRaisesRegex(CapabilityError, "divisible"):
            visual_grid(probe, values)
        values["video_grid_thw"] = torch.tensor([[1, 4, 4]])
        with self.assertRaisesRegex(CapabilityError, "still images only"):
            visual_grid(probe, values)


@unittest.skipUnless(HAS_V5, "native geometry contracts require Transformers 5.3.x")
class NativeProcessorGeometryTests(unittest.TestCase):
    def test_native_internvl_shuffle_preserves_row_major_reduced_cells(self):
        from transformers.models.internvl.modeling_internvl import InternVLModel
        markers = torch.arange(16).reshape(1, 4, 4, 1)
        result = InternVLModel.pixel_shuffle(None, markers, scale_factor=0.5)
        self.assertEqual(result.reshape(4, 4).tolist(),
                         [[0, 1, 4, 5], [2, 3, 6, 7], [8, 9, 12, 13], [10, 11, 14, 15]])

    def test_native_qwen_processor_reports_merged_rectangular_grid(self):
        from PIL import Image
        from transformers import Qwen2VLImageProcessor
        processor = Qwen2VLImageProcessor(patch_size=2, temporal_patch_size=2,
                                          merge_size=2, min_pixels=16, max_pixels=1024)
        result = dict(processor(images=Image.new("RGB", (12, 8)), return_tensors="pt"))
        t, h, w = result["image_grid_thw"][0].tolist()
        probe, values, _ = fixture("qwen2_vl", [t*h*w//4])
        values.update(result)
        grid = visual_grid(probe, values)
        self.assertEqual(grid["grids"][0]["grid_shape"], [h//2, w//2])

    def test_native_vit_processor_and_adapter_exclude_cls(self):
        from PIL import Image
        from transformers import ViTConfig, ViTForImageClassification, ViTImageProcessor
        from vlm_probing import Prober
        model = ViTForImageClassification(ViTConfig(image_size=8, patch_size=2, hidden_size=8,
                    num_hidden_layers=1, num_attention_heads=2, intermediate_size=16,
                    num_labels=2, attn_implementation="eager"))
        processor = ViTImageProcessor(size={"height": 8, "width": 8})
        image = Image.new("RGB", (31, 17), (60, 70, 80))
        inputs = processor(images=image, return_tensors="pt")
        probe = Prober(model, processor)
        result = visual_grid(probe, inputs)
        self.assertEqual(result["grids"][0]["grid_shape"], [4, 4])
        self.assertEqual(result["grids"][0]["positions"][0], [0, 1])
        report = preprocessing_report(probe, inputs, image=image, bbox_xywh=[0, 0, 31, 17])
        self.assertEqual(report["geometry_status"], "supported_processor_replay_matches")
        self.assertEqual(report["bbox"]["retained_area_fraction"], 1)

    def test_clip_crop_removes_off_center_bbox_without_modifying_inputs(self):
        from PIL import Image
        from transformers import CLIPImageProcessor
        processor = CLIPImageProcessor(size={"shortest_edge": 8}, crop_size={"height": 8, "width": 8})
        image = Image.new("RGB", (32, 8), (55, 66, 77))
        inputs = processor(images=image, return_tensors="pt")
        before = inputs["pixel_values"].clone()
        probe = SimpleNamespace(processor=SimpleNamespace(image_processor=processor))
        report = preprocessing_report(probe, inputs, image=image, bbox_xywh=[0, 0, 4, 4])
        self.assertEqual(report["bbox"]["retained_area_fraction"], 0)
        self.assertEqual(report["operations"][-1]["shift_xy"], [-12, 0])
        self.assertTrue(torch.equal(before, inputs["pixel_values"]))

    def test_explicit_demo_padding_is_separate_from_processor_crop(self):
        from PIL import Image
        from transformers import CLIPImageProcessor
        processor = CLIPImageProcessor(size={"shortest_edge": 8}, crop_size={"height": 8, "width": 8})
        image = Image.new("RGB", (32, 8), (55, 66, 77))
        padded = Image.new("RGB", (32, 32), (0, 0, 0))
        padded.paste(image, (0, 12))
        inputs = processor(images=padded, return_tensors="pt")
        probe = SimpleNamespace(processor=processor)
        report = preprocessing_report(probe, inputs, image=image, bbox_xywh=[0, 0, 4, 4],
                    explicit_padding={"left": 0, "top": 12, "right": 0, "bottom": 12, "fill": (0, 0, 0)})
        self.assertEqual(report["operations"][0]["operation"], "caller_padding")
        self.assertEqual(report["bbox"]["retained_area_fraction"], 1)
        self.assertEqual(report["bbox"]["processed_extent"], [1, 1])

    def test_override_mismatch_does_not_invent_retention(self):
        from PIL import Image
        from transformers import CLIPImageProcessor
        processor = CLIPImageProcessor(size={"shortest_edge": 8}, crop_size={"height": 8, "width": 8})
        image = Image.new("RGB", (32, 8), (55, 66, 77))
        inputs = processor(images=image, do_center_crop=False, return_tensors="pt")
        probe = SimpleNamespace(processor=processor)
        report = preprocessing_report(probe, inputs, image=image, bbox_xywh=[0, 0, 4, 4])
        self.assertEqual(report["geometry_status"], "unavailable")
        self.assertIsNone(report["bbox"])
        report = preprocessing_report(probe, inputs, image=image, bbox_xywh=[0, 0, 4, 4],
                                      processor_kwargs={"do_center_crop": False})
        self.assertEqual(report["bbox"]["retained_area_fraction"], 1)

    def test_channels_last_output_is_not_mistaken_for_native_chw(self):
        from PIL import Image
        from transformers import ViTImageProcessor
        processor = ViTImageProcessor(size={"height": 3, "width": 3})
        image = Image.new("RGB", (5, 5), (55, 66, 77))
        inputs = processor(images=image, data_format="channels_last", return_tensors="pt")
        self.assertEqual(tuple(inputs["pixel_values"].shape), (1, 3, 3, 3))
        report = preprocessing_report(SimpleNamespace(processor=processor), inputs,
                    image=image, bbox_xywh=[0, 0, 5, 5], processor_kwargs={"data_format": "channels_last"})
        self.assertEqual(report["geometry_status"], "unavailable")
        self.assertIsNone(report["bbox"])

    def test_slow_center_crop_odd_small_input_rounding(self):
        from PIL import Image
        from transformers import CLIPImageProcessor
        processor = CLIPImageProcessor(do_resize=False, crop_size={"height": 8, "width": 8})
        image = Image.new("RGB", (5, 3), (55, 66, 77))
        inputs = processor(images=image, input_data_format="channels_last", return_tensors="pt")
        report = preprocessing_report(SimpleNamespace(processor=processor), inputs,
                                      image=image, bbox_xywh=[0, 0, 5, 3],
                                      processor_kwargs={"input_data_format": "channels_last"})
        self.assertEqual(report["operations"][0]["shift_xy"], [2, 3])
        self.assertEqual(report["bbox"]["processed_xyxy"], [2, 3, 7, 6])


if __name__ == "__main__":
    unittest.main()
