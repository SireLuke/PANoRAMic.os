import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments" / "matter_elements"))
import matter_nodes as MN  # noqa: E402


class MatterNodeCatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cat = MN.build()

    def test_counts_and_ids(self):
        nodes = self.cat["nodes"]
        self.assertEqual(len(nodes), 125)
        self.assertEqual(len({n["id"] for n in nodes}), 125)
        self.assertEqual(sum(n["kind"] == "element" for n in nodes), 118)
        self.assertIn("matter:ion:H3+", {n["id"] for n in nodes})

    def test_molecules_have_no_v8_map(self):
        for n in self.cat["nodes"]:
            if n["kind"] != "element":
                self.assertIsNone(n["v8Mapping"])
                self.assertTrue(all(v is None for v in n["v8"].values()))

    def test_units_are_marked_unverified_and_sources_unverified(self):
        for n in self.cat["nodes"]:
            self.assertTrue(all(not m["unitVerified"] for m in n["measured"]))
        self.assertTrue(all(not s["verified"] for s in self.cat["sources"]))

    def test_only_hydrogen_orbital_view_is_available(self):
        avail = [n["id"] for n in self.cat["nodes"] for v in n["views"] if v["kind"] == "orbitals" and v["status"] == "available"]
        self.assertEqual(avail, ["matter:element:H"])
        self.assertTrue((ROOT / MN.ORBITALS).exists())

    def test_committed_json_matches_regeneration(self):
        self.assertEqual(json.loads(MN.OUT.read_text()), self.cat)

    def test_types_ts_declares_the_exported_fields(self):
        text = (ROOT / "core" / "library" / "types.ts").read_text()
        for name in ("export interface MatterNode", "export interface MatterCatalog", "export type V8State",
                     "export interface V8MappingRef", "export interface GridPlacement"):
            self.assertIn(name, text)
        node = self.cat["nodes"][0]
        for key in node:
            self.assertRegex(text, rf"\b{key}\b")

    @unittest.skipUnless(shutil.which("tsc") and shutil.which("node"), "tsc/node not available")
    def test_typescript_validator_accepts_catalog(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "out"
            build = subprocess.run(["tsc", "--target", "ES2020", "--module", "commonjs", "--skipLibCheck",
                                    "--outDir", str(out), str(ROOT / "tests" / "matter_catalog_check.ts")],
                                   capture_output=True, text=True, cwd=d)
            self.assertEqual(build.returncode, 0, build.stdout + build.stderr)
            js = next(out.rglob("matter_catalog_check.js"))
            run = subprocess.run(["node", str(js), str(MN.OUT)], capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
            self.assertEqual(json.loads(run.stdout)["problems"], [])

    @unittest.skipUnless(shutil.which("tsc") and shutil.which("node"), "tsc/node not available")
    def test_typescript_validator_rejects_bad_catalog(self):
        bad = json.loads(MN.OUT.read_text())
        bad["nodes"][0]["v8"]["chi"] = 2.0                  # out of range
        bad["nodes"][1]["element"]["grid"]["row"] = 1       # reuse H's grid cell? He is (1,18): force col 1
        bad["nodes"][1]["element"]["grid"]["col"] = 1
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "out"
            build = subprocess.run(["tsc", "--target", "ES2020", "--module", "commonjs", "--skipLibCheck",
                                    "--outDir", str(out), str(ROOT / "tests" / "matter_catalog_check.ts")],
                                   capture_output=True, text=True, cwd=d)
            if build.returncode != 0:
                self.skipTest("tsc could not build the check")
            p = Path(d) / "bad.json"
            p.write_text(json.dumps(bad))
            js = next(out.rglob("matter_catalog_check.js"))
            run = subprocess.run(["node", str(js), str(p)], capture_output=True, text=True)
            self.assertEqual(run.returncode, 1)
            problems = json.loads(run.stdout)["problems"]
            self.assertTrue(any("outside" in x for x in problems))
            self.assertTrue(any("reused" in x for x in problems))


if __name__ == "__main__":
    unittest.main()
