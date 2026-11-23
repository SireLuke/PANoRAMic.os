"""Deterministic basis certificate for the weight-two Moonshine-module space.

This is G0 of the constructive Griess-algebra programme. It enumerates the
three basis families and freezes canonical IDs/digests. It does NOT implement
any VOA vertex operator, twisted intertwiner, Griess product, or Monster action.

The Leech momentum basis uses one representative from each {alpha,-alpha}
pair of norm-four vectors. The twisted basis labels are formal tensor-product
indices only; they do not assert a constructed Clifford/ground-space action.
"""
from __future__ import annotations

from hashlib import sha256
import json

from experiments.moonshine_sierpinski.leech_golay_construction import (
    leech_minimal_vectors,
)


def _canonical_momentum_representatives() -> tuple[tuple[int, ...], ...]:
    """Choose lexicographically smaller representative in each +/- pair."""
    representatives = set()
    for vector in leech_minimal_vectors():
        opposite = tuple(-coordinate for coordinate in vector)
        if vector == opposite:
            raise AssertionError("nonzero Leech minimal vector cannot be antipodal-fixed")
        representatives.add(min(vector, opposite))
    ordered = tuple(sorted(representatives))
    if len(ordered) != 98_280:
        raise AssertionError(
            f"expected 98,280 antipodal momentum pairs, got {len(ordered)}"
        )
    return ordered


def _digest_json(value: object) -> str:
    payload = json.dumps(value, separators=(",", ":"), ensure_ascii=True)
    return sha256(payload.encode("ascii")).hexdigest()


def griess_weight_two_basis_certificate() -> dict:
    """Return deterministic IDs, counts, and digests for the three basis blocks.

    Basis blocks:
      U_mom: even momentum combinations indexed by {alpha,-alpha};
      U_osc: Sym^2 of the 24-dimensional Heisenberg space;
      T_osc: 24 formal oscillator labels over 4096 twisted ground labels.

    No multiplication data is included in this certificate.
    """
    momentum = _canonical_momentum_representatives()
    oscillator = tuple(
        (left, right)
        for left in range(24)
        for right in range(left, 24)
    )
    twisted = tuple(
        (ground, direction)
        for ground in range(4096)
        for direction in range(24)
    )

    if len(oscillator) != 300:
        raise AssertionError("Sym^2 of a 24-dimensional space must have dimension 300")
    if len(twisted) != 98_304:
        raise AssertionError("twisted basis index set must have 4096*24 elements")

    momentum_digest = _digest_json(momentum)
    oscillator_digest = _digest_json(oscillator)
    twisted_digest = _digest_json(twisted)

    return {
        "object": "V^natural weight-two basis index certificate",
        "conformal_weight": 2,
        "basis_blocks": {
            "untwisted_momentum_even": {
                "dimension": len(momentum),
                "basis_id_rule": "U.MOM.{index:05d}",
                "representative_rule": "lexicographic_minimum(alpha,-alpha)",
                "coordinate_scale": "integral Leech coordinates divided by sqrt(8)",
                "sha256": momentum_digest,
            },
            "untwisted_oscillator_symmetric": {
                "dimension": len(oscillator),
                "basis_id_rule": "U.OSC.{left:02d}.{right:02d}",
                "index_rule": "0 <= left <= right < 24",
                "sha256": oscillator_digest,
            },
            "twisted_oscillator_ground_tensor": {
                "dimension": len(twisted),
                "basis_id_rule": "T.GROUND.{ground:04d}.OSC.{direction:02d}",
                "index_rule": "0 <= ground < 4096; 0 <= direction < 24",
                "ground_space_status": "formal labels; representation not constructed",
                "sha256": twisted_digest,
            },
        },
        "untwisted_fixed_dimension": len(momentum) + len(oscillator),
        "twisted_fixed_dimension": len(twisted),
        "total_dimension": len(momentum) + len(oscillator) + len(twisted),
        "expected_dimensions": {
            "untwisted_fixed": 98_580,
            "twisted_fixed": 98_304,
            "total": 196_884,
        },
        "dimension_checks_passed": (
            len(momentum) == 98_280
            and len(oscillator) == 300
            and len(twisted) == 98_304
            and len(momentum) + len(oscillator) == 98_580
            and len(momentum) + len(oscillator) + len(twisted) == 196_884
        ),
        "basis_ordering": (
            "momentum representatives lexicographically sorted; oscillator "
            "pairs lexicographic; twisted labels ground-major then direction"
        ),
        "griess_product_constructed": False,
        "twisted_ground_representation_constructed": False,
        "monster_action_constructed": False,
        "scope": (
            "deterministic basis indexing and dimension certificate only; "
            "not a VOA extension, intertwining-operator, product, or group-action construction"
        ),
    }


if __name__ == "__main__":
    print(json.dumps(griess_weight_two_basis_certificate(), indent=2, sort_keys=True))
