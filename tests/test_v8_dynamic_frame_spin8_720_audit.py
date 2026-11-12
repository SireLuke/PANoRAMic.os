import unittest

from experiments.v8_dynamic_frame_spin8_720_audit import (
    ORIGIN, radial_undulation, rotate_so8, run_audit, spin_lift_sign,
)


class V8DynamicFrameSpin8Tests(unittest.TestCase):
    def test_single_plane_spinor_double_cover_is_720_degrees(self):
        import math
        self.assertEqual(spin_lift_sign((2*math.pi, 0, 0, 0)), -1)
        self.assertEqual(spin_lift_sign((4*math.pi, 0, 0, 0)), 1)

    def test_four_plane_winding_parity_is_explicit(self):
        import math
        self.assertEqual(spin_lift_sign((2*math.pi,)*4), 1)
        self.assertEqual(spin_lift_sign((4*math.pi,)*4), 1)

    def test_origin_is_fixed_under_moving_frame(self):
        self.assertEqual(rotate_so8(ORIGIN, (0.2, -0.4, 0.7, 1.1)), ORIGIN)

    def test_radial_undulation_is_positive_and_zero_amplitude_is_unit(self):
        import math
        point = radial_undulation((1,0,0,0,0,0,0,0), math.pi/2, 0.0)
        self.assertAlmostEqual(math.sqrt(sum(x*x for x in point)), 1.0)

    def test_full_gosset_frame_audit(self):
        result = run_audit()
        self.assertEqual(result["root_count"], 240)
        self.assertEqual(result["single_plane_loop"]["spin_lift_sign_at_360_degrees"], -1)
        self.assertEqual(result["single_plane_loop"]["spin_lift_sign_at_720_degrees"], 1)
        self.assertLessEqual(result["moving_frame"]["labelled_gram_matrix_max_abs_error"], 1e-10)
        self.assertTrue(result["radial_undulation"]["positive_finite_radii"])


if __name__ == "__main__":
    unittest.main()
