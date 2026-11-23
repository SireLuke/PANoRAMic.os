#!/usr/bin/env python3
"""NS-ABOM-E8-LEECH-EQBIT-002, Claude bench: independent implementation of
protocol sections A (Gosset-graph GF(2) cut-rank) and C (adapter / identity controls).

Section B (multi-module ablation) is NOT implemented here: it needs the other
bench's harness switches, and this script deliberately does not import that harness.

Independence statement
  * E8 roots, the Gosset graph, GF(2) rank (three implementations), partition sampling,
    graph rewiring and involution search are written from scratch here.
  * The only repository code called is core.abom_v8.abom_v8_model (section C adapter
    controls: the module under test) which in turn loads core.geometry.e8_root_system.
    Those are called as black boxes and compared with this file's own computations.
  * experiments/ns_abom_e8_leech_eqbit_001/integration.py and
    experiments/flip_qubit/cut_rank_audit.py are neither read nor run by this script.

Usage:  python ns_abom_claude.py [--quick] [--out DIR]
"""
import argparse
import datetime
import hashlib
import json
import math
import os
import platform
import subprocess
import sys
from decimal import Decimal, getcontext
from itertools import combinations, product

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
SCHEMA = "ns-abom-claude-002/1"
if REPO not in sys.path:
    sys.path.insert(0, REPO)

SEEDS = [101, 202, 303, 404, 505, 606, 707, 808, 909, 1010]   # published seed list
FAMILY_ID = {"transversal": 1, "balanced": 2, "graph_null": 3, "involution": 4, "adapter": 5}


# ----------------------------------------------------------------------------- E8 / Gosset
def e8_roots_doubled():
    """240 roots in doubled integer coordinates (real coordinate = value / 2)."""
    roots = []
    for i, j in combinations(range(8), 2):
        for si, sj in product((2, -2), repeat=2):
            v = [0] * 8
            v[i], v[j] = si, sj
            roots.append(tuple(v))
    for signs in product((1, -1), repeat=8):
        if sum(1 for s in signs if s < 0) % 2 == 0:
            roots.append(tuple(signs))
    return sorted(roots)  # canonical order: lexicographic on doubled coordinates


def dot4(u, v):
    """4 * (real inner product) as an exact integer."""
    return sum(a * b for a, b in zip(u, v))


def check_e8(roots):
    out = {}
    out["count"] = len(roots)
    out["distinct"] = len(set(roots)) == len(roots)
    out["all_norm2"] = all(dot4(r, r) == 8 for r in roots)              # real norm^2 = 2
    out["closed_under_negation"] = set(tuple(-x for x in r) for r in roots) == set(roots)
    ips = {}
    for u in roots:
        for v in roots:
            ips[dot4(u, v)] = ips.get(dot4(u, v), 0) + 1
    out["inner_product_histogram_x4"] = {str(k): ips[k] for k in sorted(ips)}
    # integrality: 2<u,v>/<v,v> = <u,v> must be an integer (real) -> dot4 % 4 == 0
    out["crystallographic"] = all(k % 4 == 0 for k in ips)
    # closed under reflections
    rs = set(roots)
    ok = True
    for a in roots[:40]:       # a representative subset is enough for a sanity test; full check below on perms
        for v in roots:
            k = dot4(v, a) // 4
            w = tuple(x - k * y for x, y in zip(v, a))
            if w not in rs:
                ok = False
    out["reflection_closure_subset_ok"] = ok
    return out


def canonical_hash(roots):
    s = ";".join(",".join(str(x) for x in r) for r in sorted(roots))
    return hashlib.sha256(s.encode()).hexdigest()


def gosset_adjacency(roots):
    n = len(roots)
    adj = [0] * n
    deg = [0] * n
    for a in range(n):
        for b in range(n):
            if a != b and dot4(roots[a], roots[b]) == 4:   # real inner product 1
                adj[a] |= 1 << b
                deg[a] += 1
    return adj, deg


