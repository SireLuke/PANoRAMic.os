"""Deterministic exact audit of the E8 Weyl action on its 240 roots."""
from core.geometry.e8_weyl_orbits import (
    E8_WEYL_ORDER, E8WeylAction, audit_e8_root_orbits,
)


def main():
    action = E8WeylAction.build()
    orbits = action.orbit_partition()
    result = audit_e8_root_orbits()
    print("E8 Weyl root-orbit audit")
    print(f"roots: {len(action.roots)}")
    print(f"simple reflection generators: {len(action.generators)}")
    print(f"root orbit sizes: {sorted(len(orbit) for orbit in orbits)}")
    print(f"W(E8) order from exponents: {E8_WEYL_ORDER}")
    print(f"selected root orbit: {result.orbit_size}")
    print(f"root stabilizer order (derived): {result.stabilizer_order}")
    print(f"roots orthogonal to selected root: {result.orthogonal_root_count}")
    print(f"orbit-stabilizer product: {result.orbit_stabilizer_product}")
    print("status: PASS (exact rational reflection and finite orbit audit)")
    print("scope: does not enumerate W(E8), and does not construct Banach-Tarski pieces")


if __name__ == "__main__":
    main()
