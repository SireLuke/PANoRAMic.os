"""Exact directional moment checks for the Leech minimal shell.

The four fixed directions are intentionally transparent controls. The audit
checks exact rational projection moments, not a complete spherical-design
certificate (which requires all directions / harmonic components).
"""
from __future__ import annotations

from fractions import Fraction as Q
from math import prod

from experiments.moonshine_sierpinski.leech_golay_construction import (
    leech_minimal_vectors,
)


def reference_sphere_moment_24(m: int) -> Q:
    """E[(u.y)^(2m)] for fixed unit y and uniform u on S^23."""
    numerator = prod(2 * j - 1 for j in range(1, m + 1))
    denominator = prod(24 + 2 * j for j in range(m))
    return Q(numerator, denominator)


def reference_directions() -> dict[str, tuple[int, ...]]:
    return {
        "coordinate_axis": (1,) + (0,) * 23,
        "all_ones": (1,) * 24,
        "alternating_signs": tuple(1 if i % 2 == 0 else -1 for i in range(24)),
        "fixed_integer_probe": tuple(((i * 7) % 11) - 5 for i in range(24)),
    }


def leech_minimal_shell_directional_moments(max_even_degree: int = 12) -> dict:
    """Compare exact shell projection moments with uniform S^23 moments."""
    if max_even_degree not in (2, 4, 6, 8, 10, 12):
        raise ValueError("max_even_degree must be one of 2,4,6,8,10,12")
    vectors = leech_minimal_vectors()
    directions = reference_directions()
    output = {}
    for name, direction in directions.items():
        norm_sq = sum(x * x for x in direction)
        if norm_sq == 0:
            raise AssertionError("test direction cannot be zero")
        dots = [sum(a * b for a, b in zip(vector, direction))
                for vector in vectors]
        degrees = {}
        for degree in range(2, max_even_degree + 1, 2):
            m = degree // 2
            denominator = (32 * norm_sq) ** m
            observed = Q(sum(value ** degree for value in dots),
                         len(vectors) * denominator)
            expected = reference_sphere_moment_24(m)
            degrees[str(degree)] = {
                "observed": str(observed),
                "uniform_sphere": str(expected),
                "exact_match": observed == expected,
            }
        output[name] = degrees

    return {
        "point_count": len(vectors),
        "integral_minimal_vector_norm_squared": 32,
        "lattice_minimal_norm_squared": 4,
        "directions": output,
        "interpretation": (
            "exact directional moment agreement through degree 10 on four "
            "fixed directions; degree 12 distinguishes each tested direction. "
            "This is a finite directional diagnostic, not a complete "
            "spherical-design proof."
        ),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(leech_minimal_shell_directional_moments(), indent=2, sort_keys=True))
