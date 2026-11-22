"""Stage A/B/C press run: Taylor-Green at Re=1600, N=128, instrumented.
Cosmo's production solver: rfftn-based pseudospectral, 2/3 dealiasing,
Leray projection, classical RK4. Diagnostics every OUT steps; shell
spectra saved for the Stage C front analysis. Preregistration:
ns-truly-testing-plan.md + Amendment 1 (pinned 2026-11-21)."""
import json, sys, time
import numpy as np

N = int(sys.argv[1]) if len(sys.argv) > 1 else 128
NU = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0 / 1600.0
SHUFFLE_SEED = int(sys.argv[4]) if len(sys.argv) > 4 else None
T = 12.0
DT = 0.005
OUT = 10            # diagnostics every OUT steps -> dt_out = 0.025
SPEC = 100          # spectra every SPEC steps -> dt_spec = 0.25
TAG = sys.argv[2] if len(sys.argv) > 2 else "re1600_n128"

n = N
k1 = np.fft.fftfreq(n, d=1.0 / n)
kr = np.fft.rfftfreq(n, d=1.0 / n)
KX, KY, KZ = np.meshgrid(k1, k1, kr, indexing="ij")
K2 = KX**2 + KY**2 + KZ**2
K2inv = np.where(K2 > 0, 1.0 / np.where(K2 > 0, K2, 1.0), 0.0)
keep = (np.abs(KX) <= n / 3) & (np.abs(KY) <= n / 3) & (np.abs(KZ) <= n / 3)
shell_idx = np.round(np.sqrt(K2)).astype(int).ravel()
nshell = int(shell_idx.max()) + 1

x = 2 * np.pi * np.arange(n) / n
X, Y, Z = np.meshgrid(x, x, x, indexing="ij")
u0 = [np.sin(X) * np.cos(Y) * np.cos(Z), -np.cos(X) * np.sin(Y) * np.cos(Z), np.zeros_like(X)]
uh = [np.fft.rfftn(u) / n**3 for u in u0]
if SHUFFLE_SEED is not None:
    # Stage C control (1): phase-shuffled initial field, identical spectrum.
    # Random Hermitian-symmetric phases on the full grid: |U(k)| preserved
    # exactly per mode (hence the shell spectrum is identical), and the field
    # stays divergence-free mode-by-mode since k.(e^{i ph} U) = e^{i ph}(k.U)
    # = 0 per mode. Seed declared in the run log.
    rng = np.random.default_rng(SHUFFLE_SEED)
    ph = rng.uniform(0.0, 2 * np.pi, size=(n, n, n))
    rev = (n - np.arange(n)) % n
    ph = 0.5 * (ph - ph[np.ix_(rev, rev, rev)])
    uh = []
    for u in u0:
        U = np.fft.fftn(u) * np.exp(1j * ph)
        uh.append(np.fft.rfftn(np.fft.ifftn(U).real) / n**3)
    print(f"phase-shuffled initial field, seed {SHUFFLE_SEED}", flush=True)

def project(vh):
    kdotv = KX * vh[0] + KY * vh[1] + KZ * vh[2]
    return [vh[i] - k * kdotv * K2inv for i, k in enumerate((KX, KY, KZ))]

def rhs(vh):
    v = [np.fft.irfftn(h * n**3, s=(n, n, n)) for h in vh]
    dv = [[np.fft.irfftn(1j * k * vh[j] * n**3, s=(n, n, n)) for j in range(3)]
          for k in (KX, KY, KZ)]
    nl = []
    for j in range(3):
        conv = v[0] * dv[0][j] + v[1] * dv[1][j] + v[2] * dv[2][j]
        nl.append(np.fft.rfftn(conv) / n**3 * keep)
    nl = project(nl)
    return [-nl[j] - NU * K2 * vh[j] for j in range(3)]

def diagnostics(vh):
    # Parseval with rfftn: sum over half-spectrum with weights (kz=0 and kz=n/2 planes weight 1, else 2)
    w = np.ones_like(KZ); w[:, :, 1:-1] = 2.0
    E = 0.5 * sum(np.sum(w * (h * np.conj(h)).real) for h in vh)
    grad2 = sum(np.sum(w * K2 * (h * np.conj(h)).real) for h in vh)
    Om = 0.5 * grad2
    eps = NU * grad2
    return float(E), float(Om), float(eps)

