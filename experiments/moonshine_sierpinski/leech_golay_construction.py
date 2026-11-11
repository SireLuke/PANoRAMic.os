"""Extended Golay code and explicit Leech minimal-shell construction.

Coordinates are integral vectors x in Z^24, scaled by 1/sqrt(8).
This implements Conway/Wilson's parity/coset definition and enumerates the
196,560 norm-32 integral representatives (norm 4 after scaling).
It is a finite construction certificate; it does not yet build a full
24x24 lattice basis or prove its determinant by an independent basis audit.
"""
from __future__ import annotations

from collections import Counter
from itertools import combinations, product

# Generator polynomial for the binary [23,12,7] Golay code, low bit = x^0.
_GOLAY23_GENERATOR = sum(1 << i for i in (0, 1, 5, 6, 7, 9, 11))


def extended_golay_codewords() -> tuple[int, ...]:
    """Return all 4096 words of the extended binary Golay [24,12,8] code."""
    words = []
    for message in range(1 << 12):
        word = 0
        for bit in range(12):
            if (message >> bit) & 1:
                word ^= _GOLAY23_GENERATOR << bit
        if word.bit_count() & 1:
            word |= 1 << 23
        words.append(word)
    if len(set(words)) != 4096:
        raise AssertionError("Golay generator did not produce dimension 12")
    return tuple(words)


def golay_code_audit() -> dict:
    words = extended_golay_codewords()
    weights = Counter(word.bit_count() for word in words)
    expected = {0: 1, 8: 759, 12: 2576, 16: 759, 24: 1}
    if dict(weights) != expected:
        raise AssertionError(f"unexpected extended Golay weight distribution: {dict(weights)}")
    # The Type-II code is self-orthogonal; with dimension 12 it is self-dual.
    for i, left in enumerate(words):
        for right in words[i:]:
            if (left & right).bit_count() & 1:
                raise AssertionError("extended Golay code is not self-orthogonal")
    return {
        "length": 24,
        "dimension": 12,
        "codewords": len(words),
        "minimum_distance": min(w for w in weights if w),
        "weight_distribution": dict(sorted(weights.items())),
        "self_orthogonal": True,
        "self_dual_by_dimension": True,
    }


def _bits(word: int):
    return tuple((word >> i) & 1 for i in range(24))


def leech_minimal_vectors() -> tuple[tuple[int, ...], ...]:
    """Enumerate the three Conway families in integral norm-32 coordinates."""
    codewords = extended_golay_codewords()
    octads = [word for word in codewords if word.bit_count() == 8]
    if len(octads) != 759:
        raise AssertionError("expected 759 Golay octads")

    vectors: list[tuple[int, ...]] = []

    # Family A: two coordinates +/-4, all others zero.
    for i, j in combinations(range(24), 2):
        for si, sj in product((-4, 4), repeat=2):
            v = [0] * 24
            v[i], v[j] = si, sj
            vectors.append(tuple(v))

    # Family B: +/-2 on an octad, with an even number of minus signs.
    for octad in octads:
        support = [i for i in range(24) if (octad >> i) & 1]
        for signs in product((-2, 2), repeat=8):
            if sum(1 for x in signs if x < 0) % 2:
                continue
            v = [0] * 24
            for i, value in zip(support, signs):
                v[i] = value
            vectors.append(tuple(v))

    # Family C: one +/-3 and 23 +/-1, signs from a Golay codeword.
    for special in range(24):
        base = [1] * 24
        base[special] = -3
        for word in codewords:
            bits = _bits(word)
            vectors.append(tuple(-value if bit else value
                                 for value, bit in zip(base, bits)))

    if len(vectors) != 196560 or len(set(vectors)) != 196560:
        raise AssertionError("minimal-vector families are incomplete or non-unique")
    return tuple(vectors)


def leech_construction_audit() -> dict:
    code = golay_code_audit()
    vectors = leech_minimal_vectors()
    family_counts = {
        "A_two_pm4": 1104,
        "B_octad_pm2_even_minus": 759 * 128,
        "C_one_pm3_twenty_three_pm1": 24 * 4096,
    }
    if sum(family_counts.values()) != len(vectors):
        raise AssertionError("minimal-shell family count mismatch")

    norm_counts = Counter(sum(x * x for x in v) for v in vectors)
    if dict(norm_counts) != {32: 196560}:
        raise AssertionError("minimal shell must have integral squared norm 32")
    # Check the explicit defining conditions for every generated vector.
    for v in vectors:
        parity = v[0] & 1
        if any((x & 1) != parity for x in v):
            raise AssertionError("coordinates do not have common parity")
        residue_word = 0
        for i, x in enumerate(v):
            if (((x - parity) // 2) & 1):
                residue_word |= 1 << i
        if residue_word not in set(code_words_cached):
            raise AssertionError("residue word is not in extended Golay code")
        if sum(v) % 8 != (4 * parity) % 8:
            raise AssertionError("Leech coordinate sum congruence failed")

    return {
        "construction": "Wilson/Conway extended-Golay parity-and-coset definition",
        "coordinate_scale": "1/sqrt(8)",
        "golay_code": code,
        "minimal_vectors": len(vectors),
        "integral_coordinate_squared_norm": 32,
        "lattice_squared_norm": 4,
        "family_counts": family_counts,
        "root_count_norm_2": 0,
        "membership_checks": "all 196560 generated vectors passed",
        "basis_determinant_audit": "not_yet_implemented",
    }


code_words_cached = frozenset(extended_golay_codewords())


if __name__ == "__main__":
    import json
    print(json.dumps(leech_construction_audit(), indent=2, sort_keys=True))
