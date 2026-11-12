import unittest

from experiments.moonshine_sierpinski.leech_monster_representation_bridge import (
    leech_to_monster_representation_bridge,
)


class LeechMonsterRepresentationBridgeTests(unittest.TestCase):
    def test_first_four_identity_class_decompositions(self):
        result = leech_to_monster_representation_bridge(4)
        self.assertEqual(result["identity_checks_passed"], 4)
        self.assertEqual(
            [row["representation_dimension_sum"]
             for row in result["identity_class_checks"]],
            [196884, 21493760, 864299970, 20245856256],
        )

    def test_first_three_two_b_character_coefficients(self):
        result = leech_to_monster_representation_bridge(4)
        self.assertEqual(result["two_B_checks_passed"], 3)
        self.assertEqual(
            [row["trace_sum"] for row in result["two_B_McKay_Thompson_checks"]],
            [276, -2048, 11202],
        )

    def test_reference_audit_does_not_claim_group_action_construction(self):
        result = leech_to_monster_representation_bridge(2)
        self.assertTrue(result["reference_data_only"])
        self.assertFalse(result["Monster_representation_constructed"])
        self.assertFalse(result["Monster_action_on_orbifold_constructed"])
        self.assertFalse(result["McKay_Thompson_series_derived_from_group_action"])

    def test_rejects_unsupported_degree(self):
        with self.assertRaises(ValueError):
            leech_to_monster_representation_bridge(5)


if __name__ == "__main__":
    unittest.main()
