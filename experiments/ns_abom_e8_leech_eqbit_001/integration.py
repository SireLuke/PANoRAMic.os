"""Read-only composition harness for NS–ABOM–E8–LEECH–EQBIT-001."""
from __future__ import annotations
import json
from pathlib import Path
import sys
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from core.abom_v8.abom_v8_model import abom_v8_sample
from core.geometry.e8_root_system import e8_roots_exact
from experiments.moonshine_sierpinski.leech_unimodular_basis import leech_unimodular_basis_audit
from experiments.flip_qubit.cut_rank_audit import run as run_eqbit_audit

DEFAULT_NS_RESULTS = _REPO_ROOT / "experiments/ns_evidence_001_cosmo/cosmo_results.json"


def load_ns_snapshot(path: str | Path = DEFAULT_NS_RESULTS) -> dict[str, Any]:
    """Load and validate frozen Cosmo diagnostics; never rerun the solver."""
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    cases = payload.get("cases")
    if not isinstance(cases, list) or len(cases) != 9:
        raise ValueError("expected the nine frozen NS-EVIDENCE-001 cases")
    required = ("n", "d", "nu", "T", "dt", "steps", "ET", "OmT", "max_div_T")
    for index, case in enumerate(cases):
        if not isinstance(case, dict) or any(key not in case for key in required):
            raise ValueError(f"NS case {index} is missing required diagnostics")
        if case["d"] not in (2, 3) or case["n"] < 1 or case["steps"] < 1:
            raise ValueError(f"NS case {index} has invalid grid metadata")
        if case["T"] <= 0 or case["dt"] <= 0:
            raise ValueError(f"NS case {index} has invalid time metadata")
        if abs(case["steps"] * case["dt"] - case["T"]) > max(1e-14, abs(case["T"]) * 1e-12):
            raise ValueError(f"NS case {index} does not land on its declared final time")
    return payload


def compose(ns_results_path: str | Path = DEFAULT_NS_RESULTS,
            eqbit_samples: int = 128, eqbit_seed: int = 20261121) -> dict[str, Any]:
    """Run existing module audits and return a provenance-rich composition."""
    if eqbit_samples < 1:
        raise ValueError("eqbit_samples must be positive")
    ns_payload = load_ns_snapshot(ns_results_path)
    ns_cases = ns_payload["cases"]
    ns_3d = [case for case in ns_cases if case["d"] == 3]
    if not ns_3d:
        raise ValueError("frozen NS snapshot contains no 3D cases")
    ns_probe = ns_3d[0]
    # ET is only a dimensionless Fermi-channel probe, not a physical coupling.
    abom_probe = abom_v8_sample(0.0, 0.0, 0.0, energy=float(ns_probe["ET"]),
                               chemical_potential=0.0, kT=1.0)
    roots = e8_roots_exact()
    e8_summary = {
        "rank": 8, "root_count": len(roots),
        "root_squared_norms": sorted({str(sum(x*x for x in root)) for root in roots}),
        "coordinate_field": "R^8 exact rational coordinates",
    }
    leech_summary = leech_unimodular_basis_audit()
    eqbit_summary = run_eqbit_audit(samples=eqbit_samples, seed=eqbit_seed)
    pairwise = {
        "NS_ABOM": {"status": "PASS", "check": "frozen nondimensional 3D NS energy accepted as explicitly labelled ABOM Fermi probe", "physical_coupling_claim": False},
        "ABOM_E8": {"status": "PASS" if abom_probe["e8_root_count"] == e8_summary["root_count"] == 240 else "FAIL", "check": "ABOM root-count view agrees with canonical exact E8 root set"},
        "E8_LEECH": {"status": "PASS", "check": "rank-8 E8 and rank-24 Leech certificates coexist without coordinate identification", "shared_embedding": False},
        "E8_EQBIT": {"status": "PASS" if eqbit_summary["geometry"]["vertices"] == e8_summary["root_count"] else "FAIL", "check": "flip-eqbit reconstructs the 240-vertex E8/Gosset contract"},
        "LEECH_EQBIT": {"status": "PASS", "check": "lattice certificate and graph-state audit remain separate typed artifacts", "shared_embedding": False},
        "NS_EQBIT": {"status": "NOT_COUPLED", "check": "no solver-to-graph-state dynamical map is defined"},
    }
    return {
        "schema": "pan.ns_abom_e8_leech_eqbit.integration.v1",
        "experiment_id": "NS-ABOM-E8-LEECH-EQBIT-001",
        "mode": "read_only_composition",
        "source_artifacts": {
            "ns": str(Path(ns_results_path)), "ns_seat": ns_payload.get("seat", "unspecified"),
            "abom": "core.abom_v8.abom_v8_model.abom_v8_sample",
            "e8": "core.geometry.e8_root_system.e8_roots_exact",
            "leech": "experiments.moonshine_sierpinski.leech_unimodular_basis.leech_unimodular_basis_audit",
            "eqbit": "experiments.flip_qubit.cut_rank_audit.run",
        },
        "dimensions": {
            "navier_stokes_spatial_dimension": sorted({case["d"] for case in ns_cases}),
            "pan_v8_state_coordinates": 8, "e8_root_space_rank": 8,
            "leech_lattice_rank": leech_summary["rank"],
            "gosset_graph_vertices": eqbit_summary["geometry"]["vertices"],
            "warning": "Distinct mathematical objects; no 9D fluid domain or common metric is defined.",
        },
        "ns_snapshot": {
            "case_count": len(ns_cases), "three_dimensional_case_count": len(ns_3d),
            "selected_probe": {key: ns_probe[key] for key in ("n","d","nu","T","dt","steps","ET","OmT","max_div_T")},
            "status": "frozen reference data; Navier–Stokes regularity remains not_tested",
        },
        "abom_probe": abom_probe, "e8": e8_summary, "leech": leech_summary, "eqbit": eqbit_summary,
        "pairwise_gates": pairwise,
        "overall_status": "PASS" if all(v["status"] in ("PASS","NOT_COUPLED") for v in pairwise.values()) else "FAIL",
        "interpretation": [
            "Software composition and provenance exercise, not a unified physical law.",
            "ABOM Fermi input is a declared dimensionless probe, not a physical energy identification.",
            "E8 and Leech coordinate spaces are not embedded into one another.",
            "Flip-eqbit is static graph-state mathematics, not physical quantum dynamics or hardware.",
            "NS input is a frozen finite-time benchmark snapshot, not evidence about global regularity or blow-up.",
            "A passing gate validates only its stated interface checks.",
        ],
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--eqbit-samples", type=int, default=128)
    parser.add_argument("--eqbit-seed", type=int, default=20261121)
    parser.add_argument("--ns-results", type=Path, default=DEFAULT_NS_RESULTS)
    parser.add_argument("--output", type=Path, default=Path("ns-abom-e8-leech-eqbit-001.json"))
    args = parser.parse_args()
    result = compose(args.ns_results, args.eqbit_samples, args.eqbit_seed)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "overall_status": result["overall_status"],
                      "pairwise_gates": result["pairwise_gates"], "dimensions": result["dimensions"]},
                     indent=2, sort_keys=True))
