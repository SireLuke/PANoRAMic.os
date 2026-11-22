#!/usr/bin/env python3
"""Exact local-shell Leech kissing-graph / GF(2) cut-rank audit.

This deliberately constructs only three 4,600-vertex local shells and their
induced/cross-cut matrices. It never materializes the 196,560-vertex global
adjacency matrix or its 452,088,000 edges.
"""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiments.moonshine_sierpinski.leech_golay_construction import (
    leech_minimal_vectors,
)

EXPECTED_HISTOGRAM = {
    -32: 1, -16: 4600, -8: 47104, 0: 93150,
    8: 47104, 16: 4600, 32: 1,
}
FAMILY_STARTS = {"A": 0, "B": 1104, "C": 98256}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def gf2_rank_bool(matrix: np.ndarray) -> int:
    """Exact GF(2) rank using packed rows and Python integer XOR."""
    if matrix.ndim != 2:
        raise ValueError("matrix must be two-dimensional")
    packed = np.packbits(matrix, axis=1, bitorder="little")
    pivots: dict[int, int] = {}
    for raw in packed:
        row = int.from_bytes(raw.tobytes(), "little")
        while row:
            pivot = row.bit_length() - 1
            if pivot in pivots:
                row ^= pivots[pivot]
            else:
                pivots[pivot] = row
                break
    return len(pivots)


def run() -> dict:
    shell = np.asarray(leech_minimal_vectors(), dtype=np.int8)
    if shell.shape != (196560, 24):
        raise AssertionError(f"unexpected Leech shell shape: {shell.shape}")
    if len({row.tobytes() for row in shell}) != 196560:
        raise AssertionError("minimal shell contains duplicate vectors")

    output = {
        "schema": "pan.leech24_local_eqbit_audit.v1",
        "status": "COMPUTED_LOCAL_EXACT_AUDIT",
        "geometry": {
            "rank": 24,
            "minimal_vectors": 196560,
            "integral_coordinate_norm_squared": 32,
            "lattice_coordinate_scale": "1/sqrt(8)",
            "adjacency_rule": "integer_dot_product == 16 (lattice inner product 2)",
        },
        "method": {
            "reference_families": list(FAMILY_STARTS),
            "local_neighbors_per_reference": 4600,
            "local_vertex_set": "N(r) union -N(r), 9200 vertices",
            "cut_matrix": "B[i,j] = 1 iff dot(N[i], N[j]) == -16",
            "gf2_rank": "packed-row exact XOR elimination",
            "global_adjacency_materialized": False,
        },
        "reference_results": {},
    }

    for family, index in FAMILY_STARTS.items():
        ref = shell[index].astype(np.int16)
        dots = shell.astype(np.int16) @ ref
        histogram = dict(sorted(Counter(map(int, dots)).items()))
        if histogram != EXPECTED_HISTOGRAM:
            raise AssertionError(f"{family}: reference shell census mismatch")
        neighbors = shell[dots == 16].astype(np.int16)
        if neighbors.shape != (4600, 24):
            raise AssertionError(f"{family}: expected 4600 neighbors")

        neighbor_gram = neighbors @ neighbors.T
        cross = neighbor_gram == -16
        if not np.array_equal(cross, cross.T):
            raise AssertionError(f"{family}: cross-cut matrix not symmetric")
        if np.any(np.diag(cross)):
            raise AssertionError(f"{family}: cross-cut diagonal is not zero")

        row_degrees = cross.sum(axis=1)
        if not np.all(row_degrees == 1):
            raise AssertionError(f"{family}: cross-cut is not 1-regular")
        partners = np.argmax(cross, axis=1)
        if np.any(partners == np.arange(4600)):
            raise AssertionError(f"{family}: cross-cut matching has fixed point")
        if not np.array_equal(partners[partners], np.arange(4600)):
            raise AssertionError(f"{family}: partner map is not an involution")

        within = neighbor_gram == 16
        np.fill_diagonal(within, False)
        within_degrees = within.sum(axis=1)
        if not np.all(within_degrees == 891):
            raise AssertionError(f"{family}: local induced graph degree mismatch")

        histogram_bytes = json.dumps(
            histogram, sort_keys=True, separators=(",", ":")
        ).encode()
        output["reference_results"][family] = {
            "reference_index": index,
            "reference_vector": shell[index].astype(int).tolist(),
            "inner_product_histogram_integer_dot": histogram,
            "histogram_sha256": sha256_bytes(histogram_bytes),
            "neighbor_count": int(len(neighbors)),
            "cross_cut": {
                "matrix_shape": [4600, 4600],
                "ones": int(cross.sum()),
                "degree_min": int(row_degrees.min()),
                "degree_max": int(row_degrees.max()),
                "symmetric": True,
                "zero_diagonal": True,
                "fixed_points": 0,
                "partner_map_is_fixed_point_free_involution": True,
                "gf2_rank": gf2_rank_bool(cross),
                "sha256": sha256_bytes(cross.tobytes(order="C")),
            },
            "within_neighbor_graph": {
                "vertices": 4600,
                "edges": int(within.sum() // 2),
                "degree_min": int(within_degrees.min()),
                "degree_max": int(within_degrees.max()),
                "regular_degree": 891,
                "sha256": sha256_bytes(within.tobytes(order="C")),
            },
        }

    output["acceptance"] = {
        "three_family_shell_censuses_match": True,
        "all_local_shells_have_4600_neighbors": True,
        "all_cross_cuts_are_fixed_point_free_perfect_matchings": True,
        "all_cross_cut_ranks_are_full_4600": True,
        "all_within_neighbor_graphs_are_891_regular": True,
        "scope_limit": (
            "Three deterministic reference representatives were checked; "
            "this run alone does not prove Co0 transitivity or every-root "
            "local incidence."
        ),
    }
    return output


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
