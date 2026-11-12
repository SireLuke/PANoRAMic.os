#!/usr/bin/env python3
"""Numerical horosphere section of the ideal E10 Coxeter-simplex vertex.

The Lorentzian simplex coordinates and Coxeter data remain exact rational
inputs. Hyperboloid normalization and horosphere intersections use floats
because they require square roots. This constructs the chamber cross-section
at the ideal vertex; it does not claim a complete 6_21 honeycomb.
"""
from __future__ import annotations

from fractions import Fraction as Q
from math import acos, pi, sqrt


def identity(n):
    return [[Q(int(i == j)) for j in range(n)] for i in range(n)]


def gram_from_arms(arms=(6, 2, 1)):
    n = 1 + sum(arms)
    adjacency = [[0] * n for _ in range(n)]
    cursor = 1
    for length in arms:
        previous = 0
        for _ in range(length):
            adjacency[previous][cursor] = adjacency[cursor][previous] = 1
            previous, cursor = cursor, cursor + 1
    return [[Q(int(i == j)) - Q(adjacency[i][j], 2)
             for j in range(n)] for i in range(n)]


def transpose(a):
    return [list(row) for row in zip(*a)]


def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def inverse(a):
    n = len(a)
    work = [list(map(Q, row)) + identity(n)[i] for i, row in enumerate(a)]
    for col in range(n):
        pivot = next(r for r in range(col, n) if work[r][col])
        work[col], work[pivot] = work[pivot], work[col]
        value = work[col][col]
        work[col] = [x / value for x in work[col]]
        for row in range(n):
            if row != col:
                factor = work[row][col]
                work[row] = [x - factor * y
                             for x, y in zip(work[row], work[col])]
    return [row[n:] for row in work]


def ldl(a):
    n = len(a)
    lower = identity(n)
    diagonal = []
    for k in range(n):
        pivot = a[k][k] - sum(lower[k][j] ** 2 * diagonal[j]
                              for j in range(k))
        if not pivot:
            raise ArithmeticError("zero LDL pivot")
        diagonal.append(pivot)
        for i in range(k + 1, n):
            numerator = a[i][k] - sum(
                lower[i][j] * lower[k][j] * diagonal[j] for j in range(k))
            lower[i][k] = numerator / pivot
    return lower, diagonal


def minkowski_dot(a, b, metric):
    return sum(a[i] * float(metric[i]) * b[i] for i in range(len(a)))


def matrix_rank(rows, tolerance=1e-9):
    work = [list(map(float, row)) for row in rows]
    if not work:
        return 0
    m, n = len(work), len(work[0])
    rank = 0
    for col in range(n):
        pivot = max(range(rank, m), key=lambda r: abs(work[r][col]),
                    default=rank)
        if rank >= m or abs(work[pivot][col]) <= tolerance:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        scale = work[rank][col]
        work[rank] = [x / scale for x in work[rank]]
        for r in range(m):
            if r != rank:
                factor = work[r][col]
                work[r] = [x - factor * y
                           for x, y in zip(work[r], work[rank])]
        rank += 1
        if rank == m:
            break
    return rank



def inverse_float(matrix):
    n = len(matrix)
    work = [list(map(float, row)) + [float(i == j) for j in range(n)]
            for i, row in enumerate(matrix)]
    for column in range(n):
        pivot = max(range(column, n),
                    key=lambda row: abs(work[row][column]))
        if abs(work[pivot][column]) < 1e-14:
            raise ArithmeticError("singular Euclidean edge Gram matrix")
        work[column], work[pivot] = work[pivot], work[column]
        scale = work[column][column]
        work[column] = [value / scale for value in work[column]]
        for row in range(n):
            if row == column:
                continue
            factor = work[row][column]
            work[row] = [value - factor * pivot_value
                         for value, pivot_value in zip(work[row], work[column])]
    return [row[n:] for row in work]


