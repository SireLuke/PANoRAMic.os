import math
import unittest
from experiments.strata.dp_sphere_calibration import analytic_coefficient, fourier_coefficient

class DPSphereCalibrationTests(unittest.TestCase):
    def test_displaced_sphere_at_one_radius_matches_overlap_result(self):
        self.assertAlmostEqual(analytic_coefficient(1.0), 0.31875, places=12)

    def test_overlap_and_disjoint_branches_join_at_two_radii(self):
        self.assertAlmostEqual(analytic_coefficient(2.0), 0.7, places=12)
        self.assertAlmostEqual(analytic_coefficient(2.0 - 1e-8), analytic_coefficient(2.0 + 1e-8), places=7)

    def test_identical_configurations_have_zero_energy(self):
        self.assertEqual(analytic_coefficient(0.0), 0.0)
        self.assertEqual(fourier_coefficient(0.0, q_max=10.0, intervals=100), 0.0)

    def test_fourier_integral_matches_analytic_at_d_equals_R(self):
        numeric = fourier_coefficient(1.0, q_max=200.0, intervals=200_000)
        self.assertTrue(math.isclose(numeric, 0.31875, rel_tol=1e-5), numeric)

if __name__ == '__main__':
    unittest.main()
