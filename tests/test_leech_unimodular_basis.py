import unittest

from experiments.moonshine_sierpinski.leech_unimodular_basis import (
    leech_unimodular_basis_audit,
)

class LeechUnimodularBasisTests(unittest.TestCase):
    def test_rank_and_exact_covolume(self):
        result = leech_unimodular_basis_audit()
        self.assertEqual(result["rank"], 24)
        self.assertEqual(result["basis_columns_checked"], 24)
        self.assertEqual(result["coordinate_basis_determinant"], 1 << 36)
        self.assertEqual(result["coordinate_covolume_from_index"], 1 << 36)

    def test_even_unimodular_gram_certificate(self):
        result = leech_unimodular_basis_audit()
        self.assertTrue(result["scaled_gram_integral"])
        self.assertTrue(result["scaled_gram_even"])
        self.assertEqual(result["scaled_gram_determinant"], 1)
        self.assertTrue(result["positive_definite"])
        self.assertTrue(result["even_unimodular"])

    def test_minimum_norm_four_from_golay_congruences(self):
        result = leech_unimodular_basis_audit()
        self.assertEqual(result["minimum_norm_lower_bound"], 4)
        self.assertEqual(result["minimum_norm_attained"], 4)
        self.assertEqual(result["minimal_vectors_at_minimum"], 196560)

if __name__ == "__main__":
    unittest.main()
