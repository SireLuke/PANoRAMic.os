# ABOM-v8 exploratory integration model

This module is a **testable mathematical composition**, not a claim that its
components form a single physical law. It keeps component outputs separate so
that each can be tested before any coupling is treated as meaningful.

## Included components

- Exponential scale coordinates: `x = log2(L / L0)` and inverse `L = L0 * 2**x`.
- Golden-ratio channels: `phi * 2**x`, `phi_inverse * 2**x`, and their explicitly signed counterparts.
- Fermi-Dirac occupation, complementary hole fraction, and signed contrast.
- E8 root generator: 240 roots in R^8, each with squared norm 2.
- A caller-supplied 6x6 basis transform for the crystalline-coordinate layer.
- Hyperoctahedral signed coordinate permutations; `|B_n| = 2**n * n!`.
- A radial exponential field, `2**sqrt(x*x+y*y+z*z)`, chosen because it is invariant under ordinary 3D rotations/reflections.
- Eight spatial octants from the signs of x, y, and z.
- A discrete harmonic-oscillator energy-level helper.
- A combined sample function that preserves occupation, hole, and signed-contrast channels separately.

## Important mathematical distinctions

1. The eight **spatial octants** of (x,y,z) are not the eight coordinates of V8.
   An eight-dimensional space has 2^8 = 256 sign orthants. The model's octant
   helper intentionally describes 3D space and must not be mislabeled as an
   exhaustive partition of the V8 manifold.
2. E8 has 240 roots, rank 8, and Lie algebra dimension 248. The E8 Weyl group
   has order 696,729,600; this is distinct from the hyperoctahedral B8 group
   order 10,321,920.
3. `n_h = 1 - n` is a complementary occupation fraction. Its negative/positive
   contrast is not automatically a literal negative-energy sea.
4. The oscillator formula `E_n = hbar*omega*(n+1/2)` uses n >= 0. The model does not
   invent physical oscillator states at negative n.
5. The six-dimensional lattice is not uniquely determined by dimension alone.
   The implementation requires a caller-supplied basis matrix; a specific
   crystal/lattice family must define that matrix and its metric.
6. A scalar radial exponential is rotationally symmetric, but adding an
   anisotropic lattice or axis-specific channels can break that symmetry.
   Symmetry claims must be tested on the fully combined field.
7. No E8-to-SU(3), QCD, or physical quantum-field coupling is assumed. Such a
   mapping would require an explicit representation/embedding and validation.

## Run tests

From the repository root with Python 3.10+:

```bash
python -m unittest discover -s tests -p 'test_abom_v8_model.py' -v
```

The tests check round-trip scale recovery, golden-ratio identities, Fermi
complementarity, E8 root count/norms, signed-permutation invariance, basis
mapping, octant coverage, radial symmetry, oscillator levels, and integration
channel separation. These tests do not validate a physical theory.
