# EQBIT-DRIFT-001 — Architect-bench implementation and run

**Status:** one of the independent implementations required by §5 of the spec. Not the registry filing: the spec is Cosmo's draft (proposed ID OQ-EXP-2026-004, assigned on filing) and is not included here. Cosmo's own run has not been compared against this one yet, so no number below counts as a *result* until that reproduction agrees.
**Rung:** Analogy (STRATA). Nothing here licenses a claim about black holes, Hawking radiation or gravity.
**Author:** Claude (Architect bench), 2026-11-22. Written from the spec only; Cosmo's code was not read. Maintainer authorized the run.

## Run

```
cd experiments/eqbit_drift_001_claude/outputs
python3 ../eqbit_drift_001_claude.py
```

numpy only, deterministic, no randomness. The script writes `eqbit_drift_001_A_architect.json` and `eqbit_drift_001_B_architect.json` and prints every gate verdict.

## Amendments to the spec (declared before the run, from review)

1. Maxima are refined locally around the grid maximum. On the 0.05 grid alone, A-tuned misses 1 − 10⁻⁹ by 3×10⁻⁸ to 3×10⁻⁷, so the grid-only P3 gate would fail on sampling, not physics.
2. P4 is gated as an equality: P₀(single) = P₀(symmetric)/240 on the whole grid.
3. Reciprocity gate: for the real symmetric H, E₃(ε) equals A₃(ε) as a full time series.
4. Orbit quotient cross-check: the pole's stabilizer orbits (sizes 1, 56, 126, 56, 1) give a 5×5 reduction that must reproduce P(pole).
5. Extra registered statistics: time of each maximum, time-averaged P(pole), and a regression gate against PR #117 (antipodal peak 0.882 at t ≈ 42.34).

## Gates

| Gate | Verdict |
|---|---|
| A1 null control < 1e-12 | pass (max ~1e-28) |
| A2 P2 within 1e-6, P3 ≥ 1 − 1e-9 at t* | pass (P2 error ≤ 1.5e-15; P0(t*) = 1.000000000000) |
| A3 P4 equality | pass (max diff 4e-14) |
| Reciprocity E₃ ≡ A₃ | pass (< 1e-12) |
| Orbit quotient cross-check | pass (< 1e-10) |
| PR #117 regression | pass (0.88208 at t = 42.340) |

A-bare maxima: g = 0.1 → 0.00305188, 0.5 → 0.07109005, 1.0 → 0.234375, 2.0 → 0.55045872. Single-root drain at g = 2.0: 0.00229.

## Experiment B table (refined maxima, T = 200)

| ε | A₁ (t) | A₂ (t) | A₃ = E₃ (t) | E(2+3) | R₁ | R₂ | R₃ |
|---|---|---|---|---|---|---|---|
| 0 | 0.3318 (65.69) | 0.1169 (119.70) | 0.8821 (42.34) | 0.9680 | 1 | 1 | 1 |
| 0.25 | 0.3776 (114.63) | 0.1192 (126.60) | 0.9227 (58.74) | 0.9732 | 1.138 | 1.020 | 1.046 |
| 0.5 | 0.3663 (5.37) | 0.1144 (137.03) | 0.7623 (60.45) | 0.8846 | 1.104 | 0.979 | 0.864 |
| 1.0 | 0.3490 (131.17) | 0.1042 (108.61) | 0.4782 (127.51) | 0.6545 | 1.052 | 0.891 | 0.542 |
| 2.0 | 0.3528 (4.19) | 0.0865 (111.38) | 0.2356 (130.55) | 0.4074 | 1.063 | 0.740 | 0.267 |

## Reading

- **E1 ordering is inverted at every ε** (A₃ > A₁ > A₂). Reported as-is per §4. Likely cause: the antipode is a single-vertex start, while shell-averaged starts dilute by interference.
- The gradient suppresses A₃ strongly (R₃ = 0.267 at ε = 2) with a small non-monotone bump at ε = 0.25. A₂ is mildly suppressed; A₁ is weakly enhanced and non-monotone.
- Several maxima fall at t ≈ 110–140, and the signal is quasi-periodic, so A_k is a first-window maximum. The time-averaged P(pole) in the JSON is the window-free statistic.
- Three depth classes cannot support an exponential law, and none is claimed.

