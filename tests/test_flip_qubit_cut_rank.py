import unittest
from experiments.flip_qubit.cut_rank_audit import (
    canonical_antipodal_partition, cut_rank, e8_roots_scaled,
    gf2_rank, gosset_adjacency, run,
)


class FlipEqbitCutRankTests(unittest.TestCase):
    def test_gf2_rank_known_matrices(self):
        self.assertEqual(gf2_rank([0, 0, 0]), 0)
        self.assertEqual(gf2_rank([0b001, 0b010, 0b011]), 2)
        self.assertEqual(gf2_rank([0b101, 0b010, 0b100]), 3)

    def test_e8_gosset_contract_and_antipodal_cut(self):
        roots = e8_roots_scaled()
        self.assertEqual(len(roots), 240)
        adj = gosset_adjacency(roots)
        self.assertEqual({len(row) for row in adj}, {56})
        self.assertEqual(sum(map(len, adj)) // 2, 6720)
        left, right, pairs = canonical_antipodal_partition(roots)
        self.assertEqual(len(pairs), 120)
        self.assertEqual(len(set(left) & set(right)), 0)
        self.assertEqual(cut_rank(adj, left, right), 112)

    def test_seeded_audit_is_reproducible_and_has_two_controls(self):
        a = run(samples=8, seed=20261121)
        b = run(samples=8, seed=20261121)
        self.assertEqual(a, b)
        self.assertEqual(a["antipodal_cut"]["rank_gf2"], 112)
        self.assertEqual(a["random_transversal_cuts"]["n"], 8)
        self.assertEqual(a["random_balanced_cuts"]["n"], 8)


if __name__ == "__main__":
    unittest.main()
