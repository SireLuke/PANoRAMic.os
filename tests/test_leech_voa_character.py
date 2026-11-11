import unittest

from experiments.moonshine_sierpinski.leech_voa_character import (
    eta_inverse_24_product,
    leech_lattice_voa_character,
)

class LeechVoaCharacterTests(unittest.TestCase):
    def test_eta_inverse_24_initial_coefficients(self):
        self.assertEqual(eta_inverse_24_product(3), [1, 24, 324, 3200])

    def test_leech_lattice_voa_initial_graded_dimensions(self):
        result = leech_lattice_voa_character(3)
        self.assertEqual(result["graded_dimensions"],
                         {"0": 1, "1": 24, "2": 196884, "3": 21493760})
        self.assertFalse(result["moonshine_orbifold_constructed"])
        self.assertFalse(result["monster_action_constructed"])

if __name__ == "__main__":
    unittest.main()
