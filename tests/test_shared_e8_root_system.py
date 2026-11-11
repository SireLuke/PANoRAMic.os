import unittest
from fractions import Fraction as Q

from core.geometry.e8_root_system import e8_roots_exact, e8_roots_float
from core.abom_v8.abom_v8_model import e8_roots as abom_roots
from experiments.gosset_local_cell_star_audit import build_e8_roots as gosset_exact
from experiments.gosset_sierpinski_experiment import build_e8_roots as sierpinski_roots
from experiments.strata.e8_adapter import build_roots as strata_roots


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


class SharedE8RootSystemTests(unittest.TestCase):
    def test_canonical_exact_set_cardinality_norm_and_uniqueness(self):
        roots = e8_roots_exact()
        self.assertEqual(len(roots), 240)
        self.assertEqual(len(set(roots)), 240)
        self.assertTrue(all(dot(root, root) == Q(2) for root in roots))

    def test_root_graph_has_6720_edges_and_degree_56(self):
        roots = e8_roots_exact()
        degrees = [sum(dot(root, other) == 1 for other in roots) for root in roots]
        self.assertEqual(sum(degrees) // 2, 6720)
        self.assertEqual(set(degrees), {56})

    def test_all_four_existing_adapters_match_canonical_exact_set(self):
        canonical = set(e8_roots_exact())
        self.assertEqual(set(gosset_exact()), canonical)
        self.assertEqual({tuple(Q(str(x)) for x in r) for r in abom_roots()}, canonical)
        self.assertEqual({tuple(Q(str(x)) for x in r) for r in strata_roots()}, canonical)
        self.assertEqual({tuple(Q(str(x)) for x in r) for r in sierpinski_roots()}, canonical)

    def test_float_adapter_is_explicit_and_lossless_for_e8_coordinates(self):
        self.assertEqual(
            {tuple(Q(str(x)) for x in r) for r in e8_roots_float()},
            set(e8_roots_exact()),
        )


if __name__ == "__main__":
    unittest.main()
