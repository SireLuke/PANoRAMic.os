"""Lightweight fixture checks for the exact GAP Monster audit runner."""
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


class MonsterCharacterAuditSourceTests(unittest.TestCase):
    def test_gap_runner_contains_full_orthogonality_checks(self):
        source = (ROOT / "scripts/monster_character_table_audit.g").read_text()
        self.assertIn("ScalarProduct(tbl, irr[i], irr[j])", source)
        self.assertIn("ComplexConjugate(irr[k][j])", source)
        self.assertIn('CharacterTable("M")', source)

    def test_gap_runner_checks_three_mckay_thompson_classes(self):
        source = (ROOT / "scripts/monster_character_table_audit.g").read_text()
        for label in ('"2a"', '"2b"', '"3a"'):
            self.assertIn(label, source)
        self.assertIn("10698752", source)
        self.assertIn("371520", source)

    def test_leech_involution_centralizer_distinction_is_explicit(self):
        source = (ROOT / "scripts/monster_character_table_audit.g").read_text()
        self.assertIn("2 * Size(baby)", source)
        self.assertIn("2^25 * Size(co1)", source)


if __name__ == "__main__":
    unittest.main()
