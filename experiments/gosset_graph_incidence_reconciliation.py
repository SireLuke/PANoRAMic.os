"""Reconcile graph-derived Gosset orthoplexes with the local cell-star incidence.

The 7-orthoplex facet orbit is reconstructed from the 240-root graph, not
from a Weyl seed. Those facets are lifted to 8-orthoplex Delaunay cells.
Their origin-containing 7-faces are then reconciled with the 8-simplex
cells and with one another using exact rational vertex sets and halfspaces.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction as Q
from itertools import combinations, product
import json

# --- repo-root bootstrap: makes this file runnable directly, from any
# working directory (the imports below address packages from the repo
# root). No-op when the root is already on sys.path. See
# docs/RUNNING_PYTHON.md.
import sys as _sys
from pathlib import Path as _Path

_REPO_ROOT = _Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in _sys.path:
    _sys.path.insert(0, str(_REPO_ROOT))
# --- end repo-root bootstrap ---

from core.geometry.e8_root_system import e8_roots_exact
from experiments.gosset_local_cell_star_audit_v2 import (
    dot,
    is_e8_lattice_vector,
    reflect,
    simple_roots,
    solve_exact,
    squared_distance,
)
from experiments.gosset_orthoplex_graph_orbit import (
    build_gosset_graph,
    graph_orthoplex_facets,
    weyl_orthoplex_facets,
)

ZERO = (Q(0),) * 8
EXPECTED_SIMPLEX_CELLS = 17280
EXPECTED_ORTHOPLEX_CELLS = 2160
EXPECTED_SIMPLEX_ORIGIN_FACES = 138240
EXPECTED_ORTHOPLEX_ORIGIN_FACE_INCIDENCES = 276480
EXPECTED_UNIQUE_ORIGIN_FACES = 207360


def simplex_facet_orbit(roots):
    """Generate the 8-root simplex facet orbit as a separate comparator."""
    simple = simple_roots()
    root_index = {root: index for index, root in enumerate(roots)}
    reflection_maps = [
        [root_index[reflect(root, alpha)] for root in roots]
        for alpha in simple
    ]
    weight = solve_exact(simple, [Q(int(i == 1)) for i in range(8)])
    values = [dot(root, weight) for root in roots]
    support = max(values)
    seed = frozenset(index for index, value in enumerate(values) if value == support)
    if len(seed) != 8:
        raise ArithmeticError(f"simplex seed has {len(seed)} roots, expected 8")
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
    if len(seen) != EXPECTED_SIMPLEX_CELLS:
        raise ArithmeticError(
            f"simplex orbit has {len(seen)} members, expected {EXPECTED_SIMPLEX_CELLS}"
        )
    return seen


def centroid(points):
    return tuple(
        sum((point[k] for point in points), Q(0)) / len(points)
        for k in range(8)
    )


def facet_outward_normal(cell, face):
    """Exact normal from cell centroid to facet centroid."""
    face_center = centroid(face)
    cell_center = centroid(cell)
    normal = tuple(face_center[k] - cell_center[k] for k in range(8))
    if dot(normal, normal) == 0:
        raise ArithmeticError("degenerate cell facet normal")
    if not all(
        dot(normal, tuple(point[k] - face_center[k] for k in range(8))) == 0
        for point in face
    ):
        raise ArithmeticError("facet vertices do not share exact supporting plane")
    if not all(
        dot(normal, tuple(point[k] - face_center[k] for k in range(8))) < 0
        for point in cell if point not in set(face)
    ):
        raise ArithmeticError("cell vertices are not strictly inside facet halfspace")
    return normal


def build_graph_orthoplex_cells(roots, graph_facets):
    """Lift each graph-derived 14-root facet to its 16-vertex 8-orthoplex."""
    cells = set()
    opposite_vertices = set()
    for facet in graph_facets:
        vertices = tuple(roots[index] for index in sorted(facet))
        if len(vertices) != 14:
            raise ArithmeticError("graph facet does not contain 14 roots")
        center = centroid(vertices)
        opposite = tuple(2 * value for value in center)
        if not is_e8_lattice_vector(opposite):
            raise ArithmeticError("orthoplex opposite vertex is not in the E8 lattice")
        if sum(value * value for value in opposite) != 4:
            raise ArithmeticError("orthoplex opposite vertex does not have norm squared 4")
        opposite_vertices.add(opposite)

        remaining = set(vertices)
        pairs = []
        while remaining:
            first = min(remaining)
            matches = [
                candidate for candidate in remaining
                if candidate != first and squared_distance(first, candidate) == 4
            ]
            if len(matches) != 1:
                raise ArithmeticError("orthoplex root facet lacks unique opposite pairing")
            second = matches[0]
            pairs.append((first, second))
            remaining.remove(first)
            remaining.remove(second)
        if len(pairs) != 7:
            raise ArithmeticError("graph facet does not contain seven opposite pairs")

        cell = tuple(sorted((ZERO,) + vertices + (opposite,)))
        if len(cell) != 16 or cell in cells:
            raise ArithmeticError("duplicate or malformed 8-orthoplex cell")
        distance_counts = Counter(
            squared_distance(a, b) for a, b in combinations(cell, 2)
        )
        if distance_counts != Counter({Q(2): 112, Q(4): 8}):
            raise ArithmeticError(f"invalid orthoplex metric signature: {distance_counts}")
        center_cell = centroid(cell)
        if center_cell != tuple(value / 2 for value in opposite):
            raise ArithmeticError("orthoplex cell does not share the computed center")
        if not all(squared_distance(point, center_cell) == 1 for point in cell):
            raise ArithmeticError("orthoplex vertices do not share unit circumradius")
        cells.add(cell)

    if len(opposite_vertices) != 2160:
        raise ArithmeticError(f"opposite shell has {len(opposite_vertices)} points, expected 2160")
    return cells, opposite_vertices


def origin_faces_of_simplex_cells(roots, simplex_facets):
    """Return exact 8-vertex faces containing the origin from 8-simplices."""
    incidence = Counter()
    cells = set()
    for facet in simplex_facets:
        vertices = tuple(roots[index] for index in sorted(facet))
        cell = tuple(sorted((ZERO,) + vertices))
        if len(cell) != 9 or cell in cells:
            raise ArithmeticError("duplicate or malformed 8-simplex cell")
        cells.add(cell)
        if not all(squared_distance(a, b) == 2 for a, b in combinations(cell, 2)):
            raise ArithmeticError("simplex cell is not regular with edge length squared 2")
        for omitted in vertices:
            face = tuple(sorted((ZERO,) + tuple(v for v in vertices if v != omitted)))
            incidence[face] += 1
    if len(cells) != EXPECTED_SIMPLEX_CELLS:
        raise ArithmeticError("unexpected simplex cell count")
    if len(incidence) != EXPECTED_SIMPLEX_ORIGIN_FACES:
        raise ArithmeticError("unexpected unique simplex origin-face count")
    if set(incidence.values()) != {1}:
        raise ArithmeticError("simplex origin-containing facets are not unique")
    return cells, incidence


def origin_faces_of_orthoplex_cells(cells):
    """Enumerate all 128 origin-containing facets of each 8-orthoplex."""
    incidence = Counter()
    for cell in cells:
        remaining = set(cell)
        pairs = []
        while remaining:
            first = min(remaining)
            matches = [
                candidate for candidate in remaining
                if candidate != first and squared_distance(first, candidate) == 4
            ]
            if len(matches) != 1:
                raise ArithmeticError("orthoplex cell has non-unique opposite pairing")
            second = matches[0]
            pairs.append((first, second))
            remaining.remove(first)
            remaining.remove(second)
        if len(pairs) != 8 or not any(ZERO in pair for pair in pairs):
            raise ArithmeticError("origin and opposite vertex are not one antipodal pair")
        nonzero_pairs = [pair for pair in pairs if ZERO not in pair]
        if len(nonzero_pairs) != 7:
            raise ArithmeticError("expected seven non-origin opposite pairs")
        for choices in product((0, 1), repeat=7):
            face = tuple(sorted((ZERO,) + tuple(
                nonzero_pairs[index][choices[index]] for index in range(7)
            )))
            incidence[face] += 1
    if sum(incidence.values()) != EXPECTED_ORTHOPLEX_ORIGIN_FACE_INCIDENCES:
        raise ArithmeticError("unexpected orthoplex origin-face incidence count")
    return incidence


def reconcile_incidence(simplex_cells, simplex_faces, orthoplex_cells, orthoplex_faces):
    """Check exact 2-to-1 pairing, type distribution, and opposite halfspaces."""
    owners = defaultdict(list)
    for cell in simplex_cells:
        cell_set = set(cell)
        for face in combinations(cell_set - {ZERO}, 7):
            key = tuple(sorted((ZERO,) + tuple(face)))
            owners[key].append(("simplex", cell))
    # Index orthoplex cells by their origin faces. Each cell contributes 128.
    orth_face_owners = defaultdict(list)
    for cell in orthoplex_cells:
        remaining = set(cell)
        pairs = []
        while remaining:
            first = min(remaining)
            matches = [
                candidate for candidate in remaining
                if candidate != first and squared_distance(first, candidate) == 4
            ]
            second = matches[0]
            pairs.append((first, second))
            remaining.remove(first)
            remaining.remove(second)
        nonzero_pairs = [pair for pair in pairs if ZERO not in pair]
        for choices in product((0, 1), repeat=7):
            face = tuple(sorted((ZERO,) + tuple(
                nonzero_pairs[index][choices[index]] for index in range(7)
            )))
            orth_face_owners[face].append(cell)

    if Counter(map(len, orth_face_owners.values())) != Counter({1: 138240, 2: 69120}):
        raise ArithmeticError("orthoplex origin-face multiplicity profile mismatch")
    if not set(simplex_faces).issubset(orth_face_owners):
        raise ArithmeticError(
            "a simplex origin face is absent from the graph-derived orthoplex incidence"
        )
    if any(len(orth_face_owners[face]) != 1 for face in simplex_faces):
        raise ArithmeticError(
            "each simplex/orthoplex shared face must have exactly one orthoplex owner"
        )
    if Counter(map(len, owners.values())) != Counter({1: EXPECTED_SIMPLEX_ORIGIN_FACES}):
        raise ArithmeticError("simplex owner enumeration is not unique")

    # Every simplex origin face is incident to exactly one orthoplex cell;
    # the remaining 69,120 orthoplex faces pair two orthoplex cells.
    pair_types = Counter()
    normal_pair_checks = 0
    for face, simplex_owner_list in owners.items():
        if len(simplex_owner_list) != 1:
            raise ArithmeticError("simplex face has multiple simplex owners")
        simplex_owner = simplex_owner_list[0][1]
        orth_owners = orth_face_owners[face]
        if len(orth_owners) not in (1, 2):
            raise ArithmeticError("orthoplex face has invalid owner multiplicity")
        pair_types["simplex+orthoplex"] += 1
        normal_a = facet_outward_normal(simplex_owner, face)
        for orth_owner in orth_owners:
            if set(simplex_owner).intersection(orth_owner) != set(face):
                raise ArithmeticError("simplex/orthoplex cells do not intersect exactly in shared face")
            normal_b = facet_outward_normal(orth_owner, face)
            if dot(normal_a, normal_b) >= 0:
                raise ArithmeticError("simplex and orthoplex interiors are not on opposite halfspaces")
            normal_pair_checks += 1

    ortho_ortho_faces = [
        (face, cells_for_face)
        for face, cells_for_face in orth_face_owners.items()
        if len(cells_for_face) == 2
    ]
    for face, cells_for_face in ortho_ortho_faces:
        cell_a, cell_b = cells_for_face
        if set(cell_a).intersection(cell_b) != set(face):
            raise ArithmeticError("orthoplex pair intersection is larger/smaller than shared face")
        normal_a = facet_outward_normal(cell_a, face)
        normal_b = facet_outward_normal(cell_b, face)
        if dot(normal_a, normal_b) >= 0:
            raise ArithmeticError("orthoplex interiors are not on opposite shared-facet halfspaces")
        pair_types["orthoplex+orthoplex"] += 1
        normal_pair_checks += 1

    combined_incidence = sum(simplex_faces.values()) + sum(orthoplex_faces.values())
    unique_faces = len(set(simplex_faces) | set(orthoplex_faces))
    if combined_incidence != 2 * EXPECTED_UNIQUE_ORIGIN_FACES:
        raise ArithmeticError("combined origin-facet incidence is not exactly two per face")
    if unique_faces != EXPECTED_UNIQUE_ORIGIN_FACES:
        raise ArithmeticError("unexpected unique combined origin-facet count")
    if sum(orth_face_owners[face].__len__() == 2 for face in orth_face_owners) != 69120:
        raise ArithmeticError("orthoplex/orthoplex shared-face count mismatch")

    return {
        "simplex_cells": len(simplex_cells),
        "graph_derived_orthoplex_cells": len(orthoplex_cells),
        "simplex_origin_face_incidences": sum(simplex_faces.values()),
        "orthoplex_origin_face_incidences": sum(orthoplex_faces.values()),
        "unique_origin_containing_facets": unique_faces,
        "combined_facet_incidence_multiplicity": 2,
        "orthoplex_face_multiplicity_counts": {"1": 138240, "2": 69120},
        "shared_facet_type_counts": {
            "simplex+orthoplex": 138240,
            "orthoplex+orthoplex": 69120,
            "simplex+simplex": 0,
        },
        "exact_common_vertex_set_checks": unique_faces,
        "opposite_halfspace_normal_pair_checks": normal_pair_checks,
        "all_shared_faces_pair_exactly": True,
        "all_incident_cell_intersections_equal_shared_face": True,
        "all_incident_cell_interiors_on_opposite_halfspaces": True,
    }


def run_reconciliation():
    roots = tuple(e8_roots_exact())
    if len(roots) != 240 or len(set(roots)) != 240:
        raise ArithmeticError("canonical E8 root set is not 240 unique roots")

    adjacency = build_gosset_graph(roots)
    graph_facets, graph_report = graph_orthoplex_facets(roots, adjacency)
    weyl_facets = weyl_orthoplex_facets(roots)
    if graph_facets != weyl_facets:
        raise ArithmeticError("graph-derived orthoplex facet orbit differs from Weyl orbit")

    orthoplex_cells, opposite_vertices = build_graph_orthoplex_cells(roots, graph_facets)
    simplex_facets = simplex_facet_orbit(roots)
    simplex_cells, simplex_faces = origin_faces_of_simplex_cells(roots, simplex_facets)
    orthoplex_faces = origin_faces_of_orthoplex_cells(orthoplex_cells)
    if len(orthoplex_faces) != EXPECTED_UNIQUE_ORIGIN_FACES:
        raise ArithmeticError("unexpected unique orthoplex origin-face count")

    incidence = reconcile_incidence(
        simplex_cells, simplex_faces, orthoplex_cells, orthoplex_faces
    )
    return {
        "status": "PASS",
        "root_count": len(roots),
        "graph_orthoplex_orbit": graph_report,
        "graph_orbit_equals_weyl_orbit": True,
        "simplex_cell_count": len(simplex_cells),
        "graph_derived_orthoplex_cell_count": len(orthoplex_cells),
        "opposite_norm_four_shell_count": len(opposite_vertices),
        "simplex_origin_face_unique_count": len(simplex_faces),
        "orthoplex_origin_face_incidence_count": sum(orthoplex_faces.values()),
        "incidence_reconciliation": incidence,
        "scope": (
            "Exact rational finite-star reconstruction. Orthoplex cells are "
            "generated from the graph-derived 7-orthoplex facet orbit; "
            "simplex cells provide the independent local-star comparator. "
            "This certifies the declared incidence and shared-halfspace data, "
            "not by itself global Euclidean coverage or physical interpretation."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(run_reconciliation(), indent=2, sort_keys=True))
