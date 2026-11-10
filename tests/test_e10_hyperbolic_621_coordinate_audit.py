import unittest
from experiments.e10_hyperbolic_621_coordinate_audit import run_audit

class E10HyperbolicCoordinateAuditTests(unittest.TestCase):
    def test_exact_lorentzian_coordinates_and_ideal_link(self):
        result=run_audit()
        self.assertEqual(result["status"],"PASS")
        self.assertEqual(result["gram_signature"],(9,1,0))
        self.assertEqual(result["gram_determinant"],"-1/1024")
        self.assertEqual(result["finite_vertex_count"],9)
        self.assertEqual(result["ideal_vertex_count"],1)
        self.assertEqual(result["ideal_vertex_node"],6)
        self.assertEqual(result["dual_vertex_norms"][6],"0")
        self.assertTrue(result["all_vertex_rays_same_time_cone"])
        self.assertEqual(result["lorentz_reflections"],10)
        self.assertEqual(result["reflection_metric_preservation_checks"],10)
        self.assertEqual(result["coxeter_relations"]["total"],55)
        self.assertEqual(result["ideal_link"]["principal_minor_counts"],{"positive":510,"zero":1})
        self.assertEqual(result["ideal_link"]["primitive_null_root_marks"],["6","5","4","3","2","1","4","2","3"])

if __name__=="__main__":unittest.main()
