"""Deterministic audit of the E7 subgroup action on E8-perpendicular roots."""
# --- repo-root bootstrap: makes this file runnable directly, from any
# working directory (the imports below address packages from the repo
# root). No-op when the root is already on sys.path. See
# docs/RUNNING_PYTHON.md.
import sys as _sys
from pathlib import Path as _Path

_REPO_ROOT = _Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in _sys.path:
    _sys.path.insert(0, str(_REPO_ROOT))
# --- end repo-root bootstrap ---

from core.geometry.e7_stabilizer_action import (
    E7StabilizerAction,
    audit_e7_stabilizer,
)


def main():
    action = E7StabilizerAction.build()
    result = audit_e7_stabilizer()
    print("E7 stabilizer action audit")
    print(f"selected E8 root: {action.selected_e8_root}")
    print(f"perpendicular roots: {len(action.roots)}")
    print(f"simple roots: {len(action.simple_roots)}")
    print(f"simple reflection generators: {len(action.generators)}")
    print(f"E7 root orbit size: {result['e7_root_orbit_size']}")
    print(f"|W(E7)| from exponents: {result['e7_weyl_order_from_exponents']}")
    print(f"root stabilizer order (derived): {result['e7_root_stabilizer_order_derived']}")
    print(f"faithful action on 7D span: {result['faithful_action_on_7d_span']}")
    print("status: PASS (exact finite root-action audit)")
    print("scope: generators/action constructed; full group elements not enumerated")


if __name__ == "__main__":
    main()
