import math
import unittest

from core.geometry.e8_quasicrystal import (
    PHI, breathing_phason_window, e8_lattice_shell_doubled,
    golden_4plus4_split, projected_shell, split_invariant_residual,
)
from core.holography.celestial import (
    CelestialChart8, CelestialPrimary, HardInsertion,
    leading_soft_gluon_ward_kernel, mellin_soft_factor, mellin_soft_residue,
)
from experiments.e8_spherical_shell_audit import e8_lattice_shell
from experiments.celestial_gosset_quasicrystal_audit import run_audit


class CelestialKinematicsTests(unittest.TestCase):
    def test_primary_weights_and_chart_round_trip(self):
        primary = CelestialPrimary(1.0 + 0.25j, 1.0, 0.3 + 0.4j, 1.0, -0.5, 1)
        self.assertEqual(primary.weights, (1.0 + 0.625j, 0.0 - 0.375j))
        chart = CelestialChart8.from_primary(primary)
        self.assertEqual(len(chart.as_vector()), 8)
        self.assertEqual(chart.to_primary(), primary)
        self.assertEqual(CelestialChart8.from_vector(chart.as_vector()), chart)

    def test_mellin_leading_soft_pole_and_residue(self):
        self.assertAlmostEqual(mellin_soft_factor(1.25, 1, 1.0).real, 4.0)
        self.assertEqual(mellin_soft_residue(1, 3.5 + 0j), 3.5 + 0j)
        with self.assertRaises(ZeroDivisionError):
            mellin_soft_factor(1.0, 1, 1.0)

    def test_leading_soft_current_kernel(self):
        value = leading_soft_gluon_ward_kernel(
            0.5 + 0j,
            (HardInsertion(0j, 1 + 0j), HardInsertion(1 + 0j, -1 + 0j)),
        )
        self.assertAlmostEqual(value.real, 4.0)
        self.assertAlmostEqual(value.imag, 0.0)

    def test_chart_rejects_wrong_dimension_and_invalid_eta(self):
        with self.assertRaises(ValueError):
            CelestialChart8.from_vector((0.0,) * 7)
        with self.assertRaises(ValueError):
            CelestialChart8.from_vector((0.0,) * 7 + (0.5,))


class E8GoldenCutProjectTests(unittest.TestCase):
    def test_first_three_shells_match_repository_shell_generator(self):
        expected = {1: 240, 2: 2160, 3: 6720}
        for n, count in expected.items():
            ours = e8_lattice_shell_doubled(n)
            canonical = e8_lattice_shell(n)
            self.assertEqual(len(ours), count)
            self.assertEqual(set(ours), set(canonical))

    def test_golden_split_is_orthogonal(self):
        self.assertAlmostEqual(PHI * PHI, PHI + 1.0)
        probes = (
            (1, 0, 0, 0, 0, 0, 0, 0),
            (0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, 0.5),
            (1, 1, 0, 0, 0, 0, 0, 0),
        )
        for vector in probes:
            self.assertLess(split_invariant_residual(vector), 1e-12)
            parallel, perpendicular = golden_4plus4_split(vector)
            self.assertEqual(len(parallel), 4)
            self.assertEqual(len(perpendicular), 4)

    def test_window_is_positive_and_periodic(self):
        first = breathing_phason_window(0.0)
        last = breathing_phason_window(2 * math.pi)
        self.assertGreater(first.radius, 0.0)
        self.assertAlmostEqual(first.radius, last.radius, places=14)
        self.assertEqual(first.center, last.center)

    def test_undulating_selection_is_periodic_and_phase_dependent(self):
        first = projected_shell(1, 0.0)
        last = projected_shell(1, 2 * math.pi)
        self.assertEqual(tuple(p.lattice_point for p in first),
                         tuple(p.lattice_point for p in last))
        counts = [len(projected_shell(1, phase)) for phase in (
            0.0, math.pi / 2, math.pi, 3 * math.pi / 2
        )]
        self.assertTrue(all(0 < count <= 240 for count in counts))
        self.assertGreater(len(set(counts)), 1)

    def test_combined_runner_keeps_scope_boundaries(self):
        result = run_audit()
        self.assertTrue(result["celestial"]["chart_round_trip"])
        self.assertEqual(result["quasicrystal"]["shell_counts"],
                         {"1": 240, "2": 2160, "3": 6720})
        self.assertIn("not yet defined", result["bridge_status"])


if __name__ == "__main__":
    unittest.main()
