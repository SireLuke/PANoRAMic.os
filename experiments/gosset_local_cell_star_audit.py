#!/usr/bin/env python3
"""Exact local cell-star audit for the E8 / Gosset 4_21 vertex figure.

Standard-library only. Reconstructs the two facet orbits of 4_21, the
incident 8-simplex and 8-orthoplex cells, the norm-four opposite-vertex
shell, and pairing of every cell facet containing the chosen origin.
"""
from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from itertools import combinations, product
import json


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def build_e8_roots():
    roots = []
    for i, j in combinations(range(8), 2):
        for si, sj in product((-1, 1), repeat=2):
            v = [Q(0)] * 8
            v[i], v[j] = Q(si), Q(sj)
            roots.append(tuple(v))
    for signs in product((-Q(1, 2), Q(1, 2)), repeat=8):
        if sum(x < 0 for x in signs) % 2 == 0:
            roots.append(tuple(signs))
    assert len(roots) == len(set(roots)) == 240
    assert all(dot(r, r) == 2 for r in roots)
    return roots


def simple_roots():
    return [
        tuple(map(Q, [Q(1, 2), Q(-1, 2), Q(-1, 2), Q(-1, 2),
                      Q(-1, 2), Q(-1, 2), Q(-1, 2), Q(1, 2)])),
        tuple(map(Q, [1, 1, 0, 0, 0, 0, 0, 0])),
        tuple(map(Q, [-1, 1, 0, 0, 0, 0, 0, 0])),
        tuple(map(Q, [0, -1, 1, 0, 0, 0, 0, 0])),
        tuple(map(Q, [0, 0, -1, 1, 0, 0, 0, 0])),
        tuple(map(Q, [0, 0, 0, -1, 1, 0, 0, 0])),
        tuple(map(Q, [0, 0, 0, 0, -1, 1, 0, 0])),
        tuple(map(Q, [0, 0, 0, 0, 0, -1, 1, 0])),
    ]


def solve_exact(matrix, rhs):
    n = len(matrix)
    work = [list(map(Q, row)) + [Q(value)]
            for row, value in zip(matrix, rhs)]
    for col in range(n):
        pivot_row = next(row for row in range(col, n)
                         if work[row][col] != 0)
        work[col], work[pivot_row] = work[pivot_row], work[col]
        pivot = work[col][col]
        work[col] = [value / pivot for value in work[col]]
        for row in range(n):
            if row == col:
                continue
            factor = work[row][col]
            work[row] = [
                value - factor * pivot_value
                for value, pivot_value in zip(work[row], work[col])
            ]
    return tuple(work[i][-1] for i in range(n))


def reflect(vector, root):
    coefficient = dot(vector, root)
    return tuple(x - coefficient * a for x, a in zip(vector, root))


def facet_orbit(seed, reflection_maps):
    seen = {seed}
    frontier = [seed]
    while frontier:
        following = []
        for facet in frontier:
            for mapping in reflection_maps:
                image = frozenset(mapping[index] for index in facet)
                if image not in seen:
                    seen.add(image)
                    following.append(image)
        frontier = following
    return seen


def squared_distance(a, b):
    return sum((x - y) ** 2 for x, y in zip(a, b))


def is_e8_lattice_vector(vector):
    if all(x.denominator == 1 for x in vector):
        return int(sum(vector)) % 2 == 0
    if all(x.denominator == 2 for x in vector):
        return int(sum(vector)) % 2 == 0
    return False


def norm_four_shell():
    shell = set()
    integer_values = (Q(-2), Q(-1), Q(0), Q(1), Q(2))
    half_values = (Q(-3, 2), Q(-1, 2), Q(1, 2), Q(3, 2))
    for vector in product(integer_values, repeat=8):
        if sum(x * x for x in vector) == 4 and int(sum(vector)) % 2 == 0:
            shell.add(vector)
    for vector in product(half_values, repeat=8):
        if sum(x * x for x in vector) == 4 and int(sum(vector)) % 2 == 0:
            shell.add(vector)
    return shell



