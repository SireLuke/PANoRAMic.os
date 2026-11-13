"""Explicit E7 root-stabilizer action inside the exact E8 root system.

Constructs an E7 simple system in the roots perpendicular to a selected E8
root, then represents its seven simple reflections as permutations of the
126-root subsystem. It does not enumerate all 2,903,040 group elements.
"""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from fractions import Fraction as Q
from math import prod

from core.geometry.e8_root_system import Root, dot, e8_roots_exact

E7_EXPONENTS = (1, 5, 7, 9, 11, 13, 17)
E7_WEYL_ORDER = prod(e + 1 for e in E7_EXPONENTS)
E7_EXPECTED_WEYL_ORDER = 2_903_040
E7_ROOT_COUNT = 126
# A deterministic generic vector in the selected root's orthogonal space.
_POSITIVE_WITNESS = (-5, 5, 1, 0, 5, 10, -9, -8)


def reflect(vector: Root, root: Root) -> Root:
    """Exact simply-laced reflection: v -> v - (v.root) root."""
    if dot(root, root) != 2:
        raise ValueError("reflection root must have squared norm 2")
    coefficient = dot(vector, root)
    return tuple(x - coefficient * a for x, a in zip(vector, root))


def _rank(rows: tuple[Root, ...]) -> int:
    """Exact row rank over Q."""
    matrix = [[Q(x) for x in row] for row in rows]
    if not matrix:
        return 0
    pivot_row = 0
    for col in range(len(matrix[0])):
        pivot = next((r for r in range(pivot_row, len(matrix))
                      if matrix[r][col] != 0), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = matrix[pivot_row][col]
        matrix[pivot_row] = [x / scale for x in matrix[pivot_row]]
        for r in range(len(matrix)):
            if r != pivot_row and matrix[r][col] != 0:
                factor = matrix[r][col]
                matrix[r] = [a - factor * b for a, b in
                             zip(matrix[r], matrix[pivot_row])]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return pivot_row


def _positive_simple_roots(orthogonal_roots: tuple[Root, ...]) -> tuple[Root, ...]:
    witness = tuple(Q(x) for x in _POSITIVE_WITNESS)
    if any(dot(witness, root) == 0 for root in orthogonal_roots):
        raise AssertionError("positive-system witness is not generic")
    positive = {root for root in orthogonal_roots if dot(witness, root) > 0}
    simple = []
    for alpha in positive:
        if not any(tuple(alpha[i] - beta[i] for i in range(8)) in positive
                   for beta in positive):
            simple.append(alpha)
    return tuple(sorted(simple))


def _is_e7_gram(simple_roots: tuple[Root, ...]) -> bool:
    if len(simple_roots) != 7 or _rank(simple_roots) != 7:
        return False
    edges = {(i, j) for i in range(7) for j in range(i + 1, 7)
             if dot(simple_roots[i], simple_roots[j]) == -1}
    expected = {(0, 2), (0, 4), (1, 2), (2, 3), (3, 6), (5, 6)}
    for i in range(7):
        for j in range(i + 1, 7):
            value = dot(simple_roots[i], simple_roots[j])
            if value != (-1 if (i, j) in expected else 0):
                return False
    return edges == expected


@dataclass(frozen=True)
class E7StabilizerAction:
    selected_e8_root: Root
    roots: tuple[Root, ...]
    simple_roots: tuple[Root, ...]
    generators: tuple[tuple[int, ...], ...]

    @classmethod
    def build(cls, selected_e8_root: Root | None = None) -> "E7StabilizerAction":
        e8_roots = e8_roots_exact()
        selected = e8_roots[0] if selected_e8_root is None else selected_e8_root
        if selected not in set(e8_roots):
            raise ValueError("selected vector is not an E8 root")
        perpendicular = tuple(root for root in e8_roots
                              if dot(selected, root) == 0)
        if len(perpendicular) != E7_ROOT_COUNT:
            raise AssertionError("selected root does not have 126 perpendicular roots")
        simple = _positive_simple_roots(perpendicular)
        if not _is_e7_gram(simple):
            raise AssertionError("derived simple-root Gram matrix is not E7")
        index = {root: i for i, root in enumerate(perpendicular)}
        generators = []
        for alpha in simple:
            permutation = tuple(index[reflect(root, alpha)] for root in perpendicular)
            if sorted(permutation) != list(range(E7_ROOT_COUNT)):
                raise AssertionError("E7 reflection is not a permutation of perpendicular roots")
            if any(permutation[permutation[i]] != i for i in range(E7_ROOT_COUNT)):
                raise AssertionError("E7 simple reflection is not involutive")
            if any(dot(selected, reflect(root, alpha)) != 0 for root in perpendicular):
                raise AssertionError("E7 reflection escaped the perpendicular subsystem")
            generators.append(permutation)
        return cls(selected, perpendicular, simple, tuple(generators))

    def orbit_indices(self, seed_index: int = 0) -> frozenset[int]:
        if not 0 <= seed_index < len(self.roots):
            raise IndexError("seed index outside E7 root subsystem")
        seen = {seed_index}
        queue = deque([seed_index])
        while queue:
            current = queue.popleft()
            for generator in self.generators:
                image = generator[current]
                if image not in seen:
                    seen.add(image)
                    queue.append(image)
        return frozenset(seen)

    def validate(self) -> bool:
        if len(self.roots) != E7_ROOT_COUNT or len(self.simple_roots) != 7:
            raise AssertionError("E7 root/simple-root cardinality mismatch")
        if len(self.generators) != 7:
            raise AssertionError("expected seven simple reflection generators")
        if not _is_e7_gram(self.simple_roots):
            raise AssertionError("simple roots do not have E7 Cartan/Gram graph")
        if any(dot(self.selected_e8_root, root) != 0 for root in self.roots):
            raise AssertionError("perpendicular-root membership failure")
        if len(self.orbit_indices()) != E7_ROOT_COUNT:
            raise AssertionError("E7 generators are not transitive on 126 roots")
        # The roots span the 7D orthogonal space, so this permutation action
        # is faithful: an element fixing every root fixes the whole space.
        if _rank(self.roots) != 7:
            raise AssertionError("perpendicular roots do not span the E7 space")
        return True


def audit_e7_stabilizer() -> dict[str, int | bool]:
    action = E7StabilizerAction.build()
    action.validate()
    root_orbit_size = len(action.orbit_indices())
    stabilizer_of_root = E7_WEYL_ORDER // root_orbit_size
    if E7_WEYL_ORDER != E7_EXPECTED_WEYL_ORDER:
        raise AssertionError("E7 Weyl order/exponent product mismatch")
    if E7_WEYL_ORDER * 240 != 696_729_600:
        raise AssertionError("E8/E7 orbit-stabilizer cross-check failed")
    return {
        "e8_selected_root_orbit": 240,
        "e7_perpendicular_roots": len(action.roots),
        "e7_simple_reflection_generators": len(action.generators),
        "e7_root_orbit_size": root_orbit_size,
        "e7_weyl_order_from_exponents": E7_WEYL_ORDER,
        "e7_root_stabilizer_order_derived": stabilizer_of_root,
        "faithful_action_on_7d_span": True,
        "explicit_group_element_enumeration": False,
    }
