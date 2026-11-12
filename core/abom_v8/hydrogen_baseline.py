"""Hydrogen stationary-state baseline for QWAVE (standard library only).

Purpose: the validated Schrodinger/stationary-state reference that
``docs/QWAVE_PLANCK_SCALE_ROADMAP.md`` (deferred item 4) requires *before* any V8 or
Gosset-derived projection is compared against hydrogen. It stores amplitude, phase,
probability density and probability current as separate quantities (deferred item 2).

Scope and non-claims
--------------------
Atomic units (hbar = mu = a0 = 1). Supported states: n <= 3 (all l, all m), plus (4, 2) for the
12 a0 radial node. Infinite nuclear mass; no spin, relativistic or QED corrections. This module
imposes no E8/Gosset/V8 structure on hydrogen and asserts no new physics.

Conventions: complex spherical harmonics with the Condon-Shortley phase,
psi_nlm(r, theta, phi, t) = R_nl(r) Y_l^m(theta, phi) exp(-i E_n t),  E_n = -1/(2 n^2) hartree.
The azimuthal probability current is J_phi = (m / (r sin(theta))) |psi|^2, which is
(hbar/mu) Im(psi* grad psi) . phi_hat for a stationary state with m != 0.
"""
from __future__ import annotations

import cmath
import math

from .qwave import (PLANCK_CONSTANT_J_S, SPEED_OF_LIGHT_M_S, photon_from_frequency)

HARTREE_J = 4.3597447222060e-18      # CODATA 2018 hartree energy
BOHR_RADIUS_M = 5.29177210903e-11    # CODATA 2018 a0
RYDBERG_H_M_INV = 1.096775834e7      # hydrogen (reduced-mass) Rydberg, as in the kernel spectroscopy module

_SUPPORTED = {(1, 0), (2, 0), (2, 1), (3, 0), (3, 1), (3, 2), (4, 2)}


def _check_state(n: int, l: int, m: int) -> None:
    for name, v in (("n", n), ("l", l), ("m", m)):
        if isinstance(v, bool) or not isinstance(v, int):
            raise ValueError(f"{name} must be an integer")
    if (n, l) not in _SUPPORTED or abs(m) > l:
        raise ValueError(f"unsupported state (n={n}, l={l}, m={m})")


def radial(n: int, l: int, r: float) -> float:
    """Normalised radial function R_nl(r) (a0 = 1)."""
    _check_state(n, l, 0)
    if not (math.isfinite(r) and r >= 0.0):
        raise ValueError("r must be finite and non-negative")
    s = math.sqrt
    e = math.exp
    return {
        (1, 0): lambda x: 2.0 * e(-x),
        (2, 0): lambda x: (1 / s(2)) * (1 - x / 2) * e(-x / 2),
        (2, 1): lambda x: (1 / (2 * s(6))) * x * e(-x / 2),
        (3, 0): lambda x: (2 / (3 * s(3))) * (1 - 2 * x / 3 + 2 * x * x / 27) * e(-x / 3),
        (3, 1): lambda x: (8 / (27 * s(6))) * x * (1 - x / 6) * e(-x / 3),
        (3, 2): lambda x: (4 / (81 * s(30))) * x * x * e(-x / 3),
        (4, 2): lambda x: (1 / (64 * s(5))) * x * x * (1 - x / 12) * e(-x / 4),
    }[(n, l)](r)


def radial_nodes(n: int, l: int) -> tuple:
    """Exact radial node radii (a0); count is n - l - 1."""
    _check_state(n, l, 0)
    r3 = math.sqrt(3.0)
    return {(1, 0): (), (2, 0): (2.0,), (2, 1): (), (3, 0): (1.5 * (3 - r3), 1.5 * (3 + r3)),
            (3, 1): (6.0,), (3, 2): (), (4, 2): (12.0,)}[(n, l)]


def spherical_harmonic(l: int, m: int, theta: float, phi: float) -> complex:
    """Complex Y_l^m (Condon-Shortley), l <= 2."""
    if isinstance(l, bool) or isinstance(m, bool) or not isinstance(l, int) or not isinstance(m, int):
        raise ValueError("l and m must be integers")
    if not (0 <= l <= 2 and abs(m) <= l):
        raise ValueError("supported: l in 0..2, |m| <= l")
    st, ct = math.sin(theta), math.cos(theta)
    pi = math.pi
    a = abs(m)
    if l == 0:
        mag = 1 / (2 * math.sqrt(pi))
    elif l == 1:
        mag = math.sqrt(3 / (4 * pi)) * ct if a == 0 else math.sqrt(3 / (8 * pi)) * st
    else:
        mag = {0: math.sqrt(5 / (16 * pi)) * (3 * ct * ct - 1),
               1: math.sqrt(15 / (8 * pi)) * st * ct,
               2: math.sqrt(15 / (32 * pi)) * st * st}[a]
    sign = -1.0 if (m > 0 and a % 2 == 1) else 1.0       # Condon-Shortley: (-1)^m for m > 0
    return sign * mag * cmath.exp(1j * m * phi)


def energy_hartree(n: int) -> float:
    if isinstance(n, bool) or not isinstance(n, int) or n < 1:
        raise ValueError("n must be a positive integer")
    return -0.5 / n**2


def psi(n: int, l: int, m: int, r: float, theta: float, phi: float, t: float = 0.0) -> complex:
    """Stationary-state wavefunction with its time factor exp(-i E_n t) (atomic units)."""
    _check_state(n, l, m)
    if not math.isfinite(t):
        raise ValueError("t must be finite")
    return radial(n, l, r) * spherical_harmonic(l, m, theta, phi) * cmath.exp(-1j * energy_hartree(n) * t)


def fields(n: int, l: int, m: int, r: float, theta: float, phi: float, t: float = 0.0) -> dict:
    """Amplitude, phase, probability density and azimuthal current kept as distinct fields."""
    z = psi(n, l, m, r, theta, phi, t)
    density = abs(z) ** 2
    st = math.sin(theta)
    j_phi = (m / (r * st)) * density if (r > 0 and st > 0) else 0.0
    return {"psi": z, "amplitude": abs(z), "phase": cmath.phase(z), "density": density, "j_phi": j_phi}


def halpha_wavelength_m() -> float:
    """Photon wavelength for 3 -> 2 with the Rydberg constant, via QWAVE's photon relations."""
    e_j = HARTREE_J * (energy_hartree(3) - energy_hartree(2))
    return photon_from_frequency(e_j / PLANCK_CONSTANT_J_S)["wavelength_m"]


def halpha_rydberg_wavelength_m() -> float:
    return 1.0 / (RYDBERG_H_M_INV * (1 / 4 - 1 / 9))
