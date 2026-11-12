#!/usr/bin/env python3
"""Explicit complex 16x16 Spin(8) lift and asymmetric SO(8) schedule audit.

The matrices implement the complexified Euclidean Clifford representation
Cl(8,0): Hermitian gamma_i with {gamma_i,gamma_j}=2 delta_ij I.
This is a representation-level audit, not a physical rotation claim.
"""
from __future__ import annotations

import json
from math import cos, isfinite, pi, sin
from typing import Sequence

from experiments.v8_dynamic_frame_spin8_720_audit import (
    PAIR_PLANES, rotate_so8,
)

SIZE = 16
IDENTITY_2 = ((1+0j, 0j), (0j, 1+0j))
PAULI_X = ((0j, 1+0j), (1+0j, 0j))
PAULI_Y = ((0j, -1j), (1j, 0j))
PAULI_Z = ((1+0j, 0j), (0j, -1+0j))


def identity(size: int = SIZE) -> tuple[tuple[complex, ...], ...]:
    return tuple(tuple(1+0j if i == j else 0j for j in range(size)) for i in range(size))


def matmul(a, b):
    n, inner, m = len(a), len(b), len(b[0])
    if len(a[0]) != inner:
        raise ValueError("matrix dimensions do not align")
    return tuple(
        tuple(sum(a[i][k] * b[k][j] for k in range(inner)) for j in range(m))
        for i in range(n)
    )


def matadd(a, b):
    return tuple(tuple(x+y for x, y in zip(ar, br)) for ar, br in zip(a, b))


def scale(matrix, scalar: complex):
    return tuple(tuple(scalar*x for x in row) for row in matrix)


def dagger(matrix):
    return tuple(tuple(matrix[j][i].conjugate() for j in range(len(matrix)) )
                 for i in range(len(matrix[0])))


def kron(a, b):
    return tuple(
        tuple(a[i][j] * b[k][ell] for j in range(len(a[0])) for ell in range(len(b[0])))
        for i in range(len(a)) for k in range(len(b))
    )


def clifford_generators():
    """Return eight Hermitian 16x16 gamma matrices for positive Euclidean signature."""
    result = []
    for pair_index in range(4):
        prefix = [PAULI_Z] * pair_index
        suffix = [IDENTITY_2] * (3-pair_index)
        for middle in (PAULI_X, PAULI_Y):
            factors = prefix + [middle] + suffix
            matrix = factors[0]
            for factor in factors[1:]:
                matrix = kron(matrix, factor)
            result.append(matrix)
    return tuple(result)


GAMMA = clifford_generators()


def max_abs(matrix) -> float:
    return max(abs(value) for row in matrix for value in row)


def clifford_residuals() -> dict:
    ident = identity()
    square_error = max(max_abs(matadd(matmul(g, g), scale(ident, -1)))
                       for g in GAMMA)
    anticommutator_error = 0.0
    for i in range(8):
        for j in range(i+1, 8):
            anti = matadd(matmul(GAMMA[i], GAMMA[j]), matmul(GAMMA[j], GAMMA[i]))
            anticommutator_error = max(anticommutator_error, max_abs(anti))
    hermitian_error = max(max_abs(matadd(g, scale(dagger(g), -1))) for g in GAMMA)
    return {
        "dimension": SIZE,
        "generator_count": len(GAMMA),
        "gamma_square_max_error": square_error,
        "anticommutator_max_error": anticommutator_error,
        "hermitian_max_error": hermitian_error,
    }


def spinor_plane_rotation(i: int, j: int, angle_radians: float):
    """S=exp(theta/2 gamma_i gamma_j), the chosen Spin(8) lift convention."""
    if not (0 <= i < 8 and 0 <= j < 8 and i != j):
        raise ValueError("plane indices must be distinct members of 0..7")
    if not isfinite(angle_radians):
        raise ValueError("angle must be finite")
    bivector = matmul(GAMMA[i], GAMMA[j])
    return matadd(
        scale(identity(), cos(angle_radians/2)),
        scale(bivector, sin(angle_radians/2)),
    )


def spinor_lift(plane_angles_radians: Sequence[float]):
    """Lift four commuting rotations in (01),(23),(45),(67) to Spin(8)."""
    if len(plane_angles_radians) != 4:
        raise ValueError("four plane angles are required")
    result = identity()
    for (i, j), angle in zip(PAIR_PLANES, plane_angles_radians):
        result = matmul(spinor_plane_rotation(i, j, float(angle)), result)
    return result


