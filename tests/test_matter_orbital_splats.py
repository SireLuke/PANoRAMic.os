"""Tests for the hydrogenic orbital Gaussian-splat generator (fast subset)."""
import importlib.util
import math
import sys
import unittest
from pathlib import Path

import numpy as np

from core.abom_v8 import hydrogen_baseline as HB

_path = Path(__file__).resolve().parents[1] / "experiments" / "matter_splats" / "orbital_splats.py"
_spec = importlib.util.spec_from_file_location("orbital_splats", _path)
OS = importlib.util.module_from_spec(_spec)
sys.modules["orbital_splats"] = OS
_spec.loader.exec_module(OS)


class OrbitalSplatTests(unittest.TestCase):
    def test_vectorised_radial_matches_baseline(self):
        r = np.linspace(0.0, 40.0, 61)
        for n, l in [(1, 0), (2, 0), (2, 1), (3, 0), (3, 1), (3, 2)]:
            for rv, v in zip(r, OS._radial_fast(n, l, r)):
                self.assertAlmostEqual(float(v), HB.radial(n, l, float(rv)), places=12)

    def test_real_harmonics_match_complex_baseline_for_m0_and_are_normalised(self):
        for l in (0, 1, 2):
            for th, ph in [(0.4, 0.2), (1.2, 2.0), (2.5, 4.0)]:
                x, y, z = (np.array([math.sin(th) * math.cos(ph)]), np.array([math.sin(th) * math.sin(ph)]),
                           np.array([math.cos(th)]))
                got = float(OS._real_ylm(l, 0, x, y, z)[0])
                self.assertAlmostEqual(got, HB.spherical_harmonic(l, 0, th, ph).real, places=12)
        n_pts = 400_000
        rng = np.random.default_rng(3)
        v = rng.normal(size=(n_pts, 3)); v /= np.linalg.norm(v, axis=1)[:, None]
        for l, m in [(1, 1), (1, -1), (2, 1), (2, -1), (2, 2), (2, -2)]:
            y = OS._real_ylm(l, m, v[:, 0], v[:, 1], v[:, 2])
            self.assertAlmostEqual(4 * math.pi * float(np.mean(y * y)), 1.0, delta=0.02)

    def test_fit_quality_for_1s_and_2pz(self):
        for state in [(1, 0, 0), (2, 1, 0)]:
            res = OS.fit_orbital(*state)
            q = res["quality"]
            self.assertAlmostEqual(q["weight_sum"], 1.0, places=12)
            self.assertLess(q["tail_mass_dropped"], 1e-3)
            self.assertLess(q["relative_l2_error"], 0.15)
            self.assertLess(q["mean_radius_rel_error"], 0.01)
            self.assertAlmostEqual(q["captured_probability"], 1.0, delta=1e-3)
        signs = {s["sign"] for s in OS.fit_orbital(2, 1, 0)["splats"]}
        self.assertEqual(signs, {1, -1})                      # p orbital has two opposite-sign lobes

    def test_splat_covariances_are_symmetric_positive_definite(self):
        for s in OS.fit_orbital(1, 0, 0)["splats"]:
            c = np.array(s["cov"])
            self.assertTrue(np.allclose(c, c.T, atol=1e-10))
            self.assertGreater(np.linalg.eigvalsh(c).min(), 0.0)
            self.assertGreater(s["weight"], 0.0)


if __name__ == "__main__":
    unittest.main()
