import unittest

from core.gauge_theory.su2_lattice import (
    SU2Lattice2D,
    qconj,
    qmul,
    qnorm2,
    random_gauge_transform,
    random_lattice,
)


class SU2LatticeGaugeTests(unittest.TestCase):
    def test_quaternion_inverse_and_unit_norm(self):
        lattice = random_lattice(3, 2, seed=7)
        for q in lattice.links.values():
            identity = qmul(q, qconj(q))
            self.assertAlmostEqual(identity[0], 1.0, places=12)
            self.assertAlmostEqual(sum(abs(x) for x in identity[1:]), 0.0, places=12)
            self.assertAlmostEqual(qnorm2(q), 1.0, places=12)

    def test_plaquette_half_trace_is_gauge_invariant(self):
        lattice = random_lattice(3, 3, seed=11)
        gauge = random_gauge_transform(3, 3, seed=19)
        transformed = lattice.gauge_transform(gauge)
        before = [p[0] for p in lattice.plaquettes()]
        after = [p[0] for p in transformed.plaquettes()]
        for a, b in zip(before, after):
            self.assertAlmostEqual(a, b, places=11)

    def test_wilson_action_is_gauge_invariant(self):
        lattice = random_lattice(4, 3, seed=23)
        transformed = lattice.gauge_transform(
            random_gauge_transform(4, 3, seed=29)
        )
        self.assertAlmostEqual(
            lattice.wilson_action(beta=2.4),
            transformed.wilson_action(beta=2.4),
            places=10,
        )

    def test_periodic_plaquette_count(self):
        lattice = random_lattice(2, 3, seed=31)
        self.assertEqual(len(lattice.plaquettes()), 6)

    def test_rejects_non_unit_links_and_gauge_elements(self):
        with self.assertRaises(ValueError):
            SU2Lattice2D(2, 2, {(x, y, mu): (2.0, 0.0, 0.0, 0.0)
                                  for x in range(2) for y in range(2) for mu in (0, 1)})
        lattice = random_lattice(2, 2, seed=37)
        bad = random_gauge_transform(2, 2, seed=41)
        bad[(0, 0)] = (0.0, 0.0, 0.0, 0.0)
        with self.assertRaises(ValueError):
            lattice.gauge_transform(bad)


if __name__ == "__main__":
    unittest.main()
