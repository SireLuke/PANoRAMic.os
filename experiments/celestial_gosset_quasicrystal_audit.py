"""Combined reference audit for celestial soft data and E8 model-set geometry.

The celestial identities and finite cut-and-project geometry are audited as
separate mathematical components. No physical coupling is asserted.
"""
from __future__ import annotations
import json
from pathlib import Path
import sys

_REPOSITORY_ROOT = str(Path(__file__).resolve().parents[1])
if _REPOSITORY_ROOT not in sys.path:
    sys.path.insert(0, _REPOSITORY_ROOT)

from core.geometry.e8_quasicrystal import run_quasicrystal_shell_audit
from core.holography.celestial import (
    CelestialChart8, CelestialPrimary, HardInsertion,
    leading_soft_gluon_ward_kernel, mellin_soft_factor, mellin_soft_residue,
)


def run_audit() -> dict:
    primary = CelestialPrimary(
        delta=1.0 + 0.25j, helicity=1.0, z=0.3 + 0.4j,
        color_weight_1=1.0, color_weight_2=-0.5, eta=1,
    )
    chart = CelestialChart8.from_primary(primary)
    reconstructed = chart.to_primary()
    chart_round_trip = (
        reconstructed == primary
        and CelestialChart8.from_vector(chart.as_vector()) == chart
    )
    pole_probe = mellin_soft_factor(1.25 + 0.0j, soft_power=1, cutoff=1.0)
    residue = mellin_soft_residue(soft_power=1, amplitude_coefficient=2.0 + 0.0j)
    ward_kernel = leading_soft_gluon_ward_kernel(
        z=0.25 + 0.5j,
        hard_insertions=(
            HardInsertion(0.0 + 0.0j, 1.0 + 0.0j),
            HardInsertion(1.0 + 0.0j, -1.0 + 0.0j),
        ),
    )
    return {
        "audit": "pan_celestial_gosset_quasicrystal_v0",
        "celestial": {
            "chart_coordinate_order": [
                "ReDelta", "ImDelta", "helicity", "Re(z)", "Im(z)",
                "SU3_Cartan_weight_1", "SU3_Cartan_weight_2", "in_out_eta",
            ],
            "primary_weights": {
                "h": [primary.weights[0].real, primary.weights[0].imag],
                "hbar": [primary.weights[1].real, primary.weights[1].imag],
            },
            "chart_round_trip": chart_round_trip,
            "leading_soft_mellin_probe_at_Delta_1.25": [
                pole_probe.real, pole_probe.imag
            ],
            "leading_soft_residue_at_Delta_1": [residue.real, residue.imag],
            "sample_fixed_color_current_kernel": [
                ward_kernel.real, ward_kernel.imag
            ],
            "scope": (
                "Mellin pole and current Ward-kernel bookkeeping; not a "
                "scattering-amplitude solver or full non-Abelian current algebra"
            ),
        },
        "quasicrystal": run_quasicrystal_shell_audit(),
        "bridge_status": (
            "separate baselines are audited; a data-preserving celestial-to-"
            "V8/E8 coupling is not yet defined"
        ),
    }


if __name__ == "__main__":
    print(json.dumps(run_audit(), indent=2, sort_keys=True))
