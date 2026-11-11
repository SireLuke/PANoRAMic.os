# Leech-to-Monster representation bridge

## Goal

Connect the exact Leech Z2-orbifold graded-dimension audit to the first
published Monster representation decompositions. This is a reproducible
integer-arithmetic bridge between the lattice/VOA calculation and known
finite-group representation data.

## 1. Identity class: graded dimensions

The Leech orbifold code computes the graded dimensions of the candidate
Moonshine module from its untwisted fixed and twisted fixed sectors. With
q = exp(2 pi i tau), the coefficient of q^n in J(q)=j(q)-744 corresponds
to conformal weight n+1.

The first four comparisons are:

| q power | Orbifold weight | Dimension / J coefficient | Monster irreducible decomposition |
|---:|---:|---:|---|
| 1 | 2 | 196,884 | 1 + 196,883 |
| 2 | 3 | 21,493,760 | 1 + 196,883 + 21,296,876 |
| 3 | 4 | 864,299,970 | 2(1) + 2(196,883) + 21,296,876 + 842,609,326 |
| 4 | 5 | 20,245,856,256 | 2(1) + 3(196,883) + 2(21,296,876) + 842,609,326 + 19,360,062,527 |

Each side is computed independently in the test: the orbifold side comes
from exact q-series projections; the representation side is an integer
linear combination of published irreducible dimensions.

## 2. A non-identity check: Monster class 2B

The bridge also checks the first three 2B McKay-Thompson coefficients using
the published character values of the first four irreducible Monster
representations on class 2B:

(1, 275, -2324, 12974).

The coefficient sums are:

- q^1: 1 + 275 = 276
- q^2: 1 + 275 - 2324 = -2048
- q^3: 2(1) + 2(275) - 2324 + 12974 = 11202

This extends the comparison beyond dimensions at the identity element.
It remains a check against reference character values, not a computation of
Monster matrices or traces from an implemented group action.

## 3. Interpretation boundary

What this experiment verifies:

- The Leech Z2-orbifold graded dimensions match the first four normalized
  j-function coefficients.
- Those coefficients match the documented sums of the first Monster
  irreducible dimensions.
- The first three 2B McKay-Thompson coefficients match the documented
  2B character-value combinations.

What it does not verify:

- Construction of the Monster group or its irreducible representations.
- Construction of a Monster action on the Leech orbifold VOA.
- Construction of vertex operators, intertwining operators, or VOA
  associativity/locality.
- Derivation of McKay-Thompson series from a group action.
- The full genus-zero property or Borcherds' monstrous moonshine theorem.

## 4. References

- John F. R. Duncan, Michael J. Griffin, Ken Ono, *Moonshine*:
  https://uva.theopenscholar.com/files/ken-ono/files/151.pdf
  Includes the first Monster irreducible dimensions and the first identity
  class decompositions, including the q^4 coefficient.
- *Moonshine and the BSD conjecture* lecture notes:
  https://www.math.columbia.edu/~chaoli/doc/Moonshine.html
  Includes the first four Monster irreducible character values on class 2B
  and the first 2B McKay-Thompson coefficient decompositions.
- Encyclopedia of Mathematics, *Moonshine conjectures*:
  https://encyclopediaofmath.org/wiki/Moonshine_conjectures
  Background on the graded Monster module and McKay-Thompson series.

The repository fixtures are transcribed reference data. The test verifies
their arithmetic and consistency with the Leech orbifold q-series; it does
not independently derive the character table entries.

## Reproduction

`python -m unittest tests.test_leech_monster_representation_bridge -v`
`python experiments/moonshine_sierpinski/leech_monster_representation_bridge.py`
