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


def local_relation_census(gram: np.ndarray, adjacency: np.ndarray) -> dict:
    """Verify the complete four-class association-scheme intersection table."""
    relation_dots = (16, 8, 0, -16)
    relation_mats = []
    valencies = {}
    for dot in relation_dots:
        matrix = gram == dot
        np.fill_diagonal(matrix, False)
        degrees = matrix.sum(axis=1)
        if int(degrees.min()) != int(degrees.max()):
            raise AssertionError(f"relation {dot} has nonconstant valency")
        valencies[str(dot)] = int(degrees[0])
        relation_mats.append(matrix)

    packed = [
        np.packbits(matrix, axis=1, bitorder="little")
        for matrix in relation_mats
    ]
    popcount = np.array([int(x).bit_count() for x in range(256)], dtype=np.uint8)
    table = {}
    for a, dot_a in enumerate(relation_dots):
        table[str(dot_a)] = {}
        for b, dot_b in enumerate(relation_dots):
            by_pair_class = {dot: set() for dot in relation_dots}
            for i in range(gram.shape[0] - 1):
                # Count both orientations of every unordered pair. This is
                # essential when i != j: symmetry of the relation matrices
                # alone does not establish p_ij^k == p_ji^k.
                forward = np.bitwise_and(packed[a][i], packed[b][i + 1:])
                reverse = np.bitwise_and(packed[a][i + 1:], packed[b][i])
                forward_counts = popcount[forward].sum(axis=1, dtype=np.uint16)
                reverse_counts = popcount[reverse].sum(axis=1, dtype=np.uint16)
                pair_dots = gram[i, i + 1:]
                # Reduce each relation class in NumPy rather than iterating
                # over every unordered vertex pair in Python.  The previous
                # scalar loop performed ~168M Python-level insertions per
                # local census and made this audit appear stalled for minutes.
                for pair_dot in relation_dots:
                    mask = pair_dots == pair_dot
                    if not np.any(mask):
                        raise AssertionError(
                            f"missing pair class {pair_dot} in local relation census"
                        )
                    f_values = forward_counts[mask]
                    r_values = reverse_counts[mask]
                    f_min, f_max = int(f_values.min()), int(f_values.max())
                    r_min, r_max = int(r_values.min()), int(r_values.max())
                    if f_min != f_max or r_min != r_max:
                        raise AssertionError(
                            f"intersection number varies for R{dot_a}*R{dot_b} "
                            f"on pair class {pair_dot}: "
                            f"forward=[{f_min},{f_max}], reverse=[{r_min},{r_max}]"
                        )
                    by_pair_class[pair_dot].add(f_min)
                    by_pair_class[pair_dot].add(r_min)
            if any(len(values) != 1 for values in by_pair_class.values()):
                raise AssertionError(
                    f"intersection number varies for R{dot_a}*R{dot_b}: "
                    f"{by_pair_class}"
                )
            table[str(dot_a)][str(dot_b)] = {
                str(pair_dot): next(iter(by_pair_class[pair_dot]))
                for pair_dot in relation_dots
            }

    if any(table[str(a)][str(b)] != table[str(b)][str(a)]
           for a in relation_dots for b in relation_dots):
        raise AssertionError("relation algebra is not commutative")

    # Exact simultaneous eigenvectors of the five-dimensional relation algebra.
    # Vector coordinates are [I, R16, R8, R0, R-16].
    eigenmatrix = [
        [891, 2816, 891, 1],
        [297, 0, -297, -1],
        [63, -128, 63, 1],
        [-9, 16, -9, 1],
        [-3, 0, 3, -1],
    ]
    multiplicities = [1, 23, 275, 2024, 2277]
    if sum(multiplicities) != gram.shape[0]:
        raise AssertionError("spectral multiplicities do not sum to 4600")

    # Multiplication operator M_i acts on relation-basis coefficient vectors.
    relation_basis = [None, *relation_dots]
    for relation_index, relation_dot in enumerate(relation_dots):
        multiplication = [[0] * 5 for _ in range(5)]
        multiplication[0][relation_index + 1] = 1  # A_i * I = A_i
        for row_index, other_dot in enumerate(relation_dots, start=1):
            multiplication[row_index][0] = (
                valencies[str(relation_dot)] if relation_dot == other_dot else 0
            )
            for column_index, target_dot in enumerate(relation_dots, start=1):
                multiplication[row_index][column_index] = table[str(relation_dot)][str(other_dot)][str(target_dot)]

        for eigenspace, eigenvalues in enumerate(eigenmatrix):
            vector = [1, *eigenvalues]
            eigenvalue = eigenvalues[relation_index]
            product = [
                sum(multiplication[row][column] * vector[column] for column in range(5))
                for row in range(5)
            ]
            if product != [eigenvalue * entry for entry in vector]:
                raise AssertionError(
                    f"spectral eigenvector mismatch for relation {relation_dot}, "
                    f"eigenspace {eigenspace}"
                )

    for relation_index in range(4):
        if sum(
            multiplicities[eigenspace] * eigenmatrix[eigenspace][relation_index]
            for eigenspace in range(5)
        ) != 0:
            raise AssertionError("spectral trace/multiplicity identity failed")

    # Diagonal coefficient p_ij^0: valency k_i when i=j, otherwise zero.
    diagonal = {
        str(a): {
            str(b): (valencies[str(a)] if a == b else 0)
            for b in relation_dots
        }
        for a in relation_dots
    }
    return {
        "status": "VERIFIED_FOUR_CLASS_SYMMETRIC_ASSOCIATION_SCHEME_FOR_REFERENCE",
        "relation_order": [str(dot) for dot in relation_dots],
        "per_vertex_valencies": valencies,
        "off_diagonal_intersection_numbers_p_ij_k": table,
        "diagonal_intersection_numbers_p_ij_0": diagonal,
        "commutative": True,
        "all_16_relation_products_have_constant_intersection_numbers": True,
        "simultaneous_eigenmatrix_rows_relation_order_16_8_0_minus16": eigenmatrix,
        "primitive_idempotent_multiplicities": multiplicities,
        "spectral_eigenvectors_verified_exactly_over_integers": True,
        "spectral_trace_identities_verified": True,
        "scope": (
            "Full all-pairs closure verified for this one reference neighborhood. "
            "Three-family common-neighbor census is separate; transport to every "
            "reference vector requires a Co0-transitivity argument or further tests."
        ),
    }


