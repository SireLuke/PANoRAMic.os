"""Unit tests for the exploratory ABOM-v8 mathematical integration layer."""
import math
import unittest

from core.abom_v8.abom_v8_model import (
    PHI, PHI_INV, abom_v8_sample, apply_6d_basis, e8_roots,
    exponential_scale, fermi_channels, fermi_occupation,
    golden_scale_branches, hyperoctahedral_action,
    hyperoctahedral_group_order, inverse_exponential_scale,
    oscillator_energy_level, radial_exponential_field, spatial_octants,
)


class ABOMV8ModelTests(unittest.TestCase):
    def test_exponential_round_trip(self):
        for length in (1e-6, 0.125, 1.0, 3.5, 1e6):
            self.assertAlmostEqual(
                inverse_exponential_scale(exponential_scale(length)), length,
                delta=max(1e-14, length * 1e-12))

    def test_golden_ratio_identity(self):
        self.assertAlmostEqual(PHI * PHI_INV, 1.0, places=14)
        branches = golden_scale_branches(2.0)
        self.assertAlmostEqual(branches["phi"] / branches["phi_inverse"], PHI**2)
        self.assertLess(branches["phi_negative"], 0.0)

    def test_fermi_complement_and_sign(self):
        for energy in (-20.0, -2.0, 0.0, 2.0, 20.0):
            channels = fermi_channels(energy)
            self.assertAlmostEqual(
                channels["positive_occupation"] +
                channels["complementary_hole_fraction"], 1.0, places=14)
            self.assertAlmostEqual(
                channels["signed_contrast"],
                2.0 * fermi_occupation(energy) - 1.0, places=14)
        self.assertGreater(fermi_channels(-5)["signed_contrast"], 0)
        self.assertLess(fermi_channels(5)["signed_contrast"], 0)

    def test_e8_root_system_count_and_norms(self):
        roots = e8_roots()
        self.assertEqual(len(roots), 240)
        self.assertEqual(len(set(roots)), 240)
        for root in roots:
            self.assertAlmostEqual(sum(v*v for v in root), 2.0, places=14)

    def test_hyperoctahedral_order_and_action(self):
        self.assertEqual(hyperoctahedral_group_order(8), 10321920)
        out = hyperoctahedral_action((1, 2, 3), (2, 0, 1), (-1, 1, -1))
        self.assertEqual(out, (-3.0, 1.0, -2.0))
        self.assertAlmostEqual(sum(v*v for v in out), 14.0)

    def test_six_dimensional_identity_basis(self):
        basis = [[1.0 if i == j else 0.0 for j in range(6)] for i in range(6)]
        values = (1, 2, 3, 4, 5, 6)
        self.assertEqual(apply_6d_basis(basis, values), tuple(float(v) for v in values))

    def test_octants_and_radial_symmetry(self):
        octants = spatial_octants(1, 2, 3)
        self.assertEqual(len(octants), 8)
        self.assertEqual(len(set(octants.values())), 8)
        baseline = radial_exponential_field(1, 2, 3)
        self.assertAlmostEqual(baseline, radial_exponential_field(-1, 2, -3))
        self.assertAlmostEqual(baseline, radial_exponential_field(3, 1, 2))

    def test_oscillator_levels(self):
        self.assertAlmostEqual(oscillator_energy_level(0), 0.5)
        self.assertAlmostEqual(oscillator_energy_level(3), 3.5)

    def test_integrated_sample_keeps_channels_separate(self):
        sample = abom_v8_sample(1, -2, 3, energy=1.0)
        self.assertEqual(len(sample["octants"]), 8)
        self.assertEqual(sample["e8_root_count"], 240)
        self.assertEqual(sample["hyperoctahedral_B8_order"], 10321920)
        self.assertIn("occupation_channel", sample["fermi_weighted_field"])
        self.assertIn("hole_channel", sample["fermi_weighted_field"])
        self.assertIn("signed_contrast_channel", sample["fermi_weighted_field"])
        self.assertIn("not a physical unification", sample["status"])


if __name__ == "__main__":
    unittest.main()
