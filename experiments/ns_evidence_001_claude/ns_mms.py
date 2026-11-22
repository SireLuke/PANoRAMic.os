#!/usr/bin/env python3
"""Addendum 01: manufactured-solution (MMS) test of forced periodic Navier-Stokes.

Why: in the Taylor-Green benchmarks the 2D nonlinear term is a pure gradient (it vanishes after
projection), so 2D never exercises it, and 3D only does so over a short window. Here the exact
solution is chosen so that the projected nonlinear term is genuinely non-zero, and a forcing term
makes that solution exact:

    u_m(x, t) = a(t) u0(x),   a(t) = 1 + 0.5 sin(2t),   div u0 = 0,
    P f = a'(t) u0 + a(t)^2 P[(u0 . grad) u0] - nu a(t) Lap(u0).

Independence: the forcing is built from ANALYTIC derivatives (an exact trig-sum class: d/dx_i of
c cos(k.x + phi) is c k_i cos(k.x + phi + pi/2)), not from the solver's FFT-derivative nonlinear
operator. If the solver's nonlinear term had a wrong sign, factor, or missing piece, the error
would be O(1), not roundoff. Negative controls below confirm the test has that sensitivity.

The frozen solver core (ns_spectral.PeriodicNS) is reused unchanged; only a stage-time forcing
wrapper is added here. Mode content is limited to |k_i| <= 2 so every product has |k_i| <= 4,
which the 2/3 rule keeps for N >= 12; the semi-discrete problem therefore has u_m as its exact
solution and the observed error is time-integration plus roundoff error.

No claim of regularity, blow-up, or a Clay-problem result is made.
"""

import argparse
import json
import math
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I removes the script dir
import ns_spectral as ns  # noqa: E402  (frozen solver core, unchanged)

NU = ns.NU


class Trig:
    """Scalar field  sum_j c_j cos(k_j . x + phi_j)  with exact differentiation."""

    def __init__(self, terms=()):
        self.terms = list(terms)

    def __add__(self, other):
        return Trig(self.terms + other.terms)

    def __neg__(self):
        return self.scale(-1.0)

    def __sub__(self, other):
        return self + (-other)

    def scale(self, s):
        return Trig([(c * s, k, p) for c, k, p in self.terms])

    def d(self, i):
        # d/dx_i cos(theta) = -k_i sin(theta) = k_i cos(theta + pi/2)
        return Trig([(c * k[i], k, p + math.pi / 2) for c, k, p in self.terms])

    def lap(self):
        return Trig([(-c * sum(ki * ki for ki in k), k, p) for c, k, p in self.terms])

    def __call__(self, X):
        out = np.zeros_like(X[0])
        for c, k, p in self.terms:
            out += c * np.cos(sum(ki * Xi for ki, Xi in zip(k, X)) + p)
        return out


def S_(c, k):  # c sin(k.x)
    return Trig([(c, tuple(k), -math.pi / 2)])


def C_(c, k):  # c cos(k.x)
    return Trig([(c, tuple(k), 0.0)])


def fields(d):
    """Velocity components of u0 as Trig objects (divergence-free by construction)."""
    if d == 2:
        # stream function psi = sin x sin y + 0.5 sin 2x cos y;  u = psi_y, v = -psi_x
        psi = C_(0.5, (1, -1)) + C_(-0.5, (1, 1)) + S_(0.25, (2, 1)) + S_(0.25, (2, -1))
        return [psi.d(1), -psi.d(0)]
    # vector potential A;  u = curl A
    Ax = S_(0.5, (0, 1, 1)) + C_(0.3, (2, -1, 0))
    Ay = C_(0.4, (1, 0, 1)) + S_(0.2, (0, 2, 1))
    Az = S_(0.6, (1, 1, 0)) + C_(0.25, (1, 0, -2))
    return [Az.d(1) - Ay.d(2), Ax.d(2) - Az.d(0), Ay.d(0) - Ax.d(1)]


def a_of(t):
    return 1.0 + 0.5 * math.sin(2.0 * t)


def da_of(t):
    return math.cos(2.0 * t)


