#!/usr/bin/env python3
"""EQBIT-DRIFT-001 — Cosmo's independent implementation (Memory bench).

Written from the spec alone (files/eqbit-drift-spec.md, revision 2).
Exact diagonalization, deterministic, numpy only.

Experiments:
  A — drain at 0^8: 241-dim augmented Hamiltonian, bare (E0=0) and
      tuned (E0=56), g in {0.1, 0.5, 1.0, 2.0}. Gates A1/A2/A3.
  B — depth gradient: H(eps) = A + eps*diag(depth), eps in
      {0, 0.25, 0.5, 1, 2}. Gates B0 (regression vs PR #117),
      reciprocity identity E3 == A3, 5x5 orbit-quotient cross-check.

Usage: python3 drift.py [out.json]
"""
import itertools
import json
import sys

import numpy as np

T_MAX = 200.0
DT = 0.05
GRID = np.arange(0.0, T_MAX + 0.5 * DT, DT)  # 4001 points


# ---------------------------------------------------------------- roots
def build_roots():
    """E8 roots in scaled (x2) coordinates: norm^2 = 8, adjacency dot = 4.
    Root 0 is the pole (2,2,0,0,0,0,0,0)."""
    roots = []
    # type A: permutations of (+-2, +-2, 0^6)
    for i, j in itertools.combinations(range(8), 2):
        for si in (2, -2):
            for sj in (2, -2):
                v = np.zeros(8, dtype=np.int64)
                v[i] = si
                v[j] = sj
                roots.append(v)
    # type B: (+-1)^8 with an even number of -1
    for signs in itertools.product((1, -1), repeat=8):
        if sum(1 for s in signs if s < 0) % 2 == 0:
            roots.append(np.array(signs, dtype=np.int64))
    R = np.array(roots, dtype=np.int64)
    assert R.shape == (240, 8)
    assert np.all(np.sum(R * R, axis=1) == 8)
    # move the pole to index 0
    pole = np.array([2, 2, 0, 0, 0, 0, 0, 0], dtype=np.int64)
    idx = int(np.where(np.all(R == pole, axis=1))[0][0])
    R[[0, idx]] = R[[idx, 0]]
    return R


def build_adjacency(R):
    G = R @ R.T  # scaled Gram matrix
    A = ((G == 4)).astype(np.float64)
    np.fill_diagonal(A, 0.0)
    assert np.all(A.sum(axis=1) == 56), "Gosset graph must be 56-regular"
    return A, G


def bfs_depths(A):
    depth = np.full(240, -1, dtype=int)
    depth[0] = 0
    frontier = [0]
    d = 0
    while frontier:
        d += 1
        nxt = []
        for v in frontier:
            for w in np.where(A[v] > 0)[0]:
                if depth[w] < 0:
                    depth[w] = d
                    nxt.append(int(w))
        frontier = nxt
    sizes = [int(np.sum(depth == k)) for k in range(4)]
    assert sizes == [1, 56, 182, 1], sizes
    return depth


# ---------------------------------------------------------------- helpers
def prob_series(evals, evecs, psi0, target_rows):
    """|amplitude|^2 on GRID for target basis rows, from exact diagonalization.
    evecs columns are eigenvectors. Returns array (len(target_rows), len(GRID))."""
    c = evecs.conj().T @ psi0                      # spectral coefficients of psi0
    # phase[k, t] = exp(-i lam_k t)
    phase = np.exp(-1j * np.outer(evals, GRID))    # (n, T)
    out = []
    for r in target_rows:
        amp = (evecs[r, :] * c) @ phase            # (T,)
        out.append(np.abs(amp) ** 2)
    return np.array(out)


def prob_at(evals, evecs, psi0, row, t):
    c = evecs.conj().T @ psi0
    amp = np.sum(evecs[row, :] * c * np.exp(-1j * evals * t))
    return float(np.abs(amp) ** 2)


