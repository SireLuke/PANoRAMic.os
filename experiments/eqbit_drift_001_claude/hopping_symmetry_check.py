#!/usr/bin/env python3
"""POST-HOC (unregistered) explanation check for hopping_phases.py / hopping_followup.py.
S1: the coordinate swap (x0 x1)(x2 x3)(x4 x5)(x6 x7) is a root-lattice automorphism; it fixes root 0 and its antipode and sends
    J -> -J, so V H V^T = conj(H) for the J and Jodd families. A unitary V with V H V^dagger = H^T that fixes both vertices forces
    |U_ab(t)| = |U_ba(t)| exactly. Gate: deviation < 1e-12 and V fixes root 0 and its antipode.
S2: scan ALL pairs (0, b), alpha = 0.5, families J, Jodd, ord: instantaneous non-reciprocity Dmax_b = max_t |P(b|0)-P(0|b)| and net
    Dbar_b over t in [0,200], dt = 0.02. Reports how many pairs exceed 1e-2 and the largest values.
"""
import json
from pathlib import Path
import numpy as np
import hopping_phases as hp
import hopping_followup  # registers 'Jodd' in hp.BASE (and re-runs its small script body)
import hallway_crosshair as hc

HERE = Path(__file__).resolve().parent
key = {tuple(r): i for i, r in enumerate(hc.X)}
sw = list(range(8))
for k in range(4):
    sw[2 * k], sw[2 * k + 1] = 2 * k + 1, 2 * k
perm = np.array([key[tuple(r[sw])] for r in hc.X])          # image of each root under the swap
Pm = np.zeros((240, 240)); Pm[np.arange(240), perm] = 1
out = {"S1": {}, "S2": {}}
out["S1"]["swap_fixes_root0"] = bool(perm[0] == 0)
out["S1"]["swap_fixes_antipode"] = bool(perm[hc.anti] == hc.anti)
for fam in ("J", "Jodd", "ord"):
    H = hp.hamiltonian(fam, 0.5)
    out["S1"][fam + "_dev_VHVt_minus_conjH"] = float(np.abs(Pm @ H @ Pm.T - H.conj()).max())
out["S1"]["pass"] = bool(out["S1"]["swap_fixes_root0"] and out["S1"]["swap_fixes_antipode"]
                         and out["S1"]["J_dev_VHVt_minus_conjH"] < 1e-12 and out["S1"]["Jodd_dev_VHVt_minus_conjH"] < 1e-12)
print("S1", out["S1"])
tt = np.arange(0, 200 + 1e-9, 0.02)
for fam in ("J", "Jodd", "ord"):
    H = hp.hamiltonian(fam, 0.5)
    w, Vm = np.linalg.eigh(H)
    a = np.conj(Vm[0, :])
    Wb0 = Vm * a[None, :]                  # U_{b0} = sum_k Vm[b,k] conj(Vm[0,k]) e^{-iwt}
    W0b = np.conj(Vm) * Vm[0, :][None, :]  # U_{0b}
    dmax = np.zeros(240); dbar = np.zeros(240)
    for s in range(0, len(tt), 2000):
        E = np.exp(-1j * np.outer(w, tt[s:s + 2000]))
        d = np.abs(Wb0 @ E) ** 2 - np.abs(W0b @ E) ** 2
        dmax = np.maximum(dmax, np.abs(d).max(1)); dbar += d.sum(1)
    dbar /= len(tt)
    dmax[0] = 0; dbar[0] = 0
    depth = np.array([0] * 240)
    order = np.argsort(-dmax)
    out["S2"][fam] = {"pairs_with_Dmax_gt_1e-2": int((dmax > 1e-2).sum()), "pairs_with_abs_Dbar_gt_1e-2": int((np.abs(dbar) > 1e-2).sum()),
                      "max_Dmax": float(dmax.max()), "max_abs_Dbar": float(np.abs(dbar).max()),
                      "Dmax_pole_antipode": float(dmax[hc.anti]), "n_pairs": 239,
                      "top5_Dmax": [(int(i), round(float(dmax[i]), 4)) for i in order[:5]]}
    print("S2", fam, out["S2"][fam])
json.dump(out, open(HERE / "outputs" / "eqbit_drift_001_hopping_symmetry.json", "w"), indent=1)
