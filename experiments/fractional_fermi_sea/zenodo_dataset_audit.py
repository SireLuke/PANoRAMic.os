"""Fetch and audit published FFS figure data and Zenodo license metadata.

Files are fetched transiently, checked against publisher MD5 values, and
assigned SHA-256 digests. License status is PASS only when the live record API
returns the preregistered CC BY 4.0 identifier.
"""
from __future__ import annotations
import csv
import hashlib
import io
import json
from datetime import datetime, timezone
from urllib.request import Request, urlopen

ZENODO_RECORD = "18697242"
ZENODO_API = f"https://zenodo.org/api/records/{ZENODO_RECORD}"
EXPECTED_LICENSE = "cc-by-4.0"
ZENODO_FILES = {
    "figure3A_data.csv": "068240a2069550d96d0d302c40cab666",
    "figure3B_data.csv": "2319b4d9cf9114466addc103525cd92d",
    "figure3C_data.csv": "b98af0284338f88a4fb39e8ea82972b4",
}
BASE_URL = "https://zenodo.org/records/18697242/files/{}?download=1"


def fetch_record_metadata() -> dict:
    request = Request(ZENODO_API, headers={"User-Agent": "PAN-STRATA-audit/1.0"})
    with urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def verify_record_metadata(payload: dict) -> dict:
    metadata = payload.get("metadata", {})
    doi = metadata.get("doi", "").lower()
    license_id = (metadata.get("license") or {}).get("id")
    version = metadata.get("version")
    published = metadata.get("publication_date")
    checks = {
        "doi": doi == "10.5281/zenodo.18697242",
        "version": version in ("1", "v1"),
        "published_utc": published == "2026-02-19",
        "license": license_id == EXPECTED_LICENSE,
    }
    return {
        "record_id": str(payload.get("id", "")),
        "doi": doi,
        "version": version,
        "published_utc": published,
        "license": license_id,
        "checks": checks,
        "status": "pass" if all(checks.values()) else "inconclusive",
        "retrieved_utc": datetime.now(timezone.utc).isoformat(),
    }


def fetch_verified_csv(filename: str) -> tuple[list[str], list[dict[str, str]], str, str]:
    if filename not in ZENODO_FILES:
        raise ValueError(f"unregistered Zenodo file: {filename}")
    request = Request(BASE_URL.format(filename), headers={"User-Agent": "PAN-FFS-audit/1.0"})
    with urlopen(request, timeout=30) as response:
        payload = response.read()
    digest, sha256 = hashlib.md5(payload).hexdigest(), hashlib.sha256(payload).hexdigest()
    expected = ZENODO_FILES[filename]
    if digest != expected:
        raise ValueError(f"MD5 mismatch for {filename}: {digest} != {expected}")
    reader = csv.DictReader(io.StringIO(payload.decode("utf-8-sig")))
    if not reader.fieldnames:
        raise ValueError(f"missing CSV header: {filename}")
    rows = list(reader)
    return list(reader.fieldnames), rows, digest, sha256


def _series_points(rows, x_key, y_key):
    points = []
    for row in rows:
        x_raw, y_raw = row.get(x_key, ""), row.get(y_key, "")
        if x_raw == "" and y_raw == "":
            continue
        if x_raw == "" or y_raw == "":
            raise ValueError(f"unpaired missing sample in {x_key}/{y_key}")
        points.append((float(x_raw), float(y_raw)))
    return sorted(points)


def first_zero_crossings(x_values, y_values):
    if len(x_values) != len(y_values):
        raise ValueError("x and y lengths differ")
    crossings = []
    for i in range(1, len(x_values)):
        x0, x1, y0, y1 = x_values[i-1], x_values[i], y_values[i-1], y_values[i]
        if y0 == 0.0:
            crossings.append(x0)
        elif y0 * y1 < 0.0:
            crossings.append(x0 - y0 * (x1-x0) / (y1-y0))
    if y_values and y_values[-1] == 0.0:
        crossings.append(x_values[-1])
    return crossings


