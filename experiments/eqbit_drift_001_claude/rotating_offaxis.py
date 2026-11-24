#!/usr/bin/env python3
"""EQBIT-DRIFT-001 extension 6: rotating dipole gradient from OFF-AXIS starts (E8, full 240 x 240).
Architect bench (Claude). Analogy rung only. Closed unitary system.

PREREGISTRATION (frozen in this header BEFORE any run of this script)
---------------------------------------------------------------------
Why        : rotating_gradient.py proved (gate RG3) that the rotation sense cannot matter for the pole/antipode pair, because
             the reflection S in the root r2 (the root defining the second tilt axis) is a graph automorphism that fixes root 0
             and its antipode and flips D2. An off-axis start is the only place a sense-dependence (chirality) can show.
Model      : H(t) = A + eps*[cos(Omega t + phi) D1 + sgn * sin(Omega t + phi) D2]  (same D1, D2 as rotating_gradient.py,
             same integrator and step h = 0.005, T = 200). Modes: circ (sgn = +1), rev (sgn = -1), lin (sgn = 0, cos term only).
Mirror pair: S(x) = x - (x.r2) r2 / 4 in scaled integer coordinates (norm^2 8). For a start root a with a.r2 != 0, S(a) != a.
             Because S H_circ(t) S^-1 = H_rev(t):  P_rev(b|a) = P_circ(S b | S a).  Hence for the mirror pair (a, S a):
             P_rev(S a | a) = P_circ(a | S a), i.e. reversing the rotation reverses the sign of the pair asymmetry exactly.
             For lin (no D2) S commutes with H(t), so P(S a | a) = P(a | S a) exactly.
Starts     : a1 = first root with scaled dot 4 with root 0 (a pole neighbour) and a.r2 != 0;
             a2 = first root with scaled dot 0 with root 0 and a.r2 != 0.  Each run propagates a and S a together.
Grid       : eps in {0.5, 2.0}; Omega in {2.0, 7.7, 12.0}; phi in {k*pi/4, k = 0..7}  (circ);  lin at phi = 0 for every
             (start, eps, Omega).  Extra runs: rev at (a1, 2, 12, phi 0) and (a2, 0.5, 7.7, phi 0); start -a1 at (2, 12) for
             all 8 phi; one h/2 = 0.0025 convergence run at (a1, 2, 12, circ, phi 0).
Statistics per run (grid): PE(t) = P(S a | a), PA(t) = P(a | S a);  Dmax = max|PE - PA|;  Dbar = mean(PE - PA).
  Per (start, eps, Omega): the phi-mean of Dbar over the 8 phases ('intrinsic' part), and max_phi |Dbar|.
Gates (all computed in code):
  OG1 structure: S is a root-lattice automorphism (adjacency preserved), fixes root 0 and its antipode, flips D2 and fixes D1
      (< 1e-12), and S a != a for both starts.
  OG2 lin symmetry: every lin run has max|PE - PA| < 1e-8.
  OG3 chirality identity: P_rev(S a | a) series == P_circ(a | S a) series and P_rev(a | S a) == P_circ(S a | a), within 1e-8,
      at the two rev configurations.
  OG4 convergence: h = 0.005 vs 0.0025 at the convergence run differ by < 1e-4 (max |dP| on common grid points).
  OG5 antipodal relation: Dbar_{-a1}(phi) == Dbar_{a1}(phi + pi) for all 8 phases at (eps, Omega) = (2, 12), within 1e-8
      (the antipodal map sends H(phi) to H(phi + pi) and the pair (a, S a) to (-a, S(-a))).
Claim rules (conservative; time averages, margin 1e-2):
  C1 'rotation-sense-dependent transport' at (start, eps, Omega, phi) only if |Dbar| > 1e-2 (rev then gives -Dbar by OG3).
  C2 'phase-independent (intrinsic) chirality' at (start, eps, Omega) only if |phi-mean of Dbar| > 1e-2.
  No prediction is registered for the size or sign of either; the on-axis analogue (drive-phase flip of Dbar, rotating_diag X2)
  suggests C1 can fire while C2 does not, but the mirror pair has no such guaranteed cancellation (OG5 relates a to -a, not a to a).
  No horizon/gravity language; three depth classes still forbid any exponential-law claim.
"""
import json
import os
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import numpy as np

import rotating_gradient as rg
import hallway_crosshair as hc

