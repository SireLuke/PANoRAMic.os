# NS–ABOM–E8–LEECH–EQBIT-002 — Claude bench (independent run, sections A and C)

**Grade:** deterministic software + exact algebra + seeded sampling. Not physical validation; Navier–Stokes stays `not_tested`.
**Not implemented here:** section B (ablation) and the Leech audit. Valdora's runner covers both (see "Compared with the other seats").

## Order of operations (so the independence can be checked)
1. `ns_abom_claude.py` written without reading `integration.py`, `cut_rank_audit.py` or `e8_root_system.py`; smoke-tested with `--quick`; **frozen at commit 1ff2a50** (2390bae before a rebase onto main).
2. Full run, digest `1abed21a…5735`, reproduced bit-for-bit by a second run (`outputs/results.json`, 3 m 43 s).
3. Only after the results commit were the other seats' code and outputs read and run (`outputs/phase2/`).
4. `exploratory_x1.py` is post-hoc and carries its own ID (`…-002-X1`).

## Section A — Gosset graph, GF(2) cut-rank (10 seeds × 1,000 per family)
Exact checks: 240 distinct roots, norm² 2, inner products ∈ {−2,−1,0,1,2}; Gosset graph 240 vertices, degree 56, 6,720 edges; negation is a fixed-point-free involution and a graph automorphism. Rank implemented three ways (XOR basis, dense numpy, span enumeration for small matrices); 7 hand fixtures + 300 random small matrices agree; 220/220 sampled partitions agree between the two large-matrix implementations. Relabelling invariance holds.

| family (n) | min | mean | median | max | P(R ≤ 112) | P(R ≥ 112) |
|---|---|---|---|---|---|---|
| canonical antipodal | **112** | | | | | |
| random transversal (10,000) | 114 | 118.445 | 118 | 120 | 1.0e-4 (0/10,000, CP95 upper 5.6e-4) | 1 |
| balanced 120\|120 (10,000) | 85 | 96.891 | 97 | 107 | 1 | 1.0e-4 (0/10,000, CP95 upper 5.6e-4) |
| rewired graph, same pairing (1,000, labeled null) | 117 | 119.182 | 119 | 120 | 1.0e-3 | 1 |

Plus-one estimator throughout, so 1.0e-4 is the floor of this design, not a measured probability. Two primary contrasts, two-sided, Holm: both 4.0e-4.

**The two contrasts point in opposite directions.** 112 is above every balanced sample and below every transversal sample. It is the matched control (transversals, which keep the antipodal structure) that tests the "flip pairing" idea, and there 112 is the low end, not the high end. The maximum possible is 120 and is reached by about 29% of transversals.

**Why transversal ranks are even (exact).** For a transversal S, the cut matrix is B[u,v] = A(u,−v) = [⟨u,v⟩ = −1]. That is symmetric with zero diagonal over GF(2), i.e. alternating, so its rank is even. All 10,000 sampled ranks are in {114,116,118,120}; the rewired graphs, where the argument fails, give odd ranks too (117, 119).

**Exploratory X1 (post-hoc).** All 500 random "positive systems" (roots with positive value under a generic linear functional) give rank 112, as do both of my canonical conventions. This fits the standard fact that W(E8) acts transitively on positive systems and acts by graph automorphisms, which would make 112 exact for all of them; I checked 500, I did not prove it here. Flipping a few pairs away from a positive system raises the rank quickly (mean 113.8 after 1 flip, 115.4 after 2, 117.6 after 4, ≈118.4 from 16 on). So 112 characterizes the half-space cut, not "the antipodal pairing" as such.

**Alternative involutions (secondary contrast).** Search over products of k mutually orthogonal root reflections (every Weyl-group involution has this form), 6,000 tries: the only fixed-point-free one is −1 (k=8). k=7 leaves ±β fixed, k≤6 fix 4 to 126 roots. So within W(E8) there is no alternative to test; I did not prove that Aut(Gosset graph) = W(E8).

## Section C
- **NS probe:** my nine E_T values and Cosmo's `ET` agree to ≤ 2.3e-15 absolute. Frozen-ET occupation spans 0.4381–0.4697 and signed contrast −0.1239…−0.0606.
- **ABOM channels vs a 60-digit Decimal reference:** max abs error 1.7e-16 over all 45 probe values; closed forms σ(−E), σ(E), −tanh(E/2) hold; channels sum to 1 to < 1e-15.
- **Controls:** zero probe → 0.5 / 0.5 / 0 exactly. Seeded permutation and seeded shuffle of the nine values are the same control (ABOM is a pointwise map, so the multiset of outputs is identical: verified `True`). Range-matched uniform gives a visibly narrower spread. Adapter sensitivity only.
- **ABOM ↔ E8:** count 240 equal, coordinates exact half-integers, root sets equal as sets; canonical hash of ABOM's view equals mine (`3a904a5e…`). Valdora's hash of the same set differs (`ffd4093b…`) only because it serialises Fractions differently; both sides pass their own equality check.
- **E8 ↔ Gosset:** my vertex *i* is root *i* by construction. Comparing against the other bench's labelling is Valdora's `root_vertex_map_sha256`; not reproduced here.

## Compared with the other seats
| item | flip-eqbit audit (10,000, seed 20261121) | Valdora runner | mine |
|---|---|---|---|
| antipodal rank | 112 | 112 | 112 |
| transversal mean | 118.4448 | 118.433 | 118.445 |
| balanced mean / min | 96.908 / 82 | n/a in the summary I read | 96.891 / 85 |
| graph automorphism of −1 | contract only | checked | checked |
| alternative involutions | not run | NOT_SEARCHED | searched: none besides −1 |

Means differ by less than their Monte-Carlo standard errors (≈0.011 transversal, ≈0.03 balanced); minima of the balanced family differ because they sit in a thin tail. No numeric disagreement.

**One wording disagreement.** `flip-qubit-experiment-results.md` E4 says 112 is "close to the *most* entangling balanced cut … clearly more entangling than a typical cut". That holds against unconstrained balanced cuts (max seen 107) but not against the matched control (every transversal sample ≥ 114, max 120). Its own caveat ("the claim is the 112") stands; the "close to the most" phrasing does not survive the transversal comparison. The audit's field `antipodal_rank_at_least_transversal_fraction: 0.0` already says this, but is easy to read the other way.

**Section B (Valdora's run, executed by me as a check).** Six configurations; shared observable `NOT_DEFINED_BY_CURRENT_MODULE_CONTRACTS`; full run 104.5 s, minus-Leech 100.4 s, minus-flip-eqbit 8.8 s, NS-only 0.5 ms. That matches the protocol's expectation: removing a module removes only its own output. Output: `outputs/phase2/valdora_results.json`.

## Limits
- Same standard E8 construction (doubled integer coordinates) and the same lex-positive convention as the flip-eqbit audit, so code is independent, the mathematical choice is not. The convention was chosen before reading that audit, and the spec does not fix one.
- Graph-null spectrum not checked. Seeds and RNG are mine (PCG64, `SeedSequence([seed, family_id])`), so exact sampled counts differ from the other seats by design.
- 1.0e-4 tail values are the plus-one floor; with 10,000 samples nothing smaller can be reported.
- Nothing here couples NS to the graph; `NS_EQBIT` stays `NOT_COUPLED`.

Authored-by: Claude (Anthropic, Architect bench)
