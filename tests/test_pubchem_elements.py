import importlib.util
import json
import sys
import unittest
from pathlib import Path

_dir = Path(__file__).resolve().parents[1] / "experiments" / "matter_elements"
sys.path.insert(0, str(_dir))
import element_structure as ES          # noqa: E402
import pubchem_elements as PE           # noqa: E402
import similarity_layout as SL          # noqa: E402

EXCEPTIONS = {24: "Cr", 29: "Cu", 41: "Nb", 42: "Mo", 44: "Ru", 45: "Rh", 46: "Pd", 47: "Ag", 57: "La", 58: "Ce",
              64: "Gd", 78: "Pt", 79: "Au", 89: "Ac", 90: "Th", 91: "Pa", 92: "U", 93: "Np", 96: "Cm"}


class PubChemElementsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = PE.load()

    def test_provenance_matches_file(self):
        prov = json.loads((_dir / "data" / "PubChemElements_all.provenance.json").read_text())
        self.assertEqual(prov["sha256"], PE.sha256())
        self.assertEqual(prov["rows"], len(self.rows))

    def test_validator_finds_no_errors(self):
        rep = ES.validate_table(self.rows)
        self.assertEqual(rep["errors"], [])
        self.assertEqual(rep["rows"], 118)
        for pair in ([18, 19], [27, 28], [52, 53]):           # Ar/K, Co/Ni, Te/I
            self.assertIn(pair, rep["mass_order_inversions"])

    def test_every_observed_configuration_sums_to_z(self):
        self.assertEqual(PE.configs_with_wrong_electron_count(self.rows), [])

    def test_exactly_nineteen_departures_from_the_filling_rule(self):
        got = {z: s for z, s, _, _ in PE.config_differences(self.rows)}
        self.assertEqual(got, EXCEPTIONS)

    def test_known_exception_details(self):
        d = {s: delta for _, s, _, delta in PE.config_differences(self.rows)}
        self.assertEqual(d["Cr"], {"3d": (4, 5), "4s": (2, 1)})
        self.assertEqual(d["Pd"], {"4d": (8, 10), "5s": (2, 0)})

    def test_lu_lr_group_block_conflicts_are_the_only_ones(self):
        self.assertEqual([c[:2] for c in PE.group_block_conflicts(self.rows)], [(71, "Lu"), (103, "Lr")])

    def test_parse_config_rejects_garbage(self):
        with self.assertRaises(ValueError):
            PE.parse_config("[He]2x1")

    def test_similarity_recovers_block_and_group_structure(self):
        res = SL.run(self.rows, permutations=500)
        self.assertEqual(res["complete_cases"], 85)
        self.assertAlmostEqual(res["A"], 0.6902, places=3)
        self.assertEqual(res["C_n"], 37)
        self.assertGreater(res["A"], res["A_null_p99"])
        self.assertGreater(res["C"], res["C_null_p99"])
        self.assertTrue(res["passes"])

    def test_similarity_excludes_z_and_configuration_by_construction(self):
        self.assertNotIn("AtomicMass", SL.FEATURES)
        self.assertNotIn("ElectronConfiguration", SL.FEATURES)
        self.assertNotIn("AtomicNumber", SL.FEATURES)


if __name__ == "__main__":
    unittest.main()
