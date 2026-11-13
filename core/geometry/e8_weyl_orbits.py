"""Exact finite Weyl-group action on the canonical E8 root system.

The implementation constructs the eight simple reflections as permutations
of the 240 exact roots. It explores root orbits by generator BFS; it does not
enumerate the 696,729,600 elements of W(E8).
"""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from fractions import Fraction
from math import prod
from typing import Iterable

from core.geometry.e8_root_system import (
    Root, dot, e8_roots_exact, e8_simple_roots_exact,
)

E8_EXPONENTS = (1, 7, 11, 13, 17, 19, 23, 29)
E8_WEYL_ORDER = prod(exponent + 1 for exponent in E8_EXPONENTS)
E8_EXPECTED_WEYL_ORDER = 696_729_600


def reflect_root(vector: Root, simple_root: Root) -> Root:
    """Apply s_alpha(v) = v - 2(v,alpha)/(alpha,alpha) alpha."""
    denominator = dot(simple_root, simple_root)
    if denominator != 2:
        raise ValueError("E8 simple roots must have squared norm 2")
    coefficient = dot(vector, simple_root)
    return tuple(x - coefficient * a for x, a in zip(vector, simple_root))


@dataclass(frozen=True)
class E8WeylAction:
    roots: tuple[Root, ...]
    simple_roots: tuple[Root, ...]
    generators: tuple[tuple[int, ...], ...]

    @classmethod
    def build(cls) -> "E8WeylAction":
        roots = e8_roots_exact()
        simple_roots = e8_simple_roots_exact()
        index = {root: i for i, root in enumerate(roots)}
        generators = []
        for alpha in simple_roots:
            permutation = tuple(index[reflect_root(root, alpha)] for root in roots)
            if sorted(permutation) != list(range(len(roots))):
                raise AssertionError("simple reflection is not a root permutation")
            if any(permutation[permutation[i]] != i for i in range(len(roots))):
                raise AssertionError("simple reflection is not involutive")
            generators.append(permutation)
        return cls(roots, simple_roots, tuple(generators))

    def orbit_indices(self, seed_index: int) -> frozenset[int]:
        if not 0 <= seed_index < len(self.roots):
            raise IndexError("seed index outside E8 root set")
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

    def root_orbit(self, seed: Root) -> frozenset[Root]:
        try:
            seed_index = self.roots.index(seed)
        except ValueError as exc:
            raise ValueError("seed is not an E8 root") from exc
        return frozenset(self.roots[i] for i in self.orbit_indices(seed_index))

    def orbit_partition(self) -> tuple[frozenset[int], ...]:
        remaining = set(range(len(self.roots)))
        orbits = []
        while remaining:
            seed = min(remaining)
            orbit = self.orbit_indices(seed)
            orbits.append(orbit)
            remaining.difference_update(orbit)
        return tuple(orbits)

    def orthogonal_root_count(self, seed: Root) -> int:
        if seed not in set(self.roots):
            raise ValueError("seed is not an E8 root")
        return sum(dot(seed, root) == 0 for root in self.roots)


@dataclass(frozen=True)
class E8RootStabilizerAudit:
    seed: Root
    orbit_size: int
    weyl_group_order: int
    stabilizer_order: int
    orthogonal_root_count: int

    @property
    def orbit_stabilizer_product(self) -> int:
        return self.orbit_size * self.stabilizer_order

    def validate(self) -> bool:
        if self.orbit_size <= 0 or self.stabilizer_order <= 0:
            raise ValueError("orbit and stabilizer orders must be positive")
        if self.orbit_stabilizer_product != self.weyl_group_order:
            raise ValueError("orbit-stabilizer identity failed")
        if self.orthogonal_root_count != 126:
            raise ValueError("root perpendicular subsystem is not the expected E7 system")
        return True


def audit_e8_root_orbits(seed: Root | None = None) -> E8RootStabilizerAudit:
    """Audit the root orbit and derive its stabilizer order exactly.

    |W(E8)| is computed from the E8 exponents. The orbit is computed directly
    from the simple-reflection generators. The stabilizer order then follows
    from orbit-stabilizer; it is not obtained by enumerating group elements.
    """
    if E8_WEYL_ORDER != E8_EXPECTED_WEYL_ORDER:
        raise AssertionError("E8 Weyl order/exponent product mismatch")
    action = E8WeylAction.build()
    selected = action.roots[0] if seed is None else seed
    orbit = action.root_orbit(selected)
    if len(orbit) == 0 or E8_WEYL_ORDER % len(orbit):
        raise AssertionError("root orbit size does not divide Weyl group order")
    stabilizer_order = E8_WEYL_ORDER // len(orbit)
    audit = E8RootStabilizerAudit(
        seed=selected,
        orbit_size=len(orbit),
        weyl_group_order=E8_WEYL_ORDER,
        stabilizer_order=stabilizer_order,
        orthogonal_root_count=action.orthogonal_root_count(selected),
    )
    audit.validate()
    return audit
