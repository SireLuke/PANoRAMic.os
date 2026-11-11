import unittest

from experiments.e8_spherical_shell_audit import (
    e8_lattice_shell,
    e8_root_graph_spectral_audit,
    harmonic_dimension_s7,
    polynomial_restriction_dimension_s7,
    spherical_moment_audit,
)

class E8ShellConstructionTests(unittest.TestCase):
    def test_first_three_shell_counts_and_norms(self):
        expected = {1: 240, 2: 2160, 3: 6720}
        for n, count in expected.items():
            shell = e8_lattice_shell(n)
            self.assertEqual(len(shell), count)
            self.assertTrue(all(sum(x*x for x in v) == 8*n for v in shell))

    def test_shells_are_centrally_symmetric(self):
        for n in (1, 2, 3):
            shell = set(e8_lattice_shell(n))
            self.assertTrue(all(tuple(-x for x in v) in shell for v in shell))

class E8SphericalMomentTests(unittest.TestCase):
    def test_all_three_shells_match_sphere_through_degree_seven(self):
        for n in (1, 2, 3):
            result = spherical_moment_audit(n, 6)
            self.assertTrue(result["centrally_symmetric"])
            self.assertTrue(result["odd_moments_zero_through_degree_7"])
            for degree in ("2", "4", "6"):
                self.assertEqual(result["even_moment_checks"][degree]["mismatches"], 0)

    def test_degree_eight_detects_nonuniform_eighth_moment(self):
        for n in (1, 2, 3):
            result = spherical_moment_audit(n, 8)
            self.assertEqual(result["even_moment_checks"]["8"]["even_monomials_checked"], 330)
            self.assertGreater(result["even_moment_checks"]["8"]["mismatches"], 0)

class E8HarmonicDimensionTests(unittest.TestCase):
    def test_s7_harmonic_and_polynomial_dimensions(self):
        self.assertEqual([harmonic_dimension_s7(k) for k in range(5)],
                         [1, 8, 35, 112, 294])
        self.assertEqual([polynomial_restriction_dimension_s7(k) for k in range(5)],
                         [1, 9, 44, 156, 450])

    def test_root_graph_spectrum_matches_harmonic_predictions(self):
        result = e8_root_graph_spectral_audit()
        self.assertEqual(
            [(x["eigenvalue"], x["multiplicity"]) for x in result["laplacian_spectrum"]],
            [(0, 1), (28, 8), (48, 35), (58, 112), (60, 84)],
        )
        self.assertEqual(
            [x["observed_laplacian_eigenvalue"] for x in result["gegenbauer_comparison"]],
            [0, 28, 48, 58, 60],
        )
        self.assertEqual(result["gegenbauer_comparison"][4]["observed_multiplicity"], 84)

if __name__ == "__main__":
    unittest.main()
