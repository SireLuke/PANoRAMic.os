# Griess algebra construction: basis and validation specification

## Purpose and status

This document defines the next constructive milestone after the Leech \(\mathbb Z_2\)-orbifold graded-character audit. It is a research specification, not an implementation and not evidence that the Monster action has been constructed.

The target is the weight-two Griess algebra of the moonshine VOA \(V^\natural\). With the VOA mode convention
\[
a*b = a_1b,
\]
the product on weight two is commutative and nonassociative. Its identity is \(\omega/2\), where \(\omega\) is the conformal vector, because \(\omega_1=L(0)\). The invariant form is obtained from the weight-zero scalar \(a_3b\), with normalization fixed explicitly in the implementation.

A dimension match is not a product construction. No test in this milestone may report a Griess algebra or Monster action as complete until the structure constants are generated from vertex-operator/intertwining data.

## Exact weight-two basis split to preserve

The existing character audit gives
\[
(V^\natural)_2=(V_\Lambda^+)_2\oplus(V_\Lambda^{T,+})_2,
\qquad 196{,}884=98{,}580+98{,}304.
\]

The untwisted fixed part has a useful finer basis split:

- 98,280 momentum directions: the 196,560 norm-four Leech vectors paired under \(\alpha\leftrightarrow-\alpha\), giving one even combination per pair.
- 300 oscillator directions: \(\operatorname{Sym}^2(\mathfrak h(-1))\), since \(\dim\mathfrak h=24\) and \(\dim\operatorname{Sym}^2\mathfrak h=300\).
- The 24 one-oscillator states \(h(-2)\mathbf1\) are odd under the lift of lattice negation and are not in the fixed weight-two subspace.

Thus \(98{,}280+300=98{,}580\).

The twisted fixed part has 98,304 directions, represented at weight two by one half-integer oscillator acting on the 4,096-dimensional twisted ground space:
\[
24\times 4096=98{,}304.
\]
This is a dimension/basis-shape statement inherited from the twisted character construction. It does not yet supply the twisted intertwining operators or their phases.

## Product blocks required

Use the direct-sum decomposition \(U\oplus T\), where \(U=(V_\Lambda^+)_2\) and \(T=(V_\Lambda^{T,+})_2\). The product must expose and test all four blocks:

1. \(U*U\to U\): derive from the Leech lattice VOA vertex operators, including the lattice 2-cocycle and oscillator contractions.
2. \(U*T\to T\): derive the action of untwisted fixed fields on the twisted module, retaining the chosen twisted-ground-space representation and phase conventions.
3. \(T*U\to T\): verify equality with the first mixed block under the weight-two commutativity identity.
4. \(T*T\to U\): derive from the orbifold intertwining operator, including the normalization and cocycle/Clifford data on the 4,096-dimensional twisted ground space.

For norm-four lattice exponentials, the untwisted vertex-operator expansion must be used rather than a hand-entered adjacency rule. In particular, the singular terms depend on the lattice inner product and cocycle; the opposite-vector case \(\beta=-\alpha\) also has oscillator contributions. Any compressed representation must preserve these coefficients exactly.

## Representation strategy

A dense table for all ordered pairs would have \(196{,}884^2\) entries and is not the right first representation. Use a deterministic sparse or formula-backed structure-constant interface:

- stable basis IDs and a canonical ordering for all three basis families;
- exact rational/integer coefficients where the chosen normalization permits them, with algebraic-number support only where genuinely required;
- explicit cocycle and twisted-ground-space phase conventions;
- a product API that returns a canonical sparse linear combination;
- a serialization format with basis/version metadata and reproducible hashes;
- small exhaustive fixtures plus sampled and symmetry-orbit checks for the large families.

Do not replace a missing formula with a table of expected Monster character values.

## Required algebraic checks

The first complete product implementation must verify:

