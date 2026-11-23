"""Exact Heisenberg-sector products for the untwisted weight-two space.

Implements selected exact blocks:
  * Sym^2(h(-1)) x Sym^2(h(-1)) -> Sym^2(h(-1));
  * Sym^2(h(-1)) x even norm-four momentum states -> even momentum states;
  * opposite momentum-orbit self-product -> oscillator states;
  * distinct norm-four momentum pairs with absolute inner product 2 -> momentum states.

The formulas are the z^-2 coefficients of
Y(h_i(-1)h_j(-1)1,z) = :h_i(z)h_j(z):
in an orthonormal Heisenberg basis, with lattice vectors stored as integral
coordinates x and physical coordinates alpha=x/sqrt(8).

This is a partial untwisted product kernel. It now includes all
momentum-pair inner-product classes and an exact bilinear form with
invariance checks on deterministic fixtures. The twisted module, orbifold
intertwiner, full Griess product, and Monster actions remain unimplemented.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
from typing import TypeAlias

from experiments.moonshine_sierpinski.leech_golay_construction import (
    code_words_cached,
)
from experiments.moonshine_sierpinski.leech_lattice_cocycle import (
    lattice_cocycle_sign,
    lattice_inner_product_numerator,
)

OscillatorKey: TypeAlias = tuple[str, int, int]
MomentumKey: TypeAlias = tuple[str, tuple[int, ...]]
BasisKey: TypeAlias = OscillatorKey | MomentumKey
SparseVector: TypeAlias = dict[BasisKey, Fraction]


def _oscillator_pair(pair: tuple[int, int]) -> tuple[int, int]:
    if (not isinstance(pair, tuple) or len(pair) != 2
            or any(not isinstance(i, int) for i in pair)):
        raise TypeError("oscillator basis key must be a pair of integer indices")
    i, j = pair
    if not (0 <= i <= j < 24):
        raise ValueError("oscillator indices must satisfy 0 <= i <= j < 24")
    return i, j


def _validate_minimal_leech_coordinate(vector: tuple[int, ...]) -> tuple[int, ...]:
    if not isinstance(vector, tuple) or len(vector) != 24:
        raise ValueError("momentum vector must be a 24-tuple of integral coordinates")
    if any(not isinstance(value, int) for value in vector):
        raise TypeError("momentum coordinates must be integers")
    if sum(value * value for value in vector) != 32:
        raise ValueError("momentum vector must have integral squared norm 32")

    parity = vector[0] & 1
    if any((value & 1) != parity for value in vector):
        raise ValueError("coordinates do not have common parity")
    residue_word = 0
    for index, value in enumerate(vector):
        if (((value - parity) // 2) & 1):
            residue_word |= 1 << index
    if residue_word not in code_words_cached:
        raise ValueError("coordinate residue is not in the extended Golay code")
    if sum(vector) % 8 != (4 * parity) % 8:
        raise ValueError("Leech coordinate-sum congruence failed")
    return vector


def canonical_momentum_key(vector: tuple[int, ...]) -> MomentumKey:
    """Return the even momentum-state key for {alpha,-alpha}."""
    vector = _validate_minimal_leech_coordinate(vector)
    opposite = tuple(-value for value in vector)
    return ("mom", min(vector, opposite))


def oscillator_oscillator_product(
    left: tuple[int, int], right: tuple[int, int]
) -> SparseVector:
    """Compute (h_i(-1)h_j(-1)1)_1 (h_k(-1)h_l(-1)1).

    The output is a sparse exact linear combination of the 300 oscillator
    basis states. Basis states are unnormalised monomials with i <= j.
    """
    i, j = _oscillator_pair(left)
    k, l = _oscillator_pair(right)
    terms = (
        ((i, l), int(j == k)),
        ((i, k), int(j == l)),
        ((j, l), int(i == k)),
        ((j, k), int(i == l)),
    )
    result: defaultdict[BasisKey, Fraction] = defaultdict(Fraction)
    for pair, coefficient in terms:
        if coefficient:
            a, b = _oscillator_pair(tuple(sorted(pair)))
            result[("osc", a, b)] += Fraction(coefficient)
    return {key: value for key, value in result.items() if value}


def oscillator_momentum_product(
    oscillator: tuple[int, int], momentum: tuple[int, ...]
) -> SparseVector:
    """Compute the oscillator state acting on e^alpha + e^-alpha.

    For alpha=x/sqrt(8), the coefficient is (h_i,alpha)(h_j,alpha)
    = x_i*x_j/8. The same coefficient occurs for alpha and -alpha.
    """
    i, j = _oscillator_pair(oscillator)
    key = canonical_momentum_key(momentum)
    coefficient = Fraction(momentum[i] * momentum[j], 8)
    if not coefficient:
        return {}
    return {key: coefficient}


def oscillator_bilinear_form(
    left: tuple[int, int], right: tuple[int, int]
) -> Fraction:
    """Heisenberg Fock-space form on unnormalised quadratic states."""
    i, j = _oscillator_pair(left)
    k, l = _oscillator_pair(right)
    return Fraction(int(i == k and j == l) + int(i == l and j == k))


def conformal_identity_oscillator_product(
    oscillator: tuple[int, int]
) -> SparseVector:
    """Compute (omega/2)_1 a in the 300-dimensional oscillator block."""
    i, j = _oscillator_pair(oscillator)
    result: defaultdict[BasisKey, Fraction] = defaultdict(Fraction)
    for axis in range(24):
        for key, coefficient in oscillator_oscillator_product(
            (axis, axis), (i, j)
        ).items():
            result[key] += coefficient / 4
    return {key: value for key, value in result.items() if value}


def conformal_identity_momentum_product(
    momentum: tuple[int, ...]
) -> SparseVector:
    """Compute (omega/2)_1 E_[alpha] using sum alpha_i^2 = 4."""
    key = canonical_momentum_key(momentum)
    norm_numerator = sum(value * value for value in momentum)
    coefficient = Fraction(norm_numerator, 32)
    return {key: coefficient}



def momentum_opposite_pair_self_product(momentum: tuple[int, ...]) -> SparseVector:
    """Compute E_[alpha]_1 E_[alpha] for E_[alpha]=e^alpha+e^-alpha.

    For a norm-four vector alpha, only the two opposite-charge terms contribute
    to the z^-2 coefficient. With the standard normalized lattice cocycle,
    epsilon(alpha,-alpha)=epsilon(-alpha,alpha)=1. Their oscillator expansions
    contribute +alpha(-1)^2/2 and +alpha(-1)^2/2; the alpha(-2) terms cancel.
    Thus the result is alpha(-1)^2 in Sym^2(h(-1)).

    Stored coordinates are x=sqrt(8)*alpha. In the unnormalised oscillator
    basis A_ij=h_i(-1)h_j(-1)1, the coefficients are x_i^2/8 on A_ii and
    x_i*x_j/4 on A_ij for i<j.

    This handles only the same antipodal momentum orbit. It does not implement
    products for distinct momentum orbits (inner product -2), nor a general
    lattice 2-cocycle.
    """
    vector = _validate_minimal_leech_coordinate(momentum)
    result: SparseVector = {}
    for i in range(24):
        diagonal = Fraction(vector[i] * vector[i], 8)
        if diagonal:
            result[("osc", i, i)] = diagonal
        for j in range(i + 1, 24):
            coefficient = Fraction(vector[i] * vector[j], 4)
            if coefficient:
                result[("osc", i, j)] = coefficient
    return result



def momentum_distinct_inner_product_minus_two_product(
    left: tuple[int, ...], right: tuple[int, ...]
) -> SparseVector:
    """Compute E_[alpha]_1 E_[beta] when |(alpha,beta)|=2.

    Here E_[alpha]=e^alpha+e^-alpha and both inputs have norm four.
    Exactly two of the four exponential pairs have inner product -2.
    If the supplied representatives have inner product +2, the singular
    pairs are (-alpha,beta) and (alpha,-beta); otherwise they are
    (alpha,beta) and (-alpha,-beta).

    Their common coefficient is the chosen lattice cocycle sign. Their
    outputs are antipodal, giving the even orbit state for the sum of the
    singular-pair momenta, which again has norm four.

    This implements only the absolute-inner-product-2 orbit. Other
    momentum-pair inner products and oscillator-valued opposite-pair terms
    are not handled.
    """
    left = _validate_minimal_leech_coordinate(left)
    right = _validate_minimal_leech_coordinate(right)
    inner_numerator = lattice_inner_product_numerator(left, right)
    if inner_numerator == -16:
        oriented_left, oriented_right = left, right
    elif inner_numerator == 16:
        oriented_left, oriented_right = tuple(-x for x in left), right
    else:
        raise ValueError(
            "this product fixture requires absolute lattice inner product exactly 2"
        )
    output = tuple(a + b for a, b in zip(oriented_left, oriented_right))
    output_key = canonical_momentum_key(output)
    coefficient = Fraction(lattice_cocycle_sign(oriented_left, oriented_right))
    return {output_key: coefficient}


def momentum_momentum_product(
    left: tuple[int, ...], right: tuple[int, ...]
) -> SparseVector:
    """Dispatch the weight-two product of two even norm-four momentum states.

    For E_[alpha]=e^alpha+e^-alpha and E_[beta]=e^beta+e^-beta,
    the four exponential terms contribute to the z^-2 coefficient only
    when one signed inner product is -2. Therefore:
      * alpha=+/-beta: opposite-charge terms give the oscillator self-product;
      * |(alpha,beta)|=2: two singular terms give a norm-four momentum state;
      * |(alpha,beta)|<=1: the product is zero.

    The Leech lattice has no norm-two vectors, so distinct minimal vectors
    cannot have inner product +/-3. The input validator enforces membership
    in the norm-four Leech shell. All inner products are computed exactly.
    """
    left = _validate_minimal_leech_coordinate(left)
    right = _validate_minimal_leech_coordinate(right)
    inner_numerator = lattice_inner_product_numerator(left, right)
    if inner_numerator % 8:
        raise ArithmeticError("Leech inner product is not integral")
    inner_product = inner_numerator // 8

    if inner_product in (4, -4):
        return momentum_opposite_pair_self_product(left)
    if abs(inner_product) == 2:
        return momentum_distinct_inner_product_minus_two_product(left, right)
    if abs(inner_product) <= 1:
        return {}
    raise ValueError("unexpected inner product for norm-four Leech shell vectors")


def momentum_inner_product_distribution(
    reference: tuple[int, ...],
) -> dict[int, int]:
    """Count all 196560 minimal-shell vectors by exact inner product."""
    reference = _validate_minimal_leech_coordinate(reference)
    from collections import Counter
    from experiments.moonshine_sierpinski.leech_golay_construction import (
        leech_minimal_vectors,
    )

    counts = Counter(
        lattice_inner_product_numerator(reference, vector) // 8
        for vector in leech_minimal_vectors()
    )
    return dict(sorted(counts.items()))



def griess_basis_bilinear_form(left: BasisKey, right: BasisKey) -> Fraction:
    """Invariant weight-two pairing on the implemented untwisted basis.

    Oscillator states use the Heisenberg Fock pairing. Even momentum-orbit
    states E_[alpha]=e^alpha+e^-alpha are orthogonal unless their antipodal
    orbits agree, in which case the two exponential pairings contribute 2.
    Oscillator and momentum sectors are orthogonal.
    """
    if not isinstance(left, tuple) or not isinstance(right, tuple):
        raise TypeError("Griess basis keys must be tuples")
    if len(left) == 3 and left[0] == "osc":
        if len(right) == 3 and right[0] == "osc":
            return oscillator_bilinear_form(
                (left[1], left[2]), (right[1], right[2])
            )
        if len(right) == 2 and right[0] == "mom":
            return Fraction(0)
    if len(left) == 2 and left[0] == "mom":
        if len(right) == 3 and right[0] == "osc":
            return Fraction(0)
        if len(right) == 2 and right[0] == "mom":
            left_key = canonical_momentum_key(left[1])
            right_key = canonical_momentum_key(right[1])
            return Fraction(2 if left_key == right_key else 0)
    raise ValueError("unrecognized weight-two Griess basis key")


def griess_sparse_bilinear_form(
    left: SparseVector, right: SparseVector
) -> Fraction:
    """Pair two exact sparse weight-two vectors."""
    return sum(
        left_coefficient * right_coefficient
        * griess_basis_bilinear_form(left_key, right_key)
        for left_key, left_coefficient in left.items()
        for right_key, right_coefficient in right.items()
    )


def untwisted_weight_two_product(left: BasisKey, right: BasisKey) -> SparseVector:
    """Dispatch every product block currently implemented in the untwisted space."""
    if not isinstance(left, tuple) or not isinstance(right, tuple):
        raise TypeError("Griess basis keys must be tuples")
    if len(left) == 3 and left[0] == "osc":
        left_pair = (left[1], left[2])
        if len(right) == 3 and right[0] == "osc":
            return oscillator_oscillator_product(left_pair, (right[1], right[2]))
        if len(right) == 2 and right[0] == "mom":
            return oscillator_momentum_product(left_pair, right[1])
    if len(left) == 2 and left[0] == "mom":
        if len(right) == 3 and right[0] == "osc":
            return oscillator_momentum_product((right[1], right[2]), left[1])
        if len(right) == 2 and right[0] == "mom":
            return momentum_momentum_product(left[1], right[1])
    raise ValueError("unrecognized weight-two Griess basis key")


def griess_invariance_residual(
    left: BasisKey, right: BasisKey, probe: BasisKey
) -> Fraction:
    """Return <left_1 right, probe> - <right, left_1 probe> exactly."""
    left_right = untwisted_weight_two_product(left, right)
    left_probe = untwisted_weight_two_product(left, probe)
    return (
        griess_sparse_bilinear_form(left_right, {probe: Fraction(1)})
        - griess_sparse_bilinear_form({right: Fraction(1)}, left_probe)
    )


def untwisted_invariant_form_audit() -> dict:
    """Small exact certificate for the bilinear form and invariance fixtures."""
    alpha = (4, 4) + (0,) * 22
    beta = (-4, 0, 4) + (0,) * 21
    gamma = tuple(a + b for a, b in zip(alpha, beta))
    keys: tuple[BasisKey, ...] = (
        ("osc", 0, 0),
        ("osc", 0, 1),
        ("osc", 3, 17),
        ("mom", canonical_momentum_key(alpha)[1]),
        ("mom", canonical_momentum_key(beta)[1]),
        ("mom", canonical_momentum_key(gamma)[1]),
    )
    residuals = [
        griess_invariance_residual(left, right, probe)
        for left in keys for right in keys for probe in keys
    ]
    return {
        "pairing_symmetric": all(
            griess_basis_bilinear_form(left, right)
            == griess_basis_bilinear_form(right, left)
            for left in keys for right in keys
        ),
        "invariance_fixture_count": len(residuals),
        "invariance_zero_count": sum(value == 0 for value in residuals),
        "invariance_all_zero": all(value == 0 for value in residuals),
        "scope": "exact invariant-form checks on selected untwisted basis fixtures; not a full 196884-dimensional algebra certificate",
    }



def untwisted_invariant_form_global_audit() -> dict:
    """Certify the Gram-matrix structure on the complete implemented untwisted basis.

    This enumerates every minimal Leech vector to establish the 98,280
    antipodal momentum orbits, and checks every pair in the 300-state
    oscillator block. The momentum Gram block is diagonal by construction:
    each distinct orbit is orthogonal and each orbit has norm 2.
    """
    from experiments.moonshine_sierpinski.leech_golay_construction import (
        leech_minimal_vectors,
    )

    oscillator_keys: tuple[BasisKey, ...] = tuple(
        ("osc", i, j) for i in range(24) for j in range(i, 24)
    )
    oscillator_pair_checks = 0
    for left in oscillator_keys:
        for right in oscillator_keys:
            i, j = left[1], left[2]
            expected = Fraction(2 if i == j else 1) if left == right else Fraction(0)
            actual = griess_basis_bilinear_form(left, right)
            if actual != expected:
                raise AssertionError(
                    f"oscillator Gram mismatch for {left}, {right}: {actual}"
                )
            oscillator_pair_checks += 1

    minimal_vectors = leech_minimal_vectors()
    orbit_multiplicities = Counter(
        canonical_momentum_key(vector) for vector in minimal_vectors
    )
    if len(minimal_vectors) != 196560:
        raise AssertionError("minimal Leech shell must contain 196560 vectors")
    if len(orbit_multiplicities) != 98280:
        raise AssertionError("minimal Leech shell must contain 98280 antipodal orbits")
    if set(orbit_multiplicities.values()) != {2}:
        raise AssertionError("every antipodal momentum orbit must have two representatives")

    for key in orbit_multiplicities:
        if griess_basis_bilinear_form(key, key) != 2:
            raise AssertionError(f"momentum basis vector has incorrect norm: {key}")

    oscillator_diagonal = Counter(
        int(griess_basis_bilinear_form(key, key)) for key in oscillator_keys
    )
    momentum_diagonal = Counter(
        int(griess_basis_bilinear_form(key, key)) for key in orbit_multiplicities
    )
    diagonal_multiplicities = oscillator_diagonal + momentum_diagonal
    if diagonal_multiplicities != Counter({1: 276, 2: 98304}):
        raise AssertionError(
            f"unexpected full untwisted Gram diagonal: {diagonal_multiplicities}"
        )

    dimension = len(oscillator_keys) + len(orbit_multiplicities)
    return {
        "oscillator_basis_dimension": len(oscillator_keys),
        "oscillator_gram_pair_checks": oscillator_pair_checks,
        "minimal_leech_vectors": len(minimal_vectors),
        "momentum_orbit_basis_dimension": len(orbit_multiplicities),
        "antipodal_orbit_multiplicity": 2,
        "total_untwisted_basis_dimension": dimension,
        "gram_rank": dimension,
        "gram_signature": [dimension, 0, 0],
        "gram_diagonal_multiplicities": {
            str(norm): count for norm, count in sorted(diagonal_multiplicities.items())
        },
        "gram_determinant": "2^98304",
        "positive_definite": True,
        "scope": (
            "basis-wide exact Gram-matrix certificate for the implemented "
            "98580-dimensional untwisted subspace; this is not a full "
            "196884-dimensional Griess algebra or a product-invariance proof"
        ),
    }


def untwisted_oscillator_invariance_global_audit() -> dict:
    """Exhaust the oscillator trilinear invariance identity by support class.

    For oscillator basis states A_ij, the trilinear form
    <A_ij _1 A_kl, A_mn> can be nonzero only when every coordinate index
    among i,j,k,l,m,n occurs an even number of times. Enumerating every
    ordered pairing of the even-multiplicity six-index multisets therefore
    covers every potentially nonzero basis triple; all other triples vanish
    on both sides by the contraction formula.
    """
    from itertools import combinations, permutations

    candidate_triples: set[tuple[tuple[int, int], tuple[int, int], tuple[int, int]]] = set()

    multisets = []
    multisets.extend((index,) * 6 for index in range(24))
    multisets.extend(
        (left,) * 4 + (right,) * 2
        for left in range(24) for right in range(24) if left != right
    )
    multisets.extend(
        (left, left, middle, middle, right, right)
        for left, middle, right in combinations(range(24), 3)
    )

    for values in multisets:
        for arrangement in set(permutations(values)):
            triple = tuple(
                tuple(sorted((arrangement[offset], arrangement[offset + 1])))
                for offset in (0, 2, 4)
            )
            candidate_triples.add(triple)

    if len(candidate_triples) != 45840:
        raise AssertionError(
            f"unexpected oscillator triple support count: {len(candidate_triples)}"
        )

    def trilinear(
        left: tuple[int, int],
        right: tuple[int, int],
        probe: tuple[int, int],
    ) -> Fraction:
        product = oscillator_oscillator_product(left, right)
        probe_key: BasisKey = ("osc", probe[0], probe[1])
        return griess_sparse_bilinear_form(product, {probe_key: Fraction(1)})

    checked = 0
    nonzero = 0
    for left, right, probe in candidate_triples:
        forward = trilinear(left, right, probe)
        reverse = trilinear(left, probe, right)
        if forward != reverse:
            raise AssertionError(
                "oscillator invariant-form mismatch for "
                f"{left}, {right}, {probe}: {forward} != {reverse}"
            )
        checked += 1
        nonzero += int(forward != 0)

    return {
        "oscillator_basis_dimension": 300,
        "potentially_nonzero_ordered_triples": len(candidate_triples),
        "invariance_checks": checked,
        "nonzero_trilinear_values": nonzero,
        "zero_residual_count": checked,
        "all_potentially_nonzero_triples_checked": checked == 45840,
        "scope": (
            "exhaustive exact invariance audit for the 300-dimensional "
            "oscillator block; zero-support triples vanish by the "
            "even-index-multiplicity contraction criterion"
        ),
    }


def untwisted_heisenberg_block_audit() -> dict:
    """Return formula-level scope and exact normalization checks."""
    sample = tuple([4, 4] + [0] * 22)
    sample_key = canonical_momentum_key(sample)
    identity_momentum = conformal_identity_momentum_product(sample)
    identity_oscillator = conformal_identity_oscillator_product((3, 17))
    return {
        "implemented_blocks": [
            "oscillator x oscillator -> oscillator",
            "oscillator x even norm-four momentum -> even norm-four momentum",
            "opposite momentum orbit x itself -> oscillator",
            "distinct norm-four momentum pairs with absolute inner product 2 -> momentum",
        ],
        "oscillator_basis_dimension": 300,
        "momentum_basis_dimension": 98280,
        "sample_momentum_key": sample_key,
        "sample_momentum_identity_coefficient": str(identity_momentum[sample_key]),
        "sample_oscillator_identity": {
            str(key): str(value) for key, value in identity_oscillator.items()
        },
        "momentum_opposite_pair_self_product_implemented": True,
        "distinct_momentum_inner_product_minus_two_implemented": True,
        "complete_weight_two_momentum_momentum_dispatch_implemented": True,
        "general_distinct_momentum_product_implemented": True,
        "lattice_cocycle_implemented": True,
        "invariant_bilinear_form_implemented": True,
        "invariant_form_fixture_audit": untwisted_invariant_form_audit(),
        "invariant_form_global_audit": untwisted_invariant_form_global_audit(),
        "oscillator_invariance_global_audit": untwisted_oscillator_invariance_global_audit(),
        "twisted_blocks_implemented": False,
        "full_griess_product_constructed": False,
        "monster_action_constructed": False,
        "scope": "exact oscillator and complete momentum-momentum blocks of the untwisted weight-two product; twisted sector remains open",
    }


if __name__ == "__main__":
    import json
    print(json.dumps(untwisted_heisenberg_block_audit(), indent=2, sort_keys=True))
