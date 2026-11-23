#!/usr/bin/env python3
"""EQBIT-DRIFT-001 extension 3: a 'crosshair' hallway through 0^8 on the E8 root graph.
Architect bench (Claude). Analogy rung only. Closed unitary system, exact diagonalization.

PREREGISTRATION (frozen in this header BEFORE any run of this script)
---------------------------------------------------------------------
Idea       : Experiment A coupled the origin uniformly (an EVEN pattern under v -> -v), so it could
             never mediate antipodal transfer. Here the origin couples with an ODD pattern: signed
             strength proportional to the root's coordinate along an axis n through 0^8:
                 c_v = g * (v . n),  v in true coordinates (norm^2 2),  n = unit vector along root 0.
             Hamiltonian H = A + E0|0><0| + sum_v c_v (|0><v| + h.c.).   241 x 241, exact eigh.
Exact facts that are GATED, not assumed:
  H1  A d = 28 d for d_v = v.n  (coordinate functions are an 8-dim eigenspace, eigenvalue 28). Tol 1e-10.
  H2  sum_v (v.n)^2 = 60, so V = ||c|| = g*sqrt(60).
  H3  {d/sqrt60, |0>} is an invariant two-level system with detuning Delta = 28 - E0. Starting from
      the single root 0: |<d_hat|v0>|^2 = 1/30, so P_origin(t) = (1/30) * P_two(t) EXACTLY
      (grid max abs diff < 1e-12), and the two-level peak (start d_hat) is V^2/(V^2 + (Delta/2)^2)
      (refined, tol 1e-6); full transfer (>= 1 - 1e-9) when E0 = 28.
  H4  Odd/even dark control: the even state (|v0>+|-v0>)/sqrt2 is orthogonal to d, so P_origin == 0
      (< 1e-12) at every (g, E0) in the hallway configuration.
Configurations (same ||c|| = g*sqrt60 in all three so only the PATTERN differs):
  hall : n along the pole root 0 (aligned axis through the pole and its antipode).
  uni  : c_v = g*sqrt(60/240) for all v (Experiment A pattern; even).
  perp : n along a root orthogonal to root 0 (axis that does not pass through the pole).
Grid       : g in {0.1, 0.25, 0.5, 1.0};  E0 in {0, 28, 56};  baseline g = 0.
Window/grid: t in [0,200], dt = 0.005 plus local refinement of maxima.
Registered statistics (start at root 0, single vertex):
  Tpk  = max_t P(antipode of root 0)   (compare with the baseline value at g = 0, 0.882083)
  Tavg = time average of P(antipode)   (baseline 0.3633)
  Opk  = max_t P(origin)
Claim rules (conservative; max-over-window is a weak statistic in small state spaces, learned from the
breathing-drive run, so the time average is registered alongside):
  'Hallway enhancement' of antipodal transfer at (g,E0) is claimed ONLY IF hall Tpk exceeds the g=0
  baseline by > 5e-3 AND exceeds both uni and perp Tpk at the same (g,E0) by > 5e-3 AND hall Tavg
  exceeds both controls' Tavg at the same (g,E0). Otherwise no claim; the rows are reported as found.
  No horizon/gravity language. 0^8 here means exactly the adjoined origin node.
"""
import itertools, json
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
T_MAX, DT = 200.0, 0.005
G_LIST = [0.1, 0.25, 0.5, 1.0]
E0_LIST = [0.0, 28.0, 56.0]


def e8_vectors():
    R = []
    for i, j in itertools.combinations(range(8), 2):
        for si in (2, -2):
            for sj in (2, -2):
                v = [0] * 8
                v[i], v[j] = si, sj
                R.append(v)
    for s in itertools.product((1, -1), repeat=8):
        if s.count(-1) % 2 == 0:
            R.append(list(s))
    return np.array(R, dtype=np.int64)


X = e8_vectors()
A = ((X @ X.T) == 4).astype(float)
V8 = X / 2.0                                   # true coordinates, norm^2 2
anti = int(np.nonzero(X @ X[0] == -8)[0][0])
perp_root = int(np.nonzero(X @ X[0] == 0)[0][0])
N_AX = V8[0] / np.linalg.norm(V8[0])
N_PERP = V8[perp_root] / np.linalg.norm(V8[perp_root])


def hamiltonian(c, E0):
    H = np.zeros((241, 241))
    H[:240, :240] = A
    H[240, 240] = E0
    H[240, :240] = c
    H[:240, 240] = c
    return H


def amp_rows(w, Vm, psi, rows, t, chunk=5000):
    c = Vm.T @ psi
    out = np.empty((len(rows), len(t)), dtype=complex)
    for s in range(0, len(t), chunk):
        tt = t[s:s + chunk]
        out[:, s:s + chunk] = Vm[rows, :] @ (np.exp(-1j * np.outer(w, tt)) * c[:, None])
    return out


def peak_refined(w, Vm, psi, rows, half=0.02):
    t = np.arange(0, T_MAX + 1e-9, DT)
    P = (np.abs(amp_rows(w, Vm, psi, rows, t)) ** 2).sum(0)
    i = int(P.argmax())
    f = lambda tt: (np.abs(amp_rows(w, Vm, psi, rows, tt)) ** 2).sum(0)
    ts = np.linspace(max(t[i] - half, 0), min(t[i] + half, T_MAX), 201)
    v = f(ts); j = int(v.argmax())
    lo, hi = ts[max(j - 1, 0)], ts[min(j + 1, 200)]
    for _ in range(60):
        m1, m2 = lo + (hi - lo) / 3, hi - (hi - lo) / 3
        if f(np.array([m1]))[0] < f(np.array([m2]))[0]:
            lo = m1
        else:
            hi = m2
    tr = 0.5 * (lo + hi); pr = float(f(np.array([tr]))[0])
    return max(pr, float(P.max())), float(tr if pr >= P.max() else t[i]), float(P.mean()), P, t


