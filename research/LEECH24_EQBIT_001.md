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


## 10. Valdora phase-two evidence and Leech-specific design refinement

This section incorporates the completed artifact
`experiments/ns_abom_e8_leech_eqbit_002_claude/outputs/phase2/valdora_results.json`
(`NS-ABOM-E8-LEECH-EQBIT-002-VALDORA`). It refines the next experiment; it does not transfer E8 numerical results to Leech geometry.

### 10.1 What Valdora actually establishes

The recorded Valdora run reports:

- Leech: rank 24; 24 basis columns satisfy the Golay congruences; coordinate determinant and index-derived covolume both (2^{36}); scaled Gram determinant 1; integral, even, positive definite; minimum norm 4 attained by 196,560 vectors.
- E8/Gosset EQBIT: 240 vertices, degree 56, 6,720 edges; exact E8-root/Gosset-vertex bijection; antipodal map is a fixed-point-free involutive graph automorphism.
- E8/Gosset cut-rank: canonical antipodal rank 112; 10,000 random antipodal transversals have mean 118.433 (range 114–120); 10,000 arbitrary balanced cuts have mean 96.9364 (range 78–106). A degree-preserving rewired null gives rank 119 for the fixed original cut.
- The E8 result is independently consistent with Claude's phase-two run. It sharpens interpretation: rank 112 is lower than every sampled antipodal transversal but higher than every sampled arbitrary balanced cut. Do not call it globally maximal or simply “more entangling than a typical cut.”
- The Leech and EQBIT outputs have separate hashes. The ablation explicitly reports `NOT_DEFINED_BY_CURRENT_MODULE_CONTRACTS` for a shared observable. No measured Leech–EQBIT coupling exists in this run.

The Leech certificate is an exact algebraic/software result. The E8 cut-rank distributions are graph-specific sampled statistics. Neither gives a numerical prediction for the Leech kissing graph's cut ranks.

### 10.2 Exact Leech parity prediction for antipodal-transversal cuts

There is, however, a structural prediction that transfers by proof rather than by numerical analogy.

Let (u_1,\ldots,u_m) be one chosen representative from each of (m) antipodal pairs in a selected Leech subset, and put the (u_i) on the left and (-u_i) on the right. Under the kissing-graph adjacency rule, the cut matrix over GF(2) is

\[
B_{ij}=\mathbf 1[\langle u_i,-u_j\rangle=2]
      =\mathbf 1[\langle u_i,u_j\rangle=-2].
\]

The matrix is symmetric because the lattice inner product is symmetric. Its diagonal is zero because \(\langle u_i,u_i\rangle=4\), not (-2). Therefore (B) is an alternating matrix over GF(2), and its rank is **even**.

This predicts even cut rank for every antipodal transversal under this graph definition, for every sample size—not a particular rank value. The test must verify symmetry and zero diagonal before reporting parity. This is a useful exact Leech analogue of the E8 alternating-matrix explanation, not evidence that the two rank distributions coincide.

### 10.3 Add a structured full-neighborhood tier

The original global 120-pair sample remains a useful smoke test, but a uniformly selected 240-vertex induced subgraph is expected to be sparse: its mean induced degree is approximately

\[
239\cdot\frac{4600}{196559}\approx 5.59.
\]

That is appropriate for testing sampling, hashing, and rank code, but weak as the sole probe of local Leech incidence.

Add a preregistered local tier around one deterministic reference vector (r):

1. Enumerate its complete neighbor shell (N(r)=\{v:\langle r,v\rangle=2\}), expected size 4,600, using exact integer dot products.
2. Verify the full inner-product census from Section 4, not only the degree.
3. Form the paired vertex set (N(r)\cup -N(r)), containing 9,200 vertices and 4,600 antipodal pairs.
4. Compute the full 4,600-by-4,600 cut matrix between (N(r)) and (-N(r)) using the exact predicate \(\langle v_i,v_j\rangle=-2\).
5. Verify symmetry, zero diagonal, even GF(2) rank, and deterministic digest. Record the exact rank and row/column ordering.
6. Separately compute the induced graphs within (N(r)) and within (-N(r)), preserving them as distinct outputs. Do not infer their spectra or common-neighbor parameters from the E8 run.

This local tier uses the full 4,600-neighbor incidence structure rather than extrapolating from a global random sample. It is still a local shell experiment, not a materialization of all 452,088,000 kissing edges.

### 10.4 Resource projection and implementation guardrails

Valdora reports a full-orchestration peak of 60,530,407 Python-managed bytes and 104.48 seconds, versus 2,267,873 bytes when the Leech adapter is omitted. The corresponding run without flip-EQBIT reports 60,327,100 bytes and 8.84 seconds. These are `tracemalloc` peaks, not RSS, and the configuration differences are not clean isolated microbenchmarks; they nevertheless flag the Leech shell materialization as a memory-sensitive stage and the sampled EQBIT stage as a runtime-sensitive stage.

Consequently:

- Do not build the full Leech adjacency matrix or full edge list.
- Avoid Python object-heavy adjacency sets for the 9,200-vertex local tier if a compact bitset/packed-row representation suffices.
- Prefer a streaming minimal-vector iterator and signed-byte coordinate storage (all current integral shell coordinates fit in int8) so the 196,560 Python tuple objects need not remain resident.
- Measure wall time, peak traced Python heap, and process RSS separately where available.
- Cache the exact shell once per run; do not regenerate it independently for every reference vector.
- Keep the first implementation as a correctness-first reference path and compare any optimized packed implementation against its exact outputs.

### 10.5 Revised priority order

