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
