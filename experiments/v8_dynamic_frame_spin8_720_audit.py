#!/usr/bin/env python3
"""V8 dynamic-frame, Gosset invariance, and 720-degree spin-lift audit.

This is a numerical representation audit. Generic SO(8) rotations preserve the
labelled root configuration's Gram matrix, but need not be E8 lattice
automorphisms in the fixed coordinate frame. Spin signs are tracked separately.
"""
from __future__ import annotations

import json
from math import cos, exp, pi, sin, sqrt
from typing import Sequence

from core.geometry.e8_root_system import e8_roots_float

DIMENSION = 8
EXPECTED_ROOTS = 240
ORIGIN = (0.0,) * DIMENSION
PAIR_PLANES = ((0, 1), (2, 3), (4, 5), (6, 7))


def rotate_plane(vector: Sequence[float], plane: tuple[int, int], angle: float) -> tuple[float, ...]:
    """Apply an active rotation in one oriented coordinate 2-plane."""
    i, j = plane
    result = list(vector)
    c, s = cos(angle), sin(angle)
    result[i] = c * vector[i] - s * vector[j]
    result[j] = s * vector[i] + c * vector[j]
    return tuple(result)


def rotate_so8(vector: Sequence[float], angles: Sequence[float]) -> tuple[float, ...]:
    """Apply commuting rotations in the four canonical orthogonal 2-planes."""
    if len(vector) != DIMENSION or len(angles) != 4:
        raise ValueError("SO(8) frame requires eight coordinates and four plane angles")
    result = tuple(float(x) for x in vector)
    for plane, angle in zip(PAIR_PLANES, angles):
        result = rotate_plane(result, plane, float(angle))
    return result


def spin_lift_sign(angles: Sequence[float], tolerance: float = 1e-9) -> int:
    """Return the central ±1 sign for closed 2π windings in the spin lift.

    For a loop with each plane angle an integer multiple of 2π, each odd
    winding contributes -1. This records the Spin(8) double-cover sign.
    """
    if len(angles) != 4:
        raise ValueError("Spin(8) lift requires four plane angles")
    windings = []
    for angle in angles:
        turns = angle / (2.0 * pi)
        nearest = round(turns)
        if abs(turns - nearest) > tolerance:
            raise ValueError("spin_lift_sign is defined here only for closed plane loops")
        windings.append(nearest)
    return -1 if sum(windings) % 2 else 1


def radial_undulation(direction: Sequence[float], phase: float, amplitude: float = 0.1) -> tuple[float, ...]:
    """Positive radial deformation about the fixed origin (illustrative test law)."""
    if len(direction) != DIMENSION:
        raise ValueError("direction must be eight-dimensional")
    if not -0.5 < amplitude < 0.5:
        raise ValueError("amplitude must lie strictly between -0.5 and 0.5")
    norm = sqrt(sum(float(x) ** 2 for x in direction))
    if norm == 0:
        raise ValueError("direction must be nonzero")
    unit = tuple(float(x) / norm for x in direction)
    radius = exp(amplitude * sin(phase))
    return tuple(radius * x for x in unit)


