"""Stage C analysis for the Re=1600 N=128 press run (Amendment 1).

Reads the saved shell spectra from re1600_n128.json, computes the
occupation front K(t), runs the preregistered ceiling test (saturating
vs no-ceiling fit on t in [4, t(eps_max)]), and scans the winning
model's residuals for log-periodicity at the two pinned families:
  (i)  log-phi family: 0.2406, 0.4812, 0.9624 (log t units)
  (ii) bridge-note constants: S-bar ~ 0.36, twist 2*pi/19 ~ 0.3307
Controls are NOT in this script: the periodicity verdict requires the
phase-shuffled control and the nu=0.01 baseline runs. This script
reports the scan; the verdict waits on the controls.
"""
import json
import numpy as np

DATA = "/home/hatch/workspace/goals/panoramic-os-and-pan-fractal-kernel-review/hidden_files/ns-press/re1600_n128.json"
OUT = "/home/hatch/workspace/goals/panoramic-os-and-pan-fractal-kernel-review/hidden_files/ns-press/stage_c_results.json"

d = json.load(open(DATA))
h = d["hist"]
spec_t = np.array(d["spectra"]["t"])
spec_E = [np.array(e) for e in d["spectra"]["E_shell"]]

# --- Occupation front K(t): smallest k with energy in shells > k below 1e-3 of total
K = []
for E in spec_E:
    total = E.sum()
    tail = np.cumsum(E[::-1])[::-1]  # tail[k] = sum of shells >= k
    # energy in shells > k = total - cumsum up to k
    csum = np.cumsum(E)
    above = total - csum  # above[k] = energy in shells > k
    below = np.where(above < 1e-3 * total)[0]
    K.append(int(below[0]) if len(below) else int(len(E) - 1))
K = np.array(K, dtype=float)
print("K(t) full series:")
for t, k in zip(spec_t, K):
    print(f"  t={t:5.2f}  K={int(k)}")

# --- Stage A / B recap from hist
ie = int(np.argmax(h["eps"]))
eps_max, t_eps = h["eps"][ie], h["t"][ie]
om_peak = max(h["Om"])
t_arr = np.array(h["t"])
w_arr = np.array(h["wmax"])
m10 = t_arr <= 10.0
bkm = float(np.trapz(w_arr[m10], t_arr[m10]))
print(f"\nStage A: eps_max={eps_max:.6f} at t={t_eps} "
      f"(ref 0.01286 at 8.97; ratio {eps_max/0.01286:.4f}, dt={t_eps-8.97:+.2f})")
print(f"Stage B: BKM int(0..10)={bkm:.2f} (expected ~180-210); "
      f"wmax_peak={w_arr.max():.2f}; Om_peak={om_peak:.3f} (derived ~10.3)")

# --- Ceiling test on t in [4, t(eps_max)] = [4, 8.9]
mask = (spec_t >= 4.0) & (spec_t <= t_eps)
tt = spec_t[mask]
logK = np.log(K[mask])
print(f"\nCeiling-test interval: t in [{tt[0]}, {tt[-1]}], n={len(tt)} points")
print("  logK:", np.round(logK, 4).tolist())

# model (ii): log K = a + c*log(t-3)
X2 = np.column_stack([np.ones_like(tt), np.log(tt - 3.0)])
c2, *_ = np.linalg.lstsq(X2, logK, rcond=None)
res2 = logK - X2 @ c2
rms2 = float(np.sqrt(np.mean(res2**2)))

# model (i): log K = a - b*exp(-(t-4)/tau), grid over tau
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
print(f"  model (i) saturating: rms={rms1:.4f} tau={tau_best:.3f} a={c1[0]:.4f} b={c1[1]:.4f}")
print(f"  model (ii) no-ceiling: rms={rms2:.4f} a={c2[0]:.4f} c={c2[1]:.4f}")
print(f"  residual RMS ratio (i)/(ii) = {ratio:.3f}  (ceiling reading requires < 0.8)")
print(f"  CEILING TEST: {'PASS (saturating wins by declared margin)' if ratio < 0.8 else 'FAIL (no ceiling margin)'}")

# --- Log-periodicity scan on the winning model's residuals vs log t
win_res = res1 if ratio < 1.0 else res2
win_name = "(i) saturating" if ratio < 1.0 else "(ii) no-ceiling"
x = np.log(tt)
y = win_res - win_res.mean()
print(f"\nLog-periodicity scan on {win_name} residuals vs log t "
      f"(span {x[0]:.3f}..{x[-1]:.3f}, n={len(x)}):")
periods = np.exp(np.linspace(np.log(0.10), np.log(1.50), 400))
amps = []
for P in periods:
    w = 2 * np.pi / P
    X = np.column_stack([np.ones_like(x), np.sin(w * x), np.cos(w * x)])
    c, *_ = np.linalg.lstsq(X, y, rcond=None)
    fit = X @ c
    amps.append(float(np.sqrt(np.mean(fit**2))))
amps = np.array(amps)
resid_std = float(np.std(y))
print(f"  residual std = {resid_std:.4f}")
candidates = {"log phi/2": 0.2406, "2pi/19 (twist)": 2 * np.pi / 19,
              "S-bar": 0.36, "log phi": 0.4812, "2 log phi": 0.9624}
scan = {}
for name, P0 in candidates.items():
    sel = np.abs(periods - P0) <= 0.10 * P0
    i = int(np.argmax(np.where(sel, amps, -1)))
    scan[name] = {"candidate": P0, "peak_period": float(periods[i]),
                  "amplitude": float(amps[i]),
                  "amp_over_resid_std": float(amps[i] / resid_std) if resid_std else 0.0}
    print(f"  {name:16s} candidate {P0:.4f}: best period {periods[i]:.4f} "
          f"amp {amps[i]:.4f} (amp/std {amps[i]/resid_std:.2f})")
# global best period
ib = int(np.argmax(amps))
print(f"  global best period: {periods[ib]:.4f} amp {amps[ib]:.4f}")

results = {
    "tag": "re1600_n128",
    "stage_a": {"eps_max": eps_max, "t_eps": t_eps, "ref_eps": 0.01286,
                "ref_t": 8.97, "ratio": eps_max / 0.01286,
                "gate": "+10%/-5% eps, +-0.4 t",
                "verdict": "PASS" if (0.95 <= eps_max / 0.01286 <= 1.10
                                      and abs(t_eps - 8.97) <= 0.4) else "FAIL"},
    "stage_b": {"bkm_int_0_10": bkm, "expected": "180-210",
                "wmax_peak": float(w_arr.max()), "om_peak": om_peak},
    "K_series": {"t": spec_t.tolist(), "K": K.astype(int).tolist()},
    "ceiling_test": {"interval": [float(tt[0]), float(tt[-1])], "n": int(len(tt)),
                     "rms_saturating": rms1, "tau": float(tau_best),
                     "rms_no_ceiling": rms2, "ratio": ratio,
                     "verdict": "PASS" if ratio < 0.8 else "FAIL"},
    "log_periodicity": {"winning_model": win_name, "resid_std": resid_std,
                        "candidates": scan,
                        "global_best_period": float(periods[ib]),
                        "global_best_amp": float(amps[ib]),
                        "verdict": "PENDING CONTROLS"},
    "controls_status": "phase-shuffled control and nu=0.01 baseline not yet run",
}
with open(OUT, "w") as f:
    json.dump(results, f, indent=2)
print(f"\nwrote {OUT}")
