import hashlib
import json
import sys
import unittest
from pathlib import Path

_dir = Path(__file__).resolve().parents[1] / "experiments" / "matter_molecules"
sys.path.insert(0, str(_dir))
import molecule_starter as MS           # noqa: E402


class MoleculeStarterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mols = MS.load_molecules()
        cls.by_formula = {m["formula"]: m for m in cls.mols}

    def test_seven_molecules_including_h3_cation(self):
        self.assertEqual(len(self.mols), 7)
        h3 = self.by_formula["H3"]
        self.assertEqual(h3["charge"], 1)
        self.assertEqual(h3["bond_angle_deg"], 60.0)
        self.assertIsNone(h3["smiles"])

    def test_smiles_atom_counts_match_formulas(self):
        for m in self.mols:
            if m["smiles"] is None:
                continue
            self.assertEqual(MS.smiles_counts(m["smiles"]), MS.formula_counts(m["formula"]), m["name"])

    def test_geometry_sanity(self):
        g = self.by_formula
        self.assertAlmostEqual(g["CH4"]["bond_angle_deg"], 109.47, delta=0.1)     # tetrahedral
        self.assertEqual(g["CO2"]["bond_angle_deg"], 180.0)
        self.assertTrue(104.0 <= g["H2O"]["bond_angle_deg"] <= 105.0)
        self.assertTrue(g["NH3"]["bond_angle_deg"] < 109.47)                        # lone-pair compression
        self.assertIsNone(g["HCl"]["bond_angle_deg"])                               # diatomic
        for m in self.mols:
            self.assertTrue(0.7 < m["bond_length_A"] < 1.5, m["name"])

    def test_provenance_notes_missing_sections_and_hash(self):
        prov = json.loads((_dir / "data" / "molecules_starter.json").read_text())["provenance"]
        self.assertIn("0617191ac8e12eb0913a5d0c293a85a41774de6d29b585569d00b267760ed556", prov["supplied_by_user"])
        self.assertIn("neither", prov["note"])

    def test_ea_allen_table_and_known_conflict(self):
        rows = MS.load_ea_allen()
        self.assertEqual(len(rows), 10)
        conflicts = MS.allen_conflicts(rows)
        self.assertEqual(conflicts, [("Cl", 3.481, 2.869)])                         # reported, not corrected
        by = {r["Symbol"]: r for r in rows}
        for s in ("He", "Ne", "Ar", "N"):
            self.assertLess(by[s]["EA"], 0.0)                                       # unbound anions
        for s in ("H", "Li", "C", "O", "F", "Cl"):
            self.assertGreater(by[s]["EA"], 0.0)

    def test_allen_noble_gas_exceeds_preceding_halogen_in_reference(self):
        ref = MS.ALLEN_REFERENCE
        self.assertGreater(ref["Ne"], ref["F"])
        self.assertGreater(ref["Ar"], ref["Cl"])
        self.assertGreater(ref["Kr"], ref["Br"])
        self.assertGreater(ref["Xe"], ref["I"])


if __name__ == "__main__":
    unittest.main()