def global_association_scheme_audit(shell: np.ndarray, reference_index: int = 0,
                                    sample_count: int = 20) -> dict:
    """Audit all seven Leech-shell inner-product relations from representative pairs.

    For each relation class around a fixed reference, compare the complete
    7x7 joint inner-product table for several deterministic representatives.
    This is a reproducible finite audit, not a replacement for the published
    Co0 orbit-transitivity theorem.
    """
    relation_dots = (32, 16, 8, 0, -8, -16, -32)
    reference = shell[reference_index].astype(np.int32)
    reference_dots = shell.astype(np.int32) @ reference
    observed_histogram = Counter(map(int, reference_dots))
    expected_valencies = {
        32: 1, 16: 4600, 8: 47104, 0: 93150,
        -8: 47104, -16: 4600, -32: 1,
    }
    if dict(observed_histogram) != expected_valencies:
        raise AssertionError("global Leech shell relation valencies mismatch")

    relation_tables = {}
    representatives_checked = {}
    for target_dot in relation_dots:
        indices = np.flatnonzero(reference_dots == target_dot)
        if len(indices) == 1:
            chosen = indices
        else:
            count = min(sample_count, len(indices))
            chosen = indices[np.linspace(0, len(indices) - 1, count, dtype=int)]

        signatures = []
        for index in chosen:
            y_dots = shell.astype(np.int32) @ shell[int(index)].astype(np.int32)
            counts = Counter(zip(map(int, reference_dots), map(int, y_dots)))
            matrix = [
                [int(counts.get((left, right), 0)) for right in relation_dots]
                for left in relation_dots
            ]
            signatures.append(matrix)

        first = signatures[0]
        if any(matrix != first for matrix in signatures[1:]):
            raise AssertionError(
                f"global joint relation table varies for target dot {target_dot}"
            )
        if any(first[i][j] != first[j][i]
               for i in range(len(relation_dots))
               for j in range(len(relation_dots))):
            raise AssertionError("global intersection table is not symmetric")

        for row_index, row in enumerate(first):
            if sum(row) != expected_valencies[relation_dots[row_index]]:
                raise AssertionError("global intersection table row sum mismatch")
        relation_tables[str(target_dot)] = first
        representatives_checked[str(target_dot)] = len(chosen)

    # Exact first eigenmatrix, with columns ordered I, R16, R8, R0, R-8, R-16, R-32.
    eigenmatrix = [
        [1, 4600, 47104, 93150, 47104, 4600, 1],
        [1, 2300, 11776, 0, -11776, -2300, -1],
        [1, 1000, 1024, -4050, 1024, 1000, 1],
        [1, 350, -704, 0, 704, -350, -1],
        [1, 76, -320, 486, -320, 76, 1],
        [1, -10, 16, 0, -16, 10, -1],
        [1, -20, 64, -90, 64, -20, 1],
    ]
    multiplicities = [1, 24, 299, 2576, 17250, 95680, 80730]
    if sum(multiplicities) != shell.shape[0]:
        raise AssertionError("global primitive multiplicities do not sum to shell size")

    # Multiplication matrices M_i have row j, column k equal to p_{ij}^k.
    for relation_index, relation_dot in enumerate(relation_dots[1:], start=1):
        multiplication = [[0] * 7 for _ in range(7)]
        multiplication[0][relation_index] = 1
        for row_index, other_dot in enumerate(relation_dots[1:], start=1):
            multiplication[row_index][0] = (
                expected_valencies[relation_dot] if relation_dot == other_dot else 0
            )
            for column_index, target_dot in enumerate(relation_dots[1:], start=1):
                joint = relation_tables[str(target_dot)]
                multiplication[row_index][column_index] = joint[
                    relation_dots.index(relation_dot)
                ][relation_dots.index(other_dot)]
        for eigenspace, row in enumerate(eigenmatrix):
            product = [
                sum(multiplication[r][c] * row[c] for c in range(7))
                for r in range(7)
            ]
            eigenvalue = row[relation_index]
            if product != [eigenvalue * value for value in row]:
                raise AssertionError(
                    f"global eigenmatrix fails relation {relation_dot}, "
                    f"eigenspace {eigenspace}"
                )

    for relation_index in range(1, 7):
        if sum(multiplicities[i] * eigenmatrix[i][relation_index]
               for i in range(7)) != 0:
            raise AssertionError("global spectral trace identity failed")

    return {
        "status": "COMPUTED_GLOBAL_SEVEN_RELATION_SCHEME_AUDIT",
        "reference_index": reference_index,
        "relation_order_integer_dot": list(relation_dots),
        "valencies": {str(k): v for k, v in expected_valencies.items()},
        "representatives_checked_per_target_relation": representatives_checked,
        "all_sampled_joint_intersection_tables_identical_within_relation": True,
        "all_intersection_table_rows_sum_to_relation_valencies": True,
        "first_eigenmatrix_columns_I_16_8_0_minus8_minus16_minus32": eigenmatrix,
        "primitive_multiplicities": multiplicities,
        "multiplication_eigenvectors_verified_exactly": True,
        "spectral_trace_identities_verified": True,
        "adjacency_R16_eigenvalues": [row[1] for row in eigenmatrix],
        "scope": (
            "The finite code checks deterministic representatives from each "
            "inner-product class around one reference. Global uniformity is "
            "supported by the established Co0 orbit/association-scheme theory; "
            "this sample audit alone is not a proof of pair-orbit transitivity."
        ),
        "global_adjacency_matrix_materialized": False,
    }