def _first_trough_between_crossings(x_values, y_values, crossings):
    if len(crossings) < 2:
        return None
    left, right = crossings[0], crossings[1]
    candidates = [(x,y) for x,y in zip(x_values,y_values) if left <= x <= right]
    if not candidates:
        return None
    x_min, y_min = min(candidates, key=lambda pair: pair[1])
    return {"x":x_min,"y":y_min,"window":[left,right]}


def audit_zenodo_ffs_dataset():
    metadata = verify_record_metadata(fetch_record_metadata())
    files, loaded = {}, {}
    for filename in ZENODO_FILES:
        header, rows, digest, sha256 = fetch_verified_csv(filename)
        files[filename] = {"md5":digest,"sha256":sha256,
            "retrieved_utc":datetime.now(timezone.utc).isoformat(),
            "rows":len(rows),"columns":header}
        loaded[filename] = rows
    momentum, correlations, log_correlations = (
        loaded["figure3A_data.csv"], loaded["figure3B_data.csv"], loaded["figure3C_data.csv"])
    if min(map(len,(momentum,correlations,log_correlations))) < 100:
        raise AssertionError("unexpectedly small FFS figure dataset")
    series = {}
    for ell in (0,2,4):
        suffix=f"L{ell}"
        pairs=[p for p in _series_points(correlations,f"exp_x_{suffix}",f"exp_y_{suffix}") if p[0]>=0]
        xs,ys=[p[0] for p in pairs],[p[1] for p in pairs]
        crossings=first_zero_crossings(xs,ys)
        trough=_first_trough_between_crossings(xs,ys,crossings) if ell in (2,4) else None
        item={"measured_points":len(pairs),
            "zero_crossings_um":crossings[:4] if ell in (2,4) else [],
            "control_noise_floor_sign_changes_um":crossings[:4] if ell==0 else [],
            "first_oscillation_trough":trough}
        if ell in (2,4) and crossings:
            item["homogeneous_effective_kF_per_um"]=3.141592653589793/(ell*crossings[0])
            item["homogeneous_reference_only"]=True
        series[suffix]=item
    required=["exp_x_L0","exp_y_L0","sim_x_L0","sim_mean_L0",
        "exp_x_L2","exp_y_L2","sim_x_L2","sim_mean_L2",
        "exp_x_L4","exp_y_L4","sim_x_L4","sim_mean_L4"]
    missing=[key for key in required if key not in momentum[0]]
    if missing:
        raise AssertionError(f"figure3A missing required columns: {missing}")
    return {
        "dataset":"Zeng et al., Realization of fractional Fermi seas",
        "zenodo_record":"10.5281/zenodo.18697242","source_version":"v1",
        "published_utc":"2026-02-19","record_metadata_audit":metadata,
        "license":metadata["license"],
        "license_status":metadata["status"],
        "source_url":"https://zenodo.org/records/18697242",
        "files":files,
        "file_usage":{
            "figure3A_data.csv":"checksum/provenance plus required-column schema check; momentum-profile comparison not recomputed",
            "figure3B_data.csv":"experimental correlation columns used for zero-crossing and first-trough diagnostics; supplied error columns retained but not propagated",
            "figure3C_data.csv":"checksum/provenance only; log-correlation values are not analyzed in this run"},
        "correlation_diagnostics":series,
        "interpretation":"Measured figure data and GHD series are provenance-checked. Zero-crossing-derived kF values are effective homogeneous-sinc diagnostics only, not trap-corrected physical estimates.",
        "not_performed":["raw absorption-image reanalysis","GHD simulation reproduction","parameter fitting",
            "uncertainty propagation beyond supplied pointwise errors","causal V8 mapping"]}
    

if __name__ == "__main__":
    print(json.dumps(audit_zenodo_ffs_dataset(),indent=2,sort_keys=True))
