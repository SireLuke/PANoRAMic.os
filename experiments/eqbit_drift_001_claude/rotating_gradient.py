#!/usr/bin/env python3
"""EQBIT-DRIFT-001 extension 5: rotating dipole gradient on the E8 root graph (full 240 x 240).
Architect bench (Claude). Analogy rung only. Closed unitary system.

PREREGISTRATION (frozen in this header BEFORE any run of this script)
---------------------------------------------------------------------
Model      : H(t) = A + eps * [ cos(Omega t) * D1 + sgn * sin(Omega t) * D2 ],  D1 = diag(v . e1), D2 = diag(v . e2),
             e1 = unit vector along the pole root (root 0), e2 = unit vector along a root orthogonal to root 0
             (first such root in the enumeration), v in true coordinates (norm^2 2). The tilt direction rotates
             in the (e1, e2) plane; at t = 0 it points along the pole axis (a well at the pole's side).
Modes      : 'circ'     sgn = +1   rotating gradient (the thing asked about)
             'circ_rev' sgn = -1   opposite rotation sense (chirality control, run for two configurations only)
             'lin'      sgn =  0   breathing along the pole axis only (cos term): separates ROTATION from mere driving
             Omega = 0 is the static dipole gradient eps*D1 (same for every mode).
Grid       : eps in {0.5, 2.0}.  Omega resonant = exact gaps of the integer A-spectrum {-4,-2,8,28,56}: {2,10,12,20,28,32};
             off-resonant controls {0.7, 3.3, 7.7, 15.1, 25.5}; plus static Omega = 0.   T = 200.
Integrator : 4th-order Yoshida composition of Strang splittings, e^{-iV s/2} e^{-iA s} e^{-iV s/2}, with A exponentiated exactly
             (eigh) and V(t) a diagonal phase evaluated at each substep midpoint. Step h = 0.005 (three substeps per step).
             [Header amended BEFORE the first full run: a one-case smoke test at h = 0.01 showed ~1e-5 integrator error over T = 20,
             which would approach the 1e-4 gates over T = 200; h was halved. The smoke test used no registered statistic.]
             Both starts (root 0 and its antipode) are propagated together. Unitary by construction.
Statistics (grid values; peak sampling error at h = 0.005 is bounded by ~4e-4, which is why claim margins are >= 1e-2):
  E = max_t P(antipode | start 0), A = max_t P(0 | start antipode), avgE, avgA (grid time averages),
  Dmax = max_t |P(anti|0) - P(0|anti)|, Dbar = mean_t [P(anti|0) - P(0|anti)].
  Reference (no drive, eps = 0): E = A = 0.882083, avgE = avgA = 0.3633.
Gates (all computed in code):
  RG0 unitarity: column norms within 1e-10 of 1 at the end of every run.
  RG1 static check: Omega = 0 runs equal the exact eigh solution of A + eps*D1 within 1e-4 (max |dP| on the grid), both eps.
  RG2 convergence: 'circ', eps = 2, Omega = 12 at h = 0.005 vs h = 0.0025 differ by < 1e-4 (max |dP| on common grid points).
  RG3 chirality control: 'circ' vs 'circ_rev' give identical P(anti|0) and P(0|anti) series (< 1e-8) at (eps, Omega) = (2, 12)
      and (0.5, 3.3). Reason: the reflection in the root e2 is a graph automorphism that fixes the pole root and its
      antipode and flips D2, so the rotation sense cannot matter for this pair. A violation means an error, not physics.
  RG4 static reciprocity: Omega = 0 gives Dmax < 1e-8 (real symmetric static H).
  RG5 independent solver: DOP853 (rtol 1e-11) on t in [0, 20] for 'circ', eps = 2, Omega = 12 agrees with the splitting
      integrator within 1e-4 for both starts.
Claim rules (conservative; max-over-window is a weak statistic in a small spectrum, so claims use time averages):
  R1 'non-reciprocity' at a driven (eps, Omega, mode): Dmax > 1e-2.
  R2 'rotation-specific effect' at (eps, Omega): |avgE_circ - avgE_lin| > 1e-2 (peak differences > 2e-2 are reported separately).
  R3 'resonant drive-induced enhancement of antipodal transfer' at (eps, Omega, mode) only if avgE exceeds BOTH the static-gradient
      avgE at the same eps AND the largest avgE among that mode's off-resonant controls at the same eps, each by > 1e-2.
  Expectation (registered, not a gate): the time-averaged asymmetry |Dbar| stays small (< 1e-2) for these closed real-symmetric
  drives, i.e. any non-reciprocity is transient timing, not a net current.
  No horizon/gravity language; three depth classes still forbid any exponential-law claim.
"""
import json
import os
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp

import hallway_crosshair as hc

HERE = Path(__file__).resolve().parent
N, ANTI = 240, hc.anti
T_MAX = 200.0
H_STEP = 0.005
EPS_LIST = [0.5, 2.0]
OM_RES = [2.0, 10.0, 12.0, 20.0, 28.0, 32.0]
OM_CTL = [0.7, 3.3, 7.7, 15.1, 25.5]
E1, E2 = hc.N_AX, hc.N_PERP
D1, D2 = hc.V8 @ E1, hc.V8 @ E2
A_MAT = hc.A
WA, VA = np.linalg.eigh(A_MAT)
W1 = 1.0 / (2.0 - 2.0 ** (1.0 / 3.0))
W0 = -(2.0 ** (1.0 / 3.0)) / (2.0 - 2.0 ** (1.0 / 3.0))
_UA = {}


def ua(s):
    k = round(s, 15)
    if k not in _UA:
        _UA[k] = (VA * np.exp(-1j * WA * s)[None, :]) @ VA.T
    return _UA[k]


def propagate(eps, omega, sgn, h=H_STEP, T=T_MAX):
    n = int(round(T / h))
    subs = [W1 * h, W0 * h, W1 * h]
    mats = [ua(s) for s in subs]
    psi = np.zeros((N, 2), dtype=complex)
    psi[0, 0] = 1.0
    psi[ANTI, 1] = 1.0
    PE = np.zeros(n + 1)
    PA = np.zeros(n + 1)
    for step in range(n):
        tau = step * h
        for s, U in zip(subs, mats):
            tm = tau + 0.5 * s
            ph = np.exp(-0.5j * eps * s * (np.cos(omega * tm) * D1 + sgn * np.sin(omega * tm) * D2))[:, None]
            psi = ph * (U @ (ph * psi))
            tau += s
        PE[step + 1] = abs(psi[ANTI, 0]) ** 2
        PA[step + 1] = abs(psi[0, 1]) ** 2
    norm_dev = float(np.abs((np.abs(psi) ** 2).sum(0) - 1.0).max())
    return PE, PA, norm_dev


def stats(PE, PA, h=H_STEP):
    t = np.arange(len(PE)) * h
    return {"E": float(PE.max()), "t_E": float(t[PE.argmax()]), "A": float(PA.max()), "t_A": float(t[PA.argmax()]),
            "avgE": float(PE.mean()), "avgA": float(PA.mean()),
            "Dmax": float(np.abs(PE - PA).max()), "Dbar": float((PE - PA).mean())}


def one(args):
    eps, omega, mode = args
    sgn = {"circ": 1.0, "circ_rev": -1.0, "lin": 0.0}[mode]
    PE, PA, nd = propagate(eps, omega, sgn)
    r = {"eps": eps, "omega": omega, "mode": mode, "norm_dev": nd}
    r.update(stats(PE, PA))
    return r


def static_exact(eps, n, h=H_STEP):
    H = A_MAT + eps * np.diag(D1)
    w, V = np.linalg.eigh(H)
    t = np.arange(n + 1) * h
    out = []
    for start, tgt in ((0, ANTI), (ANTI, 0)):
        c = V[start, :]
        amp = V[tgt, :] @ (np.exp(-1j * np.outer(w, t)) * c[:, None])
        out.append(np.abs(amp) ** 2)
    return out


def dop853(eps, omega, sgn, start, tgt, Tend=20.0):
    def f(t, y):
        V = eps * (np.cos(omega * t) * D1 + sgn * np.sin(omega * t) * D2)
        return -1j * (A_MAT @ y + V * y)
    y0 = np.zeros(N, dtype=complex); y0[start] = 1.0
    t_eval = np.arange(0, Tend + 1e-9, H_STEP)
    sol = solve_ivp(f, [0, Tend], y0, method="DOP853", rtol=1e-11, atol=1e-13, t_eval=t_eval)
    return np.abs(sol.y[tgt]) ** 2