def build_cell_adjacency(cell_star):
    """Build exact codimension-one adjacency for the finite origin star.

    Cells are represented by exact E8 coordinates. Every cell facet is
    keyed by its sorted global vertex IDs, so equality is exact and
    independent of traversal order.
    """
    cells = sorted(cell_star)
    all_vertices = sorted({vertex for cell in cells for vertex in cell})
    vertex_id = {vertex: index for index, vertex in enumerate(all_vertices)}
    cell_vertex_ids = [
        frozenset(vertex_id[vertex] for vertex in cell) for cell in cells
    ]
    cell_types = ["simplex" if len(cell) == 9 else "orthoplex" for cell in cells]
    facet_to_cells = {}
    facet_type_counts = Counter()

    for cell_id, cell in enumerate(cells):
        facets = []
        if len(cell) == 9:
            for omitted in range(9):
                facets.append(tuple(cell[j] for j in range(9) if j != omitted))
        elif len(cell) == 16:
            remaining = set(cell)
            opposite_pairs = []
            while remaining:
                first = min(remaining)
                matches = [
                    candidate for candidate in remaining
                    if candidate != first
                    and squared_distance(first, candidate) == 4
                ]
                assert len(matches) == 1
                second = matches[0]
                opposite_pairs.append((first, second))
                remaining.remove(first)
                remaining.remove(second)
            assert len(opposite_pairs) == 8
            for choices in product((0, 1), repeat=8):
                facets.append(tuple(
                    opposite_pairs[k][choices[k]] for k in range(8)
                ))
        else:
            raise AssertionError(f"Unexpected cell vertex count: {len(cell)}")

        expected_facets = 9 if len(cell) == 9 else 256
        assert len(facets) == expected_facets
        for facet in facets:
            assert len(facet) == 8
            assert all(
                squared_distance(a, b) == 2
                for a, b in combinations(facet, 2)
            )
            key = tuple(sorted(vertex_id[vertex] for vertex in facet))
            facet_to_cells.setdefault(key, []).append(cell_id)
            facet_type_counts[cell_types[cell_id]] += 1

    multiplicities = Counter(len(owners) for owners in facet_to_cells.values())
    assert all(multiplicity in (1, 2) for multiplicity in multiplicities)
    adjacency = {}
    pair_facet_counts = Counter()
    origin_vertex_id = vertex_id[(Q(0),) * 8]
    origin_facet_counts = Counter()
    nonorigin_facet_counts = Counter()
    shared_by_cell_type = Counter()

    for facet, owners in facet_to_cells.items():
        if origin_vertex_id in facet:
            origin_facet_counts[len(owners)] += 1
        else:
            nonorigin_facet_counts[len(owners)] += 1
        if len(owners) == 2:
            a, b = sorted(owners)
            pair = (a, b)
            pair_facet_counts[pair] += 1
            shared_vertices = cell_vertex_ids[a].intersection(cell_vertex_ids[b])
            assert shared_vertices == frozenset(facet)
            shared_by_cell_type[tuple(sorted((cell_types[a], cell_types[b])))] += 1
            adjacency.setdefault(a, set()).add(b)
            adjacency.setdefault(b, set()).add(a)

    assert all(count == 2 for count in origin_facet_counts)
    assert max(pair_facet_counts.values(), default=0) == 1
    degree_counts = Counter(len(adjacency.get(cell_id, ())) for cell_id in range(len(cells)))
    return {
        "cell_count": len(cells),
        "vertex_count": len(all_vertices),
        "facet_incidence_count": sum(facet_type_counts.values()),
        "distinct_facets": len(facet_to_cells),
        "facet_multiplicity_counts": dict(sorted(multiplicities.items())),
        "origin_containing_facets": {
            "multiplicity_counts": dict(sorted(origin_facet_counts.items())),
            "all_paired": all(count == 2 for count in origin_facet_counts),
        },
        "facets_not_containing_origin": {
            "multiplicity_counts": dict(sorted(nonorigin_facet_counts.items())),
        },
        "shared_facet_adjacencies": sum(len(v) for v in adjacency.values()) // 2,
        "shared_facet_pairings_by_cell_type": {
            "+".join(k): v for k, v in sorted(shared_by_cell_type.items())
        },
        "cell_adjacency_degree_distribution": dict(sorted(degree_counts.items())),
        "maximum_facets_shared_by_cell_pair": max(pair_facet_counts.values(), default=0),
        "every_shared_facet_is_exact_cell_intersection": True,
        "scope": (
            "Exact codimension-one adjacency among cells in the finite origin star. "
            "Singleton facets are boundary facets relative to this finite star; "
            "they may be paired by cells outside the star."
        ),
    }


