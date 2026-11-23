#!/usr/bin/env python3
"""Post-run, UNREGISTERED follow-ups to hallway_crosshair.py (declared as such).
F1: first time P(antipode | start root 0) reaches 0.95/0.99/0.999 in the hall configuration (E0=0), window 3000, dt 0.01.
F2: mechanism test. Replace the origin by a pure on-site shift delta on the dipole mode d_hat (the 28-eigenmode along the
    pole axis) of the plain 240-node graph, and also on the perpendicular dipole (control: pole state is orthogonal to it, so
    the pole dynamics must be unchanged). Peak of P(antipode) over t in [0,200], dt 0.005, refined.
"""
import json
from pathlib import Path
import numpy as np
import hallway_crosshair as h

HERE = Path(__file__).resolve().parent
out = {"F1": [], "F2": []}
psi = np.zeros(241); psi[0] = 1.0
t = np.arange(0, 3000 + 1e-9, 0.01)
for g in (0.05, 0.1, 0.25, 0.5, 1.0):
    H = h.hamiltonian(g * (h.V8 @ h.N_AX), 0.0); w, V = np.linalg.eigh(H)
    P = (np.abs(h.amp_rows(w, V, psi, [h.anti], t, chunk=20000)) ** 2).sum(0)
    rec = {"g": g, "max_over_3000": float(P.max())}
    for thr in (0.95, 0.99, 0.999):
        i = np.nonzero(P >= thr)[0]; rec[f"first_ge_{thr}"] = float(t[i[0]]) if len(i) else None
    out["F1"].append(rec)
    print("F1", rec)

dh = (h.V8 @ h.N_AX); dh = dh / np.linalg.norm(dh)
dp = (h.V8 @ h.N_PERP); dp = dp / np.linalg.norm(dp)
psi240 = np.zeros(240); psi240[0] = 1.0
tt = np.arange(0, h.T_MAX + 1e-9, 0.005)
def peak(H):
    w, V = np.linalg.eigh(H); c = V.T @ psi240
    best = 0.0
    for s in range(0, len(tt), 5000):
        x = tt[s:s+5000]
        a = V[h.anti, :] @ (np.exp(-1j * np.outer(w, x)) * c[:, None])
        best = max(best, float((np.abs(a) ** 2).max()))
    return best
for delta in (0.0, 0.01, 0.1, 0.5, 1.0, 3.0, -1.0):
    rec = {"delta": delta, "dipole_axis_shift_peak": peak(h.A + delta * np.outer(dh, dh)),
           "perp_dipole_shift_peak": peak(h.A + delta * np.outer(dp, dp))}
    out["F2"].append(rec); print("F2", rec)
json.dump(out, open(HERE / "outputs" / "eqbit_drift_001_hallway_followups.json", "w"), indent=1)
