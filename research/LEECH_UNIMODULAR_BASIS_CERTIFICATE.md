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

## Minimum norm certificate

The same coordinate congruences, together with the extended Golay code's
minimum distance 8 and Type-II weight divisibility by four, exclude every
nonzero vector of lattice norm below four.

For common even parity, write x=2y. If y mod 2 is a nonzero Golay word,
at least eight coordinates of y are odd, so sum(y_i^2)>=8 and
||x/sqrt(8)||^2>=4. If y is even, write x=4z; the sum congruence forces
sum(z_i) even, so nonzero z has sum(z_i^2)>=2 and again the norm is at least
four.

For common odd parity, every coordinate is odd. A vector with all absolute
coordinates one would have either all plus signs (sum 24, not 4 mod 8), or
minus signs supported on a nonzero Golay word. The latter word has weight
divisible by four, so the coordinate sum is 24-2 wt(c), which is 0 mod 8,
again violating the required 4 mod 8. Thus at least one coordinate has
absolute value at least three, giving integral squared norm at least 32,
or lattice norm at least four.

The existing explicit three-family enumeration supplies 196,560 vectors
with integral squared norm 32, so the lower bound is attained. Therefore
the minimum nonzero lattice norm is exactly four.

## Scope boundary

This certifies the rank-24 basis, covolume, integrality, evenness,
unimodularity, and minimum norm. It does not construct the Leech VOA,
its orbifold extension, or the Monster action.

## Reproduction

`python -m unittest tests.test_leech_unimodular_basis -v`
`python experiments/moonshine_sierpinski/leech_unimodular_basis.py`
