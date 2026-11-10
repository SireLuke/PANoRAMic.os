import unittest

from experiments.gosset_local_cell_star_audit import run_audit


class GossetLocalCellStarAuditTests(unittest.TestCase):
    def test_exact_cell_star_and_facet_pairing(self):
        result = run_audit()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["incident_cells"]["8_simplex"], 17280)
        self.assertEqual(result["incident_cells"]["8_orthoplex"], 2160)
        self.assertTrue(result["opposite_vertex_shell"]["exact_set_equality"])
        incidence = result["origin_containing_facet_incidence"]
        self.assertEqual(incidence["unique_facets"], 207360)
        self.assertEqual(incidence["multiplicity_counts"], {2: 207360})


if __name__ == "__main__":
    unittest.main()
