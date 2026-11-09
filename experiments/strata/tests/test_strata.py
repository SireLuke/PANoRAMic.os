import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from e8_adapter import build_roots, adjacency_summary
from strata_core import DimensionResult, StrataReport, retention, permutation_control

class StrataTests(unittest.TestCase):
    def test_e8_root_count_and_norm(self):
        roots = build_roots()
        self.assertEqual(len(roots), 240)
        self.assertTrue(all(sum(x*x for x in r) == 2 for r in roots))

    def test_e8_adjacency_regular(self):
        result = adjacency_summary()
        self.assertEqual(result["edges_inner_product_1"], 6720)
        self.assertTrue(result["regular_degree_56"])

    def test_retention(self):
        self.assertEqual(retention({"a", "b"}, {"a", "b", "c"}), 2/3)
        self.assertEqual(retention(set(), set()), 1.0)

    def test_seeded_control_is_reproducible(self):
        x = [0, 0, 1, 1, 0, 1]
        self.assertEqual(permutation_control(x, 42), permutation_control(x, 42))
        self.assertCountEqual(x, permutation_control(x, 42))

    def test_report_rejects_duplicate_dimensions(self):
        report = StrataReport("x", "h", "test", 1,
            [DimensionResult("scale", "pass", ""), DimensionResult("scale", "fail", "")], [])
        with self.assertRaises(ValueError):
            report.to_dict()

if __name__ == "__main__":
    unittest.main()
