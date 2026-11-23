import unittest

from experiments.moonshine_sierpinski.griess_weight_two_basis import (
    griess_weight_two_basis_certificate,
)


class GriessWeightTwoBasisTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = griess_weight_two_basis_certificate()

    def test_three_basis_block_dimensions(self):
        blocks = self.result["basis_blocks"]
        self.assertEqual(blocks["untwisted_momentum_even"]["dimension"], 98280)
        self.assertEqual(blocks["untwisted_oscillator_symmetric"]["dimension"], 300)
        self.assertEqual(blocks["twisted_oscillator_ground_tensor"]["dimension"], 98304)

    def test_sector_and_total_dimensions(self):
        self.assertEqual(self.result["untwisted_fixed_dimension"], 98580)
        self.assertEqual(self.result["twisted_fixed_dimension"], 98304)
        self.assertEqual(self.result["total_dimension"], 196884)
        self.assertTrue(self.result["dimension_checks_passed"])

    def test_basis_digests_are_stable_sha256_values(self):
        for block in self.result["basis_blocks"].values():
            digest = block["sha256"]
            self.assertEqual(len(digest), 64)
            self.assertTrue(all(character in "0123456789abcdef" for character in digest))

    def test_twisted_labels_are_not_misrepresented_as_an_action(self):
        block = self.result["basis_blocks"]["twisted_oscillator_ground_tensor"]
        self.assertEqual(block["ground_space_status"], "formal labels; representation not constructed")
        self.assertFalse(self.result["twisted_ground_representation_constructed"])

    def test_no_product_or_monster_action_is_claimed(self):
        self.assertFalse(self.result["griess_product_constructed"])
        self.assertFalse(self.result["monster_action_constructed"])


if __name__ == "__main__":
    unittest.main()
