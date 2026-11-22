"""Stage C control analysis — identical machinery to stage_c_analysis.py,
applied to a control run's saved spectra (Amendment 1).

Usage: python3 stage_c_controls.py <results.json> <out.json>

Declared before running (2026-11-21, before the baseline landed):
- K(t), ceiling fit, and periodicity scan use the SAME definitions as
  the main-run analysis: front = smallest k with energy in shells > k
  below 1e-3 of total; ceiling interval t in [4, t(eps_max)] of THIS
  run; saturating vs no-ceiling RMS ratio; scan of the winning model's
  residuals vs log t at the same pinned candidates.
- If t(eps_max) < 4 the preregistered intensification interval does
  not exist for this run: the ceiling test is reported NOT APPLICABLE
  and the K series is reported raw (the control's job is to show the
  machinery does not manufacture an intensification that is not there).
- Separation (Amendment 1): the main run's per-candidate amp/resid_std
  must exceed the control's statistic at the same candidate and the
  control's global best. With a single shuffle realization this is a
  point comparison, not an ensemble 95th percentile; the verdict text
  must carry that caveat.
"""
import json
import sys
import numpy as np

DATA, OUT = sys.argv[1], sys.argv[2]
d = json.load(open(DATA))
h = d["hist"]
spec_t = np.array(d["spectra"]["t"])
spec_E = [np.array(e) for e in d["spectra"]["E_shell"]]

K = []
for E in spec_E:
    total = E.sum()
    csum = np.cumsum(E)
    above = total - csum
    below = np.where(above < 1e-3 * total)[0]
    K.append(int(below[0]) if len(below) else int(len(E) - 1))
K = np.array(K, dtype=float)
print(f"tag={d['tag']}  K series: {K.astype(int).tolist()}")

ie = int(np.argmax(h["eps"]))
eps_max, t_eps = float(h["eps"][ie]), float(h["t"][ie])
t_arr = np.array(h["t"])
w_arr = np.array(h["wmax"])
m10 = t_arr <= 10.0
bkm = float(np.trapz(w_arr[m10], t_arr[m10]))
print(f"eps_max={eps_max:.6f} at t={t_eps}; BKM(0..10)={bkm:.2f}; "
      f"wmax_peak={w_arr.max():.2f}; Om_peak={max(h['Om']):.3f}")

out = {"tag": d["tag"], "nu": d["nu"],
       "eps_max": eps_max, "t_eps": t_eps, "bkm_int_0_10": bkm,
       "K_series": {"t": spec_t.tolist(), "K": K.astype(int).tolist()},
       "K_max": int(K.max())}

if t_eps < 4.0:
    out["ceiling_test"] = {"verdict": "NOT APPLICABLE",
                           "reason": f"t(eps_max)={t_eps} < 4: no preregistered "
                                     "intensification interval in this run"}
    out["log_periodicity"] = {"verdict": "NOT APPLICABLE",
                              "reason": "no intensification interval"}
    print("ceiling/periodicity: NOT APPLICABLE (no intensification interval)")
else:
    mask = (spec_t >= 4.0) & (spec_t <= t_eps)
    tt = spec_t[mask]
    logK = np.log(K[mask])
    X2 = np.column_stack([np.ones_like(tt), np.log(tt - 3.0)])
    c2, *_ = np.linalg.lstsq(X2, logK, rcond=None)
    res2 = logK - X2 @ c2
    rms2 = float(np.sqrt(np.mean(res2**2)))
    best = None
    for tau in np.exp(np.linspace(np.log(0.2), np.log(10.0), 200)):
        X1 = np.column_stack([np.ones_like(tt), -np.exp(-(tt - 4.0) / tau)])
        c1, *_ = np.linalg.lstsq(X1, logK, rcond=None)
        res1 = logK - X1 @ c1
        rms1 = float(np.sqrt(np.mean(res1**2)))
        if best is None or rms1 < best[0]:
            best = (rms1, tau, c1, res1)
    rms1, tau_best, c1, res1 = best
    ratio = rms1 / rms2
    print(f"ceiling: rms_sat={rms1:.4f} tau={tau_best:.3f} rms_no={rms2:.4f} "
          f"ratio={ratio:.3f} -> {'PASS' if ratio < 0.8 else 'FAIL'}")
    win_res = res1 if ratio < 1.0 else res2
    win_name = "(i) saturating" if ratio < 1.0 else "(ii) no-ceiling"
    x = np.log(tt)
    y = win_res - win_res.mean()
    periods = np.exp(np.linspace(np.log(0.10), np.log(1.50), 400))
    amps = []
    for P in periods:
        w = 2 * np.pi / P
        X = np.column_stack([np.ones_like(x), np.sin(w * x), np.cos(w * x)])
        c, *_ = np.linalg.lstsq(X, y, rcond=None)
        amps.append(float(np.sqrt(np.mean((X @ c) ** 2))))
    amps = np.array(amps)
    resid_std = float(np.std(y))
    candidates = {"log phi/2": 0.2406, "2pi/19 (twist)": 2 * np.pi / 19,
                  "S-bar": 0.36, "log phi": 0.4812, "2 log phi": 0.9624}
    scan = {}
    for name, P0 in candidates.items():
        sel = np.abs(periods - P0) <= 0.10 * P0
        i = int(np.argmax(np.where(sel, amps, -1)))
        scan[name] = {"candidate": P0, "peak_period": float(periods[i]),
                      "amplitude": float(amps[i]),
                      "amp_over_resid_std": float(amps[i] / resid_std) if resid_std else 0.0}
        print(f"  {name:16s} amp/std {amps[i]/resid_std:.3f} at period {periods[i]:.4f}")
    ib = int(np.argmax(amps))
    print(f"  global best: period {periods[ib]:.4f} amp/std {amps[ib]/resid_std:.3f}")
    out["ceiling_test"] = {"interval": [float(tt[0]), float(tt[-1])],
                           "rms_saturating": rms1, "tau": float(tau_best),
                           "rms_no_ceiling": rms2, "ratio": ratio,
                           "verdict": "PASS" if ratio < 0.8 else "FAIL"}
    out["log_periodicity"] = {"winning_model": win_name, "resid_std": resid_std,
                              "candidates": scan,
                              "global_best_period": float(periods[ib]),
                              "global_best_amp": float(amps[ib]),
                              "global_best_amp_over_resid_std":
                                  float(amps[ib] / resid_std) if resid_std else 0.0}

with open(OUT, "w") as f:
    json.dump(out, f, indent=2)
print(f"wrote {OUT}")