def dot(a: Sequence[float], b: Sequence[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def run_audit() -> dict:
    roots = e8_roots_float()
    if len(roots) != EXPECTED_ROOTS:
        raise AssertionError(f"expected 240 roots, got {len(roots)}")

    # One-plane 720° loop: vector frame closes at 360°, spin lift at 720°.
    single_plane_360 = (2*pi, 0.0, 0.0, 0.0)
    single_plane_720 = (4*pi, 0.0, 0.0, 0.0)
    vector_360_error = max(
        abs(a-b) for a,b in zip(rotate_so8((1,0,0,0,0,0,0,0), single_plane_360),
                                 (1,0,0,0,0,0,0,0))
    )
    spin_360 = spin_lift_sign(single_plane_360)
    spin_720 = spin_lift_sign(single_plane_720)

    # A simultaneous four-plane 360° loop has even total winding and + spin sign.
    four_plane_360 = (2*pi,) * 4
    four_plane_720 = (4*pi,) * 4

    # A generic moving frame preserves all labelled pairwise products and norms.
    angles = (0.37, -0.61, 1.13, 0.29)
    moved = tuple(rotate_so8(root, angles) for root in roots)
    norm_error = max(abs(dot(a,a)-2.0) for a in moved)
    gram_error = max(
        abs(dot(moved[i], moved[j]) - dot(roots[i], roots[j]))
        for i in range(len(roots)) for j in range(i, len(roots))
    )

    inverted = tuple(tuple(-x for x in root) for root in roots)
    inversion_norm_error = max(abs(dot(a,a)-2.0) for a in inverted)
    inversion_origin_error = max(abs(x) for x in rotate_so8(ORIGIN, angles))

    # Deformation is deliberately not conflated with a rigid SO(8) action.
    samples = [radial_undulation((1,2,3,4,5,6,7,8), phase)
               for phase in (0.0, pi/2, pi, 3*pi/2, 2*pi)]
    radii = [sqrt(dot(point, point)) for point in samples]

    result = {
        "audit": "pan_v8_dynamic_frame_spin8_720_v1",
        "root_count": len(roots),
        "canonical_root_norm_squared": 2,
        "single_plane_loop": {
            "vector_360_degree_max_error": vector_360_error,
            "spin_lift_sign_at_360_degrees": spin_360,
            "spin_lift_sign_at_720_degrees": spin_720,
        },
        "four_plane_torus": {
            "spin_lift_sign_at_360_degrees": spin_lift_sign(four_plane_360),
            "spin_lift_sign_at_720_degrees": spin_lift_sign(four_plane_720),
        },
        "moving_frame": {
            "angles_radians": list(angles),
            "root_norm_max_abs_error": norm_error,
            "labelled_gram_matrix_max_abs_error": gram_error,
            "origin_max_abs_error": inversion_origin_error,
        },
        "central_inversion": {
            "dimension": 8,
            "determinant": 1,
            "maps_each_root_to_antipode": True,
            "root_norm_max_abs_error": inversion_norm_error,
        },
        "radial_undulation": {
            "positive_finite_radii": all(r > 0 and r < float("inf") for r in radii),
            "sample_radii": radii,
            "zero_amplitude_recovers_unit_radius": abs(
                sqrt(dot(radial_undulation((1,0,0,0,0,0,0,0), 0.7, 0.0),
                         radial_undulation((1,0,0,0,0,0,0,0), 0.7, 0.0))) - 1.0
            ) < 1e-12,
        },
        "interpretation_limits": [
            "A generic SO(8) frame rotation preserves norms and the labelled Gram matrix, but is not generally an E8 lattice automorphism in fixed coordinates.",
            "The 720-degree return applies to the Spin(8) lift for a single 2π plane loop; ordinary vectors return after 360 degrees.",
            "Four simultaneous 2π plane rotations have even total winding, so their spin-lift central sign is +1.",
            "Radial undulation is a separate deformation, not a rigid rotation or an established physical law.",
            "This audit does not implement a full spinor module or claim physical 720-degree rotation of the Gosset polytope."
        ],
    }
    if spin_360 != -1 or spin_720 != 1:
        raise AssertionError("single-plane Spin(8) double-cover cycle failed")
    if result["four_plane_torus"]["spin_lift_sign_at_360_degrees"] != 1:
        raise AssertionError("four-plane spin-lift parity failed")
    if norm_error > 1e-10 or gram_error > 1e-10 or inversion_norm_error > 1e-12:
        raise AssertionError("Gosset root invariants failed under frame action")
    if not result["radial_undulation"]["positive_finite_radii"]:
        raise AssertionError("radial undulation produced invalid radius")
    return result


def main() -> None:
    print(json.dumps(run_audit(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
