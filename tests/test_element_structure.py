import importlib.util
import re
import sys
import unittest
from pathlib import Path

_p = Path(__file__).resolve().parents[1] / "experiments" / "matter_elements" / "element_structure.py"
_s = importlib.util.spec_from_file_location("element_structure", _p)
ES = importlib.util.module_from_spec(_s)
sys.modules["element_structure"] = ES
_s.loader.exec_module(ES)


class ElementStructureTests(unittest.TestCase):
    def test_symbol_and_name_tables(self):
        self.assertEqual(len(ES.SYMBOLS), 118)
        self.assertEqual(len(ES.NAMES), 118)
        self.assertEqual(len(set(ES.SYMBOLS)), 118)
        self.assertEqual(len(set(ES.NAMES)), 118)
        for s in ES.SYMBOLS:
            self.assertRegex(s, r"^[A-Z][a-z]?$")
        for s, n in zip(ES.SYMBOLS, ES.NAMES):
            self.assertTrue(n[0] == s[0] or s in ("Na", "K", "Fe", "Cu", "Ag", "Sn", "Sb", "W", "Au", "Hg", "Pb"),
                            msg=(s, n))        # symbols from Latin/German names: the known exceptions

    def test_madelung_electron_count_and_noble_gas_closures(self):
        for z in range(1, 119):
            self.assertEqual(sum(e for _, _, e in ES.madelung_config(z)), z)
        for z in ES.NOBLE_Z:
            n, l, e = ES.madelung_config(z)[-1]
            self.assertEqual(e, ES.capacity(l))                  # last subshell exactly full
            self.assertEqual(l, 0 if z == 2 else 1)              # He ends 1s; other noble gases end np6 (l = 1)

    def test_period_lengths_follow_from_subshell_capacities(self):
        self.assertEqual(ES.period_lengths(), [2, 8, 8, 18, 18, 32, 32])
        caps = {l: ES.capacity(l) for l in range(4)}
        self.assertEqual((caps[0], caps[1], caps[2], caps[3]), (2, 6, 10, 14))
        self.assertEqual(2 + 6, 8)
        self.assertEqual(2 + 6 + 10, 18)
        self.assertEqual(2 + 6 + 10 + 14, 32)

    def test_known_configurations_predicted_by_the_rule(self):
        self.assertEqual(ES.config_string(ES.madelung_config(1)), "1s1")
        self.assertEqual(ES.config_string(ES.madelung_config(8)), "1s2 2s2 2p4")
        self.assertEqual(ES.config_string(ES.madelung_config(26)), "1s2 2s2 2p6 3s2 3p6 3d6 4s2")
        # Cr is a known exception: the rule predicts 3d4 4s2, observed is 3d5 4s1
        self.assertEqual(ES.config_string(ES.madelung_config(24)), "1s2 2s2 2p6 3s2 3p6 3d4 4s2")

    def test_blocks_and_periods(self):
        self.assertEqual([ES.block_of(z) for z in (1, 3, 4)], ["s", "s", "s"])
        self.assertEqual({ES.block_of(z) for z in range(5, 11)}, {"p"})
        self.assertEqual(sum(1 for z in range(1, 119) if ES.block_of(z) == "f"), 28)
        self.assertEqual(sum(1 for z in range(1, 119) if ES.block_of(z) == "d"), 40)
        self.assertEqual([ES.period_of(z) for z in (1, 2, 3, 10, 11, 18, 19, 36, 37, 54, 55, 86, 87, 118)],
                         [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7])

    def test_layout_gives_unique_cells_in_groups_1_to_18(self):
        seen = {}
        for z in range(1, 119):
            L = ES.layout(z)
            key = (L["row"], L["col"])
            self.assertNotIn(key, seen, msg=(z, seen.get(key)))
            seen[key] = z
            if L["group"] is not None:
                self.assertTrue(1 <= L["group"] <= 18)
        self.assertEqual(ES.layout(2)["group"], 18)

    def test_validate_table_detects_problems(self):
        good = [{"AtomicNumber": z, "Symbol": ES.SYMBOLS[z - 1], "AtomicMass": str(float(z))} for z in range(1, 119)]
        self.assertEqual(ES.validate_table(good)["errors"], [])
        bad = [dict(r) for r in good]
        bad[5]["Symbol"] = "Xx"
        bad[10]["AtomicMass"] = "-1"
        bad.pop()
        rep = ES.validate_table(bad)
        self.assertGreaterEqual(len(rep["errors"]), 3)
        swapped = [dict(r) for r in good]
        swapped[18]["AtomicMass"] = "17.5"
        self.assertEqual(ES.validate_table(swapped)["mass_order_inversions"], [[18, 19]])

    def test_validation(self):
        for bad in (0, 119, True, "6", 3.0):
            with self.assertRaises(ValueError):
                ES.madelung_config(bad)


if __name__ == "__main__":
    unittest.main()
