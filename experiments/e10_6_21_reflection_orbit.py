#!/usr/bin/env python3
"""Bounded exact root-orbit experiment for the 6_21 / E10 Coxeter group.

The coordinates are coefficients in the simple-root basis. The Gram matrix
has diagonal 1 and -1/2 on edges. For a root coefficient column c, reflection
in simple root i is c_i <- c_i - 2 (G c)_i.

This explores only roots reached within a finite word-length bound; it does
not enumerate the full infinite root system or construct the honeycomb.
"""
from fractions import Fraction
import argparse


def build_gram(arms=(6, 2, 1)):
    n = 1 + sum(arms)
    adjacency = [[0] * n for _ in range(n)]
    cursor = 1
    for arm in arms:
        previous = 0
        for _ in range(arm):
            adjacency[previous][cursor] = adjacency[cursor][previous] = 1
            previous = cursor
            cursor += 1
    return [[Fraction(int(i == j)) - Fraction(adjacency[i][j], 2)
             for j in range(n)] for i in range(n)]


def bilinear(a, b, gram):
    return sum(a[i] * gram[i][j] * b[j]
               for i in range(len(a)) for j in range(len(b)))


def reflect(vector, node, gram):
    out = list(vector)
    pairing = sum(gram[node][j] * vector[j] for j in range(len(vector)))
    out[node] -= 2 * pairing
    return tuple(out)


def root_orbit(max_depth=12):
    gram = build_gram()
    n = len(gram)
    simple_roots = {
        tuple(Fraction(int(i == j)) for i in range(n)) for j in range(n)
    }
    seen = set(simple_roots)
    frontier = set(simple_roots)
    layer_counts = [len(seen)]

    # Check each simple reflection preserves the full bilinear form on a basis.
    basis = [tuple(Fraction(int(i == j)) for i in range(n)) for j in range(n)]
    for node in range(n):
        reflected = [reflect(v, node, gram) for v in basis]
        for i in range(n):
            for j in range(n):
                assert bilinear(reflected[i], reflected[j], gram) == bilinear(
                    basis[i], basis[j], gram
                )

    for _ in range(max_depth):
        next_frontier = set()
        for root in frontier:
            for node in range(n):
                candidate = reflect(root, node, gram)
                if candidate not in seen:
                    assert bilinear(candidate, candidate, gram) == 1
                    assert all(value.denominator == 1 for value in candidate)
                    seen.add(candidate)
                    next_frontier.add(candidate)
        frontier = next_frontier
        layer_counts.append(len(seen))
        if not frontier:
            break

    assert all(bilinear(root, root, gram) == 1 for root in seen)
    return layer_counts, seen


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--depth", type=int, default=12)
    args = parser.parse_args()
    if args.depth < 0:
        parser.error("--depth must be non-negative")
    counts, roots = root_orbit(args.depth)
    print("diagram: [3^(6,2,1)] / hyperbolic E10 / 6_21")
    print(f"word-depth bound: {args.depth}")
    print(f"cumulative distinct real roots: {len(roots)}")
    print("cumulative counts by depth: " + ", ".join(map(str, counts)))
    print("checks: reflection preserves Gram form; all generated roots have norm 1")
    print("scope: finite-depth root orbit only; not the full root system or honeycomb")


if __name__ == "__main__":
    main()