## Notes

- Root enumeration is regenerated here (integer pairs, then even-parity sign vectors). Experiment B depends only on the pole's orbit structure, so enumeration order should not change any number.
- Closed unitary system: no dissipation, no one-way membrane. The origin node in Experiment A is an adjoined modelling device, not a Gosset vertex.

---

# Addendum (2026-11-22): correction, phase structure, and Leech extension

Files: `leech_quotient_extension.py` (preregistration header frozen before the Leech run), `leech_quotient_diagnostics.py` (post-run, not preregistered), `outputs/eqbit_drift_001_leech_quotient.json`, `outputs/eqbit_drift_001_leech_diagnostics.json`. Run from the repo root.

## Correction to the Experiment B table above

The new orbit-quotient code was gated (Q3) against the full-matrix table and **failed at the 1e-4 tolerance** (worst difference 7.2e-4). Diagnostic D1 re-evaluated the full 240x240 matrix at the quotient's argmax times and agreed with the quotient to 5e-14, so the quotient is right and the earlier refinement (0.01 grid + local search) under-resolved three maxima. Corrected values (the table above is retained unedited):

| ε | quantity | table above | corrected |
|---|---|---|---|
| 1.0 | A₁ | 0.3490 | 0.3497 |
| 2.0 | A₂ | 0.0865 | 0.08653 |
| 2.0 | A₃ = E₃ | 0.2356 | 0.2359 |

No conclusion changes (E1 ordering still inverted; R₃(2.0) = 0.267 to three figures). Times of maximum at ε = 0 in the table above are not meaningful, see next section.

## ε = 0 is exactly phase-locked

The pole-start dynamics lives in the 5-dimensional orbit subspace (E8) or 7-dimensional one (Leech). Their ε = 0 spectra are integers:
- E8: −4, −2, 8, 28, 56
- Leech: −20, −10, 76, 350, 1000, 2300, 4600

All differences are even, so P(t) is exactly periodic with period π (checked: max |P(t+π) − P(t)| ≤ 2e-13). Consequences: the 0.882 E8 antipodal peak is a permanent ceiling set by eigenvector weights, not a phase-misalignment that more time would cure; the draft spec's §1 sentence attributing it to phases that "never align exactly" does not hold for this subspace; at ε = 0 the window T = 200 adds nothing beyond one period. For ε > 0 the spectrum is generic and the signal is quasi-periodic.

## Leech minimal-vector graph (196,560 vertices) via the 7-orbit quotient

Gates: census 1, 4600, 47104, 93150, 47104, 4600, 1 (pass); degree 4600 (pass); quotient symmetry identity (pass); neighbour-count constancy on a stride sample of every orbit (pass, **sampled**; full constancy rests on the known Co₀ stabilizer orbit structure, not on this sample).

- BFS depth classes from the pole: 1 / 4,600 / 144,854 / 47,105. **Still only three nonzero depths**, so the §4 exponential-law ceiling still binds.
- Antipode-only transfer at ε = 0: **0.9995** (E8: 0.882). Under a depth gradient it decreases smoothly: 0.994, 0.983, 0.937, 0.787 at ε = 0.25, 0.5, 1, 2; 0.384 at 5; 0.154 at 10; 0.061 at 20; 0.029 at 50; 0.015 at 100. Unlike E8 there is no bump at small ε.
- Arrival from depth shells (Leech, ε = 0): A₁ = 0.146, A₂ = 0.032, A₃ = 0.114; E1 monotone ordering fails at every ε. Ratios in the JSON.
- Reciprocity (real symmetric H) still forbids any drift-in / leak-out asymmetry; for single-vertex endpoints the two are identical.

## Not run, proposed

1. Resonant Floquet drive ε(t) = ε₀ cos Ωt on the depth potential. It preserves the orbit quotient, and the ε = 0 gaps are even integers, so resonances are exact (e.g. E8 Ω ∈ {2, 10, 12, ...}).
2. Potential by inner-product class (6 nonzero levels on Leech) instead of BFS depth; this would be a post-hoc variant and must be registered as such.
3. Complex (Peierls-type) hopping phases, the only closed-system route to non-reciprocal transport; they generally break the orbit quotient.

