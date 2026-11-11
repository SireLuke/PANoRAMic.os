"""600-cell neighbour graph versus S^3/Fock harmonic multiplicities.

This is a clean-room translation of the supplied Claude 600-cell experiment.
Adjacency eigenspaces are ordered from largest eigenvalue downward before
comparison with Gegenbauer degrees l=0,1,...; the source script grouped
eigenvalues ascending, which reverses that comparison.
"""
from __future__ import annotations

from collections import Counter
from itertools import permutations, product
from math import sqrt


def six_hundred_cell_vertices() -> tuple[tuple[float, ...], ...]:
    phi = (1.0 + sqrt(5.0)) / 2.0
    vertices = []
    for coordinate in range(4):
        for sign in (1.0, -1.0):
            value = [0.0] * 4
            value[coordinate] = sign
            vertices.append(tuple(value))
    for signs in product((0.5, -0.5), repeat=4):
        vertices.append(tuple(signs))

    base = (phi / 2.0, 0.5, 1.0 / (2.0 * phi), 0.0)

    def permutation_parity(order):
        return sum(
            1 for i in range(4) for j in range(i + 1, 4)
            if order[i] > order[j]
        ) % 2

    for order in permutations(range(4)):
        if permutation_parity(order):
            continue
        permuted = [base[order[i]] for i in range(4)]
        for signs in product((1.0, -1.0), repeat=3):
            sign_iter = iter(signs)
            vertices.append(tuple(
                value * (next(sign_iter) if value != 0 else 1.0)
                for value in permuted
            ))

    unique = sorted({tuple(round(x, 9) for x in v) for v in vertices})
    if len(unique) != 120:
        raise AssertionError(f"600-cell must have 120 vertices, got {len(unique)}")
    if any(abs(sum(x*x for x in v) - 1.0) > 1e-8 for v in unique):
        raise AssertionError("600-cell vertices must lie on the unit S^3")
    return tuple(unique)


def gegenbauer_c_l_1(degree: int, x: float) -> float:
    """C_l^1(x), equivalently the Chebyshev polynomial U_l(x)."""
    if degree == 0:
        return 1.0
    previous, current = 1.0, 2.0 * x
    if degree == 1:
        return current
    for _ in range(1, degree):
        previous, current = current, 2.0 * x * current - previous
    return current


def six_hundred_cell_s3_spectrum() -> dict:
    import numpy as np

    phi = (1.0 + sqrt(5.0)) / 2.0
    vertices = np.asarray(six_hundred_cell_vertices(), dtype=np.float64)
    gram = vertices @ vertices.T
    adjacency = np.isclose(gram, phi / 2.0, atol=1e-8).astype(np.float64)
    np.fill_diagonal(adjacency, 0.0)
    degrees = adjacency.sum(axis=1)
    if not np.all(degrees == 12):
        raise AssertionError("600-cell nearest-neighbour graph must be 12-regular")

    eigenvalues = np.linalg.eigvalsh(adjacency)
    grouped = Counter(int(round(float(value) * 1e8)) for value in eigenvalues)
    observed = [
        {"eigenvalue": key / 1e8, "multiplicity": grouped[key]}
        for key in sorted(grouped, reverse=True)
    ]

    predictions = []
    x = phi / 2.0
    for degree in range(6):
        predicted = 12.0 * gegenbauer_c_l_1(degree, x) / (degree + 1)
        nearest = min(observed, key=lambda item: abs(item["eigenvalue"] - predicted))
        if abs(nearest["eigenvalue"] - predicted) > 1e-7:
            raise AssertionError("600-cell spectrum disagrees with Gegenbauer prediction")
        expected_multiplicity = (degree + 1) ** 2
        if nearest["multiplicity"] != expected_multiplicity:
            raise AssertionError("600-cell eigenspace multiplicity does not match S^3 harmonics")
        predictions.append({
            "harmonic_degree": degree,
            "predicted_adjacency_eigenvalue": predicted,
            "observed_adjacency_eigenvalue": nearest["eigenvalue"],
            "observed_multiplicity": nearest["multiplicity"],
            "S3_harmonic_dimension": expected_multiplicity,
        })

    return {
        "vertices": len(vertices),
        "graph_degree": 12,
        "spectrum_descending": observed,
        "low_degree_harmonic_matches": predictions,
        "matched_harmonic_degrees": 6,
        "interpretation": (
            "the first six adjacency eigenspaces, ordered from largest "
            "eigenvalue downward, match S^3 harmonic dimensions (l+1)^2"
        ),
        "scope": "finite 600-cell graph comparison; no quantum-mechanical claim",
    }


if __name__ == "__main__":
    import json
    print(json.dumps(six_hundred_cell_s3_spectrum(), indent=2, sort_keys=True))
