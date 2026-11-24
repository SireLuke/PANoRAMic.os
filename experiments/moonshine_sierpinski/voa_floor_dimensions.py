#!/usr/bin/env python3
"""Exact per-sector dimensions of the Monster VOA floors V^natural_n.

For each weight floor n, computes the dimension split

    dim V^natural_n = dim V_Lambda,n^+  +  dim V_Lambda,n^{T,+}

(untwisted / twisted +1 eigenspaces of the FLM Z2 orbifold) in exact
integer arithmetic:

- Leech shell census from the theta series Theta_Lambda = E_4^3 - 720*Delta.
- Integer-mode oscillators in 24 colors, split by oscillator-count parity
  (the theta: alpha -> -alpha eigenspaces). For a lattice pair
  {lambda, -lambda} both parities occur (paired with the symmetric /
  antisymmetric lattice combinations); for lambda = 0 only the even
  (+1) oscillator sector survives.
- Twisted sector: the 4096-dimensional spinor ground space at weight 3/2,
  dressed with an odd number of half-integer modes.

Provenance: algorithm from a bench draft relayed by Lucas on 2026-11-23.
Running the draft as received printed every untwisted count one floor
too low (it read the state count at index n-1); the correction is the
single index change marked INDEX FIX below. With the fix, the totals
reproduce the coefficients of J(tau) = j(tau) - 744 exactly through
weight 5, and the script asserts them.

Scope: dimension counting only. This constructs no states, no Griess
product, and no group action; it is the census the tower stands on.
Complements leech_voa_character.py (the un-orbifolded lattice VOA).
"""
from __future__ import annotations

import numpy as np

# Coefficients of J(tau) = q^-1 + sum_n dim(V^natural_n) q^(n-1)... i.e.
# dim V^natural_n for n = 0..5, the standard j-invariant values.
KNOWN_TOTALS = {0: 1, 1: 0, 2: 196884, 3: 21493760, 4: 864299970,
                5: 20245856256}


def generate_voa_floors(max_weight: int = 5):
    """Return (untwisted_plus, twisted_plus) dimension arrays by weight."""
    size = max_weight + 3
    q_max = size

    # Delta(q) = q * prod (1 - q^m)^24, via repeated polynomial multiply.
    poly = np.zeros(q_max, dtype=object)
    poly[0] = 1
    for m in range(1, q_max):
        for _ in range(24):
            new_poly = poly.copy()
            new_poly[m:] -= poly[:-m]
            poly = new_poly
    tau = np.zeros(q_max, dtype=object)
    tau[1:] = poly[:-1]

    # E_4(q) = 1 + 240 * sum sigma_3(n) q^n.
    e4 = np.zeros(q_max, dtype=object)
    e4[0] = 1
    for n in range(1, q_max):
        e4[n] = 240 * sum(d ** 3 for d in range(1, n + 1) if n % d == 0)

    e4_3 = np.convolve(np.convolve(e4, e4)[:q_max], e4)[:q_max]
    theta_leech = e4_3 - 720 * tau  # theta_leech[k] = # vectors of norm^2 2k

    # Integer-mode oscillators, split by parity of the oscillator count.
    osc_plus = np.zeros(q_max, dtype=object)
    osc_minus = np.zeros(q_max, dtype=object)
    osc_plus[0] = 1
    for m in range(1, q_max):
        for _ in range(24):
            new_p = osc_plus.copy()
            new_m = osc_minus.copy()
            for k in range(m, q_max):
                new_p[k] += new_m[k - m]
                new_m[k] += new_p[k - m]
            osc_plus, osc_minus = new_p, new_m

    untwisted_plus = np.zeros(max_weight + 1, dtype=object)
    for n in range(max_weight + 1):
        idx = n  # INDEX FIX: the draft read idx = n - 1 (one floor too low)
        total = osc_plus[idx]  # lambda = 0: even oscillators only
        for k in range(1, idx + 1):
            half_lattice = theta_leech[k] // 2  # {lambda, -lambda} pairs
            total += half_lattice * (osc_plus[idx - k] + osc_minus[idx - k])
        untwisted_plus[n] = total

    # Twisted sector: odd number of half-integer modes on the 4096-dim
    # ground space at weight 3/2; mode sum for floor n is (2n - 3) half-units.
    half_max = 2 * max_weight + 1
    tw_even = np.zeros(half_max, dtype=object)
    tw_odd = np.zeros(half_max, dtype=object)
    tw_even[0] = 1
    for r_half in range(1, half_max, 2):
        for _ in range(24):
            new_e = tw_even.copy()
            new_o = tw_odd.copy()
            for k in range(r_half, half_max):
                new_e[k] += new_o[k - r_half]
                new_o[k] += new_e[k - r_half]
            tw_even, tw_odd = new_e, new_o

    twisted_plus = np.zeros(max_weight + 1, dtype=object)
    for n in range(2, max_weight + 1):
        twisted_plus[n] = 4096 * tw_odd[2 * n - 3]

    return untwisted_plus, twisted_plus


def main() -> None:
    untw, tw = generate_voa_floors(5)
    for n in range(6):
        total = untw[n] + tw[n]
        print(f"Floor V_{n}: Untwisted = {untw[n]:,} | "
              f"Twisted = {tw[n]:,} | Total = {total:,}")
        assert total == KNOWN_TOTALS[n], (n, total, KNOWN_TOTALS[n])
    print("All totals match the J(tau) coefficients for weights 0..5.")


if __name__ == "__main__":
    main()
