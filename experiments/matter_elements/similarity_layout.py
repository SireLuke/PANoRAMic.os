"""Property-similarity test of the periodic structure (numpy only).

PRE-REGISTERED before the first run (2026-11-12).
Question: do measured properties alone, with no use of Z, group, period or electron configuration,
place elements near others of the same GroupBlock and, for s/p-block elements, the same group?
Features (fixed): Electronegativity, AtomicRadius, IonizationEnergy, MeltingPoint, BoilingPoint, Density.
Excluded on purpose: AtomicMass (monotone in Z), ElectronConfiguration (circular), ElectronAffinity (61 of 118 missing).
Transforms: log10 of MeltingPoint, BoilingPoint, Density, then z-score. Complete cases only, no imputation.
Metric A: mean fraction of each element's 3 nearest neighbours (Euclidean) sharing its GroupBlock.
Metric B: macro-average of A over blocks with >= 3 complete elements (reported only).
Metric C: for s/p-block elements with a layout group (H excluded), fraction of 1-nearest-neighbours sharing the group.
Null: labels shuffled across the same elements. PASS if A and C each exceed the 99th percentile of their nulls.
No V8 mapping is used or implied: a V8 feature map would have to be declared separately.
"""
from __future__ import annotations

import math

import numpy as np

try:
    from . import element_structure as E
except ImportError:
    import element_structure as E

FEATURES = ("Electronegativity", "AtomicRadius", "IonizationEnergy", "MeltingPoint", "BoilingPoint", "Density")
LOG_FEATURES = {"MeltingPoint", "BoilingPoint", "Density"}
SEED = 20261112


def build(rows, features=FEATURES):
    keep = [r for r in rows if all(r[f] != "" for f in features)]
    X = np.array([[math.log10(float(r[f])) if f in LOG_FEATURES else float(r[f]) for f in features] for r in keep])
    return keep, (X - X.mean(0)) / X.std(0)


def knn(X, k):
    d = np.linalg.norm(X[:, None] - X[None], axis=2)
    np.fill_diagonal(d, np.inf)
    return np.argsort(d, axis=1)[:, :k]


def purity(nb, labels):
    lab = np.asarray(labels)
    return float(np.mean([(lab[nb[i]] == lab[i]).mean() for i in range(len(lab))]))


def macro_recall(nb, labels, min_n=3):
    lab = np.asarray(labels)
    vals = [np.mean([(lab[nb[i]] == b).mean() for i in np.where(lab == b)[0]])
            for b in sorted(set(lab)) if (lab == b).sum() >= min_n]
    return float(np.mean(vals)), len(vals)


def _null(fn, labels, trials, rng):
    lab = np.array(labels)
    return np.array([fn(rng.permutation(lab)) for _ in range(trials)])


def run(rows, permutations=5000, seed=SEED):
    rng = np.random.default_rng(seed)
    keep, X = build(rows)
    blocks = [r["GroupBlock"] for r in keep]
    nb3 = knn(X, 3)
    A = purity(nb3, blocks)
    nullA = _null(lambda l: purity(nb3, l), blocks, permutations, rng)
    B, n_blocks = macro_recall(nb3, blocks)
    zs = [int(r["AtomicNumber"]) for r in keep]
    sel, groups = [], []
    for i, z in enumerate(zs):
        L = E.layout(z)
        if z != 1 and L["block"] in ("s", "p"):
            sel.append(i)
            groups.append(L["group"])
    nb1 = knn(X[sel], 1)
    C = purity(nb1, groups)
    nullC = _null(lambda l: purity(nb1, l), groups, permutations, rng)
    return {"complete_cases": len(keep), "A": A, "A_null_p99": float(np.percentile(nullA, 99)),
            "A_null_ge_obs": int((nullA >= A).sum()), "B": B, "B_blocks": n_blocks,
            "C": C, "C_n": len(sel), "C_null_p99": float(np.percentile(nullC, 99)),
            "C_null_ge_obs": int((nullC >= C).sum()),
            "passes": bool(A > np.percentile(nullA, 99) and C > np.percentile(nullC, 99)),
            "symbols": [r["Symbol"] for r in keep], "blocks": blocks, "X": X}


def pca_layout(X):
    U, S, _ = np.linalg.svd(X - X.mean(0), full_matrices=False)
    return U[:, :2] * S[:2], (S ** 2 / (S ** 2).sum())[:2]
