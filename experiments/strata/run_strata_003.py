#!/usr/bin/env python3
"""Run STRATA-003 Fermi disk-partition and Zeng FFS source audit."""
from __future__ import annotations

import json

from experiments.fractional_fermi_sea.zenodo_dataset_audit import audit_zenodo_ffs_dataset
from experiments.strata.fermi_disk_partition import five_panel_states


def main() -> dict:
    states = five_panel_states()
    area_identity = all(
        abs(row["white_area_fraction"] - row["white_occupancy"]) < 1e-12
        and abs(row["black_area_fraction"] - row["black_occupancy"]) < 1e-12
        and abs(row["white_area_fraction"] + row["black_area_fraction"] - 1.0) < 1e-12
        for row in states
    )
    dataset = audit_zenodo_ffs_dataset()
    return {
        "run_id": "STRATA-003-FERMI-DISK-FFS-001",
        "protocol": "STRATA-0.1",
        "status": "INCONCLUSIVE" if area_identity and dataset["files"] else "FAIL",
        "fermi_disk_partition": {
            "status": "PASS" if area_identity else "FAIL",
            "states": states,
            "scope": "independent closed-form verification of the Fractal Kernel unit-disk semicircle partition",
            "eye_geometry": "decorative Gerono/lemniscate marks excluded from area accounting",
        },
        "zeng_ffs_dataset": dataset,
        "strata_dimensions": [
            {"dimension": "Fermi disk area identity", "status": "pass" if area_identity else "fail"},
            {"dimension": "source identity and published checksum verification", "status": "pass"},
            {"dimension": "dataset license and reuse permission", "status": "inconclusive"},
            {"dimension": "one experimental domain", "status": "pass"},
            {"dimension": "three meaningful scales", "status": "not_tested"},
            {"dimension": "independent domains", "status": "not_tested"},
            {"dimension": "independent representations of the same target", "status": "not_tested"},
            {"dimension": "randomized and structure-preserving controls", "status": "not_tested"},
            {"dimension": "domain-native baselines", "status": "not_tested"},
            {"dimension": "held-out predictive evaluation and leakage controls", "status": "not_tested"},
            {"dimension": "uncertainty propagation", "status": "not_tested"},
        ],
        "limitations": [
            "The unit-disk partition identity is exact; the eye marks are excluded.",
            "The Gerono transport curve in the Fractal Kernel is a separate curve family and is not substituted for the S-curve disk boundary.",
            "The Zeng data audit verifies published figure CSVs and extracts diagnostics; it does not reproduce the experiment or GHD simulations.",
            "The accessible Zenodo record does not declare a dataset license; files are fetched transiently and are not redistributed.",
            "No cross-domain invariant, causal mechanism, or scientific law is inferred.",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(main(), indent=2, sort_keys=True))
