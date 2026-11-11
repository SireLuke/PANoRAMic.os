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


if __name__ == "__main__":
    unittest.main()
