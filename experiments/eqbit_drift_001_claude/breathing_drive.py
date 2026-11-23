#!/usr/bin/env python3
"""EQBIT-DRIFT-001 extension 2: radial breathing drive with sign flip, E8 pole-orbit quotient.
Architect bench (Claude). Analogy rung only. Closed unitary system.

PREREGISTRATION (frozen in this header BEFORE any run of this script)
---------------------------------------------------------------------
Model      : H(t) = A_q + eps0 * cos(Omega t) * diag(depth), 5x5 orbit quotient of the E8 root graph
             around pole root 0 (sizes 1,56,126,56,1; depth 0,1,2,2,3). cos flips sign every half
             cycle: pole alternates between well (inward) and hill (outward). t=0 is a well.
             Counts/orbit matrix are taken from outputs/eqbit_drift_001_leech_quotient.json (E8 block),
             which was verified against the full 240x240 matrix (5e-14).
Integrator : scipy DOP853, rtol=1e-10, atol=1e-12, dense output sampled at dt=0.001 on [0,200].
Drive grid : eps0 in {0.25, 1.0}.
             Omega resonant = every exact gap of the integer eps=0 spectrum {-4,-2,8,28,56}:
             {2,10,12,20,28,30,32,48,58,60}.  Omega off-resonant controls: {0.7,3.3,7.7,15.1,25.5,45.5}.
             Omega = 0 is the static control (cos=1).
Starts     : pole (leak-out) and antipode (drift-in); single vertices.
Registered statistics, per (eps0, Omega):
  E      = max_t P(antipode | start pole)          (outward transfer peak)
  A      = max_t P(pole | start antipode)          (inward transfer peak)
  Dmax   = max_t | P(antipode|pole) - P(pole|antipode) |   (inward/outward asymmetry; exactly 0 for
           any static real symmetric H, so nonzero Dmax is a time-dependence effect)
  avgE   = time average of P(antipode | start pole)
Baselines  : static eps=0 antipode peak 0.882083 (ceiling at zero tilt); static eps=eps0 peaks from
             the existing tables.
Gates      : G0 norm conservation |norm-1| < 1e-8 for every run.
             G1 Omega=0 control: Dmax < 1e-8 (static reciprocity) and E equals the static-eps0 value
                from outputs/eqbit_drift_001_leech_quotient.json (E8 antipode, eps0 in {0.25,1.0}) within 2e-3.
             G2 solver check: one run (eps0=1.0, Omega=12, start pole) repeated at rtol=1e-12 must
                give the same E within 1e-6.
Claim rules: "resonant enhancement" is claimed only for E or A exceeding the static eps=0 ceiling
             0.882083 by more than 5e-3 AND exceeding the eps0-matched off-resonant controls' maximum.
             "Asymmetry" is claimed only for Dmax > 1e-3 and must be reported with the (eps0, Omega).
             Peaks are dt=0.001 grid maxima (not refined); fast components can make the grid max
             understate the true max by roughly 1e-3 or less; differences below that are not claims.
             No horizon/gravity language; no exponential-law claim (three depth classes).
"""
import json
import os
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp

HERE = Path(__file__).resolve().parent
T_MAX, DT = 200.0, 0.001
EPS0 = [0.25, 1.0]
OMEGA_RES = [2, 10, 12, 20, 28, 30, 32, 48, 58, 60]
OMEGA_CTL = [0.7, 3.3, 7.7, 15.1, 25.5, 45.5]
OMEGAS = [0.0] + OMEGA_RES + OMEGA_CTL


def load_quotient():
    Q = json.load(open(HERE / "outputs" / "eqbit_drift_001_leech_quotient.json"))
    g = Q["E8"]
    cnt = np.array(g["count_matrix"], dtype=float)
    n = np.array(g["orbit_sizes"], dtype=float)
    m = len(n)
    H = np.zeros((m, m))
    for i in range(m):
        for j in range(m):
            H[i, j] = cnt[j, i] * np.sqrt(n[j] / n[i])
    return H, np.array(g["depth_by_orbit"], dtype=float), Q


