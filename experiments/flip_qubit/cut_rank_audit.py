#!/usr/bin/env python3
"""Independent exact cut-rank audit for the E8/Gosset graph.

No quantum dynamics is simulated. Reconstruct the 240-root Gosset graph,
verify its contract, then compare GF(2) cut ranks for the canonical
antipodal bipartition, random antipodal transversals, and arbitrary balanced cuts.
"""
from __future__ import annotations
import argparse
import itertools
import json
import random
from pathlib import Path
from statistics import median


def e8_roots_scaled():
    roots = []
    for i in range(8):
        for j in range(i + 1, 8):
            for si in (-2, 2):
                for sj in (-2, 2):
                    v = [0] * 8
                    v[i], v[j] = si, sj
                    roots.append(tuple(v))
    for signs in itertools.product((-1, 1), repeat=8):
        if signs.count(-1) % 2 == 0:
            roots.append(tuple(signs))
    if len(roots) != 240 or len(set(roots)) != 240:
        raise AssertionError("E8 root construction did not yield 240 unique roots")
    return roots


def gosset_adjacency(roots):
    adj = [set() for _ in roots]
    for i in range(len(roots)):
        for j in range(i + 1, len(roots)):
            if sum(a * b for a, b in zip(roots[i], roots[j])) == 4:
                adj[i].add(j)
                adj[j].add(i)
    return adj


def gf2_rank(rows):
    pivots = {}
    for value in rows:
        row = value
        while row:
            pivot = row.bit_length() - 1
            if pivot in pivots:
                row ^= pivots[pivot]
            else:
                pivots[pivot] = row
                break
    return len(pivots)


def cut_rank(adj, left, right):
    right_bit = {vertex: bit for bit, vertex in enumerate(right)}
    rows = []
    for vertex in left:
        bits = 0
        for neighbor in adj[vertex]:
            bit = right_bit.get(neighbor)
            if bit is not None:
                bits |= 1 << bit
        rows.append(bits)
    return gf2_rank(rows)


def canonical_antipodal_partition(roots):
    index = {root: i for i, root in enumerate(roots)}
    pairs, left, right = [], [], []
    for i, root in enumerate(roots):
        if next(x for x in root if x) > 0:
            j = index[tuple(-x for x in root)]
            pairs.append((i, j))
            left.append(i)
            right.append(j)
    if len(pairs) != 120:
        raise AssertionError("Expected exactly 120 antipodal pairs")
    return left, right, pairs


def quantiles(values):
    ordered = sorted(values)
    def nearest_rank(p):
        return ordered[max(0, min(len(ordered) - 1, int((len(ordered) - 1) * p + 0.5)))]
    return {
        "n": len(ordered), "min": ordered[0], "p05": nearest_rank(0.05),
        "median": median(ordered), "p95": nearest_rank(0.95),
        "max": ordered[-1], "mean": sum(ordered) / len(ordered),
    }


def run(samples=1000, seed=20261121):
    if samples < 1:
        raise ValueError("samples must be at least one")
    roots = e8_roots_scaled()
    adj = gosset_adjacency(roots)
    if any(len(row) != 56 for row in adj) or sum(map(len, adj)) // 2 != 6720:
        raise AssertionError("Gosset graph contract failed")
    anti_left, anti_right, pairs = canonical_antipodal_partition(roots)
    anti_rank = cut_rank(adj, anti_left, anti_right)
    rng = random.Random(seed)
    transversal_ranks, balanced_ranks = [], []
    vertices = list(range(240))
    for _ in range(samples):
        left, right = [], []
        for a, b in pairs:
            if rng.getrandbits(1):
                left.append(a); right.append(b)
            else:
                left.append(b); right.append(a)
        transversal_ranks.append(cut_rank(adj, left, right))
        arbitrary_left = rng.sample(vertices, 120)
        left_set = set(arbitrary_left)
        arbitrary_right = [v for v in vertices if v not in left_set]
        balanced_ranks.append(cut_rank(adj, arbitrary_left, arbitrary_right))
    return {
        "schema": "pan.flip_eqbit_cut_rank_audit.v1",
        "seed": seed, "samples_per_control": samples,
        "geometry": {"vertices": 240, "edges": 6720, "degree_min": 56,
                     "degree_max": 56, "antipodal_pairs": 120},
        "antipodal_cut": {
            "rank_gf2": anti_rank,
            "crossing_edges": sum(len(adj[v] & set(anti_right)) for v in anti_left),
        },
        "random_transversal_cuts": quantiles(transversal_ranks),
        "random_balanced_cuts": quantiles(balanced_ranks),
        "empirical_comparisons": {
            "antipodal_rank_at_least_transversal_fraction": sum(x <= anti_rank for x in transversal_ranks) / samples,
            "antipodal_rank_at_least_arbitrary_balanced_fraction": sum(x <= anti_rank for x in balanced_ranks) / samples,
            "note": "Seeded empirical fractions, not exact tail probabilities.",
        },
        "interpretation": [
            "Cut rank is an exact graph-state entanglement measure for the specified graph state and bipartition.",
            "Random transversals split every antipodal pair and test orientation effects.",
            "Arbitrary balanced cuts control for the antipodal-pair structure itself.",
            "Finite samples do not establish a global maximum or population-wide typical value.",
            "This is graph-state mathematics, not evidence of physical quantum dynamics or hardware.",
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=20261121)
    parser.add_argument("--output", type=Path, default=Path("flip-eqbit-cut-rank-audit.json"))
    args = parser.parse_args()
    result = run(args.samples, args.seed)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(args.output), "antipodal_rank": result["antipodal_cut"]["rank_gf2"],
        "transversal": result["random_transversal_cuts"],
        "arbitrary_balanced": result["random_balanced_cuts"],
    }, indent=2))


if __name__ == "__main__":
    main()
