"""Independent implementation of the preregistered -002 ablation protocol.

This runner composes existing PAN modules without modifying their source
artifacts. It treats Navier–Stokes snapshots, ABOM samples, E8 roots, the
Leech lattice certificate, and the Gosset graph-state audit as separate
typed outputs. No physical coupling is inferred from co-presence.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
import math
import platform
import random
import statistics
import subprocess
import sys
import time
import tracemalloc
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable

_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from core.abom_v8.abom_v8_model import abom_v8_sample, e8_roots as abom_e8_roots
from core.geometry.e8_root_system import e8_roots_exact
from experiments.flip_qubit import cut_rank_audit as eqbit
from experiments.moonshine_sierpinski.leech_unimodular_basis import (
    leech_unimodular_basis_audit,
)

DEFAULT_NS_RESULTS = _REPO_ROOT / "experiments/ns_evidence_001_cosmo/cosmo_results.json"
DEFAULT_SEED = 20261121
SOURCE_PATHS = (
    "experiments/ns_evidence_001_cosmo/cosmo_results.json",
    "core/abom_v8/abom_v8_model.py",
    "core/geometry/e8_root_system.py",
    "experiments/moonshine_sierpinski/leech_unimodular_basis.py",
    "experiments/moonshine_sierpinski/leech_golay_construction.py",
    "experiments/flip_qubit/cut_rank_audit.py",
    "research/NS_ABOM_E8_LEECH_EQBIT_002_ABLATION.md",
    "experiments/ns_abom_e8_leech_eqbit_002_valdora/runner.py",
)


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"),
                       ensure_ascii=True, allow_nan=False) + "\n").encode("utf-8")


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _object_hash(value: Any) -> str:
    return _sha256_bytes(_json_bytes(value))


def _file_hash(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


def _git_commit() -> str | None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=_REPO_ROOT, check=True,
            capture_output=True, text=True, timeout=3,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return result.stdout.strip() or None


def load_ns_snapshot(path: str | Path = DEFAULT_NS_RESULTS) -> dict[str, Any]:
    """Load the frozen nine-case Cosmo snapshot and validate its declared grid."""
    source = Path(path)
    payload = json.loads(source.read_text(encoding="utf-8"))
    cases = payload.get("cases")
    if not isinstance(cases, list) or len(cases) != 9:
        raise ValueError("expected exactly nine frozen NS-EVIDENCE-001 cases")

    required = ("n", "d", "nu", "T", "dt", "steps", "ET", "OmT", "max_div_T")
    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            raise ValueError(f"NS case {index} must be an object")
        missing = [key for key in required if key not in case]
        if missing:
            raise ValueError(f"NS case {index} missing fields: {missing}")
        if case["d"] not in (2, 3):
            raise ValueError(f"NS case {index} has unsupported spatial dimension")
        for field in ("n", "nu", "T", "dt", "steps", "ET", "OmT", "max_div_T"):
            value = case[field]
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ValueError(f"NS case {index} field {field} must be numeric")
            if not math.isfinite(float(value)):
                raise ValueError(f"NS case {index} field {field} must be finite")
        if case["n"] < 1 or case["steps"] < 1 or case["nu"] <= 0:
            raise ValueError(f"NS case {index} has invalid grid or viscosity metadata")
        if case["T"] <= 0 or case["dt"] <= 0:
            raise ValueError(f"NS case {index} has invalid time metadata")
        tolerance = max(1e-14, abs(float(case["T"])) * 1e-12)
        if abs(float(case["steps"]) * float(case["dt"]) - float(case["T"])) > tolerance:
            raise ValueError(f"NS case {index} does not land on its declared final time")
    return payload


def _fraction_root(root: Iterable[Any]) -> tuple[Fraction, ...]:
    return tuple(value if isinstance(value, Fraction) else Fraction(value) for value in root)


def _root_payload(roots: Iterable[Iterable[Any]]) -> list[list[str]]:
    return [list(map(str, root)) for root in sorted(_fraction_root(r) for r in roots)]


def _exactify_adapter_roots(raw_roots: Iterable[Iterable[Any]]) -> tuple[tuple[Fraction, ...], ...]:
    """Convert the float compatibility view without rounding away discrepancies."""
    converted = []
    for index, root in enumerate(raw_roots):
        coordinates = tuple(root)
        if len(coordinates) != 8:
            raise ValueError(f"ABOM E8 root {index} must have exactly eight coordinates")
        exact = []
        for coordinate in coordinates:
            value = float(coordinate)
            if not math.isfinite(value):
                raise ValueError(f"ABOM E8 root {index} contains a non-finite coordinate")
            # Decimal round-trip preserves the adapter's represented value. It does
            # not snap near-roots onto the nearest integer/half-integer.
            exact.append(Fraction(str(value)))
        converted.append(tuple(exact))
    return tuple(converted)


def _e8_abom_comparison() -> dict[str, Any]:
    exact_roots = tuple(_fraction_root(root) for root in e8_roots_exact())
    raw_adapter_roots = tuple(abom_e8_roots())
    adapter_roots = _exactify_adapter_roots(raw_adapter_roots)
    exact_set, adapter_set = set(exact_roots), set(adapter_roots)
    exact_hash = _object_hash(_root_payload(exact_set))
    adapter_hash = _object_hash(_root_payload(adapter_set))
    exact_norms = all(sum(x * x for x in r) == 2 for r in exact_set)
    adapter_norms = all(sum(x * x for x in r) == 2 for r in adapter_set)
    return {
        "rank": 8,
        "expected_roots": 240,
        "exact_root_count": len(exact_roots),
        "exact_unique_root_count": len(exact_set),
        "abom_adapter_root_count": len(adapter_set),
        "abom_adapter_raw_root_count": len(raw_adapter_roots),
        "abom_adapter_unique_root_count": len(adapter_set),
        "all_exact_norm_squared_two": exact_norms,
        "all_adapter_norm_squared_two": adapter_norms,
        "root_sets_equal": exact_set == adapter_set,
        "exact_root_set_sha256": exact_hash,
        "abom_root_set_sha256": adapter_hash,
        "symmetric_difference_count": len(exact_set ^ adapter_set),
        "adapter_coordinate_policy": "exact decimal round-trip; no denominator limiting or nearest-root snapping",
        "comparison": "canonical exact root set versus ABOM floating compatibility view",
    }


def _build_gosset_graph() -> tuple[list[tuple[int, ...]], list[set[int]]]:
    """Reconstruct the graph from the existing scaled-root implementation."""
    roots = [tuple(root) for root in eqbit.e8_roots_scaled()]
    adjacency = eqbit.gosset_adjacency(roots)
    return roots, adjacency


def _graph_contract() -> tuple[dict[str, Any], list[tuple[int, ...]], list[set[int]],
                               list[tuple[int, int]], list[int], list[int], list[int]]:
    roots, adjacency = _build_gosset_graph()
    root_index = {root: i for i, root in enumerate(roots)}
    exact_scaled = {
        tuple(2 * coordinate for coordinate in root)
        for root in e8_roots_exact()
    }
    graph_root_set = set(roots)
    mapped = exact_scaled == graph_root_set and len(root_index) == 240
    if not mapped:
        raise AssertionError("scaled Gosset vertices are not bijective with the exact E8 roots")

    degrees = [len(row) for row in adjacency]
    edge_count = sum(degrees) // 2
    anti = []
    for i, root in enumerate(roots):
        negative = tuple(-x for x in root)
        if negative not in root_index:
            raise AssertionError("an E8 vertex has no antipode")
        anti.append(root_index[negative])

    if any(anti[anti[i]] != i or anti[i] == i for i in range(240)):
        raise AssertionError("antipodal map is not a fixed-point-free involution")
    if any({anti[j] for j in adjacency[i]} != adjacency[anti[i]] for i in range(240)):
        raise AssertionError("antipodal involution is not a graph automorphism")

    left, right, pairs = eqbit.canonical_antipodal_partition(roots)
    if len(pairs) != 120 or len(left) != 120 or len(right) != 120:
        raise AssertionError("canonical antipodal split is not 120|120")
    if sorted(degrees) != [56] * 240 or edge_count != 6720:
        raise AssertionError("Gosset graph degree/edge contract failed")

    root_to_vertex = {
        tuple(2 * coordinate for coordinate in root): root_index[tuple(2 * coordinate for coordinate in root)]
        for root in e8_roots_exact()
    }
    incidence_ok = len(root_to_vertex) == 240 and set(root_to_vertex) == exact_scaled
    summary = {
        "vertices": len(roots),
        "edges": edge_count,
        "degree_min": min(degrees),
        "degree_max": max(degrees),
        "antipodal_pairs": len(pairs),
        "e8_root_to_gosset_vertex_bijection": incidence_ok,
        "antipodal_map_fixed_point_free_involution": True,
        "antipodal_map_graph_automorphism": True,
        "adjacency_rule": "scaled E8 root inner product equals 4 (standard E8 inner product equals 1)",
        "root_vertex_map_sha256": _object_hash([
            [list(map(str, root)), root_to_vertex[root]] for root in sorted(root_to_vertex)
        ]),
    }
    return summary, roots, adjacency, pairs, left, right, anti


def _wilson_interval(successes: int, trials: int, z: float = 1.959963984540054) -> list[float]:
    if trials <= 0:
        raise ValueError("trials must be positive")
    p = successes / trials
    z2 = z * z
    denominator = 1.0 + z2 / trials
    centre = (p + z2 / (2.0 * trials)) / denominator
    half = z * math.sqrt((p * (1.0 - p) / trials) + z2 / (4.0 * trials * trials)) / denominator
    return [max(0.0, centre - half), min(1.0, centre + half)]


def _rank_summary(values: list[int], reference_rank: int) -> dict[str, Any]:
    if not values:
        raise ValueError("rank sample is empty")
    ordered = sorted(values)

    def nearest_rank(probability: float) -> int:
        return ordered[max(0, min(len(ordered) - 1, math.ceil(probability * len(ordered)) - 1))]

    tail_count = sum(value <= reference_rank for value in values)
    trials = len(values)
    return {
        "n": trials,
        "min": ordered[0],
        "p05": nearest_rank(0.05),
        "median": float(statistics.median(ordered)),
        "mean": statistics.fmean(ordered),
        "stdev": statistics.stdev(ordered) if trials > 1 else 0.0,
        "p95": nearest_rank(0.95),
        "max": ordered[-1],
        "tail_count_rank_le_antipodal": tail_count,
        "tail_probability_plus_one": (tail_count + 1) / (trials + 1),
        "tail_probability_wilson_95_raw_frequency": _wilson_interval(tail_count, trials),
        "tail_interval_method": "Wilson score interval on the observed binomial frequency",
    }


def _partition_controls(adjacency: list[set[int]], pairs: list[tuple[int, int]],
                        anti_left: list[int], anti_right: list[int],
                        *, samples_per_seed: int, seed_count: int, seed: int) -> dict[str, Any]:
    anti_rank = eqbit.cut_rank(adjacency, anti_left, anti_right)
    transversal_raw: list[int] = []
    balanced_raw: list[int] = []
    per_seed: list[dict[str, Any]] = []
    seeds = [seed + i * 10007 for i in range(seed_count)]
    vertices = list(range(len(adjacency)))

    for seed_value in seeds:
        rng_transversal = random.Random(seed_value ^ 0x5A17C9E3)
        rng_balanced = random.Random(seed_value ^ 0x2F6E2B1D)
        t_values: list[int] = []
        b_values: list[int] = []
        for _ in range(samples_per_seed):
            left: list[int] = []
            right: list[int] = []
            for a, b in pairs:
                if rng_transversal.getrandbits(1):
                    left.append(a)
                    right.append(b)
                else:
                    left.append(b)
                    right.append(a)
            t_values.append(eqbit.cut_rank(adjacency, left, right))

            balanced_left = rng_balanced.sample(vertices, len(vertices) // 2)
            left_set = set(balanced_left)
            balanced_right = [v for v in vertices if v not in left_set]
            b_values.append(eqbit.cut_rank(adjacency, balanced_left, balanced_right))

        transversal_raw.extend(t_values)
        balanced_raw.extend(b_values)
        per_seed.append({
            "seed": seed_value,
            "transversal": _rank_summary(t_values, anti_rank),
            "balanced": _rank_summary(b_values, anti_rank),
        })

    return {
        "seed_schedule": seeds,
        "samples_per_seed_per_family": samples_per_seed,
        "antipodal_reference_rank": anti_rank,
        "transversal": _rank_summary(transversal_raw, anti_rank),
        "balanced": _rank_summary(balanced_raw, anti_rank),
        "raw_transversal_ranks": transversal_raw,
        "raw_balanced_ranks": balanced_raw,
        "per_seed": per_seed,
    }


def _relabel_control(adjacency: list[set[int]], left: list[int],
                     right: list[int], seed: int) -> dict[str, Any]:
    original = eqbit.cut_rank(adjacency, left, right)
    permutation = list(range(len(adjacency)))
    random.Random(seed).shuffle(permutation)
    relabeled: list[set[int]] = [set() for _ in adjacency]
    for old_vertex, neighbors in enumerate(adjacency):
        relabeled[permutation[old_vertex]] = {permutation[v] for v in neighbors}
    relabeled_rank = eqbit.cut_rank(
        relabeled,
        [permutation[v] for v in left],
        [permutation[v] for v in right],
    )
    return {
        "seed": seed,
        "original_cut_rank": original,
        "relabelled_cut_rank": relabeled_rank,
        "invariant": original == relabeled_rank,
        "interpretation": "implementation sanity check, not an independent null family",
    }


def _degree_preserving_rewire(adjacency: list[set[int]], *, attempts: int,
                              seed: int, anti_left: list[int],
                              anti_right: list[int]) -> dict[str, Any]:
    """Double-edge-switch null; does not preserve spectrum or Gosset incidence."""
    if attempts < 0:
        raise ValueError("rewire attempts must be nonnegative")
    edges = [(u, v) for u, neighbors in enumerate(adjacency) for v in neighbors if u < v]
    edge_set = set(edges)
    original_degrees = sorted(len(row) for row in adjacency)
    rng = random.Random(seed)
    accepted = 0

    for _ in range(attempts):
        if len(edges) < 2:
            break
        i, j = rng.sample(range(len(edges)), 2)
        a, b = edges[i]
        c, d = edges[j]
        if len({a, b, c, d}) != 4:
            continue
        if rng.getrandbits(1):
            new1, new2 = (min(a, d), max(a, d)), (min(c, b), max(c, b))
        else:
            new1, new2 = (min(a, c), max(a, c)), (min(b, d), max(b, d))
        if new1 == new2 or new1 in edge_set or new2 in edge_set:
            continue
        edge_set.remove(edges[i])
        edge_set.remove(edges[j])
        edge_set.add(new1)
        edge_set.add(new2)
        edges[i], edges[j] = new1, new2
        accepted += 1

    rewired: list[set[int]] = [set() for _ in adjacency]
    for u, v in edges:
        rewired[u].add(v)
        rewired[v].add(u)
    degree_sequence_preserved = sorted(len(row) for row in rewired) == original_degrees
    if not degree_sequence_preserved:
        raise AssertionError("double-edge switching failed to preserve the degree sequence")
    cut_rank = eqbit.cut_rank(rewired, anti_left, anti_right)
    return {
        "seed": seed,
        "attempts": attempts,
        "accepted_switches": accepted,
        "original_edge_count": len(adjacency) * 56 // 2,
        "rewired_edge_count": sum(map(len, rewired)) // 2,
        "degree_sequence_preserved": degree_sequence_preserved,
        "fixed_original_antipodal_partition_cut_rank": cut_rank,
        "interpretation": (
            "degree-preserving graph-null only; the original antipodal map is not "
            "assumed to remain an automorphism and no spectral preservation is claimed"
        ),
    }


def _abom_probe_controls(cases: list[dict[str, Any]], *, seed: int) -> dict[str, Any]:
    energies = [float(case["ET"]) for case in cases]
    rng_permutation = random.Random(seed ^ 0x1F123BB5)
    permutation = list(energies)
    rng_permutation.shuffle(permutation)
    rng_shuffle = random.Random(seed ^ 0x6C8E9CF5)
    shuffled = list(energies)
    rng_shuffle.shuffle(shuffled)
    low, high = min(energies), max(energies)
    rng_range = random.Random(seed ^ 0x3A5F17D9)
    range_matched = [rng_range.uniform(low, high) for _ in energies]

    probes = {
        "frozen_ET_baseline": energies,
        "zero_probe": [0.0] * len(energies),
        "seeded_permutation": permutation,
        "seeded_shuffle": shuffled,
        "range_matched_uniform_random": range_matched,
    }
    channel_results: dict[str, Any] = {}
    for label, values in probes.items():
        samples = [
            abom_v8_sample(0.0, 0.0, 0.0, energy=value,
                           chemical_potential=0.0, kT=1.0)
            for value in values
        ]
        channel_results[label] = {
            "input_values": values,
            "fermi": [sample["fermi"] for sample in samples],
            "fermi_weighted_field": [sample["fermi_weighted_field"] for sample in samples],
            "e8_root_count_view": [sample["e8_root_count"] for sample in samples],
            "radial_field": [sample["radial_field"] for sample in samples],
        }
    return {
        "seed": seed,
        "input_semantics": "dimensionless probe only; ET is not assigned physical energy units",
        "control_families": channel_results,
    }


def _ns_snapshot_output(ns_payload: dict[str, Any], ns_source_path: Path) -> dict[str, Any]:
    cases = ns_payload["cases"]
    return {
        "case_count": len(cases),
        "dimensions": sorted({int(case["d"]) for case in cases}),
        "frozen_snapshot_sha256": _file_hash(ns_source_path),
        "snapshot_payload_sha256": _object_hash(ns_payload),
        "cases": [
            {key: case[key] for key in
             ("n", "d", "nu", "T", "dt", "steps", "ET", "OmT", "max_div_T")}
            for case in cases
        ],
        "status": "frozen finite-time benchmark data; Navier-Stokes regularity not tested",
    }


def _execute_configuration(name: str, included_modules: tuple[str, ...],
                           ns_payload: dict[str, Any], ns_source_path: Path, *,
                           samples_per_seed: int, seed_count: int, seed: int,
                           rewire_attempts: int) -> dict[str, Any]:
    """Execute one ablation configuration; omitted adapters are never invoked."""
    started = time.perf_counter()
    tracemalloc.start()
    outputs: dict[str, Any] = {
        "NS": _ns_snapshot_output(ns_payload, ns_source_path),
    }
    checks: dict[str, str] = {"NS.snapshot_schema_and_time_grid": "PASS"}
    try:
        if "ABOM" in included_modules:
            abom = _abom_probe_controls(ns_payload["cases"], seed=seed)
            family_names = set(abom["control_families"])
            expected_families = {
                "frozen_ET_baseline", "zero_probe", "seeded_permutation",
                "seeded_shuffle", "range_matched_uniform_random",
            }
            if family_names != expected_families:
                raise AssertionError("ABOM control family set is incomplete")
            if any(len(row["fermi"]) != len(ns_payload["cases"])
                   for row in abom["control_families"].values()):
                raise AssertionError("ABOM channel output length mismatch")
            outputs["ABOM"] = abom
            checks["ABOM.probe_controls_and_channel_lengths"] = "PASS"

        if "E8_COMPARISON" in included_modules:
            e8 = _e8_abom_comparison()
            if (e8["exact_root_count"] != 240
                    or e8["exact_unique_root_count"] != 240
                    or e8["abom_adapter_raw_root_count"] != 240
                    or e8["abom_adapter_unique_root_count"] != 240
                    or not e8["all_exact_norm_squared_two"]
                    or not e8["all_adapter_norm_squared_two"]
                    or not e8["root_sets_equal"]):
                raise AssertionError("ABOM/E8 exact root-set comparison failed")
            outputs["E8_COMPARISON"] = e8
            checks["E8.exact_root_set_count_norm_and_hash"] = "PASS"

        if "LEECH" in included_modules:
            leech = leech_unimodular_basis_audit()
            if (leech.get("rank") != 24
                    or not leech.get("even_unimodular")
                    or leech.get("basis_columns_checked") != 24
                    or leech.get("minimum_norm_attained") != 4
                    or leech.get("minimal_vectors_at_minimum") != 196560):
                raise AssertionError("full Leech basis/Golay/minimal-shell audit failed")
            outputs["LEECH"] = leech
            checks["LEECH.rank_basis_even_unimodular_minimal_shell"] = "PASS"

        if "EQBIT" in included_modules:
            graph_summary, roots, adjacency, pairs, anti_left, anti_right, anti_map = _graph_contract()
            partition_controls = _partition_controls(
                adjacency, pairs, anti_left, anti_right,
                samples_per_seed=samples_per_seed, seed_count=seed_count, seed=seed,
            )
            relabel_control = _relabel_control(
                adjacency, anti_left, anti_right, seed ^ 0x4E534142
            )
            if not relabel_control["invariant"]:
                raise AssertionError("cut rank changed under vertex relabeling")
            graph_null = _degree_preserving_rewire(
                adjacency, attempts=rewire_attempts, seed=seed ^ 0x7A11C0DE,
                anti_left=anti_left, anti_right=anti_right,
            )
            if (not graph_null["degree_sequence_preserved"]
                    or graph_null["rewired_edge_count"] != graph_null["original_edge_count"]):
                raise AssertionError("degree-preserving graph-null contract failed")
            outputs["EQBIT"] = {
                "graph": graph_summary,
                "partition_controls": partition_controls,
                "vertex_relabeling_control": relabel_control,
                "degree_preserving_graph_null": graph_null,
                "alternative_valid_involutions": {
                    "status": "NOT_SEARCHED",
                    "reason": "the preregistered optional secondary comparison is not implemented",
                },
                "graph_state_boundary": (
                    "exact graph-state cut-rank mathematics for a specified graph and cut; "
                    "no physical quantum dynamics, hardware, or quantum advantage claim"
                ),
            }
            checks["EQBIT.graph_partition_relabel_and_degree_null"] = "PASS"

        current_bytes, peak_bytes = tracemalloc.get_traced_memory()
    finally:
        if tracemalloc.is_tracing():
            _, peak_bytes = tracemalloc.get_traced_memory()
            tracemalloc.stop()

    elapsed = time.perf_counter() - started
    hashes = {key: _object_hash(value) for key, value in outputs.items()}
    return {
        "configuration": name,
        "included_modules": list(included_modules),
        "outputs": outputs,
        "output_sha256": hashes,
        "validation_checks": checks,
        "measurement": {
            "runtime_seconds": elapsed,
            "peak_python_heap_bytes": peak_bytes,
            "memory_method": "tracemalloc peak; Python-managed allocations only, not process RSS or native-library allocations",
        },
    }


def _ablation_report(executions: dict[str, dict[str, Any]]) -> dict[str, Any]:
    full = executions["full_orchestration"]
    full_hashes = full["output_sha256"]
    rows: dict[str, Any] = {}
    for name, execution in executions.items():
        present = execution["included_modules"]
        omitted = [key for key in ("ABOM", "E8_COMPARISON", "LEECH", "EQBIT")
                   if key not in present]
        unchanged = [
            key for key, digest in execution["output_sha256"].items()
            if key in full_hashes and full_hashes[key] == digest
        ]
        changed = [
            key for key, digest in execution["output_sha256"].items()
            if key in full_hashes and full_hashes[key] != digest
        ]
        rows[name] = {
            "present_modules": present,
            "omitted_modules": omitted,
            "output_sha256": execution["output_sha256"],
            "unchanged_output_hashes_vs_full": unchanged,
            "changed_output_hashes_vs_full": changed,
            "validation_checks_executed": execution["validation_checks"],
            "runtime_seconds": execution["measurement"]["runtime_seconds"],
            "peak_python_heap_bytes": execution["measurement"]["peak_python_heap_bytes"],
            "memory_method": execution["measurement"]["memory_method"],
            "shared_measured_observable_changes": [],
            "interpretation": (
                "This configuration independently executed only its listed adapters. "
                "The current modules expose no preregistered shared cross-module observable; "
                "omission therefore changes output availability, not a fabricated aggregate score."
            ),
        }
    return {
        "execution_mode": "independent_reexecution_per_configuration",
        "configurations": rows,
        "common_frozen_ns_snapshot_sha256": full_hashes["NS"],
        "shared_observable_status": "NOT_DEFINED_BY_CURRENT_MODULE_CONTRACTS",
        "acceptance_note": (
            "Every configuration is executed separately on the same frozen NS input and "
            "fixed seeds. Hash comparisons apply only to modules present in both runs."
        ),
    }


def _ablation_table(outputs: dict[str, Any]) -> dict[str, Any]:
    """Report output-removal ablations without fabricating a shared score."""
    full_keys = ("NS", "ABOM", "E8_COMPARISON", "LEECH", "EQBIT")
    configurations = {
        "full_orchestration": full_keys,
        "minus_ABOM_adapter": ("NS", "E8_COMPARISON", "LEECH", "EQBIT"),
        "minus_E8_comparison_adapter": ("NS", "ABOM", "LEECH", "EQBIT"),
        "minus_Leech_audit_adapter": ("NS", "ABOM", "E8_COMPARISON", "EQBIT"),
        "minus_flip_eqbit_adapter": ("NS", "ABOM", "E8_COMPARISON", "LEECH"),
        "NS_snapshot_only": ("NS",),
    }
    rows: dict[str, Any] = {}
    for name, keys in configurations.items():
        rows[name] = {
            "present_modules": list(keys),
            "output_sha256": {key: _object_hash(outputs[key]) for key in keys},
            "omitted_modules": [key for key in full_keys if key not in keys],
            "shared_measured_observable_changes": [],
            "interpretation": (
                "removal changes output availability only; no shared cross-module "
                "observable is currently defined"
            ),
        }
    return {
        "configurations": rows,
        "common_input_ns_snapshot_sha256": _object_hash(outputs["NS"]),
        "acceptance_note": "No scalar aggregate score is manufactured for disconnected modules.",
    }


def _source_provenance() -> dict[str, Any]:
    hashes = {}
    for relative in SOURCE_PATHS:
        path = _REPO_ROOT / relative
        hashes[relative] = _file_hash(path) if path.is_file() else None
    try:
        numpy_version = importlib.metadata.version("numpy")
    except importlib.metadata.PackageNotFoundError:
        numpy_version = None
    return {
        "repository_commit": _git_commit(),
        "source_sha256": hashes,
        "python": sys.version,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "numpy": numpy_version,
        "created_utc": datetime.now(timezone.utc).isoformat(),
    }


def run(*, ns_results: str | Path = DEFAULT_NS_RESULTS,
        samples_per_seed: int = 1000, seed_count: int = 10,
        seed: int = DEFAULT_SEED, rewire_attempts: int = 25000) -> dict[str, Any]:
    if samples_per_seed < 1 or seed_count < 1:
        raise ValueError("samples_per_seed and seed_count must be positive")
    if rewire_attempts < 0:
        raise ValueError("rewire_attempts must be nonnegative")

    ns_source_path = Path(ns_results)
    ns_payload = load_ns_snapshot(ns_source_path)
    full_modules = ("NS", "ABOM", "E8_COMPARISON", "LEECH", "EQBIT")
    configurations = {
        "full_orchestration": full_modules,
        "minus_ABOM_adapter": ("NS", "E8_COMPARISON", "LEECH", "EQBIT"),
        "minus_E8_comparison_adapter": ("NS", "ABOM", "LEECH", "EQBIT"),
        "minus_Leech_audit_adapter": ("NS", "ABOM", "E8_COMPARISON", "EQBIT"),
        "minus_flip_eqbit_adapter": ("NS", "ABOM", "E8_COMPARISON", "LEECH"),
        "NS_snapshot_only": ("NS",),
    }
    executions = {
        name: _execute_configuration(
            name, modules, ns_payload, ns_source_path,
            samples_per_seed=samples_per_seed, seed_count=seed_count,
            seed=seed, rewire_attempts=rewire_attempts,
        )
        for name, modules in configurations.items()
    }
    full_execution = executions["full_orchestration"]
    outputs = full_execution["outputs"]
    hashes = full_execution["output_sha256"]

    return {
        "schema": "pan.ns_abom_e8_leech_eqbit_002_valdora.v2",
        "experiment_id": "NS-ABOM-E8-LEECH-EQBIT-002-VALDORA",
        "seat": "Valdora (OpenAI / ChatGPT bench)",
        "mode": "independent_preregistered_ablation_execution",
        "preregistration": "research/NS_ABOM_E8_LEECH_EQBIT_002_ABLATION.md",
        "run_parameters": {
            "samples_per_seed_per_partition_family": samples_per_seed,
            "seed_count": seed_count,
            "seed_schedule": [seed + i * 10007 for i in range(seed_count)],
            "rewire_attempts": rewire_attempts,
            "base_seed": seed,
            "configuration_count": len(configurations),
        },
        "provenance": _source_provenance(),
        "module_outputs": outputs,
        "module_output_sha256": hashes,
        "ablation": _ablation_report(executions),
        "configuration_measurements": {
            name: execution["measurement"] for name, execution in executions.items()
        },
        "pairwise_status": {
            "NS_ABOM": "DIMENSIONLESS_PROBE_SENSITIVITY_ONLY",
            "ABOM_E8": "EXACT_ROOT_SET_EQUALITY_CHECKED_WITHOUT_SNAPPING",
            "E8_GOSSET_EQBIT": "EXPLICIT_ROOT_VERTEX_BIJECTION_AND_ANTIPODAL_AUTOMORPHISM_CHECKED",
            "E8_LEECH": "SEPARATE_CERTIFICATES_NO_EMBEDDING",
            "LEECH_EQBIT": "SEPARATE_TYPED_ARTIFACTS_NO_EMBEDDING",
            "NS_EQBIT": "NOT_COUPLED",
        },
        "dimensional_firewall": {
            "NS_spatial_domains": [2, 3],
            "PAN_V8_coordinates": ["h", "R", "u", "d", "tau", "chi", "s", "f"],
            "E8_root_space_rank": 8,
            "Leech_lattice_rank": 24,
            "Gosset_graph_vertices": 240,
            "warning": (
                "These are distinct mathematical objects. V8 coordinates are not E8 "
                "coordinates; Leech rank is not spatial dimension; no 9D fluid domain "
                "or common physical metric is defined."
            ),
        },
        "evidence_grade": {
            "exact_algebraic": ["E8 root-set comparison", "Leech certificate", "GF(2) cut ranks"],
            "deterministic_software": ["snapshot validation", "module adapters", "vertex relabeling invariance"],
            "sampled_statistics": ["random antipodal transversals", "random balanced cuts", "degree-preserving graph null"],
            "physical_validation": "not_claimed",
            "navier_stokes_regular_or_singular": "not_tested",
        },
        "interpretation": [
            "The ABOM control family measures sensitivity to declared dimensionless probe sequences only.",
            "The E8/ABOM check compares canonical root sets without rounding near-roots onto exact roots.",
            "The E8/ABOM check compares canonical root sets, not just cardinalities.",
            "The E8/Gosset check supplies an explicit root-to-vertex coordinate bijection.",
            "The antipodal map is checked as a fixed-point-free involutive graph automorphism.",
            "The Leech result is an independent rank-24 lattice certificate; no E8-to-Leech embedding is proposed.",
            "The graph-null preserves degree by double-edge switches; no spectral preservation is claimed.",
            "Each ablation configuration re-executes only the adapters it includes; no shared scalar is invented.",
            "Alternative valid fixed-point-free involutions are explicitly NOT_SEARCHED.",
            "Ablations remove module outputs; disconnected modules are not assigned a synthetic coupling score.",
            "No numerical or software result here establishes Navier-Stokes regularity or blow-up.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ns-results", type=Path, default=DEFAULT_NS_RESULTS)
    parser.add_argument("--samples-per-seed", type=int, default=1000)
    parser.add_argument("--seed-count", type=int, default=10)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--rewire-attempts", type=int, default=25000)
    parser.add_argument(
        "--output", type=Path,
        default=Path("experiments/ns_abom_e8_leech_eqbit_002_valdora/results.json"),
    )
    args = parser.parse_args()
    result = run(
        ns_results=args.ns_results,
        samples_per_seed=args.samples_per_seed,
        seed_count=args.seed_count,
        seed=args.seed,
        rewire_attempts=args.rewire_attempts,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "output": str(args.output),
        "experiment_id": result["experiment_id"],
        "module_output_sha256": result["module_output_sha256"],
        "partition_summary": result["module_outputs"]["EQBIT"]["partition_controls"],
        "leech": {
            "rank": result["module_outputs"]["LEECH"]["rank"],
            "minimum_norm": result["module_outputs"]["LEECH"]["minimum_norm_attained"],
            "minimal_vectors": result["module_outputs"]["LEECH"]["minimal_vectors_at_minimum"],
        },
        "pairwise_status": result["pairwise_status"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
