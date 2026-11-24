#!/usr/bin/env python3
"""EQBIT-DRIFT-001 extension 4: complex (Peierls-type) hopping phases on the E8 root graph.
Architect bench (Claude). Analogy rung only. Closed unitary system, exact diagonalization, 240 x 240.

PREREGISTRATION (frozen in this header BEFORE any run of this script)
---------------------------------------------------------------------
Why        : every earlier experiment used a real symmetric H, for which P(a->b,t) = P(b->a,t) exactly.
             Complex hopping phases break that identity. This is the standard closed-system route to
             direction-dependent transport, and the one the breathing drive only imitated through timing.
Model      : H_uv = A_uv * exp(i Theta_uv), Theta antisymmetric (Theta_vu = -Theta_uv) so H is Hermitian.
             Roots in true coordinates V8 (norm^2 2), root 0 = pole, antipode = root with dot -8 (scaled).
Families (phase per edge, alpha is the strength):
  J    : Theta_uv = alpha * (u^T J v), J = block-diag of four 2x2 rotation generators on coordinate
         pairs (0,1),(2,3),(4,5),(6,7). A geometric 'symplectic' phase; breaks the E8 symmetry to the
         subgroup preserving J, so the 5-orbit quotient no longer applies.
  ord  : Theta_uv = alpha * sign(v - u) in the root enumeration order (an arbitrary but fixed
         orientation; shows the result is not an artifact of the J choice).
  gauge: Theta_uv = alpha * (g_u - g_v), g_v = v . n along the pole axis. EXACT pure gauge (H is
         D H0 D^dagger with D = diag(exp(i alpha g))): it must change NOTHING. Control.
alpha grid : {0.05, 0.1, 0.25, 0.5, 1.0, pi/2}.  Baseline alpha = 0.
Dynamics   : U = exp(-iHt), numpy eigh on the complex Hermitian matrix, t in [0, 200], dt = 0.005 grid,
             maxima refined locally (ternary search).
Starts     : root 0 (single vertex) and its antipode. Statistics per (family, alpha):
  E = max_t P(antipode | start 0),  A = max_t P(0 | start antipode),  avgE, avgA (grid time averages),
  Dmax = max_t |P(anti|0) - P(0|anti)|   (instantaneous non-reciprocity),
  Dbar = mean_t [P(anti|0) - P(0|anti)]  (net, time-averaged direction asymmetry),
  plus triangle-flux statistics: fraction of the 60,480 triangles with |sin(flux/2)| > 1e-9.
Gates (all computed in code):
  HG0 Hermiticity max|H - H^dagger| < 1e-15 and eigenvector unitarity < 1e-10, every run.
  HG1 alpha = 0: E = A = 0.8820834325 within 1e-9 and Dmax < 1e-10 (static real symmetric reciprocity).
  HG2 gauge control: P(anti|0) and P(0|anti) series equal the alpha = 0 series within 1e-9 for every alpha;
      gauge triangle flux max |sin(flux/2)| < 1e-12.
  HG3 sign identity: P_{-alpha}(anti|0)(t) == P_{alpha}(0|anti)(t) within 1e-10 (J and ord at alpha = 0.5),
      since H(-alpha) = H(alpha)^T and U^T relates the two directions.
  HG4 J and ord at alpha = 0.5 have a nonzero-flux triangle fraction > 0.5 (the phases are not accidentally trivial).
Expectation (registered, NOT a gate; reported as found): the time-averaged asymmetry Dbar should be ~0 for a
  generic (non-degenerate) spectrum, because the diagonal-ensemble average of |<b|k><k|a>|^2 is symmetric
  in a <-> b. If so, closed-system non-reciprocity is a transient timing effect, not a net current.
Claim rules (conservative):
  'Non-reciprocity' is claimed at (family, alpha) only if Dmax > 1e-2.
  'Net one-way transport' is claimed only if |Dbar| > 1e-2.
  'Peak enhancement' is claimed only if max(E, A) exceeds the alpha = 0 ceiling 0.882083 by > 1e-2; max-over-window
  is a weak statistic in a small spectrum (lesson of the breathing drive), so the time average is always reported alongside.
  No horizon/gravity language; three depth classes still forbid any exponential-law claim.
"""
import json
from pathlib import Path
import numpy as np

