# STRATA Protocol v0.1

**Name:** Scale-Transition Research and Analysis  
**Status:** Experimental protocol  
**Authority:** Evidence-assessment framework; not a scientific authority or production runtime component.

## Claim ladder

- Analogy
- Reproducible domain pattern
- Scale-persistent pattern
- Cross-domain candidate
- Predictive candidate
- Candidate organizing principle

Each promotion requires new evidence. Visual resemblance alone never qualifies.

## Required dimensions

For a cross-domain invariant claim, preregister at least three meaningful scales, two independent domains, two representations, observer/implementation checks, randomized and structure-preserving controls, and held-out predictive evaluation. Record absent dimensions as `not_tested`.

## Pipeline

Source and provenance → quality checks → domain adapter → feature extraction → scale transition → representation transition → controls → held-out evaluation → report.

## Failure states

A result fails when the preregistered effect is absent, reverses, or is matched by an appropriate null/control. It is inconclusive when data quality, sample size, provenance, leakage, or implementation independence prevents interpretation. A failure is retained in the report; it is not silently discarded.

## Minimum report fields

Claim and hypothesis; source manifest; domain/scale/representation; adapter and transformation versions; random seeds; split policy; metrics and baselines; uncertainty; per-dimension status; limitations; reproduction instructions.

## Guardrails

- V8 coordinate semantics remain unchanged: `(h,R,u,d,τ,χ,s,f)`.
- Janus Hydra is a translator, not the validation authority.
- UHFE and UDFE remain distinct paired representations.
- Gosset `4_21` / E8 is the primary geometry target where relevant, not proof of cross-domain equivalence.
- Synthetic fixtures test software behavior only.
- No experiment automatically changes canonical records or runtime behavior.
