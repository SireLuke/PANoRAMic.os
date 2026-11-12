#!/usr/bin/env python3
"""Exact affine-E8 cusp-link realization extracted from the E10 ideal vertex.

This verifies the affine E8 simple-root Gram system, primitive null-root marks,
and the affine translation generator. It does not construct the full 5_21
Wythoffian or the global hyperbolic 6_21 honeycomb.
"""
from __future__ import annotations

from fractions import Fraction as Q
from itertools import combinations

from core.geometry.e8_root_system import (
    dot,
    e8_roots_exact,
    e8_simple_roots_exact,
)


LINK_NODES = (0, 1, 2, 3, 4, 5, 7, 8, 9)
NULL_MARKS = (6, 5, 4, 3, 2, 1, 4, 2, 3)
FINITE_NODE_TO_SIMPLE_ROOT = {
    0: 3,
    1: 4,
    2: 5,
    3: 6,
    4: 7,
    7: 2,
    8: 0,
    9: 1,
}


def e10_gram_from_arms(arms=(6, 2, 1)):
    n = 1 + sum(arms)
    adjacency = [[0] * n for _ in range(n)]
    cursor = 1
    for length in arms:
        previous = 0
        for _ in range(length):
            adjacency[previous][cursor] = adjacency[cursor][previous] = 1
            previous, cursor = cursor, cursor + 1
    return [
        [Q(int(i == j)) - Q(adjacency[i][j], 2) for j in range(n)]
        for i in range(n)
    ]


def identity(n):
    return [[Q(int(i == j)) for j in range(n)] for i in range(n)]


