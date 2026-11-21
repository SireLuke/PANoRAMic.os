"""Small periodic incompressible Navier-Stokes spectral evidence harness.

This is a reproducible benchmark solver, not a global-regularity proof.
"""
from __future__ import annotations

import argparse
import json
import math
import time

import numpy as np


def run_case(*, n: int = 16, dimension: int = 3, viscosity: float = 0.01,
             final_time: float = 0.1, dt: float = 0.001) -> dict:
    """Run a periodic Taylor-Green benchmark with Fourier projection.

    Domain: [0, 2*pi)^dimension.
    Scheme: Fourier pseudospectral, 2/3 dealiasing, Leray projection,
    classical RK4, unforced incompressible Navier-Stokes.
    dimension=2 uses an exact decaying Taylor-Green solution.
    dimension=3 uses the Taylor-Green vortex initial condition.
    """
    if dimension not in (2, 3):
        raise ValueError("dimension must be 2 or 3")
    if isinstance(n, bool) or not isinstance(n, int) or n < 8:
        raise ValueError("n must be an integer >= 8")
    if viscosity <= 0 or final_time <= 0 or dt <= 0:
        raise ValueError("viscosity, final_time and dt must be positive")

    axes = 2.0 * np.pi * np.arange(n) / n
    mesh = np.meshgrid(*([axes] * dimension), indexing="ij")
    if dimension == 2:
        x, y = mesh
        velocity = np.stack((
            np.sin(x) * np.cos(y),
            -np.cos(x) * np.sin(y),
        )).astype(float)
    else:
        x, y, z = mesh
        velocity = np.stack((
            np.sin(x) * np.cos(y) * np.cos(z),
            -np.cos(x) * np.sin(y) * np.cos(z),
            np.zeros_like(x),
        )).astype(float)

    wave = np.fft.fftfreq(n) * n
    wave_mesh = np.meshgrid(*([wave] * dimension), indexing="ij")
    wave_sq = sum(component ** 2 for component in wave_mesh)
    dealias = np.ones((n,) * dimension, dtype=bool)
    for component in wave_mesh:
        dealias &= np.abs(component) <= n / 3.0
    spatial_axes = tuple(range(1, dimension + 1))

    def diagnostics(field: np.ndarray) -> tuple[float, float, float, float]:
        field_hat = np.fft.fftn(field, axes=spatial_axes)
        div_hat = sum(
            1j * wave_mesh[i] * field_hat[i] for i in range(dimension)
        )
        divergence = np.fft.ifftn(div_hat).real
        gradient = np.empty(
            (dimension, dimension) + (n,) * dimension, dtype=float
        )
        gradient_norm_sq = 0.0
        for i in range(dimension):
            for j in range(dimension):
                gradient[i, j] = np.fft.ifftn(
                    1j * wave_mesh[j] * field_hat[i]
                ).real
                gradient_norm_sq += float(np.mean(gradient[i, j] ** 2))
        energy = float(0.5 * np.mean(np.sum(field ** 2, axis=0)))
        dissipation = float(viscosity * gradient_norm_sq)
        if dimension == 2:
            vorticity = gradient[1, 0] - gradient[0, 1]
            enstrophy = float(0.5 * np.mean(vorticity ** 2))
        else:
            omega_x = gradient[2, 1] - gradient[1, 2]
            omega_y = gradient[0, 2] - gradient[2, 0]
            omega_z = gradient[1, 0] - gradient[0, 1]
            enstrophy = float(0.5 * np.mean(
                omega_x ** 2 + omega_y ** 2 + omega_z ** 2
            ))
        return energy, float(np.max(np.abs(divergence))), dissipation, enstrophy

    def rhs(field: np.ndarray) -> np.ndarray:
        field_hat = np.fft.fftn(field, axes=spatial_axes) * dealias
        gradient = np.empty(
            (dimension, dimension) + (n,) * dimension, dtype=float
        )
        for i in range(dimension):
            for j in range(dimension):
                gradient[i, j] = np.fft.ifftn(
                    1j * wave_mesh[j] * field_hat[i]
                ).real

        advection = np.zeros_like(field)
        for i in range(dimension):
            for j in range(dimension):
                advection[i] += field[j] * gradient[i, j]

        nonlinear_hat = (
            np.fft.fftn(-advection, axes=spatial_axes) * dealias
        )
        longitudinal = sum(
            wave_mesh[i] * nonlinear_hat[i] for i in range(dimension)
        )
        for i in range(dimension):
            pressure_gradient = np.where(
                wave_sq > 0,
                wave_mesh[i] * longitudinal / np.where(wave_sq > 0, wave_sq, 1),
                0.0,
            )
            nonlinear_hat[i] -= pressure_gradient
            nonlinear_hat[i] -= viscosity * wave_sq * field_hat[i]
        return np.fft.ifftn(nonlinear_hat, axes=spatial_axes).real

    steps = math.ceil(final_time / dt)
    step = final_time / steps
    initial_energy, _, previous_dissipation, initial_enstrophy = diagnostics(velocity)
    integrated_dissipation = 0.0
    started = time.perf_counter()

    for _ in range(steps):
        k1 = rhs(velocity)
        k2 = rhs(velocity + 0.5 * step * k1)
        k3 = rhs(velocity + 0.5 * step * k2)
        k4 = rhs(velocity + step * k3)
        velocity = velocity + (step / 6.0) * (
            k1 + 2.0 * k2 + 2.0 * k3 + k4
        )

        # Reapply dealiasing and the Leray projection after each RK4 step.
        field_hat = np.fft.fftn(velocity, axes=spatial_axes) * dealias
        longitudinal = sum(
            wave_mesh[i] * field_hat[i] for i in range(dimension)
        )
        for i in range(dimension):
            field_hat[i] -= np.where(
                wave_sq > 0,
                wave_mesh[i] * longitudinal / np.where(wave_sq > 0, wave_sq, 1),
                0.0,
            )
        velocity = np.fft.ifftn(field_hat, axes=spatial_axes).real

        _, _, current_dissipation, _ = diagnostics(velocity)
        integrated_dissipation += (
            0.5 * step * (previous_dissipation + current_dissipation)
        )
        previous_dissipation = current_dissipation

    elapsed = time.perf_counter() - started
    final_energy, max_divergence, final_dissipation, final_enstrophy = diagnostics(velocity)
    result = {
        "n": n,
        "dimension": dimension,
        "viscosity": viscosity,
        "final_time": final_time,
        "dt": step,
        "steps": steps,
        "energy_initial": initial_energy,
        "energy_final": final_energy,
        "energy_drop": initial_energy - final_energy,
        "integrated_dissipation_trapezoid": integrated_dissipation,
        "energy_balance_residual": (
            initial_energy - final_energy - integrated_dissipation
        ),
        "max_divergence_final": max_divergence,
        "dissipation_final": final_dissipation,
        "enstrophy_initial": initial_enstrophy,
        "enstrophy_final": final_enstrophy,
        "runtime_seconds": elapsed,
    }

    if dimension == 2:
        exact = np.stack((
            np.sin(mesh[0]) * np.cos(mesh[1]),
            -np.cos(mesh[0]) * np.sin(mesh[1]),
        )) * np.exp(-2.0 * viscosity * final_time)
        rms_error = float(np.sqrt(np.mean((velocity - exact) ** 2)))
        exact_rms = float(np.sqrt(np.mean(exact ** 2)))
        result["exact_rms_error"] = rms_error
        result["exact_relative_rms_error"] = rms_error / exact_rms

    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="-")
    parser.add_argument("--time-2d", type=float, default=0.1)
    parser.add_argument("--time-3d", type=float, default=0.1)
    args = parser.parse_args()
    results = {
        "experiment": "NS-EVIDENCE-001",
        "method": "Fourier pseudospectral / 2-3 dealiasing / Leray projection / RK4",
        "domain": "[0, 2*pi)^d, periodic",
        "forcing": "none",
        "viscosity": 0.01,
        "cases": [
            run_case(n=n, dimension=2, final_time=args.time_2d, dt=0.002)
            for n in (16, 24, 32)
        ] + [
            run_case(n=n, dimension=3, final_time=args.time_3d, dt=0.001)
            for n in (16, 24, 32)
        ],
    }
    rendered = json.dumps(results, indent=2, sort_keys=True) + "\n"
    if args.output == "-":
        print(rendered, end="")
    else:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(rendered)


if __name__ == "__main__":
    main()