def refine_max(evals, evecs, psi0, row, t_lo, t_hi, tol=1e-10):
    """Golden-section maximization of P_row(t) on [t_lo, t_hi]."""
    gr = (np.sqrt(5.0) - 1.0) / 2.0
    a, b = t_lo, t_hi
    c1 = b - gr * (b - a)
    c2 = a + gr * (b - a)
    f1 = prob_at(evals, evecs, psi0, row, c1)
    f2 = prob_at(evals, evecs, psi0, row, c2)
    while b - a > tol:
        if f1 < f2:
            a, c1, f1 = c1, c2, f2
            c2 = a + gr * (b - a)
            f2 = prob_at(evals, evecs, psi0, row, c2)
        else:
            b, c2, f2 = c2, c1, f1
            c1 = b - gr * (b - a)
            f1 = prob_at(evals, evecs, psi0, row, c1)
    t_star = 0.5 * (a + b)
    return prob_at(evals, evecs, psi0, row, t_star), t_star


def grid_max_refined(evals, evecs, psi0, row):
    P = prob_series(evals, evecs, psi0, [row])[0]
    i = int(np.argmax(P))
    lo = GRID[max(i - 1, 0)]
    hi = GRID[min(i + 1, len(GRID) - 1)]
    val, t_star = refine_max(evals, evecs, psi0, row, lo, hi)
    return val, t_star, float(np.mean(P))


# ---------------------------------------------------------------- experiment A
def experiment_A(A):
    results = {}
    n = 240
    sym = np.zeros(n + 1)
    sym[:n] = 1.0 / np.sqrt(n)
    single = np.zeros(n + 1)
    single[0] = 1.0                      # the pole root
    control = np.zeros(n + 1)            # antisymmetric: orthogonal to |S>
    control[1] = 1.0 / np.sqrt(2.0)
    control[2] = -1.0 / np.sqrt(2.0)
    for variant, E0 in (("bare", 0.0), ("tuned", 56.0)):
        for g in (0.1, 0.5, 1.0, 2.0):
            H = np.zeros((n + 1, n + 1))
            H[:n, :n] = A
            H[n, :n] = g
            H[:n, n] = g
            H[n, n] = E0
            evals, evecs = np.linalg.eigh(H)
            V = g * np.sqrt(n)
            if variant == "bare":
                Om = np.sqrt(784.0 + V * V)
                closed_max = V * V / (Om * Om)
                t_star_closed = np.pi / (2.0 * Om)
            else:
                closed_max = 1.0
                t_star_closed = np.pi / (2.0 * V)
            # symmetric start -> origin
            p_sym = prob_series(evals, evecs, sym, [n])[0]
            max_num, t_num, _ = grid_max_refined(evals, evecs, sym, n)
            at_closed_t = prob_at(evals, evecs, sym, n, t_star_closed)
            # control: P0 must vanish identically
            p_ctl = prob_series(evals, evecs, control, [n])[0]
            ctl_max = float(np.max(np.abs(p_ctl)))
            # single root: equality P0(single) == P0(sym)/240 on the grid
            p_single = prob_series(evals, evecs, single, [n])[0]
            eq_dev = float(np.max(np.abs(p_single - p_sym / n)))
            results[f"{variant}/g={g}"] = {
                "closed_form_max": closed_max,
                "numeric_max_refined": max_num,
                "numeric_argmax": t_num,
                "closed_form_argmax": float(t_star_closed),
                "P_at_closed_form_t": at_closed_t,
                "A1_control_max_abs": ctl_max,
                "A1_pass": bool(ctl_max < 1e-12),
                "A2_pass": bool(abs(max_num - closed_max) < 1e-6
                                and abs(at_closed_t - closed_max) < 1e-6),
                "A3_equality_max_dev": eq_dev,
                "A3_pass": bool(eq_dev < 1e-9),
            }
    return results