def matrix_multiply(a, b):
    return [
        [sum(a[i][k] * b[k][j] for k in range(len(b)))
         for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def matrix_vector(a, vector):
    return tuple(sum(a[i][j] * vector[j] for j in range(len(vector)))
                 for i in range(len(a)))


def affine_compose(left, right):
    """Return left after right; each affine map is (linear_matrix, shift)."""
    left_matrix, left_shift = left
    right_matrix, right_shift = right
    return (
        matrix_multiply(left_matrix, right_matrix),
        tuple(a + b for a, b in zip(
            matrix_vector(left_matrix, right_shift), left_shift
        )),
    )


def affine_identity():
    return identity(8), (Q(0),) * 8


def affine_reflection(root, level=Q(0)):
    """Reflection x -> x - (x.root + level) root for root norm squared 2."""
    if dot(root, root) != 2:
        raise AssertionError("affine reflection root must have norm squared 2")
    linear = [
        [Q(int(i == j)) - root[i] * root[j] for j in range(8)]
        for i in range(8)
    ]
    shift = tuple(-level * value for value in root)
    return linear, shift


def negate(vector):
    return tuple(-value for value in vector)


def run_audit():
    e10_gram = e10_gram_from_arms()
    simple = e8_simple_roots_exact()
    roots = set(e8_roots_exact())
    marks = dict(zip(LINK_NODES, NULL_MARKS))

    if len(LINK_NODES) != 9 or len(set(LINK_NODES)) != 9:
        raise AssertionError("affine link must contain nine distinct nodes")
    if any(mark <= 0 for mark in NULL_MARKS):
        raise AssertionError("null-root marks must be positive")
    if __import__("math").gcd(*NULL_MARKS) != 1:
        raise AssertionError("null-root marks must be primitive")

    finite_roots = {
        node: simple[index]
        for node, index in FINITE_NODE_TO_SIMPLE_ROOT.items()
    }
    highest_root = tuple(
        sum((marks[node] * finite_roots[node][axis]
             for node in FINITE_NODE_TO_SIMPLE_ROOT), Q(0))
        for axis in range(8)
    )
    if highest_root not in roots:
        raise AssertionError("null marks do not construct an E8 root")
    if dot(highest_root, highest_root) != 2:
        raise AssertionError("highest root norm squared is not 2")

    affine_root = negate(highest_root)
    simple_by_node = {**finite_roots, 5: affine_root}
    if set(simple_by_node) != set(LINK_NODES):
        raise AssertionError("affine/finite root-node map is incomplete")

    null_sum = tuple(
        sum((marks[node] * simple_by_node[node][axis]
             for node in LINK_NODES), Q(0))
        for axis in range(8)
    )
    if null_sum != (Q(0),) * 8:
        raise AssertionError("primitive affine null-root relation failed")

    edge_pairs = []
    for node_a, node_b in combinations(LINK_NODES, 2):
        expected_inner = 2 * e10_gram[node_a][node_b]
        actual_inner = dot(simple_by_node[node_a], simple_by_node[node_b])
        if actual_inner != expected_inner:
            raise AssertionError(
                f"affine E8 Gram mismatch at nodes {node_a},{node_b}: "
                f"{actual_inner} != {expected_inner}"
            )
        if expected_inner == -1:
            edge_pairs.append((node_a, node_b))
    if len(edge_pairs) != 8:
        raise AssertionError("affine E8 diagram must have eight edges")

    generators = {
        node: affine_reflection(
            simple_by_node[node], Q(1) if node == 5 else Q(0)
        )
        for node in LINK_NODES
    }
    unit = affine_identity()
    for node, generator in generators.items():
        if affine_compose(generator, generator) != unit:
            raise AssertionError(f"affine reflection {node} is not involutive")

    adjacent_relations = 0
    commuting_relations = 0
    for node_a, node_b in combinations(LINK_NODES, 2):
        product_ab = affine_compose(generators[node_a], generators[node_b])
        if (node_a, node_b) in edge_pairs:
            cube = affine_compose(
                product_ab, affine_compose(product_ab, product_ab)
            )
            if cube != unit:
                raise AssertionError(
                    f"affine Coxeter order-three relation failed: {node_a},{node_b}"
                )
            adjacent_relations += 1
        else:
            reverse = affine_compose(generators[node_b], generators[node_a])
            if product_ab != reverse:
                raise AssertionError(
                    f"affine Coxeter commutation failed: {node_a},{node_b}"
                )
            commuting_relations += 1

    # The affine generator is s_0 = t_theta o s_theta. Therefore
    # s_0 o s_theta is the exact translation x -> x + theta.
    theta_reflection = affine_reflection(highest_root)
    affine_generator = generators[5]
    translation = affine_compose(affine_generator, theta_reflection)
    expected_translation = (identity(8), highest_root)
    if translation != expected_translation:
        raise AssertionError("affine reflection product did not yield translation by theta")

    return {
        "status": "PASS",
        "affine_link_type": "affine E8",
        "link_nodes": list(LINK_NODES),
        "link_edges": [list(edge) for edge in edge_pairs],
        "null_root_marks": {str(node): marks[node] for node in LINK_NODES},
        "null_root_marks_gcd": 1,
        "highest_root_coefficients_in_finite_simple_basis": [2, 3, 4, 6, 5, 4, 3, 2],
        "highest_root_norm_squared": str(dot(highest_root, highest_root)),
        "affine_root_norm_squared": str(dot(affine_root, affine_root)),
        "primitive_null_root_relation": [str(x) for x in null_sum],
        "affine_simple_root_gram_matches_e10_link": True,
        "affine_reflection_generators": len(generators),
        "involution_relations": len(generators),
        "adjacent_order_three_relations": adjacent_relations,
        "nonadjacent_commutations": commuting_relations,
        "total_pair_relations": adjacent_relations + commuting_relations,
        "translation_witness": {
            "product": "affine_reflection_at_node_5 after finite highest-root reflection",
            "translation_vector": [str(x) for x in highest_root],
            "exact_translation_by_highest_root": True,
        },
        "scope": (
            "Exact affine E8 root-system and affine-reflection realization "
            "for the E10 ideal-vertex link. This does not yet construct the "
            "5_21 Wythoffian, its vertex/facet incidence, or the global "
            "hyperbolic 6_21 honeycomb."
        ),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_audit(), indent=2, sort_keys=True))
