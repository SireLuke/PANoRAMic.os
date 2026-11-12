# PAN V8 Dynamic Frame and Spin(8) 720-Degree Audit

**Status:** Isolated computational research implementation. This is a representation/invariant audit, not a new physical law.

## Architectural placement

This experiment sits between the canonical E8/Gosset geometry and the PAN V8 / Janus Hydra evaluation path:

1. **Canonical geometry:** 240 exact E8 roots, each with squared norm 2, define Gosset 4_21.
2. **Dynamic frame adapter:** a time-varying orthogonal frame acts on labelled root coordinates while the shared origin remains fixed.
3. **Spin(8) representation audit:** the spin lift is tracked separately from the vector representation.
4. **Radial deformation:** positive radial undulation is tested separately from rigid frame motion.
5. **Field/semantic layers:** UHFE and UDFE retain independent histories; Janus Hydra remains the translator, not either field.

## Why 720 degrees?

For an ordinary vector in a single oriented 2-plane, a 360-degree rotation returns the vector. The corresponding spin representation has a double-cover property: the lifted 360-degree loop changes sign, and the 720-degree loop returns to its original sign.

For four mutually orthogonal 2-planes, the Spin(8) central sign is the parity of the sum of the plane windings. Consequently, four simultaneous 360-degree plane rotations have even winding parity and produce +1. This is why the audit reports both a single-plane loop and a four-plane torus loop instead of treating “720 degrees” as a universal scalar rule.

The current implementation computes this closed-loop central sign only. It does **not** implement explicit spinor coordinates, gamma matrices, or a full Spin(8) representation matrix.

## Geometric invariants

- Fixed reference origin: Q(t) 0 = 0.
- Rigid frame action: Q(t) in SO(8), built from four commuting oriented 2-plane rotations.
- Root identity: root labels remain in their original order.
- Norms and the complete labelled Gram matrix are preserved numerically.
- Central inversion x -> -x maps every E8 root to its antipode. In eight dimensions its determinant is +1.
- A generic SO(8) rotation does not generally preserve the fixed-coordinate E8 root set; it preserves the rotated configuration's intrinsic metric. Do not call every moving-frame orientation an E8 lattice automorphism.
- Hyperplane reflections are not silently folded into SO(8): they have determinant -1 and belong in a separately labelled orientation-reversing test.

## Undulation

The illustrative law r(phase) = exp(a sin(phase)) is positive for finite real phase and bounded amplitude. It is only a controlled deformation fixture. At zero amplitude the unit-direction radius returns to one. A deformed radial boundary is not an exact rigid Gosset polytope, even when it is represented over the same directional domain.

## Research experiment matrix

| Experiment | Primary question | Pass criteria |
|---|---|---|
| V8-FRAME-001 | Can the moving SO(8) frame preserve the fixed origin and Gosset intrinsic metric? | 240 labelled roots; norm and Gram errors below tolerance |
| V8-SPIN-720-001 | Does the single-plane Spin(8) lift exhibit the 360° sign flip and 720° return? | -1 at 360°, +1 at 720° |
| V8-TORUS-002 | Are four-plane winding parities computed correctly? | even total winding gives +1 |
| V8-UNDULATION-002 | Does radial deformation remain positive and recover the reference radius at zero amplitude? | finite positive radii; zero-amplitude unit radius |
| V8-JANUS-003 | Can field histories be evaluated independently under a moving frame? | no forced UHFE/UDFE complement; no origin drift; deterministic reconstruction |

## Integration with the broader research harness

This audit is designed to run alongside the existing shared E8 root-system, Gosset local-cell-star, Coxeter projection robustness, E8 spherical-shell, E10 Coxeter/Lorentzian, Leech/VOA/Moonshine, and ABOM V8 fractional-Fermi-sea audits. Cross-domain comparisons must keep units and mathematical objects distinct. A passing geometry audit is not evidence for a physical spinor mechanism, FFS damping, E10 stabilization, or a new field equation.

## Reproduction

```bash
python -m unittest tests.test_v8_dynamic_frame_spin8_720_audit -v
python experiments/v8_dynamic_frame_spin8_720_audit.py
```

Numerical thresholds are implementation checks. The exact root generator remains the canonical source for E8 root coordinates.
