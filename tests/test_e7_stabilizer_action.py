import unittest

from core.geometry.e7_stabilizer_action import (
    E7_EXPECTED_WEYL_ORDER,
    E7_WEYL_ORDER,
    E7StabilizerAction,
    audit_e7_stabilizer,
)


class E7StabilizerActionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.action = E7StabilizerAction.build()

    def test_perpendicular_subsystem_has_126_roots(self):
        self.assertEqual(len(self.action.roots), 126)
        self.assertTrue(all(
            sum(a * b for a, b in zip(self.action.selected_e8_root, root)) == 0
            for root in self.action.roots
        ))

    def test_seven_simple_roots_have_e7_gram_structure(self):
        self.assertEqual(len(self.action.simple_roots), 7)
        self.assertEqual(len(self.action.generators), 7)

    def test_generators_are_permutations_and_involutions(self):
        for permutation in self.action.generators:
            self.assertEqual(sorted(permutation), list(range(126)))
            self.assertTrue(all(
                permutation[permutation[i]] == i for i in range(126)
            ))

    def test_each_generator_preserves_the_perpendicular_root_set(self):
        roots = self.action.roots
        for permutation in self.action.generators:
            self.assertTrue(all(
                sum(a * b for a, b in zip(self.action.selected_e8_root,
                                           roots[permutation[i]])) == 0
                for i in range(126)
            ))

    def test_generated_action_is_transitive_on_126_roots(self):
        self.assertEqual(len(self.action.orbit_indices()), 126)

    def test_root_action_is_faithful_on_seven_dimensional_span(self):
        self.assertEqual(len(self.action.roots), 126)
        # The implementation's exact-rank validation is exercised here.
        self.assertTrue(self.action.validate())

    def test_weyl_order_and_stabilizer_audit(self):
        self.assertEqual(E7_WEYL_ORDER, E7_EXPECTED_WEYL_ORDER)
        result = audit_e7_stabilizer()
        self.assertEqual(result["e7_weyl_order_from_exponents"], 2_903_040)
        self.assertEqual(result["e7_root_stabilizer_order_derived"], 23_040)
        self.assertEqual(result["e7_root_orbit_size"], 126)
        self.assertFalse(result["explicit_group_element_enumeration"])


if __name__ == "__main__":
    unittest.main()
