"""Established-equation adapters for ABOM-v8 exploratory comparisons.

These are small, explicit model adapters. They do not make ABOM-v8 a physical
solver by themselves and do not assert a common physical theory.
"""
from __future__ import annotations

from math import exp, isfinite, log, sqrt


def radioactive_decay(initial_activity: float, decay_constant: float,
                      time: float) -> float:
    """Exponential radioactive decay A(t)=A0 exp(-lambda*t).

    decay_constant has inverse-time units; time must use the matching unit.
    """
    if not all(isfinite(v) for v in (initial_activity, decay_constant, time)):
        raise ValueError("inputs must be finite")
    if initial_activity < 0 or decay_constant < 0 or time < 0:
        raise ValueError("activity, decay constant, and time must be nonnegative")
    return initial_activity * exp(-decay_constant * time)


def decay_constant_from_half_life(half_life: float) -> float:
    """Return lambda=ln(2)/t_half, with time units inherited from half_life."""
    if not isfinite(half_life) or half_life <= 0:
        raise ValueError("half-life must be finite and positive")
    return log(2.0) / half_life


def homogeneous_gpe_stationary_amplitude(chemical_potential: float,
                                         interaction_g: float) -> float:
    """Solve the uniform stationary GPE amplitude for V=0, g>0, mu>0.

    The stationary equation is mu*psi = g*|psi|^2*psi, hence |psi|=sqrt(mu/g).
    This is an analytic homogeneous solution, not a spatial GPE PDE solver.
    """
    if not isfinite(chemical_potential) or not isfinite(interaction_g):
        raise ValueError("parameters must be finite")
    if chemical_potential <= 0 or interaction_g <= 0:
        raise ValueError("this uniform repulsive branch requires mu>0 and g>0")
    return sqrt(chemical_potential / interaction_g)


def homogeneous_gpe_residual(psi_amplitude: float, chemical_potential: float,
                             interaction_g: float) -> float:
    """Residual for the real, uniform stationary equation -mu*psi+g|psi|^2 psi=0."""
    if not all(isfinite(v) for v in (psi_amplitude, chemical_potential, interaction_g)):
        raise ValueError("inputs must be finite")
    return -chemical_potential * psi_amplitude + interaction_g * abs(psi_amplitude)**2 * psi_amplitude


def map_scalar_to_v8(value: float, coordinate: str = "f") -> dict[str, object]:
    """Place one scalar result into a named V8 channel without changing its meaning.

    This is bookkeeping/projection only: coordinate semantics and units must be
    declared by the caller before interpreting the mapped value physically.
    """
    valid = {"h", "R", "u", "d", "tau", "chi", "s", "f"}
    if coordinate not in valid:
        raise ValueError(f"coordinate must be one of {sorted(valid)}")
    if not isfinite(value):
        raise ValueError("value must be finite")
    return {
        "V8": {key: (value if key == coordinate else None) for key in
               ("h", "R", "u", "d", "tau", "chi", "s", "f")},
        "mapped_coordinate": coordinate,
        "mapping_kind": "scalar projection; not a derived physical identity",
    }