def cusp_simplex_metric_audit(points, metric, coxeter_gram, ideal_node=6,
                              tolerance=1e-7):
    """Recover the Euclidean simplex metric and its 36 internal dihedral angles.

    Each section facet is identified with the corresponding non-ideal wall.
    The expected cusp-link angle is pi/3 for adjacent Coxeter nodes and pi/2
    for nonadjacent nodes. This is a numerical reconstruction from the
    horosphere coordinates, checked against the exact rational Coxeter Gram.
    """
    if len(points) != 9:
        raise AssertionError("an 8-simplex section must have nine vertices")
    base = points[0][1]
    edge_vectors = [
        [point[1][k] - base[k] for k in range(10)]
        for point in points[1:]
    ]
    edge_gram = [
        [minkowski_dot(left, right, metric) for right in edge_vectors]
        for left in edge_vectors
    ]
    inverse_edge_gram = inverse_float(edge_gram)

    # The Euclidean dual edge vectors v_i satisfy <v_i,e_j>=delta_ij.
    # Outward normals are -v_i for facets i>=1 and sum(v_i) for facet 0.
    # Their pairwise inner products are read directly from G_edge^{-1}.
    facet_nodes = [points[0][0]] + [point[0] for point in points[1:]]
    angle_records = []
    angle_counts = {"pi/3": 0, "pi/2": 0}
    adjacency_matches = 0
    for i in range(9):
        for j in range(i + 1, 9):
            if i == 0:
                dot_out = -sum(inverse_edge_gram[k][j - 1]
                               for k in range(8))
                norm_i = sum(sum(row) for row in inverse_edge_gram)
                norm_j = inverse_edge_gram[j - 1][j - 1]
            elif j == 0:
                raise AssertionError("facet pair ordering invariant violated")
            else:
                dot_out = inverse_edge_gram[i - 1][j - 1]
                norm_i = inverse_edge_gram[i - 1][i - 1]
                norm_j = inverse_edge_gram[j - 1][j - 1]
            cosine_internal = -dot_out / sqrt(norm_i * norm_j)
            cosine_internal = max(-1.0, min(1.0, cosine_internal))
            angle = acos(cosine_internal)
            node_i, node_j = facet_nodes[i], facet_nodes[j]
            expected_adjacent = coxeter_gram[node_i][node_j] == Q(-1, 2)
            expected_angle = pi / 3 if expected_adjacent else pi / 2
            if abs(angle - expected_angle) > tolerance:
                raise AssertionError(
                    f"cusp dihedral mismatch for Coxeter nodes "
                    f"{node_i},{node_j}: {angle} vs {expected_angle}"
                )
            label = "pi/3" if expected_adjacent else "pi/2"
            angle_counts[label] += 1
            adjacency_matches += int(expected_adjacent)
            angle_records.append({
                "facet_nodes": [node_i, node_j],
                "angle": label,
                "angle_radians": angle,
            })

    distance_records = []
    for i in range(9):
        for j in range(i + 1, 9):
            delta = [points[i][1][k] - points[j][1][k]
                     for k in range(10)]
            distance_records.append({
                "vertex_nodes": [points[i][0], points[j][0]],
                "squared_distance": minkowski_dot(delta, delta, metric),
            })
    if len(angle_records) != 36 or len(distance_records) != 36:
        raise AssertionError("simplex metric audit must contain 36 pairs")
    if angle_counts != {"pi/3": 8, "pi/2": 28}:
        raise AssertionError(f"unexpected affine-E8 cusp angle counts: {angle_counts}")
    return {
        "facet_node_order": facet_nodes,
        "dihedral_pair_count": len(angle_records),
        "dihedral_angle_counts": angle_counts,
        "coxeter_adjacency_edges": adjacency_matches,
        "all_angles_match_affine_E8_link": True,
        "dihedral_angles": angle_records,
        "edge_pair_count": len(distance_records),
        "squared_edge_lengths": distance_records,
        "numerical_tolerance_radians": tolerance,
    }


