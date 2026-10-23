"""Display clipping must preserve measurements and signed/shared-scale meaning."""
import unittest

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from vlmprobe.visualization import plot_attention_comparison, plot_attention_overlay


class PercentileDisplayTests(unittest.TestCase):
    def setUp(self):
        self.image = np.zeros((12, 16, 3), dtype=np.uint8)

    def tearDown(self):
        plt.close("all")

    def test_outlier_display_improves_without_editing_measured_values(self):
        values = np.linspace(.01, .2, 100).reshape(10, 10)
        values[0, 0] = 100
        original = values.copy()
        ax = plot_attention_overlay(self.image, values, clip=(1, 99))
        artist = ax.images[1]
        np.testing.assert_allclose(artist.get_clim(), np.percentile(values, (1, 99)))
        np.testing.assert_array_equal(artist.get_array(), original)
        np.testing.assert_array_equal(values, original)
        self.assertGreater(float(artist.norm(.15)), .1)
        self.assertIn("display percentiles", ax.figure.axes[-1].get_ylabel())

    def test_default_and_explicit_bounds_are_backward_compatible(self):
        values = np.array([[1., 2.], [3., 100.]])
        full = plot_attention_overlay(self.image, values, colorbar=False)
        self.assertEqual(full.images[1].get_clim(), (0, 100))
        manual = plot_attention_overlay(self.image, values, clip=(10, 90), vmin=0, vmax=7)
        self.assertEqual(manual.images[1].get_clim(), (0, 7))
        self.assertIn("explicit display limits", manual.figure.axes[-1].get_ylabel())
        self.assertNotIn("percentiles", manual.figure.axes[-1].get_ylabel())
        partial = plot_attention_overlay(self.image, values, clip=(10, 90), vmax=7)
        self.assertIn("explicit vmax", partial.figure.axes[-1].get_ylabel())

    def test_nan_mask_and_constant_maps_remain_valid(self):
        values = np.array([[np.nan, 1.], [2., 50.]])
        ax = plot_attention_overlay(self.image, values, clip=(0, 50), colorbar=False)
        self.assertEqual(ax.images[1].get_clim(), (1, 2))
        self.assertTrue(np.ma.getmaskarray(ax.images[1].get_array())[0, 0])
        for sign in (False, True):
            zero = plot_attention_overlay(self.image, np.zeros((2, 2)), signed=sign,
                                           clip=(1, 99), colorbar=False)
            norm = zero.images[1].norm
            self.assertLess(norm.vmin, norm.vmax)
            self.assertTrue(np.isfinite(norm(np.zeros((2, 2)))).all())

    def test_signed_percentiles_keep_zero_centered_and_symmetric(self):
        values = np.array([[-100., -2., 0.], [1., 2., 3.]])
        ax = plot_attention_overlay(self.image, values, signed=True, clip=(20, 80),
                                    colorbar=False)
        norm = ax.images[1].norm
        self.assertEqual((norm.vmin, norm.vcenter, norm.vmax), (-2, 0, 2))
        np.testing.assert_array_equal(ax.images[1].get_array(), values)
        with self.assertRaisesRegex(ValueError, "negative"):
            plot_attention_overlay(self.image, values, clip=(20, 80))

    def test_comparison_percentiles_use_pooled_values_for_shared_scales(self):
        first = np.array([[0., 1.], [2., 100.]])
        second = np.array([[1., 2.], [3., 4.]])
        figure, axes = plot_attention_comparison(self.image, {"a": first, "b": second},
                                                shared_scale=True, clip=(0, 75))
        norm = axes[0, 0].images[1].norm
        self.assertIs(norm, axes[0, 1].images[1].norm)
        np.testing.assert_allclose((norm.vmin, norm.vmax),
                                   np.percentile(np.concatenate((first.ravel(), second.ravel())), (0, 75)))
        np.testing.assert_array_equal(axes[0, 0].images[1].get_array(), first)
        self.assertIn("display percentiles", figure.axes[-1].get_ylabel())

    def test_invalid_percentiles_fail_actionably(self):
        for clip in ((-1, 99), (1, 101), (50, 50), (99, 1), (np.nan, 99),
                     (1, np.inf), (True, 99), ("1", 99), (1,), 99, "19",
                     iter((1, 99)), np.array([[1], [99]])):
            with self.subTest(clip=str(clip)):
                with self.assertRaisesRegex(ValueError, "two percentiles"):
                    plot_attention_overlay(self.image, np.ones((2, 2)), clip=clip)


if __name__ == "__main__":
    unittest.main()
