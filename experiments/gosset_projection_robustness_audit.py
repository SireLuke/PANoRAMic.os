#!/usr/bin/env python3
"""Robustness audit for the E8/Gosset Coxeter-plane triangle projection.

This is a floating-point sensitivity/control experiment, not an exact proof.
The exact root-system and local-cell-star certificates remain separate.
"""
from __future__ import annotations

import json
import random
from math import sqrt

from core.geometry.e8_root_system import e8_roots_float
from experiments.gosset_sierpinski_experiment import PROJECTION

TOLERANCES = (1e-6, 1e-8, 1e-10, 1e-12)
EXPECTED_ROOTS = 240
EXPECTED_FACES = 60480
EXPECTED_COXETER_PROJECTED_COUNT = 2160


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


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


def project_roots(roots, plane):
    return [
        tuple(dot(axis, root) for axis in plane)
        for root in roots
    ]


def relative_side_spread(points):
    lengths = [
        sqrt(sum((points[a][q] - points[b][q]) ** 2 for q in range(2)))
        for a, b in ((0, 1), (1, 2), (2, 0))
    ]
    mean = sum(lengths) / 3
    return (max(lengths) - min(lengths)) / mean if mean else float("inf")


def count_equilateral(projected, faces, tolerance):
    count = 0
    for i, j, k in faces:
        if relative_side_spread((projected[i], projected[j], projected[k])) < tolerance:
            count += 1
    return count


def orthonormal_random_plane(rng):
    basis = []
    for _ in range(2):
        while True:
            vector = [rng.gauss(0.0, 1.0) for _ in range(8)]
            for previous in basis:
                coefficient = dot(vector, previous)
                vector = [x - coefficient * y for x, y in zip(vector, previous)]
            norm = sqrt(dot(vector, vector))
            if norm > 1e-12:
                basis.append([x / norm for x in vector])
                break
    return basis


def projection_gram_error(plane):
    gram = [
        [dot(plane[i], plane[j]) for j in range(2)]
        for i in range(2)
    ]
    return max(
        abs(gram[i][j] - (1.0 if i == j else 0.0))
        for i in range(2) for j in range(2)
    )


def run_audit(seed=20261111, replicates=8):
    if replicates < 1:
        raise ValueError("replicates must be positive")
    roots = list(e8_roots_float())
    if len(roots) != EXPECTED_ROOTS:
        raise AssertionError(f"expected 240 E8 roots, got {len(roots)}")
    faces = build_faces(roots)
    if len(faces) != EXPECTED_FACES:
        raise AssertionError(f"expected 60480 equilateral 8D faces, got {len(faces)}")

    coxeter_plane = [list(axis) for axis in PROJECTION]
    gram_error = projection_gram_error(coxeter_plane)
    if gram_error > 1e-10:
        raise AssertionError(f"Coxeter-plane rows are not orthonormal: {gram_error}")

    projected = project_roots(roots, coxeter_plane)
    tolerance_counts = {
        f"{tolerance:.0e}": count_equilateral(projected, faces, tolerance)
        for tolerance in TOLERANCES
    }
    canonical_count = tolerance_counts["1e-08"]
    if canonical_count != EXPECTED_COXETER_PROJECTED_COUNT:
        raise AssertionError(
            "Coxeter projection count changed at canonical 1e-8 tolerance: "
            f"{canonical_count}"
        )

    rng = random.Random(seed)
    random_counts = []
    for _ in range(replicates):
        plane = orthonormal_random_plane(rng)
        random_counts.append(
            count_equilateral(project_roots(roots, plane), faces, 1e-8)
        )
    if any(random_counts):
        raise AssertionError(
            f"random-plane control produced near-equilateral faces: {random_counts}"
        )

    return {
        "audit": "gosset_coxeter_projection_robustness_v1",
        "roots": len(roots),
        "equilateral_8d_faces": len(faces),
        "coxeter_plane_row_gram_max_abs_error": gram_error,
        "coxeter_plane_equilateral_counts_by_relative_spread_tolerance": tolerance_counts,
        "canonical_tolerance": 1e-8,
        "canonical_projected_equilateral_faces": canonical_count,
        "expected_canonical_count": EXPECTED_COXETER_PROJECTED_COUNT,
        "threshold_sensitivity_reported_not_hidden": True,
        "random_control": {
            "seed": seed,
            "replicates": replicates,
            "tolerance": 1e-8,
            "equilateral_face_counts": random_counts,
            "all_zero": all(count == 0 for count in random_counts),
        },
        "interpretation_limit": (
            "Floating-point robustness and finite randomized controls only. "
            "This does not prove uniqueness of the Coxeter plane, classify all "
            "two-planes, or replace exact E8/Gosset incidence certificates."
        ),
    }


def main():
    print(json.dumps(run_audit(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
