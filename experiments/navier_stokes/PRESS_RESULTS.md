# NS Press — Final Stage C Verdict (2026-11-21)

> **Provenance (repo filing):** Results of the preregistered NS press
> (plan: `experiments/navier_stokes/ns-truly-testing-plan.md`, OS PR #134,
> merged 2026-11-21; Amendment 1 pins recorded in the plan's workspace
> copy before analysis). Run and analysis by Cosmo (Memory bench);
> filed at the maintainer's explicit direction, 2026-11-21, together
> with the OMNIQUASI registration OQ-EXP-2026-002. Solver, analysis
> scripts, and run data are in `press_data/` beside this note.

Run: Taylor–Green, N = 128, ν = 1/1600 (Re 1600), T = 12.

## Stage A — PASS (unchanged)
ε_max = 0.0137585 at t = 8.90 vs pinned reference 0.01286 at t = 8.97
(ratio 1.070, inside the declared +10%/−5% gate; Δt = −0.07 inside ±0.4).
The solver is honest at this resolution.

## Stage B — in band (unchanged)
BKM ∫₀¹⁰‖ω‖∞dt = 188.36, inside the declared 180–210 band from the
published resolution ladder. ‖ω‖∞ peak 44.24 at t = 8.70.

## Stage C — NEGATIVE RESULT (per the preregistration's own falsifier)

The Stage C dictionary signature was two-legged: (1) a saturating
occupation front (ceiling model beats no-ceiling model by residual-RMS
ratio < 0.8 on t ∈ [4, t(ε_max)]), and (2) log-periodicity in the front's
approach at the pinned candidate periods, required to separate from the
preregistered controls.

**Leg 1 — ceiling: passes its fit test, fails specificity.**
Main run ratio 0.428 (PASS). The phase-shuffled control — identical
energy spectrum, randomized phases, no coherent Taylor–Green dynamics —
passes the same test at 0.461, with a front series of the same shape
(peak K = 56 vs the main run's 58). The saturating front is a property
of the shared spectrum and the front statistic at this resolution, not
of the coherent dynamics.

**Leg 2 — log-periodicity: fails to separate.**
Main run, log φ candidate: amp/resid_std = 0.828 (global best period
0.584). Shuffle control, same machinery: log φ = **0.938**, global best
0.959 at period 0.580. The control meets or exceeds the main run at the
log φ, S̄, and 2 log φ candidates. By Amendment 1's rule the signature
does not separate from its control.

**Verdict:** the Fermi-sea dictionary entry tested here — the
occupation front K(t) and its approach — does **not** distinguish
coherent Taylor–Green dynamics from a phase-scrambled field with the
same spectrum, at N = 128 with this statistic. Filed as a negative
result, first-class, exactly as preregistered. Navier–Stokes remains
`not_tested`. Stage A and Stage B stand; they grade the solver, not
the dictionary.

**Caveats on the record:** the control comparison rests on a single
shuffle realization (a point comparison, not an ensemble 95th
percentile — declared in `stage_c_controls.py` before it ran). The
grid caveat stands: the Kolmogorov estimate k_d ≈ 87 exceeds the
front's ~57, so truncation is a live alternative explanation, and the
shuffle result strengthens the spectrum/truncation reading. The
ν = 0.01 decaying baseline (the second control) completes the record
separately; it cannot change the separation verdict, which the
identical-spectrum control decides.

**What this does not kill:** the Fermi-sea programme. It kills one
statistic at one resolution as evidence for it. The front K(t) is
spectrum-dominated; a phase-aware dictionary entry (triadic coherence,
an enstrophy-spectrum front, structure-function fronts) or a resolution
at which the front separates from k_d is the next instrument iteration
— a new preregistration, not a patch on this one.

## Files
- Main run: `press_data/re1600_n128.json`, `press_data/stage_c_results.json`
- Shuffle control: `press_data/re1600_n128_shuffle.json`, `press_data/stage_c_shuffle_results.json`
- Baseline: `press_data/re001_nu001.json`, `press_data/stage_c_baseline_results.json`
  (appended on landing, 2026-11-21: front peak K = 12 vs the main run's
  58; eps_max 0.012975 at t = 4.9; BKM 36.48. The ceiling and periodicity
  legs are degenerate on this control - K is constant (= 12) across the
  whole intensification interval, so both fits are exact and the
  periodicity ratios are undefined (NaN) rather than detections. The
  decaying control develops no front and yields no signature, as a
  control should; the degeneracy is recorded, not laundered.)
- OMNIQUASI registration: OQ-EXP-2026-002, filed in this same change,
  as a negative result.
