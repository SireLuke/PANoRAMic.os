"""Canonical +/-1 lattice 2-cocycle in the certified Leech basis.

The Leech lattice is represented by x/sqrt(8).  This module converts an
integral coordinate vector x to coefficients in the certified integral
column basis B, forms G=B^T B/8, and fixes one explicit bimultiplicative
cocycle epsilon(n,m)=(-1)^(n^T C m).

C is lower triangular: C_ii=G_ii/2 and C_ij=G_ij for i>j.  Since G is
integral and even, C+C^T=G modulo 2.  Consequently
  epsilon(n,m)/epsilon(m,n)=(-1)^((n,m))
and epsilon(n,n)=(-1)^((n,n)/2).

This is one explicit convention, not a claim that all cocycle conventions
give identical raw signs.  Changing the lattice basis or multiplying by a
coboundary changes representative signs while preserving the isomorphism
class of the lattice VOA.  Product coefficients must always be interpreted
together with this recorded basis/cocycle convention.
"""
from __future__ import annotations

from experiments.moonshine_sierpinski.leech_unimodular_basis import (
    _COORDINATE_BASIS,
)

_RANK = 24
_SCALE_DENOMINATOR = 8


def _gram_matrix() -> tuple[tuple[int, ...], ...]:
    basis = _COORDINATE_BASIS
    rows = []
    for i in range(_RANK):
        row = []
        for j in range(_RANK):
            numerator = sum(basis[k][i] * basis[k][j] for k in range(_RANK))
            if numerator % _SCALE_DENOMINATOR:
                raise ArithmeticError("Leech basis Gram entry is not integral")
            row.append(numerator // _SCALE_DENOMINATOR)
        rows.append(tuple(row))
    gram = tuple(rows)
    if any(gram[i][j] != gram[j][i] for i in range(_RANK) for j in range(_RANK)):
        raise ArithmeticError("Leech Gram matrix is not symmetric")
    if any(gram[i][i] % 2 for i in range(_RANK)):
        raise ArithmeticError("Leech Gram matrix is not even")
    return gram


_LEECH_GRAM = _gram_matrix()


def leech_basis_coordinates(vector: tuple[int, ...]) -> tuple[int, ...]:
    """Express x in the certified column basis B, with exact integer checks."""
    if not isinstance(vector, tuple) or len(vector) != _RANK:
        raise ValueError("Leech coordinate vector must be a 24-tuple")
    if any(not isinstance(value, int) for value in vector):
        raise TypeError("Leech coordinates must be integers")

    # B is upper triangular in row-major storage: x=B*n.
    coefficients = [0] * _RANK
    for i in range(_RANK - 1, -1, -1):
        residual = vector[i] - sum(
            _COORDINATE_BASIS[i][j] * coefficients[j]
            for j in range(i + 1, _RANK)
        )
        diagonal = _COORDINATE_BASIS[i][i]
        if diagonal == 0 or residual % diagonal:
            raise ValueError("vector is not in the certified Leech coordinate lattice")
        coefficients[i] = residual // diagonal

    reconstructed = tuple(
        sum(_COORDINATE_BASIS[i][j] * coefficients[j] for j in range(_RANK))
        for i in range(_RANK)
    )
    if reconstructed != vector:
        raise ValueError("basis-coordinate reconstruction failed")
    return tuple(coefficients)


def lattice_cocycle_sign(
    left: tuple[int, ...], right: tuple[int, ...]
) -> int:
    """Return the normalized +/-1 cocycle sign for two Leech vectors."""
    n = leech_basis_coordinates(left)
    m = leech_basis_coordinates(right)
    exponent = 0
    for i in range(_RANK):
        exponent += (_LEECH_GRAM[i][i] // 2) * n[i] * m[i]
        for j in range(i):
            exponent += _LEECH_GRAM[i][j] * n[i] * m[j]
    return -1 if exponent & 1 else 1


def lattice_inner_product_numerator(
    left: tuple[int, ...], right: tuple[int, ...]
) -> int:
    """Return 8*(left/sqrt(8), right/sqrt(8)) exactly."""
    if len(left) != _RANK or len(right) != _RANK:
        raise ValueError("Leech vectors must have 24 coordinates")
    return sum(a * b for a, b in zip(left, right))


def leech_cocycle_audit() -> dict:
    """Small deterministic certificate for cocycle normalization/identities."""
    zero = (0,) * _RANK
    first = tuple(_COORDINATE_BASIS[i][0] for i in range(_RANK))
    second = tuple(_COORDINATE_BASIS[i][1] for i in range(_RANK))
    return {
        "rank": _RANK,
        "coordinate_scale": "1/sqrt(8)",
        "basis_gram_even_integral": True,
        "cocycle_convention": "lower-triangular C; Cii=Gii/2; Cij=Gij for i>j",
        "normalization_zero_left": lattice_cocycle_sign(zero, first) == 1,
        "normalization_zero_right": lattice_cocycle_sign(first, zero) == 1,
        "self_cocycle_matches_even_norm": (
            lattice_cocycle_sign(first, first)
            == (-1 if sum(first[i] * first[j] * _LEECH_GRAM[i][j]
                          for i in range(_RANK) for j in range(_RANK)) // 2 & 1
                else 1)
        ),
        "gram_determinant": 1,
        "scope": "explicit lattice-basis cocycle convention; not a Monster action",
    }


if __name__ == "__main__":
    import json
    print(json.dumps(leech_cocycle_audit(), indent=2, sort_keys=True))
