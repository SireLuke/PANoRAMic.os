import unittest
from experiments.menger_gosset.cut_rank_audit import (
    adjacency, cut_rank, gf2_rank, menger_cells, run,
)


class MengerSpatialCutRankTests(unittest.TestCase):
    def test_gf2_rank(self):
        self.assertEqual(gf2_rank([0, 0]), 0)
        self.assertEqual(gf2_rank([1, 2, 3]), 2)

    def test_level_one_geometry(self):
        cells = menger_cells(1)
        self.assertEqual(len(cells), 20)
        graph = adjacency(cells, 3)
        self.assertEqual(sum(map(len, graph)) // 2, 24)
        self.assertEqual(sorted(map(len, graph)).count(2), 12)
        self.assertEqual(sorted(map(len, graph)).count(3), 8)

    def test_seeded_run_is_reproducible(self):
        a = run(levels=(1, 2), samples=12, seed=1234)
        b = run(levels=(1, 2), samples=12, seed=1234)
        self.assertEqual(a, b)
        self.assertEqual([x["vertices"] for x in a["results"]], [20, 400])
        self.assertEqual([x["spatial_partition"]["cut_rank_gf2"] for x in a["results"]], [4, 16])

    def test_rejects_bad_level(self):
        with self.assertRaises(ValueError):
            menger_cells(0)


if __name__ == "__main__":
    unittest.main()
