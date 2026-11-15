import unittest

from experiments.gosset_graph_incidence_reconciliation import run_reconciliation


class GossetGraphIncidenceReconciliationTests(unittest.TestCase):
    def test_graph_orthoplexes_reconcile_with_simplex_star(self):
        result = run_reconciliation()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["root_count"], 240)
        self.assertTrue(result["graph_orbit_equals_weyl_orbit"])
        self.assertEqual(result["graph_derived_orthoplex_cell_count"], 2160)
        self.assertEqual(result["simplex_cell_count"], 17280)
        self.assertEqual(result["opposite_norm_four_shell_count"], 2160)
        incidence = result["incidence_reconciliation"]
        self.assertEqual(incidence["unique_origin_containing_facets"], 207360)
        self.assertEqual(incidence["combined_facet_incidence_multiplicity"], 2)
        self.assertEqual(
            incidence["orthoplex_face_multiplicity_counts"],
            {"1": 138240, "2": 69120},
        )
        self.assertEqual(
            incidence["shared_facet_type_counts"],
            {
                "simplex+orthoplex": 138240,
                "orthoplex+orthoplex": 69120,
                "simplex+simplex": 0,
            },
        )
        self.assertTrue(incidence["all_shared_faces_pair_exactly"])
        self.assertTrue(incidence["all_incident_cell_intersections_equal_shared_face"])
        self.assertTrue(incidence["all_incident_cell_interiors_on_opposite_halfspaces"])


if __name__ == "__main__":
    unittest.main()
