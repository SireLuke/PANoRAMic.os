#!/usr/bin/env python3
"""
PAN V8 Validation Harness
=========================

Exploratory, reproducible analysis for reviewer-level V8 feature scores.

Input CSV columns (one row per system/reviewer):
    system_id,split,reviewer_id,h,R,u,d,tau,chi,s,f

Optional:
    P_time

Allowed split values: development, blind
Coordinate values should be numeric or blank. Blank values remain missing; they
are not silently imputed as zero.

Dependencies:
    pip install pandas numpy scikit-learn

Example:
    python pan_v8_validation_harness.py reviewer_scores.csv --out results

Important:
- Fit scaling and K-means on development rows/systems only.
- Blind rows are assigned to frozen development centroids; they do not refit.
- This is an exploratory harness, not evidence that V8 is universal or that
  UH/UDFE is a validated physical law.
- For rigorous reviewer agreement, preregister an appropriate ICC/ordinal
  statistic and confidence interval; the agreement summary here is descriptive.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import (
    adjusted_rand_score,
    davies_bouldin_score,
    silhouette_score,
)
from sklearn.preprocessing import StandardScaler

COORDS = ["h", "R", "u", "d", "tau", "chi", "s", "f"]
REQUIRED = ["system_id", "split", "reviewer_id", *COORDS]
VALID_SPLITS = {"development", "blind"}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("csv", type=Path, help="Reviewer-level score CSV")
    p.add_argument("--out", type=Path, default=Path("pan_v8_results"))
    p.add_argument("--k-min", type=int, default=2)
    p.add_argument("--k-max", type=int, default=6)
    p.add_argument("--bootstraps", type=int, default=100)
    p.add_argument("--seed", type=int, default=20261026)
    return p.parse_args()


def load_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, comment="#")
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    df = df.copy()
    df["system_id"] = df["system_id"].astype(str).str.strip()
    df["reviewer_id"] = df["reviewer_id"].astype(str).str.strip()
    df["split"] = df["split"].astype(str).str.strip().str.lower()
    df = df[(df["system_id"] != "") & (df["reviewer_id"] != "")]
    if not set(df["split"].dropna()).issubset(VALID_SPLITS):
        raise ValueError(f"split must contain only {sorted(VALID_SPLITS)}")
    for c in COORDS + (["P_time"] if "P_time" in df.columns else []):
        df[c] = pd.to_numeric(df[c], errors="coerce")
    if df.empty:
        raise ValueError("No usable data rows found.")
    # A system must belong to exactly one split, avoiding train/blind leakage.
    split_counts = df.groupby("system_id")["split"].nunique()
    bad = split_counts[split_counts > 1].index.tolist()
    if bad:
        raise ValueError(f"Systems appear in multiple splits: {bad}")
    return df


def reviewer_summary(df: pd.DataFrame) -> dict[str, Any]:
    system_means = df.groupby(["split", "system_id"])[COORDS].mean()
    reviewer_counts = df.groupby(["split", "system_id"])["reviewer_id"].nunique()
    coordinate_summary = {}
    for c in COORDS:
        coordinate_summary[c] = {
            "n": int(df[c].notna().sum()),
            "missing_fraction": float(df[c].isna().mean()),
            "mean": None if df[c].notna().sum() == 0 else float(df[c].mean()),
            "std": None if df[c].notna().sum() < 2 else float(df[c].std()),
        }
    return {
        "rows": int(len(df)),
        "systems": int(df["system_id"].nunique()),
        "reviewers": int(df["reviewer_id"].nunique()),
        "systems_by_split": {
            str(k): int(v) for k, v in df.groupby("split")["system_id"].nunique().items()
        },
        "reviewers_per_system": {
            "min": int(reviewer_counts.min()),
            "median": float(reviewer_counts.median()),
            "max": int(reviewer_counts.max()),
        },
        "coordinate_summary": coordinate_summary,
        "system_mean_preview": system_means.reset_index().head(30).to_dict(orient="records"),
        "note": "Descriptive summaries only; reviewer means are not proof of inter-rater reliability.",
    }


def make_system_matrix(df: pd.DataFrame, split: str) -> tuple[pd.Index, pd.DataFrame]:
    subset = df[df["split"] == split]
    means = subset.groupby("system_id")[COORDS].mean()
    # Do not invent scores for missing coordinates. Median imputation is fitted
    # on development systems and explicitly reported as an analysis choice.
    return means.index, means


def prepare_development(
    dev_means: pd.DataFrame,
) -> tuple[pd.Index, np.ndarray, StandardScaler, np.ndarray, list[str]]:
    usable = dev_means.dropna(axis=1, how="all")
    active_coords = usable.columns.tolist()
    if len(active_coords) < 2:
        raise ValueError("Need at least two coordinates with development data.")
    medians = usable.median(axis=0)
    X = usable.fillna(medians).to_numpy(dtype=float)
    if X.shape[0] < 3:
        raise ValueError("Need at least three development systems for clustering diagnostics.")
    scaler = StandardScaler()
    Xs = scaler.fit_transform(X)
    return usable.index, Xs, scaler, medians.to_numpy(dtype=float), active_coords


def cluster_diagnostics(
    X: np.ndarray, k_min: int, k_max: int, bootstraps: int, seed: int
) -> tuple[list[dict[str, Any]], dict[int, KMeans]]:
    n = X.shape[0]
    reports: list[dict[str, Any]] = []
    models: dict[int, KMeans] = {}
    max_k = min(k_max, n - 1)
    for k in range(max(2, k_min), max_k + 1):
        model = KMeans(n_clusters=k, n_init=20, random_state=seed)
        labels = model.fit_predict(X)
        if len(np.unique(labels)) < 2:
            continue
        sil = float(silhouette_score(X, labels))
        db = float(davies_bouldin_score(X, labels))
        rng = np.random.default_rng(seed + k)
        stability = []
        for b in range(max(0, bootstraps)):
            # Resample systems, fit on sampled rows, then compare assignments on
            # the full development set. This is a rough stability diagnostic,
            # not a formal confidence interval.
            idx = rng.integers(0, n, size=n)
            if len(np.unique(idx)) < k:
                continue
            boot_model = KMeans(n_clusters=k, n_init=10, random_state=seed + b + k)
            boot_model.fit(X[idx])
            boot_labels = boot_model.predict(X)
            stability.append(float(adjusted_rand_score(labels, boot_labels)))
        reports.append({
            "k": int(k),
            "silhouette": sil,
            "davies_bouldin": db,
            "bootstrap_ari_mean": None if not stability else float(np.mean(stability)),
            "bootstrap_ari_sd": None if len(stability) < 2 else float(np.std(stability, ddof=1)),
            "cluster_sizes": {str(int(i)): int(np.sum(labels == i)) for i in np.unique(labels)},
        })
        models[k] = model
    return reports, models


def main() -> int:
    args = parse_args()
    if args.k_min < 2 or args.k_max < args.k_min:
        raise ValueError("Require 2 <= k-min <= k-max.")
    df = load_data(args.csv)
    args.out.mkdir(parents=True, exist_ok=True)

    summary = reviewer_summary(df)
    (args.out / "summary.json").write_text(
        json.dumps(summary, indent=2, allow_nan=False), encoding="utf-8"
    )

    dev_ids, dev_means = make_system_matrix(df, "development")
    blind_ids, blind_means = make_system_matrix(df, "blind")
    ids, X_dev, scaler, medians, active_coords = prepare_development(dev_means[COORDS])

    # Rebuild dev and blind feature matrices using only development medians and
    # the development-fitted scaler. Coordinates entirely missing in dev are
    # excluded from all subsequent analyses.
    dev_raw = dev_means.loc[ids, active_coords].fillna(
        pd.Series(medians, index=active_coords)
    ).to_numpy(dtype=float)
    X_dev = scaler.transform(dev_raw)

    pca = PCA(random_state=args.seed)
    pca.fit(X_dev)
    pca_report = {
        "coordinates_used": active_coords,
        "explained_variance_ratio": pca.explained_variance_ratio_.tolist(),
        "cumulative_explained_variance_ratio": np.cumsum(pca.explained_variance_ratio_).tolist(),
        "interpretation": "Descriptive only; PCA loadings do not establish causal importance.",
    }
    (args.out / "pca.json").write_text(
        json.dumps(pca_report, indent=2, allow_nan=False), encoding="utf-8"
    )

    diagnostics, models = cluster_diagnostics(
        X_dev, args.k_min, args.k_max, args.bootstraps, args.seed
    )
    (args.out / "cluster_diagnostics.json").write_text(
        json.dumps(diagnostics, indent=2, allow_nan=False), encoding="utf-8"
    )

    # Use the best silhouette only as a convenience for exploratory assignment.
    # The chosen k must be preregistered for confirmatory use.
    if diagnostics:
        chosen = max(diagnostics, key=lambda row: row["silhouette"])["k"]
        model = models[chosen]
        dev_labels = model.predict(X_dev)
        dev_out = pd.DataFrame({
            "system_id": ids.astype(str),
            "split": "development",
            "cluster": dev_labels.astype(int),
            "distance_to_centroid": [
                float(np.linalg.norm(X_dev[i] - model.cluster_centers_[dev_labels[i]]))
                for i in range(len(ids))
            ],
        })
        dev_out.to_csv(args.out / "development_assignments.csv", index=False)

        if not blind_means.empty:
            blind_use = blind_means.reindex(columns=active_coords)
            blind_missing = blind_use.isna().any(axis=1)
            blind_raw = blind_use.fillna(pd.Series(medians, index=active_coords)).to_numpy(dtype=float)
            X_blind = scaler.transform(blind_raw)
            blind_labels = model.predict(X_blind)
            distances = np.array([
                np.linalg.norm(X_blind[i] - model.cluster_centers_[blind_labels[i]])
                for i in range(len(blind_ids))
            ])
            # Conservative, explicit heuristic: flag distances above the 95th
            # percentile of development distances. Not a calibrated OOD test.
            dev_dist = dev_out["distance_to_centroid"].to_numpy()
            cutoff = float(np.quantile(dev_dist, 0.95))
            pd.DataFrame({
                "system_id": blind_ids.astype(str),
                "split": "blind",
                "cluster": blind_labels.astype(int),
                "distance_to_centroid": distances,
                "ood_heuristic": distances > cutoff,
                "had_missing_coordinates": blind_missing.to_numpy(),
            }).to_csv(args.out / "blind_assignments.csv", index=False)
            assignment_meta = {
                "exploratory_selected_k": int(chosen),
                "selection_rule": "maximum development silhouette; exploratory only",
                "development_distance_95th_percentile": cutoff,
                "ood_rule": "distance exceeds development 95th percentile; heuristic only",
                "warning": "For confirmatory testing, preregister k and OOD threshold before blind data are inspected.",
            }
            (args.out / "assignment_metadata.json").write_text(
                json.dumps(assignment_meta, indent=2, allow_nan=False), encoding="utf-8"
            )

    print(f"Completed exploratory analysis. Results: {args.out.resolve()}")
    print("Read the JSON reports and confirm that the split/rubric was frozen before interpreting clusters.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)
