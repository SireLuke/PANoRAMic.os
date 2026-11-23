# Untwisted Heisenberg product kernel — G1a

## Implemented scope

This increment implements two exact product blocks in the untwisted fixed
weight-two sector:

1. The 300-dimensional oscillator subalgebra
   \(\operatorname{Sym}^2(\mathfrak h(-1))\times
   \operatorname{Sym}^2(\mathfrak h(-1))\to
   \operatorname{Sym}^2(\mathfrak h(-1))\).
2. The action of oscillator quadratic states on the 98,280 even momentum
   directions.

It is intentionally called G1a. It is not the full untwisted product
\(U*U\), because momentum × momentum is not implemented.

## Formulae and normalization

Let \(h_0,\ldots,h_{23}\) be an orthonormal basis of the real Heisenberg
space, and write \(A_{ij}=h_i(-1)h_j(-1)\mathbf1\), with \(i\le j\).
The standard Heisenberg field identity is
\[
Y(A_{ij},z)=:h_i(z)h_j(z):.
\]
Taking the coefficient of \(z^{-2}\) on a quadratic oscillator state gives
\[
A_{ij}{}_1 A_{kl}=
\delta_{jk}A_{il}+\delta_{jl}A_{ik}
+\delta_{ik}A_{jl}+\delta_{il}A_{jk},
\]
with repeated basis terms combined. The unnormalised monomial convention is
important: \(A_{ii}{}_1 A_{ii}=4A_{ii}\).

For a norm-four lattice vector \(\alpha=x/\sqrt8\), the positive Heisenberg
modes annihilate the momentum ground state \(e^{\pm\alpha}\), and the
zero modes act by \(\pm(h_i,\alpha)\). Thus
\[
A_{ij}{}_1(e^\alpha+e^{-\alpha})
=(h_i,\alpha)(h_j,\alpha)(e^\alpha+e^{-\alpha})
=\frac{x_i x_j}{8}(e^\alpha+e^{-\alpha}).
\]
The sign is unchanged under \(\alpha\mapsto-\alpha\). The code uses exact
rational coefficients and validates the integral Leech-coordinate
congruences and norm 32 before accepting a momentum label.

The conformal vector is
\(\omega=\tfrac12\sum_i A_{ii}\), so the identity element for the
weight-two product is \(\omega/2=\tfrac14\sum_i A_{ii}\). The tests
verify this identity on all 300 oscillator basis states and representative
norm-four momentum states.

## Reproduction

```sh
python -m unittest tests.test_griess_untwisted_heisenberg -v
python -m experiments.moonshine_sierpinski.griess_untwisted_heisenberg
```

The opposite-pair self-product fixture is included in the same test module.

## Validation boundary

The test suite checks exact contraction fixtures, commutativity of the
oscillator block, symmetry of its Fock-space bilinear form, antipodal
invariance of the oscillator/momentum block, input lattice membership, and
the conformal identity on the implemented blocks.

A narrow momentum × momentum case is now implemented: the self-product of
one antipodal momentum orbit with itself. For the standard normalized
lattice cocycle and norm-four alpha, the opposite-charge terms combine to
the oscillator state alpha(-1)^2; the alpha(-2) contributions cancel. The
implementation stores this in the unnormalised A_ij basis with exact
rational coefficients and checks antipodal invariance.

Not implemented: products of distinct momentum orbits (the inner-product
-2 case), a general lattice 2-cocycle interface, the complete untwisted
fixed-sector product, twisted-module action, twisted-twisted intertwining
product, full Griess algebra, or Monster action. The opposite-pair formula
must be cross-checked against the primary FLM convention before it is
treated as a fully sourced general-purpose cocycle implementation.

The formulae here are the elementary Heisenberg/lattice-VOA consequences
used by the code. The full construction PR must still attach precise
primary-source FLM equation/page references for the cocycle and exponential
vertex-operator product before those blocks are accepted. No external
bibliographic page citation is claimed by this increment.