- closure and conformal-weight grading for every product block;
- commutativity on weight two: \(a*b=b*a\);
- the identity law \((\omega/2)*a=a\);
- symmetry and invariance of the bilinear form: \((a*b,c)=(a,b*c)\);
- consistency of the form with the VOA mode normalization;
- exact agreement of the untwisted block with independently computed small lattice-VOA fixtures;
- compatibility of mixed and twisted blocks with the fixed-point projection and the specified twisted-module action;
- deterministic results under basis reordering/serialization round trips.

Do not impose associativity or the Jordan identity as a blanket acceptance condition: the Griess product is nonassociative, and those are not generic defining identities for this algebra. Any additional identity must be justified by a precise theorem and tested separately.

## Staged implementation and gates

### G0 — conventions and basis certificate

Freeze the VOA mode convention, lattice inner-product scaling, cocycle convention, conformal vector normalization, basis IDs, and bilinear-form normalization. Independently reproduce the counts 98,280, 300, and 98,304 from the actual basis enumerators, not only from character coefficients.

### G1 — untwisted fixed product

Implement \(U*U\) from the lattice VOA formulas. Begin with exact hand-checkable fixtures: oscillator/oscillator, oscillator/momentum, momentum/momentum with nonzero singular terms, and opposite momentum pairs. Check cocycle identities and independence from representative choices.

This is a meaningful partial result, but it must be labelled the untwisted fixed subalgebra product, not the full Griess algebra.

### G2 — twisted module action

Implement \(U*T\) with an explicit model for the twisted ground space and half-integer oscillator action. Test the ground-space operators and phase relations independently before scaling to all 98,304 weight-two vectors.

### G3 — twisted-twisted intertwining block

Implement \(T*T\to U\) from the orbifold extension/intertwining data. This is the critical extension step. The 98,304-dimensional twisted sector cannot be treated as an arbitrary complement whose products are inferred from dimensions.

### G4 — full Griess algebra certificate

Combine the blocks, generate reproducible structure-constant fixtures, verify the identity and invariant form, and publish independent reproduction instructions. Only then mark the full weight-two Griess product constructed.

### G5 — Monster action (separate gate)

The algebra alone does not construct the Monster. The next stage must implement explicit automorphisms/generators on the VOA or Griess algebra, verify generator relations and preservation of product/form, and derive character traces from those actions. Comparing with published character-table entries remains a reference-data audit unless the matrices/actions are actually constructed.

## Repository evidence and boundary

The current repository sources deliberately distinguish the existing audits from the missing construction:

- `experiments/moonshine_sierpinski/leech_z2_orbifold_character.py` computes fixed-sector graded dimensions and explicitly reports that the VOA extension and Monster action are not constructed.
- `experiments/moonshine_sierpinski/leech_voa_weight_two.py` verifies the precursor count \(196{,}560+324=196{,}884\), not a product.
- `experiments/moonshine_sierpinski/leech_monster_representation_bridge.py` checks published representation dimensions and 2B character values; it explicitly does not construct Monster representations or actions.
- `research/LEECH_Z2_ORBIFOLD_CHARACTER_AUDIT.md` records the sector dimensions and their evidence boundary.
- `research/LEECH_TO_MONSTER_BRIDGE.md` records the reference-data bridge and its limitations.

## Acceptance language

Allowed before G4: “weight-two basis/count audited,” “untwisted fixed product implemented,” or “twisted action block implemented,” each with the exact tested scope.

Allowed only after G4: “the weight-two Griess product is implemented and its stated algebraic checks pass.”

Allowed only after G5: “the specified Monster generators act on the constructed algebra/VOA and satisfy the tested relations.” A finite set of generator checks is not by itself a proof of the full Monster presentation or monstrous moonshine.

## References to establish before implementation

The implementation PR must cite the precise source formulas and conventions from the Frenkel–Lepowsky–Meurman construction of the moonshine module and lattice/twisted-module VOA theory. It must record page/theorem/equation references for the lattice cocycle, twisted ground-space operators, intertwining operators, and normalization. The code must not silently treat a secondary summary or a model-generated formula as an authority.
