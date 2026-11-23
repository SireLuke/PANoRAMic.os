#!/usr/bin/env python3
"""NS Press II production run: Taylor-Green Re=1600, N=128, in-run phase-aware statistics (O1-O4) + shuffle ensemble.

Implements Section 4 of NS_PRESS_II_PREREGISTRATION.md. The solver core (rfftn pseudospectral, 2/3 dealiasing,
Leray projection, classical RK4, diagnostics, shell spectrum) is Press I's tg_press.py logic reproduced unchanged
in structure; tg_press.py itself runs at import and hard-codes host paths, so it cannot be imported.
Statistics conventions are those of press2_selftest.py (C1-C5) plus C6-C8 below.

*** NO RUN IS AUTHORIZED BY THE PREREGISTRATION. This file only provides the implementation. ***
Run only after the maintainer's separate go-ahead and his ruling on Section 6 of the preregistration.

Additional conventions pinned here (not in the draft; flagged in the filing PR for ruling):
  C6  A snapshot with W(t) <= 1e-3 * max_window(W) counts as NOT separating for O1/O3 (conservative).
  C7  O3 triads (k, q-k, -q): one representative per +-q pair (9 vectors with |q|^2 in {1,2}), Euclidean
      4 <= |k| <= 32 and |q-k| <= 32; all such triads are used (no sampling).
  C8  O2 shuffle ensembles are computed at the 0.25 statistics snapshots (the real O2 series is also recorded at
      the 0.025 diagnostic cadence, without ensemble).
Shuffle i at snapshot s uses numpy default_rng(SeedSequence([20261122 + i, s])), i = 0..M-1.
Usage:
  python -m experiments.navier_stokes.press2.tg_press2 run     --out DIR [--N 128 --M 100 --T 12 --dt 0.005]
  python -m experiments.navier_stokes.press2.tg_press2 analyze --out DIR [--tag TAG]
"""
import argparse, hashlib, json, os, sys, time
import numpy as np

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
if REPO not in sys.path:
    sys.path.insert(0, REPO)
from experiments.navier_stokes.press2 import press2_selftest as ST  # noqa: E402

SEED0 = 20261122
OUT_STEPS, SNAP_STEPS, CKPT_STEPS = 10, 25, 200       # 0.025, 0.25, 1.0 at dt = 0.005
WINDOW = (6.0, 10.0)
NEED, PCT, WFRAC = 9, 95.0, 1e-3


