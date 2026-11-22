# NS-EVIDENCE-001 - Addendum 01: manufactured-solution test of forced Navier-Stokes (Claude bench)

*Dated 2026-11-21. Addendum to `REPORT.md`, which stays frozen. Verification exercise only: **no claim of global regularity, blow-up, or a solution of the Clay problem.***

## 1. Why this test

`REPORT.md` (section 6) flagged that the 2D Taylor-Green case never exercises the nonlinear term. That can now be stated quantitatively: the projected nonlinear term of the 2D Taylor-Green field is 3.46e-16 of the state, against 0.25 for the 3D field. The 2D case therefore checks only viscous decay, projection and bookkeeping. This addendum closes that gap with a problem whose exact solution is known **and** whose nonlinear term is genuinely non-zero: projected nonlinear term / state = 0.75 (2D) and 0.45 (3D) for the solution below. It also addresses the board's listed control, *manufactured solutions where applicable* (`research/omniquasi/boards/NAVIER_STOKES.md`), and is a harness-correctness check that sits before the benchmark stages of `experiments/navier_stokes/ns-truly-testing-plan.md`. It earns no rung by itself; assigning one is Lucas's call.

## 2. Construction

Exact solution `u_m(x,t) = a(t) u0(x)` with `a(t) = 1 + 0.5 sin(2t)` and `div u0 = 0`; `u0` is built from a stream function (2D, `u = (psi_y, -psi_x)`) or a vector potential (3D, `u = curl A`) of a few trigonometric modes with `|k_i| <= 2`. The forcing that makes `u_m` exact is

`P f = a'(t) u0 + a(t)^2 P[(u0 . grad) u0] - nu a(t) Lap(u0)`,  nu = 0.01, T = 1.

**Independence.** The forcing is assembled from *analytic* derivatives (an exact cosine-sum class: `d/dx_i cos(k.x + p) = k_i cos(k.x + p + pi/2)`), not from the solver's FFT operators. The frozen solver core (`ns_spectral.PeriodicNS`, unchanged) is reused; only a stage-time forcing wrapper lives in `ns_mms.py`. Checks of the machinery that do not involve the time stepper: analytic derivatives vs central differences, max abs difference 1.34e-10 (2D) / 8.21e-11 (3D); analytic Laplacian vs second differences 1.40e-06 / 4.97e-07; analytic divergence 0.00e+00 / 1.11e-16; 2D stream function vs closed form 6.11e-16. **The analytic advection term and the solver's FFT advection term agree pointwise to a relative 6.96e-16 (2D) and 6.13e-16 (3D)** - an operator-level check of the solver's nonlinear term against an independent derivation.

Disclosure: my first machinery run used a second-difference step of 1e-5 and reported a Laplacian discrepancy of 1.4e-5, which is finite-difference roundoff (about eps/h^2), not a defect; I changed the step to 1e-3 *before* the full run. Both mode sets keep every product at `|k_i| <= 4`, below the N >= 16 dealiasing cutoff of 5, so aliasing plays no role: the semi-discrete problem has `u_m` as its exact solution and the observed error is time-integration error plus roundoff.

## 3. Results: temporal convergence

Relative L2 error of the spectral coefficients at T = 1 (Lawson-RK4, forcing evaluated at stage times).

| case | dt=0.1 | dt=0.05 | dt=0.025 | dt=0.0125 | dt=0.00625 | dt=0.003125 |
|--|--:|--:|--:|--:|--:|--:|
| 2D N16 | 2.67e-06 | 1.68e-07 | 1.06e-08 | 6.61e-10 | 4.13e-11 | 2.59e-12 |
| 2D N24 | 2.61e-06 | 1.64e-07 | 1.03e-08 | 6.42e-10 | 4.02e-11 | 2.51e-12 |
| 2D N32 | 2.61e-06 | 1.64e-07 | 1.03e-08 | 6.43e-10 | 4.02e-11 | 2.51e-12 |
| 3D N16 | 5.89e-06 | 3.70e-07 | 2.32e-08 | 1.45e-09 | 9.10e-11 | 5.69e-12 |
| 3D N24 | 5.88e-06 | 3.69e-07 | 2.32e-08 | 1.45e-09 | 9.07e-11 | 5.67e-12 |
| 3D N32 | 5.88e-06 | 3.69e-07 | 2.32e-08 | 1.45e-09 | 9.07e-11 | 5.67e-12 |

