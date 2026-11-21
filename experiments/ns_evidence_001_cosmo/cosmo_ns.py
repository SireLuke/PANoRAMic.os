"""Cosmo's independent third-seat run of the NS-EVIDENCE-001 benchmark.

Written from the benchmark SPEC (experiments/navier_stokes/NS_EVIDENCE_001.md)
and the public test contract only. Neither OpenAI's ns_spectral.py nor
Claude's replication code/results were read. NOTE: the spec document itself
prints OpenAI's results table, so target values were visible; the
implementation and all arithmetic below are independent.

Method (own implementation): Fourier-space state, pseudospectral nonlinear
term with 2/3 dealiasing, Leray projection, classical RK4, viscous term
spectral. Diagnostics by Parseval sums over Fourier coefficients.
"""
import json, math
import numpy as np


def validate_time_grid(T, dt):
    """Return an integer step count only when dt lands exactly on T.

    Rejecting a mismatched grid prevents round(T / dt) from silently
    integrating to a different final time than the requested T.
    """
    if not math.isfinite(T) or T <= 0:
        raise ValueError("T must be a finite positive number")
    if not math.isfinite(dt) or dt <= 0:
        raise ValueError("dt must be a finite positive number")
    steps = int(round(T / dt))
    if steps < 1 or not math.isclose(steps * dt, T, rel_tol=1e-12, abs_tol=1e-14):
        raise ValueError(
            f"T={T} is not an integer multiple of dt={dt}; "
            f"round(T/dt) gives {steps} steps ending at {steps * dt}"
        )
    return steps


def wavenumbers(n, d):
    k1 = np.fft.fftfreq(n, d=1.0 / n)  # integer wavenumbers
    grids = np.meshgrid(*([k1] * d), indexing="ij")
    return [g.astype(float) for g in grids]

def taylor_green(n, d):
    x1 = 2.0 * np.pi * np.arange(n) / n
    grids = np.meshgrid(*([x1] * d), indexing="ij")
    if d == 2:
        X, Y = grids
        return [np.sin(X) * np.cos(Y), -np.cos(X) * np.sin(Y)]
    X, Y, Z = grids
    return [np.sin(X) * np.cos(Y) * np.cos(Z),
            -np.cos(X) * np.sin(Y) * np.cos(Z),
            np.zeros_like(X)]

def run_case(n, d, nu=0.01, T=0.1, dt=0.001):
    ks = wavenumbers(n, d)
    k2 = sum(k ** 2 for k in ks)
    # 2/3 dealiasing mask: keep |k_i| <= n/3 per component
    keep = np.ones((n,) * d, dtype=bool)
    k1 = np.fft.fftfreq(n, d=1.0 / n)
    mask1 = np.abs(k1) <= n / 3.0
    for ax in range(d):
        shape = [1] * d; shape[ax] = n
        keep &= mask1.reshape(shape)
    u = taylor_green(n, d)
    uh = [np.fft.fftn(ui) / n ** d for ui in u]

    def project(vh):
        kdotv = sum(ks[i] * vh[i] for i in range(d))
        out = []
        for i in range(d):
            corr = np.where(k2 > 0, ks[i] * kdotv / np.where(k2 > 0, k2, 1.0), 0.0)
            out.append(vh[i] - corr)
        out = [np.where(k2 > 0, o, vh[i]) if False else o for i, o in enumerate(out)]
        # zero mode untouched (k2=0 -> corr=0 already)
        return out

    def rhs(vh):
        # physical velocity
        v = [np.fft.ifftn(h * n ** d).real for h in vh]
        # grad v_j componentwise: d_i v_j in Fourier space
        dv = [[np.fft.ifftn(1j * ks[i] * vh[j] * n ** d).real for j in range(d)] for i in range(d)]
        nl = []
        for j in range(d):
            conv = sum(v[i] * dv[i][j] for i in range(d))
            nlh = np.fft.fftn(conv) / n ** d
            nl.append(nlh * keep)
        nl = project(nl)
        return [-(nl[j]) - nu * k2 * vh[j] for j in range(d)]

    def diagnostics(vh):
        E = 0.5 * sum(np.sum(np.abs(h) ** 2) for h in vh)
        grad2 = sum(np.sum(k2 * np.abs(h) ** 2) for h in vh)  # <|grad u|^2>
        D = nu * grad2
        if d == 2:
            om = 1j * (ks[0] * vh[1] - ks[1] * vh[0])
            Om = 0.5 * np.sum(np.abs(om) ** 2)
        else:
            w = [1j * (ks[1] * vh[2] - ks[2] * vh[1]),
                 1j * (ks[2] * vh[0] - ks[0] * vh[2]),
                 1j * (ks[0] * vh[1] - ks[1] * vh[0])]
            Om = 0.5 * sum(np.sum(np.abs(wi) ** 2) for wi in w)
        div = sum(ks[i] * vh[i] for i in range(d))
        maxdiv = float(np.max(np.abs(div)))
        return float(E), float(D), float(Om), maxdiv

    steps = int(round(T / dt))
    steps = validate_time_grid(T, dt)
    E0, D0, Om0, _ = diagnostics(uh)
    Ds = [D0]
    for s in range(steps):
        k_a = rhs(uh)
        ub = [uh[j] + 0.5 * dt * k_a[j] for j in range(d)]
        k_b = rhs(ub)
        uc = [uh[j] + 0.5 * dt * k_b[j] for j in range(d)]
        k_c = rhs(uc)
        ud = [uh[j] + dt * k_c[j] for j in range(d)]
        k_d = rhs(ud)
        uh = [uh[j] + dt * (k_a[j] + 2 * k_b[j] + 2 * k_c[j] + k_d[j]) / 6.0 for j in range(d)]
        _, Dsamp, _, _ = diagnostics(uh)
        Ds.append(Dsamp)
    ET, DT, OmT, maxdiv = diagnostics(uh)
    trap = float(np.trapz(np.array(Ds), dx=dt))
    res = {"n": n, "d": d, "nu": nu, "T": T, "dt": dt, "steps": steps,
           "E0": E0, "ET": ET, "OmT": OmT, "max_div_T": maxdiv,
           "balance_residual": E0 - ET - trap}
    if d == 2:
        decay = math.exp(-2.0 * nu * T)
        u0 = taylor_green(n, d)
        uf = [np.fft.ifftn(h * n ** d).real for h in uh]
        err = math.sqrt(sum(np.mean((uf[j] - decay * u0[j]) ** 2) for j in range(d)))
        ref = math.sqrt(sum(np.mean((decay * u0[j]) ** 2) for j in range(d)))
        res["exact_relative_rms_error"] = err / ref
    return res

if __name__ == "__main__":
    out = {"seat": "Cosmo (Memory bench), third seat, independent implementation",
           "blindness_note": "Spec read for configuration; the spec itself prints OpenAI's table, so targets were visible. Implementation independent; neither bench's code or result files read.",
           "cases": []}
    for n in (16, 24, 32):
        out["cases"].append(run_case(n, 2, dt=0.002))
    for n in (16, 24, 32):
        out["cases"].append(run_case(n, 3, dt=0.001))
    for dt in (0.004, 0.002, 0.001):
        out["cases"].append(run_case(16, 3, T=0.5, dt=dt))
    path = "/home/hatch/workspace/goals/panoramic-os-and-pan-fractal-kernel-review/hidden_files/ns-evidence-cosmo/cosmo_results.json"
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
    for c in out["cases"]:
        print(c)
    print("frozen ->", path)
