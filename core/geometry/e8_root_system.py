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
