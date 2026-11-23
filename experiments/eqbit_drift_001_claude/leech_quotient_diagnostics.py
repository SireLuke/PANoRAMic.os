#!/usr/bin/env python3
"""Post-run diagnostics for leech_quotient_extension.py (declared as post-run; not preregistered).
D1: re-evaluate the E8 quotient maxima with the FULL 240x240 matrix at the quotient's argmax times.
    If they agree to ~1e-12 the quotient is right and any Q3 gap is the earlier full run's maxima
    being under-resolved.
D2: exact periodicity at eps = 0 (integer orbit spectrum) for E8 and Leech.
D3: antipode-only transfer peak (single vertex) at several eps for E8 and Leech.
"""
import importlib.util, json, sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from leech_quotient_extension import stats  # noqa

spec = importlib.util.spec_from_file_location("full", HERE / "eqbit_drift_001_claude.py")
full = importlib.util.module_from_spec(spec); spec.loader.exec_module(full)

Q = json.load(open(HERE / "outputs" / "eqbit_drift_001_leech_quotient.json"))
OLD = json.load(open(HERE / "outputs" / "eqbit_drift_001_B_architect.json"))
out = {}

# ---- D1 ----
rows = []
for qr, orr in zip(Q["E8"]["runs"], OLD["runs"]):
    eps = qr["eps"]
    H = full.A + eps * np.diag(full.depth.astype(float))
    w, V = full.eig(H)
    for k in (1, 2, 3):
        m = full.depth == k
        psi = np.zeros(240); psi[m] = 1 / np.sqrt(m.sum())
        tq = qr["arrival"][str(k)]["t"]
        pfull = float(full.prob_series(w, V, psi, np.array([0]), np.array([tq]))[0])
        rows.append({"eps": eps, "k": k, "quotient_A": qr["arrival"][str(k)]["A"], "full_at_quotient_t": pfull,
                     "abs_diff": abs(pfull - qr["arrival"][str(k)]["A"]),
                     "old_refined_A": orr["arrival"][str(k)]["A_refined"],
                     "quotient_minus_old": qr["arrival"][str(k)]["A"] - orr["arrival"][str(k)]["A_refined"]})
out["D1"] = rows
print("D1 full-matrix vs quotient at quotient argmax: worst |diff| =", max(r["abs_diff"] for r in rows))
print("   largest (quotient - old full-run refined):", max(r["quotient_minus_old"] for r in rows),
      " most negative:", min(r["quotient_minus_old"] for r in rows))
for r in rows:
    if abs(r["quotient_minus_old"]) > 1e-6:
        print("   ", r["eps"], r["k"], "quotient", round(r["quotient_A"], 6), "old", round(r["old_refined_A"], 6))

# ---- helpers to rebuild quotient Hamiltonians from saved counts ----
def Hq_from(g):
    cnt = np.array(g["count_matrix"], dtype=float)
    n = np.array(g["orbit_sizes"], dtype=float)
    m = len(n)
    H = np.zeros((m, m))
    for i in range(m):
        for j in range(m):
            H[i, j] = cnt[j, i] * np.sqrt(n[j] / n[i])
    return H, np.array(g["depth_by_orbit"])

# ---- D2 ----
out["D2"] = {}
for name in ("E8", "Leech"):
    g = Q[name]
    H, depth = Hq_from(g)
    w, V = np.linalg.eigh(H)
    ev = np.round(w).astype(int)
    diffs = sorted(set(abs(int(a - b)) for a in ev for b in ev if a != b))
    gcd = int(np.gcd.reduce(diffs))
    period = np.pi / (gcd / 2.0) if gcd else None  # P(t) involves e^{-i dE t}; period 2*pi/gcd
    period = 2 * np.pi / gcd
    m = len(w)
    pole = np.zeros(m); pole[0] = 1.0
    c = V.T @ pole
    t = np.linspace(0, 20, 20001)
    P = lambda tt: np.abs((np.exp(-1j * np.outer(tt, w)) * c[None, :]) @ V[[m - 1], :].T) ** 2
    dper = float(np.abs(P(t) - P(t + period)).max())
    out["D2"][name] = {"eigenvalues": ev.tolist(), "difference_gcd": gcd, "exact_period": period, "max_abs_P_diff_over_period": dper}
    print(f"D2 {name}: eigenvalues {ev.tolist()} gcd of differences {gcd} -> exact period {period:.6f}; max|P(t+T)-P(t)| = {dper:.2e}")

# ---- D3 ----
out["D3"] = {}
for name, eps_list in (("E8", [0.0, 0.25, 0.5, 1.0, 2.0]), ("Leech", [0.0, 0.25, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 50.0, 100.0])):
    g = Q[name]
    H0, depth = Hq_from(g)
    m = len(depth)
    pole = np.zeros(m); pole[0] = 1.0
    out["D3"][name] = []
    print(f"D3 {name}: antipode-only peak P(antipode | start at pole)")
    for eps in eps_list:
        w, V = np.linalg.eigh(H0 + eps * np.diag(depth.astype(float)))
        p, tt, avg = stats(w, V, pole, [m - 1])
        out["D3"][name].append({"eps": eps, "peak": p, "t": tt, "time_avg": avg})
        print(f"   eps={eps:<6} peak={p:.6f} at t={tt:8.3f}  time-avg={avg:.3e}")
json.dump(out, open(HERE / "outputs" / "eqbit_drift_001_leech_diagnostics.json", "w"), indent=1)
