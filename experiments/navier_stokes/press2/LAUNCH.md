# Press II — Launch Pad

The production run of **NS Press II** (OQ-EXP-2026-003), as preregistered in
[`NS_PRESS_II_PREREGISTRATION.md`](../NS_PRESS_II_PREREGISTRATION.md) (PR #169,
ruled by the maintainer 2026-11-22) and implemented in PR #170. This page is
the whole launch in one place: what runs, with what numbers, what to expect,
and how the result is read.

## Gate — satisfied 2026-11-22

The cadence fix (PR #172) is **merged** (merge commit `f8fe7313`). Before it,
the implementation derived its snapshot cadence from fixed step counts, which
at the production dt = 0.005 would have produced 97 snapshots / 33 in-window
instead of the preregistered 49 / 17 and silently weakened the verdict rule.
PR #172 makes the cadences derive from dt. Filed text, code, and run now
match; the launch is cleared.

## Locked parameters

| Parameter | Value | Source |
|---|---|---|
| Grid N | 128 | Preregistration §2 (held from Press I for comparability) |
| Reynolds number | 1600 | Press I configuration |
| Final time T | 12 | Preregistration §2 |
| dt | 0.005 | Preregistration §2 |
| Snapshots | every 0.25 → 49 total, 17 in window t ∈ [6, 10] | §2/§3 |
| Verdict rule | statistic beats the 95th percentile of M = 100 in-run shuffles at ≥ 9 of 17 in-window snapshots | §3 (maintainer's ruling, 2026-11-22) |
| Flagship triads | \|k\|, \|p\|, \|q\| ≤ 32, cap 200,000, seed 20261122 | §3 (O1) |
| Observables | O1 triadic coherence (flagship) · O2 vorticity kurtosis (witness) · O3 antipodal biphase · O4 front K(t) (gauge only) | §3 |

The launcher (`run_press2.sh`, this directory) pins every one of these.
Do not change a number in the script without amending the preregistration.

## Preflight — already done

- **Unit tests:** 11/11 pass (solver + self-test suites).
- **Calibration self-test, run on the run host 2026-11-22:** shuffle exactness
  at roundoff (max amplitude change 5.7e-14); incoherent field does **not**
  separate (1/17 hits); **planted-coherence control separates 17/17**;
  **null false-positive rate 0/100**; triad set 173,328 triads (matches the
  implementer's committed self-test exactly).
- **Dress rehearsal** (N=32, production dt): end-to-end run + analyze; the
  under-resolved rehearsal was correctly voided by the Stage A gate. This
  rehearsal is what caught the cadence deviation above.

## Launch

From the repository root, on a host with Python 3 + NumPy:

```bash
experiments/navier_stokes/press2/run_press2.sh
```

That starts the run detached, logs to
`experiments/navier_stokes/press2/press2_runs/press2_re1600_n128.log`, and
prints the analyze command. `FG=1` runs it in the foreground instead.

- **Checkpoints** are written every 1.0 time units (`<tag>.ckpt.npz`).
  If the host dies, re-running the same command resumes from the last one.
- **Progress** is one log line per checkpoint (`step 200/2400 t=1.00 …`).
  The first checkpoint gives a measured rate; extrapolate the ETA from it.
- **Duration, honestly:** the implementer's 3.5–4 h estimate assumed a faster
  host. On the Memory bench's VM the calibration self-test ran ~2.7× slower
  than on the implementer's host, so budget a long run there (checkpointing
  makes that safe). The maintainer's PC (Ryzen 5600X) is the faster host but
  needs the preflight repeated there first (~15 min: clone, unit tests,
  self-test).

## After the run

```bash
python3 -m experiments.navier_stokes.press2.tg_press2 analyze \
    --out experiments/navier_stokes/press2/press2_runs --tag press2_re1600_n128
```

The analyzer applies the preregistered verdict tree in order: Stage A gate
(under-resolved ⇒ RUN VOID) → O2 witness (failure to separate ⇒ RUN SUSPECT)
→ O1/O3 verdicts against the in-run shuffle nulls, including the null
calibration. The result is filed as a report PR, whatever it says — failures
are retained, per house rule.

Run outputs (checkpoints, logs, the raw results JSON) are working files.
They are **not** committed; the filed report carries the summary and the
numbers that matter.

## The fence

No outcome of this run upgrades any claim. Navier–Stokes remains
`not_tested` under every outcome, including a clean separation. Press II
tests whether a phase-aware statistic can see structure that Press I's
phase-blind statistic could not — nothing more, and that is enough.
