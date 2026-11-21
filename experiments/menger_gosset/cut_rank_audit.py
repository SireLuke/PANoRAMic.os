#!/usr/bin/env python3
"""Exact GF(2) cut-rank audit for finite Menger retained-cell graphs.

Compares a coordinate-plane spatial partition with seeded random partitions
of exactly the same cardinality. This is graph combinatorics only; no physical
or quantum dynamics is modeled.
"""
from __future__ import annotations
import argparse
import itertools
import json
import random
from pathlib import Path
from statistics import median


def menger_cells(level: int):
    if isinstance(level, bool) or not isinstance(level, int) or level < 1:
        raise ValueError("level must be a positive integer")
    patterns = [p for p in itertools.product(range(3), repeat=3)
                if sum(x == 1 for x in p) <= 1]
    cells = [(0, 0, 0)]
    for _ in range(level):
        cells = [tuple(3 * cell[i] + pattern[i] for i in range(3))
                 for cell in cells for pattern in patterns]
    return cells


def adjacency(cells, side):
    index = {cell: i for i, cell in enumerate(cells)}
    graph = [set() for _ in cells]
    for i, cell in enumerate(cells):
        for axis in range(3):
            neighbor = list(cell)
            neighbor[axis] += 1
            if neighbor[axis] < side and tuple(neighbor) in index:
                j = index[tuple(neighbor)]
                graph[i].add(j)
                graph[j].add(i)
    return graph


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


def cut_rank(graph, left, right):
    right_bits = {vertex: bit for bit, vertex in enumerate(right)}
    rows = []
    for vertex in left:
        row = 0
        for neighbor in graph[vertex]:
            bit = right_bits.get(neighbor)
            if bit is not None:
                row |= 1 << bit
        rows.append(row)
    return gf2_rank(rows)


def summarize(values):
    ordered = sorted(values)
    def nr(p):
        return ordered[max(0, min(len(ordered)-1, round((len(ordered)-1)*p)))]
    return {"n": len(ordered), "min": ordered[0], "p05": nr(.05),
            "median": median(ordered), "p95": nr(.95), "max": ordered[-1],
            "mean": sum(ordered)/len(ordered)}


def run(levels=(1, 2), samples=1000, seed=20261121):
    if samples < 1:
        raise ValueError("samples must be positive")
    reports = []
    for level in levels:
        cells = menger_cells(level)
        side = 3 ** level
        graph = adjacency(cells, side)
        degrees = [len(row) for row in graph]
        left = [i for i, cell in enumerate(cells) if cell[0] < side // 2]
        left_set = set(left)
        right = [i for i in range(len(cells)) if i not in left_set]
        spatial_rank = cut_rank(graph, left, right)
        rng = random.Random(seed + level)
        random_ranks = []
        vertices = list(range(len(cells)))
        for _ in range(samples):
            random_left = rng.sample(vertices, len(left))
            chosen = set(random_left)
            random_right = [v for v in vertices if v not in chosen]
            random_ranks.append(cut_rank(graph, random_left, random_right))
        reports.append({
            "level": level, "grid_side": side, "vertices": len(cells),
            "edges": sum(degrees)//2,
            "degree_histogram": {str(d): degrees.count(d) for d in sorted(set(degrees))},
            "spatial_partition": {"left": len(left), "right": len(right),
                                  "axis": "x", "cut_rank_gf2": spatial_rank},
            "random_same_size_partitions": summarize(random_ranks),
            "empirical_fraction_random_rank_le_spatial":
                sum(rank <= spatial_rank for rank in random_ranks) / samples,
            "interpretation_fence":
                "A low spatial cut rank indicates a sparse/structured graph boundary; it is not physical entanglement evidence."
        })
    return {"schema": "pan.menger_spatial_cut_rank.v1", "seed": seed,
            "samples_per_level": samples, "results": reports}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--levels", type=int, nargs="+", default=[1, 2])
    parser.add_argument("--samples", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=20261121)
    parser.add_argument("--output", type=Path, default=Path("menger-spatial-cut-rank.json"))
    args = parser.parse_args()
    report = run(tuple(args.levels), args.samples, args.seed)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True)+"\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
