"""Audit codimension-two links in the exact Gosset local cell star.

For every origin-containing codimension-two face, build its link multigraph:
vertices are incident origin-containing facets and edges are incident
8-cells. A manifold-like face-to-face star requires a single connected
2-regular cycle at every such face.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction as Q
from itertools import combinations, product
import json

from core.geometry.e8_root_system import e8_roots_exact
from experiments.gosset_graph_incidence_reconciliation import (
    ZERO,
    build_graph_orthoplex_cells,
    simplex_facet_orbit,
    build_gosset_graph,
    graph_orthoplex_facets,
    weyl_orthoplex_facets,
    dot,
    reflect,
    simple_roots,
    solve_exact,
    squared_distance,
)


def _opposite_pairs(cell):
    remaining = set(cell)
    pairs = []
    while remaining:
        first = min(remaining)
        matches = [
            candidate for candidate in remaining
            if candidate != first and squared_distance(first, candidate) == 4
        ]
        if len(matches) != 1:
            raise ArithmeticError("cell does not have a unique antipodal pairing")
        second = matches[0]
        pairs.append(tuple(sorted((first, second))))
        remaining.remove(first)
        remaining.remove(second)
    if len(pairs) != 8 or not any(ZERO in pair for pair in pairs):
        raise ArithmeticError("expected eight antipodal pairs including the origin pair")
    return [pair for pair in pairs if ZERO not in pair]


def _add_link_edge(link_edges, facet_owners, face, facet_a, facet_b, cell_id):
    face = tuple(sorted(face))
    facet_a = tuple(sorted(facet_a))
    facet_b = tuple(sorted(facet_b))
    if facet_a == facet_b:
        raise ArithmeticError("codimension-two face has duplicate containing facets")
    link_edges[face].append((facet_a, facet_b, cell_id))
    facet_owners[facet_a].add(cell_id)
    facet_owners[facet_b].add(cell_id)


def build_codim2_links(simplex_cells, orthoplex_cells):
    """Build each face link without using a precomputed facet-neighbor graph."""
    link_edges = defaultdict(list)
    facet_owners = defaultdict(set)
    cell_count = 0

    for cell in simplex_cells:
        cell_id = ("simplex", cell)
        nonzero = tuple(vertex for vertex in cell if vertex != ZERO)
        if len(nonzero) != 8:
            raise ArithmeticError("simplex cell must have eight non-origin vertices")
        cell_count += 1
        for selected in combinations(nonzero, 6):
            omitted = [vertex for vertex in nonzero if vertex not in selected]
            if len(omitted) != 2:
                raise ArithmeticError("simplex codimension-two completion is malformed")
            face = (ZERO,) + selected
            _add_link_edge(
                link_edges, facet_owners, face,
                face + (omitted[0],), face + (omitted[1],), cell_id,
            )

    for cell in orthoplex_cells:
        cell_id = ("orthoplex", cell)
        pairs = _opposite_pairs(cell)
        if len(pairs) != 7:
            raise ArithmeticError("orthoplex must have seven non-origin antipodal pairs")
        cell_count += 1
        for omitted_index in range(7):
            selected_pairs = [
                pair for index, pair in enumerate(pairs) if index != omitted_index
            ]
            for choices in product((0, 1), repeat=6):
                selected_vertices = tuple(
                    selected_pairs[index][choices[index]] for index in range(6)
                )
                face = (ZERO,) + selected_vertices
                omitted_pair = pairs[omitted_index]
                _add_link_edge(
                    link_edges, facet_owners, face,
                    face + (omitted_pair[0],), face + (omitted_pair[1],), cell_id,
                )

    return link_edges, facet_owners, cell_count


def audit_link_cycles(link_edges, facet_owners):
    cycle_lengths = Counter()
    edge_count_distribution = Counter()
    connected_components = Counter()
    max_degree = 0

    for face, edges in link_edges.items():
        adjacency = defaultdict(list)
        for edge_index, (facet_a, facet_b, _cell_id) in enumerate(edges):
            adjacency[facet_a].append((facet_b, edge_index))
            adjacency[facet_b].append((facet_a, edge_index))

        degrees = {facet: len(neighbors) for facet, neighbors in adjacency.items()}
        if any(degree != 2 for degree in degrees.values()):
            bad = Counter(degrees.values())
            raise ArithmeticError(
                f"link at face has non-2-regular facet degrees: {dict(bad)}"
            )
        max_degree = max(max_degree, max(degrees.values(), default=0))

        start = next(iter(adjacency))
        visited = {start}
        stack = [start]
        while stack:
            current = stack.pop()
            for neighbor, _edge_index in adjacency[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    stack.append(neighbor)
        components = 1
        if len(visited) != len(adjacency):
            components = 1 + sum(
                1 for facet in adjacency if facet not in visited
            )
            raise ArithmeticError(
                f"codimension-two link is disconnected: {components} components"
            )

        if len(edges) != len(adjacency):
            raise ArithmeticError("2-regular link violates edge/vertex cycle count")
        if len(adjacency) < 3:
            raise ArithmeticError("link cycle has fewer than three facet vertices")

        # Distinct cells must define distinct link edges; a duplicate edge would
        # be a two-cell double adjacency rather than a genuine simple cycle.
        edge_pairs = [(a, b) if a < b else (b, a) for a, b, _ in edges]
        if len(set(edge_pairs)) != len(edge_pairs):
            raise ArithmeticError("link contains parallel facet-adjacency edges")

        cycle_lengths[len(adjacency)] += 1
        edge_count_distribution[len(edges)] += 1
        connected_components[components] += 1

    owner_multiplicity = Counter(len(owners) for owners in facet_owners.values())
    if owner_multiplicity != Counter({2: len(facet_owners)}):
        raise ArithmeticError(
            f"origin-facet owner multiplicity is not exactly two: {owner_multiplicity}"
        )

    return {
        "codimension_two_faces": len(link_edges),
        "link_cycle_length_distribution": dict(sorted(cycle_lengths.items())),
        "link_edge_count_distribution": dict(sorted(edge_count_distribution.items())),
        "connected_component_distribution": dict(sorted(connected_components.items())),
        "origin_containing_facets": len(facet_owners),
        "facet_cell_owner_multiplicity": dict(sorted(owner_multiplicity.items())),
        "all_links_are_single_connected_cycles": True,
        "all_link_vertices_have_degree_two": True,
        "no_parallel_link_edges": True,
        "max_link_vertex_degree": max_degree,
    }


def run_link_audit():
    roots = tuple(e8_roots_exact())
    if len(roots) != 240 or len(set(roots)) != 240:
        raise ArithmeticError("expected 240 unique E8 roots")
    adjacency = build_gosset_graph(roots)
    graph_facets, graph_report = graph_orthoplex_facets(roots, adjacency)
    if graph_facets != weyl_orthoplex_facets(roots):
        raise ArithmeticError("graph-derived orthoplex orbit differs from Weyl orbit")
    orthoplex_cells, _opposite_shell = build_graph_orthoplex_cells(roots, graph_facets)
    simplex_facets = simplex_facet_orbit(roots)
    simplex_cells = {
        tuple(sorted((ZERO,) + tuple(roots[index] for index in sorted(facet))))
        for facet in simplex_facets
    }
    if len(simplex_cells) != 17280 or len(orthoplex_cells) != 2160:
        raise ArithmeticError("unexpected simplex/orthoplex local-star cell counts")

    link_edges, facet_owners, cell_count = build_codim2_links(
        simplex_cells, orthoplex_cells
    )
    audit = audit_link_cycles(link_edges, facet_owners)
    if cell_count != 19440:
        raise ArithmeticError("unexpected total local-star cell count")
    return {
        "status": "PASS",
        "root_count": len(roots),
        "graph_orthoplex_orbit": graph_report,
        "simplex_cells": len(simplex_cells),
        "graph_derived_orthoplex_cells": len(orthoplex_cells),
        "total_cells": cell_count,
        "link_audit": audit,
        "scope": (
            "Exact finite combinatorial audit of origin-containing codimension-two "
            "face links in the declared E8 local star. A PASS establishes one "
            "connected 2-regular cycle at each audited face; it does not alone "
            "prove global Euclidean coverage or a complete global tiling."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(run_link_audit(), indent=2, sort_keys=True))
