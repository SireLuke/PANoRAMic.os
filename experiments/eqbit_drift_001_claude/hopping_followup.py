#!/usr/bin/env python3
"""POST-HOC follow-up to hopping_phases.py (declared after seeing that the J family is exactly reciprocal for the
pole/antipode pair). NOT preregistered; claim thresholds and statistics are reused unchanged from the frozen header
of hopping_phases.py (nonreciprocity Dmax>1e-2, net one-way |Dbar|>1e-2, peak enhancement > 0.882083+1e-2).

Why the J family cannot show non-reciprocity here: Theta_uv = alpha*(u^T J v) is even under v -> -v, so the antipodal
permutation P_a leaves H invariant (P_a H P_a = H), which forces U_{anti,0}(t) = U_{0,anti}(t) exactly.
New family 'Jodd': Theta_uv = alpha * (u^T J v) * (g_u + g_v), g_v = v . n along the pole axis. It is antisymmetric,
odd under v -> -v (so P_a H P_a = conj(H), not H), and not a pure gauge (nonzero triangle flux).
Gates: JG0 antipodal invariance of J exact (< 1e-12) and Jodd satisfies P_a H P_a = conj(H) (< 1e-12); JG1 Hermitian and
unitary; JG2 Jodd triangle-flux nonzero fraction reported (no threshold); JG3 sign identity P_{-a}(anti|0) = P_a(0|anti) < 1e-10.
"""
import json
from pathlib import Path
import numpy as np
import hopping_phases as hp
import hallway_crosshair as hc

HERE = Path(__file__).resolve().parent
key = {tuple(r): i for i, r in enumerate(hc.X)}
perm = np.array([key[tuple(-r)] for r in hc.X])
P = np.zeros((240, 240)); P[np.arange(240), perm] = 1
hp.BASE["Jodd"] = hp.M_J * (hp.G_AX[:, None] + hp.G_AX[None, :])
assert np.allclose(hp.BASE["Jodd"], -hp.BASE["Jodd"].T)

g = {}
g["JG0_J_antipodal_invariant"] = bool(np.abs(P @ hp.hamiltonian("J", 0.5) @ P.T - hp.hamiltonian("J", 0.5)).max() < 1e-12)
Hj = hp.hamiltonian("Jodd", 0.5)
g["JG0_Jodd_conjugated_by_antipode"] = bool(np.abs(P @ Hj @ P.T - Hj.conj()).max() < 1e-12)
rows = []
store = {}
for a in hp.ALPHAS:
    r, PE, PA = hp.run("Jodd", a)
    r["nonreciprocity_claim"] = bool(r["Dmax"] > 1e-2)
    r["net_oneway_claim"] = bool(abs(r["Dbar"]) > 1e-2)
    r["peak_enhancement_claim"] = bool(max(r["E"], r["A"]) > 0.882083 + 1e-2)
    rows.append(r); store[float(a)] = (PE, PA)
    print(f"Jodd alpha={a:6.4f} E={r['E']:.4f} A={r['A']:.4f} avgE={r['avgE']:.4f} avgA={r['avgA']:.4f} Dmax={r['Dmax']:.4f} Dbar={r['Dbar']:+.2e} flux>0:{r['nonzero_flux_fraction']:.3f}")
g["JG1_hermitian_unitary"] = bool(all(r["herm_dev"] < 1e-15 and r["unitarity_dev"] < 1e-10 for r in rows))
w, Vm = np.linalg.eigh(hp.hamiltonian("Jodd", -0.5))
g["JG3_sign_identity_value"] = float(np.abs(hp.series(w, Vm, 0, hp.ANTI, hp.T) - store[0.5][1]).max())
g["JG3_pass"] = bool(g["JG3_sign_identity_value"] < 1e-10)
json.dump({"gates": g, "rows": rows}, open(HERE / "outputs" / "eqbit_drift_001_hopping_followup.json", "w"), indent=1,
          default=lambda o: bool(o) if isinstance(o, np.bool_) else float(o))
print("\nGATES", g)
print("claims: nonrecip", sum(r["nonreciprocity_claim"] for r in rows), "net", sum(r["net_oneway_claim"] for r in rows), "enh", sum(r["peak_enhancement_claim"] for r in rows), "of", len(rows))