def neg_perm(roots):
    idx = {r: i for i, r in enumerate(roots)}
    return [idx[tuple(-x for x in r)] for r in roots]


def is_automorphism(perm, adj):
    n = len(adj)
    for a in range(n):
        m = 0
        row = adj[a]
        while row:
            low = row & -row
            b = low.bit_length() - 1
            m |= 1 << perm[b]
            row ^= low
        if m != adj[perm[a]]:
            return False
    return True


# ----------------------------------------------------------------------------- GF(2) rank (3 impls)
def rank_int(rows):
    """Implementation 1: XOR basis keyed by leading bit, rows are Python ints."""
    basis = {}
    for r in rows:
        while r:
            h = r.bit_length() - 1
            b = basis.get(h)
            if b is None:
                basis[h] = r
                break
            r ^= b
    return len(basis)


def rank_numpy(M):
    """Implementation 2: dense uint8 Gaussian elimination with row swaps."""
    A = (np.array(M, dtype=np.uint8) & 1).copy()
    rows, cols = A.shape
    r = 0
    for c in range(cols):
        if r >= rows:
            break
        piv = np.nonzero(A[r:, c])[0]
        if piv.size == 0:
            continue
        p = r + int(piv[0])
        if p != r:
            A[[r, p]] = A[[p, r]]
        mask = A[:, c].copy()
        mask[r] = 0
        A ^= np.outer(mask, A[r])
        r += 1
    return r


def rank_bruteforce(M):
    """Implementation 3 (small only): rank = log2 |row span|, enumerating the span."""
    rows = [int("".join(str(int(x) & 1) for x in row), 2) for row in M]
    span = {0}
    for r in rows:
        span |= {s ^ r for s in span}
    return len(span).bit_length() - 1


def fixtures_crosscheck(rng):
    results = []
    cases = {
        "zero_5x5": np.zeros((5, 5), int),
        "identity_6": np.eye(6, dtype=int),
        "ones_7x7": np.ones((7, 7), int),
        "dup_rows": np.array([[1, 0, 1, 1], [1, 0, 1, 1], [0, 1, 1, 0]]),
        "xor_dependent": np.array([[1, 1, 0, 0], [0, 1, 1, 0], [1, 0, 1, 0], [0, 0, 0, 1]]),
        "known_rank_over_Z_not_GF2": np.array([[1, 1], [1, 1]]),
        "det3_odd_over_Z_even_over_GF2": np.array([[1, 1, 0], [0, 1, 1], [1, 0, 1]]),  # det=2 -> rank 2 over GF(2)
    }
    expected = {"zero_5x5": 0, "identity_6": 6, "ones_7x7": 1, "dup_rows": 2, "xor_dependent": 3,
                "known_rank_over_Z_not_GF2": 1, "det3_odd_over_Z_even_over_GF2": 2}
    for name, M in cases.items():
        ri = rank_int([int("".join(map(str, row)), 2) for row in M.tolist()])
        rn = rank_numpy(M)
        rb = rank_bruteforce(M.tolist())
        results.append(dict(name=name, expected=expected[name], int=ri, numpy=rn, brute=rb,
                            ok=(ri == rn == rb == expected[name])))
    n_rand_ok = 0
    n_rand = 300
    for _ in range(n_rand):
        r_, c_ = int(rng.integers(1, 11)), int(rng.integers(1, 13))
        M = rng.integers(0, 2, size=(r_, c_))
        a = rank_int([int("".join(map(str, row)), 2) for row in M.tolist()])
        b = rank_numpy(M)
        c = rank_bruteforce(M.tolist())
        n_rand_ok += int(a == b == c)
    results.append(dict(name="random_small_300", ok=(n_rand_ok == n_rand), agree=n_rand_ok, of=n_rand))
    return results


