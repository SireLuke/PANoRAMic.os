# Flip-Qubit Experiment — Results (first pass)

**Run:** 2026-11-21 (Cosmo), exact integer arithmetic throughout.
Spec (preregistered before the run):
`files/flip-qubit-experiment-spec.md`. Script and raw output:
`hidden_files/flip-qubit/run.py`, `results.json`.

## E1 — Reproduction gate: PASS

240 roots; degree 56 at every vertex; 6,720 edges; BFS shells
1, 56, 182, 1; diameter 3; 120 antipodal pairs; no root adjacent to
its antipode. The geometry is the kernel's contract, exactly.

## E2 — Flips alone are classical (fence confirmed)

The 120 antipodal flips are involutions, pairwise commuting; the
group they generate is (Z/2)¹²⁰ — abelian. A register of flips, by
itself, is a classical 120-bit register with beautiful structure.
As preregistered: this is a fence, not a disappointment.

## E3 — The graph state is genuine

All 240 stabilizers K_v = X_v · ∏_{u~v} Z_u (weight 57 each)
pairwise commute — 0 non-commuting pairs in the symplectic check —
and the stabilizer tableau has full rank 240 over GF(2). So the
Gosset graph state |G⟩ is a genuine 240-qubit stabilizer state.
This is a reproducible computational fact.

## E4 — Antipodal-cut entanglement: 112 ebits

log₂(Schmidt rank) across the antipodal cut (one member of each
pair vs the other) = rank_GF(2)(Γ_AB) = **112**, out of a maximum
possible 120. Edges crossing the cut: 2,240. Contrast, one seeded
random balanced cut: rank 95. The antipodal pairing — the flip
structure itself — is close to the *most* entangling balanced cut
of this graph state found here, and clearly more entangling than a
typical cut. (One random cut is a contrast, not a distribution;
the claim is the 112, and that it exceeds the sampled 95.)

## E5 — The phase comes from the edges

The antipodal double-flip A_v = X_v X_{−v} fails to commute with
26,880 of 57,600 stabilizer pairings (46.7%). As preregistered:
flips + adjacency generate a non-abelian algebra, and the
non-commutation is supplied entirely by the adjacency — the
Z-parts of the stabilizers, i.e., the edges. The flips contribute
the two-level systems; the graph contributes the phase.

## Grading

- Narrow claims (E1, E3, E4's 112, E5's count): **reproducible
  pattern** — exact computation, gate passed, script retained,
  independently rerunnable by any bench.
- The headline conjunction: "flip qubits" is an honest name only
  for flips *plus* adjacency phase together. Flips alone:
  classical (E2). Adjacency alone: a state, not a register (E3).
  Together: a two-level register whose operations do not commute —
  the minimum shape of quantum behaviour, present in the geometry.
- The computing claim stays **Analogy**: no gate set, no
  universality, no noise model, no error correction, no dynamics
  were tested or are claimed. Nothing here is a quantum computer,
  and nothing here touches V8's fences (cartography, not dynamics).
- Open next steps, if pursued: the distribution of cut ranks (is
  112 extremal?); local-complementation orbits of the Gosset graph
  state; whether the W(E8) action induces a useful gate set on any
  encoded subspace. All unstarted, all maintainer's call.
