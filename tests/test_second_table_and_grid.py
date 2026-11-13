import hashlib
import json
import sys
import unittest
from pathlib import Path

_dir = Path(__file__).resolve().parents[1] / "experiments" / "matter_elements"
sys.path.insert(0, str(_dir))
import element_structure as ES          # noqa: E402
import grid_layout as GL                # noqa: E402
import pubchem_elements as PE           # noqa: E402
import second_table as ST               # noqa: E402


class SecondTableTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = ST.load()
        cls.pub = PE.load()

    def test_provenance_matches_file(self):
        prov = json.loads((_dir / "data" / "SecondTable_user_supplied.provenance.json").read_text())
        self.assertEqual(prov["sha256"], hashlib.sha256(ST.DATA.read_bytes()).hexdigest())
        self.assertEqual(prov["rows"], len(self.rows))

    def test_same_elements_as_pubchem(self):
        self.assertEqual([(int(r["AtomicNumber"]), r["Symbol"]) for r in self.rows],
                         [(int(r["AtomicNumber"]), r["Symbol"]) for r in self.pub])

    def test_period_group_valence_agree_with_madelung_layout(self):
        for r in self.rows:
            L = ES.layout(int(r["AtomicNumber"]))
            if L["block"] != "f":
                self.assertEqual(int(r["Period"]), L["period"], r["Symbol"])
            if r["Group"] != "" and L["group"] is not None:
                self.assertEqual(int(r["Group"]), L["group"], r["Symbol"])

    def test_known_label_errors_are_reported(self):
        got = {sym: (have, want) for _, sym, have, want in ST.label_errors(self.rows)}
        self.assertEqual(got["At"], ("Noble Gas", "Halogen"))
        self.assertEqual(got["Rn"], ("Alkali Metal", "Noble Gas"))
        self.assertEqual(got["Fr"], ("Alkaline Earth Metal", "Alkali Metal"))
        self.assertEqual(got["Ra"], ("Actinide", "Alkaline Earth Metal"))

    def test_shared_properties_track_pubchem(self):
        import numpy as np
        for ka, kb in (("Density", "Density"), ("IonizationEnergy", "IonizationEnergy"), ("MeltingPoint", "MeltingPoint")):
            xs, ys = [], []
            for a, b in zip(self.rows, self.pub):
                if a[ka] != "" and b[kb] != "":
                    xs.append(float(a[ka])); ys.append(float(b[kb]))
            ra, rb = np.argsort(np.argsort(xs)), np.argsort(np.argsort(ys))
            self.assertGreater(np.corrcoef(ra, rb)[0, 1], 0.99, ka)

    def test_preregistered_replication(self):
        res = ST.run(self.rows, permutations=1000)
        self.assertEqual(res["six"]["complete_cases"], 80)
        self.assertAlmostEqual(res["six"]["A"], 0.7417, places=3)
        self.assertAlmostEqual(res["six"]["C"], 0.5429, places=3)
        self.assertTrue(res["six"]["passes"])
        self.assertTrue(res["v8"]["primary"]["passes"])
        self.assertTrue(res["v8"]["secondary"]["passes"])


class GridTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = PE.load()

    def test_118_unique_cells_in_expected_rows(self):
        cells = GL.cells()
        self.assertEqual(len(set(cells.values())), 118)
        self.assertEqual(cells[1], (1, 1))
        self.assertEqual(cells[2], (1, 18))
        self.assertEqual({r for r, _ in cells.values()}, set(range(1, 10)))
        self.assertEqual(cells[57], (8, 3))      # La starts the first f-row
        self.assertEqual(cells[89], (9, 3))      # Ac starts the second f-row

    def test_records_carry_v8_states(self):
        recs = GL.records(self.rows)
        self.assertEqual(len(recs), 118)
        for r in recs:
            self.assertIsNone(r["V8"]["tau"])
            self.assertIsNone(r["V8"]["f"])

    def test_preregistered_neighbour_test(self):
        res = GL.run(self.rows, permutations=500)
        self.assertEqual(res["n"], 96)
        self.assertEqual(res["G"], 1.0)
        self.assertTrue(res["passes"])
        self.assertGreater(res["null_median"], 4.0)

    def test_export_roundtrip(self):
        import tempfile
        recs = GL.records(self.rows)
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "g.json"
            GL.export(recs, p)
            self.assertEqual(len(json.loads(p.read_text())["elements"]), 118)

    def test_committed_json_matches_regeneration(self):
        committed = json.loads((_dir / "grid_elements.json").read_text())
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "g.json"
            GL.export(GL.records(self.rows), p)
            self.assertEqual(committed, json.loads(p.read_text()))


if __name__ == "__main__":
    unittest.main()
