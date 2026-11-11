import unittest

from experiments.moonshine_sierpinski.leech_z2_orbifold_character import (
    leech_z2_orbifold_character,
)

class LeechZ2OrbifoldCharacterTests(unittest.TestCase):
    def test_initial_moonshine_grades(self):
        result = leech_z2_orbifold_character(4)
        self.assertEqual(result["untwisted_fixed_dimensions"], {
            "0": 1, "1": 0, "2": 98580, "3": 10745856, "4": 432155586
        })
        self.assertEqual(result["twisted_fixed_dimensions"], {
            "0": 0, "1": 0, "2": 98304, "3": 10747904, "4": 432144384
        })
        self.assertEqual(result["moonshine_orbifold_graded_dimensions"], {
            "0": 1, "1": 0, "2": 196884, "3": 21493760, "4": 864299970
        })
        self.assertTrue(result["reference_match"])

    def test_weight_one_currents_are_projected_out(self):
        result = leech_z2_orbifold_character(2)
        self.assertEqual(result["untwisted_fixed_dimensions"]["1"], 0)
        self.assertEqual(result["twisted_fixed_dimensions"]["1"], 0)

    def test_twisted_sector_starts_at_weight_three_halves(self):
        result = leech_z2_orbifold_character(4)
        self.assertEqual(result["twisted_ground_conformal_weight"], "3/2")
        self.assertEqual(result["twisted_ground_multiplicity"], 4096)
        self.assertEqual(result["twisted_fixed_dimensions"]["1"], 0)
        self.assertEqual(result["twisted_fixed_dimensions"]["2"], 98304)

    def test_projection_is_exact_and_reference_only_for_voa_structure(self):
        result = leech_z2_orbifold_character(4)
        self.assertFalse(result["vertex_operator_extension_constructed"])
        self.assertFalse(result["monster_action_constructed"])

if __name__ == "__main__":
    unittest.main()