1. Reproduce Valdora's Leech certificate from the frozen source hashes and capture the source commit in the new artifact.
2. Add and test the exact reference-vector inner-product census.
3. Prove in code the alternating-matrix invariant for arbitrary sampled antipodal transversals.
4. Implement the full 4,600-neighbor local tier and its 9,200-vertex paired cut.
5. Retain the original 120-pair global sample as a secondary sampling/control path.
6. Add randomized transversals and balanced cuts only after the exact local result is frozen.
7. Compare E8 and Leech only at the level of declared graph invariants and protocol behavior; report dimension, graph construction, degree, and cut family separately.

No E8 rank value, ratio, tail probability, or ABOM/Fermi channel value is a prior for the Leech result. The next Leech rank is to be measured, not guessed.



## 11. Valdora follow-up: first local-shell computation

**Status:** computed in an independent analysis runtime; repository-runner reproduction is still pending. The raw summary is stored at `experiments/leech24_eqbit_001/results/local_shell_audit.json`, and the reproducible runner is `experiments/leech24_eqbit_001/local_shell_audit.py`.

The current-main three-family shell construction was independently reconstructed using signed 8-bit coordinate storage and exact signed 16-bit dot products. The 196,560-vector shell and family counts (1,104 / 97,152 / 98,304) matched the expected construction. For the first deterministic vector from each family, the full exact integer-dot histogram was identical:

| Integer dot product | Count |
|---:|---:|
| -32 | 1 |
| -16 | 4,600 |
| -8 | 47,104 |
| 0 | 93,150 |
| 8 | 47,104 |
| 16 | 4,600 |
| 32 | 1 |

Dividing the dot products by 8 gives the lattice inner products. The histogram digest was identical for all three representatives:
`a374826bed68944e3041f9aaf1109d8ec79bce1c731701501eb55d9806d9bb2e`.

### 11.1 Local shell results

For each of the three representatives, the exact 4,600-neighbor set was built. The 4,600-by-4,600 matrix
`B[i,j] = 1 iff dot(N[i], N[j]) == -16`
had:

- exactly 4,600 ones;
- every row and column degree equal to 1;
- symmetry and zero diagonal;
- no fixed points, and a fixed-point-free involutive partner map;
- exact GF(2) rank **4,600**.

Therefore this particular antipodal cut is not merely even-rank: it is a permutation matrix consisting of 2-by-2 swap blocks, so it is nonsingular and has full rank. This is a stronger, observed local result for the three deterministic representatives. The general alternating-matrix argument still predicts even rank for any antipodal transversal, but does not imply full rank for arbitrary transversals.

The induced graph on each (N(r)) was also computed. Each has 4,600 vertices, exactly 2,049,300 edges, and is 891-regular. The three order-sensitive adjacency digests are retained in the JSON artifact.

### 11.2 Interpretation and boundaries

The local cut has 4,600 crossing edges arranged as a perfect matching, while the within-neighbor graph is dense and 891-regular. This is a strong local incidence pattern, not yet a global Leech kissing-graph cut-rank distribution. It does not establish the spectrum, strong-regularity parameters, full automorphism group, or all-root uniformity by software enumeration.

The three reference vectors are deterministic representatives of the three construction families. Their matching histograms and local statistics are consistent with the known symmetry of the Leech minimal shell, but the computation itself has not enumerated the Co0 action or proved transitivity.

The raw result records that it was computed in an independent analysis runtime from a reconstruction of current-main source logic. It was **not** produced by running the newly committed repository runner. The next acceptance step is to execute that runner from the PR branch, compare every digest and statistic, then have a second bench reproduce it.

### 11.3 Updated next questions

1. Prove the perfect-matching map (v\mapsto w\) defined by (v,w\in N(r)) and (⟨v,w⟩=-2) from the lattice incidence identities, rather than relying only on three computed shells.
2. Determine the strongly regular / association-scheme parameters of the 891-regular graph induced on (N(r)), using exact integer common-neighbor counts and independent combinatorial derivation.
3. Establish whether the local matching and induced graph are canonically equivalent across all 196,560 choices of (r) under Co0.
4. Only then proceed to the global sampled Leech kissing-graph cut-rank distributions and compare protocol behavior with E8/Gosset.

No physical quantum or hardware claim follows from these graph-state cut-rank computations.


### 11.4 Exact explanation of the local perfect matching

The computed perfect matching has a direct lattice proof. Fix any minimal vector (r) and any (v\in N(r)), so
\[
\langle r,r\rangle=\langle v,v\rangle=4,
\qquad \langle r,v\rangle=2.
\]
Define (w=r-v). Then
\[
\langle w,w\rangle=4+4-2(2)=4,
\qquad \langle r,w\rangle=4-2=2,
\qquad \langle v,w\rangle=2-4=-2.
\]
Thus (w\in N(r)), and (w) is the unique cross-cut neighbor of (v). Conversely, if (w\in N(r)) and \(\langle v,w\rangle=-2\), then
\[
\langle v+w,v+w\rangle=4+4-4=4,
\qquad \langle r,v+w\rangle=2+2=4.
\]
Since (r) and (v+w) both have norm squared 4, equality in Cauchy–Schwarz forces (v+w=r), hence (w=r-v).

Therefore the cross-cut partner map is exactly
\[
\boxed{\;v\longmapsto r-v\;}
\]
for every (r\) and every (v\in N(r)). It is fixed-point-free and involutive because applying it twice returns (v), and (r-v=v) would imply (r=2v), incompatible with both vectors having norm squared 4 and inner product 2. Consequently the local cross-cut matrix is a permutation matrix with 2-by-2 swap blocks and has full GF(2) rank 4,600 for every reference vector—not merely the three sampled representatives.

This proof upgrades the matching/rank conclusion from a three-representative computational observation to an exact local theorem under the stated Leech norm and adjacency contract. The 891-regular within-neighborhood graph remains a computational result at this stage; its global uniformity and any stronger association-scheme classification require separate proof.
