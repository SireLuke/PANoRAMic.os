#!/usr/bin/env python3
"""Six bounded exact-arithmetic diagnostics for 6_21 / hyperbolic E10."""
from fractions import Fraction
from math import log
import argparse


def gram_from_arms(arms):
    n = 1 + sum(arms)
    adjacency = [[0] * n for _ in range(n)]
    cursor = 1
    for arm in arms:
        previous = 0
        for _ in range(arm):
            adjacency[previous][cursor] = adjacency[cursor][previous] = 1
            previous, cursor = cursor, cursor + 1
    return [[Fraction(int(i == j)) - Fraction(adjacency[i][j], 2)
             for j in range(n)] for i in range(n)]


def ldl_diagonal(matrix):
    n = len(matrix)
    lower = [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]
    diagonal = []
    for k in range(n):
        pivot = matrix[k][k] - sum(lower[k][j]**2 * diagonal[j]
                                   for j in range(k))
        if pivot == 0:
            return diagonal + [Fraction(0)]
        diagonal.append(pivot)
        for i in range(k + 1, n):
            numerator = matrix[i][k] - sum(
                lower[i][j] * lower[k][j] * diagonal[j] for j in range(k))
            lower[i][k] = numerator / pivot
    return diagonal


def product(values):
    result = Fraction(1)
    for value in values:
        result *= value
    return result


def inertia_det(matrix):
    d = ldl_diagonal(matrix)
    return (sum(x > 0 for x in d), sum(x < 0 for x in d),
            sum(x == 0 for x in d), product(d))


def reflect(v, node, gram):
    out = list(v)
    out[node] -= 2 * sum(gram[node][j] * v[j] for j in range(len(v)))
    return tuple(out)


def matmul(a, b):
    n = len(a)
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(n))
                       for j in range(n)) for i in range(n))


def generators(gram):
    n = len(gram)
    result = []
    for node in range(n):
        m = [[int(i == j) for j in range(n)] for i in range(n)]
        for j in range(n):
            m[node][j] -= int(2 * gram[node][j])
        result.append(tuple(tuple(row) for row in m))
    return result


def root_growth(depth, gram):
    n = len(gram)
    roots = {tuple(Fraction(int(i == j)) for i in range(n)) for j in range(n)}
    frontier = set(roots)
    counts = [len(roots)]
    for _ in range(depth):
        nxt = set()
        for root in frontier:
            for node in range(n):
                candidate = reflect(root, node, gram)
                if candidate not in roots:
                    assert sum(candidate[i]*gram[i][j]*candidate[j]
                               for i in range(n) for j in range(n)) == 1
                    assert all(x.denominator == 1 for x in candidate)
                    roots.add(candidate)
                    nxt.add(candidate)
        frontier = nxt
        counts.append(len(roots))
    return counts


def chamber_patch(depth, gram):
    n = len(gram)
    gens = generators(gram)
    identity = tuple(tuple(int(i == j) for j in range(n)) for i in range(n))
    seen, frontier = {identity}, {identity}
    counts = [1]
    for _ in range(depth):
        nxt = set()
        for chamber in frontier:
            for generator in gens:
                candidate = matmul(generator, chamber)
                if candidate not in seen:
                    seen.add(candidate)
                    nxt.add(candidate)
        frontier = nxt
        counts.append(len(seen))
    return counts, seen, gens


def chamber_adjacency(chambers, gens):
    directed = boundary = 0
    for chamber in chambers:
        for generator in gens:
            neighbor = matmul(generator, chamber)
            directed += 1
            if neighbor not in chambers:
                boundary += 1
            else:
                assert matmul(generator, neighbor) == chamber
    return directed, boundary


def vertex_subdiagrams():
    data = {
        "finite_E8": ((4, 2, 1), (8, 0, 0, Fraction(1, 256))),
        "affine_E9": ((5, 2, 1), (8, 0, 1, Fraction(0))),
        "hyperbolic_E10": ((6, 2, 1), (9, 1, 0, Fraction(-1, 1024))),
    }
    observed = {}
    for name, (arms, expected) in data.items():
        observed[name] = inertia_det(gram_from_arms(arms))
        assert observed[name] == expected, (name, observed[name], expected)
    return observed


def sierpinski_simplex(level, dimension):
    return (dimension + 1)**level, log(dimension + 1, 2)


def dimensional_ladder():
    return [(1 + sum(arms), arms, inertia_det(gram_from_arms(arms)))
            for arms in [(m, 2, 1) for m in range(4, 9)]]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--root-depth", type=int, default=12)
    p.add_argument("--chamber-depth", type=int, default=3)
    p.add_argument("--sierpinski-level", type=int, default=4)
    args = p.parse_args()
    if min(args.root_depth, args.chamber_depth, args.sierpinski_level) < 0:
        p.error("depths and level must be non-negative")
    g = gram_from_arms((6, 2, 1))
    assert inertia_det(g) == (9, 1, 0, Fraction(-1, 1024))
    a = root_growth(args.root_depth, g)
    b, chambers, gens = chamber_patch(args.chamber_depth, g)
    c = chamber_adjacency(chambers, gens)
    d = vertex_subdiagrams()
    e8 = sierpinski_simplex(args.sierpinski_level, 8)
    e9 = sierpinski_simplex(args.sierpinski_level, 9)
    f = dimensional_ladder()
    print("6_21 / hyperbolic E10: six bounded experiments")
    print("A root growth:", a)
    print("B distinct chambers:", b)
    print("C chamber graph directed edges / boundary edges:", c)
    print("D exact E8 / affine E9 / E10 subdiagrams:", d)
    print("E Sierpinski corner-simplex level", args.sierpinski_level,
          "8D pieces/dimension", e8, "9D pieces/dimension", e9)
    print("F star-diagram dimensional ladder:", f)
    print("PASS: exact algebraic invariants and finite chamber adjacency")
    print("LIMIT: not a complete 6_21 honeycomb construction or cell-incidence proof")


if __name__ == "__main__":
    main()
