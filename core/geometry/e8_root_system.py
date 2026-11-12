"""Canonical exact E8 root system shared by PAN geometry adapters.

Coordinates use Fraction so equality, norm, and root-set comparisons are exact.
The module defines the root set only; geometry engines and their audit logic
remain independent.
"""
from __future__ import annotations

from fractions import Fraction as Q
from itertools import combinations, product
from typing import Tuple

Root = Tuple[Q, ...]


def e8_roots_exact() -> tuple[Root, ...]:
    """Return all 240 E8 roots in R^8 with exact rational coordinates."""
    roots: list[Root] = []
    for i, j in combinations(range(8), 2):
        for si, sj in product((-1, 1), repeat=2):
            v = [Q(0)] * 8
            v[i], v[j] = Q(si), Q(sj)
            roots.append(tuple(v))
    for signs in product((-Q(1, 2), Q(1, 2)), repeat=8):
        if sum(value < 0 for value in signs) % 2 == 0:
            roots.append(tuple(signs))
    result = tuple(roots)
    if len(result) != 240 or len(set(result)) != 240:
        raise AssertionError("E8 root cardinality/uniqueness failure")
    if any(sum(x * x for x in root) != 2 for root in result):
        raise AssertionError("E8 root norm failure")
    return result


def e8_roots_float() -> tuple[tuple[float, ...], ...]:
    """Explicit floating-point adapter; exact roots remain canonical."""
    return tuple(tuple(float(x) for x in root) for root in e8_roots_exact())


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def e8_simple_roots_exact() -> tuple[Root, ...]:
    """Return one exact simple-root basis with the E8 Dynkin adjacency.

    The ordering is local to this basis and is documented by its Gram graph:
    alpha_3 is the trivalent node, with arms alpha_3-alpha_2-alpha_0,
    alpha_3-alpha_1, and alpha_3-alpha_4-alpha_5-alpha_6-alpha_7.
    """
    roots = (
        (Q(1, 2), Q(-1, 2), Q(-1, 2), Q(-1, 2),
         Q(-1, 2), Q(-1, 2), Q(-1, 2), Q(1, 2)),
        (Q(1), Q(1), Q(0), Q(0), Q(0), Q(0), Q(0), Q(0)),
        (Q(-1), Q(1), Q(0), Q(0), Q(0), Q(0), Q(0), Q(0)),
        (Q(0), Q(-1), Q(1), Q(0), Q(0), Q(0), Q(0), Q(0)),
        (Q(0), Q(0), Q(-1), Q(1), Q(0), Q(0), Q(0), Q(0)),
        (Q(0), Q(0), Q(0), Q(-1), Q(1), Q(0), Q(0), Q(0)),
        (Q(0), Q(0), Q(0), Q(0), Q(-1), Q(1), Q(0), Q(0)),
        (Q(0), Q(0), Q(0), Q(0), Q(0), Q(-1), Q(1), Q(0)),
    )
    root_set = set(e8_roots_exact())
    if len(set(roots)) != 8 or any(root not in root_set for root in roots):
        raise AssertionError("E8 simple-root basis is not a subset of E8 roots")
    if any(dot(root, root) != 2 for root in roots):
        raise AssertionError("E8 simple-root norm failure")
    gram = [[dot(a, b) for b in roots] for a in roots]
    expected_edges = {
        (0, 2), (1, 3), (2, 3), (3, 4),
        (4, 5), (5, 6), (6, 7),
    }
    for i in range(8):
        for j in range(8):
            expected = 2 if i == j else -1 if tuple(sorted((i, j))) in expected_edges else 0
            if gram[i][j] != expected:
                raise AssertionError("E8 simple-root Gram graph mismatch")
    return roots
