#!/usr/bin/env python3
"""Run synthetic STRATA-002 pipeline smoke checks; not empirical validation."""
from pathlib import Path
import json
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from e8_adapter import adjacency_summary
from strata_core import DimensionResult, StrataReport, retention, permutation_control

def main():
    e8 = adjacency_summary()
    # Toy feature sets at three declared resolutions. This fixture tests plumbing,
    # not a claim that these features are universal or naturally scale invariant.
    scales = [
        {"cycle", "branch", "hub"},
        {"cycle", "branch", "hub", "boundary"},
        {"cycle", "branch", "hub", "boundary", "nested"},
    ]
    scale_scores = [retention(scales[0], x) for x in scales]
    labels = [0, 0, 1, 1, 0, 1, 0, 1]
    shuffled = permutation_control(labels, seed=20261109)
    report = StrataReport(
        claim_id="STRATA-002-SYNTHETIC-SMOKE",
        hypothesis="The harness records scale retention and controls without promoting synthetic fixtures to empirical evidence.",
        evidence_level="software-smoke-test",
        seed=20261109,
        dimensions=[
            DimensionResult("E8 root construction", "pass" if e8["roots"] == 240 and e8["regular_degree_56"] else "fail", str(e8)),
            DimensionResult("three-scale fixture", "pass" if len(scale_scores) == 3 else "fail", f"Jaccard retention={scale_scores}"),
            DimensionResult("randomized control generation", "pass" if sorted(labels) == sorted(shuffled) else "fail", f"seeded permutation={shuffled}"),
            DimensionResult("independent empirical domains", "not_tested", "No empirical datasets are bundled in this scaffold."),
            DimensionResult("held-out cross-domain prediction", "not_tested", "No predictive transfer claim is made."),
        ],
        limitations=[
            "All non-E8 scale fixtures are synthetic.",
            "E8 checks validate root-system construction and adjacency regularity only.",
            "No biological, ecological, transport, or physical dataset has been evaluated.",
            "No STRATA invariant or scientific law is established by this run.",
        ],
    )
    print(json.dumps({"e8": e8, "report": report.to_dict()}, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