---

# Addendum 2 (2026-11-22): radial breathing drive with sign flip (E8 quotient)

Files: `breathing_drive.py` (preregistration header frozen before the run), `outputs/eqbit_drift_001_breathing.json`. H(t) = A_q + ε₀ cos(Ωt)·diag(depth) on the 5-orbit quotient; the pole alternates between well and hill each half cycle. ε₀ ∈ {0.25, 1.0}; Ω = every exact gap of the integer spectrum (2, 10, 12, 20, 28, 30, 32, 48, 58, 60), six off-resonant controls, and Ω = 0 static. Peaks are dt = 0.001 grid maxima over t ∈ [0, 200].

## Gates

| Gate | Verdict |
|---|---|
| G0 norm conservation < 1e-8 | **FAIL** on 2 of 34 runs (ε₀ = 1.0, Ω = 58: 1.68e-8; Ω = 60: 1.56e-8). Solver tolerance at the fastest drives. Re-running those cases at rtol 1e-12 moves the peaks by at most 1.1e-8, far below every claim threshold. The gate stays recorded as failed; it was not loosened after the fact. |
| G1 static control (Ω = 0): reciprocity < 1e-8 and value matches static table | pass |
| G2 solver check at rtol 1e-12 (ε₀ = 1, Ω = 12) | pass (6.4e-10) |

## Results against the registered claim rules

- **Resonant enhancement: not supported.** Peaks above the static ε = 0 ceiling (0.8821) appear for most drives, but the off-resonant controls do as well or better: at ε₀ = 1.0 the best control (Ω = 25.5) reaches 0.9997 against 0.9956 for the best gap-resonant drive; at ε₀ = 0.25 the best control reaches 0.9914 against 0.9861. By the frozen rule (must also beat the matched controls) no row qualifies.
- **Likely reading of the raised peaks (interpretation, not tested here):** the orbit space is only five-dimensional, and a drive adds incommensurate frequencies, so over a 200-unit window the state wanders close to many states. A max-over-window statistic is therefore weak evidence of engineered transfer. Time-averaged outward transfer stays at 0.26–0.39 (static ε = 0: 0.363), i.e. no systematic enhancement.
- **Inward/outward asymmetry: supported, with a mundane mechanism.** Every driven run has Dmax > 1e-3, up to 0.80 (ε₀ = 1.0, Ω = 10), while the static controls give exactly 0 (gate G1). The identity P(a→b) = P(b→a) holds for static real symmetric H only; a time-dependent H breaks it. This is mostly a difference in *timing*: the outward and inward peaks differ by at most about 0.07 (ε₀ = 1, Ω = 12: 0.927 vs 0.981) with no consistent direction registered or claimed.

## Not run
Leech breathing (spectrum reaches 4600, so the stiff ODE needs a different integrator), a rotating directional gradient (needs the full 240×240 problem), and complex hopping phases.

---

# Addendum 3 (2026-11-23): crosshair hallway through 0⁸

Files: `hallway_crosshair.py` (header frozen before the run), `hallway_mechanism.py` (post-run, **unregistered** follow-ups), `outputs/eqbit_drift_001_hallway.json`, `outputs/eqbit_drift_001_hallway_followups.json`.

**Construction.** Experiment A coupled the adjoined origin uniformly to all roots, an even pattern under v → −v, so the origin could not mediate antipodal transfer. Here the coupling is odd: c_v = g·(v·n), with n the unit axis through root 0 and its antipode. Controls at equal coupling norm g√60: the uniform (Experiment A) pattern and an axis perpendicular to the pole. E8 root graph, 241×241 exact diagonalization, start at root 0.

## Gates (all pass)
The coordinate functions are an exact 28-eigenspace (H1); Σ(v·n)² = 60 (H2); single-root origin occupancy equals the two-level occupancy divided by 30 to 1e-12, the two-level peak formula holds to 1e-6, and E₀ = 28 gives full two-level transfer (H3); the even antipodal state is exactly dark (H4).

