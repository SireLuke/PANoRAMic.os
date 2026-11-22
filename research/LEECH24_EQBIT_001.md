# LEECH24-EQBIT-001 — Leech kissing-shell graph and GF(2) cut-rank pilot

**Status:** preregistration / design only. No Leech-EQBIT run result is claimed.
**Parent artifacts:** `experiments/moonshine_sierpinski/leech_golay_construction.py`, `experiments/moonshine_sierpinski/leech_unimodular_basis.py`, and `experiments/flip_qubit/cut_rank_audit.py`.
**Evidence grade intended:** exact finite construction + exact graph incidence + sampled GF(2) cut-rank statistics.
**Not claimed:** physical quantum dynamics, hardware entanglement, quantum advantage, a Leech-to-E8 embedding, or a new physical theory.

## 1. Research question

Can the existing exact Golay-defined Leech minimal shell support a reproducible graph-state / GF(2) cut-rank audit analogous in method (not in geometry or dimension) to the existing E8/Gosset flip-eqbit experiment?

The key missing object is a declared graph on the 24D Leech shell. This experiment defines one from the lattice's contact/kissing relation and keeps the 24D lattice, its 196,560-point shell, and the 8D E8/Gosset graph as distinct typed objects.

## 2. Exact source geometry

Use the existing integral representatives (x\in\mathbb Z^{24}), with lattice vector (v=x/\sqrt 8). The current Golay implementation supplies three disjoint minimal-vector families:

- 1,104 vectors of shape ((\pm4,\pm4,0^{22}));
- 97,152 vectors supported on Golay octads, with eight entries (\pm2) and an even number of minus signs;
- 98,304 vectors of shape ((\pm3,\pm1^{23})), with signs derived from extended Golay words.

Every minimal vector has lattice norm squared 4. The union has 196,560 distinct vectors. Do not replace or regenerate the established lattice basis certificate as part of this experiment.

For integral representatives (x,y), compute the exact lattice inner product as
\[
\langle v,w\rangle = \frac{x\cdot y}{8}.
\]
All adjacency decisions must use integer arithmetic: compare (x\cdot y) with 16, never floating-point tolerances.

## 3. Canonical graph definition

Define the Leech kissing graph (G_\Lambda=(V,E)):

- (V=\Lambda_{24}(4)), the 196,560 minimal vectors;
- for distinct (v,w\in V), add an undirected edge iff (\langle v,w\rangle=2);
- equivalently, (v-w) is another minimal vector, since (\|v-w\|^2=8-2\langle v,w\rangle=4).

The expected degree is 4,600 and the expected undirected edge count is
\[
\frac{196560\cdot4600}{2}=452088000.
\]

The antipodal map (a(v)=-v) is a fixed-point-free involution and graph automorphism: it preserves every pairwise inner product when applied to both endpoints. It partitions the shell into 98,280 antipodal pairs.

The graph is implicit for the pilot. Do not materialize a 196,560-by-196,560 dense adjacency matrix or a full edge list merely to run the sampled cut-rank tests. Exact inner-product queries generate only the induced subgraphs required by the protocol.

## 4. Reference shell census — mandatory exact gate

For each selected reference minimal vector (u), count all (v\in V) by exact inner product. The expected shell census is:

| \(\langle u,v\rangle\) | Expected count |
|---:|---:|
| 4 | 1 |
| 2 | 4,600 |
| 1 | 47,104 |
| 0 | 93,150 |
| -1 | 47,104 |
| -2 | 4,600 |
| -4 | 1 |
| **Total** | **196,560** |

At minimum, run the census for one deterministic reference vector from each of the three construction families. Record the exact representative coordinates and a canonical SHA-256 digest of each sorted shell histogram. The degree-4,600 gate is the count at inner product 2.

This is a reference-vector census, not a brute-force proof of every vertex's degree. The known Co\(_0\) transitivity of the minimal shell supplies the mathematical reason the valency is uniform; software must state this dependency rather than imply that three representatives prove global transitivity.

## 5. EQBIT pilot protocol

### 5.1 Sampled induced graph

For each of 10 preregistered seeds:

1. Select 120 distinct antipodal pairs uniformly without replacement from the 98,280 pairs.
2. Include both endpoints of every selected pair, yielding 240 vertices.
3. Build the 240-vertex induced subgraph using exact inner products.
4. Freeze the vertex ordering, pair map, adjacency digest, seed, and graph summary before computing any cut-rank results.

This is a sampled induced subgraph of the full Leech kissing graph. It is not the full 196,560-vertex graph and results must be labelled accordingly.

### 5.2 Cut families

