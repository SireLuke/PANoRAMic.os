#!/usr/bin/env python3
"""EQBIT-DRIFT-001 extension: Experiment B on the Leech minimal-vector graph via the
pole-stabilizer orbit quotient. Architect bench (Claude). Analogy rung only.

PREREGISTRATION (frozen in this header BEFORE the Leech run; nothing below was tuned on Leech output)
-----------------------------------------------------------------------------------------------
Graph      : vertices = 196,560 Leech minimal vectors (integral coords, norm^2 32); edge iff x.y == 16
             (inner product 2), matching research/LEECH24_EQBIT_001.md section 3. Pole = vector index 0.
Quotient   : orbits of the pole's stabilizer = classes of x.pole in {32,16,8,0,-8,-16,-32}.
             Walk restricted to the orbit-uniform subspace is EXACT iff neighbour counts are constant
             on each orbit. Gate Q1: census equals 1,4600,47104,93150,47104,4600,1 and counts are
             constant on a deterministic stride sample of every orbit (full check for E8).
             DEPENDENCY: constancy on all vertices rests on Co0-stabilizer orbit structure (known
             group theory), not on this sample; the sample is a consistency check, not a proof.
Dynamics   : H(eps) = A_q + eps*diag(depth), depth = BFS distance from pole in the orbit graph.
             U(t)=exp(-iHt) by exact eigh of the small orbit matrix. Window T=200 (same as E8 spec).
             Time grid dt=1e-4 (quotient is tiny; Leech periods can be ~1e-3, so the spec's 0.05
             grid would alias). Maxima refined by ternary search; time-of-max and time-average recorded.
Observables: for each depth shell k>=1: A_k(eps)=max_t P(pole,t) from the uniform state on shell k.
             Leak: start at pole; E_deep(eps)=max_t total probability on the deepest shell; E_agg on
             depth>=2. Ratios R_k = A_k(eps)/A_k(0).
Gates      : Q1 census/constancy; Q2 symmetry of the quotient matrix (integer identity
             n_i*cnt[i][j]==n_j*cnt[j][i]); Q3 METHOD REGRESSION: the same code applied to E8 must
             reproduce the full-matrix A_k(eps) table in outputs/eqbit_drift_001_B_architect.json
             within 1e-4 (the full run used a coarser 0.01 grid + refinement, so tiny differences
             are possible and will be reported, not tuned away).
Eps grid   : E8: {0,.25,.5,1,2} (as before). Leech: {0,.25,.5,1,2,5,10,20,50,100}; the wider
             tail is registered because degree is 4600 vs 56, so unit-scale gradients are weak.
Claim ceiling: if the Leech orbit graph has <=3 nonzero depths, the exponential-law ceiling of
             spec section 4 still binds. No horizon/gravity language. Closed unitary system.
"""
import itertools, json, sys
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
HERE = Path(__file__).resolve().parent

T_MAX, DT = 200.0, 1e-4


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
    return np.array(R, dtype=np.int32)


def leech_vectors():
    from experiments.moonshine_sierpinski.leech_golay_construction import leech_minimal_vectors
    return np.array(leech_minimal_vectors(), dtype=np.int32)


def quotient(X, N, adj, expected_sizes=None, per_orbit_check=30):
    n = len(X)
    dp = X @ X[0]
    vals = sorted(set(int(v) for v in np.unique(dp)), reverse=True)
    cls = np.zeros(n, dtype=np.int64)
    for k, v in enumerate(vals):
        cls[dp == v] = k
    m = len(vals)
    sizes = [int((cls == k).sum()) for k in range(m)]
    cnt = np.zeros((m, m), dtype=np.int64)
    consistent = True
    checked = 0
    for i in range(m):
        members = np.nonzero(cls == i)[0]
        if len(members) <= per_orbit_check:
            pick = members
        else:
            pick = members[np.linspace(0, len(members) - 1, per_orbit_check).astype(int)]
        rows = None
        for r in pick:
            d = X @ X[r]
            nb = (d == adj)
            row = np.array([int((nb & (cls == j)).sum()) for j in range(m)])
            if rows is None:
                rows = row
            elif not np.array_equal(rows, row):
                consistent = False
            checked += 1
        cnt[i] = rows
    sym_ok = all(sizes[i] * cnt[i, j] == sizes[j] * cnt[j, i] for i in range(m) for j in range(m))
    Hq = np.zeros((m, m))
    for i in range(m):
        for j in range(m):
            Hq[i, j] = cnt[j, i] * np.sqrt(sizes[j] / sizes[i])
    depth = [-1] * m
    depth[0] = 0
    fr = [0]
    while fr:
        nxt = []
        for u in fr:
            for v in range(m):
                if cnt[u, v] > 0 and depth[v] < 0:
                    depth[v] = depth[u] + 1
                    nxt.append(v)
        fr = nxt
    antipode = m - 1
    return dict(vals=vals, sizes=sizes, cnt=cnt, Hq=Hq, depth=depth, consistent=consistent,
                sym_ok=sym_ok, census_ok=(expected_sizes is None or sizes == expected_sizes),
                antipode_orbit=antipode, checked=checked,
                degree=int(cnt[0].sum()))


