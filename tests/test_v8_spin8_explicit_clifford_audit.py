import math
import unittest

from experiments.v8_spin8_explicit_clifford_audit import (
    GAMMA, clifford_residuals, run_audit, schedule_from_degrees,
    spinor_lift, identity, matadd, max_abs, scale,
)


class ExplicitSpin8CliffordAuditTests(unittest.TestCase):
    def test_eight_hermitian_clifford_generators(self):
        residuals = clifford_residuals()
        self.assertEqual(residuals["generator_count"], 8)
        self.assertLess(max(residuals[key] for key in ("gamma_square_max_error", "anticommutator_max_error", "hermitian_max_error")), 1e-10)

    def test_single_plane_spin_lift_is_minus_identity_at_360(self):
        result = spinor_lift((2*math.pi, 0, 0, 0))
        self.assertLess(max_abs(matadd(result, identity())), 1e-10)

    def test_single_plane_spin_lift_returns_at_720(self):
        result = spinor_lift((4*math.pi, 0, 0, 0))
        self.assertLess(max_abs(matadd(result, scale(identity(), -1))), 1e-10)

    def test_asymmetric_orientation_schedule_is_unitary(self):
        result = run_audit()
        self.assertEqual(result["asymmetric_schedule"]["angles_degrees"], [60.0,90.0,180.0,720.0])
        self.assertLess(result["asymmetric_schedule"]["spinor_unitarity_max_error"], 1e-10)

    def test_schedule_rejects_wrong_plane_count(self):
        with self.assertRaises(ValueError):
            schedule_from_degrees((60, 90, 180))

    def test_full_audit(self):
        result = run_audit()
        self.assertEqual(result["orientation_cases"]["central_inversion_determinant"], 1)
        self.assertEqual(result["orientation_cases"]["single_hyperplane_reflection_determinant"], -1)


if __name__ == "__main__":
    unittest.main()
