"""Exact rank-24 basis and unimodularity certificate for the Leech lattice.

Coordinates are integral vectors scaled by 1/sqrt(8).  The basis matrix below
is a column basis for the coordinate lattice defined by the existing
extended-Golay parity/coset congruences.  Its columns are checked against those
congruences; its exact determinant is compared with the index-derived
coordinate covolume 2^36.  The scaled Gram matrix is then checked to be
integral, even, positive definite, and determinant one.

This certifies the full lattice basis and even unimodularity.  It does not by
itself prove the minimum norm; the separate Golay/short-shell audit addresses
the shortest-vector layer.
"""
from __future__ import annotations

from pathlib import Path
import sys

# Support both direct script execution and module execution from repository root.
_REPOSITORY_ROOT = str(Path(__file__).resolve().parents[2])
if _REPOSITORY_ROOT not in sys.path:
    sys.path.insert(0, _REPOSITORY_ROOT)

from experiments.moonshine_sierpinski.leech_golay_construction import (
    extended_golay_codewords,
    golay_code_audit,
    leech_minimal_vectors,
)

# Columns are basis vectors in the integral, unscaled coordinates x.
# This upper-triangular matrix is the column-Hermite basis of the natural
# generators 2*C_i, 4(e_i-e_24), 8e_24, and (1,...,1)+4e_24.
_COORDINATE_BASIS = (
    (8,4,4,4,4,4,4,4,4,4,4,4,2,2,0,0,0,2,2,2,0,2,0,5),
    (0,4,0,0,0,0,0,0,0,0,0,0,0,2,2,0,0,0,2,2,2,0,2,1),
    (0,0,4,0,0,0,0,0,0,0,0,0,2,2,2,2,0,2,2,0,2,0,0,1),
    (0,0,0,4,0,0,0,0,0,0,0,0,0,2,2,2,2,0,2,2,0,2,0,1),
    (0,0,0,0,4,0,0,0,0,0,0,0,0,0,2,2,2,2,0,2,2,0,2,1),
    (0,0,0,0,0,4,0,0,0,0,0,0,2,2,0,2,2,0,0,2,2,0,0,1),
    (0,0,0,0,0,0,4,0,0,0,0,0,0,2,2,0,2,2,0,0,2,2,0,1),
    (0,0,0,0,0,0,0,4,0,0,0,0,0,0,2,2,0,2,2,0,0,2,2,1),
    (0,0,0,0,0,0,0,0,4,0,0,0,2,2,0,2,2,2,0,0,0,2,2,1),
    (0,0,0,0,0,0,0,0,0,4,0,0,2,0,2,0,2,0,0,2,0,2,2,1),
    (0,0,0,0,0,0,0,0,0,0,4,0,2,0,0,2,0,0,2,2,2,2,2,1),
    (0,0,0,0,0,0,0,0,0,0,0,4,2,0,0,0,2,2,2,0,2,0,2,1),
    (0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,1),
    (0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,1),
    (0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,1),
    (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,1),
    (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,1),
    (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,1),
    (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,1),
    (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,1),
    (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,1),
    (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,1),
    (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,1),
    (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1),
)


