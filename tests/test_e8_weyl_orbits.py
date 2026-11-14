import unittest
from fractions import Fraction as Q

from core.geometry.e8_root_system import e8_roots_exact
from core.geometry.e8_weyl_orbits import (
    E8_EXPECTED_WEYL_ORDER, E8_WEYL_ORDER, E8WeylAction,
    audit_e8_root_orbits, reflect_root,
)


class E8WeylOrbitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.action = E8WeylAction.build()

    def test_weyl_order_from_exponents(self):
        self.assertEqual(E8_WEYL_ORDER, E8_EXPECTED_WEYL_ORDER)
        self.assertEqual(E8_WEYL_ORDER, 696729600)

    def test_all_eight_generators_are_root_permutations_and_involutions(self):
        roots = self.action.roots
        root_set = set(roots)
        self.assertEqual(len(self.action.generators), 8)
        for permutation in self.action.generators:
            self.assertEqual(set(permutation), set(range(240)))
            self.assertTrue(all(roots[permutation[permutation[i]]] == roots[i]
                                for i in range(240)))
            self.assertTrue(all(roots[permutation[i]] in root_set for i in range(240)))

    def test_reflection_formula_is_exact(self):
        alpha = self.action.simple_roots[0]
        for root in self.action.roots:
            reflected = reflect_root(root, alpha)
            self.assertIn(reflected, set(self.action.roots))
            self.assertEqual(sum(x*x for x in reflected), Q(2))

    def test_all_roots_form_one_weyl_orbit(self):
        orbits = self.action.orbit_partition()
        self.assertEqual(len(orbits), 1)
        self.assertEqual(len(orbits[0]), 240)

    def test_root_stabilizer_orbit_stabilizer(self):
        audit = audit_e8_root_orbits()
        self.assertEqual(audit.orbit_size, 240)
        self.assertEqual(audit.stabilizer_order, 2903040)
        self.assertEqual(audit.orthogonal_root_count, 126)
        self.assertTrue(audit.validate())
        self.assertEqual(audit.orbit_stabilizer_product, 696729600)

    def test_reject_non_root_seed(self):
        with self.assertRaises(ValueError):
            self.action.root_orbit((Q(0),) * 8)

    def test_each_root_has_126_orthogonal_roots(self):
        for root in self.action.roots:
            self.assertEqual(self.action.orthogonal_root_count(root), 126)


if __name__ == "__main__":
    unittest.main()
