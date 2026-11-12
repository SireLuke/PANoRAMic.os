"""Exact arithmetic bridge: Leech orbifold graded dimensions to Monster data.

This module checks published low-degree Monster representation decompositions
against the Leech Z2-orbifold graded dimensions already computed in this repo.
It also checks the first 2B McKay-Thompson coefficients against published
2B character values of the first four Monster irreducibles.

It is a reference-data consistency audit, not a construction of Monster
representations, character table, group action, or the full moonshine theorem.
"""
from __future__ import annotations

from pathlib import Path
import sys

_REPOSITORY_ROOT = str(Path(__file__).resolve().parents[2])
if _REPOSITORY_ROOT not in sys.path:
    sys.path.insert(0, _REPOSITORY_ROOT)

from experiments.moonshine_sierpinski.leech_z2_orbifold_character import (
    leech_z2_orbifold_character,
)

# Selected Monster irreducible dimensions. The q^4 Serre decomposition uses
# chi_6 (dimension 19,360,062,527), skipping chi_5 (dimension 18,538,750,076).
# Source references are documented in research/LEECH_TO_MONSTER_BRIDGE.md.
MONSTER_IRREP_LABELS = ("chi_1", "chi_2", "chi_3", "chi_4", "chi_6")
MONSTER_IRREP_DIMENSIONS = (1, 196883, 21296876, 842609326, 19360062527)

# Rows correspond to q^1, q^2, q^3, q^4 in J(q)=j(q)-744.
# Columns correspond to chi_1, chi_2, chi_3, chi_4, chi_6.
IDENTITY_MULTIPLICITIES = (
    (1, 1, 0, 0, 0),
    (1, 1, 1, 0, 0),
    (2, 2, 1, 1, 0),
    (2, 3, 2, 1, 1),
)

IDENTITY_J_COEFFICIENTS = (
    196884,
    21493760,
    864299970,
    20245856256,
)

# Published character values for the first four irreducibles on Monster class 2B.
MONSTER_2B_CHARACTER_VALUES = (1, 275, -2324, 12974)
TWO_B_MULTIPLICITIES = (
    (1, 1, 0, 0),
    (1, 1, 1, 0),
    (2, 2, 1, 1),
)
TWO_B_MCKAY_THOMPSON_COEFFICIENTS = (276, -2048, 11202)


def _linear_combination(coefficients: tuple[int, ...],
                         multiplicities: tuple[int, ...]) -> int:
    if len(coefficients) != len(multiplicities):
        raise ValueError("coefficient and multiplicity lengths differ")
    return sum(a * b for a, b in zip(coefficients, multiplicities))


def leech_to_monster_representation_bridge(max_q_power: int = 4) -> dict:
    """Compare orbifold dimensions and low-order Monster character fixtures."""
    if not isinstance(max_q_power, int) or not 1 <= max_q_power <= 4:
        raise ValueError("max_q_power must be an integer from 1 through 4")

    # q^n coefficient of J is dim V^natural_(n+1).
    orbifold = leech_z2_orbifold_character(max_weight=max_q_power + 1)
    graded = orbifold["moonshine_orbifold_graded_dimensions"]

    identity_checks = []
    for index in range(max_q_power):
        q_power = index + 1
        weight = q_power + 1
        orbifold_dimension = graded[str(weight)]
        representation_sum = _linear_combination(
            MONSTER_IRREP_DIMENSIONS,
            IDENTITY_MULTIPLICITIES[index],
        )
        reference_coefficient = IDENTITY_J_COEFFICIENTS[index]
        if orbifold_dimension != reference_coefficient:
            raise AssertionError(
                f"Leech orbifold weight {weight} gives {orbifold_dimension}, "
                f"expected J coefficient {reference_coefficient}"
            )
        if representation_sum != reference_coefficient:
            raise AssertionError(
                f"Monster identity decomposition at q^{q_power} gives "
                f"{representation_sum}, expected {reference_coefficient}"
            )
        identity_checks.append({
            "q_power": q_power,
            "orbifold_conformal_weight": weight,
            "orbifold_dimension": orbifold_dimension,
            "monster_irrep_labels": MONSTER_IRREP_LABELS,
            "monster_irrep_multiplicities": IDENTITY_MULTIPLICITIES[index],
            "representation_dimension_sum": representation_sum,
            "matches": True,
        })

    two_b_checks = []
    for index in range(min(max_q_power, len(TWO_B_MULTIPLICITIES))):
        q_power = index + 1
        trace_sum = _linear_combination(
            MONSTER_2B_CHARACTER_VALUES,
            TWO_B_MULTIPLICITIES[index],
        )
        expected = TWO_B_MCKAY_THOMPSON_COEFFICIENTS[index]
        if trace_sum != expected:
            raise AssertionError(
                f"2B character sum at q^{q_power} gives {trace_sum}, "
                f"expected {expected}"
            )
        two_b_checks.append({
            "q_power": q_power,
            "monster_2B_character_values": MONSTER_2B_CHARACTER_VALUES,
            "irrep_multiplicities": TWO_B_MULTIPLICITIES[index],
            "trace_sum": trace_sum,
            "reference_coefficient": expected,
            "matches": True,
        })

    return {
        "bridge": "Leech Z2 orbifold graded dimensions -> Monster representation data",
        "identity_class_checks": identity_checks,
        "two_B_McKay_Thompson_checks": two_b_checks,
        "identity_checks_passed": len(identity_checks),
        "two_B_checks_passed": len(two_b_checks),
        "reference_data_only": True,
        "Monster_representation_constructed": False,
        "Monster_action_on_orbifold_constructed": False,
        "McKay_Thompson_series_derived_from_group_action": False,
        "scope": (
            "exact integer consistency checks against published Monster "
            "irreducible dimensions and 2B character values; not a construction "
            "of the Monster module or a proof of monstrous moonshine"
        ),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(leech_to_monster_representation_bridge(), indent=2, sort_keys=True))
