"""STRATA Architect bench (Claude), 2026-11-17: UNVERIFIED pending another bench.
Requires numpy and scipy (not stdlib-only; not run in CI). Run: python -I generic_toy_d2.py

Smallest GENERIC (metriplectic) toy with both parts nontrivial: 3 channels (a, b, s).

x = (a, b, s)         a,b: reversible pair (proposal: V8 h coherence, R recursion); s: entropy channel
E(x) = b^2/2 + V(a) + exp(s)          energy; T = dE/ds = exp(s) > 0
S(x) = s                              entropy
L    = [[0,1,0],[-1,0,0],[0,0,0]]     constant antisymmetric (Jacobi holds trivially)
M    = (zeta/T) w w^T,  w = (0, T, -b) symmetric PSD, w.grad(E) = T*b - b*T = 0

Checks: L.gradS = 0, M.gradE = 0, M symmetric PSD, dS/dt >= 0, dE/dt = 0 along flows,
forward / backward / time-reversal, all on seeded random data.
Also a 2-channel no-go check and the radial first-integral facts (the Lagrangian
L = (y/m)xdot - H for xdot = m H_y, ydot = -m H_x is derived by hand in the report).
"""
import sys
import numpy as np
from scipy.integrate import solve_ivp

RNG = np.random.default_rng(20261117)
L = np.array([[0.0, 1, 0], [-1, 0, 0], [0, 0, 0]])


def V(a, ka, kb):  return ka * a**2 / 2 + kb * a**4 / 4
def dV(a, ka, kb): return ka * a + kb * a**3


def parts(x, zeta, ka, kb):
    a, b, s = x
    T = np.exp(s)
    gE = np.array([dV(a, ka, kb), b, T])
    gS = np.array([0.0, 0.0, 1.0])
    w = np.array([0.0, T, -b])
    M = (zeta / T) * np.outer(w, w)
    return gE, gS, M


def E(x, ka, kb): return x[1]**2 / 2 + V(x[0], ka, kb) + np.exp(x[2])


def rhs(t, x, zeta, ka, kb):
    gE, gS, M = parts(x, zeta, ka, kb)
    return L @ gE + M @ gS


def rand_params():
    return RNG.uniform(0.0, 3.0), RNG.uniform(0.1, 2.0), RNG.uniform(0.0, 1.0)  # zeta, ka, kb


results = {}

# 1. algebraic degeneracy checks on random states
worst = dict(LdS=0.0, MdE=0.0, sym=0.0, minEig=0.0, sigma_min=1e9)
for _ in range(2000):
    x = RNG.uniform(-2, 2, 3)
    zeta, ka, kb = rand_params()
    gE, gS, M = parts(x, zeta, ka, kb)
    worst["LdS"] = max(worst["LdS"], np.abs(L @ gS).max())
    worst["MdE"] = max(worst["MdE"], np.abs(M @ gE).max() / (1 + np.abs(M).max() * np.abs(gE).max()))
    worst["sym"] = max(worst["sym"], np.abs(M - M.T).max())
    worst["minEig"] = min(worst["minEig"], np.linalg.eigvalsh(M).min() / (1e-30 + np.abs(M).max()))
    worst["sigma_min"] = min(worst["sigma_min"], gS @ M @ gS)
    assert np.isclose(gS @ M @ gS, zeta * x[1]**2 / np.exp(x[2]))
results["degeneracy"] = worst
ok_alg = (worst["LdS"] == 0.0 and worst["MdE"] < 1e-12 and worst["sym"] == 0.0
          and worst["minEig"] > -1e-12 and worst["sigma_min"] >= 0.0)

# 2. dynamics: forward, backward, time reversal, randomised
rt = lambda x: np.array([x[0], -x[1], x[2]])
dyn = dict(dE_fwd=0.0, dE_bwd=0.0, dS_fwd_min=1e9, dS_bwd_max=-1e9, bwd_skipped=0, rev_defect_zeta0=0.0,
           rev_defect_zeta_pos=1e9, n=0)
