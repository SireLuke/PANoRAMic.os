"""Golden-ratio pairing of the eight Coxeter-plane ring radii of the E8 roots.

Observation test, not a theorem. It checks, with the repository's own
Coxeter-plane projection preset, that

* the 240 roots land on 8 distinct radii with 30 points each, and
* the 8 radii split into 4 pairs whose members differ by the factor phi.

It does not prove the 120 + 120 (two nested 600-cell) split of the roots; it
is consistent with it. Standard library only.
"""
import unittest
from math import hypot, sqrt

from core.geometry.e8_root_system import e8_roots_float
from experiments.gosset_sierpinski_experiment import PROJECTION

PHI = (1.0 + sqrt(5.0)) / 2.0
TOL = 1e-8


def ring_radii():
    rings = {}
    for root in e8_roots_float():
        x = sum(p * c for p, c in zip(PROJECTION[0], root))
        y = sum(p * c for p, c in zip(PROJECTION[1], root))
        key = round(hypot(x, y), 9)
        rings[key] = rings.get(key, 0) + 1
    return rings


def phi_pairs(radii):
    """Greedy partition of the sorted radii into (inner, phi * inner) pairs."""
    remaining = sorted(radii)
    pairs = []
    while remaining:
        inner = remaining.pop(0)
        match = next((r for r in remaining if abs(r / inner - PHI) < TOL), None)
        if match is None:
            return None
        remaining.remove(match)
        pairs.append((inner, match))
    return pairs


class CoxeterRingPhiPairingTests(unittest.TestCase):
    def test_eight_rings_of_thirty(self):
        rings = ring_radii()
        self.assertEqual(len(rings), 8)
        self.assertEqual(set(rings.values()), {30})

    def test_radii_split_into_four_phi_pairs(self):
        pairs = phi_pairs(ring_radii())
        self.assertIsNotNone(pairs)
        self.assertEqual(len(pairs), 4)
        for inner, outer in pairs:
            self.assertAlmostEqual(outer / inner, PHI, delta=TOL)


if __name__ == "__main__":
    unittest.main()
