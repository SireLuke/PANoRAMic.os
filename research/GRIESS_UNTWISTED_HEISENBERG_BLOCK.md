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

The oscillator and oscillator/momentum formulas originated in G1a. The
momentum × momentum dispatcher was added in the subsequent G1b work; this
file records the combined partial untwisted weight-two kernel, not the full
Moonshine Griess algebra.

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

The same test module also covers the opposite-pair self-product, distinct
momentum-pair product, dispatch across all inner-product classes, and the
full minimal-shell inner-product distribution.

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

A basis-relative lattice cocycle and one distinct-momentum orbit with
absolute inner product 2 are now implemented in the companion G1b increment.
The momentum × momentum dispatcher now covers every possible inner-product
class for two norm-four Leech vectors: equal/opposite vectors produce the
oscillator self-product; absolute inner product 2 produces the corresponding
even momentum state; absolute inner product 0 or 1 produces zero. The
remaining inner products +/-3 are excluded by the absence of norm-two
vectors in the Leech lattice. A full 196,560-vector shell census test checks
the distribution {-4:1, -2:4600, -1:47104, 0:93150, 1:47104, 2:4600, 4:1}.

This completes the weight-two momentum × momentum dispatch at the level of
the implemented cocycle convention, but does not complete the entire
untwisted VOA product across all sectors or the full Griess algebra. The
twisted-module action, twisted-twisted intertwining product, and Monster
action remain open. Precise primary FLM page/equation references for the
chosen cocycle and exponential vertex-operator convention remain a required
source-verification step.

The formulae here are the elementary Heisenberg/lattice-VOA consequences
used by the code. The full construction PR must still attach precise
primary-source FLM equation/page references for the cocycle and exponential
vertex-operator product before those blocks are accepted. No external
bibliographic page citation is claimed by this increment.


## Invariant bilinear form — G1d

The untwisted weight-two basis now has an explicit exact bilinear form.
On the 300 oscillator states it is the Heisenberg Fock pairing
\[
\langle A_{ij},A_{kl}\rangle
=\delta_{ik}\delta_{jl}+\delta_{il}\delta_{jk}.
\]
The oscillator and momentum sectors are orthogonal. For the even momentum
orbit states \(E_{[\\alpha]}=e^\\alpha+e^{-\\alpha}\), the pairing is
2 when the antipodal orbits agree and 0 otherwise.

A sparse-vector pairing and a unified dispatcher over the currently
implemented untwisted products allow the invariance residual
\[
\langle a_1 b,c\rangle-\langle b,a_1 c\rangle
\]
to be evaluated exactly. Deterministic tests cover 216 triples drawn from
oscillator states and three momentum orbits (including an inner-product-2
sum orbit). All 216 residuals are required to vanish, and symmetry and
sector orthogonality are checked separately.

This is a finite fixture audit of the implemented formulas, not an
exhaustive proof of invariance over all 196,884 dimensions and not a
construction of the twisted-sector extension.


## Basis-wide invariant-form Gram certificate — G1e

The next audit verifies the Gram matrix on the entire implemented untwisted
basis without allocating a dense matrix. It checks all 90,000 ordered pairs
in the 300-state oscillator block, enumerates the 196,560 minimal Leech
vectors, confirms that they form 98,280 antipodal momentum orbits, and
checks the norm of every momentum-orbit basis vector.

The resulting 98,580-dimensional Gram matrix is diagonal in the chosen
basis: 276 off-diagonal oscillator states have norm 1, while 24 diagonal
oscillator states and all 98,280 momentum-orbit states have norm 2. Thus
the exact diagonal multiplicities are 276 of norm 1 and 98,304 of norm 2;
the Gram matrix has rank 98,580, signature (98,580, 0, 0), determinant
\(2^{98304}\), and is positive definite.

This is a basis-wide certificate for the implemented untwisted subspace.
It is not a proof that the product-invariance identity holds for every
triple, and it does not construct the missing twisted-sector extension or
the full 196,884-dimensional Griess algebra.


## Exhaustive oscillator product-invariance audit — G1f

The next audit exhausts the invariant-form identity on the complete
300-dimensional oscillator block. For three quadratic basis states, the
trilinear pairing can be nonzero only when every coordinate index among
the six indices occurs with even multiplicity. This follows directly
from the four-term Heisenberg contraction formula and the oscillator
Fock pairing.

After identifying permutations that yield the same ordered triple of
symmetric oscillator basis states, there are exactly 45,840 distinct
potentially nonzero ordered triples from the even-multiplicity
six-index multisets. The audit enumerates those support candidates,
evaluates both sides of
\[
\langle a_1 b,c\rangle=\langle b,a_1 c\rangle,
\]
and requires exact rational equality in every case. All remaining
oscillator triples have zero pairing on both sides by the same support
criterion.

This closes the product-invariance check for the oscillator block only.
It does not establish the corresponding identity for all momentum triples,
the twisted sector, or the full Griess algebra.


## Fixed momentum-star invariant-form audit — G1g

The next momentum-sector audit fixes the minimal Leech vector
\(\alpha=(4,4,0,\ldots,0)\) and scans the complete 196,560-vector
minimal shell. Exactly 4,600 vectors \(\beta\) have
\((\alpha,\beta)=-2\). For each, the sum
\(\gamma=\alpha+\beta\) is checked to remain in the norm-four Leech
shell, the implemented momentum product is checked to land on the
antipodal orbit \([\gamma]\), and the invariant-form identity is
evaluated exactly with probe \(c=\gamma\). The reverse product
\(\alpha*\gamma\) must return the orbit \([\beta]\), with matching
pairing coefficient.

The audit requires 4,600 distinct beta orbits, 4,600 distinct output
orbits, and 4,600 exact zero residuals. This is an exhaustive local
momentum-star certificate around one fixed Leech orbit. It is not a
global all-triples proof for the 98,280-dimensional momentum sector and
does not cover mixed or twisted-sector triples.


## Mixed oscillator–momentum invariant-form star — G1h

The mixed-sector audit fixes \(\alpha=(4,4,0,\ldots,0)\) and checks
both mixed product orderings against all 300 oscillator basis states.

First, for every one of the 196,560 minimal-shell vectors \(\beta\), it
checks
\[
\langle A_{ij}{}_1 E_{[\alpha]},E_{[\beta]}\rangle
=
\langle E_{[\alpha]},A_{ij}{}_1 E_{[\beta]}\rangle.
\]
This performs 58,968,000 exact residual checks and scans the full shell;
the pairing support forces both sides to vanish unless the momentum
orbits agree.

Second, it checks
\[
\langle E_{[\alpha]}{}_1 E_{[\beta]},A_{ij}\rangle
=
\langle E_{[\beta]},E_{[\alpha]}{}_1 A_{ij}\rangle
\]
for all oscillator basis states and the 4,601 supported momentum orbits:
the opposite orbit and the 4,600 inner-product-minus-two neighbors. This
adds 1,380,300 exact residual checks.

The audit therefore requires 60,348,300 exact zero residuals. It is an
exhaustive mixed-sector star around one fixed Leech momentum orbit, not a
global all-triples certificate for the complete untwisted space. The
twisted-sector extension and full Griess algebra remain outside scope.
