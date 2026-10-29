"""ABOM-v8 exploratory mathematical integration layer.

This module combines independently defined mathematical components for testing.
It does not claim a physical unification or a validated quantum-field model.
Python standard library only.
"""
from __future__ import annotations

from itertools import combinations, product
from math import exp, isfinite, log2, sqrt
from typing import Iterable, Sequence

PHI = (1.0 + sqrt(5.0)) / 2.0
PHI_INV = PHI - 1.0


def exponential_scale(length: float, reference_length: float = 1.0) -> float:
    """Map a positive length to a base-2 scale coordinate."""
    if not isfinite(length) or not isfinite(reference_length):
        raise ValueError("lengths must be finite")
    if length <= 0.0 or reference_length <= 0.0:
        raise ValueError("lengths must be positive")
    return log2(length / reference_length)


def inverse_exponential_scale(x: float, reference_length: float = 1.0) -> float:
    """Recover a length from a base-2 scale coordinate."""
    if not isfinite(x) or not isfinite(reference_length) or reference_length <= 0.0:
        raise ValueError("x must be finite and reference_length positive")
    value = reference_length * (2.0 ** x)
    if not isfinite(value):
        raise OverflowError("exponential scale exceeds floating-point range")
    return value


def golden_scale_branches(x: float) -> dict[str, float]:
    """Return separate phi and reciprocal-phi exponential channels."""
    base = 2.0 ** x
    return {"phi": PHI * base, "phi_inverse": PHI_INV * base,
            "phi_negative": -PHI * base, "phi_inverse_negative": -PHI_INV * base}


def fermi_occupation(energy: float, chemical_potential: float = 0.0,
                     kT: float = 1.0) -> float:
    """Fermi-Dirac occupation; kT is an energy scale and must be positive."""
    if not all(isfinite(v) for v in (energy, chemical_potential, kT)) or kT <= 0:
        raise ValueError("inputs must be finite and kT must be positive")
    q = (energy - chemical_potential) / kT
    # Stable logistic evaluation avoids overflow for large |q|.
    if q >= 0:
        e = exp(-q)
        return e / (1.0 + e)
    e = exp(q)
    return 1.0 / (1.0 + e)


def fermi_channels(energy: float, chemical_potential: float = 0.0,
                   kT: float = 1.0) -> dict[str, float]:
    """Return occupation, complementary hole fraction, and signed contrast.

    The signed contrast is relative to the complementary fraction; it is not
    a literal negative-energy sea or a negative particle count.
    """
    n = fermi_occupation(energy, chemical_potential, kT)
    hole = 1.0 - n
    return {"positive_occupation": n, "complementary_hole_fraction": hole,
            "signed_contrast": n - hole}


def e8_roots() -> tuple[tuple[float, ...], ...]:
    """Generate the 240 E8 roots in R^8, each with squared norm 2."""
    roots: list[tuple[float, ...]] = []
    # Integer roots: two nonzero entries, each +/-1 (112 roots).
    for i, j in combinations(range(8), 2):
        for si, sj in product((-1.0, 1.0), repeat=2):
            v = [0.0] * 8
            v[i], v[j] = si, sj
            roots.append(tuple(v))
    # Half-integer roots: all coordinates +/-1/2, even number of minus signs (128).
    for signs in product((-1.0, 1.0), repeat=8):
        if sum(1 for s in signs if s < 0) % 2 == 0:
            roots.append(tuple(s * 0.5 for s in signs))
    return tuple(roots)


def hyperoctahedral_action(vector: Sequence[float], permutation: Sequence[int],
                           signs: Sequence[int]) -> tuple[float, ...]:
    """Apply one signed coordinate permutation (an element of B_n)."""
    n = len(vector)
    if len(permutation) != n or len(signs) != n:
        raise ValueError("vector, permutation, and signs must have equal lengths")
    if sorted(permutation) != list(range(n)):
        raise ValueError("permutation must contain each coordinate index once")
    if any(s not in (-1, 1) for s in signs):
        raise ValueError("signs must be +1 or -1")
    return tuple(float(signs[i]) * float(vector[permutation[i]]) for i in range(n))


def hyperoctahedral_group_order(n: int = 8) -> int:
    """Order of B_n: 2^n n!; does not enumerate the group."""
    if n < 1:
        raise ValueError("n must be positive")
    result = 2 ** n
    for k in range(2, n + 1):
        result *= k
    return result


def apply_6d_basis(basis: Sequence[Sequence[float]],
                   coordinates: Sequence[float]) -> tuple[float, ...]:
    """Apply a caller-supplied 6x6 basis matrix to six coordinates."""
    if len(basis) != 6 or len(coordinates) != 6 or any(len(row) != 6 for row in basis):
        raise ValueError("basis must be 6x6 and coordinates must have length 6")
    if not all(isfinite(float(v)) for row in basis for v in row):
        raise ValueError("basis values must be finite")
    if not all(isfinite(float(v)) for v in coordinates):
        raise ValueError("coordinates must be finite")
    return tuple(sum(float(basis[i][j]) * float(coordinates[j]) for j in range(6))
                 for i in range(6))


def spatial_octants(x: float, y: float, z: float) -> dict[str, tuple[float, float, float]]:
    """Return the eight sign-reflected copies of a 3D point (octants)."""
    return {
        f"{'+' if sx > 0 else '-'}{'+' if sy > 0 else '-'}{'+' if sz > 0 else '-'}":
            (sx * abs(x), sy * abs(y), sz * abs(z))
        for sx, sy, sz in product((-1.0, 1.0), repeat=3)
    }


def radial_exponential_field(x: float, y: float, z: float) -> float:
    """Rotation/reflection-invariant field 2^r with r measured in model units."""
    r = sqrt(x * x + y * y + z * z)
    value = 2.0 ** r
    if not isfinite(value):
        raise OverflowError("radial exponential exceeds floating-point range")
    return value


def oscillator_energy_level(n: int, hbar: float = 1.0, omega: float = 1.0) -> float:
    """Dimensionless/normalized harmonic-oscillator level hbar*omega*(n+1/2)."""
    if not isinstance(n, int) or n < 0:
        raise ValueError("oscillator level n must be a nonnegative integer")
    if not isfinite(hbar) or not isfinite(omega) or hbar <= 0 or omega <= 0:
        raise ValueError("hbar and omega must be finite and positive")
    return hbar * omega * (n + 0.5)


def abom_v8_sample(x: float, y: float, z: float, energy: float,
                   chemical_potential: float = 0.0, kT: float = 1.0) -> dict:
    """Assemble an inspectable sample without collapsing distinct channels."""
    field = radial_exponential_field(x, y, z)
    fermi = fermi_channels(energy, chemical_potential, kT)
    scale_x = exponential_scale(max(sqrt(x*x + y*y + z*z), 1e-300))
    return {
        "coordinates": {"x": x, "y": y, "z": z},
        "octants": spatial_octants(x, y, z),
        "radial_field": field,
        "scale_coordinate": scale_x,
        "golden_branches": golden_scale_branches(scale_x),
        "fermi": fermi,
        "fermi_weighted_field": {
            "occupation_channel": field * fermi["positive_occupation"],
            "hole_channel": field * fermi["complementary_hole_fraction"],
            "signed_contrast_channel": field * fermi["signed_contrast"],
        },
        "e8_root_count": len(e8_roots()),
        "hyperoctahedral_B8_order": hyperoctahedral_group_order(8),
        "status": "exploratory mathematical composition; not a physical unification",
    }
