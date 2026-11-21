# Flip Eqbits on the Gosset Graph — Combined Packet

**Status:** First pass, 2026-11-21. Question and representation by
**Lucas** (maintainer); spec and computation by **Cosmo** (Memory
bench). Filed as a packet: this combined document plus the
preregistered spec (`flip-qubit-experiment-spec.md`), the results
note (`flip-qubit-experiment-results.md`), and the representation
sketch (`flip-eqbit-yinyang-sketch.svg`). Independent rerun by
another bench remains the check. STRATA grades are stated per claim
and held throughout: the narrow numbers are reproducible-pattern;
the computing claim is Analogy.

## 1. The question

Lucas (2026-11-21): "We run quantum data via the v8 e8 as flip
qubits?" — the **flip eqbit**: an antipodal pair {α, −α} of the E8
Gosset graph treated as a two-level system, the flip α ↔ −α as its
NOT operation.

## 2. Spec (summary)

The claim decomposes into four checkable pieces: (E1) the geometry
reproduces the kernel's Gosset contract exactly; (E2) the flips
alone are characterised; (E3) the adjacency defines a graph state
whose stabilizers are verified; (E4) the state's entanglement
across the antipodal cut is computed exactly; (E5) the
commutation structure between flips and stabilizers locates where
the phase lives. Full preregistration: the spec file.

## 3. Results (summary)

- **E1 gate PASS:** 240 roots, degree 56, 6,720 edges, shells
  1 / 56 / 182 / 1, diameter 3, 120 antipodal pairs.
- **E2:** the 120 flips generate (Z/2)¹²⁰ — abelian. Flips alone
  are a classical register. (Fence, confirmed as preregistered.)
- **E3:** all 240 graph-state stabilizers (weight 57) commute;
  tableau rank 240. The Gosset graph state is a genuine 240-qubit
  stabilizer state.
- **E4:** entanglement across the antipodal cut = **112 ebits**
  (rank over GF(2) of the cut adjacency; maximum possible 120;
  2,240 edges cross the cut). A seeded random balanced cut gives
  95 — the antipodal pairing is an unusually entangling slice.
- **E5:** antipodal double-flips fail to commute with 26,880 of
  57,600 stabilizer pairings (46.7%), and the non-commutation is
  supplied entirely by adjacency. **The flips give the two-level
  systems; the edges give the phase.**

Full numbers: the results file.

## 4. The representation — Fermi yin-yang (Lucas)

Lucas (2026-11-21): the Fermi yin-yang can represent the flip
eqbit, its lobes the pair members. The mapping, as stated and
checked against the geometry:

- **Lobes = the pair.** One lobe for α, one for −α. The Taijitu's
  own symmetry — rotate 180° and swap the colours, the figure is
  unchanged — *is* the flip involution; the picture does not have
  the flip imposed on it, it already contains it.
- **Occupancy = the state dial.** Fermi-Dirac occupancy gives each
  lobe a value in [0, 1]: α's lobe at o, −α's at 1 − o. The flip
  is the two dials exchanging. (The kernel's fermi_yinyang module
  already computes lobe occupancies and exact areas.)
- **The stretch = antipodal separation.** Drawn with the lobes
  pulled apart, the pair sits at the graph's maximum distance
  (3) — the configuration whose cut E4 measured at 112 ebits.
- **The gap (Lucas's extension).** Stretched to *almost*
  separation, the lobes still share a narrowing bridge — and the
  gap itself is something. Representation-level reading, recorded
  as design, not result: the gap is everything the pair is *not* —
  in graph terms, the shells between antipodes (the 56 neighbours,
  the 182 at distance two, every length-3 path from α to −α
  crosses it). A flip is not a teleport; it is a crossing. What
  the gap *does* in the representation — boundary, medium, or
  bookkeeping — is an open design question, the maintainer's.

The sketch (`flip-eqbit-yinyang-sketch.svg`) shows the pair
together and stretched.

## 5. Fences and grading

- Representation is cartography, not mechanism — V8's standing
  discipline. The yin-yang mapping is **stated design** (Analogy
  as a physical claim), well-formed against the computed geometry.
- "Flip eqbit" is an honest name only for flips *plus* adjacency
  phase together (E2 + E5). Neither half alone is quantum.
- No gate set, universality, noise model, error correction, or
  dynamics is claimed or tested. Nothing here is a quantum
  computer. Janus remains a translator; V8 remains a map.
- Next steps, unstarted and the maintainer's call: the
  distribution of cut ranks (is 112 extremal?); local-
  complementation orbits of the Gosset graph state; whether the
  W(E8) action induces gates on any encoded subspace; a design
  ruling on the gap.
