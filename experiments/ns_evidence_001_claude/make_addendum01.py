#!/usr/bin/env python3
"""Render ADDENDUM_01.md from outputs/addendum01_results.json (numbers are read, not typed)."""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, "outputs", "addendum01_results.json")))


def e(x):
    return "%.2e" % x


L = []
w = L.append
M, C, O = R["machinery"], R["consistency"], R["order"]

w("# NS-EVIDENCE-001 - Addendum 01: manufactured-solution test of forced Navier-Stokes (Claude bench)")
w("")
w("*Dated 2026-11-21. Addendum to `REPORT.md`, which stays frozen. Verification exercise only: **no claim of global "
  "regularity, blow-up, or a solution of the Clay problem.***")
w("")
w("## 1. Why this test")
w("")
w("`REPORT.md` (section 6) flagged that the 2D Taylor-Green case never exercises the nonlinear term. That can now be "
  "stated quantitatively: the projected nonlinear term of the 2D Taylor-Green field is %s of the state, against %s for the 3D "
  "field. The 2D case therefore checks only viscous decay, projection and bookkeeping. This addendum closes that gap with a "
  "problem whose exact solution is known **and** whose nonlinear term is genuinely non-zero: projected nonlinear term / state "
  "= %s (2D) and %s (3D) for the solution below. It also addresses the board's listed control, *manufactured solutions where "
  "applicable* (`research/omniquasi/boards/NAVIER_STOKES.md`), and is a harness-correctness check that sits before the "
  "benchmark stages of `experiments/navier_stokes/ns-truly-testing-plan.md`. It earns no rung by itself; assigning one is "
  "Lucas's call."
  % (e(C["2D_TaylorGreen_projected_nonlinear_over_state"]), "%.2f" % C["3D_TaylorGreen_projected_nonlinear_over_state"],
     "%.2f" % C["2D_MMS_projected_nonlinear_over_state"], "%.2f" % C["3D_MMS_projected_nonlinear_over_state"]))
w("")
w("## 2. Construction")
w("")
w("Exact solution `u_m(x,t) = a(t) u0(x)` with `a(t) = 1 + 0.5 sin(2t)` and `div u0 = 0`; `u0` is built from a stream function "
  "(2D, `u = (psi_y, -psi_x)`) or a vector potential (3D, `u = curl A`) of a few trigonometric modes with `|k_i| <= 2`. "
  "The forcing that makes `u_m` exact is\n\n"
  "`P f = a'(t) u0 + a(t)^2 P[(u0 . grad) u0] - nu a(t) Lap(u0)`,  nu = 0.01, T = 1.")
w("")
w("**Independence.** The forcing is assembled from *analytic* derivatives (an exact cosine-sum class: "
  "`d/dx_i cos(k.x + p) = k_i cos(k.x + p + pi/2)`), not from the solver's FFT operators. The frozen solver core "
  "(`ns_spectral.PeriodicNS`, unchanged) is reused; only a stage-time forcing wrapper lives in `ns_mms.py`. Checks of the "
  "machinery that do not involve the time stepper: analytic derivatives vs central differences, max abs difference %s (2D) / %s (3D); "
  "analytic Laplacian vs second differences %s / %s; analytic divergence %s / %s; 2D stream function vs closed form %s. "
  "**The analytic advection term and the solver's FFT advection term agree pointwise to a relative %s (2D) and %s (3D)** - "
  "an operator-level check of the solver's nonlinear term against an independent derivation."
  % (e(M["2D_derivative_vs_central_difference_max_abs"]), e(M["3D_derivative_vs_central_difference_max_abs"]),
     e(M["2D_laplacian_vs_second_difference_max_abs"]), e(M["3D_laplacian_vs_second_difference_max_abs"]),
     e(M["2D_analytic_divergence_max_abs"]), e(M["3D_analytic_divergence_max_abs"]), e(M["2D_psi_vs_closed_form_max_abs"]),
     e(C["2D_analytic_vs_fft_advection_rel"]), e(C["3D_analytic_vs_fft_advection_rel"])))
w("")
w("Disclosure: my first machinery run used a second-difference step of 1e-5 and reported a Laplacian discrepancy of 1.4e-5, "
  "which is finite-difference roundoff (about eps/h^2), not a defect; I changed the step to 1e-3 *before* the full run. "
  "Both mode sets keep every product at `|k_i| <= 4`, below the N >= 16 dealiasing cutoff of 5, so aliasing plays no role: "
  "the semi-discrete problem has `u_m` as its exact solution and the observed error is time-integration error plus roundoff.")