class ForcedNS(ns.PeriodicNS):
    """Frozen solver plus a time-dependent forcing; nonlinear term optionally scaled (negative controls)."""

    def __init__(self, N, d, nu=NU, nl_scale=1.0, forcing_sign=1.0):
        super().__init__(N, d, nu=nu, form="convective")
        self.nl_scale = nl_scale
        self.forcing_sign = forcing_sign
        comps = fields(d)
        X = self.grid()
        U = np.array([f(X) for f in comps])
        G = np.array([sum(U[j] * comps[i].d(j)(X) for j in range(d)) for i in range(d)])  # (u0.grad)u0
        L = np.array([comps[i].lap()(X) for i in range(d)])
        self.U0h = self.to_hat(U)
        self.G_raw_h = self.to_hat(G)
        self.Gh = self.project(self.G_raw_h)
        self.Lh = self.to_hat(L)

    def fhat(self, t):
        a, da = a_of(t), da_of(t)
        # forcing always uses the TRUE nu = NU, independent of the solver's nu (viscosity control)
        return self.forcing_sign * (da * self.U0h + a * a * self.Gh - NU * a * self.Lh)

    def rhs(self, uh, t):
        return self.nl_scale * self.nonlinear(uh) + self.fhat(t)

    def step_forced(self, uh, t, dt, Efac, E2fac):
        k1 = self.rhs(uh, t)
        b = E2fac * (uh + 0.5 * dt * k1)
        k2 = self.rhs(b, t + 0.5 * dt)
        c = E2fac * uh + 0.5 * dt * k2
        k3 = self.rhs(c, t + 0.5 * dt)
        dd = Efac * uh + dt * E2fac * k3
        k4 = self.rhs(dd, t + dt)
        return Efac * uh + (dt / 6.0) * (Efac * k1 + 2.0 * E2fac * (k2 + k3) + k4)


def run(d, N, T, dt, **kw):
    S = ForcedNS(N, d, **kw)
    uh = a_of(0.0) * S.U0h
    nsteps = int(round(T / dt))
    assert abs(nsteps * dt - T) < 1e-12
    Efac = np.exp(-S.nu * S.k2 * dt)
    E2fac = np.exp(-0.5 * S.nu * S.k2 * dt)
    t0 = time.perf_counter()
    for n in range(nsteps):
        uh = S.step_forced(uh, n * dt, dt, Efac, E2fac)
    runtime = time.perf_counter() - t0
    exact = a_of(T) * S.U0h
    diff = uh - exact
    rel_spec = math.sqrt(float(np.sum(np.abs(diff) ** 2)) / float(np.sum(np.abs(exact) ** 2)))
    maxabs = float(np.max(np.abs(S.to_phys(diff))))
    return dict(d=d, N=N, T=T, dt=dt, nsteps=nsteps, rel_l2_error=rel_spec, max_abs_error=maxabs,
                finite=bool(np.all(np.isfinite(uh))), runtime_s=runtime, **{k: v for k, v in kw.items()})


def validate_machinery():
    """Checks that do not involve the time stepper."""
    out = {}
    rng = np.random.default_rng(11)
    for d in (2, 3):
        comps = fields(d)
        P = rng.uniform(0.0, 2 * math.pi, size=(d, 7))
        h = 1e-5
        worst = 0.0
        for f in comps:
            for i in range(d):
                Pp, Pm = P.copy(), P.copy()
                Pp[i] += h
                Pm[i] -= h
                fd = (f(Pp) - f(Pm)) / (2 * h)
                worst = max(worst, float(np.max(np.abs(fd - f.d(i)(P)))))
        out["%dD_derivative_vs_central_difference_max_abs" % d] = worst
        div = sum(comps[i].d(i)(P) for i in range(d))
        out["%dD_analytic_divergence_max_abs" % d] = float(np.max(np.abs(div)))
        # Laplacian against second central difference
        worst = 0.0
        h2 = 1e-3  # second differences need a larger step: roundoff ~ eps/h^2, truncation ~ h^2 f''''/12
        for f in comps:
            lap_fd = np.zeros(7)
            for i in range(d):
                Pp, Pm = P.copy(), P.copy()
                Pp[i] += h2
                Pm[i] -= h2
                lap_fd += (f(Pp) - 2 * f(P) + f(Pm)) / (h2 * h2)
            worst = max(worst, float(np.max(np.abs(lap_fd - f.lap()(P)))))
        out["%dD_laplacian_vs_second_difference_max_abs" % d] = worst
    # closed-form stream function check (2D)
    X = ns.PeriodicNS(16, 2).grid()
    psi = C_(0.5, (1, -1)) + C_(-0.5, (1, 1)) + S_(0.25, (2, 1)) + S_(0.25, (2, -1))
    closed = np.sin(X[0]) * np.sin(X[1]) + 0.5 * np.sin(2 * X[0]) * np.cos(X[1])
    out["2D_psi_vs_closed_form_max_abs"] = float(np.max(np.abs(psi(X) - closed)))
    return out


def consistency_and_teeth():
    """Pointwise agreement of analytic and FFT advection, and how non-trivial the nonlinear term is."""
    out = {}
    for d in (2, 3):
        S = ForcedNS(24, d)
        Nsolver = S.nonlinear(S.U0h)  # = -P F[(u0.grad)u0] from the FFT-derivative operator
        out["%dD_analytic_vs_fft_advection_rel" % d] = float(np.max(np.abs(Nsolver + S.Gh)) / np.max(np.abs(S.Gh)))
        out["%dD_MMS_projected_nonlinear_over_state" % d] = float(np.max(np.abs(Nsolver)) / np.max(np.abs(S.U0h)))
        out["%dD_MMS_fraction_surviving_projection" % d] = float(
            np.linalg.norm(S.Gh) / np.linalg.norm(S.G_raw_h))
        T = ns.PeriodicNS(24, d)
        tg = T.to_hat(T.taylor_green())
        out["%dD_TaylorGreen_projected_nonlinear_over_state" % d] = float(np.max(np.abs(T.nonlinear(tg))) / np.max(np.abs(tg)))
    return out