def run_config(kind, g, E0):
    if kind == "hall":
        c = g * (V8 @ N_AX)
    elif kind == "perp":
        c = g * (V8 @ N_PERP)
    else:
        c = np.full(240, g * np.sqrt(60.0 / 240.0))
    H = hamiltonian(c, E0)
    w, Vm = np.linalg.eigh(H)
    psi = np.zeros(241); psi[0] = 1.0
    Tpk, tT, Tavg, Pt, t = peak_refined(w, Vm, psi, [anti])
    Opk, tO, _, Po, _ = peak_refined(w, Vm, psi, [240])
    return {"kind": kind, "g": g, "E0": E0, "Tpk": Tpk, "t_Tpk": tT, "Tavg": Tavg, "Opk": Opk, "t_Opk": tO}, (w, Vm, Po, t)


if __name__ == "__main__":
    d = V8 @ N_AX
    gates = {}
    gates["H1_dipole_eigen28"] = bool(np.abs(A @ d - 28 * d).max() < 1e-10)
    gates["H2_norm60"] = bool(abs((d ** 2).sum() - 60.0) < 1e-10)
    dhat = d / np.sqrt(60.0)
    h3 = []; h4 = []
    for g in G_LIST:
        for E0 in E0_LIST:
            c = g * d
            H = hamiltonian(c, E0)
            w, Vm = np.linalg.eigh(H)
            t = np.arange(0, T_MAX + 1e-9, DT)
            single = np.zeros(241); single[0] = 1.0
            two = np.zeros(241); two[:240] = dhat
            Pone = (np.abs(amp_rows(w, Vm, single, [240], t)) ** 2).sum(0)
            Ptwo = (np.abs(amp_rows(w, Vm, two, [240], t)) ** 2).sum(0)
            diff = float(np.abs(Pone - Ptwo / 30.0).max())
            Vc = g * np.sqrt(60.0); half_delta = abs(28.0 - E0) / 2
            pred = Vc ** 2 / (Vc ** 2 + half_delta ** 2)
            ptwo_ref, _, _, _, _ = peak_refined(w, Vm, two, [240])
            even = np.zeros(241); even[0] = even[anti] = 1 / np.sqrt(2)
            Peven = (np.abs(amp_rows(w, Vm, even, [240], t)) ** 2).sum(0)
            h3.append({"g": g, "E0": E0, "single_vs_two_over_30_maxdiff": diff, "two_level_peak": ptwo_ref, "pred": pred,
                       "err": abs(ptwo_ref - pred)})
            h4.append(float(Peven.max()))
    gates["H3_single_equals_two_level_over_30"] = bool(all(r["single_vs_two_over_30_maxdiff"] < 1e-12 for r in h3))
    gates["H3_two_level_peak_formula"] = bool(all(r["err"] < 1e-6 for r in h3))
    gates["H3_full_transfer_at_E0_28"] = bool(all(r["two_level_peak"] >= 1 - 1e-9 for r in h3 if r["E0"] == 28.0))
    gates["H4_even_state_dark"] = bool(max(h4) < 1e-12)
    # baseline g=0 (origin decoupled)
    Hb = hamiltonian(np.zeros(240), 0.0)
    wb, Vb = np.linalg.eigh(Hb)
    psi = np.zeros(241); psi[0] = 1.0
    base_pk, base_t, base_avg, _, _ = peak_refined(wb, Vb, psi, [anti])
    rows = []
    for g in G_LIST:
        for E0 in E0_LIST:
            trio = {}
            for kind in ("hall", "uni", "perp"):
                r, _ = run_config(kind, g, E0)
                trio[kind] = r; rows.append(r)
            h, u, p = trio["hall"], trio["uni"], trio["perp"]
            claim = bool(h["Tpk"] > base_pk + 5e-3 and h["Tpk"] > max(u["Tpk"], p["Tpk"]) + 5e-3 and h["Tavg"] > max(u["Tavg"], p["Tavg"]))
            for r in trio.values():
                r["hallway_enhancement_claim_at_this_gE0"] = claim
    res = {"gates": gates, "baseline_g0": {"Tpk": base_pk, "t": base_t, "Tavg": base_avg}, "H3": h3, "rows": rows}
    json.dump(res, open(HERE / "outputs" / "eqbit_drift_001_hallway.json", "w"), indent=1, default=lambda o: bool(o) if isinstance(o, np.bool_) else float(o))
    print("GATES", gates)
    print(f"baseline g=0: Tpk={base_pk:.6f} Tavg={base_avg:.4f}")
    print("g     E0 | hall Tpk  Tavg   Opk   | uni Tpk  Tavg   Opk   | perp Tpk  Tavg   Opk   | claim")
    for g in G_LIST:
        for E0 in E0_LIST:
            tr = {r["kind"]: r for r in rows if r["g"] == g and r["E0"] == E0}
            s = " | ".join(f"{tr[k]['Tpk']:.4f} {tr[k]['Tavg']:.4f} {tr[k]['Opk']:.4f}" for k in ("hall", "uni", "perp"))
            print(f"{g:<5} {E0:>4} | {s} | {tr['hall']['hallway_enhancement_claim_at_this_gE0']}")
