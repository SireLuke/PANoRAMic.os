# Leech lattice: rank-24 basis and even-unimodular certificate

## Purpose

The existing Golay implementation verifies the [24,12,8] extended binary
Golay code and explicitly enumerates all 196,560 vectors in the three known
minimal-vector families. This audit fills the next structural gap: an explicit
rank-24 basis for the full coordinate lattice and an exact determinant check.

## Coordinate definition

The Leech lattice is represented as (L={x/sqrt{8}:xinmathbb Z^{24}}),
where the integral coordinate vector x satisfies:

1. all coordinates have common parity p;
2. the binary residue (((x-pmathbf 1)/2)mod 2) belongs to the extended
   Golay code C;
3. (sum_i x_iequiv4ppmod8).

Since C is Type II, every codeword has weight divisible by four. Writing
(x=pmathbf1+2c+4z), the final congruence reduces to
(sum_i z_iequiv ppmod2).

## Index / covolume calculation

The defining constraints give the exact index of the integral coordinate
lattice in Z^24:

- common coordinate parity: factor (2^{23});
- Golay residue subspace of dimension 12: factor (2^{12});
- final coordinate-sum parity condition: factor 2.

Thus the coordinate covolume is (2^{23+12+1}=2^{36}). Scaling each of
24 coordinates by (1/sqrt8) multiplies covolume by
((1/sqrt8)^{24}=8^{-12}=2^{-36}), giving lattice covolume one.

## Explicit basis and Gram matrix

The code stores a 24-by-24 integral coordinate basis. Every basis column is
checked against all three defining congruences. Its determinant is computed
with fraction-free Bareiss elimination and equals (2^{36}), exactly the
index-derived coordinate covolume. Therefore the columns form a basis of
the full coordinate lattice, not merely a finite-index sublattice.

For the scaled lattice basis, the Gram matrix is (G=B^TB/8). Every entry
is checked to be integral, every diagonal entry even, and the exact
determinant is one. Since (G=B^TB/8) with B invertible, it is positive
definite. This certifies that the Golay-defined lattice is even and
unimodular.

## Scope boundary

This is an exact basis, covolume, integrality, evenness and unimodularity
certificate. It does not independently prove that the minimum nonzero norm
is four; that is a separate shortest-vector problem. Nor does this audit
construct the Leech VOA, its orbifold extension, or the Monster action.

## Reproduction

`python -m unittest tests.test_leech_unimodular_basis -v`
`python experiments/moonshine_sierpinski/leech_unimodular_basis.py`
