"""Exact 18-column grid placement of the 118 elements with their declared V8 states (numpy only).

Placement is NOT similarity-derived: (row, col) comes from element_structure.layout (Madelung). Similarity is used
only to ask how well the measured V8 channels agree with that placement.

PRE-REGISTERED before the first run (2026-11-12).
  Question: is an element's nearest neighbour in measured V8 space (s, d) closer on the grid than chance?
  Space:    (s, d) from v8_element_map, every PubChem element with both values.
  Statistic G: median Chebyshev grid distance (|d row|, |d col| max) from each element to its 1-nearest neighbour.
  Null:     element positions shuffled over the same elements, 5000 permutations, seed 20261112.
  PASS:     G below the null 1st percentile.
  Reported, not required: the ten elements with the largest neighbour grid distance ("pattern breakers").
Non-claims: grid placement is a display convention (He in column 18, La/Ac start the f-rows, Lu/Lr in group 3).
"""
from __future__ import annotations

import json

import numpy as np

try:
    from . import element_structure as E
    from . import similarity_layout as S
    from . import v8_element_map as M
except ImportError:
    import element_structure as E
    import similarity_layout as S
    import v8_element_map as M


def cells():
    out = {z: (E.layout(z)["row"], E.layout(z)["col"]) for z in range(1, 119)}
    if len(set(out.values())) != 118:
        raise ValueError("grid cells are not unique")
    return out


def records(rows):
    pos = cells()
    recs = []
    for st, r in zip(M.build_states(rows), rows):
        z = st["Z"]
        L = E.layout(z)
        recs.append({"Z": z, "Symbol": r["Symbol"], "Name": r["Name"], "row": pos[z][0], "col": pos[z][1],
                     "period": L["period"], "block": L["block"], "group": L["group"], "V8": st["V8"]})
    return recs


def _cheb(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


def neighbour_distances(recs):
    keep = [r for r in recs if r["V8"]["s"] is not None and r["V8"]["d"] is not None]
    X = np.array([[r["V8"]["s"], r["V8"]["d"]] for r in keep])
    X = (X - X.mean(0)) / X.std(0)
    nb = S.knn(X, 1)[:, 0]
    pos = np.array([[r["row"], r["col"]] for r in keep])
    return keep, nb, pos


def stat_G(nb, pos):
    d = np.maximum(np.abs(pos[:, 0] - pos[nb, 0]), np.abs(pos[:, 1] - pos[nb, 1]))
    return float(np.median(d))


def run(rows, permutations=5000, seed=S.SEED):
    recs = records(rows)
    keep, nb, pos = neighbour_distances(recs)
    G = stat_G(nb, pos)
    rng = np.random.default_rng(seed)
    null = np.array([stat_G(nb, pos[rng.permutation(len(pos))]) for _ in range(permutations)])
    dist = np.maximum(np.abs(pos[:, 0] - pos[nb, 0]), np.abs(pos[:, 1] - pos[nb, 1]))
    order = np.argsort(-dist)[:10]
    return {"n": len(keep), "G": G, "null_p1": float(np.percentile(null, 1)), "null_median": float(np.median(null)),
            "null_le_obs": int((null <= G).sum()), "passes": bool(G < np.percentile(null, 1)),
            "breakers": [(keep[i]["Symbol"], keep[nb[i]]["Symbol"], int(dist[i])) for i in order],
            "dist": {keep[i]["Symbol"]: int(dist[i]) for i in range(len(keep))}, "records": recs}


def export(recs, path):
    with open(path, "w") as f:
        json.dump({"schema": "v8_element_map v0 (declared, non-canonical); grid from element_structure.layout",
                   "elements": recs}, f, indent=1)
