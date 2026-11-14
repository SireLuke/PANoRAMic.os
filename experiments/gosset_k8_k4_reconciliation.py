"""Reconcile Gosset graph cliques with the exact E8 Delaunay simplex orbit.

The geometric side obtains 8-vertex facets from a Weyl-reflection orbit.
The graph side independently enumerates cliques from the exact 240-root
adjacency relation. No floating-point arithmetic or full Weyl-group
enumeration is used.
"""
from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from itertools import combinations

from core.geometry.e8_root_system import e8_roots_exact
from experiments.gosset_local_cell_star_audit_v2 import (
    dot,
    facet_orbit,
    reflect,
    simple_roots,
    solve_exact,
)

ROOT_COUNT = 240
ROOT_GRAPH_DEGREE = 56
EXPECTED_SIMPLEX_CELLS = 17_280
EXPECTED_GLOBAL_K4 = 241_920
EXPECTED_K4_PER_VERTEX = 4_032
EXPECTED_K4_PER_EDGE = 216
EXPECTED_K8_PER_VERTEX = 576
EXPECTED_K8_PER_EDGE = 72
EXPECTED_K8_PER_K4 = 5


def build_root_graph(roots):
    """Build the Gosset 1-skeleton: distinct roots with exact inner product 1."""
    adjacency = []
    for index, root in enumerate(roots):
        neighbors = {
            other for other, candidate in enumerate(roots)
            if other != index and dot(root, candidate) == 1
        }
        if len(neighbors) != ROOT_GRAPH_DEGREE:
            raise ArithmeticError(
                f"root {index} has graph degree {len(neighbors)}; "
                f"expected {ROOT_GRAPH_DEGREE}"
            )
        adjacency.append(neighbors)
    return tuple(adjacency)


def enumerate_cliques(adjacency, size):
    """Enumerate each clique once using ordered common-neighbor intersections."""
    found = []

    def extend(prefix, candidates):
        needed = size - len(prefix)
        if needed == 0:
            found.append(prefix)
            return
        if len(candidates) < needed:
            return
        for position, vertex in enumerate(candidates):
            remaining = candidates[position + 1:]
            next_candidates = tuple(
                candidate for candidate in remaining
                if candidate in adjacency[vertex]
            )
            if len(next_candidates) >= needed - 1:
                extend(prefix + (vertex,), next_candidates)

    extend((), tuple(range(len(adjacency))))
    return tuple(found)


def enumerate_simplex_facet_orbit(roots):
    """Reconstruct the 17,280 simplex facets by the existing Weyl orbit method."""
    simple = simple_roots()
    root_index = {root: index for index, root in enumerate(roots)}
    reflection_maps = [
        [root_index[reflect(root, alpha)] for root in roots]
        for alpha in simple
    ]
    weight = solve_exact(simple, [Q(int(i == 1)) for i in range(8)])
    values = [dot(root, weight) for root in roots]
    support = max(values)
    seed = frozenset(
        index for index, value in enumerate(values) if value == support
    )
    if len(seed) != 8:
        raise ArithmeticError(f"simplex facet seed has {len(seed)} vertices; expected 8")
    orbit = facet_orbit(seed, reflection_maps)
    if len(orbit) != EXPECTED_SIMPLEX_CELLS:
        raise ArithmeticError(
            f"simplex facet orbit has {len(orbit)} members; "
            f"expected {EXPECTED_SIMPLEX_CELLS}"
        )
    return {tuple(sorted(facet)) for facet in orbit}


