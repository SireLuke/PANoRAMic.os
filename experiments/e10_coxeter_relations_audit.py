#!/usr/bin/env python3
"""Exact Coxeter-relation and vertex-link audit for hyperbolic E10 / 6_21.

Standard-library only. Checks the rank-10 [3^(6,2,1)] Coxeter Gram form,
all 55 defining Coxeter relations, Gram preservation by each generator,
and the finite/affine character of all rank-nine principal subdiagrams.
"""
from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from itertools import combinations
import json


def gram_from_arms(arms=(6, 2, 1)):
    size = 1 + sum(arms)
    adjacency = [[0] * size for _ in range(size)]
    cursor = 1
    for arm_length in arms:
        previous = 0
        for _ in range(arm_length):
            adjacency[previous][cursor] = 1
            adjacency[cursor][previous] = 1
            previous, cursor = cursor, cursor + 1
    return [
        [Q(int(i == j)) - Q(adjacency[i][j], 2)
         for j in range(size)]
        for i in range(size)
    ]


def determinant(matrix):
    work = [list(map(Q, row)) for row in matrix]
    n = len(work)
    result = Q(1)
    for col in range(n):
        pivot_row = next(
            (row for row in range(col, n) if work[row][col] != 0), None
        )
        if pivot_row is None:
            return Q(0)
        if pivot_row != col:
            work[col], work[pivot_row] = work[pivot_row], work[col]
            result = -result
        pivot = work[col][col]
        result *= pivot
        for row in range(col + 1, n):
            factor = work[row][col] / pivot
            for j in range(col + 1, n):
                work[row][j] -= factor * work[col][j]
    return result


def ldl_diagonal(matrix):
    n = len(matrix)
    lower = [[Q(int(i == j)) for j in range(n)] for i in range(n)]
    diagonal = []
    for k in range(n):
        pivot = matrix[k][k] - sum(
            lower[k][j] ** 2 * diagonal[j] for j in range(k)
        )
        if pivot == 0:
            return diagonal + [Q(0)]
        diagonal.append(pivot)
        for i in range(k + 1, n):
            numerator = matrix[i][k] - sum(
                lower[i][j] * lower[k][j] * diagonal[j]
                for j in range(k)
            )
            lower[i][k] = numerator / pivot
    return diagonal


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def matmul(a, b):
    return [
        [sum(a[i][k] * b[k][j] for k in range(len(b)))
         for j in range(len(b))]
        for i in range(len(a))
    ]


def identity(n):
    return [[Q(int(i == j)) for j in range(n)] for i in range(n)]


def reflection_generators(gram):
    n = len(gram)
    generators = []
    for node in range(n):
        matrix = identity(n)
        for column in range(n):
            matrix[node][column] -= 2 * gram[node][column]
        generators.append(matrix)
    return generators


def principal_minor_counts(matrix):
    counts = Counter()
    n = len(matrix)
    for size in range(1, n + 1):
        for indices in combinations(range(n), size):
            submatrix = [
                [matrix[i][j] for j in indices] for i in indices
            ]
            value = determinant(submatrix)
            counts["zero" if value == 0
                   else "positive" if value > 0 else "negative"] += 1
    return counts


def run_audit():
    gram = gram_from_arms()
    n = len(gram)
    diagonal = ldl_diagonal(gram)
    inertia = (
        sum(value > 0 for value in diagonal),
        sum(value < 0 for value in diagonal),
        sum(value == 0 for value in diagonal),
    )
    gram_det = determinant(gram)
    assert inertia == (9, 1, 0)
    assert gram_det == Q(-1, 1024)

    generators = reflection_generators(gram)
    unit = identity(n)
    relations = Counter()
    for i, generator in enumerate(generators):
        assert matmul(generator, generator) == unit
        assert matmul(
            transpose(generator), matmul(gram, generator)
        ) == gram
        relations["involution"] += 1
        relations["gram_preservation"] += 1

    for i, j in combinations(range(n), 2):
        product_ij = matmul(generators[i], generators[j])
        if gram[i][j] == Q(-1, 2):
            assert matmul(matmul(product_ij, product_ij), product_ij) == unit
            relations["adjacent_order_3"] += 1
        else:
            assert matmul(generators[i], generators[j]) == matmul(
                generators[j], generators[i]
            )
            relations["nonadjacent_commutation"] += 1

    assert sum(relations[key] for key in (
        "involution", "adjacent_order_3", "nonadjacent_commutation"
    )) == 55
    assert relations["gram_preservation"] == 10

    rank_nine = []
    for deleted in range(n):
        keep = [i for i in range(n) if i != deleted]
        submatrix = [[gram[i][j] for j in keep] for i in keep]
        d = ldl_diagonal(submatrix)
        rank_nine.append({
            "deleted_node": deleted,
            "positive_pivots": sum(x > 0 for x in d),
            "negative_pivots": sum(x < 0 for x in d),
            "zero_pivots": sum(x == 0 for x in d),
            "determinant": str(determinant(submatrix)),
        })

    # In this node convention, deleting terminal node 6 on the six-edge
    # arm leaves the affine E9 principal subdiagram.
    keep = [i for i in range(n) if i != 6]
    affine_e9 = [[gram[i][j] for j in keep] for i in keep]
    minors = principal_minor_counts(affine_e9)
    assert minors == Counter({"positive": 510, "zero": 1})
    assert sum(row["positive_pivots"] == 9 for row in rank_nine) == 9
    assert sum(row["zero_pivots"] == 1 for row in rank_nine) == 1

    return {
        "status": "PASS",
        "gram_signature": inertia,
        "gram_determinant": str(gram_det),
        "coxeter_relations": {
            "involutions": relations["involution"],
            "adjacent_order_3": relations["adjacent_order_3"],
            "nonadjacent_commutations": relations["nonadjacent_commutation"],
            "total": 55,
        },
        "generator_gram_preservation_checks": relations["gram_preservation"],
        "rank_nine_vertex_links": rank_nine,
        "affine_E9_principal_minor_counts": dict(minors),
        "scope": (
            "Exact Coxeter simplex algebra and vertex-link classification. "
            "This does not construct hyperbolic coordinates or the global "
            "6_21 honeycomb."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(run_audit(), indent=2, sort_keys=True))
