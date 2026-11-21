import unittest

from experiments.navier_stokes.ns_spectral import run_case


class NavierStokesEvidenceTests(unittest.TestCase):
    def test_two_dimensional_exact_taylor_green_recovery(self):
        result = run_case(n=16, dimension=2, viscosity=0.01, final_time=0.1, dt=0.002)
        self.assertLess(result['exact_relative_rms_error'], 1e-11)
        self.assertLess(result['max_divergence_final'], 1e-11)

    def test_three_dimensional_taylor_green_energy_balance(self):
        result = run_case(n=16, dimension=3, viscosity=0.01, final_time=0.1, dt=0.001)
        self.assertGreater(result['energy_drop'], 0.0)
        self.assertLess(abs(result['energy_balance_residual']), 1e-8)
        self.assertLess(result['max_divergence_final'], 1e-11)
        self.assertGreater(result['enstrophy_final'], 0.0)

    def test_resolution_consistency_for_resolved_low_modes(self):
        low = run_case(n=16, dimension=3, final_time=0.1, dt=0.001)
        high = run_case(n=24, dimension=3, final_time=0.1, dt=0.001)
        self.assertLess(abs(low['energy_final'] - high['energy_final']), 2e-12)

    def test_rejects_unsupported_dimension_and_noninteger_grid(self):
        with self.assertRaises(ValueError):
            run_case(dimension=4)
        with self.assertRaises(ValueError):
            run_case(n=8.5)


if __name__ == '__main__':
    unittest.main()
