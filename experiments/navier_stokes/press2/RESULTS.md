# NS Press II — Results (2026-11-23)

> **Provenance (repo filing):** Results of the preregistered NS Press II
> (preregistration: `experiments/navier_stokes/NS_PRESS_II_PREREGISTRATION.md`,
> OS PR #169, merged 2026-11-22; implementation OS PR #170; cadence fix
> OS PR #172; launch pad OS PR #174). Run and analysis by Cosmo (Memory
> bench) on the maintainer's host; filed at the maintainer's explicit
> direction, 2026-11-23, together with the OMNIQUASI registration
> OQ-EXP-2026-003. Run data and the analysis summary are filed beside
> this note (`press2_re1600_n128.json`,
> `press2_re1600_n128_analysis.json`).

Run: Taylor–Green, N = 128, ν = 1/1600 (Re 1600), T = 12, dt = 0.005,
2400 steps. Controls are in-run: at every statistics snapshot the live
field is phase-shuffled M = 100 times (Hermitian-symmetric, spectrum
preserved exactly, seeds 20261122 + i) and every observable is
recomputed on each shuffle. Window t ∈ [6, 10], snapshots every 0.25
(49 total, 17 in-window); separation = the real observable beats the
ensemble 95th percentile at ≥ 9 of 17 in-window snapshots. Conventions
C1–C8 as preregistered (C6–C8 ratified by the maintainer 2026-11-22).

## Verdict — NEGATIVE RESULT (per the preregistration's own rule)

**O1 fails: the phase-aware repair fails at N = 128.**

| Check | Result | Detail |
|---|---|---|
| Stage A (solver honesty, inherited gate) | **PASS** | eps_max 0.0138 at t = 8.925, ratio 1.070 vs the pinned reference |
| O1 triadic phase coherence (flagship) | **FAILS** | 1/17 hits (≥ 9 required); real mean 0.3189 vs shuffle mean 0.3414 |
| O3 antipodal biphase | **FAILS** | 0/17 hits; real mean 0.00695 vs shuffle mean 0.01041 |
| O2 vorticity kurtosis (witness, not a gate) | separates 17/17 | real mean 14.88 vs shuffle mean 3.00 |

Null false-positive rate 0.0 on all three observables: the gates are
calibrated, and the calibration self-test (planted control separates
17/17) passed before the run. The real run simply does not beat the
phase-shuffled null — on O1 and O3 the real means sit *below* their
shuffle means.

## Reading

The run was live and honest: Stage A passed, and O2 confirms the field
is strongly non-Gaussian (genuinely turbulent). The negative is a
measurement, not a dead run: at N = 128, Re = 1600, neither triadic
phase coherence nor the antipodal biphase carries signal above a
phase-shuffled control of the same field at the same instant. This is
the same shape as Press I's Stage C negative — there the statistic was
phase-blind by construction; here the statistics are phase-aware by
construction and still do not separate at this rung.

**Fence (maintainer-ruled): no outcome upgrades any claim.
Navier–Stokes remains `not_tested` under every outcome.**

## Run record

Launched 2026-11-22 21:16 CST. The host VM rebooted three times during
the run (fifth, sixth, and seventh reboots of the host's recent
history); each time the run resumed from its checkpoint exactly, with
no steps lost:

- Died ~23:23 CST at step 1000/2400 (checkpoint intact); relaunched
  ~01:02 CST.
- Died ~01:17 CST before the next checkpoint; relaunched ~01:34 CST.
- Died ~03:13 CST at step 1800/2400 (checkpoint intact); relaunched
  ~03:33 CST.
- **Landed 04:38 CST** — step 2400/2400, t = 12.00. An eighth reboot
  ~05:13 CST, after the landing, left all artifacts intact (verified).

Analysis (`tg_press2.py analyze`) was run twice on the filed data with
identical output; the summary is filed as
`press2_re1600_n128_analysis.json`.

## Next steps (maintainer's call)

Whether a Press III is worth designing — a different observable, not
merely higher resolution, per the preregistration's declared ladder —
is the maintainer's decision. Nothing in this filing authorizes one.
