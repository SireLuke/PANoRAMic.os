# STRATA — Scale-Transition Research and Analysis

**Status:** Architectural layer specification, v0.1  
**Placement:** Research and validation layer; not part of the canonical runtime boot path  
**Authority:** Non-authoritative. STRATA evaluates claims; it does not promote a result into PAN canon.

## Purpose

STRATA is PAN's reproducible framework for testing whether a proposed structure or relationship survives changes in scale, domain, representation, and observer/implementation. It is designed to distinguish:

1. **Analogy** — a useful resemblance, without demonstrated structural equivalence.
2. **Domain pattern** — reproducible within a bounded domain.
3. **Scale-persistent pattern** — retained across declared scales in that domain.
4. **Cross-domain candidate** — retained across independent domains and representations.
5. **Predictive candidate** — improves a preregistered prediction or classification task against appropriate baselines and controls.
6. **Candidate organizing principle** — repeatedly predictive under independent replication. This is still not automatically a scientific law.

No level is awarded from visual similarity alone. A failed test is a valid result and may narrow or redefine the claim.

## Architectural boundaries

- **PAN V8** remains the canonical eight-coordinate state description: `(h, R, u, d, τ, χ, s, f)`. STRATA may test mappings to V8 but must not silently redefine coordinates, weights, or units.
- **Janus Hydra** may serve as a feature/geometry translator. It is not STRATA's validation authority and must not score its own success.
- **UHFE/UDFE** remain paired formation/dissolution representations. STRATA may evaluate their outputs as candidate representations; it does not collapse them into Janus Hydra.
- **Gosset 4_21 / E8** is the primary geometric target for the relevant geometry experiments. Hyper-octahedral comparisons are auxiliary. A correct E8 construction is a mathematical control, not evidence of cross-domain universality.
- STRATA is an analysis/research layer. It does not mutate canonical records, change runtime state, or participate in boot unless a separately reviewed adapter is later approved.

## Required test dimensions

Every claim must declare its tested dimensions before analysis:

| Dimension | Minimum requirement | Audit question |
|---|---|---|
| Scale | At least 3 declared scales | Does the feature persist under meaningful coarse/fine transitions? |
| Domain | At least 2 independent domains for cross-domain claims | Are domains genuinely distinct, not relabeled copies? |
| Representation | At least 2 encodings | Does the result survive a representation change? |
| Observer / implementation | Independent implementation or reviewer where feasible | Is the result tied to one pipeline or analyst? |
| Controls | Randomized and structure-preserving controls | Does the result exceed what trivial structure explains? |
| Prediction | Held-out target and baseline comparison | Does it add measurable out-of-sample value? |

A missing dimension is reported as **not tested**, never silently counted as a pass.

## Standard pipeline

`source → provenance/quality checks → domain adapter → feature extraction → scale transition → representation transition → controls → held-out evaluation → report`

Every run records:

- immutable source identifiers, license, retrieval date, and checksums where applicable;
- dataset inclusion/exclusion rules and missingness;
- adapter and transformation versions;
- random seeds and software/runtime versions;
- preregistered hypotheses, metrics, thresholds, and baseline models;
- development/blind split identity and leakage checks;
- positive, negative, null, and inconclusive outcomes.

## Controls and failure conditions

At minimum, select controls appropriate to the data-generating process. Examples include label permutation, feature permutation, degree-preserving graph rewiring, null models, simple domain-native baselines, and ablations. Do not apply an inappropriate control merely to satisfy a checklist.

A claim fails or remains inconclusive when:

- the effect disappears at one or more required scales;
- transfer fails in an independent domain;
- an alternative representation reverses or erases the effect;
- randomized or structure-preserving controls perform comparably;
- predictive performance does not beat the preregistered baseline on held-out data;
- leakage, provenance gaps, or implementation dependence prevent interpretation.

Report effect sizes, uncertainty intervals, sample sizes, and failure cases. Do not convert a threshold pass into a claim of physical mechanism.

## Evidence record

Each STRATA result should be a versioned record containing:

- `claim_id`, hypothesis, and evidence level;
- source manifest and provenance;
- domains, scales, and representations actually tested;
- adapters, transformations, controls, and seeds;
- metrics, baselines, uncertainty, and blind-set performance;
- status per test dimension: `pass`, `fail`, `inconclusive`, or `not_tested`;
- limitations, reviewer notes, and reproduction instructions.

## Initial research program: STRATA-002

STRATA-002 is a cross-domain representation benchmark. Its first milestone is deliberately modest: validate the pipeline and its controls on deterministic synthetic structures, then add independently sourced empirical datasets. Synthetic results are software checks only; they cannot establish biological, ecological, infrastructural, or physical invariants.

The Gosset/E8 adapter is tested against the repository's existing construction and exact mathematical checks. It is a geometry benchmark, not a substitute for empirical domains.

## Reference implementation and records

The dependency-free STRATA-002 smoke implementation lives in [`experiments/strata/`](../experiments/strata/README.md). Its evidence record shape is defined by [`strata-run.schema.json`](../experiments/strata/strata-run.schema.json), and the latest bounded geometry audit is [`STRATA-002-GEOMETRY-AUDIT-2026-11-09.json`](../experiments/strata/runs/STRATA-002-GEOMETRY-AUDIT-2026-11-09.json). Run `python experiments/strata/validate_run.py` from the repository root to validate the record structure.

## Non-goals

STRATA does not assume that one representation is universal, that V8 is a physical law, that a geometric analogy implies causal identity, or that every domain must map cleanly into the same coordinates. Its job is to make such claims testable and falsifiable.
