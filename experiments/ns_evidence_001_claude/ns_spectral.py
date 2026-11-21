#!/usr/bin/env python3
"""NS-EVIDENCE-001 independent verification (Claude bench).

Periodic incompressible Navier-Stokes on [0, 2*pi)^d, d = 2 or 3, solved with a
Fourier pseudo-spectral method written from the equations, not from any other
implementation.

Equations
    u_t + (u . grad) u = -grad p + nu * Laplace(u),   div u = 0.
Applying the Leray projector P = I - k k^T / |k|^2 in Fourier space removes p:
    d/dt u_hat = -P[ F{(u . grad) u} ] - nu |k|^2 u_hat.

Method
    Space   : Fourier collocation on an N^d grid, 2/3-rule dealiasing applied per
              direction (modes with |k_i| <= floor(N/3) are kept).
    Time    : Lawson integrating-factor RK4. The viscous term is integrated
              exactly; the nonlinear term uses classical RK4 stages.
    Precision: float64 / complex128.
    Nonlinear term: convective form (u . grad) u by default; the rotational form
              omega x u is implemented as an independent self-consistency check
              (the two differ by a gradient that P removes).

Diagnostics (all volume averages over the periodic box, i.e. divided by (2*pi)^d)
    E      = 1/2 <|u|^2>
    eps    = nu <|grad u|^2>              (viscous dissipation rate)
    Omega  = 1/2 <|omega|^2>              (enstrophy, from the curl of u_hat)
    D      = integral_0^t eps dt'         (integrated dissipation)
    maxdiv = max over grid nodes of |div u|, with div u evaluated spectrally
    resid  = E(T) - E(0) + D(T)           (energy-balance residual, ideally 0)
D is accumulated with the same RK4 stage values as the flow (the RK4 scheme
applied to the augmented system), so it carries the scheme's order. A trapezoid
estimate is kept as a lower-order cross-check.

Domain-integral values equal the volume averages times (2*pi)^d and are also
stored in the results so that either normalisation can be compared.

No claim of regularity, blow-up, or a Clay-problem result is made here.
"""

import argparse
import csv
import hashlib
import json
import math
import os
import platform
import sys
import time

import numpy as np

NU = 0.01
TWO_PI = 2.0 * math.pi

# Analytic t = 0 values (volume averages) for the Taylor-Green fields below.
ANALYTIC_T0 = {
    2: {"E": 0.25, "Omega": 0.5, "eps": 0.01},
    3: {"E": 0.125, "Omega": 0.375, "eps": 0.0075},
}


