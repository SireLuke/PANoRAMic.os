#!/usr/bin/env python3
"""EQBIT-DRIFT-001 -- independent implementation (Architect bench), written from the spec only.
Deterministic, no randomness. numpy only.
Includes the review amendments: refined maxima, equality gate for P4, reciprocity gate,
5-orbit quotient cross-check, time-of-max, window-free time average, PR #117 regression.
"""
import itertools, json
import numpy as np

T_MAX = 200.0
DT = 0.05

# ---------------- Gosset graph ----------------
def build_roots():
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

R = build_roots()
assert R.shape == (240, 8) and set((R * R).sum(1)) == {8}
D = R @ R.T
A = (D == 4).astype(float)
assert set(A.sum(1)) == {56.0} and int(A.sum() // 2) == 6720

# BFS depth from pole = root 0
depth = np.full(240, -1)
depth[0] = 0
frontier = [0]
d = 0
while frontier:
    d += 1
    nxt = []
    for u in frontier:
        for v in np.nonzero(A[u])[0]:
            if depth[v] < 0:
                depth[v] = d
                nxt.append(v)
    frontier = nxt
shells = [int((depth == k).sum()) for k in range(4)]
assert shells == [1, 56, 182, 1], shells

# ---------------- propagation helpers ----------------
def eig(H):
    return np.linalg.eigh(H)

def prob_series(w, V, psi, sel, t, chunk=4000):
    """total probability on index set `sel` at times t, for exact U(t)=exp(-iHt)."""
    c = V.T @ psi
    out = np.empty(len(t))
    for s in range(0, len(t), chunk):
        tt = t[s:s + chunk]
        phase = np.exp(-1j * np.outer(w, tt)) * c[:, None]
        amp = V[sel, :] @ phase
        out[s:s + chunk] = (np.abs(amp) ** 2).sum(0)
    return out

def refine_max(f, t0, half, lo_b=0.0, hi_b=T_MAX):
    ts = np.linspace(max(t0 - half, lo_b), min(t0 + half, hi_b), 401)
    v = f(ts)
    i = int(v.argmax())
    lo, hi = ts[max(i - 1, 0)], ts[min(i + 1, 400)]
    for _ in range(70):
        m1 = lo + (hi - lo) / 3
        m2 = hi - (hi - lo) / 3
        if f(np.array([m1]))[0] < f(np.array([m2]))[0]:
            lo = m1
        else:
            hi = m2
    t = 0.5 * (lo + hi)
    return float(t), float(f(np.array([t]))[0])

TGRID = np.arange(0, T_MAX + 1e-9, DT)          # spec grid
TFINE = np.arange(0, T_MAX + 1e-9, 0.01)        # registered fine grid (review amendment)

# ======================================================================
# Experiment A
# ======================================================================
def exp_A():
    out = {"experiment": "A-drain", "runs": [], "gates": {}}
    N = 241
    sym = np.zeros(N); sym[:240] = 1 / np.sqrt(240)
    single = np.zeros(N); single[0] = 1.0
    null = np.zeros(N); null[0] = 1 / np.sqrt(2)
    anti = int(np.nonzero(D[0] == -8)[0][0])
    null[anti] = -1 / np.sqrt(2)
    origin = np.array([240])
    a1 = a2 = a3 = True
    for variant, E0 in (("A-bare", 0.0), ("A-tuned", 56.0)):
        for g in (0.1, 0.5, 1.0, 2.0):
            H = np.zeros((N, N))
            H[:240, :240] = A
            H[240, 240] = E0
            H[240, :240] = g
            H[:240, 240] = g
            w, V = eig(H)
            Vc = g * np.sqrt(240)
            P_null = prob_series(w, V, null, origin, TGRID)
            P_sym = prob_series(w, V, sym, origin, TGRID)
            P_one = prob_series(w, V, single, origin, TGRID)
            f_sym = lambda t: prob_series(w, V, sym, origin, t)
            ib = int(P_sym.argmax())
            t_ref, p_ref = refine_max(f_sym, TGRID[ib], 0.06)
            rec = {"variant": variant, "g": g, "V": Vc, "E0": E0,
                   "null_max": float(P_null.max()),
                   "sym_max_grid": float(P_sym.max()),
                   "sym_max_refined": p_ref, "sym_t_refined": t_ref,
                   "single_max_grid": float(P_one.max()),
                   "single_vs_sym_over_240_maxabsdiff": float(np.abs(P_one - P_sym / 240).max()),
                   "single_bound_violation": float((P_one - P_sym / 240).max())}
            ok1 = rec["null_max"] < 1e-12
            if variant == "A-bare":
                pred = Vc**2 / (Vc**2 + 28.0**2)
                rec["P2_pred"] = pred
                rec["P2_err"] = abs(p_ref - pred)
                ok2 = rec["P2_err"] < 1e-6
            else:
                tstar = np.pi / (2 * Vc)
                p_star = float(prob_series(w, V, sym, origin, np.array([tstar]))[0])
                rec["P3_t_star"] = tstar
                rec["P3_P0_at_t_star"] = p_star
                rec["P3_grid_best_misses_by"] = float(1 - P_sym.max())
                ok2 = (p_star >= 1 - 1e-9) and (abs(t_ref - tstar) < 1e-3 or p_ref >= 1 - 1e-9)
            ok3 = rec["single_bound_violation"] < 1e-12 and rec["single_vs_sym_over_240_maxabsdiff"] < 1e-12
            rec.update({"A1": ok1, "A2": ok2, "A3": ok3})
            a1 &= ok1; a2 &= ok2; a3 &= ok3
            out["runs"].append(rec)
    out["gates"] = {"A1_null_zero": a1, "A2_P2_P3": a2, "A3_P4_equality": a3}
    return out

# ======================================================================
# Experiment B
# ======================================================================
def orbit_quotient():
    cls_of = {8: 0, 4: 1, 0: 2, -4: 3, -8: 4}
    cls = np.array([cls_of[int(x)] for x in D[0]])
    sizes = [int((cls == k).sum()) for k in range(5)]
    cnt = np.zeros((5, 5), dtype=int)  # cnt[i][j]: neighbours in orbit j of a vertex in orbit i
    for i in range(5):
        v = int(np.nonzero(cls == i)[0][0])
        for j in range(5):
            cnt[i, j] = int(A[v][cls == j].sum())
    # check constant across each orbit (stabilizer-invariance)
    for i in range(5):
        for v in np.nonzero(cls == i)[0]:
            for j in range(5):
                assert int(A[v][cls == j].sum()) == cnt[i, j]
    O = np.zeros((240, 5))
    for k in range(5):
        O[cls == k, k] = 1 / np.sqrt(sizes[k])
    return cls, sizes, cnt, O

def exp_B():
    eps_list = [0.0, 0.25, 0.5, 1.0, 2.0]
    pole = np.array([0])
    cls, sizes, cnt, O = orbit_quotient()
    out = {"experiment": "B-depth", "shells": shells, "orbit_sizes": sizes,
           "orbit_count_matrix_rows_from": cnt.tolist(), "runs": [], "gates": {}}
    starts = {}
    for k in (1, 2, 3):
        m = depth == k
        psi = np.zeros(240); psi[m] = 1 / np.sqrt(m.sum())
        starts[k] = psi
    pole_psi = np.zeros(240); pole_psi[0] = 1.0
    anti = int(np.nonzero(depth == 3)[0][0])
    s3 = np.nonzero(depth == 3)[0]
    s23 = np.nonzero(depth >= 2)[0]
    base = {}
    g_recip = g_quot = True
    for eps in eps_list:
        H = A + eps * np.diag(depth.astype(float))
        w, V = eig(H)
        rec = {"eps": eps, "arrival": {}, "escape": {}}
        # quotient cross-check
        Hq = O.T @ H @ O
        assert np.linalg.norm(H @ O - O @ Hq) < 1e-10  # orbit subspace invariant
        wq, Vq = np.linalg.eigh(Hq)
        for k in (1, 2, 3):
            f = lambda t, k=k: prob_series(w, V, starts[k], pole, t)
            Pg = f(TGRID)
            Pf = f(TFINE)
            ib = int(Pf.argmax())
            t_r, p_r = refine_max(f, TFINE[ib], 0.02)
            # quotient evolution
            cq = O.T @ starts[k]
            cqv = Vq.T @ cq
            idx_pole = 0
            Pq = np.empty(len(TGRID))
            ph = np.exp(-1j * np.outer(wq, TGRID)) * cqv[:, None]
            Pq = np.abs(Vq[idx_pole, :] @ ph) ** 2
            qdiff = float(np.abs(Pq - Pg).max())
            g_quot &= qdiff < 1e-10
            rec["arrival"][str(k)] = {
                "A_grid": float(Pg.max()), "t_grid": float(TGRID[Pg.argmax()]),
                "A_refined": p_r, "t_refined": t_r,
                "time_avg_P_pole": float(np.trapezoid(Pf, TFINE) / T_MAX),
                "quotient_maxabsdiff": qdiff}
            base.setdefault(k, {})[eps] = p_r
        # leak-out
        Pl3 = prob_series(w, V, pole_psi, s3, TGRID)
        Pl23 = prob_series(w, V, pole_psi, s23, TGRID)
        f3 = lambda t: prob_series(w, V, pole_psi, s3, t)
        Pf3 = f3(TFINE)
        t3, p3 = refine_max(f3, TFINE[int(Pf3.argmax())], 0.02)
        f23 = lambda t: prob_series(w, V, pole_psi, s23, t)
        Pf23 = f23(TFINE)
        t23, p23 = refine_max(f23, TFINE[int(Pf23.argmax())], 0.02)
        # reciprocity identity: E(eps) shell3 series == arrival-from-shell-3 series
        P_arr3 = prob_series(w, V, starts[3], pole, TGRID)
        rdiff = float(np.abs(Pl3 - P_arr3).max())
        g_recip &= rdiff < 1e-12
        rec["escape"] = {"E3_grid": float(Pl3.max()), "E3_refined": p3, "E3_t": t3,
                         "E23_grid": float(Pl23.max()), "E23_refined": p23, "E23_t": t23,
                         "reciprocity_maxabsdiff": rdiff}
        base.setdefault("E3", {})[eps] = p3
        base.setdefault("E23", {})[eps] = p23
        out["runs"].append(rec)
    # ratios
    for rec in out["runs"]:
        e = rec["eps"]
        rec["R"] = {str(k): base[k][e] / base[k][0.0] for k in (1, 2, 3)}
        rec["E3_ratio"] = base["E3"][e] / base["E3"][0.0]
        rec["E23_ratio"] = base["E23"][e] / base["E23"][0.0]
        a = [rec["arrival"][str(k)]["A_refined"] for k in (1, 2, 3)]
        rec["E1_ordering_A1>=A2>=A3"] = bool(a[0] >= a[1] >= a[2])
    # PR #117 regression at eps = 0: antipodal fidelity peak near t = 42.34
    H0 = A.copy()
    w0, V0 = eig(H0)
    f0 = lambda t: prob_series(w0, V0, pole_psi, s3, t)
    tt = np.arange(40, 45 + 1e-9, 0.001)
    ib = int(f0(tt).argmax())
    t_r, p_r = refine_max(f0, tt[ib], 0.01, 40, 45)
    out["pr117_regression"] = {"peak_in_[40,45]": p_r, "t": t_r,
                               "pass": bool(abs(p_r - 0.882) < 1e-3 and abs(t_r - 42.34) < 0.02)}
    out["gates"] = {"reciprocity_E3_eq_A3": g_recip, "quotient_crosscheck": g_quot,
                    "PR117_regression": out["pr117_regression"]["pass"]}
    return out

def _j(o):
    if isinstance(o, (np.bool_,)): return bool(o)
    if isinstance(o, np.integer): return int(o)
    if isinstance(o, np.floating): return float(o)
    raise TypeError(type(o))

if __name__ == "__main__":
    a = exp_A()
    b = exp_B()
    json.dump(a, open("eqbit_drift_001_A_architect.json", "w"), indent=1, default=_j)
    json.dump(b, open("eqbit_drift_001_B_architect.json", "w"), indent=1, default=_j)
    print("== Experiment A gates ==", a["gates"])
    for r in a["runs"]:
        if r["variant"] == "A-bare":
            print(f"{r['variant']} g={r['g']:<4} P2 refined={r['sym_max_refined']:.8f} pred={r['P2_pred']:.8f} err={r['P2_err']:.1e}  "
                  f"single/sym diff={r['single_vs_sym_over_240_maxabsdiff']:.1e} single_max={r['single_max_grid']:.5f} null={r['null_max']:.1e}")
        else:
            print(f"{r['variant']} g={r['g']:<4} P0(t*={r['P3_t_star']:.4f})={r['P3_P0_at_t_star']:.12f}  grid-best misses 1 by {r['P3_grid_best_misses_by']:.1e}  null={r['null_max']:.1e}")
    print("== Experiment B ==", b["gates"])
    print("shells", b["shells"], "orbit sizes", b["orbit_sizes"])
    print("count matrix\n", np.array(b["orbit_count_matrix_rows_from"]))
    print("PR117 regression:", b["pr117_regression"])
    print("eps   | A1 (t)         A2 (t)         A3 (t)         | E3 (t)         E23    | R1     R2     R3     E3r    ordering")
    for r in b["runs"]:
        a1, a2, a3 = (r["arrival"][k] for k in "123")
        print(f"{r['eps']:<5} | {a1['A_refined']:.4f} ({a1['t_refined']:6.2f}) {a2['A_refined']:.4f} ({a2['t_refined']:6.2f}) "
              f"{a3['A_refined']:.4f} ({a3['t_refined']:6.2f}) | {r['escape']['E3_refined']:.4f} ({r['escape']['E3_t']:6.2f}) {r['escape']['E23_refined']:.4f} | "
              f"{r['R']['1']:.3f}  {r['R']['2']:.3f}  {r['R']['3']:.3f}  {r['E3_ratio']:.3f}  {r['E1_ordering_A1>=A2>=A3']}")
    print("time-avg P(pole) by start/eps:")
    for r in b["runs"]:
        print(r["eps"], [round(r["arrival"][k]["time_avg_P_pole"], 5) for k in "123"])
