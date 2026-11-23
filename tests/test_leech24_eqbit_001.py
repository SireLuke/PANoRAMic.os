import unittest

import numpy as np

from experiments.leech24_eqbit_001.local_shell_audit import gf2_rank_bool


class TestGF2RankFixtures(unittest.TestCase):
    def test_known_fixtures(self):
        self.assertEqual(gf2_rank_bool(np.array([[1, 0], [0, 1]], dtype=bool)), 2)
        self.assertEqual(gf2_rank_bool(np.array([[1, 1], [1, 1]], dtype=bool)), 1)
        self.assertEqual(gf2_rank_bool(np.zeros((3, 5), dtype=bool)), 0)

    def test_row_permutation_invariant(self):
        matrix = np.array(
            [[1, 0, 1, 1], [0, 1, 1, 0], [1, 1, 0, 1]],
            dtype=bool,
        )
        permutation = [2, 0, 1]
        self.assertEqual(gf2_rank_bool(matrix), gf2_rank_bool(matrix[permutation]))


if __name__ == "__main__":
    unittest.main()
