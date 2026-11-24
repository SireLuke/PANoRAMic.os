#!/usr/bin/env python3
"""POST-HOC (unregistered) diagnostics for rotating_gradient.py.
X1 leakage: weight of the state outside the 5-dim pole-orbit subspace (classes of v.root0) for 'lin' vs 'circ'.
    D1 depends only on the orbit class, so 'lin' must stay inside (leak ~ 1e-12); 'circ' adds D2 and can leave.
X2 drive-phase dependence of the net asymmetry Dbar: the drive angle is Omega*t + phi, phi in {0, pi/2, pi, 3pi/2}.
    If Dbar changes sign with phi it is a protocol (timing) effect, not an intrinsic one-way property.
"""
import json
from pathlib import Path
import numpy as np
import rotating_gradient as rg
import hallway_crosshair as hc

HERE = Path(__file__).resolve().parent
dp = hc.X @ hc.X[0]
O = np.zeros((240, 5))
for k, v in enumerate((8, 4, 0, -4, -8)):
    m = dp == v
    O[m, k] = 1 / np.sqrt(m.sum())
assert abs(np.linalg.norm(O, axis=0) - 1).max() < 1e-12


def prop2(eps, omega, sgn, phi, h=0.005, T=200.0):
    n = int(round(T / h)); subs = [rg.W1 * h, rg.W0 * h, rg.W1 * h]; mats = [rg.ua(s) for s in subs]
    psi = np.zeros((240, 2), dtype=complex); psi[0, 0] = 1; psi[rg.ANTI, 1] = 1
    PE = np.zeros(n + 1); PA = np.zeros(n + 1); leak = []
    for step in range(n):
        tau = step * h
        for s, U in zip(subs, mats):
            tm = tau + 0.5 * s; ang = omega * tm + phi
            ph = np.exp(-0.5j * eps * s * (np.cos(ang) * rg.D1 + sgn * np.sin(ang) * rg.D2))[:, None]
            psi = ph * (U @ (ph * psi)); tau += s
        PE[step + 1] = abs(psi[rg.ANTI, 0]) ** 2; PA[step + 1] = abs(psi[0, 1]) ** 2
        if step % 100 == 0:
            leak.append(1 - float((np.abs(O.T @ psi[:, 0]) ** 2).sum()))
    return PE, PA, np.array(leak)


out = {"X1": [], "X2": []}
for (e, om) in ((2.0, 12.0), (0.5, 3.3), (2.0, 2.0)):
    for mode, sgn in (("lin", 0.0), ("circ", 1.0)):
        PE, PA, lk = prop2(e, om, sgn, 0.0)
        rec = {"eps": e, "omega": om, "mode": mode, "leak_max": float(lk.max()), "leak_mean": float(lk.mean()), "avgE": float(PE.mean())}
        out["X1"].append(rec); print("X1", rec)
for mode, sgn in (("lin", 0.0), ("circ", 1.0)):
    for phi in (0.0, np.pi / 2, np.pi, 3 * np.pi / 2):
        PE, PA, _ = prop2(2.0, 2.0, sgn, phi)
        rec = {"eps": 2.0, "omega": 2.0, "mode": mode, "phi": float(phi), "avgE": float(PE.mean()), "avgA": float(PA.mean()), "Dbar": float((PE - PA).mean()), "Dmax": float(np.abs(PE - PA).max())}
        out["X2"].append(rec); print("X2", {k: (round(v, 4) if isinstance(v, float) else v) for k, v in rec.items()})
json.dump(out, open(HERE / "outputs" / "eqbit_drift_001_rotating_diag.json", "w"), indent=1)
