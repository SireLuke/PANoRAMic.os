import unittest

from experiments.fractional_fermi_sea.zenodo_dataset_audit import (
    ZENODO_FILES,
    first_zero_crossings,
    _series_points,
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

    def test_sparse_padded_csv_columns_are_extracted_as_pairs(self):
        rows = [
            {"x": "0", "y": "1"},
            {"x": "", "y": ""},
            {"x": "2", "y": "-1"},
        ]
        self.assertEqual(_series_points(rows, "x", "y"), [(0.0, 1.0), (2.0, -1.0)])

    def test_rejects_half_missing_sample(self):
        with self.assertRaises(ValueError):
            _series_points([{"x": "1", "y": ""}], "x", "y")

    def test_rejects_length_mismatch(self):
        with self.assertRaises(ValueError):
            first_zero_crossings([0.0], [1.0, -1.0])


if __name__ == "__main__":
    unittest.main()
