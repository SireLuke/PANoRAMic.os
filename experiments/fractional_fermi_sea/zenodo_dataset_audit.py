"""Fetch and audit the published FFS figure data from Zenodo.

No experimental files are copied into the repository. Each CSV is fetched at
runtime and verified against the Zenodo record's published MD5 digest.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
from urllib.request import Request, urlopen

ZENODO_FILES = {
    "figure3A_data.csv": "068240a2069550d96d0d302c40cab666",
    "figure3B_data.csv": "2319b4d9cf9114466addc103525cd92d",
    "figure3C_data.csv": "b98af0284338f88a4fb39e8ea82972b4",
}
BASE_URL = "https://zenodo.org/records/18697242/files/{}?download=1"


def fetch_verified_csv(filename: str) -> tuple[list[str], list[dict[str, str]], str]:
    if filename not in ZENODO_FILES:
        raise ValueError(f"unregistered Zenodo file: {filename}")
    request = Request(BASE_URL.format(filename), headers={"User-Agent": "PAN-FFS-audit/1.0"})
    with urlopen(request, timeout=30) as response:
        payload = response.read()
    digest = hashlib.md5(payload).hexdigest()
    expected = ZENODO_FILES[filename]
    if digest != expected:
        raise ValueError(f"MD5 mismatch for {filename}: {digest} != {expected}")
    text = payload.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(text))
    if not reader.fieldnames:
        raise ValueError(f"missing CSV header: {filename}")
    rows = list(reader)
    return list(reader.fieldnames), rows, digest


def _number(row: dict[str, str], key: str) -> float:
    value = row.get(key, "")
    if value == "":
        raise ValueError(f"missing {key}")
    return float(value)


def _series_points(rows: list[dict[str, str]], x_key: str, y_key: str) -> list[tuple[float, float]]:
    """Extract paired nonblank samples; Zenodo figure CSVs pad unequal series."""
    points = []
    for row in rows:
        x_raw, y_raw = row.get(x_key, ""), row.get(y_key, "")
        if x_raw == "" and y_raw == "":
            continue
        if x_raw == "" or y_raw == "":
            raise ValueError(f"unpaired missing sample in {x_key}/{y_key}")
        points.append((float(x_raw), float(y_raw)))
    return sorted(points)


def first_zero_crossings(x_values: list[float], y_values: list[float]) -> list[float]:
    """Linearly interpolate every strict sign change in an ordered series."""
    if len(x_values) != len(y_values):
        raise ValueError("x and y lengths differ")
    crossings = []
    for i in range(1, len(x_values)):
        x0, x1 = x_values[i - 1], x_values[i]
        y0, y1 = y_values[i - 1], y_values[i]
        if y0 == 0.0:
            crossings.append(x0)
        elif y0 * y1 < 0.0:
            crossings.append(x0 - y0 * (x1 - x0) / (y1 - y0))
    if y_values and y_values[-1] == 0.0:
        crossings.append(x_values[-1])
    return crossings


def _first_trough_between_crossings(
    x_values: list[float], y_values: list[float], crossings: list[float]
) -> dict | None:
    if len(crossings) < 2:
        return None
    left, right = crossings[0], crossings[1]
    candidates = [
        (x, y) for x, y in zip(x_values, y_values)
        if left <= x <= right
    ]
    if not candidates:
        return None
    x_min, y_min = min(candidates, key=lambda pair: pair[1])
    return {"x": x_min, "y": y_min, "window": [left, right]}


def audit_zenodo_ffs_dataset() -> dict:
    files = {}
    loaded = {}
    for filename in ZENODO_FILES:
        header, rows, digest = fetch_verified_csv(filename)
        files[filename] = {
            "md5": digest,
            "rows": len(rows),
            "columns": header,
        }
        loaded[filename] = rows

    momentum = loaded["figure3A_data.csv"]
    correlations = loaded["figure3B_data.csv"]
    log_correlations = loaded["figure3C_data.csv"]
    if len(momentum) < 100 or len(correlations) < 100 or len(log_correlations) < 100:
        raise AssertionError("unexpectedly small FFS figure dataset")

    series = {}
    for ell in (0, 2, 4):
        suffix = f"L{ell}"
        pairs = [pair for pair in _series_points(correlations, f"exp_x_{suffix}", f"exp_y_{suffix}") if pair[0] >= 0.0]
        x_sorted = [p[0] for p in pairs]
        y_sorted = [p[1] for p in pairs]
        crossings = first_zero_crossings(x_sorted, y_sorted)
        trough = _first_trough_between_crossings(x_sorted, y_sorted, crossings)
        result = {
            "measured_points": len(pairs),
            "zero_crossings_um": crossings[:4],
            "first_oscillation_trough": trough,
        }
        if ell in (2, 4) and crossings:
            # For an ideal homogeneous FFS, x0 = pi/(ell*k_F).
            # This is only an effective diagnostic; tube/trap averaging modifies it.
            result["homogeneous_effective_kF_per_um"] = 3.141592653589793 / (ell * crossings[0])
            result["homogeneous_reference_only"] = True
        series[suffix] = result

    # Ensure that the experimental and GHD columns for each state are present.
    required = [
        "exp_x_L0", "exp_y_L0", "sim_x_L0", "sim_mean_L0",
        "exp_x_L2", "exp_y_L2", "sim_x_L2", "sim_mean_L2",
        "exp_x_L4", "exp_y_L4", "sim_x_L4", "sim_mean_L4",
    ]
    missing = [key for key in required if key not in momentum[0]]
    if missing:
        raise AssertionError(f"figure3A missing required columns: {missing}")

    return {
        "dataset": "Zeng et al., Realization of fractional Fermi seas",
        "zenodo_record": "10.5281/zenodo.18697242",
        "files": files,
        "correlation_diagnostics": series,
        "interpretation": (
            "Measured figure data and GHD series are provenance-checked. "
            "Zero-crossing-derived kF values are effective homogeneous-sinc "
            "diagnostics only; they are not trap-corrected physical estimates."
        ),
        "not_performed": [
            "raw absorption-image reanalysis",
            "GHD simulation reproduction",
            "parameter fitting",
            "uncertainty propagation beyond supplied pointwise errors",
            "causal V8 mapping",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(audit_zenodo_ffs_dataset(), indent=2, sort_keys=True))
