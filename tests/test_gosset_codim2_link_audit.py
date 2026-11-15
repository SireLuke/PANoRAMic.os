import unittest

from experiments.gosset_codim2_link_audit import run_link_audit


class GossetCodimensionTwoLinkAuditTests(unittest.TestCase):
    def test_all_origin_codimension_two_links_are_single_cycles(self):
        result = run_link_audit()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["root_count"], 240)
        self.assertEqual(result["simplex_cells"], 17280)
        self.assertEqual(result["graph_derived_orthoplex_cells"], 2160)
        self.assertEqual(result["total_cells"], 19440)
        audit = result["link_audit"]
        self.assertTrue(audit["all_links_are_single_connected_cycles"])
        self.assertTrue(audit["all_link_vertices_have_degree_two"])
        self.assertTrue(audit["no_parallel_link_edges"])
        self.assertEqual(audit["max_link_vertex_degree"], 2)
        self.assertEqual(audit["facet_cell_owner_multiplicity"], {2: 207360})


if __name__ == "__main__":
    unittest.main()
