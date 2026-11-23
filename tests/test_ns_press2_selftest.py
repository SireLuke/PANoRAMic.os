"""Tests for the NS Press II calibration self-test pipeline (statistic-level; no integration)."""
import unittest
import numpy as np

from experiments.navier_stokes.press2 import press2_selftest as P


class Press2SelfTest(unittest.TestCase):
    N, KMAX = 24, 6

    def setUp(self):
        self.rng = np.random.default_rng(1)
        self.tri = P.triad_set(self.N, self.KMAX, 3000, 7)

    def test_triads_sum_to_zero_and_are_deterministic(self):
        a, b, c, meta = self.tri
        K = P.kvec(self.N).reshape(3, -1).T
        self.assertTrue(np.all(K[a] + K[b] + K[c] == 0))
        self.assertTrue(np.all((K[a] ** 2).sum(1) <= self.KMAX ** 2))
        self.assertEqual(meta["sha256"], P.triad_set(self.N, self.KMAX, 3000, 7)[3]["sha256"])

    def test_shuffle_preserves_amplitude_solenoidality_and_reality(self):
        u = P.synthetic_field(self.N, self.rng)
        s = P.hermitian_shuffle(u, self.rng)
        self.assertLess(float(np.max(np.abs(np.abs(s) - np.abs(u)))), 1e-12)
        self.assertLess(float(np.max(np.abs((P.kvec(self.N) * s).sum(0)))), 1e-10 * float(np.max(np.abs(u))))
        self.assertLess(float(np.max(np.abs(np.fft.ifftn(s[0], axes=(0, 1, 2)).imag))), 1e-12)

    def test_perfectly_locked_field_gives_one_and_shuffle_gives_small(self):
        u = P.synthetic_field(self.N, self.rng)
        locked = P.planted_field(u, self.rng, sigma=0.0)
        self.assertAlmostEqual(P.c_tri(locked, self.tri[:3])[0], 1.0, places=9)
        self.assertLess(P.c_tri(P.hermitian_shuffle(locked, self.rng), self.tri[:3])[0], 0.15)

    def test_separation_rule_counts(self):
        ens = np.tile(np.arange(100.0), (17, 1))           # 95th percentile = 94.05
        real = np.array([200.0] * 9 + [0.0] * 8)
        ok, cnt, _ = P.separates(real, ens)
        self.assertTrue(ok); self.assertEqual(cnt, 9)
        real[0] = 0.0
        ok, cnt, _ = P.separates(real, ens)
        self.assertFalse(ok); self.assertEqual(cnt, 8)

    def test_null_calibration_runs_and_planted_control_separates(self):
        r = P.run_demo(self.N, self.KMAX, 3000, 30, 17, 11)
        self.assertTrue(r["planted_control"]["separates"])
        self.assertLessEqual(r["null_calibration"]["false_positive_rate"], 0.2)
        self.assertLess(r["shuffle_checks"]["max_abs_amplitude_change"], 1e-12)


if __name__ == "__main__":
    unittest.main()