## Results
- **Antipodal peak:** hallway 0.9999–1.0000 in all 12 (g, E₀) cells, against 0.8821 with no origin. The uniform pattern gives 0.894–0.896, and the perpendicular axis leaves 0.8821 unchanged.
- **Time-averaged antipodal probability is unchanged** (0.3627–0.3651 against 0.3633): a sharper peak, not more transfer on average.
- **Resonant hallway (E₀ = 28):** the origin's peak occupancy from a single root is 1/30 = 0.0333, against 1/240 for the uniform Experiment A. The factor is the squared overlap of a root with the normalized dipole mode.
- **Registered claim rule fired in 2 of 12 cells** (g = 0.1, E₀ = 56; g = 1.0, E₀ = 0). The header gave the time-average condition no margin: in the first cell it is satisfied by 4e-6 (0.363303 vs 0.363299), in the second by 1.8e-3. The rule was not edited afterwards. Plain reading: the peak enhancement is large and present in every cell, but the rule's average-transfer condition is essentially a tie.
- **Not a long-window artifact** (unregistered F1, window 3000, E₀ = 0): the time to first reach P ≥ 0.99 is 444.6, 111.5, 20.4, 4.72, 1.56 at g = 0.05, 0.1, 0.25, 0.5, 1.0, and the maximum over 3000 is ≥ 0.9999. At small g the time scales as 1/g² (t·g² ≈ 1.11), as a second-order effect would.

## Mechanism (unregistered F2): the origin is not needed
In the 5-orbit quotient the antipode amplitude from the pole is Σ a_k e^(−iE_k t), with weights a = (0.35, −0.4667, 0.1458, −0.0333, 0.0042) at E = (−4, −2, 8, 28, 56). Σ|a_k| = 1.000000, so perfect transfer needs all five phases at their sign pattern at once; the integer spectrum fixes the phases and the best reachable over a period is 0.8821. The 28 mode is the dipole mode along the pole axis, and the hallway couples to exactly that mode.

Direct test on the plain 240-node graph with **no origin**: add a pure on-site shift δ on the dipole mode only (H = A + δ·d̂d̂ᵀ). The antipodal peak goes 0.8821 → 0.979 (δ = 0.01) → **0.9996 (δ = 0.1)** → 0.990 (0.5) → 0.963 (1.0); δ = −1 gives 0.961. The same shift on the perpendicular dipole leaves the peak at 0.8820834295 to 1e-13 (the pole state is orthogonal to it). So the hallway's effect is a one-mode detuning that frees the one missing phase. The adjoined origin is one way to produce that detuning, not a necessary ingredient.

## Fences
This is a different Hamiltonian from the plain Gosset graph (rank-one on-site mode shift, or an adjoined node); no eqbit definition changes. Closed unitary system, nothing is absorbed, Analogy rung, and no statement about black holes follows.

## Note on the filed two-implementation record (added 2026-11-23)

