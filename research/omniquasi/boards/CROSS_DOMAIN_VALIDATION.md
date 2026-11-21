# Cross-Domain Methods & Validation Board

**Status:** proposal. **Purpose:** ensure cross-domain analogies and shared tools produce testable results rather than accidental pattern matching.

## Core test for a proposed mapping

1. **Objects:** identify source and target objects.
2. **Map:** define the transformation explicitly.
3. **Preserved structure:** name quantities, relations, symmetries, or invariants preserved.
4. **Lost structure:** state what information is discarded or distorted.
5. **Null model:** specify a simpler or randomized mapping expected not to perform as well.
6. **Metric:** define a measurable outcome.
7. **Domain review:** identify reviewers qualified in each field.
8. **Falsifier:** state what observation would reject the correspondence.

A shared diagram, vocabulary, dimension count, or visual resemblance is not enough.

## Shared experiment manifest

Stable experiment ID/version; question and claim class; hypothesis, null, controls, and success criteria; data provenance, licensing, exclusions, preprocessing; code revision, environment, dependencies, commands, seeds; parameters and stopping criteria; raw outputs, summaries, uncertainty, failures; independent reproduction/review; scope of inference and limitations.

## STRATA and scale transitions

Specify scales and domains before inspecting outcomes, define transition invariants, include leakage checks, and report uncertainty. Three scales and two domains may be a useful design pattern where justified, not a universal law. Negative and inconclusive results remain part of the record.

## Claim classes

Keep formal proof, proof-assistant checked theorem, exact computation, numerical experiment, empirical measurement, simulation, software test, analogy, and conjecture separate. Evidence in one class does not silently upgrade a claim in another.

Entry fields: mapping/hypothesis; source and target domains; preserved/lost structure; null and controls; metric/falsifier; result/uncertainty; independent domain review.

Authored-by: OpenAI (ChatGPT bench)
