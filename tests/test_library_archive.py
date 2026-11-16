import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS_OK = bool(shutil.which("tsc") and shutil.which("node"))


def compile_ts(source: Path, out: Path) -> Path:
    # Run from a temp dir so an installed tsc does not pick up the repo tsconfig.json.
    build = subprocess.run(
        ["tsc", "--target", "ES2020", "--module", "commonjs", "--strict", "--skipLibCheck",
         "--outDir", str(out), str(source)],
        capture_output=True, text=True, cwd=out.parent,
    )
    if build.returncode != 0:
        raise AssertionError(build.stdout + build.stderr)
    return next(out.rglob(source.stem + ".js"))


class ArchiveSourceTests(unittest.TestCase):
    def test_module_layout_and_exports(self):
        index = (ROOT / "core" / "library" / "archive" / "index.ts").read_text()
        for name in ("KiwixServeSource", "findInArchive", "promoteToNode", "archiveRoutes", "htmlToText"):
            self.assertIn(name, index)
        self.assertIn('export * from "./archive";', (ROOT / "core" / "library" / "index.ts").read_text())

    def test_source_has_no_telemetry_or_disk_writes(self):
        for path in (ROOT / "core" / "library" / "archive").glob("*.ts"):
            text = path.read_text()
            for banned in ("writeFile", "appendFile", "localStorage", "sendBeacon", "XMLHttpRequest", "WebSocket"):
                self.assertNotIn(banned, text, f"{banned} in {path.name}")

    @unittest.skipUnless(TOOLS_OK, "tsc/node not available")
    def test_behaviour_against_fake_kiwix_serve(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "out"
            js = compile_ts(ROOT / "tests" / "library_archive_check.ts", out)
            run = subprocess.run(["node", str(js)], capture_output=True, text=True, timeout=120)
            self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
            result = json.loads(run.stdout.strip().splitlines()[-1])
            self.assertEqual(result["failures"], [])
            self.assertGreaterEqual(result["passed"], 16)

    @unittest.skipUnless(TOOLS_OK, "tsc/node not available")
    def test_smoke_script_compiles_and_fails_cleanly_without_a_server(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "out"
            js = compile_ts(ROOT / "tools" / "kiwix_smoke.ts", out)
            run = subprocess.run(["node", str(js), "http://127.0.0.1:1"], capture_output=True, text=True, timeout=60)
            self.assertNotEqual(run.returncode, 0)
            self.assertIn("FAIL  list books", run.stdout)
            self.assertNotIn("Traceback", run.stderr)

    @unittest.skipUnless(TOOLS_OK, "tsc/node not available")
    def test_smoke_script_refuses_a_remote_host(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "out"
            js = compile_ts(ROOT / "tools" / "kiwix_smoke.ts", out)
            run = subprocess.run(["node", str(js), "http://example.com"], capture_output=True, text=True, timeout=60)
            self.assertNotEqual(run.returncode, 0)
            self.assertIn("refusing a non-loopback host", run.stdout)
            self.assertEqual(run.stderr.strip(), "")


if __name__ == "__main__":
    unittest.main()