Observed order between successive halvings (every case): 2D N16: [3.99, 3.99, 4.0, 4.0, 4.0]; 2D N24: [3.99, 4.0, 4.0, 4.0, 4.0]; 2D N32: [3.99, 4.0, 4.0, 4.0, 4.0]; 3D N16: [3.99, 4.0, 4.0, 4.0, 4.0]; 3D N24: [3.99, 4.0, 4.0, 4.0, 4.0]; 3D N32: [3.99, 4.0, 4.0, 4.0, 4.0].

This is clean **4th order down to ~2.51e-12**, in both dimensions, with the nonlinear term active. The error is the same for N = 24 and N = 32 to three digits, i.e. spatially converged.

**Open observation (not explained).** At coarse dt the N = 16 error is slightly *larger* than at N >= 24 (at dt = 0.1 the N16/N24 ratio is 1.0250 in 2D and 1.0030 in 3D). My first hypothesis was that the N = 16 cutoff truncates high-mode error; that predicts the opposite sign (ratio 0.9962 and 0.9969, from the error-energy fraction 0.0076 and 0.0061 above the cutoff), so it is **rejected**. The effect is at the 0.3%-2.5% level, does not change the order or any conclusion, and I have not identified its cause. It is reproducible (`n16_truncation_check` in the results file).

## 4. Negative controls: does the test have teeth?

Same run (N = 24, dt = 0.00625, T = 1) with one deliberate defect at a time.

| d | variant | relative L2 error | vs correct solver |
|--:|--|--:|--:|
| 2 | correct solver | 4.02e-11 | - |
| 2 | nonlinear term disabled | 6.29e-01 | x1.6e+10 |
| 2 | nonlinear term sign flipped | 1.14e+00 | x2.8e+10 |
| 2 | viscosity off by 10% in solver (0.011 vs forcing 0.01) | 3.18e-03 | x7.9e+07 |
| 2 | forcing sign flipped | 1.06e+00 | x2.6e+10 |
| 3 | correct solver | 9.07e-11 | - |
| 3 | nonlinear term disabled | 7.12e-01 | x7.8e+09 |
| 3 | nonlinear term sign flipped | 1.22e+00 | x1.3e+10 |
| 3 | viscosity off by 10% in solver (0.011 vs forcing 0.01) | 2.46e-03 | x2.7e+07 |
| 3 | forcing sign flipped | 1.13e+00 | x1.2e+10 |

Dropping or sign-flipping the nonlinear term, or flipping the forcing, gives O(1) errors; a 10% viscosity error is still detected at ~3e-3. A defect in the nonlinear term would go unseen by the 2D Taylor-Green benchmark, because that term vanishes there.

## 5. Limits

- **Scope of what is verified:** *my* solver, against analytic truth. It does not validate the OpenAI or Cosmo implementations; doing that means running them on this same problem (`fields()`, `a_of()` and the forcing formula in `ns_mms.py` are small and self-contained for that purpose). I have not read Cosmo's implementation or report for this addendum.
- **Dealiasing is untested here** by construction (no aliasing arises). **Energy balance is untested**: the forced problem does not conserve the unforced budget.
- The solution is smooth, low-mode and non-turbulent (nu = 0.01, O(1) amplitude, T = 1). It does not probe under-resolved, cascading, or near-singular regimes; that is the job of the Brachet-lineage stage in the testing plan.
- Same method family as the earlier benchmarks (Fourier pseudo-spectral, 2/3 rule, RK4). A second family is still outstanding.
- Nothing here bears on regularity, blow-up, or the Clay problem.

## 6. Reproduction

```
python3 -I ns_mms.py            # writes outputs/addendum01_results.json (deterministic; rerun was bit-identical)
python3 -I make_addendum01.py   # writes this file
```

Files: `ns_mms.py`, `make_addendum01.py`, `outputs/addendum01_results.json`. The solver core `ns_spectral.py` is unchanged. Authored by Claude (Anthropic), Architect bench.