class Solver:
    def __init__(self, N, nu):
        n = self.n = N
        self.nu = nu
        k1 = np.fft.fftfreq(n, d=1.0 / n)
        kr = np.fft.rfftfreq(n, d=1.0 / n)
        self.KX, self.KY, self.KZ = np.meshgrid(k1, k1, kr, indexing="ij")
        self.K2 = self.KX ** 2 + self.KY ** 2 + self.KZ ** 2
        self.K2inv = np.where(self.K2 > 0, 1.0 / np.where(self.K2 > 0, self.K2, 1.0), 0.0)
        self.keep = (np.abs(self.KX) <= n / 3) & (np.abs(self.KY) <= n / 3) & (np.abs(self.KZ) <= n / 3)
        self.shell_idx = np.round(np.sqrt(self.K2)).astype(int).ravel()
        self.nshell = int(self.shell_idx.max()) + 1
        self.w = np.ones_like(self.KZ); self.w[:, :, 1:-1] = 2.0

    def init_tg(self):
        n = self.n
        x = 2 * np.pi * np.arange(n) / n
        X, Y, Z = np.meshgrid(x, x, x, indexing="ij")
        u0 = [np.sin(X) * np.cos(Y) * np.cos(Z), -np.cos(X) * np.sin(Y) * np.cos(Z), np.zeros_like(X)]
        return [np.fft.rfftn(u) / n ** 3 for u in u0]

    def project(self, vh):
        kd = self.KX * vh[0] + self.KY * vh[1] + self.KZ * vh[2]
        return [vh[i] - k * kd * self.K2inv for i, k in enumerate((self.KX, self.KY, self.KZ))]

    def rhs(self, vh):
        n = self.n
        v = [np.fft.irfftn(h * n ** 3, s=(n, n, n)) for h in vh]
        dv = [[np.fft.irfftn(1j * k * vh[j] * n ** 3, s=(n, n, n)) for j in range(3)] for k in (self.KX, self.KY, self.KZ)]
        nl = []
        for j in range(3):
            conv = v[0] * dv[0][j] + v[1] * dv[1][j] + v[2] * dv[2][j]
            nl.append(np.fft.rfftn(conv) / n ** 3 * self.keep)
        nl = self.project(nl)
        return [-nl[j] - self.nu * self.K2 * vh[j] for j in range(3)]

    def step(self, uh, dt):
        a = self.rhs(uh)
        b = self.rhs([uh[j] + 0.5 * dt * a[j] for j in range(3)])
        c = self.rhs([uh[j] + 0.5 * dt * b[j] for j in range(3)])
        d = self.rhs([uh[j] + dt * c[j] for j in range(3)])
        return [uh[j] + dt * (a[j] + 2 * b[j] + 2 * c[j] + d[j]) / 6.0 for j in range(3)]

    def diagnostics(self, vh):
        E = 0.5 * sum(np.sum(self.w * (h * np.conj(h)).real) for h in vh)
        grad2 = sum(np.sum(self.w * self.K2 * (h * np.conj(h)).real) for h in vh)
        return float(E), float(0.5 * grad2), float(self.nu * grad2)

    def vort_phys(self, vh):
        n = self.n
        wh = [1j * (self.KY * vh[2] - self.KZ * vh[1]), 1j * (self.KZ * vh[0] - self.KX * vh[2]),
              1j * (self.KX * vh[1] - self.KY * vh[0])]
        return [np.fft.irfftn(h * n ** 3, s=(n, n, n)) for h in wh]

    def max_vorticity(self, vh):
        w = self.vort_phys(vh)
        return float(np.max(np.sqrt(w[0] ** 2 + w[1] ** 2 + w[2] ** 2)))

    def flatness(self, vh):
        """O2: component-wise <w_i^4>/<w_i^2>^2 averaged over i."""
        return float(np.mean([np.mean(w ** 4) / np.mean(w ** 2) ** 2 for w in self.vort_phys(vh)]))

    def spectrum(self, vh):
        dens = 0.5 * sum(self.w * (h * np.conj(h)).real for h in vh)
        return np.bincount(self.shell_idx, weights=dens.ravel(), minlength=self.nshell)

    def full_hat(self, vh):
        n = self.n
        return np.array([np.fft.fftn(np.fft.irfftn(h * n ** 3, s=(n, n, n))) / n ** 3 for h in vh])


def front_K(E):
    """O4: smallest k with energy in shells > k below 1e-3 of total (Press I definition)."""
    total = E.sum(); above = total - np.cumsum(E)
    below = np.where(above < 1e-3 * total)[0]
    return int(below[0]) if len(below) else int(len(E) - 1)


def flat_index(N, k):
    return ((k[:, 0] % N) * N + (k[:, 1] % N)) * N + (k[:, 2] % N)


def o3_triads(N, kmin=4, kmax=32):
    """Convention C7."""
    K = ST.kvec(N).reshape(3, -1).T
    n2 = (K ** 2).sum(1)
    ball = K[(n2 >= kmin * kmin) & (n2 <= kmax * kmax)]
    qs = [np.array(q) for q in ((1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0), (1, -1, 0), (1, 0, 1), (1, 0, -1), (0, 1, 1), (0, 1, -1))]
    A, B, C = [], [], []
    for q in qs:
        r = q[None, :] - ball
        ok = (r ** 2).sum(1) <= kmax * kmax
        k, rr = ball[ok], r[ok]
        A.append(flat_index(N, k)); B.append(flat_index(N, rr)); C.append(flat_index(N, np.tile(-q, (len(k), 1))))
    a, b, c = np.concatenate(A), np.concatenate(B), np.concatenate(C)
    return a, b, c, dict(n_triads=int(len(a)), sha256=hashlib.sha256(np.stack([a, b, c]).tobytes()).hexdigest(), kmin=kmin, kmax=kmax)


class TriadStat:
    """Fast path for C_tri and W on the real field and on common-phase shuffles (convention C3: Phi_shuf = Phi + Theta)."""
    def __init__(self, amp, ph, tri):
        a, b, c = tri
        self.tri = tri
        w = amp[:, a] * amp[:, b] * amp[:, c]                       # (3, T)
        self.W = w.sum(1)                                           # (3,)
        self.Z = w * np.exp(1j * (ph[:, a] + ph[:, b] + ph[:, c]))  # (3, T)

    def value(self, theta=None):
        z = self.Z if theta is None else self.Z * np.exp(1j * (theta[self.tri[0]] + theta[self.tri[1]] + theta[self.tri[2]]))[None]
        C = np.abs(z.sum(1)) / np.where(self.W > 0, self.W, 1.0)
        return float(C.mean())

    def active_weight(self):
        return float(self.W.mean())


