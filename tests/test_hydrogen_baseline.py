"""Tests for the QWAVE hydrogen stationary-state baseline."""
import cmath
import math
import unittest

from core.abom_v8 import hydrogen_baseline as H

STATES = [(1, 0), (2, 0), (2, 1), (3, 0), (3, 1), (3, 2), (4, 2)]


class HydrogenBaselineTests(unittest.TestCase):
    def test_radial_normalisation(self):
        steps, rmax = 200_000, 250.0
        dr = rmax / steps
        for n, l in STATES:
            total = sum(H.radial(n, l, (i + 0.5) * dr) ** 2 * ((i + 0.5) * dr) ** 2 for i in range(steps)) * dr
            self.assertAlmostEqual(total, 1.0, places=7, msg=(n, l))

    def test_radial_nodes_count_and_values(self):
        for n, l in STATES:
            nodes = H.radial_nodes(n, l)
            self.assertEqual(len(nodes), n - l - 1)
            for r0 in nodes:
                self.assertAlmostEqual(H.radial(n, l, r0), 0.0, places=12)
        self.assertEqual(H.radial_nodes(4, 2), (12.0,))

    def test_harmonics_are_orthonormal(self):
        nt, npd = 400, 8
        labels = [(l, m) for l in range(3) for m in range(-l, l + 1)]
        def inner(a, b):
            s = 0j
            for i in range(nt):
                th = (i + 0.5) * math.pi / nt
                for j in range(npd):
                    ph = 2 * math.pi * (j + 0.5) / npd
                    s += (H.spherical_harmonic(*a, th, ph).conjugate() * H.spherical_harmonic(*b, th, ph)
                          * math.sin(th))
            return s * (math.pi / nt) * (2 * math.pi / npd)
        for a in labels:
            for b in labels:
                self.assertAlmostEqual(inner(a, b).real, 1.0 if a == b else 0.0, places=3, msg=(a, b))

    def test_conical_node_angle(self):
        theta = math.acos(1 / math.sqrt(3))
        self.assertAlmostEqual(abs(H.spherical_harmonic(2, 0, theta, 0.0)), 0.0, places=14)
        self.assertAlmostEqual(math.degrees(theta), 54.7356103172, places=8)

    def test_stationary_state_time_phase(self):
        z0 = H.psi(2, 1, 1, 3.0, 1.0, 0.4, 0.0)
        z1 = H.psi(2, 1, 1, 3.0, 1.0, 0.4, 5.0)
        self.assertAlmostEqual(abs(z0), abs(z1), places=14)             # density is time independent
        self.assertAlmostEqual(cmath.phase(z1 / z0), -H.energy_hartree(2) * 5.0, places=12)

    def test_azimuthal_current_matches_numerical_gradient(self):
        n, l, m, r, th, ph, h = 3, 2, 1, 4.0, 0.9, 0.7, 1e-6
        z = H.psi(n, l, m, r, th, ph)
        dz = (H.psi(n, l, m, r, th, ph + h) - H.psi(n, l, m, r, th, ph - h)) / (2 * h)
        j_numeric = (z.conjugate() * dz).imag / (r * math.sin(th))     # Im(psi* grad psi) . phi_hat
        self.assertAlmostEqual(H.fields(n, l, m, r, th, ph)["j_phi"], j_numeric, places=9)
        self.assertEqual(H.fields(3, 2, 0, r, th, ph)["j_phi"], 0.0)   # m = 0 carries no azimuthal flow

    def test_fields_are_distinct_and_consistent(self):
        f = H.fields(2, 1, -1, 2.5, 1.1, 0.3, 1.0)
        self.assertAlmostEqual(f["amplitude"] ** 2, f["density"], places=14)
        self.assertAlmostEqual(abs(f["psi"]), f["amplitude"], places=14)
        self.assertLess(f["j_phi"], 0.0)                               # m < 0 circulates the other way

    def test_halpha_agrees_with_rydberg_and_qwave_relations(self):
        self.assertAlmostEqual(H.halpha_rydberg_wavelength_m() * 1e9, 656.47, places=2)
        # hartree-based Bohr levels use the infinite-mass Rydberg: ~656.11 nm; differs from R_H by the mass ratio
        self.assertAlmostEqual(H.halpha_wavelength_m() * 1e9, 656.11, places=1)
        ratio = H.halpha_rydberg_wavelength_m() / H.halpha_wavelength_m()
        self.assertAlmostEqual(ratio, 1.000545, places=4)

    def test_validation(self):
        for call in (lambda: H.radial(5, 0, 1.0), lambda: H.radial(2, 0, -1.0), lambda: H.radial(2, 0, float("nan")),
                     lambda: H.psi(2, 1, 2, 1.0, 1.0, 0.0), lambda: H.psi(1, 0, 0, 1.0, 1.0, 0.0, float("inf")),
                     lambda: H.spherical_harmonic(3, 0, 1.0, 0.0), lambda: H.energy_hartree(0),
                     lambda: H.radial(True, 0, 1.0)):
            with self.assertRaises(ValueError):
                call()


if __name__ == "__main__":
    unittest.main()