HERE = Path(__file__).resolve().parent
X = hc.X
KEY = {tuple(r): i for i, r in enumerate(X)}
R2 = X[hc.perp_root]
ANTI = hc.anti


def mirror_index(i):
    x = X[i]
    y = x - ((x @ R2) // 4) * R2
    return KEY[tuple(y)]


SIDX = np.array([mirror_index(i) for i in range(240)])
NEG = np.array([KEY[tuple(-r)] for r in X])


def pick_starts():
    a1 = next(i for i in range(240) if X[i] @ X[0] == 4 and X[i] @ R2 != 0)
    a2 = next(i for i in range(240) if X[i] @ X[0] == 0 and X[i] @ R2 != 0)
    return a1, a2


A1, A2 = pick_starts()
EPS_LIST = [0.5, 2.0]
OMEGAS = [2.0, 7.7, 12.0]
PHIS = [k * np.pi / 4 for k in range(8)]


def propagate(a, eps, omega, sgn, phi, h=0.005, T=200.0):
    sa = int(SIDX[a])
    n = int(round(T / h))
    subs = [rg.W1 * h, rg.W0 * h, rg.W1 * h]
    mats = [rg.ua(s) for s in subs]
    psi = np.zeros((240, 2), dtype=complex)
    psi[a, 0] = 1.0
    psi[sa, 1] = 1.0
    PE = np.zeros(n + 1)
    PA = np.zeros(n + 1)
    for step in range(n):
        tau = step * h
        for s, U in zip(subs, mats):
            tm = tau + 0.5 * s
            ang = omega * tm + phi
            ph = np.exp(-0.5j * eps * s * (np.cos(ang) * rg.D1 + sgn * np.sin(ang) * rg.D2))[:, None]
            psi = ph * (U @ (ph * psi))
            tau += s
        PE[step + 1] = abs(psi[sa, 0]) ** 2
        PA[step + 1] = abs(psi[a, 1]) ** 2
    return PE, PA


def job(args):
    a, eps, om, mode, phi, h = args
    sgn = {"circ": 1.0, "rev": -1.0, "lin": 0.0}[mode]
    PE, PA = propagate(a, eps, om, sgn, phi, h=h)
    return args, PE, PA


if __name__ == "__main__":
    gates = {}
    # OG1 structure
    Aperm_ok = bool(np.array_equal(hc.A[np.ix_(SIDX, SIDX)], hc.A))
    d2 = hc.V8 @ hc.N_PERP
    d1 = hc.V8 @ hc.N_AX
    og1 = {"adjacency_preserved": Aperm_ok, "fixes_root0": bool(SIDX[0] == 0), "fixes_antipode": bool(SIDX[ANTI] == ANTI),
           "D2_flipped_dev": float(np.abs(d2[SIDX] + d2).max()), "D1_fixed_dev": float(np.abs(d1[SIDX] - d1).max()),
           "a1": int(A1), "a2": int(A2), "S_a1_ne_a1": bool(SIDX[A1] != A1), "S_a2_ne_a2": bool(SIDX[A2] != A2)}
    gates["OG1_structure"] = og1
    gates["OG1_pass"] = bool(Aperm_ok and og1["fixes_root0"] and og1["fixes_antipode"] and og1["D2_flipped_dev"] < 1e-12
                             and og1["D1_fixed_dev"] < 1e-12 and og1["S_a1_ne_a1"] and og1["S_a2_ne_a2"])
    print("OG1", og1, gates["OG1_pass"], flush=True)
    jobs = []
    for a in (A1, A2):
        for e in EPS_LIST:
            for om in OMEGAS:
                jobs.append((a, e, om, "lin", 0.0, 0.005))
                for phi in PHIS:
                    jobs.append((a, e, om, "circ", float(phi), 0.005))
    jobs += [(A1, 2.0, 12.0, "rev", 0.0, 0.005), (A2, 0.5, 7.7, "rev", 0.0, 0.005), (A1, 2.0, 12.0, "circ", 0.0, 0.0025)]
    na1 = int(NEG[A1])
    for phi in PHIS:
        jobs.append((na1, 2.0, 12.0, "circ", float(phi), 0.005))
    print("jobs", len(jobs), flush=True)
    nproc = max(1, min(os.cpu_count() or 1, 8))
    res = {}
    with ProcessPoolExecutor(nproc) as ex:
        for k, (args, PE, PA) in enumerate(ex.map(job, jobs)):
            res[args] = (PE, PA)
            if k % 10 == 0:
                print("done", k + 1, "/", len(jobs), flush=True)
    rows = []
    for (a, e, om, mode, phi, h), (PE, PA) in res.items():
        if h != 0.005:
            continue
        rows.append({"start": int(a), "eps": e, "omega": om, "mode": mode, "phi": phi, "Dmax": float(np.abs(PE - PA).max()),
                     "Dbar": float((PE - PA).mean()), "avgE": float(PE.mean()), "avgA": float(PA.mean())})
    # OG2
    lin = [r for r in rows if r["mode"] == "lin"]
    gates["OG2_lin_max_asym"] = float(max(r["Dmax"] for r in lin))
    gates["OG2_pass"] = bool(gates["OG2_lin_max_asym"] < 1e-8)
    # OG3
    og3 = []
    for (a, e, om) in ((A1, 2.0, 12.0), (A2, 0.5, 7.7)):
        PEc, PAc = res[(a, e, om, "circ", 0.0, 0.005)]
        PEr, PAr = res[(a, e, om, "rev", 0.0, 0.005)]
        og3.append(max(float(np.abs(PEr - PAc).max()), float(np.abs(PAr - PEc).max())))
    gates["OG3_values"] = og3
    gates["OG3_pass"] = bool(max(og3) < 1e-8)
    # OG4
    PEh, PAh = res[(A1, 2.0, 12.0, "circ", 0.0, 0.005)]
    PEq, PAq = res[(A1, 2.0, 12.0, "circ", 0.0, 0.0025)]
    gates["OG4_value"] = max(float(np.abs(PEh - PEq[::2]).max()), float(np.abs(PAh - PAq[::2]).max()))
    gates["OG4_pass"] = bool(gates["OG4_value"] < 1e-4)
    # OG5
    og5 = []
    for k, phi in enumerate(PHIS):
        r_neg = next(r for r in rows if r["start"] == na1 and r["mode"] == "circ" and abs(r["phi"] - phi) < 1e-12)
        r_pos = next(r for r in rows if r["start"] == A1 and r["eps"] == 2.0 and r["omega"] == 12.0 and r["mode"] == "circ"
                     and abs(r["phi"] - PHIS[(k + 4) % 8]) < 1e-12)
        og5.append(abs(r_neg["Dbar"] - r_pos["Dbar"]))
    gates["OG5_values"] = og5
    gates["OG5_pass"] = bool(max(og5) < 1e-8)
    # claims
    summary = []
    for a in (A1, A2):
        for e in EPS_LIST:
            for om in OMEGAS:
                cs = [r for r in rows if r["start"] == a and r["eps"] == e and r["omega"] == om and r["mode"] == "circ"]
                for r in cs:
                    r["C1_sense_dependent"] = bool(abs(r["Dbar"]) > 1e-2)
                mean = float(np.mean([r["Dbar"] for r in cs]))
                summary.append({"start": int(a), "eps": e, "omega": om, "phi_mean_Dbar": mean,
                                "max_abs_Dbar": float(max(abs(r["Dbar"]) for r in cs)),
                                "n_phases_C1": int(sum(r["C1_sense_dependent"] for r in cs)),
                                "C2_intrinsic": bool(abs(mean) > 1e-2),
                                "Dbar_by_phi": [round(r["Dbar"], 4) for r in sorted(cs, key=lambda x: x["phi"])]})
    out = {"gates": gates, "summary": summary, "rows": rows}
    json.dump(out, open(HERE / "outputs" / "eqbit_drift_001_offaxis.json", "w"), indent=1,
              default=lambda o: bool(o) if isinstance(o, np.bool_) else float(o))
    print("\nGATES", {k: v for k, v in gates.items() if k != "OG1_structure"})
    print("\nstart eps  Omega | phi-mean Dbar | max|Dbar| | #phases>1e-2 | C2 | Dbar by phi (k*pi/4)")
    for s in summary:
        print(f"{s['start']:>4} {s['eps']:<4} {s['omega']:<5} | {s['phi_mean_Dbar']:+.4f} | {s['max_abs_Dbar']:.4f} | {s['n_phases_C1']} | {s['C2_intrinsic']!s:5} | {s['Dbar_by_phi']}")