def run_reconciliation():
    """Compare the geometric simplex orbit with graph cliques and incidences."""
    roots = e8_roots_exact()
    if len(roots) != ROOT_COUNT or len(set(roots)) != ROOT_COUNT:
        raise ArithmeticError("canonical E8 root set cardinality/uniqueness failure")
    adjacency = build_root_graph(roots)

    geometric_simplex_facets = enumerate_simplex_facet_orbit(roots)
    graph_k8 = set(enumerate_cliques(adjacency, 8))
    if graph_k8 != geometric_simplex_facets:
        raise ArithmeticError(
            "graph K8 set differs from the Weyl-orbit simplex-facet set "
            f"(graph_only={len(graph_k8 - geometric_simplex_facets)}, "
            f"geometry_only={len(geometric_simplex_facets - graph_k8)})"
        )

    graph_k4 = set(enumerate_cliques(adjacency, 4))
    k4_from_k8 = Counter()
    k8_vertex_incidence = Counter()
    k8_edge_incidence = Counter()
    for simplex in graph_k8:
        k8_vertex_incidence.update(simplex)
        k8_edge_incidence.update(combinations(simplex, 2))
        k4_from_k8.update(combinations(simplex, 4))

    if len(graph_k4) != EXPECTED_GLOBAL_K4:
        raise ArithmeticError(
            f"direct graph K4 count is {len(graph_k4)}; expected {EXPECTED_GLOBAL_K4}"
        )
    if set(k4_from_k8) != graph_k4:
        raise ArithmeticError(
            "K4s covered by geometric simplex cells differ from all graph K4s "
            f"(uncovered={len(graph_k4 - set(k4_from_k8))}, "
            f"unexpected={len(set(k4_from_k8) - graph_k4)})"
        )
    if set(k4_from_k8.values()) != {EXPECTED_K8_PER_K4}:
        raise ArithmeticError("every global K4 must lie in exactly five simplex cells")

    k4_vertex_incidence = Counter()
    k4_edge_incidence = Counter()
    for clique in graph_k4:
        k4_vertex_incidence.update(clique)
        k4_edge_incidence.update(combinations(clique, 2))

    if set(k4_vertex_incidence.values()) != {EXPECTED_K4_PER_VERTEX}:
        raise ArithmeticError("global K4 vertex incidence is not uniformly 4,032")
    if len(k4_edge_incidence) != 6_720 or set(k4_edge_incidence.values()) != {
        EXPECTED_K4_PER_EDGE
    }:
        raise ArithmeticError("global K4 edge incidence is not uniformly 216")
    if set(k8_vertex_incidence.values()) != {EXPECTED_K8_PER_VERTEX}:
        raise ArithmeticError("simplex-cell vertex incidence is not uniformly 576")
    if len(k8_edge_incidence) != 6_720 or set(k8_edge_incidence.values()) != {
        EXPECTED_K8_PER_EDGE
    }:
        raise ArithmeticError("simplex-cell edge incidence is not uniformly 72")

    if len(graph_k8) * 70 != len(graph_k4) * EXPECTED_K8_PER_K4:
        raise ArithmeticError("K8-to-K4 incidence totals do not balance")
    if len(graph_k8) * 8 != ROOT_COUNT * EXPECTED_K8_PER_VERTEX:
        raise ArithmeticError("K8-to-vertex incidence totals do not balance")
    if len(graph_k8) * 28 != 6_720 * EXPECTED_K8_PER_EDGE:
        raise ArithmeticError("K8-to-edge incidence totals do not balance")

    return {
        "status": "PASS",
        "arithmetic": "exact rational root coordinates and integer graph incidence",
        "e8_roots": len(roots),
        "gosset_graph": {
            "vertices": len(roots),
            "degree": ROOT_GRAPH_DEGREE,
            "edges": len(k8_edge_incidence),
        },
        "simplex_cell_reconciliation": {
            "weyl_orbit_simplex_facets": len(geometric_simplex_facets),
            "independently_enumerated_graph_k8": len(graph_k8),
            "sets_equal": graph_k8 == geometric_simplex_facets,
        },
        "global_k4_reconciliation": {
            "direct_graph_k4": len(graph_k4),
            "k4_covered_by_simplex_cells": len(k4_from_k8),
            "every_k4_covered": set(k4_from_k8) == graph_k4,
            "simplex_cells_per_k4": EXPECTED_K8_PER_K4,
            "k4_per_vertex": EXPECTED_K4_PER_VERTEX,
            "k4_per_edge": EXPECTED_K4_PER_EDGE,
        },
        "simplex_cell_incidence": {
            "cells": len(graph_k8),
            "vertices_per_cell": 8,
            "edges_per_cell": 28,
            "k4s_per_cell": 70,
            "cells_per_vertex": EXPECTED_K8_PER_VERTEX,
            "cells_per_edge": EXPECTED_K8_PER_EDGE,
        },
        "double_counting": {
            "cell_k4_incidences": len(graph_k8) * 70,
            "k4_cell_incidences": len(graph_k4) * EXPECTED_K8_PER_K4,
            "balanced": len(graph_k8) * 70 == len(graph_k4) * EXPECTED_K8_PER_K4,
        },
        "weyl_group_enumerated": False,
        "physical_validation_claimed": False,
        "scope": (
            "Reconciles the Weyl-orbit 8-simplex facets in the exact origin "
            "Delaunay star with independently enumerated K8 cliques of the "
            "240-root Gosset graph, and reconciles their K4 incidences. "
            "It does not by itself certify the 8-orthoplex orbit or global "
            "space-filling."
        ),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_reconciliation(), indent=2, sort_keys=True))