class PeriodicNS:
    def __init__(self, N, d, nu=NU, form="convective"):
        if d not in (2, 3):
            raise ValueError("d must be 2 or 3")
        if form not in ("convective", "rotational"):
            raise ValueError("form must be 'convective' or 'rotational'")
        self.N, self.d, self.nu, self.form = N, d, nu, form
        k1 = np.fft.fftfreq(N, d=1.0 / N)  # integer wavenumbers, box length 2*pi
        self.k = np.array(np.meshgrid(*([k1] * d), indexing="ij"))
        self.k2 = np.sum(self.k ** 2, axis=0)
        self.k2safe = np.where(self.k2 == 0.0, 1.0, self.k2)
        kc = N // 3
        self.mask = np.all(np.abs(self.k) <= kc, axis=0)
        self.ax = tuple(range(1, d + 1))  # transform axes for (d, N, ..., N) arrays
        self.norm = float(N) ** (2 * d)  # Parseval: <f^2> = sum |f_hat|^2 / N^(2d)

    # ---- grid, initial data, transforms -------------------------------------
    def grid(self):
        x = TWO_PI * np.arange(self.N) / self.N
        return np.meshgrid(*([x] * self.d), indexing="ij")

    def taylor_green(self):
        X = self.grid()
        if self.d == 2:
            x, y = X
            return np.array([np.sin(x) * np.cos(y), -np.cos(x) * np.sin(y)])
        x, y, z = X
        return np.array(
            [
                np.sin(x) * np.cos(y) * np.cos(z),
                -np.cos(x) * np.sin(y) * np.cos(z),
                np.zeros_like(x),
            ]
        )

    def to_hat(self, u):
        return np.fft.fftn(u, axes=self.ax) * self.mask

    def to_phys(self, uh):
        return np.fft.ifftn(uh, axes=self.ax).real

    # ---- operators -----------------------------------------------------------
    def project(self, fh):
        kdotf = np.sum(self.k * fh, axis=0)
        return fh - self.k * (kdotf / self.k2safe)

    def vorticity_hat(self, uh):
        k = self.k
        if self.d == 2:
            return 1j * (k[0] * uh[1] - k[1] * uh[0])  # scalar, shape (N, N)
        return 1j * np.array(
            [
                k[1] * uh[2] - k[2] * uh[1],
                k[2] * uh[0] - k[0] * uh[2],
                k[0] * uh[1] - k[1] * uh[0],
            ]
        )

    def nonlinear(self, uh):
        u = self.to_phys(uh)
        if self.form == "convective":
            adv = np.zeros_like(u)
            for j in range(self.d):
                dudx = np.fft.ifftn(1j * self.k[j] * uh, axes=self.ax).real  # d u_i / d x_j
                adv += u[j] * dudx
        else:
            wh = self.vorticity_hat(uh)
            if self.d == 2:
                w = np.fft.ifftn(wh, axes=(0, 1)).real
                adv = np.array([-w * u[1], w * u[0]])  # omega z_hat x u
            else:
                w = np.fft.ifftn(wh, axes=self.ax).real
                adv = np.array(
                    [
                        w[1] * u[2] - w[2] * u[1],
                        w[2] * u[0] - w[0] * u[2],
                        w[0] * u[1] - w[1] * u[0],
                    ]
                )
        nh = np.fft.fftn(adv, axes=self.ax) * self.mask
        nh = -self.project(nh)
        nh[(slice(None),) + (0,) * self.d] = 0.0
        return nh

    # ---- diagnostics ---------------------------------------------------------
    def eps_of(self, uh):
        return self.nu * float(np.sum(self.k2 * np.sum(np.abs(uh) ** 2, axis=0))) / self.norm

    def diagnostics(self, uh):
        e2 = np.sum(np.abs(uh) ** 2, axis=0)
        E = 0.5 * float(e2.sum()) / self.norm
        eps = self.nu * float(np.sum(self.k2 * e2)) / self.norm
        wh = self.vorticity_hat(uh)
        w2 = np.abs(wh) ** 2 if self.d == 2 else np.sum(np.abs(wh) ** 2, axis=0)
        Om = 0.5 * float(w2.sum()) / self.norm
        div = np.fft.ifftn(1j * np.sum(self.k * uh, axis=0)).real
        return {"E": E, "eps": eps, "Omega": Om, "maxdiv": float(np.max(np.abs(div)))}

    # ---- time stepping -------------------------------------------------------
    def step(self, uh, dt, E, E2):
        """One Lawson-RK4 step. Returns the new state and the RK4-weighted dissipation increment."""
        a = uh
        k1 = self.nonlinear(a)
        b = E2 * (uh + 0.5 * dt * k1)
        k2 = self.nonlinear(b)
        c = E2 * uh + 0.5 * dt * k2
        k3 = self.nonlinear(c)
        dd = E * uh + dt * E2 * k3
        k4 = self.nonlinear(dd)
        new = E * uh + (dt / 6.0) * (E * k1 + 2.0 * E2 * (k2 + k3) + k4)
        dinc = (dt / 6.0) * (
            self.eps_of(a) + 2.0 * self.eps_of(b) + 2.0 * self.eps_of(c) + self.eps_of(dd)
        )
        return new, dinc

    def exact_2d(self, t):
        x, y = self.grid()
        f = math.exp(-2.0 * self.nu * t)
        return f * np.array([np.sin(x) * np.cos(y), -np.cos(x) * np.sin(y)])


def case_id(c):
    return "%dD_N%d_T%g_dt%g_%s" % (c["d"], c["N"], c["T"], c["dt"], c["form"])