def snapshot(sv, uh, s, tri1, tri3, M, shuffle_ens=True):
    n = sv.n
    U = sv.full_hat(uh)
    amp = np.abs(U).reshape(3, -1); ph = np.angle(U).reshape(3, -1)
    t1, t3 = TriadStat(amp, ph, tri1), TriadStat(amp, ph, tri3)
    rec = dict(O1=t1.value(), W1=t1.active_weight(), O3=t3.value(), W3=t3.active_weight(), O2=sv.flatness(uh),
               E_shell=sv.spectrum(uh).tolist())
    rec["O4_K"] = front_K(np.array(rec["E_shell"]))
    if shuffle_ens:
        K = ST.kvec(n).astype(float)
        wh = np.array([1j * (K[1] * U[2] - K[2] * U[1]), 1j * (K[2] * U[0] - K[0] * U[2]), 1j * (K[0] * U[1] - K[1] * U[0])])
        e1, e2, e3 = [], [], []
        for m in range(M):
            rng = np.random.default_rng(np.random.SeedSequence([SEED0 + m, s]))
            theta = np.angle(np.fft.fftn(rng.normal(size=(n, n, n)))).reshape(-1)
            e1.append(t1.value(theta)); e3.append(t3.value(theta))
            ws = wh * np.exp(1j * theta.reshape(n, n, n))[None]
            om = [np.fft.ifftn(w_ * n ** 3).real for w_ in ws]
            e2.append(float(np.mean([np.mean(w_ ** 4) / np.mean(w_ ** 2) ** 2 for w_ in om])))
        rec.update(O1_ens=e1, O3_ens=e3, O2_ens=e2)
    return rec


