"""Contract tests for NS–ABOM–E8–LEECH–EQBIT-001 composition."""
import json
from pathlib import Path
import tempfile
import unittest
from experiments.ns_abom_e8_leech_eqbit_001.integration import DEFAULT_NS_RESULTS, load_ns_snapshot


class IntegrationSnapshotTests(unittest.TestCase):
    def test_frozen_ns_snapshot_has_nine_cases_and_2d_3d_domains(self):
        payload = load_ns_snapshot(DEFAULT_NS_RESULTS)
        self.assertEqual(len(payload["cases"]), 9)
        self.assertEqual({case["d"] for case in payload["cases"]}, {2, 3})

    def test_snapshot_rejects_mismatched_final_time(self):
        payload = json.loads(DEFAULT_NS_RESULTS.read_text(encoding="utf-8"))
        payload["cases"][0]["steps"] += 1
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "final time"):
                load_ns_snapshot(path)

    def test_snapshot_rejects_missing_diagnostic(self):
        payload = json.loads(DEFAULT_NS_RESULTS.read_text(encoding="utf-8"))
        del payload["cases"][0]["ET"]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "missing required diagnostics"):
                load_ns_snapshot(path)


if __name__ == "__main__":
    unittest.main()
