import random
import unittest

from experiments.moonshine_sierpinski.leech_golay_construction import (
    leech_minimal_vectors,
)
from experiments.moonshine_sierpinski.leech_unimodular_basis import (
    _COORDINATE_BASIS,
)
from experiments.moonshine_sierpinski.leech_lattice_cocycle import (
    lattice_cocycle_sign,
    lattice_inner_product_numerator,
    leech_basis_coordinates,
)


class LeechLatticeCocycleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.basis = _COORDINATE_BASIS
        cls.columns = [
            tuple(cls.basis[row][column] for row in range(24))
            for column in range(24)
        ]

    def test_basis_coordinates_round_trip(self):
        rng = random.Random(20261123)
        for _ in range(100):
            coefficients = [rng.randint(-3, 3) for _ in range(24)]
            vector = tuple(
                sum(self.basis[i][j] * coefficients[j] for j in range(24))
                for i in range(24)
            )
            self.assertEqual(leech_basis_coordinates(vector), tuple(coefficients))

    def test_rejects_nonlattice_coordinate_vector(self):
        with self.assertRaises(ValueError):
            leech_basis_coordinates((1,) * 24)

    def test_cocycle_is_normalized(self):
        zero = (0,) * 24
        vector = self.columns[0]
        self.assertEqual(lattice_cocycle_sign(zero, vector), 1)
        self.assertEqual(lattice_cocycle_sign(vector, zero), 1)

    def test_commutator_matches_lattice_inner_product_parity(self):
        rng = random.Random(240024)
        for _ in range(300):
            a = tuple(sum(self.basis[i][j] * (rng.randint(-2, 2) if j == k else 0)
                          for j in range(24)) for i in range(24) for k in [])
            # Generate coefficient vectors independently, then map through B.
            n = [rng.randint(-2, 2) for _ in range(24)]
            m = [rng.randint(-2, 2) for _ in range(24)]
            left = tuple(sum(self.basis[i][j] * n[j] for j in range(24)) for i in range(24))
            right = tuple(sum(self.basis[i][j] * m[j] for j in range(24)) for i in range(24))
            sign_ratio = lattice_cocycle_sign(left, right) * lattice_cocycle_sign(right, left)
            inner_numerator = lattice_inner_product_numerator(left, right)
            self.assertEqual(sign_ratio, -1 if (inner_numerator // 8) & 1 else 1)

    def test_bimultiplicative_two_cocycle_identity(self):
        rng = random.Random(20261124)
        for _ in range(150):
            vectors = []
            for _ in range(3):
                coeffs = [rng.randint(-1, 1) for _ in range(24)]
                vectors.append(tuple(
                    sum(self.basis[i][j] * coeffs[j] for j in range(24))
                    for i in range(24)
                ))
            a, b, c = vectors
            ab = tuple(x + y for x, y in zip(a, b))
            bc = tuple(x + y for x, y in zip(b, c))
            self.assertEqual(
                lattice_cocycle_sign(a, b) * lattice_cocycle_sign(ab, c),
                lattice_cocycle_sign(b, c) * lattice_cocycle_sign(a, bc),
            )

    def test_self_cocycle_matches_half_norm(self):
        rng = random.Random(20261125)
        for _ in range(100):
            coeffs = [rng.randint(-2, 2) for _ in range(24)]
            vector = tuple(
                sum(self.basis[i][j] * coeffs[j] for j in range(24))
                for i in range(24)
            )
            norm_numerator = sum(x * x for x in vector)
            self.assertEqual(norm_numerator % 16, 0)
            self.assertEqual(
                lattice_cocycle_sign(vector, vector),
                -1 if (norm_numerator // 16) & 1 else 1,
            )

    def test_minimal_shell_vectors_are_in_basis_lattice(self):
        shell = leech_minimal_vectors()
        for vector in (shell[0], shell[1103], shell[1104], shell[-1]):
            coords = leech_basis_coordinates(vector)
            self.assertEqual(len(coords), 24)


if __name__ == "__main__":
    unittest.main()
