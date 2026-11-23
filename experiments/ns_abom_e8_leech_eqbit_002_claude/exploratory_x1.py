#!/usr/bin/env python3
"""NS-ABOM-E8-LEECH-EQBIT-002-X1  (EXPLORATORY, post-hoc; not part of the preregistered run).

Motivated by seeing the other bench's audit after the frozen run: (i) why are all transversal cut
ranks even, (ii) is the canonical rank 112 specific to the lexicographic convention, or shared by every
'positive system' (roots with positive value under a generic linear functional)?
Reuses functions from ns_abom_claude.py (same directory)."""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import ns_abom_claude as A

roots = A.e8_roots_doubled(); n = 240
adj, _ = A.gosset_adjacency(roots); neg = A.neg_perm(roots)
pairs = sorted({tuple(sorted((i, neg[i]))) for i in range(n)})
V = np.array(roots, float)

# (i) exact reason for even rank: for a transversal (S, -S), B[u,v] = A(u,-v) = [<u,v> = -1]
# is symmetric with zero diagonal over GF(2) => alternating => even rank.
rng = np.random.Generator(np.random.PCG64(np.random.SeedSequence([4242, 1])))
sym_ok = diag_ok = True
for _ in range(200):
    S = [p[int(k)] for p, k in zip(pairs, rng.integers(0, 2, 120))]
    B = np.array([[(adj[a] >> neg[b]) & 1 for b in S] for a in S], dtype=np.uint8)
    sym_ok &= bool((B == B.T).all()); diag_ok &= bool((np.diag(B) == 0).all())

# (ii) positive systems from random generic functionals
ranks = []; mxsep = 0
for _ in range(500):
    f = rng.normal(size=8)
    val = V @ f
    S = [i for i in range(n) if val[i] > 0]
    assert len(S) == 120
    ranks.append(A.cut_rank(adj, A.mask_of(S), n))

# (iii) rank vs number of pairs flipped away from the lexicographic positive system
lexpos = [i for i, r in enumerate(roots) if next(x for x in r if x) > 0]
curve = {}
for k in (0, 1, 2, 4, 8, 16, 32, 60, 120):
    vals = []
    for _ in range(100 if k else 1):
        S = set(lexpos)
        for i in rng.choice(120, size=k, replace=False):
            v = lexpos[int(i)]; S.discard(v); S.add(neg[v])
        vals.append(A.cut_rank(adj, A.mask_of(S), n))
    curve[k] = dict(min=min(vals), mean=float(np.mean(vals)), max=max(vals))

out = dict(id="NS-ABOM-E8-LEECH-EQBIT-002-X1", status="EXPLORATORY_POST_HOC", seed_note="SeedSequence([4242,1])",
           transversal_B_symmetric_zero_diag_200_of_200=bool(sym_ok and diag_ok),
           positive_system_ranks=dict(n=500, values={str(k): int(v) for k, v in zip(*np.unique(ranks, return_counts=True))}),
           flip_curve=curve)
json.dump(out, open(os.path.join(HERE, "outputs", "exploratory_x1.json"), "w"), indent=1, sort_keys=True)
print(json.dumps(out, indent=1, sort_keys=True))
