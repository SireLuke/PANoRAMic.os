"""Exact E8 root-system sanity adapter; standard library only."""
# --- repo-root bootstrap: makes this file runnable directly, from any
# working directory (the imports below address packages from the repo
# root). No-op when the root is already on sys.path. See
# docs/RUNNING_PYTHON.md.
import sys as _sys
from pathlib import Path as _Path

_REPO_ROOT = _Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in _sys.path:
    _sys.path.insert(0, str(_REPO_ROOT))
# --- end repo-root bootstrap ---

from core.geometry.e8_root_system import e8_roots_float

def dot(a, b):
    return sum(x*y for x, y in zip(a, b))

def build_roots():
    """Float compatibility view of the canonical exact E8 root set."""
    return list(e8_roots_float())

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
