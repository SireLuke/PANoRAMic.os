# Flip-Qubit Experiment — Spec (preregistered)

**Status:** Spec written before the run, 2026-11-21 (Cosmo), at Lucas's
direction. Question, from Lucas (2026-11-21): "We run quantum data via
the v8 e8 as flip qubits?" STRATA position of the *computing* claim:
**Analogy**. This experiment tests only the narrow computational
sub-claims below; no outcome of it promotes the computing claim.

## Decomposition

"Flip qubits on the Gosset graph" splits into four checkable pieces:

1. The antipodal structure gives natural two-level systems (flips).
2. The adjacency structure defines a graph state (a genuine entangled
   stabilizer state) — *if* its stabilizers check out.
3. That state is entangled across the antipodal cut — *by a computable
   amount*.
4. The phase-like behaviour (non-commutation) enters through
   adjacency, not through the flips — *testable* via symplectic
   commutation.

## Definitions (exact)

- E8 roots: the 240 vectors of norm² 2 — 112 integer type
  (permutations of (±1, ±1, 0⁶)) and 128 half-integer type
  ((±½)⁸ with an even number of minus signs). Computed in scaled
  integer coordinates (×2) so all arithmetic is exact.
- Gosset graph: vertices = roots; α ~ β iff ⟨α, β⟩ = 1.
- Antipodal pair: {α, −α}. Flip: the involution swapping a pair.
- Graph state |G⟩: one qubit per root, CZ on every edge, from
  |+⟩^⊗240. Stabilizers K_v = X_v · ∏_{u~v} Z_u.
- Antipodal cut: A holds one member of each pair (120 qubits),
  B the other 120. For a graph state, log₂(Schmidt rank across the
  cut) = rank over GF(2) of the A×B adjacency submatrix.

## Steps and declared expectations

- **E1 — Reproduction gate.** 240 roots; every degree 56; 6,720
  edges; BFS shells from any root = 1, 56, 182, 1; diameter 3;
  120 antipodal pairs. *Gate: any mismatch stops the experiment —
  the geometry would not be the kernel's contract.*
- **E2 — Flip register.** The 120 flips are involutions and pairwise
  commute; the group they generate is (Z/2)¹²⁰. *Declared
  expectation: confirmed — flips alone are a classical register.
  This is a fence, not a disappointment.*
- **E3 — Graph-state stabilizers.** All 240 K_v pairwise commute
  (symplectic check over GF(2)) and are independent (tableau rank
  240). *If both hold, |G⟩ is a genuine 240-qubit stabilizer state —
  a reproducible computational fact, not a computing claim.*
- **E4 — Antipodal-cut entanglement.** Compute r = rank_GF(2)(Γ_AB).
  r is the exact entanglement (in ebits) of |G⟩ across the antipodal
  cut. Contrast: one seeded random balanced cut, same computation.
  *Declared expectation: r > 0; the value is the result, whatever
  it is.*
- **E5 — Where the phase lives.** For the antipodal double-flip
  A_v = X_v X_{−v} and each stabilizer K_u, compute the symplectic
  commutation. *Declared expectation: some (v, u) pairs do not
  commute — i.e., flips + adjacency generate a non-abelian algebra,
  and the non-commutation is supplied by the edges (the Z-parts of
  the stabilizers), not by the flips.*

## Fences (hold regardless of outcome)

- No gate set, no universality claim, no noise model, no error
  correction, no dynamics. Nothing here is a quantum computer.
- "Flip qubit" remains a *name* for the antipodal two-level systems.
  Qubit behaviour requires the adjacency phase structure of E3–E5
  *in addition* — that conjunction is the finding, whichever way
  E5 lands.
- V8 stays a cartography engine; Janus stays a translator, not a
  dynamics engine. This experiment touches the Gosset graph only.

## Run record

Script and raw results: `hidden_files/flip-qubit/` (review-goal
workspace). Results note: `files/flip-qubit-experiment-results.md`.