if __name__ == "__main__":
    jobs = []
    for e in EPS_LIST:
        jobs.append((e, 0.0, "lin"))
        for om in OM_RES + OM_CTL:
            jobs.append((e, om, "lin"))
            jobs.append((e, om, "circ"))
    jobs += [(2.0, 12.0, "circ_rev"), (0.5, 3.3, "circ_rev")]
    nproc = max(1, min(os.cpu_count() or 1, 8))
    with ProcessPoolExecutor(nproc) as ex:
        rows = list(ex.map(one, jobs))
    key = {(r["eps"], r["omega"], r["mode"]): r for r in rows}
    gates = {}
    gates["RG0_unitarity"] = bool(max(r["norm_dev"] for r in rows) < 1e-10)
    n = int(round(T_MAX / H_STEP))
    g1 = []
    for e in EPS_LIST:
        PE, PA, _ = propagate(e, 0.0, 0.0)
        xe, xa = static_exact(e, n)
        g1.append(max(float(np.abs(PE - xe).max()), float(np.abs(PA - xa).max())))
    gates["RG1_static_vs_exact_values"] = g1
    gates["RG1_pass"] = bool(max(g1) < 1e-4)
    PEa, PAa, _ = propagate(2.0, 12.0, 1.0, h=0.005)
    PEb, PAb, _ = propagate(2.0, 12.0, 1.0, h=0.0025)
    g2 = max(float(np.abs(PEa - PEb[::2]).max()), float(np.abs(PAa - PAb[::2]).max()))
    gates["RG2_convergence_value"] = g2
    gates["RG2_pass"] = bool(g2 < 1e-4)
    g3 = []
    for (e, om) in ((2.0, 12.0), (0.5, 3.3)):
        P1 = propagate(e, om, 1.0); P2 = propagate(e, om, -1.0)
        g3.append(max(float(np.abs(P1[0] - P2[0]).max()), float(np.abs(P1[1] - P2[1]).max())))
    gates["RG3_chirality_values"] = g3
    gates["RG3_pass"] = bool(max(g3) < 1e-8)
    gates["RG4_static_reciprocity_values"] = [key[(e, 0.0, "lin")]["Dmax"] for e in EPS_LIST]
    gates["RG4_pass"] = bool(max(gates["RG4_static_reciprocity_values"]) < 1e-8)
    d0 = dop853(2.0, 12.0, 1.0, 0, ANTI); d1_ = dop853(2.0, 12.0, 1.0, ANTI, 0)
    m = len(d0)
    g5 = max(float(np.abs(PEa[:m] - d0).max()), float(np.abs(PAa[:m] - d1_).max()))
    gates["RG5_dop853_value"] = g5
    gates["RG5_pass"] = bool(g5 < 1e-4)
    # claims
    for e in EPS_LIST:
        stat = key[(e, 0.0, "lin")]["avgE"]
        for mode in ("lin", "circ"):
            ctl = max(key[(e, om, mode)]["avgE"] for om in OM_CTL)
            for om in OM_RES + OM_CTL:
                r = key[(e, om, mode)]
                r["R1_nonreciprocity"] = bool(r["Dmax"] > 1e-2)
                r["R3_resonant_enhancement"] = bool(om in OM_RES and r["avgE"] > stat + 1e-2 and r["avgE"] > ctl + 1e-2)
        for om in OM_RES + OM_CTL:
            c, l = key[(e, om, "circ")], key[(e, om, "lin")]
            c["R2_rotation_specific_avg"] = bool(abs(c["avgE"] - l["avgE"]) > 1e-2)
            c["R2_peak_diff_gt_2e-2"] = bool(abs(c["E"] - l["E"]) > 2e-2)
    res = {"gates": gates, "rows": rows}
    json.dump(res, open(HERE / "outputs" / "eqbit_drift_001_rotating.json", "w"), indent=1,
              default=lambda o: bool(o) if isinstance(o, np.bool_) else float(o))
    print("GATES", gates)
    for e in EPS_LIST:
        print(f"\n== eps = {e}  static: E={key[(e,0.0,'lin')]['E']:.4f} avgE={key[(e,0.0,'lin')]['avgE']:.4f} ==")
        print("Omega kind | lin: E avgE Dmax Dbar        | circ: E avgE Dmax Dbar         | R2avg R2peak R3lin R3circ")
        for om in OM_RES + OM_CTL:
            l, c = key[(e, om, "lin")], key[(e, om, "circ")]
            kind = "res" if om in OM_RES else "ctl"
            print(f"{om:>5} {kind} | {l['E']:.4f} {l['avgE']:.4f} {l['Dmax']:.4f} {l['Dbar']:+.1e} | {c['E']:.4f} {c['avgE']:.4f} {c['Dmax']:.4f} {c['Dbar']:+.1e} | "
                  f"{c['R2_rotation_specific_avg']!s:5} {c['R2_peak_diff_gt_2e-2']!s:5} {l['R3_resonant_enhancement']!s:5} {c['R3_resonant_enhancement']!s:5}")
