# PAN Moonshine × Sierpiński bridge (research v1)

This experiment reuses the repository's exact E8 root system and existing
Gosset/Coxeter-plane/Sierpiński implementation. It adds two independent
mathematical reference tracks:

1. finite-stage Sierpiński gasket graph Laplacians and low-stage numerical spectra;
2. exact low-order modular-form q-series for E8 products and the Leech theta identity.

## Existing repository foundation

- The existing Python experiment computes 240 E8 roots, 6,720 Gosset edges,
  60,480 equilateral 8D triangular faces, and 2,160 projected equilateral
  faces in 72 C30 orbits.
- Existing TypeScript checks cover Sierpiński recursion counts, retained area,
  similarity dimension, D3 symmetry, projection-seeded recursion.
- STRATA-0.1 already defines a claim ladder, provenance, randomized controls,
  held-out evaluation, and explicit not_tested states.

## New v1 checks

- Build finite gasket graphs recursively and compute combinatorial-Laplacian
  eigenvalues for bounded stages using a symmetric Jacobi method.
- Retain exact graph counts and integer Laplacian trace invariants at larger
  stages without dense diagonalization.
- Compute E4, Delta, Theta(E8^k)=E4^k, and
  Theta_Leech=E4^3-720 Delta using exact integer coefficients.
- Record initial J=j-744 coefficients and 196884=1+196883 as reference
  fixtures, not as outputs derived by this implementation.

## Explicit limits

- E8^3 is not the Leech lattice. E8^3 has 720 norm-2 roots; Leech has none.
- The Leech theta identity is not a Leech coordinate construction. A later
  phase must implement and independently validate a Construction A realization
  from the extended binary Golay code: generator/parity conventions,
  integrality, evenness, determinant, and minimum norm.
- V-natural is not constructed here. Its Z2 orbifold requires the untwisted
  fixed-point algebra, twisted sector, and simple-current extension; simply
  subtracting 24 from a lattice partition function is not that construction.
- The Monster action and McKay-Thompson series are not computed.
- No correspondence between Sierpiński spectra and Monster/VOA data is
  asserted. Cross-system comparisons need preregistered statistics,
  randomized and structure-preserving controls, and held-out checks.
- No quantum-gravity duality or physical mechanism follows from these tests.

## Reproduction

```bash
python -m unittest tests.test_moonshine_sierpinski_bridge -v
python experiments/moonshine_sierpinski/sierpinski_graph_spectrum.py
python experiments/moonshine_sierpinski/lattice_modular_audit.py
```

All calculations use the Python standard library.


## Extended Golay / Leech construction phase

The branch now includes an explicit extended binary Golay generator and
Wilson/Conway parity-and-coset membership test. It checks the [24,12,8]
weight enumerator and enumerates the three minimal-vector families, totaling
196,560 vectors of lattice squared norm 4. The root count is therefore zero
within this constructed minimal shell.

The new code does not yet construct a full lattice basis or independently
verify its Gram determinant. It also does not construct the Moonshine VOA.


## Leech lattice VOA character precursor

The branch computes the Leech lattice VOA character
Theta_Leech/eta^24 with exact integer q-series arithmetic and checks the first
graded dimensions 1, 24, 196884, 21493760. This is V_Lambda, not V-natural:
the Z2 fixed-point and twisted-sector extension remains a distinct next task.
