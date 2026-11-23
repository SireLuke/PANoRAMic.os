> **Filing note (2026-11-22, Claude, Architect bench).** Filed before any Press II run, as a successor to
> OS PR #134. The body below (Sections 0–5) is Cosmo's draft as ruled by the maintainer, reproduced
> verbatim from the workspace copy. Only this note and Section 6 are added by the filer. The calibration
> self-test script and its tests are committed in this same change (`experiments/navier_stokes/press2/`,
> `tests/test_ns_press2_selftest.py`). **No run is authorized by this document.**

# NS Press II — Preregistration (DRAFT for maintainer review)

> **Status:** Workspace copy, written 2026-11-21 by Cosmo
> (Memory bench) at the maintainer's direction. **Maintainer decisions
> ruled 2026-11-22** (see §5): all four decisions adopted as
> recommended, plus Claude's two additions (calibration self-test;
> snapshot-comparison declaration) adopted and folded into §3.
> Ready for filing — the filing PR is Claude's to open, per his
> offer. **No run is authorized by this document**; running awaits
> the maintainer's separate word.
> **Lineage:** Successor to the Press I preregistration (OS PR #134)
> and its outcome (OS PR #157; OMNIQUASI OQ-EXP-2026-002, negative
> result). Nothing in Press I is relitigated here; its Stage A/B solver
> calibration stands and is inherited.

## 0. Why Press II exists

Press I's Stage C statistic — the spectral occupation front K(t) — is
built from shell energies E_j(t) alone. Shell energies carry no phase
information, so the statistic is **phase-blind by construction**: a
phase-shuffled field with the identical spectrum reproduced both the
ceiling shape and the log-periodicity scan statistics, and the
dictionary entry was refuted at N = 128 under the preregistered
falsifier.

Press II tests the repair proposed by the maintainer on 2026-11-21:
observables that are **phase-aware** — quantities that vanish or drop
sharply under phase randomization. If a Fermi-sea dictionary entry is
to say anything about coherent dynamics, it must be built from
observables of this kind.

## 1. Runs

- **Main run (one):** Taylor–Green, N = 128, ν = 1/1600 (Re 1600),
  T = 12, dt = 0.005 — identical parameters to Press I, for direct
  comparability. Resolution is deliberately *not* raised in Press II:
  the question is statistic-vs-null, and comparability with Press I
  is worth more than resolution here. (Declared ladder: if separation
  appears at 128, Press III confirms at 192; if it does not, raising
  resolution is not the next move — the statistic is.)
- **Controls (in-run, no extra integrations):** at every statistics
  snapshot (§3), the live field û is phase-shuffled **M = 100** times
  (Hermitian-symmetric shuffles preserving |û(k)| exactly, seeds
  20261122 + i, i = 0…99) and every observable is recomputed on each
  shuffle. The null is therefore *the same field, same spectrum,
  phases destroyed* — the sharp null for "does this observable detect
  coherence present in this field at this instant."
- **Secondary control:** the Press I ν = 0.01 decaying baseline
  already stands in the record (front peak 12, no signature). A
  Press II baseline run with the new diagnostics is optional and the
  verdict does not hinge on it.
- Out of scope: shuffled-initial-condition *evolution* runs (how fast
  dynamics regenerates coherence is a different question, for a later
  preregistration).

## 2. Observables (definitions pinned before any run)

Statistics snapshots at cadence 0.25 from t = 0 to t = 12
(49 snapshots), computed in-run.

**O1 — Triadic phase coherence (flagship).**
Triad set, declared: all (k, p, q) with k + p + q = 0 and
|k|, |p|, |q| ≤ 32, modulo the standard symmetries; if the exact count
exceeds 200,000, a seeded sample of 200,000 (seed 20261122) is used
and the count recorded. Statistic: the amplitude-weighted mean
resultant length of the biphase Φ = φ(k) + φ(p) + φ(q),

  C_tri(t) = |Σ w·e^{iΦ}| / Σ w,   w = |û_k|·|û_p|·|û_q|,

with the weights (spectrum-determined) held identical between the
field and its shuffles; only the phases differ. Under shuffling,
C_tri → O(1/√N_eff). **Active weight:** W(t) = Σ w is reported
alongside C_tri, which is read only at snapshots where W(t) >
10⁻³ × (maximum W over the window) — the initial condition is a
single-mode family with essentially no active triads at t = 0, and
W certifies when the statistic has anything to read. (Added
2026-11-22, with the V8-channel preregistration, whose ABC leg
pins W(0) ≈ 0 and F(0) = 2.25 as exact calibration points.) This observable is the phase content of the
energy-transfer mechanism itself, not a proxy for it.

**O2 — Vorticity kurtosis (witness).**
Component-wise flatness F_i(t) = ⟨ω_i⁴⟩ / ⟨ω_i²⟩², averaged over
i = 1, 2, 3, computed in physical space at the diagnostic cadence
0.025. Gaussian value 3; developed Taylor–Green flow runs well above
3 through the intensification window; same-field shuffles sit at ~3
by Gaussianization. (Not retro-computable from Press I data — no
field snapshots were saved — which is why it is an in-run diagnostic
here.)

**O3 — Antipodal biphase (the repaired EQBIT-flavoured entry).**
Triads of the form (k, q−k, −q), which sum to zero, for declared
small modes |q| ∈ {1, 2} (shells by |q|² = 1, 2) and 4 ≤ |k| ≤ 32.
Statistic: amplitude-weighted mean resultant of
Φ = φ(k) + φ(q−k) + φ(−q), as in O1. φ(q−k) is a genuinely free
phase, so the statistic can separate.
**Preregistered non-observable:** any statistic built from
φ(k) + φ(−k). For a real field û(−k) = û*(k) identically, so that
sum is zero by arithmetic in *every* field, shuffled or not; it is
recorded here as excluded, so that no later analysis "discovers"
perfect antipodal locking that was never there to find.

**O4 — Occupation front K(t) (demoted).** Computed exactly as in
Press I and reported as a **spectrum gauge only**. No dictionary
claim attaches to it in Press II; the Press I ceiling and
log-periodicity verdicts stand unrevised.

**Out of scope — the E₈ axes version of O3.** Mapping the 120 E₈
antipodal axes onto 3D Fourier modes requires a declared projection
adapter (the composition line's firewall discipline). It is not
assumed here; if pursued, it gets its own preregistration with the
projection stated as a choice.

## 3. Windows, thresholds, verdict rules (pinned)

- **Intensification window:** t ∈ [6, 10] — taken from Press I's
  measured dynamics (ε_max at t = 8.90), declared now, before
  Press II data exists. Snapshots in window: 17.
- **Separation, per observable:** the main run's statistic exceeds
  the 95th percentile of its own 100-shuffle ensemble at the same
  snapshot, at **≥ 9 of the 17** in-window snapshots.
- **Snapshot comparison, declared** (Claude's addition, adopted
  2026-11-22): the main run's 17 in-window snapshots are one
  trajectory and are temporally correlated; the shuffles are redrawn
  independently at each snapshot. The ≥ 9-of-17 count is therefore a
  declared decision rule, not a binomial calculation, and its
  operating characteristics are measured by the calibration
  self-test below rather than derived from independence assumptions.
- **Calibration self-test** (Claude's addition, adopted 2026-11-22;
  run and committed before the real run; statistic recomputes only,
  no new integrations):
  - *Null calibration:* each of the 100 shuffles is treated in turn
    as the "real" field, with the remaining 99 as its ensemble, and
    the full separation rule is applied across the in-window
    snapshots. The fraction of shuffles that separate is the rule's
    empirical false-positive rate, and it is reported alongside the
    run's results.
  - *Positive control:* a planted-coherence field with a deliberate
    triadic phase-lock on the O1 triad set (construction declared in
    the self-test script, committed with this preregistration) must
    separate under the full rule. If it does not, the pipeline is
    reviewed before any verdict is read — a rule that cannot fire
    on planted coherence cannot acquit the real field either.
- **Verdicts:**
  - O1 fails → the phase-aware repair fails at N = 128; filed as a
    negative result; the dictionary programme returns to design.
  - O1 passes, O3 fails → triadic coherence is detectable but the
    antipodal entry specifically is refuted — a sharper negative,
    filed as such.
  - O2 is a witness, not a gate: its separation is expected on
    textbook grounds; if O2 *fails* to separate, the run itself is
    suspect (implementation review before any verdict is read).
- **Grades:** STRATA ladder throughout. A pass is a
  reproducible-pattern-grade result *about the dictionary* — it
  shows a phase-aware entry can detect coherent dynamics at this
  resolution. **Navier–Stokes remains `not_tested` under every
  outcome.** Press I's refuted ceiling/log-periodicity claims are
  not revived by any Press II result: they were spectrum-level
  claims and stay refuted.

## 4. Implementation commitments

- Solver: Press I's `tg_press.py` machinery extended in a new file
  (`tg_press2.py`): same integrator, dealiasing, projection, and
  checkpointing; new in-run statistics module for O1–O4 and the
  shuffle ensemble. Triad set precomputed once and frozen to disk
  with its seed before the run.
- The Stage A gate is re-checked on the Press II run's own
  diagnostics (ε_max within the Press I gate) before any Stage C2
  verdict is read; a calibration failure voids the run, not the
  preregistration.
- Runtime estimate (declared, not promised): ~2.5–3 h for the main
  run on the Press I host, statistics overhead included. Checkpoint
  discipline as Press I (the host reboots; the run must resume).
- **Registration:** the outcome — positive, negative, or mixed — is
  registered as OMNIQUASI OQ-EXP-2026-003 and filed with its data,
  under the same pattern as Press I. Failures are retained.

## 5. Decisions — ruled by the maintainer, 2026-11-22

1. **N = 128** for comparability with Press I. (Claude's supporting
   receipt: 128 is not divisible by 3, so the 2/3-rule cutoff is 42
   and the boundary-aliasing of HB-014, which affects N = 24, 48,
   does not apply.)
2. **Window [6, 10] and the ≥ 9-of-17 separation rule** as pinned
   in §3.
3. **M = 100** shuffle ensemble at the **95th percentile** (Claude's
   amendment, accepted in Cosmo's HB-013 response; in-run, cost is
   minutes, not runs).
4. **File before run**, as a PR successor to #134, as with Press I.
   The filing PR is Claude's to open, per his offer of 2026-11-22.
5. **Claude's two additions adopted:** the calibration self-test
   (null calibration + planted-coherence positive control) and the
   snapshot-comparison declaration, both folded into §3.

The fence stands as ruled: **no outcome of Press II upgrades any
claim — Navier–Stokes remains `not_tested` under every outcome.**
Nothing runs until the maintainer's separate go-ahead.

## 6. Filing notes (Claude) — items the draft leaves open, for the maintainer's ruling before the run

Writing the self-test forced these conventions, which the draft text does not fix. The script pins one choice
for each so it can run; none is ruled until the maintainer says so, and a different ruling means changing the
script first. Nothing in Sections 0–5 is altered.

1. **Norm in the triad set (C1).** "|k|, |p|, |q| ≤ 32" read as the Euclidean norm. The alternative, the max-norm (box), gives a different set.
2. **Vector field (C2).** O1/O3 are written for a scalar phase φ(k). û is a 3-vector. Pinned: compute per Cartesian component (amplitude |û_i|, phase arg û_i) and report the mean over i = 1, 2, 3 for C_tri and W.
3. **Shuffle construction (C3).** Pinned: one phase θ_k shared by all three components, Hermitian (θ_{−k} = −θ_k, θ_0 = 0). This keeps |û| exactly and keeps k·û = 0, so shuffled fields are still solenoidal and O2 can be computed on them. Independent per-component phases would break incompressibility.
4. **Percentile and comparison (C4).** numpy linear interpolation; "exceeds" is strict.
5. **Planted-coherence control (C5).** Built at the statistic level (û_i(k) = |û_i(k)| e^{−ik·x₀ + iσg_k}); solenoidality not enforced since O1 reads only amplitudes and phases.
6. **Inactive snapshots (proposed, not in the script's pins).** The draft reads C_tri only where W(t) > 10⁻³ × max W over the window but does not say how an inactive in-window snapshot counts toward the ≥ 9-of-17 rule. Proposed: it counts as **not separating** (conservative).
7. **Window endpoints.** [6, 10] at cadence 0.25 is read as inclusive at both ends (6.00 … 10.00 = 17 snapshots).

**Self-test demo (`press2/selftest_demo.json`, produced by `press2_selftest.py` with defaults).** Pipeline check on *synthetic* random-phase fields (N = 32, |k| ≤ 8, 173,328 triads, M = 100, 17 snapshots, seed 20261122): a shuffle changes |û| by at most 6e-14, leaves the divergence at 2e-16 relative and the field real to 4e-17; the incoherent field does not separate (hit count 1 of 17); the null calibration over 100 shuffles gives a false-positive rate of 0/100 (hit counts 0…4 of 17); the planted-lock field separates at 17 of 17 (mean C_tri 0.25 against 0.008 for its shuffles). **This is a demonstration that the pipeline runs and can fire; it is not a Press II result and says nothing about Navier–Stokes.** The operating characteristics that matter are those measured on the real run's own snapshots, per Section 3.

Registration: the outcome is to be registered as OMNIQUASI OQ-EXP-2026-003 when it exists; no registry row is added by this filing.

*Authored-by: Cosmo (Memory bench) for Sections 0–5; Claude (Anthropic, Architect bench) for the filing note, Section 6, the self-test and its tests.*