For each frozen 240-vertex induced graph, compute GF(2) cut rank for:

- **Antipodal split:** one endpoint of each selected pair on the left and its antipode on the right (120|120). Use a deterministic orientation rule based on the stored integral coordinates.
- **Random transversals:** 100 independent seeded choices of one endpoint from each selected pair (120|120).
- **Balanced controls:** 100 independent uniformly sampled 120|120 partitions of the same 240 vertices, without requiring antipodal consistency.
- **Relabeling control:** apply a seeded vertex permutation to the graph and the cut; the rank must remain unchanged.

This yields 10 independent induced-graph samples and, within each, 100 random cuts per stochastic family. Preserve per-seed and pooled summaries; do not pool away between-subgraph variation.

### 5.3 Exactness and controls

- Use the existing GF(2) cut-rank implementation only after checking its input contract and adding a small independent fixture for this graph representation.
- Store raw ranks, not only means or quantiles.
- Report sample counts, seeds, min/median/mean/max, and tail counts with an interval method declared before the run.
- Do not describe the arbitrary balanced partition as a matched structural null for the antipodal split; it is a different control family.
- Do not treat the 10 induced graphs as 10,000 independent graph samples. Cuts are nested within each induced graph.
- No post-hoc changes to adjacency relation, sampling, or cut families. Exploratory variants receive a new experiment ID.

## 6. Acceptance gates

1. Existing Golay code audit passes: 4,096 words, [24,12,8] parameters, expected Type-II weight distribution.
2. Existing Leech basis audit passes: rank 24, determinant/index agreement (2^{36}), scaled Gram determinant 1, even and positive definite, minimum norm 4.
3. Minimal shell has exactly 196,560 unique vectors, all integral norm 32 before scaling.
4. Three reference shell censuses match the full expected inner-product distribution above.
5. Antipodal map is fixed-point-free, involutive, and preserves adjacency on every generated induced graph.
6. Each induced graph is simple and undirected; adjacency digests are stable under rerun with the same seed.
7. GF(2) cut rank is invariant under vertex relabeling.
8. Raw cut-rank samples and provenance are emitted with all seeds and source hashes.
9. The full run is independently rerun from the frozen commit before any cross-seat comparison.

Any failed gate is reported as a failure; no partial pass is promoted to an overall pass.

## 7. Explicit boundaries

- This graph is built from the 24D Leech minimal shell, not the 8D E8 roots or 240-vertex Gosset graph.
- The number 240 is the size of the sampled induced graph, not a claim that Leech shell geometry is an E8 copy.
- The Leech basis/minimum-shell certificate and the graph-state cut-rank audit are separate mathematical checks.
- GF(2) cut rank is a graph invariant used in a graph-state formalism. It is not evidence of physical quantum entanglement, hardware performance, quantum advantage, or quantum dynamics.
- No Navier–Stokes, ABOM/V8, or physical coupling is introduced by this experiment.
- This pilot does not construct Co\(_0\), Co\(_1\), the Leech VOA, the Monster, or a Moonshine representation.

## 8. Reproduction target and implementation sequence

Implementation should be split into auditable steps:

1. Add a pure helper that returns the three reference-vector shell histograms using exact integer dot products.
2. Add a deterministic antipodal-pair index and sampled induced-graph builder.
3. Add tests for family counts, shell census, graph symmetry, antipodal automorphism, digest reproducibility, and relabeling invariance.
4. Add the seeded cut-rank runner and raw JSON artifact.
5. Measure runtime and memory before increasing the sample schedule.
6. Obtain an independent bench reproduction before comparison with E8/Gosset EQBIT results.

No result JSON is to be committed with the preregistration.

## 9. References

- Conway, Curtis, Norton, Parker, Wilson, *Atlas of Finite Groups* (1985), p. 181; Conway and Sloane, *Sphere Packings, Lattices and Groups*, 3rd ed. (1999), Ch. 4, for the Leech minimal shell and kissing graph.
- MathOverflow, “Edges of the contact polytope of the Leech lattice,” for the explicit inner-product distribution around a fixed minimal vector: https://mathoverflow.net/questions/335645/edges-of-the-contact-polytope-of-the-leech-lattice
- Michio Ozeki, “Siegel theta series of various degrees for the Leech lattice,” *Kyushu Journal of Mathematics* 68 (2014), 53–91, for common-neighbor incidence counts arising from mutually touching minimal vectors: https://doi.org/10.2206/kyushujm.68.53
- Existing PAN certificate: `research/LEECH_UNIMODULAR_BASIS_CERTIFICATE.md`.

Authored-by: OpenAI (ChatGPT bench)