def stats(w, V, s, sel, T=T_MAX, dt=DT, chunk=200000):
    c = V.T @ s
    n = int(round(T / dt)) + 1
    best, tb, integ = -1.0, 0.0, 0.0
    for a in range(0, n, chunk):
        t = np.arange(a, min(a + chunk, n)) * dt
        ph = np.exp(-1j * np.outer(t, w)) * c[None, :]
        amp = ph @ V[sel, :].T
        P = (np.abs(amp) ** 2).sum(1)
        i = int(P.argmax())
        if P[i] > best:
            best, tb = float(P[i]), float(t[i])
        integ += float(P.sum()) * dt
    f = lambda tt: (np.abs((np.exp(-1j * np.outer(tt, w)) * c[None, :]) @ V[sel, :].T) ** 2).sum(1)
    lo, hi = max(tb - dt, 0.0), min(tb + dt, T)
    for _ in range(60):
        m1, m2 = lo + (hi - lo) / 3, hi - (hi - lo) / 3
        if f(np.array([m1]))[0] < f(np.array([m2]))[0]:
            lo = m1
        else:
            hi = m2
    tr = 0.5 * (lo + hi)
    pr = float(f(np.array([tr]))[0])
    if pr < best:
        pr, tr = best, tb
    return pr, tr, integ / T


def run_graph(name, q, eps_list):
    m = len(q["sizes"])
    depth = np.array(q["depth"])
    D = int(depth.max())
    sizes = np.array(q["sizes"], dtype=float)
    out = {"graph": name, "orbit_values": q["vals"], "orbit_sizes": q["sizes"], "depth_by_orbit": q["depth"],
           "max_depth": D, "degree": q["degree"], "count_matrix": q["cnt"].tolist(), "runs": []}
    w0, V0 = np.linalg.eigh(q["Hq"])
    out["eigenvalues_eps0"] = w0.tolist()
    out["eigenvalues_eps0_all_integer"] = bool(np.allclose(w0, np.round(w0), atol=1e-8))
    pole = np.zeros(m); pole[0] = 1.0
    base = {}
    for eps in eps_list:
        Hq = q["Hq"] + eps * np.diag(depth.astype(float))
        w, V = np.linalg.eigh(Hq)
        rec = {"eps": eps, "arrival": {}, "escape": {}}
        for k in range(1, D + 1):
            sel_orb = np.nonzero(depth == k)[0]
            s = np.zeros(m); s[sel_orb] = np.sqrt(sizes[sel_orb] / sizes[sel_orb].sum())
            p, t, avg = stats(w, V, s, [0])
            rec["arrival"][str(k)] = {"A": p, "t": t, "time_avg": avg}
            base.setdefault(("A", k), {})[eps] = p
        deep = list(np.nonzero(depth == D)[0])
        agg = list(np.nonzero(depth >= 2)[0])
        pd, td, _ = stats(w, V, pole, deep)
        pa, ta, _ = stats(w, V, pole, agg)
        rec["escape"] = {"E_deepest": pd, "t_deepest": td, "E_depth_ge2": pa, "t_ge2": ta}
        base.setdefault(("E", 0), {})[eps] = pd
        out["runs"].append(rec)
    for rec in out["runs"]:
        e = rec["eps"]
        rec["R"] = {str(k): base[("A", k)][e] / base[("A", k)][0.0] for k in range(1, D + 1)}
        rec["E_deepest_ratio"] = base[("E", 0)][e] / base[("E", 0)][0.0]
        a = [rec["arrival"][str(k)]["A"] for k in range(1, D + 1)]
        rec["E1_ordering_monotone_decreasing"] = bool(all(a[i] >= a[i + 1] for i in range(len(a) - 1)))
    return out