import hallway_crosshair as hc

HERE = Path(__file__).resolve().parent
T_MAX, DT = 200.0, 0.005
ALPHAS = [0.05, 0.1, 0.25, 0.5, 1.0, np.pi / 2]
V8, A, ANTI = hc.V8, hc.A, hc.anti
N = 240
IDX = np.arange(N)
JMAT = np.zeros((8, 8))
for k in range(4):
    JMAT[2 * k, 2 * k + 1] = 1.0
    JMAT[2 * k + 1, 2 * k] = -1.0
M_J = V8 @ JMAT @ V8.T                                   # antisymmetric
S_ORD = np.sign(np.subtract.outer(IDX, IDX)).astype(float) * -1  # S[u,v] = +1 if v>u
G_AX = V8 @ hc.N_AX
M_GAUGE = G_AX[:, None] - G_AX[None, :]
BASE = {"J": M_J, "ord": S_ORD, "gauge": M_GAUGE}

assert np.allclose(M_J, -M_J.T) and np.allclose(S_ORD, -S_ORD.T) and np.allclose(M_GAUGE, -M_GAUGE.T)


def hamiltonian(family, alpha):
    if alpha == 0.0:
        return A.astype(complex)
    return A * np.exp(1j * alpha * BASE[family])


def triangles():
    tris = []
    for u in range(N):
        for v in np.nonzero(A[u])[0]:
            if v <= u:
                continue
            ws = np.nonzero(A[u] * A[v])[0]
            for w in ws[ws > v]:
                tris.append((u, v, w))
    return np.array(tris)


TRI = triangles()
assert len(TRI) == 60480, len(TRI)


def flux_stats(family, alpha):
    Th = alpha * BASE[family]
    fl = Th[TRI[:, 0], TRI[:, 1]] + Th[TRI[:, 1], TRI[:, 2]] + Th[TRI[:, 2], TRI[:, 0]]
    s = np.abs(np.sin(fl / 2))
    return {"nonzero_flux_fraction": float((s > 1e-9).mean()), "max_abs_sin_half_flux": float(s.max()),
            "mean_abs_sin_half_flux": float(s.mean())}


def series(w, Vm, start, target, t, chunk=4000):
    c = Vm.conj().T[:, start]
    out = np.empty(len(t))
    for s in range(0, len(t), chunk):
        tt = t[s:s + chunk]
        amp = Vm[target, :] @ (np.exp(-1j * np.outer(w, tt)) * c[:, None])
        out[s:s + chunk] = np.abs(amp) ** 2
    return out


def refine(w, Vm, start, target, t0, half=0.02):
    f = lambda tt: series(w, Vm, start, target, tt)
    ts = np.linspace(max(t0 - half, 0), min(t0 + half, T_MAX), 201)
    v = f(ts); j = int(v.argmax())
    lo, hi = ts[max(j - 1, 0)], ts[min(j + 1, 200)]
    for _ in range(60):
        m1, m2 = lo + (hi - lo) / 3, hi - (hi - lo) / 3
        if f(np.array([m1]))[0] < f(np.array([m2]))[0]:
            lo = m1
        else:
            hi = m2
    tr = 0.5 * (lo + hi)
    return float(f(np.array([tr]))[0]), float(tr)


T = np.arange(0, T_MAX + 1e-9, DT)


def run(family, alpha):
    H = hamiltonian(family, alpha)
    herm = float(np.abs(H - H.conj().T).max())
    w, Vm = np.linalg.eigh(H)
    unit = float(np.abs(Vm.conj().T @ Vm - np.eye(N)).max())
    PE = series(w, Vm, 0, ANTI, T)       # start 0 -> antipode
    PA = series(w, Vm, ANTI, 0, T)       # start antipode -> 0
    ep, et = refine(w, Vm, 0, ANTI, T[PE.argmax()])
    ap, at = refine(w, Vm, ANTI, 0, T[PA.argmax()])
    E = max(ep, float(PE.max())); A_ = max(ap, float(PA.max()))
    rec = {"family": family, "alpha": float(alpha), "E": E, "t_E": et, "A": A_, "t_A": at,
           "avgE": float(PE.mean()), "avgA": float(PA.mean()),
           "Dmax": float(np.abs(PE - PA).max()), "Dbar": float((PE - PA).mean()),
           "herm_dev": herm, "unitarity_dev": unit}
    rec.update(flux_stats(family, alpha) if alpha != 0.0 else {"nonzero_flux_fraction": 0.0, "max_abs_sin_half_flux": 0.0, "mean_abs_sin_half_flux": 0.0})
    return rec, PE, PA


