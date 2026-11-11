import unittest

from experiments.moonshine_sierpinski.leech_golay_construction import (
    extended_golay_codewords,
    golay_code_audit,
    leech_construction_audit,
    leech_minimal_vectors,
)

class GolayCodeTests(unittest.TestCase):
    def test_extended_golay_parameters_and_weight_enumerator(self):
        audit = golay_code_audit()
        self.assertEqual((audit["length"], audit["dimension"], audit["codewords"]), (24, 12, 4096))
        self.assertEqual(audit["minimum_distance"], 8)
        self.assertEqual(audit["weight_distribution"], {0: 1, 8: 759, 12: 2576, 16: 759, 24: 1})
        self.assertTrue(audit["self_orthogonal"])
        self.assertTrue(audit["self_dual_by_dimension"])

    def test_codeword_count_and_uniqueness(self):
        words = extended_golay_codewords()
        self.assertEqual(len(words), 4096)
        self.assertEqual(len(set(words)), 4096)

class LeechMinimalShellTests(unittest.TestCase):
    def test_three_minimal_vector_families(self):
        vectors = leech_minimal_vectors()
        self.assertEqual(len(vectors), 196560)
        self.assertEqual(len(set(vectors)), 196560)

    def test_full_explicit_construction_membership(self):
        audit = leech_construction_audit()
        self.assertEqual(audit["minimal_vectors"], 196560)
        self.assertEqual(audit["integral_coordinate_squared_norm"], 32)
        self.assertEqual(audit["lattice_squared_norm"], 4)
        self.assertEqual(audit["family_counts"], {
            "A_two_pm4": 1104,
            "B_octad_pm2_even_minus": 97152,
            "C_one_pm3_twenty_three_pm1": 98304,
        })
        self.assertEqual(audit["root_count_norm_2"], 0)
        self.assertEqual(audit["membership_checks"], "all 196560 generated vectors passed")

if __name__ == "__main__":
    unittest.main()
