import unittest

from experiments.monster_voa_seed.model import (
    MAX_CLASSES,
    MAX_JSON_BYTES,
    EXPECTED_SECTORS,
    aggregate_census,
    audit_closure,
    audit_corrupted_shell_control,
    audit_exactness,
    audit_permutation_control,
    audit_transition_edges,
    build_audit_summary,
    build_class_table,
    canonical_table_bytes,
    shell_census,
)


class MonsterVOASeedModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.shells = shell_census()
        cls.rows = build_class_table(cls.shells)

    def test_exact_sector_census_matches_both_reference_paths(self):
        result = audit_exactness(self.rows)
        self.assertTrue(result["passed"])
        self.assertEqual(aggregate_census(self.rows), EXPECTED_SECTORS)

    def test_class_budget_and_canonical_serialization(self):
        encoded = canonical_table_bytes(self.rows)
        self.assertLessEqual(len(self.rows), MAX_CLASSES)
        self.assertLessEqual(len(encoded), MAX_JSON_BYTES)

    def test_d1_and_explicit_seed_closure(self):
        result = audit_closure(self.rows)
        self.assertTrue(result["passed"], result["missing_classes"])
        self.assertEqual(result["root_seeds"], 1)
        self.assertEqual(result["shell_seeds"], 4)
        self.assertEqual(result["twisted_ground_seeds"], 1)

    def test_explicit_transition_edge_audit(self):
        result = audit_transition_edges(self.rows)
        self.assertTrue(result["passed"], result["violations"])
        self.assertEqual(result["enumerated_children"], len(self.rows))
        self.assertEqual(result["seed_counts"]["root"], 1)
        self.assertEqual(result["seed_counts"]["d2_leech_shell"], 4)
        self.assertEqual(result["seed_counts"]["d3_twisted_ground"], 1)
        self.assertTrue(all(edge["grade_increment"] == "1" for edge in result["edges"]))
        self.assertTrue(all(edge["sector_transition_valid"] for edge in result["edges"]))
        self.assertTrue(all(edge["parity_valid"] for edge in result["edges"]))

    def test_transition_edge_audit_rejects_missing_parent(self):
        from experiments.monster_voa_seed.model import _parent_untwisted

        child = next(
            row for row in self.rows
            if row.sector == "untwisted" and row.floor == 3 and row.tau
        )
        parent = _parent_untwisted(child)
        reduced = tuple(row for row in self.rows if row != parent)
        result = audit_transition_edges(reduced)
        self.assertFalse(result["passed"])
        self.assertTrue(any(
            item["kind"] == "orphan_edge_parent_not_enumerated"
            for item in result["violations"]
        ))

    def test_corrupted_s2_control_fails_exact_census(self):
        self.assertTrue(audit_corrupted_shell_control(self.shells)["passed"])

    def test_permutation_control_requires_classwise_check(self):
        result = audit_permutation_control(self.rows)
        self.assertTrue(result["aggregate_census_preserved"])
        self.assertTrue(result["classwise_check_rejected"])
        self.assertTrue(result["passed"])

    def test_summary_keeps_diagnostic_status_and_evidence_fence(self):
        result = build_audit_summary()
        self.assertEqual(
            result["status"],
            "SPEC_DIAGNOSTIC_ONLY_NOT_PREREGISTERED_RUN",
        )
        self.assertIn("no VOA states", result["evidence_boundary"])


if __name__ == "__main__":
    unittest.main()