def run_horosphere_audit():
    g = gram_from_arms()
    lower, diagonal = ldl(g)
    lower_inverse = inverse(lower)
    # In an orthogonal Lorentz frame, G = L J L^T. The dual columns
    # are J^{-1} L^{-1} and have Gram matrix G^{-1}.
    dual = matmul(
        [[Q(1, 1) / x if i == j else Q(0)
          for j, x in enumerate(diagonal)] for i, _ in enumerate(diagonal)],
        lower_inverse,
    )
    dual_gram = matmul(transpose(dual), matmul(
        [[diagonal[i] if i == j else Q(0)
          for j in range(10)] for i in range(10)], dual))
    assert dual_gram == inverse(g)

    ideal_node = 6
    metric = diagonal
    p = [-float(dual[i][ideal_node]) for i in range(10)]
    p_norm = minkowski_dot(p, p, metric)
    if abs(p_norm) > 1e-10 or p[-1] <= 0:
        raise AssertionError("ideal ray is not future-pointing null")

    points = []
    intersection_residuals = []
    for node in range(10):
        if node == ideal_node:
            continue
        q = [-float(dual[i][node]) for i in range(10)]
        q_norm = minkowski_dot(q, q, metric)
        if q_norm >= 0:
            raise AssertionError(f"dual vertex {node} is not timelike")
        scale = sqrt(-q_norm)
        q = [x / scale for x in q]
        c = minkowski_dot(q, p, metric)
        if c >= 0:
            raise AssertionError("finite and ideal rays are not in one future cone")
        b = -1.0 / c
        a = (b * b - 1.0) / (2.0 * b * c)
        x = [a * p[k] + b * q[k] for k in range(10)]
        norm_residual = abs(minkowski_dot(x, x, metric) + 1.0)
        horosphere_residual = abs(minkowski_dot(x, p, metric) + 1.0)
        if norm_residual > 1e-8 or horosphere_residual > 1e-8:
            raise AssertionError("horosphere intersection residual too large")
        points.append((node, x))
        intersection_residuals.append(max(norm_residual, horosphere_residual))

    # Differences of points on one horosphere lie in p-perp modulo the
    # null direction; their Lorentz norms give the induced Euclidean metric.
    distance_squared = []
    for i in range(len(points)):
        row = []
        for j in range(len(points)):
            delta = [points[i][1][k] - points[j][1][k] for k in range(10)]
            value = minkowski_dot(delta, delta, metric)
            if value < -1e-8:
                raise AssertionError("horosphere separation is not Euclidean")
            row.append(max(0.0, value))
        distance_squared.append(row)

    base = points[0][1]
    edge_vectors = [[point[1][k] - base[k] for k in range(10)]
                    for point in points[1:]]
    affine_rank = matrix_rank(edge_vectors)
    nonzero_distances = [
        distance_squared[i][j]
        for i in range(9) for j in range(i + 1, 9)
    ]
    if affine_rank != 8 or min(nonzero_distances) <= 1e-10:
        raise AssertionError("horosphere section is not a nondegenerate 8-simplex")

    cusp_metric = cusp_simplex_metric_audit(points, metric, g, ideal_node)

    return {
        "status": "PASS",
        "ambient_signature": (9, 1),
        "ideal_vertex_node": ideal_node,
        "ideal_ray_null_norm": p_norm,
        "ideal_ray_future_time_coordinate": p[-1],
        "finite_vertices_intersected": len(points),
        "horosphere_level": -1.0,
        "hyperboloid_level": -1.0,
        "max_intersection_residual": max(intersection_residuals),
        "horosphere_section_vertex_nodes": [node for node, _ in points],
        "horosphere_section_affine_rank": affine_rank,
        "horosphere_section_dimension": 8,
        "minimum_pairwise_euclidean_distance_squared": min(nonzero_distances),
        "maximum_pairwise_euclidean_distance_squared": max(nonzero_distances),
        "cusp_simplex_metric_audit": cusp_metric,
        "scope": (
            "Constructs the 8-dimensional Euclidean horosphere section of "
            "one E10 Coxeter chamber at its ideal vertex. This is a local "
            "cusp cross-section, not a construction or completeness proof "
            "for the full hyperbolic 6_21 honeycomb."
        ),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_horosphere_audit(), indent=2, sort_keys=True))