def max_vorticity(vh):
    w = [np.fft.irfftn(1j * (KY * vh[2] - KZ * vh[1]) * n**3, s=(n, n, n)),
         np.fft.irfftn(1j * (KZ * vh[0] - KX * vh[2]) * n**3, s=(n, n, n)),
         np.fft.irfftn(1j * (KX * vh[1] - KY * vh[0]) * n**3, s=(n, n, n))]
    return float(np.max(np.sqrt(w[0]**2 + w[1]**2 + w[2]**2)))

def spectrum(vh):
    w = np.ones_like(KZ); w[:, :, 1:-1] = 2.0
    dens = 0.5 * sum(w * (h * np.conj(h)).real for h in vh)
    return np.bincount(shell_idx, weights=dens.ravel(), minlength=nshell)

import os
CKPT = f"/home/hatch/workspace/goals/panoramic-os-and-pan-fractal-kernel-review/hidden_files/ns-press/{TAG}.ckpt.npz"
steps = int(round(T / DT))
start_step = 0
hist = {"t": [], "E": [], "Om": [], "eps": [], "wmax": []}
specs = {"t": [], "E_shell": []}
if os.path.exists(CKPT):
    z = np.load(CKPT, allow_pickle=True)
    uh = [z[f"u{j}"] for j in range(3)]
    start_step = int(z["step"])
    hist = {k: list(v) for k, v in json.loads(str(z["hist"])).items()}
    specs = {k: list(v) for k, v in json.loads(str(z["specs"])).items()}
    print(f"resumed at step {start_step} t={start_step*DT}", flush=True)
else:
    hist = {"t": [], "E": [], "Om": [], "eps": [], "wmax": []}
    specs = {"t": [], "E_shell": []}
t0 = time.time()
if start_step == 0:
    E, Om, eps = diagnostics(uh)
    hist["t"].append(0.0); hist["E"].append(E); hist["Om"].append(Om); hist["eps"].append(eps)
    hist["wmax"].append(max_vorticity(uh))
    specs["t"].append(0.0); specs["E_shell"].append(spectrum(uh).tolist())
for s in range(start_step + 1, steps + 1):
    a = rhs(uh)
    ub = [uh[j] + 0.5 * DT * a[j] for j in range(3)]
    b = rhs(ub)
    uc = [uh[j] + 0.5 * DT * b[j] for j in range(3)]
    c = rhs(uc)
    ud = [uh[j] + DT * c[j] for j in range(3)]
    d = rhs(ud)
    uh = [uh[j] + DT * (a[j] + 2 * b[j] + 2 * c[j] + d[j]) / 6.0 for j in range(3)]
    if s % OUT == 0:
        E, Om, eps = diagnostics(uh)
        hist["t"].append(s * DT); hist["E"].append(E); hist["Om"].append(Om)
        hist["eps"].append(eps); hist["wmax"].append(max_vorticity(uh))
    if s % SPEC == 0:
        specs["t"].append(s * DT); specs["E_shell"].append(spectrum(uh).tolist())
    if s % 200 == 0:
        np.savez(CKPT, u0=uh[0], u1=uh[1], u2=uh[2], step=s,
                 hist=json.dumps(hist), specs=json.dumps(specs))
        print(f"step {s}/{steps} t={s*DT:.2f} wall={time.time()-t0:.0f}s ckpt saved", flush=True)
out = {"tag": TAG, "N": N, "nu": NU, "Re": 1.0 / NU, "T": T, "dt": DT,
       "hist": hist, "spectra": specs, "wall_s": time.time() - t0}
path = f"/home/hatch/workspace/goals/panoramic-os-and-pan-fractal-kernel-review/hidden_files/ns-press/{TAG}.json"
with open(path, "w") as f:
    json.dump(out, f)
ie = int(np.argmax(hist["eps"]))
print("eps_max", hist["eps"][ie], "at t", hist["t"][ie], "| Om_peak", max(hist["Om"]))
print("wmax_peak", max(hist["wmax"]), "| BKM int(0..10) trapz:",
      float(np.trapz([w for t, w in zip(hist["t"], hist["wmax"]) if t <= 10.0],
                     [t for t in hist["t"] if t <= 10.0])))
print("done ->", path, "wall", out["wall_s"])