def run_case(c):
    N, d, T, dt, form = c["N"], c["d"], c["T"], c["dt"], c["form"]
    S = PeriodicNS(N, d, form=form)
    uh = S.to_hat(S.taylor_green())
    nsteps = int(round(T / dt))
    if abs(nsteps * dt - T) > 1e-12:
        raise ValueError("dt must divide T")
    Efac = np.exp(-S.nu * S.k2 * dt)
    E2fac = np.exp(-0.5 * S.nu * S.k2 * dt)

    t0 = time.perf_counter()
    d0 = S.diagnostics(uh)
    D = 0.0
    Dtrap = 0.0
    prev = d0
    maxdiv_all = d0["maxdiv"]
    hist = [dict(t=0.0, **d0, D=0.0)]
    for n in range(nsteps):
        uh, dinc = S.step(uh, dt, Efac, E2fac)
        D += dinc
        dg = S.diagnostics(uh)
        Dtrap += 0.5 * dt * (prev["eps"] + dg["eps"])
        maxdiv_all = max(maxdiv_all, dg["maxdiv"])
        hist.append(dict(t=(n + 1) * dt, **dg, D=D))
        prev = dg
    runtime = time.perf_counter() - t0
    dT = prev
    vol = TWO_PI ** d

    res = dict(c)
    res.update(
        id=case_id(c),
        nsteps=nsteps,
        finite=bool(np.all(np.isfinite(uh))),
        E0=d0["E"], E_T=dT["E"],
        eps0=d0["eps"], eps_T=dT["eps"],
        Omega0=d0["Omega"], Omega_T=dT["Omega"],
        D_int=D, D_int_trapezoid=Dtrap,
        maxdiv_final=dT["maxdiv"], maxdiv_max_over_time=maxdiv_all,
        resid_abs=dT["E"] - d0["E"] + D,
        resid_rel=(dT["E"] - d0["E"] + D) / d0["E"],
        resid_abs_trapezoid=dT["E"] - d0["E"] + Dtrap,
        eps_minus_2nuOmega_T=dT["eps"] - 2.0 * S.nu * dT["Omega"],
        E0_integral=d0["E"] * vol, E_T_integral=dT["E"] * vol, D_int_integral=D * vol,
        runtime_s=runtime,
        history=hist,
    )
    a0 = ANALYTIC_T0[d]
    res["t0_abs_error"] = {k: abs(d0[k] - a0[k]) for k in a0}
    if d == 2:
        u = S.to_phys(uh)
        ue = S.exact_2d(T)
        diff = u - ue
        res["exact2d_max_abs_error"] = float(np.max(np.abs(diff)))
        res["exact2d_l2_rel_error"] = float(
            math.sqrt(np.mean(np.sum(diff ** 2, axis=0))) / math.sqrt(np.mean(np.sum(ue ** 2, axis=0)))
        )
        Eex = 0.25 * math.exp(-4.0 * S.nu * T)
        res["exact2d_E_T"] = Eex
        res["exact2d_E_T_abs_error"] = abs(dT["E"] - Eex)
        res["exact2d_D_abs_error"] = abs(D - (0.25 - Eex))
        res["exact2d_eps_T_abs_error"] = abs(dT["eps"] - 0.01 * math.exp(-4.0 * S.nu * T))
    return res


def build_cases():
    cases = []
    for d in (2, 3):
        for N in (16, 24, 32):
            cases.append(dict(d=d, N=N, T=0.1, dt=0.001, form="convective", tag="primary"))
    for d in (2, 3):
        for dt in (0.002, 0.0005):
            cases.append(dict(d=d, N=32, T=0.1, dt=dt, form="convective", tag="dt_check"))
    for N in (16, 24, 32):
        for dt in (0.004, 0.002, 0.001):
            cases.append(dict(d=3, N=N, T=0.5, dt=dt, form="convective", tag="temporal"))
    for d, T in ((2, 0.1), (3, 0.1), (3, 0.5)):
        cases.append(dict(d=d, N=32, T=T, dt=0.001, form="rotational", tag="form_check"))
    cases.append(dict(d=3, N=64, T=0.5, dt=0.002, form="convective", tag="reference"))
    return cases