def schedule_from_degrees(plane_angles_degrees: Sequence[float]):
    if len(plane_angles_degrees) != 4:
        raise ValueError("four plane angles are required")
    values = tuple(float(x) for x in plane_angles_degrees)
    if not all(isfinite(x) for x in values):
        raise ValueError("all plane angles must be finite")
    radians = tuple(x*pi/180.0 for x in values)
    return {
        "degrees": values,
        "radians": radians,
        "spinor_matrix": spinor_lift(radians),
        "vector_frame_determinant": 1,
    }


def conjugation_error(spinor, i: int, j: int, angle: float) -> float:
    """Check S gamma_i S^-1 against the vector-frame convention."""
    transformed = matmul(matmul(spinor, GAMMA[i]), dagger(spinor))
    expected = matadd(scale(GAMMA[i], cos(angle)), scale(GAMMA[j], -sin(angle)))
    return max_abs(matadd(transformed, scale(expected, -1)))


def run_audit() -> dict:
    ident = identity()
    gamma = clifford_residuals()

    one_turn = spinor_lift((2*pi, 0, 0, 0))
    two_turns = spinor_lift((4*pi, 0, 0, 0))
    single_360_error = max_abs(matadd(one_turn, ident))
    single_720_error = max_abs(matadd(two_turns, scale(ident, -1)))

    schedule_degrees = (60.0, 90.0, 180.0, 720.0)
    schedule = schedule_from_degrees(schedule_degrees)
    schedule_matrix = schedule["spinor_matrix"]
    unitarity_error = max_abs(matadd(matmul(dagger(schedule_matrix), schedule_matrix),
                                     scale(ident, -1)))

    test_angle = pi/3
    test_spinor = spinor_plane_rotation(0, 1, test_angle)
    action_error = conjugation_error(test_spinor, 0, 1, test_angle)

    # Four simultaneous 180-degree turns are central inversion in R^8.
    central_inversion = rotate_so8((1,2,3,4,5,6,7,8), (pi,)*4)
    central_inversion_error = max(abs(central_inversion[i] + (i+1)) for i in range(8))

    # A single coordinate reflection is O(8)\SO(8), not a Spin(8) rotation.
    reflection_determinant = -1
    central_inversion_determinant = (-1) ** 8

    result = {
        "audit": "pan_v8_spin8_explicit_clifford_multiplane_v1",
        "clifford": gamma,
        "single_plane_spin_lift": {
            "360_degree_minus_identity_max_error": single_360_error,
            "720_degree_plus_identity_max_error": single_720_error,
            "vector_action_360_degree_returns": True,
        },
        "asymmetric_schedule": {
            "plane_order": ["(0,1)", "(2,3)", "(4,5)", "(6,7)"],
            "angles_degrees": list(schedule_degrees),
            "spinor_unitarity_max_error": unitarity_error,
            "vector_frame_determinant": 1,
            "not_asserted_to_be_an_E8_lattice_automorphism": True,
        },
        "spin_vector_action": {
            "single_plane_60_degree_conjugation_max_error": action_error,
        },
        "orientation_cases": {
            "central_inversion_determinant": central_inversion_determinant,
            "four_plane_180_degree_central_inversion_max_error": central_inversion_error,
            "single_hyperplane_reflection_determinant": reflection_determinant,
            "reflection_is_not_in_SO8": True,
        },
        "interpretation_limits": [
            "The 16x16 complex matrices are an explicit Clifford/Spin(8) representation fixture, not a claim about a physical spinor field.",
            "A 720-degree single-plane loop returns the spinor matrix to +I; a 360-degree loop gives -I.",
            "Independent plane angles such as 60, 90, 180, and 720 degrees form a valid SO(8) schedule but are not thereby E8 lattice symmetries.",
            "Central inversion in eight dimensions has determinant +1; a single hyperplane reflection has determinant -1 and is outside SO(8).",
            "The Gosset origin remains fixed; radial deformation and UHFE/UDFE history coupling are separate experiments.",
        ],
    }

    tolerance = 1e-10
    if max(gamma.values()) > tolerance:
        raise AssertionError("Clifford generator identities failed")
    if single_360_error > tolerance or single_720_error > tolerance:
        raise AssertionError("Spin(8) single-plane double-cover loop failed")
    if unitarity_error > tolerance or action_error > tolerance:
        raise AssertionError("Spinor schedule unitarity/vector action failed")
    if central_inversion_error > tolerance:
        raise AssertionError("four-plane half-turn did not produce central inversion")
    return result


def main():
    print(json.dumps(run_audit(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