def _j(o):
    if isinstance(o, np.bool_): return bool(o)
    if isinstance(o, np.integer): return int(o)
    if isinstance(o, np.floating): return float(o)
    raise TypeError(type(o))


if __name__ == "__main__":
    res = {"preregistration_header": "see module docstring"}
    # ---- E8 regression of the quotient method ----
    qe = quotient(e8_vectors(), 8, 4, expected_sizes=[1, 56, 126, 56, 1], per_orbit_check=240)
    e8 = run_graph("E8-240", qe, [0.0, 0.25, 0.5, 1.0, 2.0])
    full = json.load(open(HERE / "outputs" / "eqbit_drift_001_B_architect.json"))
    worst = 0.0
    for fr, qr in zip(full["runs"], e8["runs"]):
        # E8 orbit depths: orbit(ip2)=1, orbit(ip0)=orbit(ip-1)=2, antipode=3 -> same shells as BFS
        for k in "123":
            worst = max(worst, abs(fr["arrival"][k]["A_refined"] - qr["arrival"][k]["A"]))
        worst = max(worst, abs(fr["escape"]["E3_refined"] - qr["escape"]["E_deepest"]))
    e8["Q3_regression_worst_abs_diff_vs_full_matrix_run"] = worst
    e8["Q3_pass"] = bool(worst < 1e-4)
    # ---- Leech ----
    X = leech_vectors()
    assert X.shape == (196560, 24)
    ql = quotient(X, 32, 16, expected_sizes=[1, 4600, 47104, 93150, 47104, 4600, 1], per_orbit_check=30)
    lc = run_graph("Leech-196560", ql, [0.0, 0.25, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 50.0, 100.0])
    res.update({"E8": e8, "Leech": lc,
                "gates": {"E8_Q1_census_constancy": bool(qe["census_ok"] and qe["consistent"]),
                          "E8_Q2_symmetry": bool(qe["sym_ok"]),
                          "E8_Q3_regression": e8["Q3_pass"],
                          "Leech_Q1_census": bool(ql["census_ok"]),
                          "Leech_Q1_constancy_sampled": bool(ql["consistent"]),
                          "Leech_Q2_symmetry": bool(ql["sym_ok"]),
                          "Leech_degree_4600": ql["degree"] == 4600}})
    json.dump(res, open(HERE / "outputs" / "eqbit_drift_001_leech_quotient.json", "w"), indent=1, default=_j)
    print("GATES", res["gates"])
    print("E8 regression worst diff", worst)
    for g in (e8, lc):
        print(f"\n== {g['graph']}  orbits {g['orbit_sizes']}  depth/orbit {g['depth_by_orbit']}  max depth {g['max_depth']}")
        print("eigenvalues(eps=0):", np.round(g["eigenvalues_eps0"], 6), " all integer:", g["eigenvalues_eps0_all_integer"])
        print("count matrix:\n", np.array(g["count_matrix"]))
        D = g["max_depth"]
        hdr = "eps    | " + " ".join(f"A{k}(t)".ljust(17) for k in range(1, D + 1)) + "| Edeep(t)        | " + " ".join(f"R{k}".ljust(6) for k in range(1, D + 1)) + " Er     mono"
        print(hdr)
        for r in g["runs"]:
            a = " ".join(f"{r['arrival'][str(k)]['A']:.4f}({r['arrival'][str(k)]['t']:7.2f})".ljust(17) for k in range(1, D + 1))
            rr = " ".join(f"{r['R'][str(k)]:.3f}".ljust(6) for k in range(1, D + 1))
            print(f"{r['eps']:<6} | {a}| {r['escape']['E_deepest']:.4f}({r['escape']['t_deepest']:7.2f}) | {rr} {r['E_deepest_ratio']:.3f}  {r['E1_ordering_monotone_decreasing']}")
        print("time-avg P(pole):")
        for r in g["runs"]:
            print(r["eps"], [round(r["arrival"][str(k)]["time_avg"], 6) for k in range(1, D + 1)])