def sha256_of(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


OUT_DIR = None


def hist_at(res, t):
    rows = res.get("history")
    if rows is None:  # results.json is stored without histories; read the CSV instead
        rows = []
        with open(os.path.join(OUT_DIR, "histories", res["id"] + ".csv")) as fh:
            for rec in csv.DictReader(fh):
                rows.append({k: float(v) for k, v in rec.items()})
        rows = [dict(r, D=r["D"]) for r in rows]
    for row in rows:
        if abs(row["t"] - t) < 1e-12:
            return row
    raise KeyError(t)


def analyze(cases):
    by = {r["id"]: r for r in cases.values()}
    out = {}

    def pick(d, N, T, dt, form="convective"):
        return by.get(case_id(dict(d=d, N=N, T=T, dt=dt, form=form)))

    # t = 0 against analytic values
    out["t0_abs_error_max"] = {
        str(d): max(max(r["t0_abs_error"].values()) for r in by.values() if r["d"] == d) for d in (2, 3)
    }

    # spatial sensitivity at T = 0.1, dt = 0.001
    keys = ("E_T", "Omega_T", "eps_T", "D_int", "resid_abs")
    out["spatial_T0.1"] = {}
    for d in (2, 3):
        rows = {N: pick(d, N, 0.1, 0.001) for N in (16, 24, 32)}
        if all(rows.values()):
            out["spatial_T0.1"][str(d)] = {
                k: max(rows[N][k] for N in rows) - min(rows[N][k] for N in rows) for k in keys[:4]
            }

    # time-step sensitivity at T = 0.1
    out["dt_T0.1_N32"] = {}
    for d in (2, 3):
        base = pick(d, 32, 0.1, 0.001)
        for dt in (0.002, 0.0005):
            r = pick(d, 32, 0.1, dt)
            if base and r:
                out["dt_T0.1_N32"]["%dD_dt%g_vs_0.001" % (d, dt)] = {k: r[k] - base[k] for k in keys[:4]}

    # 3D temporal sensitivity at T = 0.5
    out["temporal_T0.5"] = {}
    for N in (16, 24, 32):
        r4, r2, r1 = (pick(3, N, 0.5, dt) for dt in (0.004, 0.002, 0.001))
        if r4 and r2 and r1:
            ent = {}
            for k in ("E_T", "Omega_T", "eps_T", "D_int"):
                d42, d21 = r4[k] - r2[k], r2[k] - r1[k]
                ent[k] = dict(
                    d_0p004_minus_0p002=d42,
                    d_0p002_minus_0p001=d21,
                    ratio=(d42 / d21) if d21 != 0 else None,
                    d_0p004_minus_0p001=r4[k] - r1[k],
                )
            out["temporal_T0.5"]["N%d" % N] = ent

    # convective vs rotational form
    out["form_check"] = {}
    for d, T in ((2, 0.1), (3, 0.1), (3, 0.5)):
        a, b = pick(d, 32, T, 0.001), pick(d, 32, T, 0.001, "rotational")
        if a and b:
            out["form_check"]["%dD_T%g" % (d, T)] = {k: b[k] - a[k] for k in keys[:4]}

    # N = 64 reference (3D, dt = 0.002)
    ref = pick(3, 64, 0.5, 0.002)
    if ref:
        out["vs_N64_ref"] = {}
        for N in (16, 24, 32):
            r = pick(3, N, 0.5, 0.002)
            if r:
                out["vs_N64_ref"]["T0.5_N%d_dt0.002" % N] = {k: r[k] - ref[k] for k in keys[:4]}
        h = hist_at(ref, 0.1)
        for N in (16, 24, 32):
            r = pick(3, N, 0.1, 0.001)
            if r:
                out["vs_N64_ref"]["T0.1_N%d_dt0.001" % N] = {
                    "E_T": r["E_T"] - h["E"], "Omega_T": r["Omega_T"] - h["Omega"],
                    "eps_T": r["eps_T"] - h["eps"], "D_int": r["D_int"] - h["D"],
                }
    return out


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", default=os.path.join(here, "outputs"))
    ap.add_argument("--tags", default="primary,dt_check,temporal,form_check",
                    help="comma-separated subset of: primary, dt_check, temporal, form_check, reference")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        r = run_case(dict(d=2, N=16, T=0.1, dt=0.001, form="convective", tag="selftest"))
        r3 = run_case(dict(d=3, N=16, T=0.1, dt=0.001, form="convective", tag="selftest"))
        assert max(r["t0_abs_error"].values()) < 1e-13 and max(r3["t0_abs_error"].values()) < 1e-13
        assert r["exact2d_max_abs_error"] < 1e-10, r["exact2d_max_abs_error"]
        assert abs(r3["resid_abs"]) < 1e-9 and r3["maxdiv_max_over_time"] < 1e-10
        print("selftest ok")
        return

    global OUT_DIR
    OUT_DIR = args.out
    os.makedirs(os.path.join(args.out, "histories"), exist_ok=True)
    res_path = os.path.join(args.out, "results.json")
    store = {}
    if os.path.exists(res_path):
        with open(res_path) as fh:
            store = json.load(fh).get("cases", {})

    wanted = set(args.tags.split(","))
    for c in build_cases():
        if c["tag"] not in wanted:
            continue
        r = run_case(c)
        store[r["id"]] = r
        with open(os.path.join(args.out, "histories", r["id"] + ".csv"), "w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["t", "E", "eps", "Omega", "maxdiv", "D"])
            for row in r["history"]:
                w.writerow([repr(row[k]) for k in ("t", "E", "eps", "Omega", "maxdiv", "D")])
        print("%-34s E_T=%.15g D=%.15g Om_T=%.15g resid=%.2e div=%.1e  %.2fs"
              % (r["id"], r["E_T"], r["D_int"], r["Omega_T"], r["resid_abs"], r["maxdiv_max_over_time"], r["runtime_s"]))

    slim = {k: {kk: vv for kk, vv in v.items() if kk != "history"} for k, v in store.items()}
    meta = dict(
        python=sys.version.split()[0], numpy=np.__version__, platform=platform.platform(),
        machine=platform.machine(), cpu_count=os.cpu_count(), precision="float64/complex128",
        fft="numpy.fft (pocketfft), single process", nu=NU,
        source_sha256=sha256_of(os.path.abspath(__file__)),
    )
    with open(res_path, "w") as fh:
        json.dump(dict(meta=meta, cases=slim, derived=analyze(store)), fh, indent=1, sort_keys=True)
    print("wrote", res_path)


if __name__ == "__main__":
    main()
