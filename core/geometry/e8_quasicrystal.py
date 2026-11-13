"""Experimental E8 cut-and-project model with a breathing/phason window.

The split here is a simple orthogonal golden-block 4+4 decomposition. It is
NOT the canonical Elser-Sloane H4-invariant projection. Only finite E8 shells
are enumerated; this is not an infinite model-set generator.
"""
from __future__ import annotations
from dataclasses import dataclass
from itertools import product
from math import exp, isfinite, sin, sqrt
from typing import Sequence

PHI = (1.0 + sqrt(5.0)) / 2.0
SPLIT_NORM = sqrt(1.0 + PHI * PHI)
DIMENSION = 8


def e8_lattice_shell_doubled(n: int) -> tuple[tuple[int, ...], ...]:
    """Doubled integer coordinates for E8 vectors of norm squared 2n.

    Supports the first three nonzero shells (240, 2160, 6720 points), matching
    the repository's exact shell audit. Divide coordinates by two to recover
    conventional E8 lattice coordinates.
    """
    if not isinstance(n, int) or n not in (1, 2, 3):
        raise ValueError("supported shell indices are 1, 2, and 3")
    target = 8 * n
    shell: set[tuple[int, ...]] = set()
    for x in product(range(-2, 3), repeat=8):
        if sum(x) % 2 == 0 and 4 * sum(v * v for v in x) == target:
            shell.add(tuple(2 * v for v in x))
    for z in product((-3, -1, 1, 3), repeat=8):
        if sum(v * v for v in z) == target and sum(z) % 4 == 0:
            shell.add(tuple(z))
    result = tuple(sorted(shell))
    expected = {1: 240, 2: 2160, 3: 6720}[n]
    if len(result) != expected:
        raise AssertionError(f"E8 shell {n}: expected {expected}, got {len(result)}")
    if any(sum(value * value for value in point) != target for point in result):
        raise AssertionError("doubled E8 shell norm mismatch")
    return result


def golden_4plus4_split(
    vector: Sequence[float],
) -> tuple[tuple[float, ...], tuple[float, ...]]:
    """Orthogonally split R8 into two R4 charts using the golden ratio.

    For x=(a,b):
      x_parallel = (a + phi*b)/sqrt(1+phi^2)
      x_perp     = (phi*a - b)/sqrt(1+phi^2)

    This is a generic irrational golden split, not the Elser-Sloane H4 split.
    """
    if len(vector) != DIMENSION:
        raise ValueError("golden 4+4 split requires an eight-vector")
    if not all(isfinite(float(value)) for value in vector):
        raise ValueError("vector coordinates must be finite")
    a = tuple(float(value) for value in vector[:4])
    b = tuple(float(value) for value in vector[4:])
    parallel = tuple((a[i] + PHI * b[i]) / SPLIT_NORM for i in range(4))
    perpendicular = tuple((PHI * a[i] - b[i]) / SPLIT_NORM for i in range(4))
    return parallel, perpendicular


@dataclass(frozen=True)
class WindowState:
    phase: float
    radius: float
    center: tuple[float, float, float, float]


@dataclass(frozen=True)
class ProjectedLatticePoint:
    lattice_point: tuple[float, ...]
    parallel: tuple[float, ...]
    perpendicular: tuple[float, ...]
    internal_radius: float


def breathing_phason_window(
    phase: float, base_radius: float = 0.8,
    breathing_amplitude: float = 0.1, phason_amplitude: float = 0.03,
) -> WindowState:
    """Compact 4D ball window with periodic breathing and internal shift.

    The center translation is the internal-space phason parameter; the radius
    modulation is the undulating/breathing component.
    """
    values = (phase, base_radius, breathing_amplitude, phason_amplitude)
    if not all(isfinite(float(value)) for value in values):
        raise ValueError("window parameters must be finite")
    if base_radius <= 0:
        raise ValueError("base_radius must be positive")
    if abs(breathing_amplitude) >= 0.5:
        raise ValueError("breathing amplitude magnitude must be below 0.5")
    if phason_amplitude < 0:
        raise ValueError("phason amplitude must be nonnegative")
    radius = base_radius * exp(breathing_amplitude * sin(phase))
    center = (phason_amplitude * sin(phase), 0.0, 0.0, 0.0)
    return WindowState(float(phase), radius, center)


