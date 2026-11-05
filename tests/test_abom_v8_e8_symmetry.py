"""Which signed-permutation subgroup of B8 actually preserves the E8 root set?

Full B8 does not (one sign flip breaks the half-integer parity rule); the
even-sign-flip subgroup D8 (order 2^7 * 8!, index 135 in W(E8)) does.
"""
import random
import unittest

from core.abom_v8.abom_v8_model import e8_roots, hyperoctahedral_action


def _canon(v):
    return tuple(x + 0.0 for x in v)


class E8SymmetryTest(unittest.TestCase):
    def setUp(self):
        self.roots = {_canon(r) for r in e8_roots()}
        self.rng = random.Random(20261104)

    def _image(self, perm, signs):
        return {_canon(hyperoctahedral_action(r, perm, signs)) for r in self.roots}

    def test_even_sign_flips_preserve_root_set(self):
        for _ in range(300):
            perm = list(range(8)); self.rng.shuffle(perm)
            signs = [self.rng.choice((-1, 1)) for _ in range(8)]
            if signs.count(-1) % 2:
                signs[0] = -signs[0]
            self.assertEqual(self._image(perm, signs), self.roots)

    def test_single_sign_flip_breaks_root_set(self):
        signs = [1] * 8
        signs[0] = -1
        self.assertNotEqual(self._image(list(range(8)), signs), self.roots)

    def test_index_of_d8_in_weyl_e8(self):
        import math
        self.assertEqual(696729600 // (2 ** 7 * math.factorial(8)), 135)
        self.assertEqual(696729600 % (2 ** 7 * math.factorial(8)), 0)


if __name__ == "__main__":
    unittest.main()
