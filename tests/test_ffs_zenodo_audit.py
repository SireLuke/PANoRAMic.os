import unittest
from unittest.mock import patch
from experiments.fractional_fermi_sea.zenodo_dataset_audit import (
    ZENODO_FILES, first_zero_crossings, _series_points, verify_record_metadata,
)

class FFSZenodoAuditTests(unittest.TestCase):
    def test_registered_files_have_md5_provenance(self):
        self.assertEqual(set(ZENODO_FILES), {"figure3A_data.csv","figure3B_data.csv","figure3C_data.csv"})
        self.assertTrue(all(len(value)==32 for value in ZENODO_FILES.values()))

    def test_license_metadata_is_verified_not_assumed(self):
        payload={"id":18697242,"metadata":{"doi":"10.5281/zenodo.18697242","version":"1",
            "publication_date":"2026-02-19","license":{"id":"cc-by-4.0"}}}
        result=verify_record_metadata(payload)
        self.assertEqual(result["status"],"pass")
        payload["metadata"]["license"]["id"]="unknown"
        self.assertEqual(verify_record_metadata(payload)["status"],"inconclusive")

    def test_zero_crossing_linear_interpolation(self):
        self.assertEqual(first_zero_crossings([0.,1.,2.],[1.,.5,-.5]),[1.5])

    def test_multiple_crossings(self):
        self.assertEqual(first_zero_crossings([0.,1.,2.,3.,4.],[1.,-1.,-1.,1.,-1.]),[.5,2.5,3.5])

    def test_sparse_padded_csv_columns_are_extracted_as_pairs(self):
        rows=[{"x":"0","y":"1"},{"x":"","y":""},{"x":"2","y":"-1"}]
        self.assertEqual(_series_points(rows,"x","y"),[(0.,1.),(2.,-1.)])

    def test_rejects_half_missing_sample(self):
        with self.assertRaises(ValueError): _series_points([{"x":"1","y":""}],"x","y")

    def test_rejects_length_mismatch(self):
        with self.assertRaises(ValueError): first_zero_crossings([0.],[1.,-1.])

if __name__=="__main__": unittest.main()
