"""Reference-model audit for fractional Fermi seas in a 1D Bose gas.

Implements the ideal homogeneous endpoint profiles described by Zeng et al.
(2026): at cycle index ell=2,4, n(k)=1/ell for |k|<ell*k_F and zero outside.
This is a momentum/rapidity-space reference profile, not a Lieb-Liniger GHD
solver or a simulation of the experimental interaction ramps.
"""
from __future__ import annotations

from math import isfinite, sin, pi
from typing import Iterable


def ffs_parameters(ell: int, k_f: float) -> dict:
    """Return ideal homogeneous FFS parameters for cycle index ell=2 or 4."""
    if ell not in (2, 4):
        raise ValueError("this reference audit supports the reported ell=2 and ell=4 states")
    if not isfinite(k_f) or k_f <= 0:
        raise ValueError("k_f must be finite and positive")
    return {
        "cycle_index_ell": ell,
        "fractional_occupancy": 1.0 / ell,
        "momentum_cutoff": ell * k_f,
        "reference_fermi_wavevector": k_f,
        "normalization_density": k_f / pi,
        "profile": "box",
        "status": "ideal homogeneous endpoint reference profile",
    }


def fractional_fermi_occupation(k: float, ell: int, k_f: float) -> float:
    """Ideal FFS occupation n(k)=1/ell for |k|<ell*k_F; zero otherwise."""
    if not isfinite(k):
        raise ValueError("k must be finite")
    p = ffs_parameters(ell, k_f)
    if abs(k) < p["momentum_cutoff"]:
        return p["fractional_occupancy"]
    return 0.0


def ffs_momentum_profile(k_values: Iterable[float], ell: int, k_f: float) -> list[float]:
    """Evaluate the ideal box occupation on supplied momentum samples."""
    return [fractional_fermi_occupation(float(k), ell, k_f) for k in k_values]


def normalized_one_body_correlation(x: float, ell: int, k_f: float) -> float:
    """Normalized homogeneous G1(x)/G1(0)=sin(ell*kF*x)/(ell*kF*x)."""
    if not isfinite(x):
        raise ValueError("x must be finite")
    p = ffs_parameters(ell, k_f)
    z = p["momentum_cutoff"] * x
    if z == 0.0:
        return 1.0
    return sin(z) / z


def one_body_correlation(x: float, ell: int, k_f: float) -> float:
    """Homogeneous G1(x), normalized so G1(0)=density=kF/pi."""
    p = ffs_parameters(ell, k_f)
    return p["normalization_density"] * normalized_one_body_correlation(x, ell, k_f)


def ffs_diagnostics(ell: int, k_f: float, x_samples: Iterable[float]) -> dict:
    """Return observables and explicitly tentative PAN/V8 adapter fields."""
    p = ffs_parameters(ell, k_f)
    xs = [float(x) for x in x_samples]
    corr = [normalized_one_body_correlation(x, ell, k_f) for x in xs]
    return {
        **p,
        "correlation_samples_x": xs,
        "normalized_g1_samples": corr,
        "first_zero_x": pi / p["momentum_cutoff"],
        "first_minimum_x": 1.430296653124202 * pi / p["momentum_cutoff"],
        "v8_candidate_observables": {
            "h": "derive from measured phase/coherence, not from occupancy alone",
            "R": "derive from scale dependence of measured correlations",
            "u": None,
            "d": "measure entropy production separately; do not equate to 1-occupancy",
            "tau": "measure persistence/lifetime of the prepared state",
            "chi": None,
            "s": "candidate information/occupation descriptor; requires declared estimator",
            "f": "record interaction-ramp protocol and cycle count",
        },
        "v8_mapping_status": "proposal_only_no_coordinates_computed",
        "physics_status": "ideal homogeneous endpoint; no GHD ramp dynamics",
    }


def compare_with_fermi_dirac(k: float, ell: int, k_f: float,
                              temperature_energy: float,
                              chemical_potential: float) -> dict:
    """Compare FFS box occupation with conventional Fermi-Dirac occupation.

    The two distributions are intentionally kept separate: a fractional
    Fermi sea is not a thermal Fermi-Dirac distribution.
    """
    if not all(isfinite(v) for v in (k, temperature_energy, chemical_potential)):
        raise ValueError("comparison inputs must be finite")
    if temperature_energy <= 0:
        raise ValueError("temperature_energy must be positive")
    q = (k * k - chemical_potential) / temperature_energy
    if q >= 0:
        e = __import__("math").exp(-q)
        fd = e / (1.0 + e)
    else:
        e = __import__("math").exp(q)
        fd = 1.0 / (1.0 + e)
    return {
        "momentum": k,
        "fractional_fermi_sea_occupation": fractional_fermi_occupation(k, ell, k_f),
        "fermi_dirac_thermal_occupation": fd,
        "same_distribution": False,
    }
