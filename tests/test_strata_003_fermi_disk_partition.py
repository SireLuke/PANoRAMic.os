import math
import unittest

from experiments.strata.fermi_disk_partition import (
    black_area_fraction,
    energy_ratio_from_occupancy,
    fermi_occupancy,
    five_panel_states,
    head_diameters,
    white_area_fraction,
)


class FermiDiskPartitionTests(unittest.TestCase):
    def test_five_panel_closed_form_areas(self):
        for state in five_panel_states():
            self.assertAlmostEqual(state["white_area_fraction"], state["white_occupancy"], places=14)
            self.assertAlmostEqual(state["black_area_fraction"], state["black_occupancy"], places=14)
            self.assertAlmostEqual(state["white_area_fraction"] + state["black_area_fraction"], 1.0, places=14)

    def test_semicircle_diameters_sum_to_disk_diameter(self):
        for n in (0.0, 0.05, 0.25, 0.5, 0.75, 0.95, 1.0):
            d_black, d_white = head_diameters(n)
            self.assertAlmostEqual(d_black + d_white, 2.0)
            self.assertGreaterEqual(d_black, 0.0)
            self.assertGreaterEqual(d_white, 0.0)

    def test_fermi_complement_symmetry(self):
        for x in (-4.0, -1.1, 0.0, 1.1, 4.0):
            self.assertAlmostEqual(fermi_occupancy(-x), 1.0 - fermi_occupancy(x), places=14)

    def test_occupancy_inverse_and_five_energy_values(self):
        expected = (-math.log(19.0), -math.log(3.0), 0.0, math.log(3.0), math.log(19.0))
        for state, value in zip(five_panel_states(), expected):
            x = energy_ratio_from_occupancy(state["white_occupancy"])
            self.assertAlmostEqual(x, value, places=14)
            self.assertAlmostEqual(fermi_occupancy(x), state["white_occupancy"], places=14)

    def test_delta_tanh_identity(self):
        for x in (-3.0, -0.5, 0.0, 1.2, 4.0):
            n = fermi_occupancy(x)
            self.assertAlmostEqual(2.0 * n - 1.0, -math.tanh(x / 2.0), places=14)

    def test_numeric_disk_grid_matches_exact_area(self):
        # Independent midpoint quadrature over a square bounding the unit disk.
        m = 360
        for n in (0.25, 0.5, 0.75):
            inside = white = 0
            d_black, d_white = head_diameters(n)
            c_black = -1.0 + d_black / 2.0
            c_white = -1.0 + d_black + d_white / 2.0
            for i in range(m):
                x = -1.0 + (i + 0.5) * 2.0 / m
                for j in range(m):
                    y = -1.0 + (j + 0.5) * 2.0 / m
                    if x*x + y*y > 1.0:
                        continue
                    inside += 1
                    if y > 0.0:
                        point_white = (x-c_black)**2 + y*y > (d_black/2.0)**2
                    else:
                        point_white = (x-c_white)**2 + y*y <= (d_white/2.0)**2
                    white += point_white
            self.assertAlmostEqual(white / inside, n, delta=0.004)

    def test_invalid_inputs_rejected(self):
        for n in (-0.1, 1.1, float("nan")):
            with self.assertRaises(ValueError):
                head_diameters(n)
        for n in (0.0, 1.0):
            with self.assertRaises(ValueError):
                energy_ratio_from_occupancy(n)
        with self.assertRaises(ValueError):
            fermi_occupancy(float("inf"))


if __name__ == "__main__":
    unittest.main()
