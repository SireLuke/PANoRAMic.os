"""Tests for QWAVE v0 SI relations and temporal metadata."""
import math
import unittest

from core.abom_v8.qwave import (
    PLANCK_CONSTANT_J_S,
    REDUCED_PLANCK_CONSTANT_J_S,
    SPEED_OF_LIGHT_M_S,
    photon_from_frequency,
    photon_from_wavelength,
    planck_scales,
    temporal_measurement_metadata,
)


class QWaveTests(unittest.TestCase):
    def test_planck_scales_are_positive_and_dimensionally_related(self):
        scales = planck_scales()
        self.assertGreater(scales["planck_length_m"], 0.0)
        self.assertGreater(scales["planck_time_s"], 0.0)
        self.assertGreater(scales["planck_energy_j"], 0.0)
        self.assertAlmostEqual(
            scales["planck_length_m"] / scales["planck_time_s"],
            SPEED_OF_LIGHT_M_S,
        )
        self.assertAlmostEqual(
            scales["planck_frequency_hz"] * scales["planck_time_s"], 1.0
        )

    def test_frequency_wavelength_energy_relations(self):
        frequency = 5.0e14
        result = photon_from_frequency(frequency)
        self.assertAlmostEqual(result["wavelength_m"] * frequency, SPEED_OF_LIGHT_M_S)
        self.assertAlmostEqual(result["photon_energy_j"], PLANCK_CONSTANT_J_S * frequency)
        self.assertAlmostEqual(
            REDUCED_PLANCK_CONSTANT_J_S * result["angular_frequency_rad_s"],
            result["photon_energy_j"],
        )

    def test_wavelength_entrypoint_matches_frequency_entrypoint(self):
        wavelength = 500e-9
        from_wavelength = photon_from_wavelength(wavelength)
        from_frequency = photon_from_frequency(SPEED_OF_LIGHT_M_S / wavelength)
        self.assertAlmostEqual(
            from_wavelength["photon_energy_j"], from_frequency["photon_energy_j"]
        )
        self.assertAlmostEqual(from_wavelength["wavenumber_m_inv"], 1.0 / wavelength)

    def test_temporal_metadata_records_scale_without_enforcing_floor(self):
        metadata = temporal_measurement_metadata(
            1e-30, 2e-31, physical_time_s=1.25, timing_uncertainty_s=0.0
        )
        self.assertLess(metadata["sample_interval_s"], metadata["planck_time_s"])
        self.assertEqual(
            metadata["planck_time_role"],
            "derived_reference_scale_not_a_measurement_floor",
        )
        self.assertEqual(metadata["physical_time_s"], 1.25)
        self.assertEqual(metadata["timing_uncertainty_s"], 0.0)

    def test_invalid_temporal_values_are_rejected(self):
        for value in (0.0, -1.0, math.inf, math.nan):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    temporal_measurement_metadata(value, 1e-9)
        with self.assertRaises(ValueError):
            temporal_measurement_metadata(1e-9, 1e-9, timing_uncertainty_s=-1.0)

    def test_invalid_photon_inputs_are_rejected(self):
        for value in (0.0, -1.0, math.inf, math.nan):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    photon_from_frequency(value)
                with self.assertRaises(ValueError):
                    photon_from_wavelength(value)


if __name__ == "__main__":
    unittest.main()
