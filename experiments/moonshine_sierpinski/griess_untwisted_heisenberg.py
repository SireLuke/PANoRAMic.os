"""Exact Heisenberg-sector products for the untwisted weight-two space.

Implements only:
  * Sym^2(h(-1)) x Sym^2(h(-1)) -> Sym^2(h(-1));
  * Sym^2(h(-1)) x even norm-four momentum states -> even momentum states.

The formulas are the z^-2 coefficients of
Y(h_i(-1)h_j(-1)1,z) = :h_i(z)h_j(z):
in an orthonormal Heisenberg basis, with lattice vectors stored as integral
coordinates x and physical coordinates alpha=x/sqrt(8).

This is a partial untwisted product kernel. It does not implement
momentum x momentum, lattice cocycles, the twisted module, the orbifold
intertwiner, the full Griess product, or Monster actions.
"""
from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from typing import TypeAlias

from experiments.moonshine_sierpinski.leech_golay_construction import (
    code_words_cached,
)

OscillatorKey: TypeAlias = tuple[str, int, int]
MomentumKey: TypeAlias = tuple[str, tuple[int, ...]]
BasisKey: TypeAlias = OscillatorKey | MomentumKey
SparseVector: TypeAlias = dict[BasisKey, Fraction]


def _oscillator_pair(pair: tuple[int, int]) -> tuple[int, int]:
    if (not isinstance(pair, tuple) or len(pair) != 2
            or any(not isinstance(i, int) for i in pair)):
        raise TypeError("oscillator basis key must be a pair of integer indices")
    i, j = pair
    if not (0 <= i <= j < 24):
        raise ValueError("oscillator indices must satisfy 0 <= i <= j < 24")
    return i, j


def _validate_minimal_leech_coordinate(vector: tuple[int, ...]) -> tuple[int, ...]:
    if not isinstance(vector, tuple) or len(vector) != 24:
        raise ValueError("momentum vector must be a 24-tuple of integral coordinates")
    if any(not isinstance(value, int) for value in vector):
        raise TypeError("momentum coordinates must be integers")
    if sum(value * value for value in vector) != 32:
        raise ValueError("momentum vector must have integral squared norm 32")

    parity = vector[0] & 1
    if any((value & 1) != parity for value in vector):
        raise ValueError("coordinates do not have common parity")
    residue_word = 0
    for index, value in enumerate(vector):
        if (((value - parity) // 2) & 1):
            residue_word |= 1 << index
    if residue_word not in code_words_cached:
        raise ValueError("coordinate residue is not in the extended Golay code")
    if sum(vector) % 8 != (4 * parity) % 8:
        raise ValueError("Leech coordinate-sum congruence failed")
    return vector


def canonical_momentum_key(vector: tuple[int, ...]) -> MomentumKey:
    """Return the even momentum-state key for {alpha,-alpha}."""
    vector = _validate_minimal_leech_coordinate(vector)
    opposite = tuple(-value for value in vector)
    return ("mom", min(vector, opposite))


def oscillator_oscillator_product(
    left: tuple[int, int], right: tuple[int, int]
) -> SparseVector:
    """Compute (h_i(-1)h_j(-1)1)_1 (h_k(-1)h_l(-1)1).

    The output is a sparse exact linear combination of the 300 oscillator
    basis states. Basis states are unnormalised monomials with i <= j.
    """
    i, j = _oscillator_pair(left)
    k, l = _oscillator_pair(right)
    terms = (
        ((i, l), int(j == k)),
        ((i, k), int(j == l)),
        ((j, l), int(i == k)),
        ((j, k), int(i == l)),
    )
    result: defaultdict[BasisKey, Fraction] = defaultdict(Fraction)
    for pair, coefficient in terms:
        if coefficient:
            a, b = _oscillator_pair(tuple(sorted(pair)))
            result[("osc", a, b)] += Fraction(coefficient)
    return {key: value for key, value in result.items() if value}


def oscillator_momentum_product(
    oscillator: tuple[int, int], momentum: tuple[int, ...]
) -> SparseVector:
    """Compute the oscillator state acting on e^alpha + e^-alpha.

    For alpha=x/sqrt(8), the coefficient is (h_i,alpha)(h_j,alpha)
    = x_i*x_j/8. The same coefficient occurs for alpha and -alpha.
    """
    i, j = _oscillator_pair(oscillator)
    key = canonical_momentum_key(momentum)
    coefficient = Fraction(momentum[i] * momentum[j], 8)
    if not coefficient:
        return {}
    return {key: coefficient}


def oscillator_bilinear_form(
    left: tuple[int, int], right: tuple[int, int]
) -> Fraction:
    """Heisenberg Fock-space form on unnormalised quadratic states."""
    i, j = _oscillator_pair(left)
    k, l = _oscillator_pair(right)
    return Fraction(int(i == k and j == l) + int(i == l and j == k))


def conformal_identity_oscillator_product(
    oscillator: tuple[int, int]
) -> SparseVector:
    """Compute (omega/2)_1 a in the 300-dimensional oscillator block."""
    i, j = _oscillator_pair(oscillator)
    result: defaultdict[BasisKey, Fraction] = defaultdict(Fraction)
    for axis in range(24):
        for key, coefficient in oscillator_oscillator_product(
            (axis, axis), (i, j)
        ).items():
            result[key] += coefficient / 4
    return {key: value for key, value in result.items() if value}


def conformal_identity_momentum_product(
    momentum: tuple[int, ...]
) -> SparseVector:
    """Compute (omega/2)_1 E_[alpha] using sum alpha_i^2 = 4."""
    key = canonical_momentum_key(momentum)
    norm_numerator = sum(value * value for value in momentum)
    coefficient = Fraction(norm_numerator, 32)
    return {key: coefficient}


def untwisted_heisenberg_block_audit() -> dict:
    """Return formula-level scope and exact normalization checks."""
    sample = tuple([4, 4] + [0] * 22)
    sample_key = canonical_momentum_key(sample)
    identity_momentum = conformal_identity_momentum_product(sample)
    identity_oscillator = conformal_identity_oscillator_product((3, 17))
    return {
        "implemented_blocks": [
            "oscillator x oscillator -> oscillator",
            "oscillator x even norm-four momentum -> even norm-four momentum",
        ],
        "oscillator_basis_dimension": 300,
        "momentum_basis_dimension": 98280,
        "sample_momentum_key": sample_key,
        "sample_momentum_identity_coefficient": str(identity_momentum[sample_key]),
        "sample_oscillator_identity": {
            str(key): str(value) for key, value in identity_oscillator.items()
        },
        "momentum_x_momentum_implemented": False,
        "lattice_cocycle_implemented": False,
        "twisted_blocks_implemented": False,
        "full_griess_product_constructed": False,
        "monster_action_constructed": False,
        "scope": "exact Heisenberg sub-blocks of the untwisted weight-two product only",
    }


if __name__ == "__main__":
    import json
    print(json.dumps(untwisted_heisenberg_block_audit(), indent=2, sort_keys=True))
