import unittest

from experiments.six_hundred_cell_s3_spectrum import (
    six_hundred_cell_s3_spectrum,
    six_hundred_cell_vertices,
)

class SixHundredCellSpectrumTests(unittest.TestCase):
    def test_vertex_set(self):
        vertices = six_hundred_cell_vertices()
        self.assertEqual(len(vertices), 120)
        self.assertTrue(all(abs(sum(x*x for x in v)-1.0) < 1e-8 for v in vertices))

    def test_first_six_s3_harmonic_eigenspaces(self):
        result = six_hundred_cell_s3_spectrum()
        self.assertEqual(result["vertices"], 120)
        self.assertEqual(result["graph_degree"], 12)
        self.assertEqual(result["matched_harmonic_degrees"], 6)
        self.assertEqual(
            [x["observed_multiplicity"] for x in result["low_degree_harmonic_matches"]],
            [1, 4, 9, 16, 25, 36],
        )

if __name__ == "__main__":
    unittest.main()
