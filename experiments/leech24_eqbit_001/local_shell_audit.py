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

ROOT = Path(__file__).resolve().parents[1]
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


def local_relation_census(gram: np.ndarray, adjacency: np.ndarray) -> dict:
    """Exact pair census for the four nontrivial inner-product relations."""
    relation_dots = (16, 8, 0, -16)
    per_vertex = {
        str(dot): (gram == dot).sum(axis=1)
        for dot in relation_dots
    }
    valencies = {
        str(dot): {
            "min": int(values.min()),
            "max": int(values.max()),
            "value": int(values[0]),
        }
        for dot, values in ((d, per_vertex[str(d)]) for d in relation_dots)
    }
    if any(v["min"] != v["max"] for v in valencies.values()):
        raise AssertionError("local inner-product relation valencies vary by vertex")

    row_bits = []
    for row in adjacency:
        bits = 0
        for j in np.flatnonzero(row):
            bits |= 1 << int(j)
        row_bits.append(bits)

    pair_counts = Counter()
    common_counts = {str(dot): Counter() for dot in relation_dots}
    n = gram.shape[0]
    for i in range(n):
        left = row_bits[i]
        for j in range(i + 1, n):
            dot = int(gram[i, j])
            if dot not in relation_dots:
                raise AssertionError(f"unexpected off-diagonal dot product: {dot}")
            common = (left & row_bits[j]).bit_count()
            pair_counts[str(dot)] += 1
            common_counts[str(dot)][str(common)] += 1

    expected_pairs = {"16": 2049300, "8": 6476800, "0": 2049300, "-16": 2300}
    expected_common = {
        "16": {"336": 2049300},
        "8": {"162": 6476800},
        "0": {"42": 2049300},
        "-16": {"0": 2300},
    }
    actual_common = {
        dot: dict(sorted(counts.items(), key=lambda item: int(item[0])))
        for dot, counts in common_counts.items()
    }
    if dict(pair_counts) != expected_pairs:
        raise AssertionError(f"local relation pair counts mismatch: {dict(pair_counts)}")
    if actual_common != expected_common:
        raise AssertionError(f"local common-neighbor census mismatch: {actual_common}")

    return {
        "relation_partition": "identity plus four exact off-diagonal inner-product relations",
        "inner_product_units": "integer coordinate dot product; divide by 8 for lattice inner product",
        "per_vertex_valencies": valencies,
        "unordered_pair_counts": dict(pair_counts),
        "common_neighbor_counts_by_relation": actual_common,
        "strongly_regular": False,
        "interpretation": (
            "The adjacency relation alone is not strongly regular: nonadjacent "
            "pairs have three distinct common-neighbor counts. Full association-"
            "scheme closure has not yet been tested."
        ),
    }


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
        if family == "A":
            output["local_relation_census"] = local_relation_census(
                neighbor_gram, within
            )

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
