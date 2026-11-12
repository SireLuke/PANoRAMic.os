"""Gaussian-splat representation of hydrogenic orbital densities (reference generator).

Fits a weighted Gaussian mixture to |psi_nlm|^2 for real orbitals (atomic units, a0 = 1; exact
hydrogen from ``core.abom_v8.hydrogen_baseline`` radial functions and real harmonics l <= 2).
Each splat is (mean, covariance, weight, sign): weights sum to 1 (probability), sign is the
orbital's lobe sign (display hue). This is a rendering aid for an accurate density, not new physics:
the mixture is judged against the exact density by the metrics returned in ``quality``.

Limits: infinite nuclear mass, no spin/relativity; anisotropic Gaussians smear sharp radial nodes,
so ``node_depth`` (fitted density at a node / its maximum) is reported, not assumed to be zero.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from core.abom_v8 import hydrogen_baseline as HB

STATES = [(1, 0, 0), (2, 0, 0), (2, 1, 0), (3, 0, 0), (3, 1, 0), (3, 2, 0), (3, 2, 1), (3, 2, 2)]
EXTENT = {1: 9.0, 2: 24.0, 3: 50.0}        # box half-width (a0), enough to hold > 99.9% probability
GRID = 72
SEED = 11


def _real_ylm(l, m, x, y, z):
    r = np.sqrt(x * x + y * y + z * z)
    pi = math.pi
    with np.errstate(divide="ignore", invalid="ignore"):
        if l == 0:
            return np.full_like(x, 1 / (2 * math.sqrt(pi)))
        if l == 1:
            return np.where(r > 0, math.sqrt(3 / (4 * pi)) * {0: z, 1: x, -1: y}[m] / np.where(r > 0, r, 1), 0.0)
        c = {0: 0.25 * math.sqrt(5 / pi) * (3 * z * z - r * r), 1: 0.5 * math.sqrt(15 / pi) * x * z,
             -1: 0.5 * math.sqrt(15 / pi) * y * z, 2: 0.25 * math.sqrt(15 / pi) * (x * x - y * y),
             -2: 0.5 * math.sqrt(15 / pi) * x * y}[m]
        return np.where(r > 0, c / np.where(r > 0, r, 1) ** 2, 0.0)


def _radial(n, l, r):
    return np.vectorize(lambda v: HB.radial(n, l, float(v)))(r) if r.size < 50 else _radial_fast(n, l, r)


def _radial_fast(n, l, x):
    s, e = math.sqrt, np.exp
    return {(1, 0): lambda: 2 * e(-x), (2, 0): lambda: (1 / s(2)) * (1 - x / 2) * e(-x / 2),
            (2, 1): lambda: (1 / (2 * s(6))) * x * e(-x / 2),
            (3, 0): lambda: (2 / (3 * s(3))) * (1 - 2 * x / 3 + 2 * x * x / 27) * e(-x / 3),
            (3, 1): lambda: (8 / (27 * s(6))) * x * (1 - x / 6) * e(-x / 3),
            (3, 2): lambda: (4 / (81 * s(30))) * x * x * e(-x / 3)}[(n, l)]()


def psi_grid(n, l, m, half, grid=GRID):
    ax = (np.arange(grid) + 0.5) / grid * 2 * half - half
    x, y, z = np.meshgrid(ax, ax, ax, indexing="ij")
    r = np.sqrt(x * x + y * y + z * z)
    return _radial_fast(n, l, r) * _real_ylm(l, m, x, y, z), np.stack([x, y, z], -1).reshape(-1, 3), (2 * half / grid) ** 3


def _kmeanspp(pts, w, k, rng):
    idx = [rng.choice(len(pts), p=w / w.sum())]
    d2 = np.sum((pts - pts[idx[0]]) ** 2, 1)
    for _ in range(k - 1):
        p = d2 * w
        idx.append(rng.choice(len(pts), p=p / p.sum()))
        d2 = np.minimum(d2, np.sum((pts - pts[idx[-1]]) ** 2, 1))
    return pts[idx]


def weighted_gmm(pts, w, k, rng, iters=60, reg=1e-4):
    """EM for a Gaussian mixture where each point carries probability mass w (sum to 1)."""
    mu = _kmeanspp(pts, w, k, rng)
    cov = np.array([np.eye(3) * 0.5 for _ in range(k)])
    pi = np.full(k, 1.0 / k)
    for _ in range(iters):
        logp = np.empty((len(pts), k))
        for j in range(k):
            d = pts - mu[j]
            inv = np.linalg.inv(cov[j]); _, logdet = np.linalg.slogdet(cov[j])
            logp[:, j] = np.log(pi[j] + 1e-300) - 0.5 * (np.einsum("ni,ij,nj->n", d, inv, d) + logdet + 3 * math.log(2 * math.pi))
        logp -= logp.max(1, keepdims=True)
        resp = np.exp(logp); resp /= resp.sum(1, keepdims=True)
        rw = resp * w[:, None]
        nk = rw.sum(0) + 1e-300
        pi = nk / nk.sum()
        mu = (rw.T @ pts) / nk[:, None]
        for j in range(k):
            d = pts - mu[j]
            cov[j] = (rw[:, j, None] * d).T @ d / nk[j] + reg * np.eye(3)
    return pi, mu, cov


def mixture_density(pi, mu, cov, pts):
    out = np.zeros(len(pts))
    for j in range(len(pi)):
        d = pts - mu[j]
        inv = np.linalg.inv(cov[j]); det = np.linalg.det(cov[j])
        out += pi[j] * np.exp(-0.5 * np.einsum("ni,ij,nj->n", d, inv, d)) / math.sqrt((2 * math.pi) ** 3 * det)
    return out


def fit_orbital(n, l, m, k_per_lobe=6, seed=SEED):
    half = EXTENT[n]
    psi, pts, dv = psi_grid(n, l, m, half)
    rho = (psi ** 2).reshape(-1)
    sign = np.sign(psi.reshape(-1))
    mass = rho * dv
    total = mass.sum()
    keep = mass > 1e-9 * total
    rng = np.random.default_rng([seed, n, l, m + 5])
    splats = []
    for s in (1.0, -1.0):
        sel = keep & (sign == s)
        if sel.sum() < 50 or mass[sel].sum() < 1e-6 * total:
            continue
        frac = mass[sel].sum() / total
        k = max(2, int(round(k_per_lobe * (2 if (n, l) != (1, 0) else 1) * max(frac, 0.25) * 2)))
        pi, mu, cov = weighted_gmm(pts[sel], mass[sel] / mass[sel].sum(), k, rng)
        for j in range(len(pi)):
            splats.append({"mean": mu[j].tolist(), "cov": cov[j].tolist(), "weight": float(pi[j] * frac), "sign": int(s)})
    raw = sum(s_["weight"] for s_ in splats)
    tail_dropped = 1.0 - raw                                  # probability mass in tiny-density voxels
    for s_ in splats:
        s_["weight"] /= raw
    pi = np.array([s["weight"] for s in splats]); mu = np.array([s["mean"] for s in splats])
    cov = np.array([s["cov"] for s in splats])
    fit = mixture_density(pi / pi.sum(), mu, cov, pts)
    exact = mass / dv / total
    err = float(np.linalg.norm(fit - exact) / np.linalg.norm(exact))
    r_fit = float(np.sum(fit * np.linalg.norm(pts, axis=1)) * dv / (np.sum(fit) * dv))
    r_exact = 1.5 * n * n - l * (l + 1) / 2.0
    q = {"splats": len(splats), "relative_l2_error": err, "weight_sum": float(pi.sum()),
         "captured_probability": float(total), "tail_mass_dropped": float(tail_dropped),
         "mean_radius_fit_a0": r_fit, "mean_radius_exact_a0": r_exact,
         "mean_radius_rel_error": abs(r_fit - r_exact) / r_exact}
    nodes = HB.radial_nodes(n, l)
    if nodes:
        rr = np.linalg.norm(pts, axis=1)
        nd = []
        spacing = 2 * half / GRID
        for r0 in nodes:
            band = np.abs(rr - r0) < spacing
            nd.append(float(fit[band].mean() / fit.max()))
        q["fitted_density_at_radial_nodes_over_max"] = nd
    return {"state": [n, l, m], "splats": splats, "quality": q}


def main(path=None):
    out = [fit_orbital(*s) for s in STATES]
    for o in out:
        print(o["state"], json.dumps({k: (round(v, 4) if isinstance(v, float) else v) for k, v in o["quality"].items() if k != "fitted_density_at_radial_nodes_over_max"}),
              o["quality"].get("fitted_density_at_radial_nodes_over_max"))
    if path:
        def rnd(v):
            if isinstance(v, float):
                return round(v, 6)
            if isinstance(v, list):
                return [rnd(x) for x in v]
            if isinstance(v, dict):
                return {k: rnd(x) for k, x in v.items()}
            return v
        json.dump(rnd(out), open(path, "w"), separators=(",", ":"))
    return out


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