def _determinant_bareiss(matrix: tuple[tuple[int, ...], ...]) -> int:
    """Exact determinant over Z using fraction-free Bareiss elimination."""
    a = [list(row) for row in matrix]
    n = len(a)
    if any(len(row) != n for row in a):
        raise ValueError("determinant requires a square matrix")
    sign, previous = 1, 1
    for k in range(n - 1):
        if a[k][k] == 0:
            pivot = next((i for i in range(k + 1, n) if a[i][k]), None)
            if pivot is None:
                return 0
            a[k], a[pivot] = a[pivot], a[k]
            sign *= -1
        pivot_value = a[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                numerator = a[i][j] * pivot_value - a[i][k] * a[k][j]
                if numerator % previous:
                    raise ArithmeticError("Bareiss division was not exact")
                a[i][j] = numerator // previous
        for i in range(k + 1, n):
            a[i][k] = 0
        previous = pivot_value
    return sign * a[-1][-1]


def _is_coordinate_lattice_vector(
    vector: tuple[int, ...], codeword_set: frozenset[int]
) -> bool:
    parity = vector[0] % 2
    if any(value % 2 != parity for value in vector):
        return False
    residue = 0
    for i, value in enumerate(vector):
        if (((value - parity) // 2) % 2):
            residue |= 1 << i
    return residue in codeword_set and sum(vector) % 8 == (4 * parity) % 8


def leech_unimodular_basis_audit() -> dict:
    basis = _COORDINATE_BASIS
    if len(basis) != 24 or any(len(row) != 24 for row in basis):
        raise AssertionError("basis matrix must be 24 by 24")

    # The stored matrix is row-major; its columns are the 24 basis vectors.
    codeword_set = frozenset(extended_golay_codewords())
    columns = tuple(
        tuple(basis[row][column] for row in range(24))
        for column in range(24)
    )
    if not all(_is_coordinate_lattice_vector(v, codeword_set) for v in columns):
        raise AssertionError("a basis column violates Leech coordinate congruences")

    coordinate_det = _determinant_bareiss(basis)
    expected_coordinate_covolume = 1 << 36
    if abs(coordinate_det) != expected_coordinate_covolume:
        raise AssertionError("basis determinant does not match index-derived covolume")

    # G = (1/8) B^T B is the Gram matrix in the lattice's 1/sqrt(8) scale.
    gram_numerators = tuple(
        tuple(sum(basis[k][i] * basis[k][j] for k in range(24))
              for j in range(24))
        for i in range(24)
    )
    if any(value % 8 for row in gram_numerators for value in row):
        raise AssertionError("scaled Gram matrix is not integral")
    gram = tuple(tuple(value // 8 for value in row) for row in gram_numerators)
    if any(gram[i][i] % 2 for i in range(24)):
        raise AssertionError("lattice is not even")
    gram_det = _determinant_bareiss(gram)
    if gram_det != 1:
        raise AssertionError("scaled Gram determinant is not one")

    # Minimum norm lower bound from the Golay congruences:
    # p=0: x=2y. If y mod 2 is nonzero, Golay distance >=8 gives
    # sum(y_i^2)>=8 and ||x/sqrt(8)||^2>=4. If y is even, x=4z;
    # sum(z_i) is even, so nonzero z has sum(z_i^2)>=2, again norm>=4.
    # p=1: x is odd in every coordinate. If all |x_i|=1, its sign
    # pattern is either all +1 (residue 0, sum 24 !=4 mod 8), or has
    # minus signs exactly on a nonzero Golay word c. Such a word has
    # weight divisible by 4, making 24-2 wt(c) ==0 mod 8, not 4.
    # Thus at least one coordinate has |x_i|>=3 and sum(x_i^2)>=32.
    golay = golay_code_audit()
    if golay["minimum_distance"] != 8:
        raise AssertionError("minimum-norm proof requires Golay minimum distance 8")
    if any(weight % 4 for weight in golay["weight_distribution"]):
        raise AssertionError("minimum-norm proof requires Type-II weights divisible by 4")
    minimal_vectors = leech_minimal_vectors()
    if len(minimal_vectors) != 196560 or any(
        sum(value * value for value in vector) != 32
        for vector in minimal_vectors
    ):
        raise AssertionError("explicit norm-four shell witness audit failed")

    # Positive definiteness follows exactly from G=B^T B/8 and det(B)!=0.
    return {
        "rank": 24,
        "coordinate_scale": "1/sqrt(8)",
        "basis_columns_checked": 24,
        "all_columns_satisfy_golay_congruences": True,
        "coordinate_basis_determinant": coordinate_det,
        "coordinate_covolume_from_index": expected_coordinate_covolume,
        "index_factors": {
            "common_coordinate_parity": 1 << 23,
            "Golay_residue_subspace": 1 << 12,
            "coordinate_sum_congruence": 2,
        },
        "scaled_gram_integral": True,
        "scaled_gram_even": True,
        "scaled_gram_determinant": gram_det,
        "positive_definite": True,
        "even_unimodular": True,
        "minimum_norm_lower_bound": 4,
        "minimum_norm_attained": 4,
        "minimal_vectors_at_minimum": len(minimal_vectors),
        "minimum_norm_proof": (
            "Golay minimum distance 8 and Type-II weights divisible by 4 "
            "exclude every nonzero coordinate vector of lattice norm below 4"
        ),
        "scope": (
            "exact rank-24 basis, covolume, even-unimodular and minimum-norm "
            "certificate for the Golay-defined coordinate lattice"
        ),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(leech_unimodular_basis_audit(), indent=2, sort_keys=True))
