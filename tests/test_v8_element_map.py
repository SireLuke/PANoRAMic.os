import copy
import math
import sys
import unittest
from pathlib import Path

_dir = Path(__file__).resolve().parents[1] / "experiments" / "matter_elements"
sys.path.insert(0, str(_dir))
import element_structure as ES          # noqa: E402
import pubchem_elements as PE           # noqa: E402
import v8_element_map as M              # noqa: E402


class V8ElementMapTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = PE.load()
        cls.states = M.build_states(cls.rows)

    def test_structural_channels_are_exact(self):
        for z in range(1, 119):
            s = M.structural(z)
            self.assertAlmostEqual(s["R"], (ES.period_of(z) - 1) / 6.0)
            self.assertTrue(0.0 < s["h"] <= 1.0 and 0.0 < s["u"] <= 1.0)
            self.assertEqual(s["h"] == 1.0, z in ES.NOBLE_Z)

    def test_phase_wraps_at_every_noble_gas(self):
        for z in ES.NOBLE_Z:
            self.assertAlmostEqual(M.phase_angle(z), 2.0 * math.pi)
        self.assertLess(M.phase_angle(3), M.phase_angle(10))      # rises across period 2

    def test_period_lengths_recovered_from_h(self):
        firsts = [1, 3, 11, 19, 37, 55, 87]                       # first element of each period
        lengths = [round(1.0 / M.structural(z)["h"]) for z in firsts]
        self.assertEqual(lengths, ES.period_lengths())            # h of the first element is 1/length

    def test_convention_ranges_and_unassigned_channels(self):
        for st in self.states:
            v = st["V8"]
            self.assertEqual(set(v), set(M.COORDS))
            self.assertIsNone(v["tau"])
            self.assertIsNone(v["f"])
            for k in ("h", "R", "u", "d", "s", "chi"):
                if v[k] is not None:
                    self.assertTrue(0.0 <= v[k] <= 1.0, (st["Symbol"], k, v[k]))
            self.assertIn("not a derived physical identity", st["mapping_kind"])

    def test_missing_source_gives_none_not_zero(self):
        he = self.states[1]["V8"]
        self.assertEqual(self.rows[1]["Symbol"], "He")
        self.assertIsNone(he["chi"])                  # He has no electronegativity in the table
        self.assertIsNotNone(he["d"])

    def test_measured_channels_ignore_configuration(self):
        rows2 = copy.deepcopy(self.rows)
        for r in rows2:
            r["ElectronConfiguration"] = "1s1"
        for a, b in zip(self.states, M.build_states(rows2)):
            for k in ("chi", "s", "d"):
                self.assertEqual(a["V8"][k], b["V8"][k])

    def test_preregistered_primary_result(self):
        res = M.run(self.rows, permutations=1000)
        p = res["primary"]
        self.assertEqual(p["complete_cases"], 88)
        self.assertAlmostEqual(p["A"], 0.6742, places=3)
        self.assertAlmostEqual(p["C"], 0.4211, places=3)
        self.assertTrue(p["passes"])
        self.assertTrue(res["secondary"]["A"] > res["secondary"]["A_null_p99"])


if __name__ == "__main__":
    unittest.main()
