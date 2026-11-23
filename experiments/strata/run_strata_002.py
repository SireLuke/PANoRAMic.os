#!/usr/bin/env python3
"""Run synthetic STRATA-002 pipeline smoke checks; not empirical validation."""
from __future__ import annotations

import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from e8_adapter import adjacency_summary
from strata_core import DimensionResult, StrataReport, permutation_control, retention


REQUIRED_DIMENSIONS = (
    "three_meaningful_scales",
    "two_independent_domains",
    "two_representations",
    "observer_implementation_checks",
    "randomized_controls",
    "structure_preserving_controls",
    "held_out_predictive_evaluation",
    "leakage_controls",
    "domain_native_baselines",
    "uncertainty",
    "provenance",
    "reproducibility",
)


def main() -> None:
    e8 = adjacency_summary()

    # Toy feature sets exercise the report plumbing only. They are not
    # qualifying empirical scales and must remain not_tested in STRATA.
    scales = [
        {"cycle", "branch", "hub"},
        {"cycle", "branch", "hub", "boundary"},
        {"cycle", "branch", "hub", "boundary", "nested"},
    ]
    scale_scores = [retention(scales[0], features) for features in scales]

    labels = [0, 0, 1, 1, 0, 1, 0, 1]
    shuffled = permutation_control(labels, seed=20261109)

    dimension_details = {
        "three_meaningful_scales": "Synthetic feature sets are a plumbing fixture, not qualifying meaningful scales.",
        "two_independent_domains": "No independent empirical domains are included.",
        "two_representations": "No independently derived representations are compared.",
        "observer_implementation_checks": "No observer implementation is evaluated by this smoke run.",
        "randomized_controls": "A seeded shuffle is generated as a plumbing check only; no inferential control is claimed.",
        "structure_preserving_controls": "No structure-preserving control is evaluated.",
        "held_out_predictive_evaluation": "No held-out predictive evaluation is performed.",
        "leakage_controls": "No train/test or cross-domain leakage analysis is performed.",
        "domain_native_baselines": "No domain-native baseline is evaluated.",
        "uncertainty": "No empirical uncertainty estimate is produced.",
        "provenance": "The synthetic fixture and fixed seed are recorded; no empirical source provenance is claimed.",
        "reproducibility": (
            f"Software smoke checks are deterministic: seed=20261109, "
            f"E8 roots={e8['roots']}, degree-56 regular={e8['regular_degree_56']}, "
            f"toy Jaccard retention={scale_scores}, shuffled labels={shuffled}."
        ),
    }

    dimensions = [
        DimensionResult(
            name,
            "pass" if name == "reproducibility" else "not_tested",
            dimension_details[name],
        )
        for name in REQUIRED_DIMENSIONS
    ]

    report = StrataReport(
        claim_id="STRATA-002-SYNTHETIC-SMOKE",
        hypothesis=(
            "The harness records software checks without promoting synthetic "
            "fixtures to empirical evidence."
        ),
        evidence_level="software-smoke-test",
        seed=20261109,
        dimensions=dimensions,
        limitations=[
            "All non-E8 scale fixtures are synthetic.",
            "E8 checks validate root-system construction and adjacency regularity only.",
            "The seeded label shuffle is a plumbing check, not an inferential randomized control.",
            "No biological, ecological, transport, or physical dataset has been evaluated.",
            "No STRATA invariant or scientific law is established by this run.",
        ],
    )

    output = {
        "e8": e8,
        "smoke_fixtures": {
            "toy_scale_jaccard_retention": scale_scores,
            "seed": 20261109,
            "shuffled_labels": shuffled,
        },
        "report": report.to_dict(),
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