w("")
w("## 3. Results: temporal convergence")
w("")
w("Relative L2 error of the spectral coefficients at T = 1 (Lawson-RK4, forcing evaluated at stage times).")
w("")
dts = O["2D_N16"]["dt"]
w("| case | " + " | ".join("dt=%g" % d for d in dts) + " |")
w("|--|" + "--:|" * len(dts))
for k, v in O.items():
    w("| %s | " % k.replace("_", " ") + " | ".join(e(x) for x in v["rel_l2_error"]) + " |")
w("")
w("Observed order between successive halvings (every case): "
  + "; ".join("%s: %s" % (k.replace("_", " "), v["observed_order"]) for k, v in O.items()) + ".")
w("")
w("This is clean **4th order down to ~%s**, in both dimensions, with the nonlinear term active. The error is the same for "
  "N = 24 and N = 32 to three digits, i.e. spatially converged." % e(min(v["rel_l2_error"][-1] for v in O.values())))
w("")
w("**Open observation (not explained).** At coarse dt the N = 16 error is slightly *larger* than at N >= 24 (at dt = 0.1 the "
  "N16/N24 ratio is %.4f in 2D and %.4f in 3D). My first hypothesis was that the N = 16 cutoff truncates high-mode error; that "
  "predicts the opposite sign (ratio %.4f and %.4f, from the error-energy fraction %.4f and %.4f above the cutoff), so it is "
  "**rejected**. The effect is at the 0.3%%-2.5%% level, does not change the order or any conclusion, and I have not identified "
  "its cause. It is reproducible (`n16_truncation_check` in the results file)."
  % (R["n16_truncation_check"]["2D"]["measured_ratio_N16_over_N24"], R["n16_truncation_check"]["3D"]["measured_ratio_N16_over_N24"],
     R["n16_truncation_check"]["2D"]["H1_predicted_ratio_N16_over_N24"], R["n16_truncation_check"]["3D"]["H1_predicted_ratio_N16_over_N24"],
     R["n16_truncation_check"]["2D"]["error_energy_fraction_above_N16_cutoff"], R["n16_truncation_check"]["3D"]["error_energy_fraction_above_N16_cutoff"]))
w("")
w("## 4. Negative controls: does the test have teeth?")
w("")
w("Same run (N = 24, dt = 0.00625, T = 1) with one deliberate defect at a time.")
w("")
w("| d | variant | relative L2 error | vs correct solver |")
w("|--:|--|--:|--:|")
base = {}
for c in R["negative_controls"]:
    if c["control"] == "correct solver":
        base[c["d"]] = c["rel_l2_error"]
for c in R["negative_controls"]:
    w("| %d | %s | %s | %s |" % (c["d"], c["control"], e(c["rel_l2_error"]),
                                 "-" if c["control"] == "correct solver" else "x%s" % ("%.1e" % (c["rel_l2_error"] / base[c["d"]]))))
w("")
w("Dropping or sign-flipping the nonlinear term, or flipping the forcing, gives O(1) errors; a 10% viscosity error is still "
  "detected at ~3e-3. A defect in the nonlinear term would go unseen by the 2D Taylor-Green benchmark, because that term vanishes "
  "there.")
w("")
w("## 5. Limits")
w("")
w("- **Scope of what is verified:** *my* solver, against analytic truth. It does not validate the OpenAI or Cosmo implementations; "
  "doing that means running them on this same problem (`fields()`, `a_of()` and the forcing formula in `ns_mms.py` are small and "
  "self-contained for that purpose). I have not read Cosmo's implementation or report for this addendum.")
w("- **Dealiasing is untested here** by construction (no aliasing arises). **Energy balance is untested**: the forced problem does "
  "not conserve the unforced budget.")
w("- The solution is smooth, low-mode and non-turbulent (nu = 0.01, O(1) amplitude, T = 1). It does not probe under-resolved, "
  "cascading, or near-singular regimes; that is the job of the Brachet-lineage stage in the testing plan.")
w("- Same method family as the earlier benchmarks (Fourier pseudo-spectral, 2/3 rule, RK4). A second family is still outstanding.")
w("- Nothing here bears on regularity, blow-up, or the Clay problem.")
w("")
w("## 6. Reproduction")
w("")
w("```")
w("python3 -I ns_mms.py            # writes outputs/addendum01_results.json (deterministic; rerun was bit-identical)")
w("python3 -I make_addendum01.py   # writes this file")
w("```")
w("")
w("Files: `ns_mms.py`, `make_addendum01.py`, `outputs/addendum01_results.json`. The solver core `ns_spectral.py` is unchanged. "
  "Authored by Claude (Anthropic), Architect bench.")
w("")
open(os.path.join(HERE, "ADDENDUM_01.md"), "w").write("\n".join(L))
print("wrote ADDENDUM_01.md (%d lines)" % len(L))
