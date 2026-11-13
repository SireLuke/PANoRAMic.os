"""Typed reference objects for 4D celestial-amplitude kinematics.

This module implements kinematic bookkeeping and the Mellin pole of a
power-law soft factor. It does not compute scattering amplitudes or claim a
complete celestial CFT.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import isfinite
from typing import Iterable

@dataclass(frozen=True)
class CelestialPrimary:
    """Massless 4D celestial primary in a chosen color-weight basis.

    For radiative massless states, celestial spin J is identified with
    helicity. The conformal weights are h=(Delta+J)/2 and
    hbar=(Delta-J)/2. Incoming/outgoing is eta=-1/+1.
    """
    delta: complex
    helicity: float
    z: complex
    color_weight_1: float = 0.0
    color_weight_2: float = 0.0
    eta: int = 1

    def __post_init__(self) -> None:
        values = (self.delta.real, self.delta.imag, self.helicity,
                  self.z.real, self.z.imag, self.color_weight_1,
                  self.color_weight_2)
        if not all(isfinite(float(value)) for value in values):
            raise ValueError("celestial primary values must be finite")
        if self.eta not in (-1, 1):
            raise ValueError("eta must be -1 (incoming) or +1 (outgoing)")

    @property
    def celestial_spin(self) -> float:
        """For a radiative massless primary, J equals its helicity."""
        return self.helicity

    @property
    def weights(self) -> tuple[complex, complex]:
        j = complex(self.celestial_spin)
        return ((self.delta + j) / 2, (self.delta - j) / 2)


@dataclass(frozen=True)
class CelestialChart8:
    """Lossless eight-real-coordinate chart for one massless colored leg.

    Order: (Re Delta, Im Delta, helicity, Re z, Im z, q1, q2, eta).
    q1,q2 are coordinates in a caller-declared SU(3) Cartan weight basis.
    This chart is NOT PAN V8 and is NOT an E8 Cartan weight.
    """
    delta_real: float
    delta_imag: float
    helicity: float
    z_real: float
    z_imag: float
    color_weight_1: float
    color_weight_2: float
    eta: int

    def __post_init__(self) -> None:
        numeric = (self.delta_real, self.delta_imag, self.helicity,
                   self.z_real, self.z_imag, self.color_weight_1,
                   self.color_weight_2)
        if not all(isfinite(float(value)) for value in numeric):
            raise ValueError("chart coordinates must be finite")
        if self.eta not in (-1, 1):
            raise ValueError("eta coordinate must be -1 or +1")

    @classmethod
    def from_primary(cls, primary: CelestialPrimary) -> "CelestialChart8":
        return cls(primary.delta.real, primary.delta.imag, primary.helicity,
                   primary.z.real, primary.z.imag, primary.color_weight_1,
                   primary.color_weight_2, primary.eta)

    @classmethod
    def from_vector(cls, values: Iterable[float]) -> "CelestialChart8":
        vector = tuple(values)
        if len(vector) != 8:
            raise ValueError("celestial chart requires exactly eight coordinates")
        eta_value = int(vector[7])
        if float(eta_value) != float(vector[7]):
            raise ValueError("eta must be exactly -1 or +1")
        return cls(*map(float, vector[:7]), eta_value)

    def as_vector(self) -> tuple[float, ...]:
        return (self.delta_real, self.delta_imag, self.helicity,
                self.z_real, self.z_imag, self.color_weight_1,
                self.color_weight_2, float(self.eta))

    def to_primary(self) -> CelestialPrimary:
        return CelestialPrimary(complex(self.delta_real, self.delta_imag),
                                self.helicity,
                                complex(self.z_real, self.z_imag),
                                self.color_weight_1, self.color_weight_2,
                                self.eta)


@dataclass(frozen=True)
class HardInsertion:
    """One hard leg's position and one chosen color-generator matrix element."""
    z: complex
    color_component: complex

    def __post_init__(self) -> None:
        if not all(isfinite(float(value)) for value in (
            self.z.real, self.z.imag,
            self.color_component.real, self.color_component.imag,
        )):
            raise ValueError("hard insertion values must be finite")


def mellin_soft_factor(delta: complex, soft_power: int = 1,
                       cutoff: float = 1.0) -> complex:
    """IR Mellin integral of omega**(-soft_power) from 0 to cutoff.

    Integral = cutoff**(Delta-soft_power)/(Delta-soft_power).
    At the pole, use mellin_soft_residue instead of evaluating the divergence.
    """
    if not isfinite(delta.real) or not isfinite(delta.imag):
        raise ValueError("Delta must be finite")
    if not isinstance(soft_power, int) or soft_power < 1:
        raise ValueError("soft_power must be a positive integer")
    if not isfinite(cutoff) or cutoff <= 0:
        raise ValueError("cutoff must be finite and positive")
    denominator = delta - soft_power
    if denominator == 0:
        raise ZeroDivisionError("Mellin soft factor has a pole at Delta=soft_power")
    return cutoff ** denominator / denominator


def mellin_soft_residue(soft_power: int = 1,
                        amplitude_coefficient: complex = 1.0) -> complex:
    """Residue at Delta=soft_power for coefficient*omega**(-soft_power)."""
    if not isinstance(soft_power, int) or soft_power < 1:
        raise ValueError("soft_power must be a positive integer")
    if not isfinite(amplitude_coefficient.real) or not isfinite(amplitude_coefficient.imag):
        raise ValueError("amplitude coefficient must be finite")
    return amplitude_coefficient


def leading_soft_gluon_ward_kernel(
    z: complex, hard_insertions: Iterable[HardInsertion]
) -> complex:
    """Compute sum_i (T_i^a)/(z-z_i) for one fixed color component.

    This is a scalar matrix-element coefficient of the leading tree-level
    holomorphic soft-gluon current Ward identity. It omits normalization
    conventions and the full non-Abelian operator algebra.
    """
    total = 0j
    for insertion in hard_insertions:
        denominator = z - insertion.z
        if denominator == 0:
            raise ZeroDivisionError("current insertion coincides with a hard leg")
        total += insertion.color_component / denominator
    return total
