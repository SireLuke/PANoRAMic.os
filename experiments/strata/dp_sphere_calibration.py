#!/usr/bin/env python3
"""STRATA-004 analytic/Fourier calibration for a displaced uniform sphere.

This is a finite, sharp-edged sphere calibration only. It is not a nuclear
smearing prescription, an empirical result, or evidence for collapse.
"""
from __future__ import annotations
import json
import math

def analytic_coefficient(separation_over_radius: float) -> float:
    """Return E_G / (G M^2/R) for two equal uniform spheres.

    Uses eta=d/(2R). The overlapping and non-overlapping branches agree
    at eta=1 (d=2R).
    """
    x = float(separation_over_radius)
    if not math.isfinite(x) or x < 0:
        raise ValueError("separation_over_radius must be finite and nonnegative")
    eta = x / 2.0
    if eta <= 1.0:
        return 2.0 * eta**2 - 1.5 * eta**3 + 0.2 * eta**5
    return 1.2 - 1.0 / x

def sphere_form_factor(q: float) -> float:
    """Normalized Fourier transform 3(sin(q)-q cos(q))/q^3."""
    if abs(q) < 1e-4:
        q2 = q * q
        return 1.0 - q2 / 10.0 + q2 * q2 / 280.0
    return 3.0 * (math.sin(q) - q * math.cos(q)) / (q**3)

def sinc(x: float) -> float:
    if abs(x) < 1e-8:
        x2 = x * x
        return 1.0 - x2 / 6.0 + x2 * x2 / 120.0
    return math.sin(x) / x

def fourier_coefficient(separation_over_radius: float, q_max: float = 400.0, intervals: int = 800_000) -> float:
    """Numerically evaluate E_G/(G M^2/R) by independent Fourier quadrature.

    E_G = (2 G M^2)/(pi R) integral_0^infinity dq
          (1-sinc(q*d/R)) * F(q)^2.
    Composite Simpson integration truncates at q_max; callers must report
    q_max and interval count and demonstrate convergence.
    """
    x = float(separation_over_radius)
    if not math.isfinite(x) or x < 0:
        raise ValueError("separation_over_radius must be finite and nonnegative")
    if not math.isfinite(q_max) or q_max <= 0:
        raise ValueError("q_max must be finite and positive")
    if intervals < 2 or intervals % 2:
        raise ValueError("intervals must be a positive even integer >= 2")
    if x == 0:
        return 0.0
    step = q_max / intervals
    total = 0.0
    for i in range(intervals + 1):
        q = i * step
        form = sphere_form_factor(q)
        value = (1.0 - sinc(q * x)) * form * form
        weight = 1.0 if i == 0 or i == intervals else (4.0 if i % 2 else 2.0)
        total += weight * value
    integral = (step / 3.0) * total
    return (2.0 / math.pi) * integral

def run() -> dict:
    ratio = 1.0
    analytic = analytic_coefficient(ratio)
    coarse = fourier_coefficient(ratio, q_max=200.0, intervals=400_000)
    fine = fourier_coefficient(ratio, q_max=400.0, intervals=800_000)
    relative_error = abs(fine - analytic) / analytic
    convergence_delta = abs(fine - coarse)
    return {
        "run_id": "STRATA-004-DP-UNIFORM-SPHERE-001",
        "protocol": "STRATA-0.1",
        "evidence_level": "analytic-calibration-plus-numerical-software-check",
        "model": "two equal sharp uniform spheres; signed density difference rho_1-rho_2",
        "separation_over_radius": ratio,
        "analytic_coefficient_EG_over_GM2_over_R": analytic,
        "fourier_coarse": coarse,
        "fourier_fine": fine,
        "relative_error_vs_analytic": relative_error,
        "absolute_change_under_refinement": convergence_delta,
        "q_max": 400.0,
        "intervals": 800_000,
        "dimensions": {
            "analytic_overlap_reference": "pass" if abs(analytic - 0.31875) < 1e-12 else "fail",
            "independent_fourier_agreement": "pass" if relative_error < 1e-5 else "fail",
            "resolution_convergence": "pass" if convergence_delta < 1e-6 else "fail",
            "smearing_and_nuclear_density_model": "not_tested",
            "empirical_validation": "not_tested",
            "held_out_prediction": "not_tested",
        },
        "limitations": [
            "Sharp uniform-sphere analytic calibration only; no physical smearing kernel is applied.",
            "This is not an empirical test and does not validate objective collapse.",
            "Taijitu occupancy and Gosset-shell cases remain gated on this calibration and a declared smearing model.",
            "Donadi constraints must be evaluated for the exact stochastic model and mass-density cutoff; no exclusion plot is recomputed here.",
        ],
        "status": "PASS" if relative_error < 1e-5 and convergence_delta < 1e-6 else "FAIL",
    }

if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
