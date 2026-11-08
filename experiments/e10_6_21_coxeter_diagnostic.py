#!/usr/bin/env python3
"""Exact Coxeter-Gram diagnostic for the 6_21 / E10 hyperbolic honeycomb.

This checks the rank-10 Coxeter simplex Gram matrix for the T_9 diagram
[3^(6,2,1)]: a trivalent tree with arms of 6, 2, and 1 edges.
It does NOT construct the infinite honeycomb or enumerate its cells.
Only Python's standard library is required.
"""
from fractions import Fraction


def build_gram(arms=(6, 2, 1)):
    """Return the exact Gram matrix for a simply-laced star tree."""
    size = 1 + sum(arms)
    adjacency = [[0] * size for _ in range(size)]
    cursor = 1
    for arm_length in arms:
        previous = 0
        for _ in range(arm_length):
            adjacency[previous][cursor] = 1
            adjacency[cursor][previous] = 1
            previous = cursor
            cursor += 1
    return [
        [
            Fraction(1 if i == j else 0) - Fraction(adjacency[i][j], 2)
            for j in range(size)
        ]
        for i in range(size)
    ]


def ldl_inertia(matrix):
    """Exact no-pivot LDL^T factorization; return signs of diagonal D."""
    n = len(matrix)
    lower = [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]
    diagonal = []
    for k in range(n):
        pivot = matrix[k][k] - sum(
            lower[k][j] * lower[k][j] * diagonal[j] for j in range(k)
        )
        if pivot == 0:
            raise ArithmeticError("Zero LDL pivot; use a pivoted exact factorization")
        diagonal.append(pivot)
        for i in range(k + 1, n):
            numerator = matrix[i][k] - sum(
                lower[i][j] * lower[k][j] * diagonal[j] for j in range(k)
            )
            lower[i][k] = numerator / pivot
    return diagonal


def main():
    gram = build_gram()
    diagonal = ldl_inertia(gram)
    positive = sum(value > 0 for value in diagonal)
    negative = sum(value < 0 for value in diagonal)
    determinant = Fraction(1)
    for value in diagonal:
        determinant *= value

    assert len(gram) == 10
    assert (positive, negative) == (9, 1), (positive, negative)
    assert determinant == Fraction(-1, 1024), determinant

    print("diagram: [3^(6,2,1)] / T_9 / E10")
    print(f"rank: {len(gram)}")
    print(f"Gram inertia: ({positive} positive, {negative} negative)")
    print(f"determinant: {determinant}")
    print("classification check: Lorentzian signature (9,1) — PASS")
    print("scope: Coxeter simplex Gram diagnostic only; no global tiling generated")


if __name__ == "__main__":
    main()
