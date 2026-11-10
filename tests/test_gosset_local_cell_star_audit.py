import unittest

from experiments.gosset_local_cell_star_audit import run_audit


class GossetLocalCellStarAuditTests(unittest.TestCase):
    def test_exact_cell_star_and_facet_pairing(self):
        result = run_audit()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["incident_cells"]["8_simplex"], 17280)
        self.assertEqual(result["incident_cells"]["8_orthoplex"], 2160)
        self.assertTrue(result["opposite_vertex_shell"]["exact_set_equality"])
        self.assertTrue(result["cell_metric_checks"]["orthoplex_common_center_and_unit_circumradius"])
        self.assertTrue(result["cell_metric_checks"]["all_eight_opposite_pairs_share_center"])
        incidence = result["origin_containing_facet_incidence"]
        self.assertEqual(incidence["unique_facets"], 207360)
        self.assertEqual(incidence["multiplicity_counts"], {2: 207360})
        self.assertEqual(incidence["simplex_orthoplex_shared_facets"], 138240)
        self.assertEqual(incidence["orthoplex_orthoplex_shared_facets"], 69120)
        self.assertEqual(incidence["simplex_simplex_shared_facets"], 0)
        reroot = result["neighboring_star_reroot_closure"]
        self.assertEqual(reroot["distinct_neighbor_vertices"], 2400)
        self.assertEqual(reroot["neighbor_norm_counts"], {"2": 240, "4": 2160})
        self.assertGreater(reroot["cell_re_root_checks"], 0)
        self.assertEqual(reroot["failed_re_root_checks"], 0)
        self.assertTrue(reroot["all_shared_cells_agree"])
        self.assertEqual(
            reroot["cells_shared_with_origin_star_by_neighbor_type"],
            {"norm_two_root_edge": 702, "norm_four_orthoplex_opposite": 1},
        )
        adjacency = result["cell_adjacency_audit"]
        self.assertEqual(adjacency["cell_count"], 19440)
        self.assertEqual(adjacency["facet_incidence_count"], 708480)
        self.assertEqual(adjacency["origin_containing_facets"]["multiplicity_counts"], {2: 207360})
        self.assertTrue(adjacency["origin_containing_facets"]["all_paired"])
        self.assertEqual(adjacency["maximum_facets_shared_by_cell_pair"], 1)
        self.assertTrue(adjacency["shared_facet_vertex_sets_equal_cell_common_vertices"])
        self.assertTrue(adjacency["adjacent_cells_occupy_opposite_facet_halfspaces"])
        self.assertTrue(adjacency["facet_adjacent_convex_intersection_is_exactly_shared_facet"])
        self.assertEqual(sum(
            degree * count for degree, count in adjacency["cell_adjacency_degree_distribution"].items()
        ), 2 * adjacency["shared_facet_adjacencies"])


if __name__ == "__main__":
    unittest.main()
