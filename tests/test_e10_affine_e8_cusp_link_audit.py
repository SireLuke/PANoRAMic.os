import unittest

from experiments.e10_affine_e8_cusp_link_audit import run_audit


class E10AffineE8CuspLinkTests(unittest.TestCase):
    def test_exact_affine_e8_root_link_and_translation(self):
        result = run_audit()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["affine_link_type"], "affine E8")
        self.assertEqual(len(result["link_nodes"]), 9)
        self.assertEqual(len(result["link_edges"]), 8)
        self.assertEqual(result["null_root_marks_gcd"], 1)
        self.assertEqual(
            result["highest_root_coefficients_in_finite_simple_basis"],
            [2, 3, 4, 6, 5, 4, 3, 2],
        )
        self.assertEqual(result["highest_root_norm_squared"], "2")
        self.assertEqual(result["affine_root_norm_squared"], "2")
        self.assertTrue(result["affine_simple_root_gram_matches_e10_link"])
        self.assertEqual(result["affine_reflection_generators"], 9)
        self.assertEqual(result["involution_relations"], 9)
        self.assertEqual(result["adjacent_order_three_relations"], 8)
        self.assertEqual(result["nonadjacent_commutations"], 28)
        self.assertEqual(result["total_pair_relations"], 36)
        self.assertTrue(
            result["translation_witness"]["exact_translation_by_highest_root"]
        )


if __name__ == "__main__":
    unittest.main()
