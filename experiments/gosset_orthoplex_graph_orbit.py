"""Independently reconstruct the Gosset 7-orthoplex facet orbit from its graph.

The graph-side construction finds seven mutually compatible orthogonal pairs.
Within each pair the E8 roots have inner product 0; across distinct pairs
every inner product is 1. Thus each 14-set induces K_14 minus a perfect
matching. This construction does not use a Weyl seed or reflection orbit.
A separate Weyl-orbit construction is used only as the comparison target.
"""
from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from itertools import combinations
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
    facet_orbit,
    reflect,
    simple_roots,
    solve_exact,
)

ROOT_COUNT = 240
ROOT_GRAPH_DEGREE = 56
ROOT_GRAPH_EDGE_COUNT = 6720
ORTHOPLEX_FACET_SIZE = 14
ORTHOPLEX_PAIR_COUNT = 7
EXPECTED_PAIR_NODES = 15120
EXPECTED_ORBIT_SIZE = 2160


def build_gosset_graph(roots):
    """Build the exact Gosset graph using the root inner-product rule 1."""
    adjacency = []
    for index, root in enumerate(roots):
        neighbors = {
            other
            for other, candidate in enumerate(roots)
            if other != index and dot(root, candidate) == 1
        }
        if len(neighbors) != ROOT_GRAPH_DEGREE:
            raise ArithmeticError(
                f"root {index} has degree {len(neighbors)}; "
                f"expected {ROOT_GRAPH_DEGREE}"
            )
        adjacency.append(neighbors)
    return tuple(adjacency)


def build_orthogonal_pair_graph(roots, adjacency):
    """Make a graph whose nodes are orthogonal root-pairs.

    Two pair-nodes are adjacent exactly when every cross-pair of roots is
    adjacent in the Gosset graph. A 7-clique is therefore seven disjoint
    orthogonal pairs with all cross-pairs adjacent: K_14 minus a 1-factor.
    """
    pairs = [
        (i, j)
        for i, j in combinations(range(len(roots)), 2)
        if dot(roots[i], roots[j]) == 0
    ]
    if len(pairs) != EXPECTED_PAIR_NODES:
        raise ArithmeticError(
            f"orthogonal pair-node count {len(pairs)}; expected {EXPECTED_PAIR_NODES}"
        )
    pair_index = {pair: index for index, pair in enumerate(pairs)}
    compatibility = [set() for _ in pairs]

    for pair_id, (i, j) in enumerate(pairs):
        common_neighbors = sorted(adjacency[i].intersection(adjacency[j]))
        for a, b in combinations(common_neighbors, 2):
            if dot(roots[a], roots[b]) == 0:
                other_pair_id = pair_index[(a, b)]
                compatibility[pair_id].add(other_pair_id)

    # Compatibility is a symmetric relation; assert this independently.
    for pair_id, neighbors in enumerate(compatibility):
        if any(pair_id not in compatibility[other] for other in neighbors):
            raise ArithmeticError("orthogonal-pair compatibility is not symmetric")
    return tuple(pairs), tuple(compatibility)


def enumerate_pair_cliques(compatibility, target_size=ORTHOPLEX_PAIR_COUNT):
    """Enumerate each target clique once, using increasing pair-node IDs."""
    found = []

    def extend(prefix, candidates):
        needed = target_size - len(prefix)
        if needed == 0:
            found.append(tuple(prefix))
            return
        if len(candidates) < needed:
            return
        for position, pair_id in enumerate(candidates):
            remaining = candidates[position + 1 :]
            next_candidates = [
                candidate
                for candidate in remaining
                if candidate in compatibility[pair_id]
            ]
            if len(next_candidates) >= needed - 1:
                extend(prefix + [pair_id], next_candidates)

    extend([], list(range(len(compatibility))))
    return tuple(found)


