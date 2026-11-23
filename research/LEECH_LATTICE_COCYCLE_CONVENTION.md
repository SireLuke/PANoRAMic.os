# Leech lattice 2-cocycle convention — G1b foundation

## What is implemented

The existing exact rank-24 Leech basis is now used to express integral
coordinate vectors in a canonical lattice basis. From its Gram matrix
\(G=B^TB/8\), this module defines one explicit bimultiplicative sign
cocycle.

In basis coordinates \(n,m\in\mathbb Z^{24}\), set
\[
\epsilon(n,m)=(-1)^{n^TCm},
\]
where \(C\) is lower triangular, \(C_{ii}=G_{ii}/2\), and
\(C_{ij}=G_{ij}\) for \(i>j\). The evenness and integrality of \(G\)
ensure
\[
C+C^T\equiv G\pmod 2.
\]
Thus the implementation has the expected lattice-VOA commutator
\[
\epsilon(n,m)/\epsilon(m,n)=(-1)^{(n,m)}
\]
and the diagonal normalization
\[
\epsilon(n,n)=(-1)^{(n,n)/2}.
\]
The 2-cocycle identity follows from bimultiplicativity and is tested on
deterministic random lattice-coordinate fixtures.

## Why this convention is explicit

A lattice-VOA cocycle is not a basis-free table of signs. Different
normalized choices can differ by a coboundary, changing basis-state phases
without changing the isomorphism class of the VOA. This implementation fixes
one convention relative to the repository's certified column basis. Raw
product signs must be interpreted together with this convention.

## Validation

Run:
```sh
python -m unittest tests.test_leech_lattice_cocycle -v
python -m experiments.moonshine_sierpinski.leech_lattice_cocycle
```

Tests cover exact basis-coordinate round trips, rejection of vectors outside
the basis lattice, normalization at zero, the commutator law, the
bimultiplicative 2-cocycle identity, diagonal normalization, and membership
of sampled Golay minimal-shell vectors.

## Boundary

This is the cocycle foundation, not yet the distinct-momentum Griess product.
The next step is to use the cocycle sign in the \((\alpha,\beta)=-2\)
exponential-product fixture, then verify invariance under antipodal
representative changes and the exact output momentum \(\alpha+\beta\).
It does not construct twisted-module operators, the full Griess algebra, or
Monster actions.
