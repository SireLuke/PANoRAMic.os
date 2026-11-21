import hashlib
import unittest
from experiments.menger_seed.propagation import (
    PropagationBudget, PropagationLimitExceeded, menger_cells, propagate_seed,
)


class MengerSeedPropagationTests(unittest.TestCase):
    def test_menger_cell_counts_and_reference_inheritance(self):
        base = b"PAN shared base memory: immutable seed payload"
        for level, expected in ((1, 20), (2, 400)):
            cells = menger_cells(level)
            result = propagate_seed(cells, base)
            self.assertEqual(len(cells), expected)
            self.assertEqual(result["node_count"], expected)
            self.assertTrue(result["base_memory_unchanged"])
            self.assertEqual(result["base_digest"], hashlib.sha256(base).hexdigest())
            self.assertTrue(all(n.base_digest == result["base_digest"] for n in result["nodes"].values()))
            self.assertLessEqual(result["reference_storage_bytes"], result["naive_copy_bytes"])

    def test_base_is_not_replaced_by_child_delta(self):
        base = b"original canonical context"
        result = propagate_seed(menger_cells(1), base,
                                delta_factory=lambda cell, depth: f"{cell}:{depth}".encode())
        self.assertEqual(result["base_digest"], hashlib.sha256(base).hexdigest())
        self.assertGreater(result["delta_bytes"], 0)
        self.assertTrue(result["base_memory_unchanged"])

    def test_node_and_byte_budgets_fail_closed(self):
        cells = menger_cells(1)
        with self.assertRaises(PropagationLimitExceeded):
            propagate_seed(cells, b"base", budget=PropagationBudget(max_nodes=10))
        with self.assertRaises(PropagationLimitExceeded):
            propagate_seed(cells, b"base", budget=PropagationBudget(max_delta_bytes=3),
                           delta_factory=lambda cell, depth: b"1234")

    def test_invalid_seed_and_delta_contract(self):
        with self.assertRaises(ValueError):
            propagate_seed(menger_cells(1), b"")
        with self.assertRaises(TypeError):
            propagate_seed(menger_cells(1), b"base",
                           delta_factory=lambda cell, depth: "not bytes")


if __name__ == "__main__":
    unittest.main()
