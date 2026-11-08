#!/usr/bin/env python3
"""Reproduce the E8/Gosset 4_21 Sierpinski Coxeter-plane experiment.

Pure Python standard library; no NumPy/SciPy dependency.
"""
from collections import deque
from itertools import combinations, product
from math import sqrt

TOL = 1e-8
PROJECTION = (
    (0.0, -0.119117702264, -0.192736490926, -0.217638871657,
     -0.192736490926, -0.119117702264, 0.0, -0.921933054885),
    (-0.096899068700, -0.463505659945, -0.236930326056, 0.0,
     0.236930326056, 0.463505659945, 0.669823572348, 0.0),
)
SIMPLE_ROOTS = (
    (0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, 0.5),
    (1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
    (-1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
    (0.0, -1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0),
    (0.0, 0.0, -1.0, 1.0, 0.0, 0.0, 0.0, 0.0),
    (0.0, 0.0, 0.0, -1.0, 1.0, 0.0, 0.0, 0.0),
    (0.0, 0.0, 0.0, 0.0, -1.0, 1.0, 0.0, 0.0),
    (0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 1.0, 0.0),
)


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def reflect(x, alpha):
    coefficient = dot(x, alpha)
    return tuple(round(xi - coefficient * ai, 8)
                 for xi, ai in zip(x, alpha))


def build_e8_roots():
    roots = []
    # 112 roots with two nonzero integer coordinates.
    for i, j in combinations(range(8), 2):
        for si, sj in product((-1.0, 1.0), repeat=2):
            v = [0.0] * 8
            v[i], v[j] = si, sj
            roots.append(tuple(v))
    # 128 half-integer roots with an even number of minus signs.
    for signs in product((-0.5, 0.5), repeat=8):
        if sum(value < 0 for value in signs) % 2 == 0:
            roots.append(tuple(signs))
    assert len(roots) == 240 and len(set(roots)) == 240
    assert all(dot(root, root) == 2 for root in roots)
    return roots


def project(root):
    return tuple(dot(row, root) for row in PROJECTION)


def relative_side_spread(points):
    lengths = (
        sqrt(sum((points[0][i] - points[1][i]) ** 2 for i in range(2))),
        sqrt(sum((points[1][i] - points[2][i]) ** 2 for i in range(2))),
        sqrt(sum((points[2][i] - points[0][i]) ** 2 for i in range(2))),
    )
    mean = sum(lengths) / 3
    return (max(lengths) - min(lengths)) / mean if mean else float("inf")


def coxeter_map(root):
    # c = s_0 s_1 ... s_7 acting on column vectors:
    # apply s_7 first, then ... s_0.
    value = root
    for alpha in reversed(SIMPLE_ROOTS):
        value = reflect(value, alpha)
    return value


def main():
    roots = build_e8_roots()
    root_index = {root: index for index, root in enumerate(roots)}
    projected = [project(root) for root in roots]

    # E8 edges: root inner product 1.
    adjacency = [
        {j for j, other in enumerate(roots) if dot(root, other) == 1}
        for root in roots
    ]
    edge_count = sum(map(len, adjacency)) // 2
    assert edge_count == 6720
    assert all(len(neighbors) == 56 for neighbors in adjacency)

    # Enumerate 3-cliques in the edge graph. Each has all three 8D side
    # lengths sqrt(2), so it is an equilateral triangular face.
    faces = []
    for i in range(240):
        for j in adjacency[i]:
            if j > i:
                for k in adjacency[i].intersection(adjacency[j]):
                    if k > j:
                        faces.append((i, j, k))
    assert len(faces) == 60480

    # Full Weyl-group transitivity on triangular faces via simple reflections.
    reflection_maps = []
    for alpha in SIMPLE_ROOTS:
        reflection_maps.append([
            root_index[reflect(root, alpha)] for root in roots
        ])
    visited = {faces[0]}
    queue = deque([faces[0]])
    while queue:
        face = queue.popleft()
        for mapping in reflection_maps:
            image = tuple(sorted(mapping[index] for index in face))
            if image not in visited:
                visited.add(image)
                queue.append(image)
    assert len(visited) == len(faces)

    # Count faces that remain equilateral after the specified Coxeter-plane
    # projection.
    projected_equilateral = []
    for face in faces:
        spread = relative_side_spread([projected[index] for index in face])
        if spread < TOL:
            projected_equilateral.append(face)
    assert len(projected_equilateral) == 2160

    # The Coxeter element has order 30. Verify its action on all roots.
    c_map = [root_index[coxeter_map(root)] for root in roots]
    current = list(range(240))
    for _ in range(30):
        current = [c_map[index] for index in current]
    assert current == list(range(240))

    # Partition the projected-equilateral subset into C30 orbits.
    remaining = set(projected_equilateral)
    orbit_sizes = []
    while remaining:
        seed = next(iter(remaining))
        orbit = set()
        current_face = seed
        for _ in range(30):
            orbit.add(tuple(sorted(c_map[index] for index in current_face)))
            current_face = tuple(sorted(c_map[index] for index in current_face))
        orbit_sizes.append(len(orbit))
        remaining.difference_update(orbit)
    assert len(orbit_sizes) == 72 and set(orbit_sizes) == {30}

    # All 8D edges are equilateral by construction: |a-b|^2=2.
    # Gosset/Weyl group order divided by face orbit gives face stabilizer.
    stabilizer_order = 696729600 // len(faces)
    assert stabilizer_order == 11520

    print("E8 roots / Gosset vertices:", len(roots))
    print("Gosset edges:", edge_count)
    print("8D equilateral triangular faces:", len(faces))
    print("W(E8) orbit from one face:", len(visited))
    print("Setwise triangular-face stabilizer:", stabilizer_order)
    print("Coxeter-plane equilateral projected faces:", len(projected_equilateral))
    print("C30 orbit count / sizes:", len(orbit_sizes), sorted(set(orbit_sizes)))
    print("PASS")


if __name__ == "__main__":
    main()
