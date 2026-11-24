"""Exact class census model for PROP-VOA-001.

This is an independent specification/audit layer, not a VOA construction.
The projected census is kept separate from unprojected vacuum-sector bridge
classes required for one-grade propagation.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass
from hashlib import sha256
from fractions import Fraction
from math import comb
import json
from typing import Iterable

from core.seed_sharing.contract import SeedEnvelope
from experiments.moonshine_sierpinski.lattice_modular_audit import (
    leech_theta_reference,
)
from experiments.moonshine_sierpinski.leech_z2_orbifold_character import (
    leech_z2_orbifold_character,
)

MAX_FLOOR = 5
MAX_CLASSES = 512
MAX_JSON_BYTES = 65_536
OSCILLATOR_COLORS = 24
TWISTED_GROUND_DIMENSION = 4096

EXPECTED_SECTORS = {
    0: (1, 0),
    1: (0, 0),
    2: (98_580, 98_304),
    3: (10_745_856, 10_747_904),
    4: (432_155_586, 432_144_384),
    5: (10_122_903_552, 10_122_952_704),
}


@dataclass(frozen=True)
class StateClass:
    floor: int
    sector: str
    shell: int | None
    tau: tuple[tuple[int, int], ...]
    parity: int
    projected: bool
    multiplicity: int

    def record(self) -> dict:
        row = asdict(self)
        row["tau"] = [list(pair) for pair in self.tau]
        row["mode_unit"] = (
            "integer" if self.sector == "untwisted"
            else "twice_half_integer"
        )
        return row


def _integer_partitions(total: int, minimum: int = 1):
    """Yield nondecreasing integer partitions of total."""
    if total == 0:
        yield ()
        return
    for mode in range(minimum, total + 1):
        for tail in _integer_partitions(total - mode, mode):
            yield (mode,) + tail


def _odd_partitions(total: int, minimum: int = 1):
    """Yield nondecreasing partitions into odd positive integers."""
    if total == 0:
        yield ()
        return
    for mode in range(minimum, total + 1, 2):
        for tail in _odd_partitions(total - mode, mode):
            yield (mode,) + tail


def _partition_type(parts: Iterable[int]) -> tuple[tuple[int, int], ...]:
    counts = Counter(parts)
    return tuple(sorted(counts.items()))


def _color_multiplicity(tau: tuple[tuple[int, int], ...]) -> int:
    """24 bosonic colors: product_m binomial(23 + r_m, 23)."""
    result = 1
    for _mode, occupancy in tau:
        result *= comb(OSCILLATOR_COLORS - 1 + occupancy,
                       OSCILLATOR_COLORS - 1)
    return result


def shell_census(max_floor: int = MAX_FLOOR) -> tuple[int, ...]:
    if isinstance(max_floor, bool) or not isinstance(max_floor, int):
        raise ValueError("max_floor must be an integer")
    if not 0 <= max_floor <= MAX_FLOOR:
        raise ValueError("max_floor must be between 0 and 5")
    values = leech_theta_reference(max_floor)["coefficients_q0_to_qN"]
    return tuple(int(value) for value in values)


def build_class_table(
    shells: Iterable[int] | None = None,
    max_floor: int = MAX_FLOOR,
) -> tuple[StateClass, ...]:
    """Build projected VOA classes plus explicitly marked bridge classes.

    Untwisted nonzero shells are antipodal pairs. Their oscillator parity is
    unrestricted: the pair eigenvector sign compensates oscillator parity.
    In the zero shell, only even oscillator count is projected; odd-count
    rows are retained as unprojected transit classes for D1 closure.

    Twisted fixed classes have an odd number of half-integer oscillators.
    A half-mode is encoded by its odd doubled mode number (1, 3, 5, ...).
    """
    if isinstance(max_floor, bool) or not isinstance(max_floor, int):
        raise ValueError("max_floor must be an integer")
    if not 0 <= max_floor <= MAX_FLOOR:
        raise ValueError("max_floor must be between 0 and 5")

    shell_values = tuple(shells) if shells is not None else shell_census(max_floor)
    if len(shell_values) < max_floor + 1:
        raise ValueError("shell census does not cover requested floors")
    if shell_values[0] != 1:
        raise ValueError("zero shell must contain exactly the lattice vacuum")

    rows: list[StateClass] = []
    for floor in range(max_floor + 1):
        for shell in range(floor + 1):
            shell_count = int(shell_values[shell])
            if shell_count < 0:
                raise ValueError("shell counts must be non-negative")
            if shell > 0 and shell_count % 2:
                raise ValueError("nonzero Leech shells must split into antipodal pairs")
            if shell_count == 0:
                continue

            for parts in _integer_partitions(floor - shell):
                tau = _partition_type(parts)
                parity = len(parts) % 2
                projected = shell > 0 or parity == 0
                shell_factor = shell_count // 2 if shell > 0 else 1
                rows.append(StateClass(
                    floor=floor,
                    sector="untwisted",
                    shell=shell,
                    tau=tau,
                    parity=parity,
                    projected=projected,
                    multiplicity=shell_factor * _color_multiplicity(tau),
                ))

        # 3/2 + sum_j r_j*(odd_j/2) = floor.
        doubled_energy = 2 * floor - 3
        if doubled_energy >= 1:
            for parts in _odd_partitions(doubled_energy):
                if len(parts) % 2 != 1:
                    continue
                tau = _partition_type(parts)
                rows.append(StateClass(
                    floor=floor,
                    sector="twisted",
                    shell=None,
                    tau=tau,
                    parity=1,
                    projected=True,
                    multiplicity=(
                        TWISTED_GROUND_DIMENSION * _color_multiplicity(tau)
                    ),
                ))

    return tuple(sorted(
        rows,
        key=lambda row: (
            row.floor, row.sector,
            -1 if row.shell is None else row.shell,
            row.tau, row.parity,
        ),
    ))


def aggregate_census(
    rows: Iterable[StateClass],
    projected_only: bool = True,
) -> dict[int, tuple[int, int]]:
    result = {}
    for floor in range(MAX_FLOOR + 1):
        untwisted = 0
        twisted = 0
        for row in rows:
            if row.floor != floor or (projected_only and not row.projected):
                continue
            if row.sector == "untwisted":
                untwisted += row.multiplicity
            else:
                twisted += row.multiplicity
        result[floor] = (untwisted, twisted)
    return result


def reference_census(max_floor: int = MAX_FLOOR) -> dict[int, tuple[int, int]]:
    """Independent aggregate q-series path already audited in the repository."""
    result = leech_z2_orbifold_character(max_weight=max_floor)
    untwisted = result["untwisted_fixed_dimensions"]
    twisted = result["twisted_fixed_dimensions"]
    return {
        floor: (int(untwisted[str(floor)]), int(twisted[str(floor)]))
        for floor in range(max_floor + 1)
    }


def _key(row: StateClass):
    return (
        row.floor, row.sector, row.shell, row.tau,
        row.parity, row.projected,
    )


def _parent_untwisted(row: StateClass) -> StateClass:
    parts = []
    for mode, occupancy in row.tau:
        parts.extend([mode] * occupancy)

    if not parts:
        raise ValueError("empty untwisted class is a shell seed")
    if 1 in parts:
        parts.remove(1)  # reverse of adjoining alpha_-1
    else:
        mode = min(parts)
        parts.remove(mode)
        parts.append(mode - 1)  # reverse of m -> m+1

    parent_parts = tuple(sorted(parts))
    parent_tau = _partition_type(parent_parts)
    parent_parity = len(parent_parts) % 2
    parent_projected = row.shell > 0 or parent_parity == 0
    return StateClass(
        floor=row.floor - 1,
        sector="untwisted",
        shell=row.shell,
        tau=parent_tau,
        parity=parent_parity,
        projected=parent_projected,
        multiplicity=0,
    )


def _parent_twisted(row: StateClass) -> StateClass:
    parts = []
    for doubled_mode, occupancy in row.tau:
        parts.extend([doubled_mode] * occupancy)

    if parts.count(1) >= 2:
        parts.remove(1)
        parts.remove(1)  # two 1/2 modes add one full grade
    elif any(mode >= 3 for mode in parts):
        mode = min(mode for mode in parts if mode >= 3)
        parts.remove(mode)
        parts.append(mode - 2)  # raise a half-mode by one
    else:
        raise ValueError("twisted class is a ground-space seed")

    parent_parts = tuple(sorted(parts))
    parent_tau = _partition_type(parent_parts)
    return StateClass(
        floor=row.floor - 1,
        sector="twisted",
        shell=None,
        tau=parent_tau,
        parity=1,
        projected=True,
        multiplicity=0,
    )


def audit_closure(rows: Iterable[StateClass]) -> dict:
    table = tuple(rows)
    keys = {_key(row) for row in table}
    d1 = d2 = d3 = roots = 0
    missing = []

    for row in table:
        if row.floor == 0 and row.sector == "untwisted" and row.shell == 0:
            roots += 1
            continue
        if (
            row.sector == "untwisted"
            and row.shell == row.floor
            and not row.tau
        ):
            d2 += 1  # Leech shell seed from B1
            continue
        if (
            row.sector == "twisted"
            and row.floor == 2
            and row.tau == ((1, 1),)
        ):
            d3 += 1  # one 1/2 oscillator over the 3/2 twisted ground
            continue

        try:
            parent = (
                _parent_untwisted(row)
                if row.sector == "untwisted"
                else _parent_twisted(row)
            )
        except ValueError:
            missing.append(_key(row))
            continue
        if _key(parent) not in keys:
            missing.append(_key(row))
        else:
            d1 += 1

    return {
        "passed": not missing,
        "root_seeds": roots,
        "shell_seeds": d2,
        "twisted_ground_seeds": d3,
        "d1_edges": d1,
        "missing_classes": missing,
    }



def _flat_parts(row: StateClass) -> tuple[int, ...]:
    return tuple(
        mode
        for mode, occupancy in row.tau
        for _ in range(occupancy)
    )


def conformal_grade(row: StateClass) -> Fraction:
    """Return the exact VOA conformal grade represented by a class.

    Untwisted: lattice shell grade plus integer oscillator modes.
    Twisted: 3/2 ground grade plus doubled half-integer oscillator modes.
    """
    if row.sector == "untwisted":
        shell_grade = row.shell if row.shell is not None else 0
        return Fraction(shell_grade + sum(
            mode * occupancy for mode, occupancy in row.tau
        ))
    if row.sector == "twisted":
        return Fraction(3, 2) + sum(
            Fraction(mode * occupancy, 2)
            for mode, occupancy in row.tau
        )
    raise ValueError(f"unknown VOA sector: {row.sector!r}")


def _d1_operation(parent: StateClass, child: StateClass) -> str:
    parent_parts = _flat_parts(parent)
    child_parts = _flat_parts(child)
    if parent.sector == "untwisted":
        if child_parts.count(1) == parent_parts.count(1) + 1:
            return "D1_ADD_INTEGER_MODE_1"
        return "D1_RAISE_INTEGER_MODE"
    if child_parts.count(1) == parent_parts.count(1) + 2:
        return "D1_ADD_HALF_MODE_PAIR"
    return "D1_RAISE_HALF_MODE"


def audit_transition_edges(rows: Iterable[StateClass]) -> dict:
    """Audit every class as a seed or an explicit one-grade D1 edge.

    D2 Leech shell seeds and the D3 twisted-ground seed remain separately
    classified seed operations; neither is counted as propagation.
    """
    table = tuple(rows)
    keys = {_key(row) for row in table}
    duplicate_keys = len(keys) != len(table)
    edges = []
    seeds = []
    violations = []

    for child in table:
        child_grade = conformal_grade(child)
        if child_grade != child.floor:
            violations.append({
                "kind": "child_grade_floor_mismatch",
                "child": _key(child),
                "conformal_grade": str(child_grade),
                "declared_floor": child.floor,
            })

        if (
            child.sector == "untwisted"
            and child.floor == 0
            and child.shell == 0
            and not child.tau
        ):
            seeds.append({
                "operation": "ROOT_BASE_SEED",
                "child": _key(child),
                "grade": str(child_grade),
            })
            continue

        if (
            child.sector == "untwisted"
            and child.floor > 0
            and child.shell == child.floor
            and not child.tau
        ):
            seeds.append({
                "operation": "D2_LEECH_SHELL_SEED",
                "child": _key(child),
                "grade": str(child_grade),
            })
            continue

        if (
            child.sector == "twisted"
            and child.floor == 2
            and child.tau == ((1, 1),)
        ):
            seeds.append({
                "operation": "D3_TWISTED_GROUND_SEED",
                "child": _key(child),
                "grade": str(child_grade),
            })
            continue

        try:
            parent = (
                _parent_untwisted(child)
                if child.sector == "untwisted"
                else _parent_twisted(child)
            )
        except ValueError as exc:
            violations.append({
                "kind": "orphan_child_without_candidate_parent",
                "child": _key(child),
                "detail": str(exc),
            })
            continue

        parent_key = _key(parent)
        if parent_key not in keys:
            violations.append({
                "kind": "orphan_edge_parent_not_enumerated",
                "parent": parent_key,
                "child": _key(child),
            })
            continue

        parent_grade = conformal_grade(parent)
        increment = child_grade - parent_grade
        operation = _d1_operation(parent, child)
        parent_parts = _flat_parts(parent)
        child_parts = _flat_parts(child)

        sector_ok = parent.sector == child.sector
        if child.sector == "untwisted":
            parity_ok = (
                parent.parity == len(parent_parts) % 2
                and child.parity == len(child_parts) % 2
                and (child.parity - parent.parity) % 2
                    == (len(child_parts) - len(parent_parts)) % 2
            )
            projection_ok = (
                parent.projected == (parent.shell > 0 or parent.parity == 0)
                and child.projected == (child.shell > 0 or child.parity == 0)
            )
        else:
            parity_ok = (
                parent.parity == child.parity == 1
                and len(parent_parts) % 2 == len(child_parts) % 2 == 1
            )
            projection_ok = parent.projected and child.projected

        allowed_operation = operation in {
            "D1_ADD_INTEGER_MODE_1",
            "D1_RAISE_INTEGER_MODE",
            "D1_ADD_HALF_MODE_PAIR",
            "D1_RAISE_HALF_MODE",
        }
        edge_ok = (
            allowed_operation
            and increment == 1
            and sector_ok
            and parity_ok
            and projection_ok
        )
        edge = {
            "operation": operation,
            "parent": parent_key,
            "child": _key(child),
            "parent_grade": str(parent_grade),
            "child_grade": str(child_grade),
            "grade_increment": str(increment),
            "allowed_operation": allowed_operation,
            "sector_transition_valid": sector_ok,
            "parity_valid": parity_ok,
            "projection_valid": projection_ok,
            "passed": edge_ok,
        }
        edges.append(edge)
        if not edge_ok:
            violations.append({
                "kind": "invalid_transition_edge",
                "edge": edge,
            })

    return {
        "passed": not violations and not duplicate_keys,
        "enumerated_children": len(table),
        "candidate_d1_edges": len(edges),
        "d1_edges": sum(edge["passed"] for edge in edges),
        "seed_counts": {
            "root": sum(seed["operation"] == "ROOT_BASE_SEED" for seed in seeds),
            "d2_leech_shell": sum(
                seed["operation"] == "D2_LEECH_SHELL_SEED" for seed in seeds
            ),
            "d3_twisted_ground": sum(
                seed["operation"] == "D3_TWISTED_GROUND_SEED" for seed in seeds
            ),
        },
        "edges": edges,
        "seeds": seeds,
        "duplicate_class_keys": duplicate_keys,
        "violations": violations,
    }


def canonical_table_bytes(rows: Iterable[StateClass]) -> bytes:
    payload = {
        "schema": "PROP-VOA-001-class-table-v0.1",
        "classes": [row.record() for row in rows],
    }
    return json.dumps(
        payload, sort_keys=True, separators=(",", ":"),
        ensure_ascii=False, allow_nan=False,
    ).encode("utf-8")


def base_seed_record(shells: Iterable[int]) -> dict:
    envelope = SeedEnvelope(
        seed_id="PROP-VOA-001/base",
        source_id="PANoRAMic.os:leech_theta_reference",
        version="1",
        payload={
            "leech_shell_counts_q0_to_q5": list(shells),
            "oscillator_colors": OSCILLATOR_COLORS,
            "twisted_ground_dimension": TWISTED_GROUND_DIMENSION,
        },
    )
    return envelope.to_record()


def audit_exactness(rows: Iterable[StateClass]) -> dict:
    actual = aggregate_census(rows, projected_only=True)
    aggregate_reference = reference_census(MAX_FLOOR)
    fixtures = {
        floor: EXPECTED_SECTORS[floor]
        for floor in range(MAX_FLOOR + 1)
    }
    return {
        "passed": actual == aggregate_reference == fixtures,
        "actual": actual,
        "aggregate_q_series_reference": aggregate_reference,
        "preregistered_reference": fixtures,
    }


def audit_permutation_control(rows: Iterable[StateClass], seed: int = 17) -> dict:
    """A permutation preserves aggregate sums; classwise checking must catch it."""
    import random
    from dataclasses import replace

    original = tuple(rows)
    # Keep the permutation inside the projected census. Mixing projected
    # classes with bridge-only rows changes the projected aggregate by design.
    candidates = [
        index for index, row in enumerate(original)
        if row.floor == 5 and row.sector == "untwisted" and row.projected
    ]
    original_values = [original[index].multiplicity for index in candidates]
    if len(candidates) < 2 or len(set(original_values)) < 2:
        raise AssertionError(
            "permutation control needs two projected classes with distinct multiplicities"
        )

    shuffled_values = list(original_values)
    random.Random(seed).shuffle(shuffled_values)
    if shuffled_values == original_values:
        # Guarantee a nontrivial permutation even for an unlucky seed/order.
        left = next(i for i, value in enumerate(original_values)
                    if value != original_values[0])
        shuffled_values[0], shuffled_values[left] = (
            shuffled_values[left], shuffled_values[0]
        )

    mutated = list(original)
    for index, value in zip(candidates, shuffled_values):
        mutated[index] = replace(mutated[index], multiplicity=value)

    aggregate_preserved = (
        aggregate_census(original) == aggregate_census(mutated)
    )
    classwise_rejected = any(
        _key(left) == _key(right) and left.multiplicity != right.multiplicity
        for left, right in zip(original, mutated)
    )
    return {
        "aggregate_census_preserved": aggregate_preserved,
        "classwise_check_rejected": classwise_rejected,
        "passed": aggregate_preserved and classwise_rejected,
    }


def audit_corrupted_shell_control(shells: Iterable[int]) -> dict:
    corrupted = list(shells)
    corrupted[2] += 2
    rows = build_class_table(corrupted, MAX_FLOOR)
    actual = aggregate_census(rows)
    return {
        "passed": actual != EXPECTED_SECTORS,
        "actual": actual,
        "expected": EXPECTED_SECTORS,
    }


def build_audit_summary() -> dict:
    shells = shell_census(MAX_FLOOR)
    rows = build_class_table(shells, MAX_FLOOR)
    encoded = canonical_table_bytes(rows)
    exactness = audit_exactness(rows)
    closure = audit_closure(rows)
    transition_edges = audit_transition_edges(rows)
    transition_edges["matches_c2_d1_edge_count"] = (
        transition_edges["d1_edges"] == closure["d1_edges"]
    )
    transition_edges["passed"] = (
        transition_edges["passed"]
        and transition_edges["matches_c2_d1_edge_count"]
    )
    permutation = audit_permutation_control(rows)
    corrupted = audit_corrupted_shell_control(shells)
    return {
        "schema": "PROP-VOA-001-independent-audit-v0.1",
        "status": "SPEC_DIAGNOSTIC_ONLY_NOT_PREREGISTERED_RUN",
        "base_seed": base_seed_record(shells),
        "class_count_including_bridge_nodes": len(rows),
        "projected_class_count": sum(row.projected for row in rows),
        "class_count_by_floor": {
            floor: sum(row.floor == floor for row in rows)
            for floor in range(MAX_FLOOR + 1)
        },
        "census": exactness,
        "closure": closure,
        "transition_edge_audit": transition_edges,
        "compression": {
            "canonical_json_bytes": len(encoded),
            "limit_bytes": MAX_JSON_BYTES,
            "passes_size_limit": len(encoded) <= MAX_JSON_BYTES,
            "floor_5_states_per_byte": (
                EXPECTED_SECTORS[5][0] + EXPECTED_SECTORS[5][1]
            ) / len(encoded),
        },
        "controls": {
            "corrupted_shell_S2_plus_2": corrupted,
            "partition_multiplicity_permutation": permutation,
        },
        "budget": {
            "max_classes": MAX_CLASSES,
            "used_classes": len(rows),
            "passes": len(rows) <= MAX_CLASSES,
            "max_floor": MAX_FLOOR,
            "max_transition_increment_conformal_grade": 1,
        },
        "evidence_boundary": (
            "Exact class-count representation diagnostic only; constructs no "
            "VOA states, vertex operators, Griess product, or Monster action."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(build_audit_summary(), indent=2, sort_keys=True))
