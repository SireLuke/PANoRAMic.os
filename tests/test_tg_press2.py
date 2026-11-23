"""Tests for the Press II production implementation (tg_press2). Small sizes only; no Press II run is performed."""
import json, os, sys, tempfile, unittest
import numpy as np

from experiments.navier_stokes.press2 import press2_selftest as ST
from experiments.navier_stokes.press2 import tg_press2 as G

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "experiments", "ns_evidence_001_claude"))


class TGPress2(unittest.TestCase):
    def test_solver_matches_independent_lawson_solver(self):
        import ns_spectral as ns
        r = ns.run_case(dict(d=3, N=16, T=0.1, dt=0.005, form="convective"))
        sv = G.Solver(16, 0.01)
        uh = sv.init_tg()
        E0, Om0, eps0 = sv.diagnostics(uh)
        self.assertAlmostEqual(E0, 0.125, places=14)
        self.assertAlmostEqual(E0, r["E0"], places=14)
        self.assertAlmostEqual(Om0, r["Omega0"], places=12)
        for _ in range(20):
            uh = sv.step(uh, 0.005)
        E, Om, eps = sv.diagnostics(uh)
        self.assertLess(abs(E - r["E_T"]) / r["E_T"], 1e-7)
        self.assertLess(abs(eps - r["eps_T"]) / r["eps_T"], 1e-6)

    def test_fast_shuffle_path_equals_selftest_statistic(self):
        N = 20
        rng = np.random.default_rng(3)
        U = ST.synthetic_field(N, rng)
        tri = ST.triad_set(N, 5, 2000, 5)[:3]
        amp, ph = np.abs(U).reshape(3, -1), np.angle(U).reshape(3, -1)
        ts = G.TriadStat(amp, ph, tri)
        theta = np.angle(np.fft.fftn(rng.normal(size=(N, N, N))))
        self.assertAlmostEqual(ts.value(), ST.c_tri(U, tri)[0], places=12)
        self.assertAlmostEqual(ts.value(theta.reshape(-1)), ST.c_tri(U * np.exp(1j * theta)[None], tri)[0], places=12)
        self.assertLess(abs(ts.active_weight() / ST.c_tri(U, tri)[1] - 1.0), 1e-12)

    def test_o3_triads_sum_to_zero(self):
        a, b, c, meta = G.o3_triads(24, 4, 8)
        K = ST.kvec(24).reshape(3, -1).T
        self.assertTrue(np.all(K[a] + K[b] + K[c] == 0))
        self.assertGreater(meta["n_triads"], 100)

    def test_front_and_stage_a(self):
        E = np.zeros(20); E[:5] = 1.0
        self.assertEqual(G.front_K(E), 4)
        h = dict(t=[8.0, 8.9, 9.5], eps=[0.01, 0.0137585, 0.012])
        self.assertTrue(G.stage_a(h)["gate_pass"])
        h2 = dict(t=[8.0, 8.9, 9.5], eps=[0.01, 0.0155, 0.012])
        self.assertFalse(G.stage_a(h2)["gate_pass"])

    def test_analysis_rule_on_synthetic_results(self):
        t = [0.25 * i for i in range(49)]
        rng = np.random.default_rng(0)
        snaps = []
        for ti in t:
            base = rng.normal(0.01, 0.002, 100)
            hi = 0.5 if 6 <= ti <= 10 else 0.01
            snaps.append(dict(O1=hi, W1=1.0, O1_ens=base.tolist(), O3=0.01, W3=1.0, O3_ens=base.tolist(),
                              O2=6.0 if 6 <= ti <= 10 else 3.0, O2_ens=(3 + 0.01 * base).tolist()))
        hist = dict(t=[8.9], eps=[0.0137585])
        r = G.analyze(dict(stats=dict(t=t, snap=snaps), hist=hist))
        self.assertTrue(r["O1"]["separates"]); self.assertEqual(r["O1"]["hit_count"], 17)
        self.assertFalse(r["O3"]["separates"]); self.assertTrue(r["O2"]["separates"])
        self.assertIn("O1 passes, O3 fails", r["verdict_text"])

    def test_smoke_run_and_resume(self):
        with tempfile.TemporaryDirectory() as d:
            class A: pass
            a = A(); a.out = d; a.N = 16; a.Re = 100.0; a.T = 0.5; a.dt = 0.01; a.M = 3; a.cap = 300; a.kmax = 5; a.tag = "smoke"
            G.run(a)
            with open(os.path.join(d, "smoke.json")) as fh:
                res = json.load(fh)
            self.assertEqual(len(res["stats"]["t"]), 3)                 # t = 0, 0.25, 0.5
            self.assertEqual(len(res["stats"]["snap"][0]["O1_ens"]), 3)
            E = res["hist"]["E"]
            self.assertAlmostEqual(E[0], 0.125, places=12)
            self.assertTrue(all(E[i + 1] <= E[i] + 1e-12 for i in range(len(E) - 1)))
            # determinism: second run in a fresh dir gives identical statistics
            with tempfile.TemporaryDirectory() as d2:
                a.out = d2; G.run(a)
                with open(os.path.join(d2, "smoke.json")) as fh:
                    res2 = json.load(fh)
                self.assertEqual(res["stats"]["snap"][2]["O1_ens"], res2["stats"]["snap"][2]["O1_ens"])


if __name__ == "__main__":
    unittest.main()
