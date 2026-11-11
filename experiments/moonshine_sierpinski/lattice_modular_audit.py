"""Exact low-order modular-form checks for E8 products and Leech theta series.
This does not construct Leech coordinates, the Moonshine VOA, or Monster action.
All q-series coefficients are exact integers.
"""
from math import comb

def mul(a, b, degree):
    out = [0] * (degree + 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            if i + j <= degree:
                out[i + j] += x * y
    return out

def power(series, exponent, degree):
    result = [1] + [0] * degree
    for _ in range(exponent):
        result = mul(result, series, degree)
    return result

def sigma3(n):
    return sum(d**3 for d in range(1, n + 1) if n % d == 0)

def eisenstein_e4(degree):
    if degree < 0:
        raise ValueError("degree must be non-negative")
    return [1] + [240 * sigma3(n) for n in range(1, degree + 1)]

def discriminant_delta(degree):
    if degree < 0:
        raise ValueError("degree must be non-negative")
    product_series = [1] + [0] * degree
    for m in range(1, degree + 1):
        factor = [0] * (degree + 1)
        for j in range(min(24, degree // m) + 1):
            factor[m * j] = (-1) ** j * comb(24, j)
        product_series = mul(product_series, factor, degree)
    return [0] + product_series[:degree]

def e8_product_theta(k, degree=4):
    if not isinstance(k, int) or k < 1:
        raise ValueError("k must be a positive integer")
    return {
        "lattice": f"E8^{k}",
        "rank": 8 * k,
        "theta_weight": 4 * k,
        "coefficients_q0_to_qN": power(eisenstein_e4(degree), k, degree),
        "identity": "Theta_(E8^k) = E4(q)^k",
    }

def leech_theta_reference(degree=6):
    e4_cube = power(eisenstein_e4(degree), 3, degree)
    delta = discriminant_delta(degree)
    coefficients = [a - 720 * b for a, b in zip(e4_cube, delta)]
    return {
        "lattice_reference": "Leech lattice Lambda_24",
        "rank": 24,
        "theta_weight": 12,
        "coefficients_q0_to_qN": coefficients,
        "identity": "Theta_Leech(q) = E4(q)^3 - 720*Delta(q)",
        "first_shell_checks": {
            "q1_norm2_vectors": coefficients[1] if degree >= 1 else None,
            "q2_norm4_vectors": coefficients[2] if degree >= 2 else None,
            "q3_norm6_vectors": coefficients[3] if degree >= 3 else None,
        },
        "construction_status": "reference_theta_identity_only; Golay/coordinate construction not implemented",
    }

def moonshine_character_reference():
    return {
        "series": "J(q)=j(q)-744",
        "coefficients": {"q^-1": 1, "q^0": 0, "q^1": 196884,
                         "q^2": 21493760, "q^3": 864299970},
        "first_monster_decomposition": {
            "graded_dimension_q1": 196884,
            "trivial_representation": 1,
            "smallest_nontrivial_monster_representation": 196883,
            "identity": "196884 = 1 + 196883",
        },
        "construction_status": "published reference values only; orbifold and Monster action not computed",
    }

def scaling_ladder():
    return [e8_product_theta(k, degree=3) for k in (56, 112, 208)]

if __name__ == "__main__":
    import json
    print(json.dumps({"leech_theta": leech_theta_reference(),
                      "moonshine_character": moonshine_character_reference(),
                      "e8_scaling": scaling_ladder()},
                     indent=2, sort_keys=True))
