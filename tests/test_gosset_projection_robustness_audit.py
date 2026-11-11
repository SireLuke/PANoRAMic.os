import unittest

from experiments.gosset_projection_robustness_audit import run_audit


class GossetProjectionRobustnessTests(unittest.TestCase):
    def test_projection_count_and_orthonormality(self):
        result = run_audit(seed=20261111, replicates=3)
        self.assertEqual(result["roots"], 240)
        self.assertEqual(result["equilateral_8d_faces"], 60480)
        self.assertLessEqual(result["coxeter_plane_row_gram_max_abs_error"], 1e-10)
        self.assertEqual(result["canonical_projected_equilateral_faces"], 2160)

    def test_randomized_controls_are_zero_and_reproducible(self):
        first = run_audit(seed=20261111, replicates=3)
        second = run_audit(seed=20261111, replicates=3)
        self.assertEqual(
            first["random_control"]["equilateral_face_counts"],
            second["random_control"]["equilateral_face_counts"],
        )
        self.assertEqual(first["random_control"]["equilateral_face_counts"], [0, 0, 0])

    def test_tolerance_sweep_is_reported(self):
        result = run_audit(seed=7, replicates=1)
        counts = result["coxeter_plane_equilateral_counts_by_relative_spread_tolerance"]
        self.assertEqual(set(counts), {"1e-06", "1e-08", "1e-10", "1e-12"})
        self.assertTrue(result["threshold_sensitivity_reported_not_hidden"])


if __name__ == "__main__":
    unittest.main()
