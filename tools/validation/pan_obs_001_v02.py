#!/usr/bin/env python3
"""
PAN-OBS-001 v0.2: topological invariance under observation-channel changes.

This is a classical synthetic point-cloud experiment. It tests robustness of
topological reconstruction to sampling density, angular sampling bias, noise,
and rigid coordinate rotation. It does NOT model quantum measurement or
physical measurement back-action.

Dependencies:
    pip install -r requirements-observer.txt

Example:
    python tools/validation/pan_obs_001_v02.py --out results/pan_obs_001_v02

Outputs:
    replicate_metrics.csv
    summary.json

The clean latent point cloud is a known reference, not a claim that arbitrary
real-world latent states are directly observable. Bootstrap intervals resample
independent experiment replicates; they do not turn repeated measurements of
one synthetic manifold into independent physical systems.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any, Iterable

import numpy as np

DEFAULT_SEED = 20261108
DEFAULT_NOISE = (0.0, 0.02, 0.05, 0.10)
DEFAULT_SAMPLE_FRACTIONS = (0.25, 0.50, 0.75, 1.0)
DEFAULT_BIASES = ("uniform", "sector_biased")
CHANNELS = ("identity", "rotated")


def parse_csv_floats(value: str) -> tuple[float, ...]:
    try:
        values = tuple(float(item.strip()) for item in value.split(",") if item.strip())
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from exc
    if not values:
        raise argparse.ArgumentTypeError("Expected at least one comma-separated number.")
    return values


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path("pan_obs_001_v02_results"))
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--points", type=int, default=240,
                        help="Number of points in the clean latent reference.")
    parser.add_argument("--replicates", type=int, default=30,
                        help="Independent sampling/noise replicates per condition.")
    parser.add_argument("--bootstraps", type=int, default=1000,
                        help="Replicate-level bootstrap draws for percentile CIs.")
    parser.add_argument("--noise-levels", type=parse_csv_floats,
                        default=DEFAULT_NOISE)
    parser.add_argument("--sample-fractions", type=parse_csv_floats,
                        default=DEFAULT_SAMPLE_FRACTIONS)
    parser.add_argument("--bias-kappa", type=float, default=2.0,
                        help="Concentration of sector-biased angular sampling.")
    parser.add_argument("--lifetime-threshold", type=float, default=0.15)
    parser.add_argument("--maxdim", type=int, default=1)
    return parser.parse_args()


def latent_circle(n: int) -> np.ndarray:
    """Return a deterministic, evenly sampled circle embedded in R^3."""
    if n < 12:
        raise ValueError("points must be at least 12.")
    theta = np.linspace(0.0, 2.0 * np.pi, n, endpoint=False)
    return np.column_stack((np.cos(theta), np.sin(theta), np.zeros(n)))


def rotation_matrix_xyz(degrees: tuple[float, float, float]) -> np.ndarray:
    """Construct an XYZ Euler rotation matrix without a SciPy dependency."""
    ax, ay, az = np.deg2rad(degrees)
    rx = np.array([[1, 0, 0], [0, np.cos(ax), -np.sin(ax)],
                   [0, np.sin(ax), np.cos(ax)]], dtype=float)
    ry = np.array([[np.cos(ay), 0, np.sin(ay)], [0, 1, 0],
                   [-np.sin(ay), 0, np.cos(ay)]], dtype=float)
    rz = np.array([[np.cos(az), -np.sin(az), 0],
                   [np.sin(az), np.cos(az), 0], [0, 0, 1]], dtype=float)
    return rz @ ry @ rx


def sample_indices(
    n: int,
    fraction: float,
    strategy: str,
    rng: np.random.Generator,
    kappa: float = 2.0,
) -> np.ndarray:
    """Sample without replacement, uniformly or with an angular-sector bias."""
    if n < 1:
        raise ValueError("n must be positive.")
    if not 0.0 < fraction <= 1.0:
        raise ValueError("sample fraction must be in (0, 1].")
    count = max(3, min(n, int(round(n * fraction))))
    if strategy == "uniform":
        return np.sort(rng.choice(n, size=count, replace=False))
    if strategy == "sector_biased":
        theta = 2.0 * np.pi * np.arange(n) / n
        weights = np.exp(kappa * np.cos(theta))
        probabilities = weights / weights.sum()
        return np.sort(rng.choice(n, size=count, replace=False, p=probabilities))
    raise ValueError(f"Unknown sampling strategy: {strategy}")


def observe(
    points: np.ndarray,
    noise: float,
    channel: str,
    rng: np.random.Generator,
) -> np.ndarray:
    """Apply additive isotropic noise and an optional rigid rotation."""
    if noise < 0:
        raise ValueError("noise must be non-negative.")
    observed = np.array(points, dtype=float, copy=True)
    if noise:
        observed += rng.normal(0.0, noise, size=observed.shape)
    if channel == "rotated":
        observed = observed @ rotation_matrix_xyz((37.0, 51.0, 19.0)).T
    elif channel != "identity":
        raise ValueError(f"Unknown observation channel: {channel}")
    return observed


def persistence_diagrams(points: np.ndarray, maxdim: int = 1) -> list[np.ndarray]:
    """Compute Vietoris-Rips persistence diagrams using ripser."""
    try:
        from ripser import ripser
    except ImportError as exc:
        raise RuntimeError(
            "Missing optional dependency 'ripser'. Install requirements-observer.txt."
        ) from exc
    result = ripser(np.asarray(points, dtype=float), maxdim=maxdim)
    return result["dgms"]


def finite_lifetimes(diagram: np.ndarray) -> np.ndarray:
    diagram = np.asarray(diagram, dtype=float)
    if diagram.size == 0:
        return np.array([], dtype=float)
    finite = diagram[np.isfinite(diagram[:, 1])]
    return finite[:, 1] - finite[:, 0]


def count_persistent_features(diagram: np.ndarray, threshold: float) -> int:
    return int(np.count_nonzero(finite_lifetimes(diagram) >= threshold))


def bottleneck_distance(diagram_a: np.ndarray, diagram_b: np.ndarray) -> float:
    try:
        from persim import bottleneck
    except ImportError as exc:
        raise RuntimeError(
            "Missing optional dependency 'persim'. Install requirements-observer.txt."
        ) from exc
    return float(bottleneck(np.asarray(diagram_a), np.asarray(diagram_b)))


def percentile_bootstrap_ci(
    values: Iterable[float],
    rng: np.random.Generator,
    n_bootstrap: int = 1000,
    confidence: float = 0.95,
) -> dict[str, float | int | None]:
    """Percentile CI for a mean, resampling independent replicate-level values."""
    array = np.asarray(list(values), dtype=float)
    array = array[np.isfinite(array)]
    if array.size == 0:
        return {"n": 0, "mean": None, "lower": None, "upper": None}
    mean = float(array.mean())
    if array.size < 2 or n_bootstrap < 1:
        return {"n": int(array.size), "mean": mean, "lower": None, "upper": None}
    indices = rng.integers(0, array.size, size=(n_bootstrap, array.size))
    means = array[indices].mean(axis=1)
    alpha = (1.0 - confidence) / 2.0
    lower, upper = np.quantile(means, [alpha, 1.0 - alpha])
    return {
        "n": int(array.size),
        "mean": mean,
        "lower": float(lower),
        "upper": float(upper),
    }


def run_experiment(args: argparse.Namespace) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    if args.replicates < 1:
        raise ValueError("replicates must be at least 1.")
    if args.bootstraps < 0:
        raise ValueError("bootstraps cannot be negative.")
    if args.maxdim < 1:
        raise ValueError("maxdim must be at least 1 for the H1 target.")
    if args.lifetime_threshold < 0:
        raise ValueError("lifetime threshold cannot be negative.")
    if any(level < 0 for level in args.noise_levels):
        raise ValueError("noise levels must be non-negative.")
    if any(not 0 < fraction <= 1 for fraction in args.sample_fractions):
        raise ValueError("sample fractions must be in (0, 1].")

    rng = np.random.default_rng(args.seed)
    clean = latent_circle(args.points)
    reference_diagrams = persistence_diagrams(clean, maxdim=args.maxdim)
    rows: list[dict[str, Any]] = []

    for bias in DEFAULT_BIASES:
        for fraction in args.sample_fractions:
            for noise in args.noise_levels:
                for replicate in range(args.replicates):
                    indices = sample_indices(
                        args.points, fraction, bias, rng, args.bias_kappa
                    )
                    sampled = clean[indices]
                    # Generate one noisy sample and apply both coordinate channels
                    # to it, making the rotation comparison paired.
                    noisy = sampled.copy()
                    if noise:
                        noisy += rng.normal(0.0, noise, size=noisy.shape)
                    for channel in CHANNELS:
                        if channel == "rotated":
                            observed = noisy @ rotation_matrix_xyz(
                                (37.0, 51.0, 19.0)
                            ).T
                        else:
                            observed = noisy.copy()
                        diagrams = persistence_diagrams(
                            observed, maxdim=args.maxdim
                        )
                        h0 = diagrams[0]
                        h1 = diagrams[1]
                        rows.append({
                            "seed": int(args.seed),
                            "bias": bias,
                            "sample_fraction": float(fraction),
                            "sample_count": int(len(indices)),
                            "noise": float(noise),
                            "replicate": int(replicate),
                            "channel": channel,
                            "h0_feature_count": count_persistent_features(
                                h0, args.lifetime_threshold
                            ),
                            "h1_feature_count": count_persistent_features(
                                h1, args.lifetime_threshold
                            ),
                            "h1_bottleneck_to_clean_reference": bottleneck_distance(
                                reference_diagrams[1], h1
                            ),
                        })

    # Bootstrap intervals are computed across replicate-level observations,
    # separately for every experimental condition and observation channel.
    summary: dict[str, Any] = {
        "protocol": "PAN-OBS-001",
        "version": "0.2",
        "seed": int(args.seed),
        "points": int(args.points),
        "replicates_per_condition": int(args.replicates),
        "bootstrap_draws": int(args.bootstraps),
        "confidence_level": 0.95,
        "lifetime_threshold": float(args.lifetime_threshold),
        "bias_kappa": float(args.bias_kappa),
        "noise_levels": [float(x) for x in args.noise_levels],
        "sample_fractions": [float(x) for x in args.sample_fractions],
        "channels": list(CHANNELS),
        "reference": "clean evenly sampled circle in R^3",
        "metrics": {},
        "limitations": [
            "Classical synthetic point-cloud experiment only; no quantum back-action.",
            "Bootstrap resamples experiment replicates, not individual points.",
            "The clean reference is known by construction and is not available in ordinary field observations.",
            "The sector-biased sampler is a controlled stress test, not a model of every real sampling bias.",
            "H1 bottleneck distances compare sampled/noisy diagrams to the clean full-reference diagram.",
        ],
    }

    conditions = sorted({
        (row["bias"], row["sample_fraction"], row["noise"], row["channel"])
        for row in rows
    })
    for bias, fraction, noise, channel in conditions:
        selected = [
            row for row in rows
            if row["bias"] == bias
            and row["sample_fraction"] == fraction
            and row["noise"] == noise
            and row["channel"] == channel
        ]
        key = f"{bias}|fraction={fraction:g}|noise={noise:g}|channel={channel}"
        summary["metrics"][key] = {
            "h0_feature_count": percentile_bootstrap_ci(
                (r["h0_feature_count"] for r in selected),
                rng, args.bootstraps
            ),
            "h1_feature_count": percentile_bootstrap_ci(
                (r["h1_feature_count"] for r in selected),
                rng, args.bootstraps
            ),
            "h1_bottleneck_to_clean_reference": percentile_bootstrap_ci(
                (r["h1_bottleneck_to_clean_reference"] for r in selected),
                rng, args.bootstraps
            ),
        }
    return rows, summary


def write_outputs(
    rows: list[dict[str, Any]], summary: dict[str, Any], output_dir: Path
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "replicate_metrics.csv"
    if rows:
        with csv_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
    (output_dir / "summary.json").write_text(
        json.dumps(summary, indent=2, allow_nan=False) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    args = parse_args()
    rows, summary = run_experiment(args)
    write_outputs(rows, summary, args.out)
    print(f"PAN-OBS-001 v0.2 completed: {len(rows)} replicate/channel records")
    print(f"Results written to: {args.out.resolve()}")
    print("Interpretation: robustness diagnostics only; not evidence of observer-effect elimination.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)
