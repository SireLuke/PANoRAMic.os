#!/usr/bin/env python3
"""Validate a STRATA-0.1 run record with the Python standard library."""
import argparse
import json
import re
import sys
from pathlib import Path

STATUSES = {"pass", "fail", "inconclusive", "not_tested"}
DEFAULT_RECORD = Path(__file__).parent / "runs" / "STRATA-002-GEOMETRY-AUDIT-2026-11-09.json"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate(record):
    require(record.get("schema_version") == "strata-run-v0.1", "unsupported schema_version")
    require(record.get("protocol") == "STRATA-0.1", "unsupported protocol")
    source = record.get("source", {})
    for key in ("commit", "evidence_commit", "additional_control_commit"):
        require(bool(re.fullmatch(r"[0-9a-f]{40}", source.get(key, ""))),
                f"source.{key} must be a 40-character lowercase Git SHA")

    report = record.get("strata_runner_output", {}).get("report", {})
    require(report.get("protocol") == "STRATA-0.1", "runner report protocol mismatch")
    dimensions = report.get("dimensions", [])
    names = [item.get("dimension") for item in dimensions]
    require(len(names) == len(set(names)), "runner dimension names must be unique")
    require(all(item.get("status") in STATUSES for item in dimensions),
            "runner dimension has an invalid status")

    e8 = record.get("strata_runner_output", {}).get("e8", {})
    require(e8.get("roots") == 240, "E8 root count mismatch")
    require(e8.get("edges_inner_product_1") == 6720, "E8 edge count mismatch")
    require(e8.get("degree_min") == e8.get("degree_max") == 56,
            "E8 adjacency degree mismatch")

    for group, result in record.get("verification", {}).items():
        require(result.get("status") in STATUSES, f"{group}: invalid status")
        if "run" in result:
            require(result.get("run") == result.get("passed", 0) + result.get("failed", 0),
                    f"{group}: run count does not match passed + failed")

    geometry = record.get("geometry_runs", [])
    require(geometry, "at least one geometry run is required")
    require(all(item.get("status") in STATUSES for item in geometry),
            "geometry run has an invalid status")
    catalogue = record.get("geometry_catalogue", {})
    require(catalogue.get("status") in STATUSES, "geometry catalogue status is invalid")
    require(all(item.get("status") in STATUSES for item in catalogue.get("items", [])),
            "geometry catalogue item has an invalid status")
    eleven_d = record.get("eleven_d_parameters", {})
    require(eleven_d.get("status") in STATUSES, "11D status is invalid")
    require(record.get("limitations"), "limitations must be recorded")
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("record", nargs="?", type=Path, default=DEFAULT_RECORD)
    args = parser.parse_args()
    try:
        data = json.loads(args.record.read_text(encoding="utf-8"))
        validate(data)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"INVALID: {exc}", file=sys.stderr)
        return 1
    print(f"VALID: {args.record}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
