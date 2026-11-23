import random
import unittest
from fractions import Fraction

from experiments.moonshine_sierpinski.griess_untwisted_heisenberg import (
    canonical_momentum_key,
    conformal_identity_momentum_product,
    conformal_identity_oscillator_product,
    oscillator_bilinear_form,
    oscillator_momentum_product,
    oscillator_oscillator_product,
    momentum_opposite_pair_self_product,
    momentum_distinct_inner_product_minus_two_product,
    momentum_momentum_product,
    momentum_inner_product_distribution,
)
from experiments.moonshine_sierpinski.leech_lattice_cocycle import (
    lattice_cocycle_sign,
)


class UntwistedHeisenbergProductTests(unittest.TestCase):
    def test_oscillator_product_is_commutative(self):
        pairs = [(i, j) for i in range(24) for j in range(i, 24)]
        rng = random.Random(20261123)
        for _ in range(500):
            left, right = rng.choice(pairs), rng.choice(pairs)
            self.assertEqual(
                oscillator_oscillator_product(left, right),
                oscillator_oscillator_product(right, left),
            )

    def test_oscillator_product_exact_contraction_fixtures(self):
        self.assertEqual(
            oscillator_oscillator_product((2, 2), (2, 2)),
            {("osc", 2, 2): Fraction(4)},
        )
        self.assertEqual(
            oscillator_oscillator_product((1, 3), (3, 7)),
            {("osc", 1, 7): Fraction(1)},
        )
        self.assertEqual(
            oscillator_oscillator_product((1, 3), (1, 3)),
            {
                ("osc", 3, 3): Fraction(1),
                ("osc", 1, 1): Fraction(1),
            },
        )

    def test_oscillator_identity_on_all_300_basis_states(self):
        for i in range(24):
            for j in range(i, 24):
                self.assertEqual(
                    conformal_identity_oscillator_product((i, j)),
                    {("osc", i, j): Fraction(1)},
                )

    def test_oscillator_form_is_symmetric(self):
        pairs = [(i, j) for i in range(24) for j in range(i, 24)]
        rng = random.Random(240024)
        for _ in range(1000):
            left, right = rng.choice(pairs), rng.choice(pairs)
            self.assertEqual(
                oscillator_bilinear_form(left, right),
                oscillator_bilinear_form(right, left),
            )

    def test_oscillator_momentum_formula_and_antipodal_invariance(self):
        vector = (4, 4) + (0,) * 22
        key = canonical_momentum_key(vector)
        self.assertEqual(oscillator_momentum_product((0, 1), vector), {
            key: Fraction(2)
        })
        self.assertEqual(
            oscillator_momentum_product((0, 1), vector),
            oscillator_momentum_product((0, 1), tuple(-x for x in vector)),
        )
        self.assertEqual(oscillator_momentum_product((0, 2), vector), {})

    def test_conformal_identity_on_norm_four_momentum_states(self):
        fixtures = [
            (4, 4) + (0,) * 22,
            (4, -4) + (0,) * 22,
        ]
        for vector in fixtures:
            key = canonical_momentum_key(vector)
            self.assertEqual(
                conformal_identity_momentum_product(vector),
                {key: Fraction(1)},
            )

    def test_rejects_non_leech_or_wrong_norm_inputs(self):
        with self.assertRaises(ValueError):
            canonical_momentum_key((1,) * 24)
        with self.assertRaises(ValueError):
            canonical_momentum_key((4, 0) + (0,) * 22)
        with self.assertRaises(TypeError):
            canonical_momentum_key(tuple([4.0, 4] + [0] * 22))


    def test_opposite_pair_self_product_exact_coefficients(self):
        vector = (4, 4) + (0,) * 22
        self.assertEqual(
            momentum_opposite_pair_self_product(vector),
            {
                ("osc", 0, 0): Fraction(2),
                ("osc", 0, 1): Fraction(4),
                ("osc", 1, 1): Fraction(2),
            },
        )

    def test_opposite_pair_self_product_is_antipodally_invariant(self):
        vectors = [
            (4, 4) + (0,) * 22,
            (4, -4) + (0,) * 22,
            (0, 0, 4, 4) + (0,) * 20,
        ]
        for vector in vectors:
            self.assertEqual(
                momentum_opposite_pair_self_product(vector),
                momentum_opposite_pair_self_product(tuple(-x for x in vector)),
            )

    def test_opposite_pair_self_product_has_only_oscillator_outputs(self):
        result = momentum_opposite_pair_self_product((4, 4) + (0,) * 22)
        self.assertTrue(result)
        self.assertTrue(all(key[0] == "osc" for key in result))
        self.assertEqual(sum(result.values()), Fraction(8))

    def test_opposite_pair_self_product_rejects_nonminimal_vectors(self):
        with self.assertRaises(ValueError):
            momentum_opposite_pair_self_product((4, 0) + (0,) * 22)


    def test_distinct_momentum_inner_product_minus_two_product(self):
        left = (4, 4) + (0,) * 22
        right = (-4, 0, 4) + (0,) * 21
        output = tuple(a + b for a, b in zip(left, right))
        key = canonical_momentum_key(output)
        self.assertEqual(
            momentum_distinct_inner_product_minus_two_product(left, right),
            {key: Fraction(lattice_cocycle_sign(left, right))},
        )
        self.assertEqual(sum(value * value for value in output), 32)

    def test_distinct_momentum_product_is_commutative(self):
        left = (4, 4) + (0,) * 22
        right = (-4, 0, 4) + (0,) * 21
        self.assertEqual(
            momentum_distinct_inner_product_minus_two_product(left, right),
            momentum_distinct_inner_product_minus_two_product(right, left),
        )

    def test_distinct_momentum_product_is_independent_of_antipodal_representatives(self):
        left = (4, 4) + (0,) * 22
        right = (-4, 0, 4) + (0,) * 21
        expected = momentum_distinct_inner_product_minus_two_product(left, right)
        for a, b in (
            (tuple(-x for x in left), right),
            (left, tuple(-x for x in right)),
            (tuple(-x for x in left), tuple(-x for x in right)),
        ):
            self.assertEqual(
                momentum_distinct_inner_product_minus_two_product(a, b),
                expected,
            )

    def test_distinct_momentum_product_rejects_wrong_inner_product(self):
        left = (4, 4) + (0,) * 22
        right = (4, -4) + (0,) * 22
        with self.assertRaises(ValueError):
            momentum_distinct_inner_product_minus_two_product(left, right)


    def test_complete_momentum_product_dispatches_all_inner_product_classes(self):
        alpha = (4, 4) + (0,) * 22
        opposite = tuple(-x for x in alpha)
        beta = (-4, 0, 4) + (0,) * 21  # (alpha,beta)=-2
        orthogonal = (4, -4) + (0,) * 22  # (alpha,orthogonal)=0

        self.assertEqual(
            momentum_momentum_product(alpha, alpha),
            momentum_opposite_pair_self_product(alpha),
        )
        self.assertEqual(
            momentum_momentum_product(alpha, opposite),
            momentum_opposite_pair_self_product(alpha),
        )
        self.assertEqual(
            momentum_momentum_product(alpha, beta),
            momentum_distinct_inner_product_minus_two_product(alpha, beta),
        )
        self.assertEqual(momentum_momentum_product(alpha, orthogonal), {})

    def test_complete_momentum_product_is_commutative_on_fixtures(self):
        alpha = (4, 4) + (0,) * 22
        fixtures = [
            alpha,
            tuple(-x for x in alpha),
            (-4, 0, 4) + (0,) * 21,
            (4, -4) + (0,) * 22,
            (0, 0, 4, -4) + (0,) * 20,
        ]
        for left in fixtures:
            for right in fixtures:
                self.assertEqual(
                    momentum_momentum_product(left, right),
                    momentum_momentum_product(right, left),
                )

    def test_minimal_shell_inner_product_distribution(self):
        reference = (4, 4) + (0,) * 22
        self.assertEqual(
            momentum_inner_product_distribution(reference),
            {-4: 1, -2: 4600, -1: 47104, 0: 93150, 1: 47104, 2: 4600, 4: 1},
        )


if __name__ == "__main__":
    unittest.main()
