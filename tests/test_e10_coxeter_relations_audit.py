import unittest

from experiments.e10_coxeter_relations_audit import run_audit


class E10CoxeterAuditTests(unittest.TestCase):
    def test_exact_coxeter_relations_and_affine_link(self):
        result = run_audit()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["gram_signature"], (9, 1, 0))
        self.assertEqual(result["gram_determinant"], "-1/1024")
        self.assertEqual(result["coxeter_relations"]["total"], 55)
        self.assertEqual(result["generator_gram_preservation_checks"], 10)
        self.assertEqual(
            result["affine_E9_principal_minor_counts"],
            {"positive": 510, "zero": 1},
        )


if __name__ == "__main__":
    unittest.main()