def run() -> dict:
    shell = np.asarray(leech_minimal_vectors(), dtype=np.int8)
    if shell.shape != (196560, 24):
        raise AssertionError(f"unexpected Leech shell shape: {shell.shape}")
    if len({row.tobytes() for row in shell}) != 196560:
        raise AssertionError("minimal shell contains duplicate vectors")

    output = {
        "schema": "pan.leech24_local_eqbit_audit.v2",
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
            "antipodal_relation_matrix": "B[i,j] = 1 iff dot(N[i], N[j]) == -16",
            "gf2_rank": "packed-row exact XOR elimination",
            "global_adjacency_materialized": False,
        },
        "reference_results": {},
    }

    print("[local-shell] starting global seven-relation audit", file=sys.stderr, flush=True)
    output["global_association_scheme"] = global_association_scheme_audit(shell)
    print("[local-shell] global seven-relation audit complete", file=sys.stderr, flush=True)
    output["local_relation_censuses"] = {}

    for family, index in FAMILY_STARTS.items():
        print(f"[local-shell] starting family {family} reference {index}", file=sys.stderr, flush=True)
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

        # Genuine cut-rank: GF(2) rank of the bipartite adjacency block
        # across each construction-family partition of this local graph.
        neighbor_indices = np.flatnonzero(dots == 16)
        local_families = np.where(
            neighbor_indices < FAMILY_STARTS["B"], 0,
            np.where(neighbor_indices < FAMILY_STARTS["C"], 1, 2)
        )
        family_cut_ranks = {}
        for family_id, family_name in enumerate(("A", "B", "C")):
            left = np.flatnonzero(local_families == family_id)
            right = np.flatnonzero(local_families != family_id)
            cut_block = within[np.ix_(left, right)]
            family_cut_ranks[family_name] = {
                "partition_sizes": [int(len(left)), int(len(right))],
                "gf2_cut_rank": gf2_rank_bool(cut_block),
                "cut_matrix_shape": [int(len(left)), int(len(right))],
            }

        # Exact common-neighbor census for every unordered pair in N(r).
        # Packed row intersections avoid a cubic dense matrix multiplication.
        packed_within = np.packbits(within, axis=1, bitorder="little")
        popcount = np.array([int(x).bit_count() for x in range(256)], dtype=np.uint8)
        common_counts: dict[int, Counter] = {}
        for i in range(len(neighbors) - 1):
            intersections = np.bitwise_and(packed_within[i], packed_within[i + 1:])
            counts = popcount[intersections].sum(axis=1, dtype=np.uint16)
            pair_dots = neighbor_gram[i, i + 1:]
            for dot, count in zip(pair_dots.tolist(), counts.tolist()):
                common_counts.setdefault(int(dot), Counter())[int(count)] += 1

        expected_pair_classes = {
            -16: {0: 2300},
            0: {42: 2049300},
            8: {162: 6476800},
            16: {336: 2049300},
        }
        observed_pair_classes = {
            dot: dict(sorted(counter.items()))
            for dot, counter in sorted(common_counts.items())
        }
        if observed_pair_classes != expected_pair_classes:
            raise AssertionError(
                f"{family}: common-neighbor census mismatch: {observed_pair_classes}"
            )

        histogram_bytes = json.dumps(
            histogram, sort_keys=True, separators=(",", ":")
        ).encode()
        # Run the complete 4-class closure/spectral audit independently for
        # every deterministic construction-family representative. Do not
        # infer B/C from A or silently promote a sampled census to a proof.
        output["local_relation_censuses"][family] = local_relation_census(
            neighbor_gram, within
        )
        if family == "A":
            # Backward-compatible alias for consumers of the v1 result shape.
            output["local_relation_census"] = output["local_relation_censuses"][family]

        print(f"[local-shell] family {family} complete", file=sys.stderr, flush=True)
        output["reference_results"][family] = {
            "reference_index": index,
            "reference_vector": shell[index].astype(int).tolist(),
            "inner_product_histogram_integer_dot": histogram,
            "histogram_sha256": sha256_bytes(histogram_bytes),
            "neighbor_count": int(len(neighbors)),
            "construction_family_cut_ranks": family_cut_ranks,
            "antipodal_relation": {
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
                "common_neighbor_census_by_integer_dot": {
                    str(dot): {str(count): pairs for count, pairs in sorted(counter.items())}
                    for dot, counter in sorted(common_counts.items())
                },
                "is_strongly_regular": False,
                "distinct_nonadjacent_common_neighbor_counts": [0, 42, 162],
            },
        }

    output["acceptance"] = {
        "three_family_shell_censuses_match": True,
        "all_local_shells_have_4600_neighbors": True,
        "all_antipodal_relations_are_fixed_point_free_perfect_matchings": True,
        "all_antipodal_relation_matrix_ranks_are_full_4600": True,
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
