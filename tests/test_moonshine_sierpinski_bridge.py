import unittest

from experiments.moonshine_sierpinski.lattice_modular_audit import (
    discriminant_delta, e8_product_theta, leech_theta_reference,
    moonshine_character_reference, scaling_ladder,
)
from experiments.moonshine_sierpinski.sierpinski_graph_spectrum import (
    audit_sierpinski_stage, run_stages, sierpinski_graph,
)

class ModularThetaTests(unittest.TestCase):
    def test_e8_theta_first_coefficients(self):
        result = e8_product_theta(1, degree=3)
        self.assertEqual(result["rank"], 8)
        self.assertEqual(result["theta_weight"], 4)
        self.assertEqual(result["coefficients_q0_to_qN"], [1, 240, 2160, 6720])

    def test_leech_theta_shells(self):
        result = leech_theta_reference(6)
        self.assertEqual(result["first_shell_checks"]["q1_norm2_vectors"], 0)
        self.assertEqual(result["first_shell_checks"]["q2_norm4_vectors"], 196560)
        self.assertEqual(result["first_shell_checks"]["q3_norm6_vectors"], 16773120)

    def test_delta_initial_coefficients(self):
        self.assertEqual(discriminant_delta(4), [0, 1, -24, 252, -1472])

    def test_e8_product_ladder(self):
        ladder = scaling_ladder()
        self.assertEqual([(x["rank"], x["theta_weight"]) for x in ladder],
                         [(448, 224), (896, 448), (1664, 832)])
        self.assertEqual([x["coefficients_q0_to_qN"][1] for x in ladder],
                         [13440, 26880, 49920])

    def test_moonshine_values_are_reference_only(self):
        ref = moonshine_character_reference()
        self.assertEqual(ref["coefficients"]["q^1"], 196884)
        self.assertEqual(ref["first_monster_decomposition"]["identity"], "196884 = 1 + 196883")
        self.assertIn("not computed", ref["construction_status"])

class SierpinskiGraphTests(unittest.TestCase):
    def test_graph_count_recurrence(self):
        expected = [(3, 3), (6, 9), (15, 27), (42, 81), (123, 243)]
        for stage, counts in enumerate(expected):
            vertices, edges = sierpinski_graph(stage)
            self.assertEqual((len(vertices), len(edges)), counts)

    def test_stage_zero_spectrum(self):
        result = audit_sierpinski_stage(0)
        self.assertEqual(result["spectral_status"], "computed_jacobi_float")
        self.assertEqual(result["laplacian_eigenvalues"], [0.0, 3.0, 3.0])

    def test_low_stage_spectra(self):
        for result in run_stages(3):
            self.assertEqual(result["spectral_status"], "computed_jacobi_float")
            self.assertAlmostEqual(result["laplacian_eigenvalues"][0], 0.0, places=8)
            self.assertAlmostEqual(sum(result["laplacian_eigenvalues"]),
                                   result["laplacian_trace"], places=6)

    def test_stage_four_combinatorial_only(self):
        result = audit_sierpinski_stage(4)
        self.assertEqual((result["vertices"], result["edges"]), (123, 243))
        self.assertEqual(result["spectral_status"], "not_computed")

if __name__ == "__main__":
    unittest.main()
