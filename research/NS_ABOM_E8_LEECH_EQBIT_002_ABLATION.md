# NS–ABOM–E8–LEECH–EQBIT-002
## Preregistered multi-module ablation and null-control study

**Status:** protocol only; no new experiment runs or outcomes are claimed.
**Parent experiment:** NS–ABOM–E8–LEECH–EQBIT-001.
**Mode:** read-only analysis of existing artifacts plus deterministic control generation.
**Evidence grade:** preregistration / experimental design.

## 1. Question and scope

The first composition harness established that existing modules can be called together and that provenance and dimensional boundaries can be retained. Its pairwise PASS labels mostly certify interface compatibility or artifact coexistence. This follow-up asks a narrower, falsifiable question:

> Do the declared adapters and structural choices produce measurable, reproducible outputs that differ from appropriately constrained null controls?

This is a software/mathematical-structure experiment. It does not test a unified physical law, Navier–Stokes regularity, quantum hardware, quantum advantage, or physical coupling among the modules.

## 2. Frozen inputs

Before running, record immutable commit SHA, file SHA-256 hashes, Python and dependency versions, OS, command line, seed, and UTC timestamp for:
- the nine frozen NS-EVIDENCE-001 cases;
- ABOM V8 implementation and its declared input/output schema;
- exact E8 root generator;
- Leech basis/minimal-shell audit;
- flip-eqbit/Gosset graph and cut-rank audit.

Do not regenerate or edit the frozen NS results. Do not silently change V8 coordinate order (h,R,u,d,tau,chi,s,f). Do not identify PAN V8's eight state coordinates with the rank-8 E8 root space. Keep Leech rank 24 and Navier–Stokes spatial dimension 2/3 distinct.

## 3. Primary outcomes

### A. Flip-eqbit partition structure

Primary statistic: GF(2) rank of the adjacency cut matrix for a 120|120 vertex partition of the 240-vertex Gosset graph.

Predeclared partitions:
1. canonical antipodal partition;
2. random transversal partitions that select exactly one endpoint from each of the 120 antipodal pairs;
3. uniformly sampled balanced 120|120 partitions.

Use 10,000 samples per randomized family, with a fixed published seed list (at least 10 seeds, 1,000 samples per seed). Store every sampled rank, not only summary quantiles. Report min, max, mean, median, standard deviation, 5th/95th percentiles, empirical tail counts, and Monte Carlo uncertainty. The previously observed 1,000-sample results (antipodal rank 112; transversal mean about 118.47; balanced mean about 96.96) are exploratory and are not confirmatory data for this preregistered run.

For each empirical tail probability, use the plus-one estimator (k+1)/(n+1) and report a 95% binomial interval. Do not report zero probability from zero observed events.

Controls:
- vertex relabeling must leave rank invariant; this is an implementation sanity check, not an independent null;
- verify the involution is a fixed-point-free graph automorphism before calling a partition antipodal;
- include degree-preserving random graph rewires as a separately labeled graph-null family; do not claim they preserve spectrum unless explicitly checked;
- optionally include spectrum-preserving controls only if a documented algorithm and exact verification are supplied.

Primary contrast: canonical antipodal rank versus the two partition null distributions. Secondary contrast: whether any effect survives alternative valid fixed-point-free involutions/automorphisms. If no such involutions are available, report that limitation rather than substitute arbitrary pairings and call them automorphisms.

### B. Multi-module ablation

The harness currently reports pairwise checks, but several gates are compatibility checks rather than measured coupling. The ablation must make this distinction explicit.

Run the following configurations on the same frozen inputs:
- full orchestration;
- minus ABOM adapter;
- minus E8 comparison adapter;
- minus Leech audit adapter;
- minus flip-eqbit adapter;
- NS snapshot only.

For each configuration, report: which outputs are present; which validation checks remain executable; runtime and peak memory where measured; deterministic output hashes for unchanged modules; and whether removing a component changes any shared measured observable.

Ablation of a module that has no shared observable is expected to remove only that module's output. This is a valid negative result. Do not manufacture a scalar score to force every module to appear coupled.

### C. Adapter and mapping controls

The current NS-to-ABOM energy input is an explicitly dimensionless probe. Compare it with: a constant-zero probe; a seeded permutation of the nine frozen ET values; a seeded shuffle of the nine ET values with the multiset preserved; and a range-matched random probe, with distribution and seed recorded.

For every probe, report ABOM outputs channel-by-channel (occupation, hole fraction, signed contrast, root-count view, and any other documented output). This tests adapter sensitivity only. No physical units or energy identification are implied.

For ABOM-to-E8, test exact root-count equality and, separately, compare canonical root-set hashes after canonical serialization. Root count alone is not a strong structural identity test.

For E8-to-Gosset/flip-eqbit, compare canonical vertex/root incidence or an explicitly documented bijection, not only the shared number 240. If no canonical mapping is exposed by existing code, mark the stronger check NOT_IMPLEMENTED.

For E8 and Leech, retain independent certificates. No embedding or shared-coordinate assertion is allowed in this study.

## 4. Statistical and reproducibility rules

- Freeze hypotheses, seeds, sample counts, and exclusion rules before execution.
- Use independent random streams for each control family; record the generator and seed.
- Report raw machine-readable samples plus a human-readable summary.
- No post-hoc threshold tuning. Any exploratory follow-up receives a new experiment ID.
- For multiple primary comparisons, report adjusted p-values or clearly label unadjusted exploratory comparisons.
- Distinguish exact algebraic results, deterministic software checks, sampled estimates, and interpretation.
- A failed test is retained with traceback and environment metadata; do not delete or overwrite failed runs.
- Repeated runs must reproduce exact deterministic outputs; randomized outputs must reproduce from recorded seeds.

## 5. Acceptance criteria

The protocol is considered implemented only when:
1. each configuration can run without mutating source artifacts;
2. every output includes provenance and schema version;
3. the partition controls validate balance and antipodal-pair constraints;
4. rank calculations are independently cross-checked on small fixtures;
5. randomized outputs reproduce exactly from fixed seeds;
6. ablation results report absent/unchanged/changed outputs without inventing cross-module coupling;
7. all claimed gates map to explicit assertions and tests.

A scientific effect is not accepted merely because the harness exits successfully. It requires a preregistered statistic, null distribution, uncertainty report, and independent reproduction.

## 6. Explicit non-claims

This study does not establish a common physical system or metric across modules; a 9D fluid domain; an E8-to-Leech embedding; physical Fermi-sea dynamics; a quantum computer, quantum advantage, or hardware implementation; Navier–Stokes global regularity or blow-up; or a physical interpretation of ABOM probe values.

## 7. Execution status

**Not run.** This file is a preregistration only. No new benchmark result, p-value, confidence interval, or CI status is asserted.

Suggested future commands should be added only after an implementation PR supplies the actual runner and tests.

Authored-by: OpenAI (ChatGPT bench)
