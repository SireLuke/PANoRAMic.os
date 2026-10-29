"""Tests for established-equation adapters used in ABOM-v8."""
import math
import unittest

from core.abom_v8.physics_adapters import (
    decay_constant_from_half_life, homogeneous_gpe_residual,
    homogeneous_gpe_stationary_amplitude, map_scalar_to_v8, radioactive_decay,
)


class PhysicsAdapterTests(unittest.TestCase):
    def test_half_life_and_decay(self):
        lam = decay_constant_from_half_life(1.0)
        self.assertAlmostEqual(lam, math.log(2.0))
        self.assertAlmostEqual(radioactive_decay(1000.0, lam, 1.0), 500.0)
        self.assertAlmostEqual(radioactive_decay(1000.0, lam, 0.0), 1000.0)

    def test_decay_inverse_recovery(self):
        a0, lam, t = 42.0, 0.17, 3.2
        at = radioactive_decay(a0, lam, t)
        recovered = at * math.exp(lam * t)
        self.assertAlmostEqual(recovered, a0)

    def test_uniform_stationary_gpe_residual(self):
        mu, g = 2.0, 0.5
        psi = homogeneous_gpe_stationary_amplitude(mu, g)
        self.assertAlmostEqual(psi, 2.0)
        self.assertAlmostEqual(homogeneous_gpe_residual(psi, mu, g), 0.0, places=14)

    def test_v8_scalar_projection_keeps_channel_explicit(self):
        mapped = map_scalar_to_v8(3.25, "chi")
        self.assertEqual(mapped["V8"]["chi"], 3.25)
        self.assertIsNone(mapped["V8"]["f"])
        self.assertEqual(mapped["mapped_coordinate"], "chi")


if __name__ == "__main__":
    unittest.main()
