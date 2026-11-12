"""Small research kernel for finite periodic SU(2) lattice gauge theory.

SU(2) elements are represented by unit quaternions (a, b, c, d), with
matrix trace equal to 2*a. This module is a finite-lattice computational
reference, not a continuum construction or a mass-gap argument.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, sqrt
from random import Random
from typing import Dict, Tuple

Quaternion = Tuple[float, float, float, float]
Site = Tuple[int, int]


def qmul(p: Quaternion, q: Quaternion) -> Quaternion:
    """Quaternion product; the scalar component is the SU(2) half-trace."""
    a, b, c, d = p
    e, f, g, h = q
    return (
        a * e - b * f - c * g - d * h,
        a * f + b * e + c * h - d * g,
        a * g - b * h + c * e + d * f,
        a * h + b * g - c * f + d * e,
    )


def qconj(q: Quaternion) -> Quaternion:
    a, b, c, d = q
    return (a, -b, -c, -d)


def qnorm2(q: Quaternion) -> float:
    return sum(x * x for x in q)


def qnormalize(q: Quaternion) -> Quaternion:
    n2 = qnorm2(q)
    if not isfinite(n2) or n2 <= 0.0:
        raise ValueError("SU(2) quaternion must have finite nonzero norm")
    scale = 1.0 / sqrt(n2)
    return tuple(x * scale for x in q)  # type: ignore[return-value]


def qinv_unit(q: Quaternion, tol: float = 1e-10) -> Quaternion:
    if abs(qnorm2(q) - 1.0) > tol:
        raise ValueError("inverse shortcut requires a unit quaternion")
    return qconj(q)


def random_su2(rng: Random) -> Quaternion:
    """Deterministic-seed Haar-uniform SU(2) sample via normalized Gaussians."""
    return qnormalize(tuple(rng.gauss(0.0, 1.0) for _ in range(4)))


@dataclass(frozen=True)
class SU2Lattice2D:
    """Two-dimensional periodic Lx-by-Ly lattice with one link per direction."""

    lx: int
    ly: int
    links: Dict[Tuple[int, int, int], Quaternion]

    def __post_init__(self) -> None:
        if self.lx < 2 or self.ly < 2:
            raise ValueError("periodic lattice extents must both be at least 2")
        expected = {
            (x, y, mu)
            for x in range(self.lx)
            for y in range(self.ly)
            for mu in (0, 1)
        }
        if set(self.links) != expected:
            raise ValueError("links must contain exactly two outgoing links per site")
        for link in self.links.values():
            if any(not isfinite(v) for v in link) or abs(qnorm2(link) - 1.0) > 1e-9:
                raise ValueError("every link must be a finite unit quaternion")

    def shift(self, site: Site, mu: int) -> Site:
        x, y = site
        if mu == 0:
            return ((x + 1) % self.lx, y)
        if mu == 1:
            return (x, (y + 1) % self.ly)
        raise ValueError("direction must be 0 or 1")

    def link(self, site: Site, mu: int) -> Quaternion:
        return self.links[(site[0], site[1], mu)]

    def plaquette(self, site: Site) -> Quaternion:
        """Oriented 0-1 plaquette based at site."""
        x1 = self.shift(site, 0)
        x2 = self.shift(site, 1)
        return qmul(
            qmul(
                qmul(self.link(site, 0), self.link(x1, 1)),
                qinv_unit(self.link(x2, 0)),
            ),
            qinv_unit(self.link(site, 1)),
        )

    def plaquettes(self) -> Tuple[Quaternion, ...]:
        return tuple(
            self.plaquette((x, y))
            for x in range(self.lx)
            for y in range(self.ly)
        )

    def wilson_action(self, beta: float) -> float:
        """Wilson action beta * sum_p (1 - Tr(U_p)/2)."""
        return beta * sum(1.0 - p[0] for p in self.plaquettes())

    def gauge_transform(self, gauge: Dict[Site, Quaternion]) -> "SU2Lattice2D":
        """Apply U_mu(x) -> g(x) U_mu(x) g(x+mu)^(-1)."""
        sites = {(x, y) for x in range(self.lx) for y in range(self.ly)}
        if set(gauge) != sites:
            raise ValueError("gauge transformation must assign one SU(2) element per site")
        for element in gauge.values():
            if any(not isfinite(v) for v in element) or abs(qnorm2(element) - 1.0) > 1e-9:
                raise ValueError("gauge transformations must be unit quaternions")
        transformed = {}
        for x in range(self.lx):
            for y in range(self.ly):
                site = (x, y)
                for mu in (0, 1):
                    end = self.shift(site, mu)
                    transformed[(x, y, mu)] = qmul(
                        qmul(gauge[site], self.link(site, mu)),
                        qconj(gauge[end]),
                    )
        return SU2Lattice2D(self.lx, self.ly, transformed)


def random_lattice(lx: int, ly: int, seed: int) -> SU2Lattice2D:
    rng = Random(seed)
    links = {
        (x, y, mu): random_su2(rng)
        for x in range(lx)
        for y in range(ly)
        for mu in (0, 1)
    }
    return SU2Lattice2D(lx, ly, links)


def random_gauge_transform(lx: int, ly: int, seed: int) -> Dict[Site, Quaternion]:
    rng = Random(seed)
    return {
        (x, y): random_su2(rng)
        for x in range(lx)
        for y in range(ly)
    }