def evolve(eps0, omega, start, rtol=1e-10):
    H, D, _ = load_quotient()
    m = len(D)
    y0 = np.zeros(m, dtype=complex)
    y0[start] = 1.0
    f = lambda t, y: -1j * (H @ y + eps0 * np.cos(omega * t) * D * y)
    sol = solve_ivp(f, [0, T_MAX], y0, method="DOP853", rtol=rtol, atol=1e-12, dense_output=True)
    t = np.arange(0, T_MAX + 1e-9, DT)
    Y = sol.sol(t)
    P = np.abs(Y) ** 2
    return t, P


def one(args):
    eps0, omega = args
    m = 5
    t, Pp = evolve(eps0, omega, 0)        # start at pole
    _, Pa = evolve(eps0, omega, m - 1)    # start at antipode
    norm_dev = float(max(abs(Pp.sum(0) - 1).max(), abs(Pa.sum(0) - 1).max()))
    out_ = Pp[m - 1]                      # P(antipode | pole)
    in_ = Pa[0]                           # P(pole | antipode)
    return {"eps0": eps0, "omega": omega, "E": float(out_.max()), "t_E": float(t[out_.argmax()]),
            "A": float(in_.max()), "t_A": float(t[in_.argmax()]),
            "Dmax": float(np.abs(out_ - in_).max()), "avgE": float(out_.mean()), "norm_dev": norm_dev}


if __name__ == "__main__":
    H, D, Q = load_quotient()
    diag = json.load(open(HERE / "outputs" / "eqbit_drift_001_leech_diagnostics.json"))["D3"]["E8"]
    static_peak = {r["eps"]: r["peak"] for r in diag}
    jobs = [(e, o) for e in EPS0 for o in OMEGAS]
    nproc = max(1, min(os.cpu_count() or 1, 8))
    with ProcessPoolExecutor(nproc) as ex:
        rows = list(ex.map(one, jobs))
    # G2 solver check
    t1, P1 = evolve(1.0, 12.0, 0, rtol=1e-10)
    t2, P2 = evolve(1.0, 12.0, 0, rtol=1e-12)
    g2 = float(abs(P1[4].max() - P2[4].max()))
    gates = {"G0_norm": bool(max(r["norm_dev"] for r in rows) < 1e-8),
             "G1_static_reciprocity": bool(all(r["Dmax"] < 1e-8 for r in rows if r["omega"] == 0.0)),
             "G1_static_value": bool(all(abs(r["E"] - static_peak[r["eps0"]]) < 2e-3 for r in rows if r["omega"] == 0.0)),
             "G2_solver_diff": g2, "G2_pass": bool(g2 < 1e-6)}
    ceiling = 0.882083
    verdicts = []
    for e in EPS0:
        ctl = [r for r in rows if r["eps0"] == e and r["omega"] in OMEGA_CTL]
        ctlmax = max(max(r["E"], r["A"]) for r in ctl)
        for r in rows:
            if r["eps0"] != e:
                continue
            best = max(r["E"], r["A"])
            r["resonant_enhancement_claim"] = bool(r["omega"] in OMEGA_RES and best > ceiling + 5e-3 and best > ctlmax)
            r["asymmetry_claim"] = bool(r["Dmax"] > 1e-3)
    res = {"gates": gates, "static_peaks_E8": static_peak, "ceiling_eps0": ceiling, "rows": rows}
    json.dump(res, open(HERE / "outputs" / "eqbit_drift_001_breathing.json", "w"), indent=1)
    print("GATES", gates)
    print("static antipode peaks:", static_peak)
    for e in EPS0:
        print(f"\n== eps0 = {e} ==   Omega |   E (out)    t_E |   A (in)    t_A |  Dmax   | avgE  | res-claim asym-claim")
        for r in rows:
            if r["eps0"] != e:
                continue
            tag = "gap" if r["omega"] in OMEGA_RES else ("static" if r["omega"] == 0 else "ctl")
            print(f"  {r['omega']:>5} {tag:6s} | {r['E']:.4f} {r['t_E']:7.2f} | {r['A']:.4f} {r['t_A']:7.2f} | {r['Dmax']:.4f} | {r['avgE']:.4f} | {r['resonant_enhancement_claim']!s:5} {r['asymmetry_claim']}")
