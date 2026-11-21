"""Bounded, reference-based seed propagation over finite Menger cell graphs.

The base memory is immutable and content-addressed. Propagated nodes retain a
reference to that base plus a small local delta; they do not recursively copy
the inherited payload. This models safe context inheritance, not AI memory
internals or a ZIP archive format.
"""
from __future__ import annotations
from collections import deque
from dataclasses import dataclass
import hashlib
import itertools


class PropagationLimitExceeded(RuntimeError):
    pass


@dataclass(frozen=True)
class PropagationBudget:
    max_nodes: int = 20_000
    max_depth: int = 32
    max_delta_bytes: int = 1_000_000
    max_children_per_node: int = 6

    def __post_init__(self):
        if self.max_nodes < 1 or self.max_depth < 0 or self.max_delta_bytes < 0 or self.max_children_per_node < 1:
            raise ValueError("invalid propagation budget")


@dataclass(frozen=True)
class SeedNode:
    cell: tuple[int, int, int]
    base_digest: str
    parent: tuple[int, int, int] | None
    depth: int
    delta: bytes


def menger_cells(level: int):
    if isinstance(level, bool) or not isinstance(level, int) or level < 1:
        raise ValueError("level must be a positive integer")
    patterns = [p for p in itertools.product(range(3), repeat=3)
                if sum(v == 1 for v in p) <= 1]
    cells = [(0, 0, 0)]
    for _ in range(level):
        cells = [tuple(3*c[i] + p[i] for i in range(3))
                 for c in cells for p in patterns]
    return cells


def face_graph(cells):
    index = set(cells)
    graph = {cell: [] for cell in cells}
    for cell in cells:
        for axis in range(3):
            neighbor = list(cell)
            neighbor[axis] += 1
            neighbor = tuple(neighbor)
            if neighbor in index:
                graph[cell].append(neighbor)
                graph[neighbor].append(cell)
    return graph


def propagate_seed(cells, base_memory: bytes, *, budget=None, delta_factory=None):
    """BFS propagation with immutable shared base and bounded per-cell deltas."""
    limits = budget or PropagationBudget()
    if not isinstance(base_memory, bytes) or not base_memory:
        raise ValueError("base_memory must be non-empty bytes")
    graph = face_graph(cells)
    root = min(cells)
    digest = hashlib.sha256(base_memory).hexdigest()
    make_delta = delta_factory or (lambda cell, depth: b"")
    nodes = {}
    pending = deque([(root, None, 0)])
    total_delta = 0
    while pending:
        cell, parent, depth = pending.popleft()
        if cell in nodes:
            continue
        if len(nodes) >= limits.max_nodes:
            raise PropagationLimitExceeded("node budget exceeded")
        if depth > limits.max_depth:
            raise PropagationLimitExceeded("depth budget exceeded")
        delta = make_delta(cell, depth)
        if not isinstance(delta, bytes):
            raise TypeError("delta_factory must return bytes")
        if total_delta + len(delta) > limits.max_delta_bytes:
            raise PropagationLimitExceeded("aggregate delta-byte budget exceeded")
        total_delta += len(delta)
        nodes[cell] = SeedNode(cell, digest, parent, depth, delta)
        children = sorted(graph[cell])
        if len(children) > limits.max_children_per_node:
            raise PropagationLimitExceeded("per-node fanout budget exceeded")
        for child in children:
            if child not in nodes:
                pending.append((child, cell, depth + 1))
    if len(nodes) != len(cells):
        raise PropagationLimitExceeded("graph not fully covered within declared limits")
    if any(node.base_digest != digest for node in nodes.values()):
        raise AssertionError("base reference drift")
    if hashlib.sha256(base_memory).hexdigest() != digest:
        raise AssertionError("base memory mutated during propagation")
    return {
        "base_digest": digest,
        "base_bytes": len(base_memory),
        "nodes": nodes,
        "node_count": len(nodes),
        "delta_bytes": total_delta,
        "reference_storage_bytes": len(digest) * len(nodes) + total_delta,
        "naive_copy_bytes": len(base_memory) * len(nodes) + total_delta,
        "base_memory_unchanged": True,
    }
