#!/usr/bin/env python3
"""HB-014 reproduction script (Claude bench): kernel of the positive-system cut matrix of the Gosset graph.

Experiment ID NS-ABOM-E8-LEECH-EQBIT-002-X2 (exploratory, post-hoc). Reuses ns_abom_claude.py helpers.
For a positive system P (120 roots with positive value under a generic linear functional) let
B[a,b] = A(a,-b) = [<a,b> = -1] (a,b in P), the GF(2) cut matrix of the cut (P | -P).
Checks: rank 112, kernel dim 8; zero columns; the named kernel pieces of Cosmo's HB-013 reply and the
'e0-star' (roots e0 +- e_j) of HB-014; and the kernel weight spectrum over many random positive systems."""
import itertools, json, os, sys, collections
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import ns_abom_claude as A

roots = A.e8_roots_doubled(); n = 240
adj, _ = A.gosset_adjacency(roots); neg = A.neg_perm(roots)
V = np.array(roots, float)


def cut_B(P):
    return np.array([[(adj[a] >> neg[b]) & 1 for b in P] for a in P], dtype=np.uint8)


def kernel_basis(B):
    m = B.shape[0]
    M = np.concatenate([B.copy(), np.eye(m, dtype=np.uint8)], axis=1)
    r = 0
    for c in range(m):
        p = [i for i in range(r, m) if M[i, c]]
        if not p:
            continue
        M[[r, p[0]]] = M[[p[0], r]]
        for i in range(m):
            if i != r and M[i, c]:
                M[i] ^= M[r]
        r += 1
    return r, M[r:, m:]


def weight_spectrum(K):
    w = collections.Counter()
    for coef in itertools.product((0, 1), repeat=K.shape[0]):
        if any(coef):
            v = np.zeros(K.shape[1], dtype=np.uint8)
            for c, k in zip(coef, K):
                if c:
                    v ^= k
            w[int(v.sum())] += 1
    return dict(sorted(w.items()))


out = dict(id="NS-ABOM-E8-LEECH-EQBIT-002-X2", status="EXPLORATORY_POST_HOC")
lex = [i for i, r in enumerate(roots) if next(x for x in r if x) > 0]
B = cut_B(lex); m = 120
rank, K = kernel_basis(B)
out["lex"] = dict(rank=rank, kernel_dim=int(K.shape[0]), zero_columns=[list(map(int, roots[lex[j]])) for j in range(m) if B[:, j].sum() == 0])
R = lambda l: np.array([(A.dot4(roots[l], roots[lex[j]]) // 4) % 2 for j in range(m)], dtype=np.uint8)
inK = [l for l in range(n) if R(l).any() and ((B @ R(l)) % 2 == 0).all()]
named = [R(l) for l in inK]
e = np.zeros(m, dtype=np.uint8); e[lex.index(roots.index((2, 2, 0, 0, 0, 0, 0, 0)))] = 1
star = np.array([1 if (roots[lex[j]][0] == 2 and sum(1 for x in roots[lex[j]][1:] if x) == 1) else 0 for j in range(m)], dtype=np.uint8)
out["lex"].update(
    roots_with_mod2_functional_in_kernel=len(inK),
    rank_of_functionals=A.rank_numpy(np.array(named)),
    rank_functionals_plus_e_theta=A.rank_numpy(np.array(named + [e])),
    star_weight=int(star.sum()), star_in_kernel=bool(((B @ star) % 2 == 0).all()),
    rank_functionals_plus_e_theta_plus_star=A.rank_numpy(np.array(named + [e, star])),
    kernel_weight_spectrum=weight_spectrum(K))
# many positive systems
rng = np.random.default_rng(np.random.SeedSequence([4242, 2]))
spectra = collections.Counter(); ranks = collections.Counter(); zc = collections.Counter()
NS = 100
for _ in range(NS):
    P = [i for i in range(n) if V[i] @ rng.normal(size=8) > 0] if False else None
    f = rng.normal(size=8); P = [i for i in range(n) if V[i] @ f > 0]
    Bp = cut_B(P); r, Kp = kernel_basis(Bp)
    ranks[r] += 1; zc[int((Bp.sum(0) == 0).sum())] += 1
    spectra[json.dumps(weight_spectrum(Kp), sort_keys=True)] += 1
out["random_positive_systems"] = dict(n=NS, ranks=dict(ranks), zero_column_counts=dict(zc),
                                      distinct_kernel_weight_spectra=len(spectra),
                                      lex_spectrum_matches_all=(len(spectra) == 1 and json.dumps(out["lex"]["kernel_weight_spectrum"], sort_keys=True) in spectra))
json.dump(out, open(os.path.join(HERE, "outputs", "hb014_kernel.json"), "w"), indent=1, sort_keys=True)
print(json.dumps({k: v for k, v in out.items() if k != "lex"}, indent=1))
print({k: v for k, v in out["lex"].items() if k != "kernel_weight_spectrum"})