def point_in_window(
    perpendicular: Sequence[float], window: WindowState,
    tolerance: float = 1e-12,
) -> bool:
    if len(perpendicular) != 4:
        raise ValueError("internal coordinate must have dimension four")
    if tolerance < 0 or not isfinite(tolerance):
        raise ValueError("tolerance must be finite and nonnegative")
    distance2 = sum(
        (float(perpendicular[i]) - window.center[i]) ** 2 for i in range(4)
    )
    return distance2 <= (window.radius + tolerance) ** 2


def projected_shell(
    n: int, phase: float, base_radius: float = 0.8,
    breathing_amplitude: float = 0.1, phason_amplitude: float = 0.03,
) -> tuple[ProjectedLatticePoint, ...]:
    """Finite-shell points whose internal coordinates lie in W(phase)."""
    window = breathing_phason_window(
        phase, base_radius, breathing_amplitude, phason_amplitude
    )
    selected = []
    for doubled in e8_lattice_shell_doubled(n):
        lattice_point = tuple(value / 2.0 for value in doubled)
        parallel, perpendicular = golden_4plus4_split(lattice_point)
        radius = sqrt(sum(value * value for value in perpendicular))
        if point_in_window(perpendicular, window):
            selected.append(ProjectedLatticePoint(
                lattice_point, parallel, perpendicular, radius
            ))
    return tuple(selected)


def split_invariant_residual(vector: Sequence[float]) -> float:
    """Return | ||x||^2 - ||x_parallel||^2 - ||x_perp||^2 |."""
    parallel, perpendicular = golden_4plus4_split(vector)
    original = sum(float(value) ** 2 for value in vector)
    split_norm = sum(value * value for value in parallel) + sum(
        value * value for value in perpendicular
    )
    return abs(original - split_norm)


def run_quasicrystal_shell_audit() -> dict:
    """Finite-shell audit of the golden split and periodic window cycle."""
    shell_counts = {
        str(n): len(e8_lattice_shell_doubled(n)) for n in (1, 2, 3)
    }
    phases = (0.0, 0.5 * 3.141592653589793, 3.141592653589793,
              1.5 * 3.141592653589793, 2.0 * 3.141592653589793)
    window_counts = {
        str(index): len(projected_shell(1, phase))
        for index, phase in enumerate(phases)
    }
    first = projected_shell(1, phases[0])
    last = projected_shell(1, phases[-1])
    periodic_match = tuple(p.lattice_point for p in first) == tuple(
        p.lattice_point for p in last
    )
    probes = (
        (1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
        (0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, 0.5),
        (1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
    )
    residuals = [split_invariant_residual(probe) for probe in probes]
    return {
        "audit": "e8_golden_4plus4_breathing_phason_window_v0",
        "split": "generic orthogonal golden-block 4+4; not canonical Elser-Sloane",
        "shell_counts": shell_counts,
        "window": {
            "base_radius": 0.8,
            "breathing_amplitude": 0.1,
            "phason_amplitude": 0.03,
            "phase_samples_radians": list(phases),
            "selected_root_shell_counts": window_counts,
            "phase_0_and_2pi_selection_identical": periodic_match,
        },
        "orthogonal_split_max_abs_norm_residual": max(residuals),
        "interpretation_limits": [
            "Only the first three finite E8 lattice shells are enumerated.",
            "The ball is an experimental window, not the Elser-Sloane Voronoi window.",
            "This split is not certified to have H4 point symmetry.",
            "The phase-dependent window is not a derived physical time evolution.",
            "No celestial-CFT or quantum-gravity correspondence is asserted."
        ],
    }
