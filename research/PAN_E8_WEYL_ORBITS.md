# E8 Weyl Root-Orbit Audit — v0

**Status:** isolated research branch; no production wiring and no changes to the V8 schema.

## Mathematical target

Use the canonical exact E8 root set from `core/geometry/e8_root_system.py` (240 roots in Q^8, each squared norm 2). Use the eight exact simple roots already provided there. For each simple root alpha, apply the reflection

    s_alpha(v) = v - 2 (v, alpha) / (alpha, alpha) alpha
              = v - (v, alpha) alpha

because every E8 root has squared norm 2.

## Computed results

The implementation builds eight permutations of the 240-root set and verifies each is a bijection and an involution. Breadth-first search over these eight generators computes the orbit of a root without enumerating the entire Weyl group.

The expected E8 exponents are 1, 7, 11, 13, 17, 19, 23, 29, giving

    |W(E8)| = product_i (m_i + 1) = 696,729,600.

The root action is transitive, so a selected root has orbit size 240. Orbit–stabilizer gives

    |Stab_W(E8)(alpha)| = 696,729,600 / 240 = 2,903,040.

There are 126 E8 roots orthogonal to the selected root. The expected E7 exponents 1, 5, 7, 9, 11, 13, 17 independently give |W(E7)| = 2,903,040. The code cross-checks these values. This supports the standard identification of the root stabilizer with an E7 Weyl subgroup, but the code does not enumerate that subgroup or provide a formal group-theoretic proof of the identification.

## Exact validation

Run:

    python -m unittest tests.test_e8_weyl_orbits -v
    python experiments/e8_weyl_orbit_audit.py

The test suite checks reflection permutations, involutions, exact norm preservation, transitivity, 126 orthogonal roots per root, and the orbit–stabilizer/E7-order cross-check.

## Scope boundaries

- No enumeration of all 696,729,600 Weyl group elements.
- No floating-point approximations in the reflection/orbit computation.
- The orbit–stabilizer quotient uses the established Weyl-group order from the E8 exponents.
- This is a finite root-system audit, not a Banach–Tarski construction.
- It does not establish physical dynamics, physical volume duplication, or a physical interpretation of PAN.
- Janus Hydra and UHFE/UDFE are not modified or conflated.
- The canonical V8 coordinate order remains (h, R, u, d, tau, chi, s, f).

## Follow-on

A later module can explicitly generate the E7 stabilizer subgroup from the simple reflections perpendicular to a selected root, verify its action on the 126-root perpendicular subsystem, and then test carefully typed equivariant maps to Janus Hydra's five dynamic inverse pairs. Those maps must be proposed and justified rather than inferred from visual similarity.