def run_audit():
    roots = build_e8_roots()
    simple = simple_roots()
    root_index = {root: index for index, root in enumerate(roots)}
    # Fundamental weights satisfy alpha_i . omega_j = delta_ij.
    # The simple-root coordinate rows form the linear system directly;
    # using the Cartan Gram matrix here would instead solve for coefficients
    # in the simple-root basis and is not the same Euclidean vector.
    weights = [
        solve_exact(simple, [Q(int(i == j)) for i in range(8)])
        for j in range(8)
    ]
    reflection_maps = [
        [root_index[reflect(root, alpha)] for root in roots]
        for alpha in simple
    ]

    seed_facets = {}
    for node in (0, 1):
        values = [dot(root, weights[node]) for root in roots]
        support_value = max(values)
        seed_facets[node] = frozenset(
            index for index, value in enumerate(values)
            if value == support_value
        )
    orthoplex_facets = facet_orbit(seed_facets[0], reflection_maps)
    simplex_facets = facet_orbit(seed_facets[1], reflection_maps)
    assert len(seed_facets[0]) == 14
    assert len(seed_facets[1]) == 8
    assert len(orthoplex_facets) == 2160
    assert len(simplex_facets) == 17280

    zero = (Q(0),) * 8
    simplex_face_incidence = Counter()
    cell_star = set()
    for facet in simplex_facets:
        cell = (zero,) + tuple(roots[i] for i in sorted(facet))
        cell_star.add(tuple(sorted(cell)))
        assert len(cell) == 9
        assert all(squared_distance(a, b) == 2
                   for a, b in combinations(cell, 2))
        # Every cell facet containing the origin omits one nonzero vertex.
        for omit in range(1, 9):
            simplex_face_incidence[
                tuple(sorted(cell[j] for j in range(9) if j != omit))
            ] += 1

    opposite_vertices = set()
    orthoplex_face_incidence = Counter()
    for facet in orthoplex_facets:
        facet_vertices = [roots[i] for i in sorted(facet)]
        assert len(facet_vertices) == 14
        centroid = tuple(
            sum((v[k] for v in facet_vertices), Q(0)) / 14
            for k in range(8)
        )
        opposite = tuple(2 * x for x in centroid)
        assert is_e8_lattice_vector(opposite)
        assert sum(x * x for x in opposite) == 4
        opposite_vertices.add(opposite)

        cell = (zero,) + tuple(facet_vertices) + (opposite,)
        cell_star.add(tuple(sorted(cell)))
        distances = Counter(
            squared_distance(a, b) for a, b in combinations(cell, 2)
        )
        assert distances == Counter({Q(2): 112, Q(4): 8})

        # The 14 facet vertices form seven opposite pairs in this cell.
        remaining = set(facet_vertices)
        opposite_pairs = []
        while remaining:
            first = min(remaining)
            matches = [
                candidate for candidate in remaining
                if candidate != first
                and squared_distance(first, candidate) == 4
            ]
            assert len(matches) == 1
            second = matches[0]
            opposite_pairs.append((first, second))
            remaining.remove(first)
            remaining.remove(second)
        assert len(opposite_pairs) == 7
        center = tuple(x / 2 for x in opposite)
        assert all(squared_distance(vertex, center) == 1 for vertex in cell)
        assert all(
            tuple((a[k] + b[k]) / 2 for k in range(8)) == center
            for a, b in opposite_pairs
        )

        # An 8-orthoplex facet containing the origin chooses one vertex
        # from each of the seven other opposite pairs.
        for choices in product((0, 1), repeat=7):
            face = (zero,) + tuple(
                opposite_pairs[k][choices[k]] for k in range(7)
            )
            orthoplex_face_incidence[tuple(sorted(face))] += 1

    norm4 = norm_four_shell()
    assert len(opposite_vertices) == len(norm4) == 2160
    assert opposite_vertices == norm4

    # Build the complete codimension-one adjacency graph of this finite star.
    adjacency_audit = build_cell_adjacency(cell_star)
    assert adjacency_audit["cell_count"] == 19440
    assert adjacency_audit["origin_containing_facets"]["all_paired"]

    # Re-root closure: for every cell C in the origin star and every
    # non-origin vertex v of C, translate C by -v. The translated cell
    # must also occur in the origin star. This checks that overlapping
    # neighboring vertex stars agree on every cell they share.
    reroot_checks = 0
    reroot_failures = []
    neighbor_vertices = set()
    vertex_cell_degree = Counter(
        vertex for cell_key in cell_star for vertex in cell_key
    )
    for cell_key in cell_star:
        for vertex in cell_key:
            if vertex == zero:
                continue
            neighbor_vertices.add(vertex)
            translated = tuple(sorted(
                tuple(point[k] - vertex[k] for k in range(8))
                for point in cell_key
            ))
            reroot_checks += 1
            if translated not in cell_star:
                if len(reroot_failures) < 5:
                    reroot_failures.append({
                        "vertex": [str(x) for x in vertex],
                        "cell": [[str(x) for x in point] for point in cell_key],
                    })
    assert not reroot_failures
    assert len(neighbor_vertices) == 240 + 2160
    neighbor_norms = Counter(sum(x * x for x in v) for v in neighbor_vertices)
    assert neighbor_norms == Counter({Q(2): 240, Q(4): 2160})
    root_degrees = {
        vertex_cell_degree[v] for v in neighbor_vertices
        if sum(x * x for x in v) == 2
    }
    norm4_degrees = {
        vertex_cell_degree[v] for v in neighbor_vertices
        if sum(x * x for x in v) == 4
    }
    assert root_degrees == {702}
    assert norm4_degrees == {1}

    combined = simplex_face_incidence + orthoplex_face_incidence
    multiplicities = Counter(combined.values())
    orthoplex_multiplicities = Counter(orthoplex_face_incidence.values())
    simplex_multiplicities = Counter(simplex_face_incidence.values())
    cross_type_facets = set(simplex_face_incidence).intersection(
        orthoplex_face_incidence
    )
    assert multiplicities == Counter({2: 207360})
    assert len(simplex_face_incidence) == 138240
    assert simplex_multiplicities == Counter({1: 138240})
    assert len(orthoplex_face_incidence) == 207360
    assert orthoplex_multiplicities == Counter({1: 138240, 2: 69120})
    assert len(cross_type_facets) == 138240
    assert len(combined) == 207360

    return {
        "status": "PASS",
        "arithmetic": "exact rational",
        "e8_roots": len(roots),
        "gosset_facets": {
            "7_orthoplex": len(orthoplex_facets),
            "7_simplex": len(simplex_facets),
        },
        "incident_cells": {
            "8_orthoplex": len(orthoplex_facets),
            "8_simplex": len(simplex_facets),
            "total": len(orthoplex_facets) + len(simplex_facets),
        },
        "opposite_vertex_shell": {
            "constructed_vertices": len(opposite_vertices),
            "independent_norm4_shell": len(norm4),
            "exact_set_equality": opposite_vertices == norm4,
        },
        "cell_metric_checks": {
            "simplex_pairs_per_cell": 36,
            "simplex_pair_squared_distance": 2,
            "orthoplex_edge_pairs_per_cell": 112,
            "orthoplex_edge_squared_distance": 2,
            "orthoplex_opposite_pairs_per_cell": 8,
            "orthoplex_opposite_squared_distance": 4,
            "orthoplex_common_center_and_unit_circumradius": True,
            "all_eight_opposite_pairs_share_center": True,
        },
        "cell_adjacency_audit": adjacency_audit,
        "neighboring_star_reroot_closure": {
            "distinct_neighbor_vertices": len(neighbor_vertices),
            "neighbor_norm_counts": {str(k): v for k, v in neighbor_norms.items()},
            "cell_re_root_checks": reroot_checks,
            "failed_re_root_checks": len(reroot_failures),
            "all_shared_cells_agree": not reroot_failures,
            "cells_shared_with_origin_star_by_neighbor_type": {
                "norm_two_root_edge": 702,
                "norm_four_orthoplex_opposite": 1,
            },
        },
        "origin_containing_facet_incidence": {
            "simplex_facets_with_origin": sum(simplex_face_incidence.values()),
            "orthoplex_facets_with_origin": sum(orthoplex_face_incidence.values()),
            "unique_facets": len(combined),
            "multiplicity_counts": dict(multiplicities),
            "simplex_orthoplex_shared_facets": len(cross_type_facets),
            "orthoplex_orthoplex_shared_facets": 69120,
            "simplex_simplex_shared_facets": 0,
            "orthoplex_incidence_multiplicity_counts": dict(orthoplex_multiplicities),
        },
        "scope": (
            "Exact local incidence around one vertex. This does not alone prove "
            "global space-filling, completeness, or absence of nonlocal overlaps."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(run_audit(), indent=2, sort_keys=True))
