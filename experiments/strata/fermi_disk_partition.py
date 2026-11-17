"""Independent area audit of the Fractal Kernel Fermi yin-yang disk.

The source-of-truth geometry is pan-fractal-kernel/fermi_yinyang.py:
a unit disk partitioned by two semicircular boundary arcs. The decorative
lemniscate/Gerono-style eyes are excluded from the area calculation.

For delta=2N-1, the black and white semicircle diameters are
d1=1-delta and d2=1+delta. The white region is a half-disk with the
black upper semicircle removed and the white lower semicircle added:
A_white = pi/2 - pi*d1^2/8 + pi*d2^2/8 = pi*(1+delta)/2 = pi*N.
This independent verifier intentionally does not implement the eye curves.
"""
from __future__ import annotations

import math


def fermi_occupancy(x: float) -> float:
    """Fermi-Dirac occupancy for x=(E-mu)/(k_B T), with k_B absorbed into T."""
    if not math.isfinite(x):
        raise ValueError("dimensionless energy must be finite")
    if x >= 0.0:
        z = math.exp(-x)
        return z / (1.0 + z)
    z = math.exp(x)
    return 1.0 / (1.0 + z)


def energy_ratio_from_occupancy(n: float) -> float:
    if not math.isfinite(n) or not 0.0 < n < 1.0:
        raise ValueError("occupancy must be finite and strictly between 0 and 1")
    return math.log((1.0 - n) / n)


def head_diameters(n: float) -> tuple[float, float]:
    if not math.isfinite(n) or not 0.0 <= n <= 1.0:
        raise ValueError("occupancy must be finite and in [0, 1]")
    delta = 2.0 * n - 1.0
    return 1.0 - delta, 1.0 + delta


def white_area_fraction(n: float) -> float:
    """Closed-form white disk-area fraction from the two semicircle areas."""
    d_black, d_white = head_diameters(n)
    return 0.5 - d_black * d_black / 8.0 + d_white * d_white / 8.0


def black_area_fraction(n: float) -> float:
    return 1.0 - white_area_fraction(n)


def five_panel_states() -> list[dict]:
    rows = []
    for n in (0.95, 0.75, 0.50, 0.25, 0.05):
        delta = 2.0 * n - 1.0
        d_black, d_white = head_diameters(n)
        rows.append({
            "white_occupancy": n,
            "black_occupancy": 1.0 - n,
            "delta": delta,
            "dimensionless_energy_ratio": energy_ratio_from_occupancy(n),
            "black_head_diameter": d_black,
            "white_head_diameter": d_white,
            "white_area_fraction": white_area_fraction(n),
            "black_area_fraction": black_area_fraction(n),
        })
    return rows
