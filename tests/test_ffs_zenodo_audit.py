import unittest

from experiments.fractional_fermi_sea.zenodo_dataset_audit import (
    ZENODO_FILES,
    first_zero_crossings,
)


class FFSZenodoAuditTests(unittest.TestCase):
    def test_registered_files_have_md5_provenance(self):
        self.assertEqual(set(ZENODO_FILES), {
            "figure3A_data.csv", "figure3B_data.csv", "figure3C_data.csv"
        })
        self.assertTrue(all(len(value) == 32 for value in ZENODO_FILES.values()))

    def test_zero_crossing_linear_interpolation(self):
        crossings = first_zero_crossings([0.0, 1.0, 2.0], [1.0, 0.5, -0.5])
        self.assertEqual(crossings, [1.5])

    def test_multiple_crossings(self):
        crossings = first_zero_crossings(
            [0.0, 1.0, 2.0, 3.0, 4.0],
            [1.0, -1.0, -1.0, 1.0, -1.0],
        )
        self.assertEqual(crossings, [0.5, 2.5, 3.5])

    def test_rejects_length_mismatch(self):
        with self.assertRaises(ValueError):
            first_zero_crossings([0.0], [1.0, -1.0])


if __name__ == "__main__":
    unittest.main()