# ---------------------------------------------------------------- experiment B
def experiment_B(A, G, depth):
    results = {}
    shells = {k: np.where(depth == k)[0] for k in range(4)}
    antipode = int(np.where(np.all(G[0] == -8, axis=0))[0][0]) \
        if False else int(np.argmin(G[0]))  # scaled dot -8 with the pole
    assert G[0, antipode] == -8 and depth[antipode] == 3
    # orbit partition by scaled inner product with the pole: 8,4,0,-4,-8
    orbit_id = {8: 0, 4: 1, 0: 2, -4: 3, -8: 4}
    orbits = np.array([orbit_id[int(v)] for v in G[0]])
    orbit_sizes = [int(np.sum(orbits == k)) for k in range(5)]
    assert orbit_sizes == [1, 56, 126, 56, 1], orbit_sizes
    # orthonormal orbit basis (240 x 5)
    W = np.zeros((240, 5))
    for k in range(5):
        W[orbits == k, k] = 1.0 / np.sqrt(orbit_sizes[k])

    for eps in (0.0, 0.25, 0.5, 1.0, 2.0):
        H = A + eps * np.diag(depth.astype(np.float64))
        evals, evecs = np.linalg.eigh(H)
        Hq = W.T @ H @ W
        q_evals, q_evecs = np.linalg.eigh(Hq)
        entry = {}
        # drift-in: shell starts -> pole
        A_k = {}
        for k in (1, 2, 3):
            psi = np.zeros(240)
            psi[shells[k]] = 1.0 / np.sqrt(len(shells[k]))
            val, t_star, tavg = grid_max_refined(evals, evecs, psi, 0)
            # quotient cross-check: psi in orbit basis
            psi_q = W.T @ psi
            val_q, _, _ = grid_max_refined(q_evals, q_evecs, psi_q, 0)
            rec = {"arrival": val, "argmax": t_star, "time_avg": tavg,
                   "quotient_arrival": val_q,
                   "quotient_dev": abs(val - val_q)}
            if k == 3:
                rec["P_at_t42.34"] = prob_at(evals, evecs, psi, 0, 42.34)
            A_k[k] = rec
        entry["A"] = A_k
        # leak-out: pole start -> shells (shell-3 escape refined like A_3,
        # so the reciprocity identity compares like with like)
        psi_pole = np.zeros(240)
        psi_pole[0] = 1.0
        e3_val, _e3_t, _e3_avg = grid_max_refined(evals, evecs, psi_pole,
                                                  antipode)
        rows_s2 = list(shells[2]) + list(shells[3])
        P_s23 = prob_series(evals, evecs, psi_pole, rows_s2).sum(axis=0)
        entry["E_shell3_max"] = e3_val
        entry["E_shells23_max"] = float(np.max(P_s23))
        entry["reciprocity_dev"] = abs(e3_val - A_k[3]["arrival"])
        # single-vertex distributions of max P(pole), per shell (secondary)
        dist = {}
        c_all = evecs.conj().T  # rows: spectral coeffs for each basis start
        phase = np.exp(-1j * np.outer(evals, GRID))
        amps = (evecs[0, :] * c_all) @ phase  # (240 starts, T) amp at pole
        P_all = np.abs(amps) ** 2
        mx = P_all.max(axis=1)
        for k in (1, 2, 3):
            vals = mx[shells[k]]
            dist[k] = {"min": float(vals.min()), "max": float(vals.max()),
                       "mean": float(vals.mean())}
        entry["single_vertex_max_dist"] = dist
        results[f"eps={eps}"] = entry
    return results


def main():
    R = build_roots()
    A, G = build_adjacency(R)
    depth = bfs_depths(A)
    out = {"experiment_A": experiment_A(A),
           "experiment_B": experiment_B(A, G, depth)}
    # gate summary
    a_ok = all(v["A1_pass"] and v["A2_pass"] and v["A3_pass"]
               for v in out["experiment_A"].values())
    b0 = out["experiment_B"]["eps=0.0"]["A"][3]
    recip = max(v["reciprocity_dev"] for v in out["experiment_B"].values())
    qdev = max(v["A"][k]["quotient_dev"]
               for v in out["experiment_B"].values() for k in (1, 2, 3))
    out["gate_summary"] = {
        "A_all_pass": bool(a_ok),
        "B0_arrival_eps0_shell3": b0["arrival"],
        "B0_argmax_eps0_shell3": b0["argmax"],
        "B0_reference": "0.882 at t ~= 42.34 (PR #117)",
        "reciprocity_max_dev": recip,
        "quotient_max_dev": qdev,
    }
    path = sys.argv[1] if len(sys.argv) > 1 else "results_cosmo.json"
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out["gate_summary"], indent=2))


if __name__ == "__main__":
    main()
