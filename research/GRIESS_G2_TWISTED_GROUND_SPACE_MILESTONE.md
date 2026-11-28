# G2 milestone: twisted ground-space representation and untwisted action

**Status:** staged research/implementation contract. This document is not a construction, proof, or validation result.

## Why this is the next constructive gate

The repository already has an exact graded-character projection for the Leech \\(\\mathbb Z_2\\)-orbifold, a deterministic weight-two basis index certificate, and a substantial untwisted product kernel. The remaining weight-two split is

\\[
(V^\\natural)_2=U\\oplus T,\\qquad
\\dim U=98{,}580,\\quad \\dim T=98{,}304.
\\]

Here \\(T\\) is indexed formally by 24 half-integer oscillator directions over a 4,096-dimensional twisted ground space. The existing basis certificate explicitly says those ground labels do not yet carry a constructed representation. G2 must turn that formal factor into an exact module before any mixed Griess product is claimed.

This milestone is deliberately narrower than “construct the Griess algebra.” It addresses the finite twisted ground-space action and prepares the \\(U*T\\) block. It does not attempt \\(T*T\\), the full extension, or a Monster action.

## Mathematical object to construct

For the canonical lattice-negation twist, the twisted ground space is 4,096-dimensional. The implementation must recover the relevant finite central extension of the mod-two Leech lattice and its irreducible representation from a stated FLM convention.

The expected architecture is a finite Heisenberg/extraspecial 2-group representation associated with \\(\\Lambda/2\\Lambda\\), whose underlying vector space has dimension 24 over \\(\\mathbb F_2\\), with a nondegenerate alternating commutator form induced by the lattice pairing modulo 2. A symplectic basis identifies an irreducible representation space of dimension \\(2^{12}=4096\\).

This paragraph is a construction target, not permission to hard-code a guessed cocycle or sign convention. The exact central extension, quadratic refinement, lift, and central character must be derived from and cited to the primary FLM construction before the implementation freezes them. If the convention differs from the expected presentation above, the source-backed convention wins and this document must be amended.

## G2a — finite ground-space representation

Deliver a small, exact module that:

1. Constructs a canonical symplectic basis of \\(\\Lambda/2\\Lambda\\) from the repository's actual Leech basis/construction, with a deterministic ordering and digest.
2. Computes the induced bilinear form and quadratic refinement over \\(\\mathbb F_2\\), verifies nondegeneracy, and records the convention for every lift.
3. Constructs the 4,096-dimensional irreducible ground-space representation using sparse/permutation-with-sign operators where possible; avoid dense 4,096-by-4,096 matrices unless a test fixture requires them.
4. Implements the lattice-element operators for the chosen canonical lifts, including their exact phase/sign data.
5. Exposes a stable API from a Leech vector (or its mod-two class plus lift data) to a ground-space operator.

### G2a acceptance tests

- The 24-dimensional mod-two form is alternating and nondegenerate.
- The symplectic basis reconstructs the full form exactly and round-trips deterministically.
- Every generator satisfies the exact square/order relation derived from the cited quadratic refinement.
- Pairwise commutators match the lattice-pairing commutator law for all generator pairs and for a deterministic, seeded set of composite elements.
- The representation dimension is exactly 4,096; the generated operator algebra acts irreducibly (prove via a commutant/dimension argument or a complete exact computational certificate, not a handful of vectors).
- Changing the symplectic basis by a verified symplectic transformation yields an equivalent representation, with the intertwiner or an explicit equivalence certificate recorded.
- Deliberately corrupted cocycle signs, basis vectors, and lift data are rejected by negative controls.

## G2b — action of the untwisted weight-two sector on the twisted weight-two sector

Use the actual twisted-module vertex-operator formulas to implement

\\[
U*T\\longrightarrow T,
\\]

where \\(U=(V_\\Lambda^+)_2\\) has the existing 98,580-dimensional basis and \\(T=(V_\\Lambda^{T,+})_2\\) has the 98,304-dimensional basis.

