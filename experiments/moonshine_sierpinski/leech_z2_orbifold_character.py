"""Exact graded-character audit of the Leech Z2 orbifold sectors.

Computes the theta-fixed untwisted sector and the theta-fixed twisted sector
from their oscillator products. This verifies the graded-dimension character
of V^natural through a finite q-order. It does NOT construct vertex operators,
the VOA extension/intertwining operators, or the Monster action.

Conventions:
  V_Lambda character: q^-1 Theta_Lambda(q) prod_{n>=1}(1-q^n)^-24
  untwisted theta trace: q^-1 prod_{n>=1}(1+q^n)^-24
  twisted full character: 2^12 q^(1/2) prod_{m>=0}(1-q^(m+1/2))^-24
  theta acts as -1 on twisted ground space and as -1 on each oscillator.
Thus the theta-fixed twisted character is the odd-oscillator projection.
"""
from __future__ import annotations

from math import comb

from experiments.moonshine_sierpinski.leech_voa_character import (
    leech_lattice_voa_character,
)


def _multiply(a: list[int], b: list[int], degree: int) -> list[int]:
    out = [0] * (degree + 1)
    for i, x in enumerate(a):
        if not x:
            continue
        for j, y in enumerate(b):
            if i + j <= degree and y:
                out[i + j] += x * y
    return out


def _inverse_power_product(
    steps: list[int], degree: int, plus_sign: bool
) -> list[int]:
    """Coefficients of product (1 +/- t^step)^(-24), exact over Z."""
    result = [1] + [0] * degree
    for step in steps:
        factor = [0] * (degree + 1)
        for j in range(degree // step + 1):
            coefficient = comb(23 + j, 23)
            if plus_sign and j % 2:
                coefficient = -coefficient
            factor[step * j] = coefficient
        result = _multiply(result, factor, degree)
    return result


def _untwisted_theta_trace(max_weight: int) -> list[int]:
    """Trace of theta on V_Lambda by conformal weight, q^-1 normalized."""
    return _inverse_power_product(
        list(range(1, max_weight + 1)), max_weight, plus_sign=True
    )


def _twisted_fixed_character(max_weight: int) -> list[int]:
    """Theta-fixed twisted-sector dimensions by integer conformal weight."""
    if max_weight < 0:
        return []
    max_t_degree = max(0, 2 * max_weight - 3)
    odd_steps = list(range(1, max_t_degree + 1, 2))
    # A: all twisted oscillators; B: theta-trace with oscillator sign reversed.
    full = _inverse_power_product(odd_steps, max_t_degree, plus_sign=False)
    trace_osc = _inverse_power_product(odd_steps, max_t_degree, plus_sign=True)
    result = [0] * (max_weight + 1)
    for weight in range(2, max_weight + 1):
        exponent = 2 * weight - 3
        result[weight] = 2048 * (full[exponent] - trace_osc[exponent])
    return result


def leech_z2_orbifold_character(max_weight: int = 4) -> dict:
    """Return exact untwisted/twisted fixed-sector dimensions and their sum."""
    if not isinstance(max_weight, int) or max_weight < 0:
        raise ValueError("max_weight must be a non-negative integer")

    leech = leech_lattice_voa_character(max_weight)["graded_dimensions"]
    theta_trace = _untwisted_theta_trace(max_weight)
    twisted_fixed = _twisted_fixed_character(max_weight)

    untwisted_fixed = {}
    moonshine = {}
    for weight in range(max_weight + 1):
        full_dimension = leech[str(weight)]
        trace_dimension = theta_trace[weight]
        numerator = full_dimension + trace_dimension
        if numerator % 2:
            raise AssertionError("untwisted fixed-space projection is not integral")
        fixed_dimension = numerator // 2
        untwisted_fixed[str(weight)] = fixed_dimension
        moonshine[str(weight)] = fixed_dimension + twisted_fixed[weight]

    expected = {
        "0": 1,
        "1": 0,
        "2": 196884,
        "3": 21493760,
        "4": 864299970,
    }
    for weight, reference in expected.items():
        if int(weight) <= max_weight and moonshine[weight] != reference:
            raise AssertionError(
                f"orbifold graded dimension at weight {weight}: "
                f"{moonshine[weight]} != reference {reference}"
            )

    return {
        "object": "Leech Z2 orbifold graded-character audit",
        "central_charge": 24,
        "involution": "canonical lift of lattice negation",
        "twisted_ground_conformal_weight": "3/2",
        "twisted_ground_multiplicity": 4096,
        "untwisted_fixed_dimensions": untwisted_fixed,
        "twisted_fixed_dimensions": {
            str(i): value for i, value in enumerate(twisted_fixed)
        },
        "moonshine_orbifold_graded_dimensions": moonshine,
        "reference_match": True,
        "vertex_operator_extension_constructed": False,
        "monster_action_constructed": False,
        "scope": (
            "exact finite q-series projection audit; verifies graded dimensions "
            "but not VOA intertwining operators, locality/associativity, or "
            "the Monster automorphism action"
        ),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(leech_z2_orbifold_character(), indent=2, sort_keys=True))