if __name__ == "__main__":
    rows, store = [], {}
    r0, PE0, PA0 = run("J", 0.0)
    r0["family"] = "baseline"
    rows.append(r0); store[("baseline", 0.0)] = (PE0, PA0)
    for fam in ("J", "ord", "gauge"):
        for a in ALPHAS:
            r, PE, PA = run(fam, a)
            rows.append(r); store[(fam, float(a))] = (PE, PA)
            print(f"{fam:6s} alpha={a:6.4f} E={r['E']:.4f} A={r['A']:.4f} avgE={r['avgE']:.4f} avgA={r['avgA']:.4f} Dmax={r['Dmax']:.4f} Dbar={r['Dbar']:+.2e} flux>0:{r['nonzero_flux_fraction']:.3f}")
    gates = {}
    gates["HG0_hermitian_unitary"] = bool(all(r["herm_dev"] < 1e-15 and r["unitarity_dev"] < 1e-10 for r in rows))
    gates["HG1_alpha0_ceiling_and_reciprocity"] = bool(abs(r0["E"] - 0.8820834325) < 1e-9 and abs(r0["A"] - 0.8820834325) < 1e-9 and r0["Dmax"] < 1e-10)
    g2 = max(max(np.abs(store[("gauge", float(a))][0] - PE0).max(), np.abs(store[("gauge", float(a))][1] - PE0).max()) for a in ALPHAS)
    gflux = max(r["max_abs_sin_half_flux"] for r in rows if r["family"] == "gauge")
    gates["HG2_gauge_changes_nothing"] = bool(g2 < 1e-9 and gflux < 1e-12)
    gates["HG2_values"] = {"max_series_diff": float(g2), "max_gauge_flux": float(gflux)}
    # HG3: P_{-alpha}(anti|0) == P_alpha(0|anti)
    hg3 = {}
    for fam in ("J", "ord"):
        Hm = hamiltonian(fam, -0.5)
        w, Vm = np.linalg.eigh(Hm)
        PEm = series(w, Vm, 0, ANTI, T)
        hg3[fam] = float(np.abs(PEm - store[(fam, 0.5)][1]).max())
    gates["HG3_sign_identity"] = bool(all(v < 1e-10 for v in hg3.values()))
    gates["HG3_values"] = hg3
    gates["HG4_flux_nontrivial"] = bool(all(next(r for r in rows if r["family"] == f and abs(r["alpha"] - 0.5) < 1e-12)["nonzero_flux_fraction"] > 0.5 for f in ("J", "ord")))
    verdicts = []
    for r in rows:
        if r["family"] == "baseline":
            continue
        r["nonreciprocity_claim"] = bool(r["Dmax"] > 1e-2)
        r["net_oneway_claim"] = bool(abs(r["Dbar"]) > 1e-2)
        r["peak_enhancement_claim"] = bool(max(r["E"], r["A"]) > 0.882083 + 1e-2)
    res = {"gates": gates, "rows": rows}
    json.dump(res, open(HERE / "outputs" / "eqbit_drift_001_hopping.json", "w"), indent=1,
              default=lambda o: bool(o) if isinstance(o, np.bool_) else float(o))
    print("\nGATES", {k: v for k, v in gates.items()})
    print("\nfamily alpha | nonrecip net-oneway peak-enh | max|Dbar| by family:")
    for fam in ("J", "ord", "gauge"):
        rr = [r for r in rows if r["family"] == fam]
        print(fam, "max Dmax", round(max(r["Dmax"] for r in rr), 4), " max|Dbar|", f"{max(abs(r['Dbar']) for r in rr):.2e}",
              " claims nonrecip:", sum(r["nonreciprocity_claim"] for r in rr), " net:", sum(r["net_oneway_claim"] for r in rr), " enh:", sum(r["peak_enhancement_claim"] for r in rr))
