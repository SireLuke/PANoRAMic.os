"""Explicit weight-two grading of the Leech lattice VOA precursor.

For V_Lambda, the weight-two subspace splits into:
- 196,560 momentum states from Leech vectors of squared norm 4;
- 324 oscillator-only states from the 24-boson Fock factor.

Their sum is 196,884, the same integer appearing as the q^1 coefficient of
J(q)=j(q)-744. This numerical equality is not itself the Monster action or
the Moonshine orbifold decomposition.
""""""
from pathlib import Path
import sys

_REPOSITORY_ROOT = str(Path(__file__).resolve().parents[2])
if _REPOSITORY_ROOT not in sys.path:
    sys.path.insert(0, _REPOSITORY_ROOT)


from experiments.moonshine_sierpinski.lattice_modular_audit import (
    leech_theta_reference,
    moonshine_character_reference,
)
from experiments.moonshine_sierpinski.leech_voa_character import (
    eta_inverse_24_product,
)


def leech_voa_weight_two_decomposition() -> dict:
    theta = leech_theta_reference(2)["coefficients_q0_to_qN"]
    oscillator = eta_inverse_24_product(2)
    momentum_states = theta[2]
    oscillator_states = oscillator[2]
    total = momentum_states + oscillator_states
    moonshine_q1 = moonshine_character_reference()["coefficients"]["q^1"]
    if (momentum_states, oscillator_states, total) != (196560, 324, 196884):
        raise AssertionError("unexpected Leech VOA weight-two decomposition")
    if total != moonshine_q1:
        raise AssertionError("weight-two dimension differs from J(q) q^1 coefficient")
    return {
        "object": "Leech lattice VOA V_Lambda",
        "weight": 2,
        "momentum_states_from_norm_4_vectors": momentum_states,
        "oscillator_only_states": oscillator_states,
        "total_weight_two_dimension": total,
        "moonshine_J_q1_reference": moonshine_q1,
        "numerical_dimension_match": True,
        "monster_representation_decomposition": "not_computed",
        "moonshine_Z2_orbifold": "not_constructed",
    }


if __name__ == "__main__":
    import json
    print(json.dumps(leech_voa_weight_two_decomposition(), indent=2, sort_keys=True))
