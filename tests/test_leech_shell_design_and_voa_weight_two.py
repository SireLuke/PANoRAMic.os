import unittest

from experiments.moonshine_sierpinski.leech_shell_design_moments import (
    leech_minimal_shell_directional_moments,
)
from experiments.moonshine_sierpinski.leech_voa_weight_two import (
    leech_voa_weight_two_decomposition,
)

class LeechShellMomentTests(unittest.TestCase):
    def test_four_directions_match_through_degree_ten(self):
        result = leech_minimal_shell_directional_moments(10)
        self.assertEqual(result["point_count"], 196560)
        for direction, degrees in result["directions"].items():
            for degree in ("2", "4", "6", "8", "10"):
                self.assertTrue(degrees[degree]["exact_match"],
                                msg=f"{direction} failed degree {degree}")

    def test_degree_twelve_distinguishes_all_test_directions(self):
        result = leech_minimal_shell_directional_moments(12)
        for direction, degrees in result["directions"].items():
            self.assertFalse(degrees["12"]["exact_match"],
                             msg=f"{direction} unexpectedly matched degree 12")

class LeechVoaWeightTwoTests(unittest.TestCase):
    def test_weight_two_decomposition(self):
        result = leech_voa_weight_two_decomposition()
        self.assertEqual(result["momentum_states_from_norm_4_vectors"], 196560)
        self.assertEqual(result["oscillator_only_states"], 324)
        self.assertEqual(result["total_weight_two_dimension"], 196884)
        self.assertTrue(result["numerical_dimension_match"])
        self.assertEqual(result["monster_representation_decomposition"], "not_computed")
        self.assertEqual(result["moonshine_Z2_orbifold"], "not_constructed")

if __name__ == "__main__":
    unittest.main()