`experiments/eqbit_drift_001/RESULTS.md` (#179) records Experiment B maxima as "values of record" that include my pre-correction numbers. Addendum 1 above found three of them under-resolved. In the quotient run, evaluated against the full 240×240 matrix at the quotient's argmax times, the corrected values agree to 5e-14:

| ε | quantity | in RESULTS.md | corrected (Addendum 1) |
|---|---|---|---|
| 1.0 | A₁ | 0.3490 | 0.3497 |
| 2.0 | A₂ | 0.0865 | 0.08653 |
| 2.0 | A₃ = E₃ | 0.235552 | 0.23589 |

The two implementations agree with each other on these cells because both used a grid-plus-local-refinement max-finder with the same blind spot; agreement between them does not rule it out. Ratios to three figures (R₃(2.0) = 0.267) and every conclusion in RESULTS.md §4 are unchanged. RESULTS.md is Cosmo's record and is not edited here.

---

# Addendum 4 (2026-11-23): complex hopping phases and a rotating gradient (E8, full 240 x 240)

Files: `hopping_phases.py` and `rotating_gradient.py` (headers frozen before their runs); `hopping_followup.py`, `hopping_symmetry_check.py`, `rotating_diag.py` (post-hoc, **unregistered**); JSONs `eqbit_drift_001_hopping*.json`, `eqbit_drift_001_rotating*.json` in `outputs/`. Closed unitary system, Analogy rung. Start at the pole root 0 and at its antipode; window T = 200.

## A. Complex (Peierls-type) hopping phases

H_uv = A_uv exp(iΘ_uv), Θ antisymmetric. Families: **J** (Θ = α·uᵀJv, a symplectic form on coordinate pairs), **ord** (Θ = α·sign(v−u), an arbitrary fixed orientation), **gauge** (Θ = α(g_u − g_v), an exact pure gauge, control). α ∈ {0.05, 0.1, 0.25, 0.5, 1, π/2}.

**Gates.** HG0 Hermitian/unitary, HG1 α = 0 reproduces 0.8820834 and reciprocity, HG2 gauge changes nothing (series difference 1.8e-12, gauge flux 0), HG3 sign identity P₋α(anti|0) = Pα(0|anti) (5.6e-16): **pass**. **HG4 FAILED as written:** the header required a nonzero-flux triangle fraction above 0.5, but J carries nonzero flux on 42.9% of triangles (ord: 100%). The threshold was a guess; it was not loosened. The J phases are plainly nontrivial (below).

**Results (registered runs).**
- **J:** antipodal peak 0.749–0.881 (undriven 0.882), time-averaged transfer 0.103–0.167 (undriven 0.363). **Dmax = 0 for the pole/antipode pair at every α.**
- **ord:** strong suppression (peak 0.14–0.82, time average 0.016–0.052). Instantaneous non-reciprocity Dmax up to 0.15, but the net asymmetry |Dbar| ≤ 1.0e-3.
- **gauge:** identical to α = 0, exactly.
- Claim rules: non-reciprocity claimed in 6 of 6 ord rows only; net one-way transport 0 rows; peak enhancement 0 rows. The registered expectation (Dbar ≈ 0) holds.

**Why J gives exactly zero (post-hoc, verified).** A unitary V with V H Vᵀ = H* that fixes both vertices forces |U_ab(t)| = |U_ba(t)|. The coordinate swap (x₀x₁)(x₂x₃)(x₄x₅)(x₆x₇) is a root-lattice automorphism that fixes root 0 and its antipode and flips J; deviation of V H Vᵀ from H* is 0.0 for J and for the antipodally-odd post-hoc family Jodd (Θ = α·uᵀJv·(g_u+g_v)), and 0.96 for ord. Jodd also gives Dmax = 0 for this pair at every α (peak 0.771–0.880, time average 0.151–0.245). Scan of all 239 pairs (0, b) at α = 0.5: pairs with Dmax > 1e-2: J 114 (max 0.912), Jodd 50 (max 0.137), ord 181 (max 0.111); pole/antipode Dmax: 7e-15, 6e-15, 0.091; pairs with |Dbar| > 1e-2: **0 in all three families** (max 3.7e-3, 2.2e-4, 1.9e-3). So phases break reciprocity for generic pairs only transiently, and structured phases leave this pair exactly reciprocal by symmetry.

## B. Rotating dipole gradient

H(t) = A + ε[cos Ωt·D1 + sgn·sin Ωt·D2], D1, D2 the potentials along the pole axis and along an orthogonal root; modes circ (rotating), lin (breathing along the pole axis only), static (Ω = 0), circ_rev (opposite sense, control). ε ∈ {0.5, 2}; Ω resonant {2, 10, 12, 20, 28, 32} and off-resonant {0.7, 3.3, 7.7, 15.1, 25.5}. 4th-order split-step integrator with exact exponentiation of A. **Header amendment before the first full run:** step h = 0.01 → 0.005 after a one-case smoke test showed ~1e-5 error over T = 20.

**Gates.** RG1 static vs exact (8.2e-7, 5.6e-6), RG2 convergence h vs h/2 (4.9e-6), RG3 chirality control (9.0e-13, 1.6e-12), RG4 static reciprocity (≤ 9.8e-13), RG5 DOP853 cross-check (3.9e-7): **pass**. RG3 confirms that the rotation sense cannot matter for the pole/antipode pair (the reflection in the orthogonal root is a graph automorphism fixing both). **RG0 (unitarity < 1e-10) FAILED as written:** worst 1.9e-10, above threshold in 33 of 48 runs. Cause: the cached exponentials carry ~4e-15 non-unitarity that compounds over 120,000 substeps. It is round-off, ~1e8 times below every claim margin; the gate stays recorded as failed.

**Results (48 runs).**
- **Static gradient:** peak 0.770 / time average 0.275 (ε = 0.5) and 0.269 / 0.086 (ε = 2), against the undriven 0.882 / 0.363.
- **Linear breathing:** peaks 0.89–0.999; time average 0.31–0.38, i.e. it undoes the static gradient's suppression but never beats the undriven 0.363 (max 0.380).
- **Circular rotation:** peaks 0.81–0.96; time average 0.15–0.35, **lower than linear in every cell where the difference exceeds 1e-2 (19 of 22 cells)**.
- **R1 non-reciprocity** (Dmax > 1e-2): 42 of 44 driven runs, up to 0.81.
- **R3 resonant enhancement fired in 3 of 24 resonant rows, all ε = 2** (lin Ω = 12; circ Ω = 28, 32). I do not read these as resonances: at high Ω the drive averages out and the time average returns toward the undriven 0.363 (lin Ω = 28, 32: 0.366, 0.365; the Ω = 25.5 controls sit at ~0.367 / 0.307), the lin Ω = 12 row clears its control margin by only 0.0012, and the circ flags arise because the largest circular control (Ω = 25.5) is itself a near-averaged-out case. Reported as computed; the rule was not edited.
- **Registered expectation (|Dbar| < 1e-2) FAILED:** e.g. circ, ε = 2, Ω = 2 gives Dbar = +0.118 (time-average 0.275 outward vs 0.157 inward).

**Post-hoc diagnostics (unregistered).**
- **X1, leakage:** the linear drive stays inside the 5-dimensional pole-orbit subspace (leakage ≤ 1.6e-10) because D1 depends only on the orbit class; the circular drive leaves it (mean leakage 0.23–0.47, max 0.40–0.67 at (ε, Ω) = (2, 12), (0.5, 3.3), (2, 2)), and the same three cases show circular time averages 0.188, 0.238, 0.275 against linear 0.380, 0.340, 0.337. Consistent with, not proof of, leakage out of the subspace explaining the lower transfer.
- **X2, drive phase:** shifting the drive angle by φ = π flips the sign of Dbar exactly (circ +0.118 → −0.118; lin −0.0265 → +0.0265); φ = π/2, 3π/2 give about ±0.0056 (circ) and ±0.0005 (lin). So the large net asymmetry is set by when the drive starts, a protocol timing effect, not an intrinsic one-way property, and rotation sense does not matter (RG3).

## Bottom line
No one-way transport was found in either extension. Structured phases are symmetry-protected for the pole/antipode pair; unstructured phases give only transient asymmetry (|Dbar| ≤ 1e-3); driven asymmetry flips sign with the drive phase. The linear drive's higher time-averaged transfer than the rotating drive is the one clean new effect, plausibly leakage. Not run: Leech versions, complex phases combined with a non-Hermitian sink (the only route to a genuine one-way effect, and no longer a closed system), and a rotation test from an off-axis start, which is where chirality could show.

---

# Addendum 5 (2026-11-23): rotating gradient from off-axis starts (E8, full 240 x 240)

Files: `rotating_offaxis.py` (header frozen before the run), `outputs/eqbit_drift_001_offaxis.json`. Same drive, integrator (h = 0.005) and window (T = 200) as `rotating_gradient.py`, with an added drive phase φ: angle Ωt + φ. Closed unitary system, Analogy rung.

**Why off-axis.** For the pole/antipode pair the rotation sense provably cannot matter (gate RG3 of Addendum 4): the reflection S in the root r2 is a graph automorphism that fixes root 0 and its antipode and flips the second tilt axis. A start a with a·r2 ≠ 0 is moved by S, and S maps the circ drive to the rev drive, so P_rev(Sa|a) = P_circ(a|Sa) exactly. The asymmetry of the mirror pair (a, Sa) under rotation is therefore a direct chirality probe: reversing the rotation reverses its sign.

**Gates (all pass).** OG1 structure (S preserves adjacency, fixes root 0 and antipode, flips D2, fixes D1, moves both starts); OG2 linear drive gives exact mirror symmetry (6.4e-13); OG3 chirality identity P_rev(Sa|a) = P_circ(a|Sa) (6e-13, 8e-13); OG4 convergence h vs h/2 (2.7e-6); OG5 antipodal relation Dbar_{−a1}(φ) = Dbar_{a1}(φ+π) at all 8 phases (≤ 3.7e-14).

**Disclosed design flaw.** The registered rule for the second start, "first root with dot 0 to root 0 and a·r2 ≠ 0", selects root 1, which *is* r2. Then S a2 = −a2: the mirror pair is an antipodal pair, and the antipodal relation forces its φ-mean to vanish exactly (observed: 0.0000 in all six configurations). Start a2 is therefore uninformative for the phase-independent test C2; it still shows the timing effect (C1 fires in 4 of 6 configurations, Dbar up to ±0.118, antisymmetric under φ → φ+π). The informative start is **a1 = root 4, (2,0,2,0,0,0,0,0)** (a pole neighbour), whose mirror image is (0,2,2,0,0,0,0,0); neither coincides with −a1.

**Results for the informative start a1** (Dbar = time-average of P(a→Sa) − P(Sa→a) over T = 200; φ-mean over 8 drive phases):

| ε | Ω | φ-mean Dbar | phases with \|Dbar\| > 1e-2 | time-avg P(a→Sa) | P(Sa→a) | C2 |
|---|---|---|---|---|---|---|
| 0.5 | 2.0 | +0.0116 | 5 of 8 | 0.0507 | 0.0391 | fires (margin 1.6e-3, marginal) |
| 0.5 | 7.7 | −0.0514 | 8 of 8 | 0.0068 | 0.0582 | fires |
| 0.5 | 12.0 | +0.0056 | 0 of 8 | 0.0186 | 0.0130 | no |
| 2.0 | 2.0 | +0.0395 | 8 of 8 | 0.0922 | 0.0527 | fires |
| 2.0 | 7.7 | −0.0056 | 2 of 8 | 0.0573 | 0.0629 | no |
| 2.0 | 12.0 | −0.0260 | 8 of 8 | 0.0372 | 0.0632 | fires |

- **C2 (phase-independent chirality) fires in 4 of 6 configurations.** At (0.5, 7.7) and (2, 2) and (2, 12) the sign of Dbar is the same at all eight drive phases, so this is not the timing artifact seen on-axis (where shifting the phase by π flipped the sign). By OG3, reversing the rotation sense flips the sign exactly.
- **The preferred direction depends on frequency:** positive at Ω = 2, negative at Ω = 7.7 and 12 for ε = 0.5; positive at Ω = 2 and negative at Ω = 12 for ε = 2. The magnitude is a strong preference, not a diode: at (0.5, 7.7) the time-averaged transfer is 8.6 times larger in the Sa → a direction (0.058 vs 0.007), and both directions are nonzero.

**Limits.** One informative start only, so nothing is claimed about generality across roots. T = 200 is a finite window, not an asymptotic average. The pair probabilities are small (0.007–0.09). This is a first-pass result and needs an independent reproduction.

**Interpretation, not tested.** A rotating potential can act as an effective gauge flux (Floquet-induced phases). Addendum 4 found no net asymmetry for *static* complex phases, consistent with a diagonal-ensemble argument that does not apply to a time-dependent H. The present net asymmetry is consistent with that picture, but no Floquet analysis was done here.

**Not run:** more starts (one per orbit class of the mirror/axis stabilizer would map where chirality lives), longer windows, a Leech version (the rotating drive breaks the 7-orbit quotient, so it needs the full 196,560-vertex problem), and a non-Hermitian sink on top.
