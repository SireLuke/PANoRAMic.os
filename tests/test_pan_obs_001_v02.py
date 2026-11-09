"""Unit tests for PAN-OBS-001 v0.2 helper functions."""
import unittest

import numpy as np

from tools.validation.pan_obs_001_v02 import (
    latent_circle,
    percentile_bootstrap_ci,
    rotation_matrix_xyz,
    sample_indices,
)


class PanObs001V02Tests(unittest.TestCase):
    def test_latent_circle_has_expected_shape_and_radius(self):
        points = latent_circle(64)
        self.assertEqual(points.shape, (64, 3))
        np.testing.assert_allclose(
            np.linalg.norm(points[:, :2], axis=1), 1.0, atol=1e-12
        )
        np.testing.assert_allclose(points[:, 2], 0.0, atol=1e-12)

    def test_uniform_sampling_is_reproducible_and_without_replacement(self):
        a = sample_indices(100, 0.4, "uniform", np.random.default_rng(7))
        b = sample_indices(100, 0.4, "uniform", np.random.default_rng(7))
        np.testing.assert_array_equal(a, b)
        self.assertEqual(len(a), 40)
        self.assertEqual(len(np.unique(a)), 40)

    def test_sector_biased_sampling_is_reproducible(self):
        a = sample_indices(100, 0.4, "sector_biased",
                           np.random.default_rng(9), kappa=2.0)
        b = sample_indices(100, 0.4, "sector_biased",
                           np.random.default_rng(9), kappa=2.0)
        np.testing.assert_array_equal(a, b)
        self.assertEqual(len(np.unique(a)), 40)

    def test_full_fraction_selects_every_point_for_both_samplers(self):
        for strategy in ("uniform", "sector_biased"):
            indices = sample_indices(
                32, 1.0, strategy, np.random.default_rng(3)
            )
            np.testing.assert_array_equal(indices, np.arange(32))

    def test_rotation_is_orthonormal_and_preserves_pairwise_distances(self):
        rotation = rotation_matrix_xyz((37.0, 51.0, 19.0))
        np.testing.assert_allclose(rotation.T @ rotation, np.eye(3), atol=1e-12)
        points = latent_circle(25)
        rotated = points @ rotation.T
        original_distances = np.linalg.norm(
            points[:, None, :] - points[None, :, :], axis=2
        )
        rotated_distances = np.linalg.norm(
            rotated[:, None, :] - rotated[None, :, :], axis=2
        )
        np.testing.assert_allclose(
            original_distances, rotated_distances, atol=1e-12
        )

    def test_bootstrap_interval_is_reproducible_and_contains_mean(self):
        values = [1.0, 2.0, 3.0, 4.0, 5.0]
        a = percentile_bootstrap_ci(
            values, np.random.default_rng(11), n_bootstrap=500
        )
        b = percentile_bootstrap_ci(
            values, np.random.default_rng(11), n_bootstrap=500
        )
        self.assertEqual(a, b)
        self.assertEqual(a["n"], 5)
        self.assertLessEqual(a["lower"], a["mean"])
        self.assertGreaterEqual(a["upper"], a["mean"])

    def test_single_replicate_reports_no_confidence_interval(self):
        result = percentile_bootstrap_ci(
            [2.0], np.random.default_rng(1), n_bootstrap=100
        )
        self.assertEqual(result["mean"], 2.0)
        self.assertIsNone(result["lower"])
        self.assertIsNone(result["upper"])


if __name__ == "__main__":
    unittest.main()
