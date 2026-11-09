"""Exact E8 root-system sanity adapter; standard library only."""
from itertools import combinations, product

def dot(a, b):
    return sum(x*y for x, y in zip(a, b))

def build_roots():
    roots = []
    for i, j in combinations(range(8), 2):
        for si, sj in product((-1, 1), repeat=2):
            v = [0]*8
            v[i], v[j] = si, sj
            roots.append(tuple(v))
    for signs in product((-0.5, 0.5), repeat=8):
        if sum(x < 0 for x in signs) % 2 == 0:
            roots.append(tuple(signs))
    if len(roots) != 240 or len(set(roots)) != 240:
        raise AssertionError("E8 root cardinality/uniqueness failure")
    if any(dot(r, r) != 2 for r in roots):
        raise AssertionError("E8 root norm failure")
    return roots

def adjacency_summary():
    roots = build_roots()
    degrees = [sum(dot(a, b) == 1 for b in roots) for a in roots]
    edges = sum(degrees)//2
    return {
        "roots": len(roots),
        "edges_inner_product_1": edges,
        "degree_min": min(degrees),
        "degree_max": max(degrees),
        "regular_degree_56": all(d == 56 for d in degrees),
    }

if __name__ == "__main__":
    print(adjacency_summary())