def graph_orthoplex_facets(roots, adjacency):
    """Return the 14-root orthoplex facets found without Weyl reflections."""
    pairs, compatibility = build_orthogonal_pair_graph(roots, adjacency)
    pair_cliques = enumerate_pair_cliques(compatibility)
    facets = set()

    for clique in pair_cliques:
        selected_pairs = [pairs[pair_id] for pair_id in clique]
        vertices = tuple(sorted(index for pair in selected_pairs for index in pair))
        if len(vertices) != ORTHOPLEX_FACET_SIZE:
            raise ArithmeticError("pair clique did not contain 14 distinct roots")
        facet = frozenset(vertices)
        if facet in facets:
            raise ArithmeticError("duplicate orthoplex facet from pair-clique enumeration")
        facets.add(facet)

        # Exact induced-subgraph signature: 7 orthogonal nonedges, 84 edges.
        inner_products = Counter(
            dot(roots[a], roots[b]) for a, b in combinations(vertices, 2)
        )
        if inner_products != Counter({Q(1): 84, Q(0): 7}):
            raise ArithmeticError(
                f"invalid K14-minus-matching signature: {inner_products}"
            )

    return facets, {
        "orthogonal_pair_nodes": len(pairs),
        "pair_compatibility_edges": sum(map(len, compatibility)) // 2,
        "pair_cliques_of_size_7": len(pair_cliques),
        "facets": len(facets),
    }


def weyl_orthoplex_facets(roots):
    """Build the comparison orbit from the node-0 fundamental-weight seed."""
    simple = simple_roots()
    root_index = {root: index for index, root in enumerate(roots)}
    reflection_maps = [
        [root_index[reflect(root, alpha)] for root in roots]
        for alpha in simple
    ]
    weight = solve_exact(simple, [Q(int(i == 0)) for i in range(8)])
    values = [dot(root, weight) for root in roots]
    support = max(values)
    seed = frozenset(index for index, value in enumerate(values) if value == support)
    if len(seed) != ORTHOPLEX_FACET_SIZE:
        raise ArithmeticError(f"Weyl seed has {len(seed)} vertices; expected 14")
    orbit = facet_orbit(seed, reflection_maps)
    if len(orbit) != EXPECTED_ORBIT_SIZE:
        raise ArithmeticError(
            f"Weyl orthoplex orbit has {len(orbit)} facets; expected {EXPECTED_ORBIT_SIZE}"
        )
    return orbit


def run_reconciliation():
    """Compare independent graph and Weyl constructions at exact set level."""
    roots = tuple(e8_roots_exact())
    if len(roots) != ROOT_COUNT or len(set(roots)) != ROOT_COUNT:
        raise ArithmeticError("canonical E8 root set cardinality/uniqueness failure")

    adjacency = build_gosset_graph(roots)
    graph_edge_count = sum(map(len, adjacency)) // 2
    if graph_edge_count != ROOT_GRAPH_EDGE_COUNT:
        raise ArithmeticError(
            f"Gosset graph edge count {graph_edge_count}; expected {ROOT_GRAPH_EDGE_COUNT}"
        )

    graph_facets, pair_graph_report = graph_orthoplex_facets(roots, adjacency)
    weyl_facets = weyl_orthoplex_facets(roots)
    if graph_facets != weyl_facets:
        raise ArithmeticError(
            "graph-derived orthoplex facets differ from Weyl orbit: "
            f"graph_only={len(graph_facets - weyl_facets)}, "
            f"weyl_only={len(weyl_facets - graph_facets)}"
        )

    return {
        "status": "PASS",
        "root_count": len(roots),
        "root_graph_degree": ROOT_GRAPH_DEGREE,
        "root_graph_edge_count": graph_edge_count,
        "graph_pair_construction": pair_graph_report,
        "graph_facet_count": len(graph_facets),
        "weyl_orbit_facet_count": len(weyl_facets),
        "exact_set_equality": graph_facets == weyl_facets,
        "facet_signature": {
            "vertices": ORTHOPLEX_FACET_SIZE,
            "orthogonal_opposite_pairs": ORTHOPLEX_PAIR_COUNT,
            "induced_graph_edges": 84,
            "induced_graph_non_edges": 7,
            "induced_graph": "K14 minus a perfect matching",
        },
        "scope": (
            "Exact finite combinatorial reconstruction of the 7-orthoplex "
            "facet orbit from the 240-root Gosset graph, compared as a set "
            "against the independent Weyl-reflection orbit. This does not "
            "alone prove global Delaunay coverage or physical interpretation."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(run_reconciliation(), indent=2, sort_keys=True))
