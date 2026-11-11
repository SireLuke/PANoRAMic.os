import math
import unittest

from core.abom_v8.fractional_fermi_sea import (
    compare_with_fermi_dirac,
    ffs_diagnostics,
    ffs_parameters,
    fractional_fermi_occupation,
    normalized_one_body_correlation,
    one_body_correlation,
)


class FractionalFermiSeaTests(unittest.TestCase):
    def test_reported_fractional_plateau_levels(self):
        p2 = ffs_parameters(2, 1.0)
        p4 = ffs_parameters(4, 1.0)
        self.assertEqual(p2["fractional_occupancy"], 0.5)
        self.assertEqual(p4["fractional_occupancy"], 0.25)
        self.assertEqual(p2["momentum_cutoff"], 2.0)
        self.assertEqual(p4["momentum_cutoff"], 4.0)

    def test_box_profile_and_cutoff(self):
        self.assertEqual(fractional_fermi_occupation(0.0, 2, 1.0), 0.5)
        self.assertEqual(fractional_fermi_occupation(1.99, 2, 1.0), 0.5)
        self.assertEqual(fractional_fermi_occupation(2.0, 2, 1.0), 0.0)
        self.assertEqual(fractional_fermi_occupation(-2.0, 2, 1.0), 0.0)

    def test_density_normalization(self):
        # Integral dk/(2pi) n(k) = k_F/pi for either ell.
        for ell in (2, 4):
            p = ffs_parameters(ell, 1.7)
            integral = (2 * p["momentum_cutoff"] * p["fractional_occupancy"]) / (2 * math.pi)
            self.assertAlmostEqual(integral, p["normalization_density"], places=12)

    def test_fourier_transform_is_sinc_and_has_expected_zero(self):
        for ell in (2, 4):
            kf = 1.3
            x0 = math.pi / (ell * kf)
            self.assertAlmostEqual(normalized_one_body_correlation(0.0, ell, kf), 1.0)
            self.assertAlmostEqual(normalized_one_body_correlation(x0, ell, kf), 0.0, places=12)
            self.assertAlmostEqual(one_body_correlation(0.0, ell, kf), kf / math.pi)

    def test_fd_and_ffs_are_not_conflated(self):
        result = compare_with_fermi_dirac(0.0, 2, 1.0, 0.2, 0.0)
        self.assertEqual(result["fractional_fermi_sea_occupation"], 0.5)
        self.assertEqual(result["fermi_dirac_thermal_occupation"], 0.5)
        self.assertFalse(result["same_distribution"])
        result = compare_with_fermi_dirac(0.5, 2, 1.0, 0.2, 0.0)
        self.assertNotEqual(result["fractional_fermi_sea_occupation"],
                            result["fermi_dirac_thermal_occupation"])

    def test_v8_outputs_are_proposals_not_automatic_mapping(self):
        result = ffs_diagnostics(2, 1.0, [0.0, 1.0])
        self.assertEqual(result["v8_mapping_status"], "proposal_only_no_coordinates_computed")
        self.assertIsNone(result["v8_candidate_observables"]["u"])
        self.assertIn("measure entropy", result["v8_candidate_observables"]["d"])

    def test_invalid_cycle_index_rejected(self):
        with self.assertRaises(ValueError):
            ffs_parameters(3, 1.0)


if __name__ == "__main__":
    unittest.main()