The twisted basis state labels are \\(h_i(-1/2)t_a\\), with \\(0\\le i<24\\) and ground label \\(a\\) in the 4,096-dimensional representation. Implement the action in two separately testable families:

- The 300 untwisted quadratic-Heisenberg states acting through the half-integer Heisenberg commutators.
- The 98,280 even norm-four momentum-orbit states acting through the finite ground-space operators and the twisted vertex-operator expansion.

The output must be a canonical sparse linear combination of twisted basis states. Exact coefficients may be rational or algebraic as forced by the sourced normalization; do not round them to floating point.

### G2b acceptance tests

- Every product preserves conformal weight and lands in the declared twisted basis.
- The conformal identity \\(\\omega/2\\) acts as the identity on every tested twisted basis vector; include exhaustive coverage of all 98,304 basis vectors if the operator representation permits it.
- The 300 Heisenberg actions satisfy the exact commutator/contraction identities and are compatible with the half-integer mode convention.
- Momentum actions are independent of the chosen representative of \\(\\{\\alpha,-\\alpha\\}\\) after applying the canonical fixed-point projection.
- Product matrices/operators respect the fixed-point parity and the chosen twisted-ground-space phase convention.
- Basis permutation/serialization round trips preserve operator outputs and digests.
- Independent small fixtures, generated from the primary formula by a separate implementation path, agree exactly.
- Negative controls perturb a cocycle sign, a ground-space generator, and an oscillator normalization; each must trigger a specific failed assertion.

## Source and convention gate

Before G2 code is merged, add a source note with precise FLM page/equation/theorem references for:

- the finite central extension and its quotient/kernel;
- the twisted ground-space representation and central character;
- the lift of lattice negation and its action on the twisted ground space;
- the twisted Heisenberg mode algebra;
- the twisted vertex operator for lattice exponentials and its normalization.

Record the lattice inner-product scaling used by this repository alongside the source's convention. A formula copied from a secondary summary, existing code comment, or model-generated derivation is not sufficient source verification. Where FLM notation differs from repository notation, provide an explicit conversion table.

## Separation from later milestones

- **G3 remains separate:** implement \\(T*T\\to U\\) from the orbifold intertwining operator, with its own cocycle, phase, normalization, and invariance checks.
- **G4 remains separate:** combine all four product blocks and certify closure, commutativity, identity, and invariant-form invariance for the full 196,884-dimensional algebra. Do not demand associativity of the Griess product.
- **G5 remains separate:** construct explicit Monster generators/actions and verify their relations and preservation of the product/form. Published character-table comparisons are reference-data checks, not an implemented action.

## Repository entry points and dependencies

- `research/GRIESS_PRODUCT_CONSTRUCTION_SPEC.md` — global G0–G5 programme and product-block contract.
- `research/GRIESS_WEIGHT_TWO_BASIS_CERTIFICATE.md` and `experiments/moonshine_sierpinski/griess_weight_two_basis.py` — formal basis indexing; twisted ground labels are not yet represented.
- `research/GRIESS_UNTWISTED_HEISENBERG_BLOCK.md` and `experiments/moonshine_sierpinski/griess_untwisted_heisenberg.py` — existing untwisted product and invariant-form audits.
- `experiments/moonshine_sierpinski/leech_lattice_cocycle.py` — existing untwisted lattice cocycle; do not assume it automatically supplies the twisted-module lift.
- `research/LEECH_Z2_ORBIFOLD_CHARACTER_AUDIT.md` — character dimensions and parity projection only.

## Acceptance language

Before G2a passes: “twisted ground-space indexing/specification staged.”

After G2a passes: “the 4,096-dimensional twisted ground-space representation is implemented under the cited convention,” with the exact tests and scope reported.

After G2b passes: “the untwisted weight-two sector acts on the twisted weight-two sector under the implemented twisted-module formulas.”

Neither statement alone means the orbifold VOA extension or the full Griess product is constructed.
