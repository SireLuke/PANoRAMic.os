"""Focused tests for Valdora's independent NS–ABOM–E8–LEECH–EQBIT-002 runner."""
import unittest

from experiments.ns_abom_e8_leech_eqbit_002_valdora.runner import (
    DEFAULT_NS_RESULTS,
    _build_gosset_graph,
    _e8_abom_comparison,
    _graph_contract,
    _partition_controls,
    _rank_summary,
    load_ns_snapshot,
)


class ValdoraNSABOME8LeechEqbitTests(unittest.TestCase):
    def test_frozen_ns_snapshot_has_nine_finite_cases(self):
        payload = load_ns_snapshot(DEFAULT_NS_RESULTS)
        self.assertEqual(len(payload["cases"]), 9)
        self.assertEqual({case["d"] for case in payload["cases"]}, {2, 3})
        for case in payload["cases"]:
            self.assertLessEqual(
                abs(case["steps"] * case["dt"] - case["T"]),
                max(1e-14, abs(case["T"]) * 1e-12),
            )

    def test_abom_and_exact_e8_root_sets_match_not_just_counts(self):
        result = _e8_abom_comparison()
        self.assertEqual(result["exact_root_count"], 240)
        self.assertEqual(result["abom_adapter_root_count"], 240)
        self.assertTrue(result["all_exact_norm_squared_two"])
        self.assertTrue(result["root_sets_equal"])
        self.assertEqual(result["symmetric_difference_count"], 0)
        self.assertEqual(result["exact_root_set_sha256"], result["abom_root_set_sha256"])

    def test_gosset_graph_has_explicit_e8_bijection_and_antipodal_automorphism(self):
        summary, roots, adjacency, pairs, left, right, anti = _graph_contract()
        self.assertEqual(summary["vertices"], 240)
        self.assertEqual(summary["edges"], 6720)
        self.assertEqual(summary["degree_min"], 56)
        self.assertEqual(summary["degree_max"], 56)
        self.assertEqual(summary["antipodal_pairs"], 120)
        self.assertTrue(summary["e8_root_to_gosset_vertex_bijection"])
        self.assertTrue(summary["antipodal_map_graph_automorphism"])
        self.assertEqual(len(set(anti)), 240)
        self.assertEqual(len(left), 120)
        self.assertEqual(len(right), 120)

    def test_partition_samples_are_reproducible(self):
        _, _, adjacency, pairs, left, right, _ = _graph_contract()
        first = _partition_controls(
            adjacency, pairs, left, right,
            samples_per_seed=3, seed_count=2, seed=12345,
        )
        second = _partition_controls(
            adjacency, pairs, left, right,
            samples_per_seed=3, seed_count=2, seed=12345,
        )
        self.assertEqual(first["raw_transversal_ranks"], second["raw_transversal_ranks"])
        self.assertEqual(first["raw_balanced_ranks"], second["raw_balanced_ranks"])
        self.assertEqual(len(first["raw_transversal_ranks"]), 6)
        self.assertEqual(len(first["raw_balanced_ranks"]), 6)

    def test_plus_one_tail_estimator_never_reports_zero(self):
        result = _rank_summary([118, 119, 120], reference_rank=1)
        self.assertEqual(result["tail_count_rank_le_antipodal"], 0)
        self.assertGreater(result["tail_probability_plus_one"], 0.0)
        self.assertLessEqual(result["tail_probability_plus_one"], 1.0)

    def test_gosset_graph_builder_contract(self):
        roots, adjacency = _build_gosset_graph()
        self.assertEqual(len(roots), 240)
        self.assertEqual(len(adjacency), 240)
        self.assertTrue(all(len(neighbors) == 56 for neighbors in adjacency))


if __name__ == "__main__":
    unittest.main()