# ----------------------------------------------------------------------------- partitions
def cut_rank(adj, S_mask, n_total):
    full = (1 << n_total) - 1
    comp = full ^ S_mask
    rows = []
    m = S_mask
    while m:
        low = m & -m
        v = low.bit_length() - 1
        rows.append(adj[v] & comp)
        m ^= low
    return rank_int(rows)


def cut_matrix_dense(adj, S_idx, T_idx):
    return [[(adj[a] >> b) & 1 for b in T_idx] for a in S_idx]


def mask_of(idx):
    m = 0
    for i in idx:
        m |= 1 << i
    return m


def sample_transversal(rng, pairs):
    pick = rng.integers(0, 2, size=len(pairs))
    return mask_of(p[int(k)] for p, k in zip(pairs, pick))


def sample_balanced(rng, n):
    return mask_of(rng.choice(n, size=n // 2, replace=False).tolist())


def stream(seed, family):
    return np.random.Generator(np.random.PCG64(np.random.SeedSequence([seed, FAMILY_ID[family]])))


def summarize(x):
    a = np.array(x)
    return dict(n=int(a.size), min=int(a.min()), max=int(a.max()), mean=float(a.mean()),
                median=float(np.median(a)), std=float(a.std(ddof=1)),
                p05=float(np.percentile(a, 5)), p95=float(np.percentile(a, 95)),
                histogram={str(k): int(v) for k, v in zip(*np.unique(a, return_counts=True))})


def _logbinom_pmf(k, n, p):
    if p <= 0:
        return 0.0 if k else 1.0
    if p >= 1:
        return 1.0 if k == n else 0.0
    return math.exp(math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)
                    + k * math.log(p) + (n - k) * math.log1p(-p))


def _binom_sf(k, n, p):  # P(X >= k)
    return sum(_logbinom_pmf(j, n, p) for j in range(k, n + 1))


def _binom_cdf(k, n, p):  # P(X <= k)
    return sum(_logbinom_pmf(j, n, p) for j in range(0, k + 1))


def clopper_pearson(k, n, alpha=0.05):
    lo = 0.0 if k == 0 else None
    hi = 1.0 if k == n else None
    if lo is None:   # solve P(X>=k | p) = alpha/2
        a, b = 0.0, 1.0
        for _ in range(80):
            m = (a + b) / 2
            if _binom_sf(k, n, m) < alpha / 2:
                a = m
            else:
                b = m
        lo = (a + b) / 2
    if hi is None:   # solve P(X<=k | p) = alpha/2
        a, b = 0.0, 1.0
        for _ in range(80):
            m = (a + b) / 2
            if _binom_cdf(k, n, m) > alpha / 2:
                a = m
            else:
                b = m
        hi = (a + b) / 2
    return lo, hi


def tail_report(obs, sample):
    a = np.array(sample)
    n = int(a.size)
    out = {}
    for name, k in (("lower_P(R<=obs)", int((a <= obs).sum())), ("upper_P(R>=obs)", int((a >= obs).sum()))):
        p = (k + 1) / (n + 1)
        lo, hi = clopper_pearson(k + 1, n + 1)
        out[name] = dict(k=k, n=n, plus_one_estimate=p, cp95=[lo, hi])
    return out


def sha_ints(xs):
    return hashlib.sha256(",".join(map(str, xs)).encode()).hexdigest()


# ----------------------------------------------------------------------------- graph null
def rewire(rng, edges, nswaps):
    """Degree-preserving double-edge swap. edges: list of (a,b) a<b; returns new list."""
    E = list(edges)
    S = set(a * 240 + b for a, b in E)
    m = len(E)
    done = 0
    for _ in range(nswaps):
        i, j = int(rng.integers(0, m)), int(rng.integers(0, m))
        if i == j:
            continue
        a, b = E[i]
        c, d = E[j]
        if rng.integers(0, 2):
            c, d = d, c
        # (a,b),(c,d) -> (a,d),(c,b)
        if len({a, b, c, d}) < 4:
            continue
        e1 = (min(a, d), max(a, d))
        e2 = (min(c, b), max(c, b))
        k1, k2 = e1[0] * 240 + e1[1], e2[0] * 240 + e2[1]
        if k1 in S or k2 in S:
            continue
        S.discard(a * 240 + b) if a < b else S.discard(b * 240 + a)
        k_old2 = min(c, d) * 240 + max(c, d)
        S.discard(k_old2)
        # remove old by recomputing keys from the stored pair order
        E[i] = e1
        E[j] = e2
        S.add(k1)
        S.add(k2)
        done += 1
    return E, done


def edges_to_adj(E, n):
    adj = [0] * n
    for a, b in E:
        adj[a] |= 1 << b
        adj[b] |= 1 << a
    return adj


# ----------------------------------------------------------------------------- involution search
def reflection_perm(roots, idx, alpha):
    p = []
    for v in roots:
        k = dot4(v, alpha) // 4
        p.append(idx[tuple(x - k * y for x, y in zip(v, alpha))])
    return p


def compose(p, q):  # apply q then p
    return [p[x] for x in q]


def find_fpf_involutions(roots, adj, rng, tries=4000):
    n = len(roots)
    idx = {r: i for i, r in enumerate(roots)}
    refl = {}

    def R(i):
        if i not in refl:
            refl[i] = reflection_perm(roots, idx, roots[i])
        return refl[i]

    found = {}
    counts = {}
    for _ in range(tries):
        k = int(rng.integers(1, 9))
        chosen = []
        cand = list(range(n))
        rng.shuffle(cand)
        for c in cand:
            if all(dot4(roots[c], roots[d]) == 0 for d in chosen):
                chosen.append(c)
                # forbid +-same line: negation of a chosen root has dot -8 != 0, so excluded automatically
                if len(chosen) == k:
                    break
        if len(chosen) < k:
            continue
        perm = list(range(n))
        for c in chosen:
            perm = compose(R(c), perm)
        key = tuple(perm)
        fixed = sum(1 for i in range(n) if perm[i] == i)
        inv = all(perm[perm[i]] == i for i in range(n))
        if inv and fixed == 0 and key not in found:
            found[key] = dict(k=len(chosen), automorphism=is_automorphism(perm, adj))
        counts[(len(chosen), fixed)] = counts.get((len(chosen), fixed), 0) + 1
    return found, counts


# ----------------------------------------------------------------------------- section C helpers
def decimal_fermi(E, dps=60):
    getcontext().prec = dps
    e = Decimal(repr(float(E))).exp()   # exp(E), exact decimal of the given binary64 literal
    n = Decimal(1) / (Decimal(1) + e)   # sigma(-E)
    h = Decimal(1) - n
    return dict(positive_occupation=n, complementary_hole_fraction=h, signed_contrast=n - h)


def load_frozen_ET():
    p = os.path.join(REPO, "experiments", "ns_evidence_001_claude", "outputs", "results.json")
    R = json.load(open(p))["cases"]
    ids = ["2D_N16_T0.1_dt0.002_convective", "2D_N24_T0.1_dt0.002_convective", "2D_N32_T0.1_dt0.002_convective",
           "3D_N16_T0.1_dt0.001_convective", "3D_N24_T0.1_dt0.001_convective", "3D_N32_T0.1_dt0.001_convective",
           "3D_N16_T0.5_dt0.004_convective", "3D_N16_T0.5_dt0.002_convective", "3D_N16_T0.5_dt0.001_convective"]
    return [(i, float(R[i]["E_T"])) for i in ids], hashlib.sha256(open(p, "rb").read()).hexdigest()


def file_sha(path):
    try:
        return hashlib.sha256(open(path, "rb").read()).hexdigest()
    except OSError:
        return None


def manifest(argv):
    def git(*a):
        try:
            return subprocess.check_output(("git", "-C", REPO) + a, text=True).strip()
        except Exception as e:  # noqa
            return "unavailable: %s" % e
    files = ["core/abom_v8/abom_v8_model.py", "core/geometry/e8_root_system.py",
             "experiments/ns_evidence_001_claude/outputs/results.json",
             "experiments/ns_evidence_001_cosmo/cosmo_results.json",
             "experiments/ns_abom_e8_leech_eqbit_002_claude/ns_abom_claude.py"]
    return dict(schema=SCHEMA, utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                git_head=git("rev-parse", "HEAD"), git_branch=git("rev-parse", "--abbrev-ref", "HEAD"),
                git_dirty=bool(git("status", "--porcelain")),
                python=sys.version.split()[0], numpy=np.__version__, platform=platform.platform(),
                argv=argv, seeds=SEEDS, rng="numpy PCG64, SeedSequence([seed, family_id])",
                family_id=FAMILY_ID, file_sha256={f: file_sha(os.path.join(REPO, f)) for f in files})


# ----------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true", help="smoke run: 2 seeds x 50 samples")
    ap.add_argument("--out", default=os.path.join(HERE, "outputs"))
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    seeds = SEEDS[:2] if a.quick else SEEDS
    per_seed = 50 if a.quick else 1000
    null_graphs_per_seed = 5 if a.quick else 100

    R = dict(manifest=manifest(sys.argv), quick=a.quick, per_seed=per_seed)

    # --- E8 + Gosset ---------------------------------------------------------------------
    roots = e8_roots_doubled()
    R["e8"] = check_e8(roots)
    R["e8"]["canonical_sha256"] = canonical_hash(roots)
    assert R["e8"]["count"] == 240 and R["e8"]["distinct"] and R["e8"]["all_norm2"]
    n = len(roots)
    adj, deg = gosset_adjacency(roots)
    R["gosset"] = dict(vertices=n, degree_set=sorted(set(deg)), edges=sum(deg) // 2,
                       symmetric=all(((adj[a] >> b) & 1) == ((adj[b] >> a) & 1) for a in range(n) for b in range(n)))
    assert R["gosset"]["degree_set"] == [56]
    neg = neg_perm(roots)
    R["antipodal"] = dict(involution=all(neg[neg[i]] == i for i in range(n)),
                          fixed_points=sum(1 for i in range(n) if neg[i] == i),
                          graph_automorphism=is_automorphism(neg, adj))
    assert R["antipodal"]["involution"] and R["antipodal"]["fixed_points"] == 0 and R["antipodal"]["graph_automorphism"]
    pairs = sorted({tuple(sorted((i, neg[i]))) for i in range(n)})
    assert len(pairs) == 120

    # --- rank fixtures ---------------------------------------------------------------------
    fx = fixtures_crosscheck(np.random.Generator(np.random.PCG64(12345)))
    R["rank_fixtures"] = fx
    assert all(f["ok"] for f in fx), fx

    # --- canonical antipodal partitions ------------------------------------------------------
    lexpos = [i for i, r in enumerate(roots) if next(x for x in r if x != 0) > 0]
    low_index = [p[0] for p in pairs]
    can = {}
    for name, S in (("lex_positive_first_nonzero_coord", lexpos), ("lower_index_of_pair", low_index)):
        assert len(S) == 120 and all(neg[i] not in set(S) for i in S)
        Sm = mask_of(S)
        r1 = cut_rank(adj, Sm, n)
        Tidx = [i for i in range(n) if i not in set(S)]
        r2 = rank_numpy(cut_matrix_dense(adj, S, Tidx))
        can[name] = dict(rank=r1, rank_numpy=r2, agree=(r1 == r2))
        assert r1 == r2
    R["canonical_antipodal"] = can
    obs = can["lex_positive_first_nonzero_coord"]["rank"]       # preregistered-style choice: lex-positive
    R["primary_observed_rank"] = obs

    # --- relabeling invariance (sanity) ---------------------------------------------------------
    rr = np.random.Generator(np.random.PCG64(777))
    ok = True
    for _ in range(20 if not a.quick else 5):
        perm = rr.permutation(n).tolist()   # new label of old vertex i
        adj2 = [0] * n
        for v in range(n):
            m = 0
            row = adj[v]
            while row:
                low = row & -row
                b = low.bit_length() - 1
                m |= 1 << perm[b]
                row ^= low
            adj2[perm[v]] = m
        S2 = mask_of(perm[i] for i in lexpos)
        ok &= cut_rank(adj2, S2, n) == obs
    R["relabeling_invariance_ok"] = bool(ok)

    # --- families ---------------------------------------------------------------------------------
    fam = {"transversal": [], "balanced": []}
    cross = 0
    cross_n = 0
    for s in seeds:
        rng_t = stream(s, "transversal")
        rng_b = stream(s, "balanced")
        for j in range(per_seed):
            St = sample_transversal(rng_t, pairs)
            Sb = sample_balanced(rng_b, n)
            # validate constraints
            assert bin(St).count("1") == 120 and bin(Sb).count("1") == 120
            for p in pairs:
                assert ((St >> p[0]) & 1) + ((St >> p[1]) & 1) == 1
            rt, rb_ = cut_rank(adj, St, n), cut_rank(adj, Sb, n)
            fam["transversal"].append(rt)
            fam["balanced"].append(rb_)
            if j % 97 == 0:   # cross-check against implementation 2 on a deterministic subset
                for S, r in ((St, rt), (Sb, rb_)):
                    Sidx = [i for i in range(n) if (S >> i) & 1]
                    Tidx = [i for i in range(n) if not (S >> i) & 1]
                    cross += int(rank_numpy(cut_matrix_dense(adj, Sidx, Tidx)) == r)
                    cross_n += 1
    R["rank_crosscheck_numpy_vs_int_on_samples"] = dict(agree=cross, of=cross_n)
    assert cross == cross_n

    # graph null (degree-preserving rewires), labeled as such
    edges = [(i, j) for i in range(n) for j in range(i + 1, n) if (adj[i] >> j) & 1]
    gnull = {"canonical_pairing_on_rewired": [], "transversal_on_rewired": []}
    deg_ok = True
    swaps_done = []
    Sm_can = mask_of(lexpos)
    for s in seeds:
        rng_g = stream(s, "graph_null")
        for _ in range(null_graphs_per_seed):
            E2, done = rewire(rng_g, edges, 6 * len(edges))
            swaps_done.append(done)
            adj2 = edges_to_adj(E2, n)
            deg_ok &= all(bin(x).count("1") == 56 for x in adj2)
            gnull["canonical_pairing_on_rewired"].append(cut_rank(adj2, Sm_can, n))
            gnull["transversal_on_rewired"].append(cut_rank(adj2, sample_transversal(rng_g, pairs), n))
    R["graph_null_degree_preserved"] = bool(deg_ok)
    R["graph_null_mean_swaps_done"] = float(np.mean(swaps_done))
    R["graph_null_note"] = ("degree-preserving rewires of the Gosset graph; spectrum NOT checked/preserved; "
                            "the antipodal pairing is generally not an automorphism of the rewired graphs")

    R["families"] = {}
    for k, v in list(fam.items()) + list(gnull.items()):
        R["families"][k] = dict(summary=summarize(v), sha256_ranks=sha_ints(v),
                                tails_vs_canonical=tail_report(obs, v), ranks=v)
    # primary comparisons (two): canonical vs transversal, canonical vs balanced; two-sided, Holm
    comp = []
    for k in ("transversal", "balanced"):
        t = R["families"][k]["tails_vs_canonical"]
        p2 = min(1.0, 2 * min(t["lower_P(R<=obs)"]["plus_one_estimate"], t["upper_P(R>=obs)"]["plus_one_estimate"]))
        comp.append((k, p2))
    comp.sort(key=lambda x: x[1])
    holm, run = {}, 0.0
    for i, (k, p) in enumerate(comp):
        run = max(run, min(1.0, p * (2 - i)))      # Holm step-down, monotone
        holm[k] = dict(p_unadjusted=p, p_holm=run)
    R["primary_contrasts_two_sided_plus_one"] = holm

    # --- alternative involutions -----------------------------------------------------------------
    rng_i = stream(SEEDS[0], "involution")
    found, counts = find_fpf_involutions(roots, adj, rng_i, tries=300 if a.quick else 6000)
    alt = []
    n_alt = 1000 if not a.quick else 50
    for perm, meta in found.items():
        perm = list(perm)
        prs = sorted({tuple(sorted((i, perm[i]))) for i in range(n)})
        can_idx = [p[0] for p in prs]
        rc = cut_rank(adj, mask_of(can_idx), n)
        rg = stream(SEEDS[0], "involution")
        samp = [cut_rank(adj, sample_transversal(rg, prs), n) for _ in range(n_alt)]
        # is this tau actually -1 on the nose?
        alt.append(dict(reflection_factors=meta["k"], graph_automorphism=meta["automorphism"],
                        equals_antipodal_map=(perm == neg), canonical_rank=rc,
                        transversal_summary={k: v for k, v in summarize(samp).items() if k != "histogram"},
                        canonical_vs_transversal=tail_report(rc, samp)))
    R["involutions"] = dict(
        search="random products of k mutually orthogonal root reflections (every Weyl-group involution has this form); "
               "fixed-point-free ones kept and verified as graph automorphisms",
        tries=300 if a.quick else 6000,
        distinct_fpf_found=len(found),
        distinct_not_equal_to_antipodal=sum(1 for x in alt if not x["equals_antipodal_map"]),
        outcome_counts={"k=%d,fixed=%d" % kk: vv for kk, vv in sorted(counts.items())},
        entries=alt,
        limitation=("only automorphisms of the form 'involution in W(E8) acting on roots' are searched; "
                    "this script does not prove the graph automorphism group equals W(E8)"))

    # --- Section C ---------------------------------------------------------------------------------
    (ET_pairs, ET_hash) = load_frozen_ET()
    ET = [e for _, e in ET_pairs]
    rngc = stream(SEEDS[0], "adapter")
    probes = {
        "frozen_ET": ET,
        "constant_zero": [0.0] * 9,
        "seeded_permutation": [ET[i] for i in rngc.permutation(9)],
        "seeded_shuffle_multiset": [ET[i] for i in rngc.permutation(9)],
        "range_matched_uniform": [float(x) for x in rngc.uniform(min(ET), max(ET), size=9)],
    }
    from core.abom_v8.abom_v8_model import abom_v8_sample, fermi_channels  # black-box module under test
    xyz = (1.0, 2.0, 2.0)
    C = dict(frozen_ET_source_sha256=ET_hash, frozen_ET_ids=[i for i, _ in ET_pairs], probes={})
    max_err = 0.0
    for name, vals in probes.items():
        rows = []
        for e in vals:
            smp = abom_v8_sample(*xyz, e)
            ref = decimal_fermi(e)
            f = smp["fermi"]
            errs = {k: abs(Decimal(repr(f[k])) - ref[k]) for k in ref}
            max_err = max(max_err, float(max(errs.values())))
            # closed forms: n = sigma(-E), hole = sigma(E), signed = -tanh(E/2)
            closed = dict(n=1 / (1 + math.exp(e)), signed=-math.tanh(e / 2))
            rows.append(dict(E=e, occupation=f["positive_occupation"], hole=f["complementary_hole_fraction"],
                             signed_contrast=f["signed_contrast"],
                             root_count_view=smp["e8_root_count"],
                             max_abs_err_vs_decimal60=float(max(errs.values())),
                             closed_form_signed_diff=abs(f["signed_contrast"] - closed["signed"]),
                             channels_sum_to_one=abs(f["positive_occupation"] + f["complementary_hole_fraction"] - 1) < 1e-15,
                             x_independent_fields=dict(radial_field=smp["radial_field"],
                                                       scale_coordinate=smp["scale_coordinate"])))
        C["probes"][name] = dict(values=vals, rows=rows)
    C["max_abs_err_all_channels_vs_decimal60"] = max_err
    # pointwise-map consequence: permutation/shuffle controls preserve the multiset of channel outputs
    key = lambda nm: sorted(round(r["signed_contrast"], 15) for r in C["probes"][nm]["rows"])
    C["pointwise_multiset_identical"] = dict(
        permutation=key("seeded_permutation") == key("frozen_ET"),
        shuffle=key("seeded_shuffle_multiset") == key("frozen_ET"))
    C["fermi_channel_spread"] = {nm: dict(
        occ_min=min(r["occupation"] for r in p["rows"]), occ_max=max(r["occupation"] for r in p["rows"]),
        signed_min=min(r["signed_contrast"] for r in p["rows"]), signed_max=max(r["signed_contrast"] for r in p["rows"]))
        for nm, p in C["probes"].items()}

    # ABOM-E8 identity: count and canonical root-set hash
    from core.geometry.e8_root_system import e8_roots_float
    other = e8_roots_float()
    other_doubled = []
    exact_half = True
    for r in other:
        d = []
        for x in r:
            y = 2.0 * x
            exact_half &= (y == round(y))
            d.append(int(round(y)))
        other_doubled.append(tuple(d))
    C["abom_e8_identity"] = dict(
        count_abom_module=len(other), count_mine=len(roots), count_equal=len(other) == len(roots),
        coordinates_exactly_half_integers=bool(exact_half),
        set_equal_as_sets=set(other_doubled) == set(roots),
        sha256_mine=canonical_hash(roots), sha256_module_canonicalized=canonical_hash(other_doubled),
        order_identical_to_my_lexicographic_order=(other_doubled == roots))
    C["e8_to_gosset_incidence"] = ("MINE: vertex i of my Gosset graph IS root i (adjacency = inner product 1), so the "
                                   "bijection is the identity by construction; checking the OTHER bench's graph against "
                                   "E8 requires its exposed vertex labelling: NOT_IMPLEMENTED in this independent script")
    R["section_C"] = C
    R["section_B"] = "NOT_IMPLEMENTED (requires the other bench's harness switches; not attempted)"
    R["leech"] = "NOT_RUN (rank-24 audit is outside this script; E8 and Leech certificates are not merged)"

    # --- write ----------------------------------------------------------------------------------------
    outp = os.path.join(a.out, "results_quick.json" if a.quick else "results.json")
    with open(outp, "w") as fh:
        json.dump(R, fh, indent=1, sort_keys=True, default=str)
    # determinism digest: everything but the manifest timestamp/dirty flag
    det = {k: v for k, v in R.items() if k != "manifest"}
    dig = hashlib.sha256(json.dumps(det, sort_keys=True, default=str).encode()).hexdigest()
    print("wrote", outp)
    print("deterministic_digest", dig)
    print("observed canonical rank (lex-positive):", obs, "| other convention:",
          can["lower_index_of_pair"]["rank"])
    for k, v in R["families"].items():
        s = v["summary"]
        print("%-30s n=%d min=%d max=%d mean=%.3f med=%.1f sd=%.3f" % (k, s["n"], s["min"], s["max"], s["mean"], s["median"], s["std"]))
    print("involutions:", {k: R["involutions"][k] for k in ("distinct_fpf_found", "distinct_not_equal_to_antipodal")})


if __name__ == "__main__":
    main()
