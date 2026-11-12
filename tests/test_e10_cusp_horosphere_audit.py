import unittest

from experiments.e10_cusp_horosphere_audit import run_horosphere_audit


class E10CuspHorosphereAuditTests(unittest.TestCase):
    def test_ideal_vertex_horosphere_section_is_euclidean_8_simplex(self):
        result = run_horosphere_audit()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["ambient_signature"], (9, 1))
        self.assertEqual(result["ideal_vertex_node"], 6)
        self.assertLess(abs(result["ideal_ray_null_norm"]), 1e-10)
        self.assertEqual(result["finite_vertices_intersected"], 9)
        self.assertLess(result["max_intersection_residual"], 1e-8)
        self.assertEqual(result["horosphere_section_affine_rank"], 8)
        self.assertEqual(result["horosphere_section_dimension"], 8)
        self.assertGreater(
            result["minimum_pairwise_euclidean_distance_squared"], 0
        )

    def test_cusp_simplex_metric_matches_affine_e8_coxeter_angles(self):
        result = run_horosphere_audit()["cusp_simplex_metric_audit"]
        self.assertEqual(result["dihedral_pair_count"], 36)
        self.assertEqual(result["edge_pair_count"], 36)
        self.assertEqual(result["dihedral_angle_counts"], {"pi/3": 8, "pi/2": 28})
        self.assertEqual(result["coxeter_adjacency_edges"], 8)
        self.assertTrue(result["all_angles_match_affine_E8_link"])
        self.assertEqual(len(result["squared_edge_lengths"]), 36)


if __name__ == "__main__":
    unittest.main()
