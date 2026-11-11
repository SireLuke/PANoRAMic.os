"""QWAVE v0: SI photon relations and temporal-resolution metadata.

This module is a measurement/metadata bridge, not a quantum solver. Planck
scales are derived reference scales; they are not imposed as measurement or
sampling limits.
"""
from __future__ import annotations

import math
from typing import Any

# Exact SI-defined constants where applicable. G is the measured Newtonian
# constant; its finite experimental uncertainty is not represented here.
SPEED_OF_LIGHT_M_S = 299_792_458.0
PLANCK_CONSTANT_J_S = 6.626_070_15e-34
REDUCED_PLANCK_CONSTANT_J_S = PLANCK_CONSTANT_J_S / (2.0 * math.pi)
NEWTONIAN_CONSTANT_M3_KG_S2 = 6.67430e-11


def _positive_finite(name: str, value: float) -> float:
    number = float(value)
    if not math.isfinite(number) or number <= 0.0:
        raise ValueError(f"{name} must be finite and greater than zero")
    return number


def planck_scales() -> dict[str, float]:
    """Return derived Planck scales in SI units (not measurement thresholds)."""
    c = SPEED_OF_LIGHT_M_S
    hbar = REDUCED_PLANCK_CONSTANT_J_S
    gravity = NEWTONIAN_CONSTANT_M3_KG_S2
    length = math.sqrt(hbar * gravity / c**3)
    time = length / c
    energy = math.sqrt(hbar * c**5 / gravity)
    return {
        "planck_length_m": length,
        "planck_time_s": time,
        "planck_energy_j": energy,
        "planck_frequency_hz": 1.0 / time,
    }


def photon_from_frequency(frequency_hz: float) -> dict[str, float]:
    """Derive vacuum photon wavelength, wave number, and energy from frequency."""
    frequency = _positive_finite("frequency_hz", frequency_hz)
    wavelength = SPEED_OF_LIGHT_M_S / frequency
    return {
        "frequency_hz": frequency,
        "wavelength_m": wavelength,
        "wavenumber_m_inv": 1.0 / wavelength,
        "angular_frequency_rad_s": 2.0 * math.pi * frequency,
        "angular_wavenumber_rad_m": 2.0 * math.pi / wavelength,
        "photon_energy_j": PLANCK_CONSTANT_J_S * frequency,
    }


def photon_from_wavelength(wavelength_m: float) -> dict[str, float]:
    """Derive vacuum photon frequency, wave number, and energy from wavelength."""
    wavelength = _positive_finite("wavelength_m", wavelength_m)
    return photon_from_frequency(SPEED_OF_LIGHT_M_S / wavelength)


def temporal_measurement_metadata(
    sample_interval_s: float,
    instrument_resolution_s: float,
    *,
    physical_time_s: float | None = None,
    timing_uncertainty_s: float | None = None,
) -> dict[str, Any]:
    """Validate temporal metadata and compare scales to Planck time.

    The Planck-time ratios are dimensionless context only. No lower bound is
    imposed on sample intervals, instrument resolution, or uncertainty.
    """
    interval = _positive_finite("sample_interval_s", sample_interval_s)
    resolution = _positive_finite("instrument_resolution_s", instrument_resolution_s)
    scales = planck_scales()

    result: dict[str, Any] = {
        "sample_interval_s": interval,
        "instrument_resolution_s": resolution,
        "planck_time_s": scales["planck_time_s"],
        "sample_interval_over_planck_time": interval / scales["planck_time_s"],
        "instrument_resolution_over_planck_time": resolution / scales["planck_time_s"],
        "planck_time_role": "derived_reference_scale_not_a_measurement_floor",
    }
    if physical_time_s is not None:
        timestamp = float(physical_time_s)
        if not math.isfinite(timestamp):
            raise ValueError("physical_time_s must be finite")
        result["physical_time_s"] = timestamp
    if timing_uncertainty_s is not None:
        uncertainty = float(timing_uncertainty_s)
        if not math.isfinite(uncertainty) or uncertainty < 0.0:
            raise ValueError("timing_uncertainty_s must be finite and nonnegative")
        result["timing_uncertainty_s"] = uncertainty
        result["timing_uncertainty_over_planck_time"] = (
            uncertainty / scales["planck_time_s"]
        )
    return result