def run(a):
    os.makedirs(a.out, exist_ok=True)
    N, nu, dt, T = a.N, 1.0 / a.Re, a.dt, a.T
    sv = Solver(N, nu)
    # frozen triad sets, saved with seeds before any stepping
    tri_path = os.path.join(a.out, "%s_triads.npz" % a.tag)
    ka = max(1, min(32, int(N // 4))) if a.kmax is None else a.kmax
    if os.path.exists(tri_path):
        z = np.load(tri_path, allow_pickle=True); tri1 = (z["a1"], z["b1"], z["c1"]); tri3 = (z["a3"], z["b3"], z["c3"]); meta = json.loads(str(z["meta"]))
    else:
        t1 = ST.triad_set(N, ka, a.cap, SEED0); tri1 = t1[:3]
        t3 = o3_triads(N, kmin=4, kmax=ka); tri3 = t3[:3]
        meta = dict(O1=t1[3], O3=t3[3])
        np.savez(tri_path, a1=tri1[0], b1=tri1[1], c1=tri1[2], a3=tri3[0], b3=tri3[1], c3=tri3[2], meta=json.dumps(meta))
    steps = int(round(T / dt))
    ckpt = os.path.join(a.out, "%s.ckpt.npz" % a.tag)
    hist = {"t": [], "E": [], "Om": [], "eps": [], "wmax": [], "O2_diag_t": [], "O2_diag": []}
    stats = {"t": [], "snap": []}
    start = 0
    if os.path.exists(ckpt):
        z = np.load(ckpt, allow_pickle=True)
        uh = [z["u%d" % j] for j in range(3)]; start = int(z["step"])
        hist = json.loads(str(z["hist"])); stats = json.loads(str(z["stats"]))
        print("resumed at step", start, flush=True)
    else:
        uh = sv.init_tg()
    t0 = time.time()

    def record_diag(s):
        E, Om, eps = sv.diagnostics(uh)
        hist["t"].append(s * dt); hist["E"].append(E); hist["Om"].append(Om); hist["eps"].append(eps)
        hist["wmax"].append(sv.max_vorticity(uh))
        hist["O2_diag_t"].append(s * dt); hist["O2_diag"].append(sv.flatness(uh))

    def record_snap(s):
        rec = snapshot(sv, uh, s // SNAP_STEPS, tri1, tri3, a.M)
        stats["t"].append(s * dt); stats["snap"].append(rec)

    if start == 0:
        record_diag(0); record_snap(0)
    for s in range(start + 1, steps + 1):
        uh = sv.step(uh, dt)
        if s % OUT_STEPS == 0:
            record_diag(s)
        if s % SNAP_STEPS == 0:
            record_snap(s)
        if s % CKPT_STEPS == 0:
            np.savez(ckpt, u0=uh[0], u1=uh[1], u2=uh[2], step=s, hist=json.dumps(hist), stats=json.dumps(stats))
            print("step %d/%d t=%.2f wall=%ds ckpt" % (s, steps, s * dt, time.time() - t0), flush=True)
    res = dict(tag=a.tag, N=N, nu=nu, Re=a.Re, T=T, dt=dt, M=a.M, seed0=SEED0, triads=meta, hist=hist, stats=stats,
               wall_s=time.time() - t0, conventions="press2_selftest C1-C5; tg_press2 C6-C8")
    path = os.path.join(a.out, "%s.json" % a.tag)
    json.dump(res, open(path, "w"))
    print("done ->", path, "wall", res["wall_s"])


def stage_a(hist):
    eps, t = np.array(hist["eps"]), np.array(hist["t"])
    i = int(np.argmax(eps))
    ratio = float(eps[i] / 0.01286)
    return dict(eps_max=float(eps[i]), t_eps_max=float(t[i]), ratio=ratio, dt_vs_ref=float(t[i] - 8.97),
                gate_pass=bool(0.95 <= ratio <= 1.10 and abs(t[i] - 8.97) <= 0.4))


def separation(real, ens, active=None, need=NEED, pct=PCT):
    thr = np.percentile(ens, pct, axis=1, method="linear")
    hit = np.asarray(real) > thr
    if active is not None:
        hit = hit & active
    return bool(hit.sum() >= need), int(hit.sum()), hit.tolist()


def analyze(res):
    t = np.array(res["stats"]["t"]); snaps = res["stats"]["snap"]
    win = (t >= WINDOW[0] - 1e-9) & (t <= WINDOW[1] + 1e-9)
    out = dict(n_snapshots=int(len(t)), n_window=int(win.sum()), stage_a=stage_a(res["hist"]))
    for name, wkey in (("O1", "W1"), ("O3", "W3"), ("O2", None)):
        real = np.array([s[name] for s in snaps])[win]
        ens = np.array([s[name + "_ens"] for s in snaps])[win]
        active = None
        if wkey:
            W = np.array([s[wkey] for s in snaps])[win]
            active = W > WFRAC * W.max()
        ok, cnt, hit = separation(real, ens, active)
        M = ens.shape[1]
        nfp = 0
        for j in range(M):
            ok_j, _, _ = separation(ens[:, j], np.delete(ens, j, axis=1), active)
            nfp += ok_j
        out[name] = dict(separates=ok, hit_count=cnt, hits=hit, null_false_positive_rate=nfp / M,
                         real_mean=float(real.mean()), shuffle_mean=float(ens.mean()),
                         active_snapshots=None if active is None else int(active.sum()))
    o1, o3, o2 = out["O1"]["separates"], out["O3"]["separates"], out["O2"]["separates"]
    if not out["stage_a"]["gate_pass"]:
        v = "RUN VOID: Stage A gate failed; no Stage C2 verdict is read"
    elif not o2:
        v = "RUN SUSPECT: O2 witness did not separate; implementation review before any verdict is read"
    elif not o1:
        v = "O1 fails: phase-aware repair fails at N=128 (negative result)"
    elif not o3:
        v = "O1 passes, O3 fails: triadic coherence detectable, antipodal entry refuted (sharper negative)"
    else:
        v = "O1 and O3 pass: a phase-aware entry detects coherent dynamics at this resolution"
    out["verdict_text"] = v
    out["fence"] = "Navier-Stokes remains not_tested under every outcome. Positive-control self-test is run separately (press2_selftest.py)."
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["run", "analyze"])
    ap.add_argument("--out", required=True)
    ap.add_argument("--N", type=int, default=128); ap.add_argument("--Re", type=float, default=1600.0)
    ap.add_argument("--T", type=float, default=12.0); ap.add_argument("--dt", type=float, default=0.005)
    ap.add_argument("--M", type=int, default=100); ap.add_argument("--cap", type=int, default=200000)
    ap.add_argument("--kmax", type=int, default=None, help="triad |k| bound; default 32 at N=128 (N//4 for smaller smoke runs)")
    ap.add_argument("--tag", default="press2_re1600_n128")
    a = ap.parse_args()
    if a.N == 128 and a.kmax is None:
        a.kmax = 32
    if a.cmd == "run":
        run(a)
    else:
        res = json.load(open(os.path.join(a.out, "%s.json" % a.tag)))
        r = analyze(res)
        json.dump(r, open(os.path.join(a.out, "%s_analysis.json" % a.tag), "w"), indent=1)
        print(json.dumps(r, indent=1))


if __name__ == "__main__":
    main()