for _ in range(300):
    x0 = RNG.uniform(-1.5, 1.5, 3)
    zeta, ka, kb = rand_params()
    args = (zeta, ka, kb)
    kw = dict(method="DOP853", rtol=1e-12, atol=1e-13, dense_output=False)
    tt = np.linspace(0, 8, 81)
    f = solve_ivp(rhs, (0, 8), x0, t_eval=tt, args=args, **kw)
    b = solve_ivp(rhs, (0, -1), x0, t_eval=-np.linspace(0, 1, 31), args=args, **kw)
    e0 = E(x0, ka, kb)
    if b.status != 0 or b.y.shape[1] < 3:      # reversed dissipative flow can blow up: skip, count
        dyn["bwd_skipped"] = dyn.get("bwd_skipped", 0) + 1
        continue
    dyn["dE_fwd"] = max(dyn["dE_fwd"], max(abs(E(c, ka, kb) - e0) for c in f.y.T) / abs(e0))
    dyn["dE_bwd"] = max(dyn["dE_bwd"], max(abs(E(c, ka, kb) - e0) for c in b.y.T) / abs(e0))
    dyn["dS_fwd_min"] = min(dyn["dS_fwd_min"], np.diff(f.y[2]).min())
    dyn["dS_bwd_max"] = max(dyn["dS_bwd_max"], np.diff(b.y[2]).max())
    # time reversal: R o flow_t o R vs flow_{-t}  (equivalently flow_t(R flow_t(x0)) == R x0)
    for z, key in ((0.0, "rev_defect_zeta0"), (max(zeta, 0.5), "rev_defect_zeta_pos")):
        a2 = (z, ka, kb)
        x1 = solve_ivp(rhs, (0, 4), x0, args=a2, **kw).y[:, -1]
        x2 = solve_ivp(rhs, (0, 4), rt(x1), args=a2, **kw).y[:, -1]
        d = np.abs(rt(x2) - x0).max()
        dyn[key] = max(dyn[key], d) if key == "rev_defect_zeta0" else min(dyn[key], d)
    dyn["n"] += 1
    dyn["bwd_used"] = dyn.get("bwd_used", 0) + 1
results["dynamics"] = dyn
ok_dyn = (dyn["dE_fwd"] < 1e-9 and dyn["dE_bwd"] < 1e-9 and dyn["dS_fwd_min"] >= -1e-10
          and dyn["dS_bwd_max"] <= 1e-10 and dyn["rev_defect_zeta0"] < 1e-8
          and dyn["rev_defect_zeta_pos"] > 1e-3)

# 3. no-go: with 2 channels L is 0 or invertible, so L.gradS = 0 forces gradS = 0
nogo = True
for _ in range(500):
    lam = RNG.uniform(0.1, 3.0) * RNG.choice([-1, 1])
    L2 = np.array([[0.0, lam], [-lam, 0.0]])
    gS2 = RNG.normal(size=2)
    nogo &= np.linalg.matrix_rank(L2) == 2 and np.abs(L2 @ gS2).max() > 0
results["two_channel_nogo_ok"] = bool(nogo)

# 4. radial first integral H = [y/(2-y)]^beta e^{-y^3/24} / (1-x^2): structure on |x|<1, 0<y<2
ys = np.linspace(1e-4, 2 - 1e-4, 200001)
rad = {}
for beta in (0.05, 0.1, 0.25, 0.5, 1.0, 2.0):
    lg = beta * (np.log(ys) - np.log(2 - ys)) - ys**3 / 24
    d = np.diff(lg)
    flips = ys[1:][np.where(np.diff(np.sign(d)) != 0)[0]]
    rad[beta] = ("g strictly increasing: dH/dy never 0, no critical points, no closed orbits"
                 if (d > 0).all() else
                 "dg/dy changes sign at y = " + ", ".join(f"{v:.3f}" for v in flips)
                 + ": critical points of H exist")
results["radial_g(y)"] = rad

for k, v in results.items():
    print(k, "->", v)
ok = ok_alg and ok_dyn and nogo
print("ALL_PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
