"""Reproducible finite-lattice SU(2) gauge-invariance audit."""
from __future__ import annotations

import json

from core.gauge_theory.su2_lattice import random_gauge_transform, random_lattice


def run_audit() -> dict:
    lattice = random_lattice(4, 3, seed=20261112)
    transformed = lattice.gauge_transform(
        random_gauge_transform(4, 3, seed=20261113)
    )
    original_traces = [p[0] for p in lattice.plaquettes()]
    transformed_traces = [p[0] for p in transformed.plaquettes()]
    trace_residual = max(abs(a - b) for a, b in zip(original_traces, transformed_traces))
    action_before = lattice.wilson_action(beta=2.0)
    action_after = transformed.wilson_action(beta=2.0)
    action_residual = abs(action_before - action_after)
    return {
        "status": "PASS" if trace_residual < 1e-10 and action_residual < 1e-10 else "FAIL",
        "group": "SU(2)",
        "lattice": {"dimensions": [4, 3], "periodic": True, "sites": 12, "links": 24, "plaquettes": 12},
        "seeds": {"links": 20261112, "gauge_transform": 20261113},
        "checks": {
            "plaquette_half_trace_gauge_invariance_max_abs_residual": trace_residual,
            "wilson_action_gauge_invariance_abs_residual": action_residual,
            "beta": 2.0,
        },
        "scope": [
            "finite periodic two-dimensional lattice",
            "unit-quaternion SU(2) representation",
            "floating-point gauge-invariance regression",
            "not a continuum-limit proof",
            "not a mass-gap result",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(run_audit(), indent=2, sort_keys=True))
