"""Leech lattice VOA character precursor (not the Moonshine orbifold).

For the Leech lattice VOA V_Lambda, ch(V_Lambda)=Theta_Lambda/eta^24.
This module derives its first graded dimensions from exact q-series.
It does not construct the Z2 orbifold V^natural or its Monster action.
"""
from __future__ import annotations

from math import comb

from experiments.moonshine_sierpinski.lattice_modular_audit import (
    leech_theta_reference,
)


def eta_inverse_24_product(degree: int) -> list[int]:
    """Return coefficients of product_{n>=1}(1-q^n)^(-24) to q^degree."""
    if degree < 0:
        raise ValueError("degree must be non-negative")
    result = [1] + [0] * degree
    for n in range(1, degree + 1):
        factor = [0] * (degree + 1)
        for j in range(degree // n + 1):
            # (1-x)^(-24) coefficient is binomial(23+j, 23).
            factor[n * j] = comb(23 + j, 23)
        out = [0] * (degree + 1)
        for i, a in enumerate(result):
            for j, b in enumerate(factor):
                if i + j <= degree:
                    out[i + j] += a * b
        result = out
    return result


def leech_lattice_voa_character(max_weight: int = 5) -> dict:
    """Compute ch(V_Lambda)=q^-1 Theta_Lambda prod(1-q^n)^-24."""
    if not isinstance(max_weight, int) or max_weight < 0:
        raise ValueError("max_weight must be non-negative")
    theta = leech_theta_reference(max_weight + 2)["coefficients_q0_to_qN"]
    oscillators = eta_inverse_24_product(max_weight + 1)
    # Character coefficient at q^(weight-1) is convolution of theta and
    # oscillator series. Return weights starting at 0.
    graded = {}
    for weight in range(max_weight + 1):
        power = weight + 1
        graded[str(weight)] = sum(
            theta[k] * oscillators[power - k]
            for k in range(min(power, len(theta) - 1) + 1)
        )
    expected = {
        "0": 1,
        "1": 24,
        "2": 196884,
        "3": 21493760,
    }
    for weight, value in expected.items():
        if int(weight) <= max_weight and graded[weight] != value:
            raise AssertionError(
                f"V_Lambda graded dimension at weight {weight}: "
                f"{graded[weight]} != {value}"
            )
    return {
        "object": "Leech lattice VOA V_Lambda",
        "character_identity": "Theta_Leech(q) / eta(q)^24",
        "graded_dimensions": graded,
        "weight_one_dimension": graded.get("1"),
        "moonshine_orbifold_constructed": False,
        "monster_action_constructed": False,
        "interpretation": (
            "V_Lambda precursor only; V^natural requires the Z2 fixed-point "
            "subalgebra and twisted-sector extension"
        ),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(leech_lattice_voa_character(), indent=2, sort_keys=True))
