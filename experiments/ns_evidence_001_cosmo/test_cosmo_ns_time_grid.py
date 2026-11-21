"""Regression tests for the Cosmo NS-EVIDENCE-001 runner time grid."""
import importlib.util
import pathlib
import unittest

MODULE_PATH = pathlib.Path(__file__).with_name("cosmo_ns.py")
SPEC = importlib.util.spec_from_file_location("cosmo_ns", MODULE_PATH)
cosmo_ns = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(cosmo_ns)

class TimeGridValidationTests(unittest.TestCase):
    def test_exact_grid_returns_step_count(self):
        self.assertEqual(cosmo_ns.validate_time_grid(0.1, 0.002), 50)
        self.assertEqual(cosmo_ns.validate_time_grid(0.5, 0.004), 125)

    def test_rejects_non_divisible_grid(self):
        with self.assertRaisesRegex(ValueError, "not an integer multiple"):
            cosmo_ns.validate_time_grid(0.1, 0.008)

    def test_rejects_non_positive_or_non_finite_values(self):
        cases = ((0.0, 0.1), (-1.0, 0.1), (0.1, 0.0),
                 (0.1, -0.1), (float("nan"), 0.1),
                 (0.1, float("inf")))
        for T, dt in cases:
            with self.subTest(T=T, dt=dt):
                with self.assertRaises(ValueError):
                    cosmo_ns.validate_time_grid(T, dt)

    def test_runner_rejects_mismatched_grid_before_integrating(self):
        with self.assertRaisesRegex(ValueError, "not an integer multiple"):
            cosmo_ns.run_case(8, 2, T=0.1, dt=0.008)

if __name__ == "__main__":
    unittest.main()
