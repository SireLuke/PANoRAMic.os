import unittest

from experiments.gosset_k8_k4_reconciliation import run_reconciliation


class GossetK8K4ReconciliationTests(unittest.TestCase):
    def test_geometric_simplex_orbit_equals_graph_k8_cliques(self):
        report = run_reconciliation()
        self.assertEqual(report["status"], "PASS")
        simplex = report["simplex_cell_reconciliation"]
        self.assertEqual(simplex["weyl_orbit_simplex_facets"], 17_280)
        self.assertEqual(simplex["independently_enumerated_graph_k8"], 17_280)
        self.assertTrue(simplex["sets_equal"])

    def test_every_global_k4_is_covered_by_exactly_five_simplex_cells(self):
        report = run_reconciliation()
        incidence = report["global_k4_reconciliation"]
        self.assertEqual(incidence["direct_graph_k4"], 241_920)
        self.assertEqual(incidence["k4_covered_by_simplex_cells"], 241_920)
        self.assertTrue(incidence["every_k4_covered"])
        self.assertEqual(incidence["simplex_cells_per_k4"], 5)
        self.assertEqual(incidence["k4_per_vertex"], 4_032)
        self.assertEqual(incidence["k4_per_edge"], 216)

    def test_simplex_cell_vertex_edge_and_k4_incidence_balances(self):
        report = run_reconciliation()
        cells = report["simplex_cell_incidence"]
        self.assertEqual(cells["cells"], 17_280)
        self.assertEqual(cells["cells_per_vertex"], 576)
        self.assertEqual(cells["cells_per_edge"], 72)
        self.assertEqual(cells["k4s_per_cell"], 70)
        self.assertTrue(report["double_counting"]["balanced"])


if __name__ == "__main__":
    unittest.main()
