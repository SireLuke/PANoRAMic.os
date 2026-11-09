#!/usr/bin/env python3
"""Seeded random-plane control for the Gosset 4_21 Coxeter projection."""
import argparse
import json
import random
from math import sqrt

from e8_adapter import build_roots, dot


def orthonormal_plane(rng):
    basis = []
    for _ in range(2):
        vector = [rng.gauss(0.0, 1.0) for _ in range(8)]
        for previous in basis:
            coefficient = sum(a * b for a, b in zip(vector, previous))
            vector = [a - coefficient * b for a, b in zip(vector, previous)]
        norm = sqrt(sum(value * value for value in vector))
        basis.append([value / norm for value in vector])
    return basis


def build_faces(roots):
    adjacency = [set() for _ in roots]
    for i, root in enumerate(roots):
        for j in range(i + 1, len(roots)):
            if dot(root, roots[j]) == 1:
                adjacency[i].add(j)
                adjacency[j].add(i)
    faces = []
    for i in range(len(roots)):
        for j in adjacency[i]:
            if j > i:
                for k in adjacency[i].intersection(adjacency[j]):
                    if k > j:
                        faces.append((i, j, k))
    return faces


def projected_equilateral_count(roots, faces, plane, tolerance):
    projected = [
        [sum(a * b for a, b in zip(root, axis)) for axis in plane]
        for root in roots
    ]
    count = 0
    for i, j, k in faces:
        points = (projected[i], projected[j], projected[k])
        lengths = [
            sqrt(sum((points[a][q] - points[b][q]) ** 2 for q in range(2)))
            for a, b in ((0, 1), (1, 2), (2, 0))
        ]
        mean = sum(lengths) / 3
        spread = (max(lengths) - min(lengths)) / mean if mean else float("inf")
        if spread < tolerance:
            count += 1
    return count


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=20261109)
    parser.add_argument("--replicates", type=int, default=5)
    parser.add_argument("--tolerance", type=float, default=1e-8)
    args = parser.parse_args()
    if args.replicates < 1 or args.tolerance <= 0:
        parser.error("replicates and tolerance must be positive")

    roots = build_roots()
    faces = build_faces(roots)
    rng = random.Random(args.seed)
    counts = [
        projected_equilateral_count(roots, faces, orthonormal_plane(rng), args.tolerance)
        for _ in range(args.replicates)
    ]
    result = {
        "control": "random_orthonormal_2d_projection",
        "seed": args.seed,
        "replicates": args.replicates,
        "face_count": len(faces),
        "relative_side_spread_tolerance": args.tolerance,
        "equilateral_face_counts": counts,
        "status": "pass" if counts == [0] * args.replicates else "effect_observed",
        "interpretation_limit": "Finite randomized control sample; not a theorem about all projection planes.",
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "pass":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
