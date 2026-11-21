# Pressing for truly Navier–Stokes — preregistered test plan

**Status:** APPROVED by the maintainer 2026-11-21 ("looks
excellent and push your pre reg plans"). This document *is* the
preregistration: parameters are pinned before any run, and
deviations are recorded as amendments, never edited in silently.

**Where we stand.** NS-EVIDENCE-001 is frozen and reproduced by
three independent implementations (OpenAI, Claude blind, Cosmo):
the machinery is a trustworthy baseline. What it never touched:
high-Reynolds dynamics, small-scale generation, any
near-singular regime. This plan presses the same machinery,
unchanged in kind, toward the actual question — in stages, each
with its null declared in advance.

**Global fences (apply to every stage).** No numerical run can
prove blow-up or global regularity; stages produce *evidence
patterns*, graded on the STRATA ladder. Negative results are
first-class and get OMNIQUASI registry entries like successes.
Any stage whose result would be cited gets the three-seat
treatment (independent implementations, numbers frozen before
comparison). Navier–Stokes remains `not_tested` until a stage
earns a rung — and no stage here can earn the top ones.

## Stage A — Literature calibration (claim class: numerical reproduction)

Classic 3D Taylor–Green at high Reynolds number, the community's
standard reference case. Purpose: prove the harness survives
contact with a regime where energy cascades and small scales
form, against published reference behaviour (enstrophy peak
time and magnitude, spectrum at peak time).

- Reference values to be **pinned from the cited literature at
  preregistration** (Brachet-lineage TG data), never from memory.
- Compute honesty: literature-grade resolution (N ≥ 256) may
  exceed the benches' current environments; if so, run a reduced
  Re with the scaling expectation declared in advance, and say
  which one was done.
- Null: the harness is a low-mode toy and will miss the
  reference outside tolerance at every affordable resolution.
  Gate: match the pinned references within declared tolerance,
  or the press stops here and the harness gets upgraded first.

## Stage B — BKM monitoring (claim class: numerical evidence pattern)

The Beale–Kato–Majda criterion: a singularity at T* requires
∫₀^T* ‖ω‖∞ dt to diverge. Track M(t) = ‖ω‖∞(t) and its running
integral across a declared family of increasingly strong smooth
initial data, at increasing resolution.

- Pattern sought: saturation of the integral under refinement
  (regularity-consistent behaviour) vs super-critical
  acceleration that *stiffens* under refinement
  (singularity-consistent trend).
- Fence, in bold: finite resolution can never certify
  divergence. A stiffening trend is a pattern to report, not a
  blow-up claim; a saturating trend is not a regularity proof.
- Null: trends are resolution artefacts that invert between
  successive refinements — recorded as inconclusive, which is a
  result.

## Stage C — The Fermi-sea dictionary test (claim class: preregistered comparison)

The programme's own picture, made falsifiable. From each run's
energy spectrum define the **occupation front** K(t): the
smallest wavenumber beyond which shell occupation stays below a
declared threshold for the remainder of the run.

- **Prediction (declared in advance):** in the intensifying
  cases, log K(t) advances toward a finite ceiling, with
  log-periodic modulation. The period candidates are pinned
  before running from **two** families, because the project's
  own bridge note (PR #126, merged) returned *same family,
  different constants* for the one concrete blow-up
  construction on the table — its self-similar period
  S̄ ≈ 0.36 is **not** a φ constant, and its half-period twist
  is π/19: (i) the barbershop construction's log φ family, and
  (ii) the bridge-note constants (period scale set by S̄;
  twist structure 2π/19). A signature at either family counts;
  a signature at neither is the null. The fitting band is
  declared with the candidates.
  *(Stage C amended 2026-11-21 at the maintainer's direction,
  before merge, to record the bridge-note verdict.)*
- **Nulls:** (i) no ceiling — the front exits the resolved range
  without deceleration structure; (ii) approach without
  log-periodicity beyond what the controls show.
- **Controls:** phase-shuffled fields with identical spectra
  (same occupation, no coherence) run through the identical
  pipeline; a standard decaying case with no intensification.
- **Falsifier:** if the ceiling/log-periodic signature does not
  separate the intensifying cases from the controls by the
  declared margin, the dictionary reading **fails at this rung**
  and is filed as a negative result. The programme keeps its
  other rungs; this one is spent honestly.

## Stage D — The Alpöge–Buckmaster cross-check (conditional)

Runs only if their certificate is released (the 2026-11-22 check
watches for it). Any log-periodic quantities observed in
Stages B–C are compared against the bridge note's extraction
(S̄ ≈ 0.36, half-period twist π/19) under the bridge note's own
criteria. Until then this stage is a placeholder, not a task.

## Sequence and seats

A → B → C, D when unlocked. Each stage: preregistered
parameters appended below before execution; one bench runs,
the others replicate before anything is cited; results —
including failures — registered in OMNIQUASI and reported to
the maintainer with grades attached.

*Drafted by Cosmo (Memory bench), 2026-11-21, at the
maintainer's direction: "take our results and press for testing
truly Navier–Stokes."*
