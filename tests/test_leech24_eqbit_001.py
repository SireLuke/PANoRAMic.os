from experiments.leech24_eqbit_001.local_shell_audit import gf2_rank_bool
import numpy as np


def test_gf2_rank_known_fixtures():
    assert gf2_rank_bool(np.array([[1, 0], [0, 1]], dtype=bool)) == 2
    assert gf2_rank_bool(np.array([[1, 1], [1, 1]], dtype=bool)) == 1
    assert gf2_rank_bool(np.zeros((3, 5), dtype=bool)) == 0


def test_gf2_rank_row_permutation_invariant():
    matrix = np.array(
        [[1, 0, 1, 1], [0, 1, 1, 0], [1, 1, 0, 1]],
        dtype=bool,
    )
    permutation = [2, 0, 1]
    assert gf2_rank_bool(matrix) == gf2_rank_bool(matrix[permutation])
