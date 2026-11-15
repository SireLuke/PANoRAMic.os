import unittest

from experiments.gosset_orthoplex_graph_orbit import (
    build_gosset_graph,
    graph_orthoplex_facets,
    run_reconciliation,
)
from core.geometry.e8_root_system import e8_roots_exact


class GossetOrthoplexGraphOrbitTests(unittest.TestCase):
    def test_exact_graph_to_weyl_orbit_reconciliation(self):
        result = run_reconciliation()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["root_count"], 240)
        self.assertEqual(result["root_graph_degree"], 56)
        self.assertEqual(result["root_graph_edge_count"], 6720)
        self.assertEqual(result["graph_pair_construction"]["orthogonal_pair_nodes"], 15120)
        self.assertEqual(result["graph_facet_count"], 2160)
        self.assertEqual(result["weyl_orbit_facet_count"], 2160)
        self.assertTrue(result["exact_set_equality"])
        self.assertEqual(result["facet_signature"]["induced_graph_edges"], 84)
        self.assertEqual(result["facet_signature"]["induced_graph_non_edges"], 7)

    def test_every_graph_facet_has_exact_matching_complement(self):
        roots = tuple(e8_roots_exact())
        adjacency = build_gosset_graph(roots)
        facets, report = graph_orthoplex_facets(roots, adjacency)
        self.assertEqual(len(facets), 2160)
        self.assertEqual(report["pair_cliques_of_size_7"], 2160)
        for facet in facets:
            self.assertEqual(len(facet), 14)


if __name__ == "__main__":
    unittest.main()