def n16_truncation_check():
    """Test of a hypothesis for why N=16 time-integration error is slightly LARGER than N>=24.

    Hypothesis H1: N=16 truncates high modes (max|k_i| > 5) of the error. H1 predicts N=16 error
    SMALLER than N=24 by sqrt(1 - f), f = fraction of N=24 error energy above the N=16 cutoff.
    The measured ratio has the opposite sign, so H1 is rejected as the explanation.
    """
    out = {}
    for d in (2, 3):
        N, T, dt = 24, 1.0, 0.1
        S = ForcedNS(N, d)
        uh = a_of(0.0) * S.U0h
        Ef = np.exp(-S.nu * S.k2 * dt)
        E2 = np.exp(-0.5 * S.nu * S.k2 * dt)
        for n in range(int(round(T / dt))):
            uh = S.step_forced(uh, n * dt, dt, Ef, E2)
        diff = uh - a_of(T) * S.U0h
        e2 = np.sum(np.abs(diff) ** 2, axis=0)
        f = float(e2[np.max(np.abs(S.k), axis=0) > 5].sum() / e2.sum())
        e16 = run(d, 16, T, dt)["rel_l2_error"]
        e24 = run(d, 24, T, dt)["rel_l2_error"]
        out["%dD" % d] = dict(dt=dt, error_energy_fraction_above_N16_cutoff=f,
                              H1_predicted_ratio_N16_over_N24=math.sqrt(1.0 - f),
                              measured_ratio_N16_over_N24=e16 / e24)
    return out


def order(errs, floor=1e-13):
    res = []
    for e1, e2 in zip(errs[:-1], errs[1:]):
        res.append(round(math.log(e1 / e2) / math.log(2.0), 2) if (e1 > floor and e2 > 0) else None)
    return res


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", default=os.path.join(here, "outputs", "addendum01_results.json"))
    ap.add_argument("--quick", action="store_true", help="small subset for a fast smoke run")
    args = ap.parse_args()

    T = 1.0
    dts = [0.1, 0.05, 0.025, 0.0125, 0.00625, 0.003125]
    Ns = (16, 24, 32)
    if args.quick:
        dts, Ns = [0.1, 0.05, 0.025], (16,)

    res = dict(
        meta=dict(T=T, nu=NU, a_of_t="1 + 0.5 sin(2t)", numpy=np.__version__, python=sys.version.split()[0],
                  solver_core="ns_spectral.PeriodicNS (frozen, unchanged)"),
        machinery=validate_machinery(),
        consistency=consistency_and_teeth(),
        n16_truncation_check=n16_truncation_check() if not args.quick else None,
        runs=[], order={}, negative_controls=[],
    )
    for d in (2, 3):
        for N in Ns:
            rows = [run(d, N, T, dt) for dt in dts]
            res["runs"] += rows
            res["order"]["%dD_N%d" % (d, N)] = dict(
                dt=dts, rel_l2_error=[r["rel_l2_error"] for r in rows], observed_order=order([r["rel_l2_error"] for r in rows]))
            print("%dD N=%d  " % (d, N) + "  ".join("dt=%g:%.2e" % (r["dt"], r["rel_l2_error"]) for r in rows), flush=True)

    # negative controls: the test must FAIL when the physics is wrong
    ctrl_dt = 0.00625 if not args.quick else 0.025
    for d in (2, 3):
        base = run(d, 24 if not args.quick else 16, T, ctrl_dt)
        res["negative_controls"].append(dict(control="correct solver", **base))
        for name, kw in (("nonlinear term disabled", dict(nl_scale=0.0)),
                         ("nonlinear term sign flipped", dict(nl_scale=-1.0)),
                         ("viscosity off by 10% in solver (0.011 vs forcing 0.01)", dict(nu=0.011)),
                         ("forcing sign flipped", dict(forcing_sign=-1.0))):
            r = run(d, 24 if not args.quick else 16, T, ctrl_dt, **kw)
            res["negative_controls"].append(dict(control=name, **r))
    for c in res["negative_controls"]:
        print("%dD %-58s rel L2 err %.3e" % (c["d"], c["control"], c["rel_l2_error"]))

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w") as fh:
        json.dump(res, fh, indent=1, sort_keys=True)
    print("wrote", args.out)


if __name__ == "__main__":
    main()
