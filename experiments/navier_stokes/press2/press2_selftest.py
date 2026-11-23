#!/usr/bin/env python3
"""NS Press II calibration self-test (pre-run). Statistic recomputes only; no Navier-Stokes integration.

Implements, as written in the Press II preregistration (section 3), on declared conventions listed below:
  * the triad set for O1 (Euclidean |k|,|p|,|q| <= kmax, k+p+q = 0, seeded sample if the count exceeds the cap)
  * the Hermitian-symmetric phase shuffle that preserves |u_hat(k)| exactly
  * the O1 statistic C_tri and the active weight W
  * the separation rule (real beats the 95th percentile of its own M-shuffle ensemble at >= 9 of 17 snapshots)
  * the null calibration (each shuffle treated as 'real' against the other M-1) and a planted-coherence control.

Conventions this script PINS because the draft text does not (flagged for ruling in the filing PR, section 6):
  C1  Norm: |k| is the Euclidean norm.
  C2  Vector field: C_tri is computed per Cartesian component i (amplitude |u_i(k)|, phase arg u_i(k)) and the
      reported C_tri and W are the means over i = 0,1,2.
  C3  Shuffle: u_hat(k) -> u_hat(k) * exp(i theta_k) with ONE phase theta_k shared by all three components
      (theta_{-k} = -theta_k, theta_0 = 0), obtained as arg FFT of real Gaussian noise. This keeps |u_i(k)|
      exactly and keeps k . u_hat = 0, so a shuffled field is still solenoidal.
  C4  Percentile: numpy 'linear' interpolation; strict '>' for the real value exceeding the threshold.
  C5  Planted control: built at the statistic level, u_i(k) = |u_i(k)| exp(-i k.x0 + i sigma g_k); solenoidality is
      not enforced because O1 reads only amplitudes and phases.
The real run's own statistics module must use these same conventions or the ruling must change them here first."""
import argparse, hashlib, json, math, os, sys, time
import numpy as np

M_DEFAULT, NSNAP_WINDOW, NEED, PCT = 100, 17, 9, 95.0


def kvec(N):
    k1 = np.fft.fftfreq(N, d=1.0 / N).astype(int)
    return np.array(np.meshgrid(k1, k1, k1, indexing="ij"))


def triad_set(N, kmax, cap, seed):
    """Return (idx_k, idx_p, idx_q) flat indices into an N^3 spectrum, and metadata. Triads are k+p+q=0 with all
    three non-zero and Euclidean norm <= kmax; (k,p,q) up to permutation and global sign. Full enumeration if the
    count (before symmetry reduction) is <= 4*cap, else seeded rejection sampling to `cap` distinct triads."""
    K = kvec(N).reshape(3, -1).T
    n2 = (K ** 2).sum(1)
    ball = np.nonzero((n2 > 0) & (n2 <= kmax * kmax))[0]
    pts = K[ball]
    lookup = {tuple(v): i for i, v in zip(ball.tolist(), pts)}
    rng = np.random.default_rng(np.random.SeedSequence([seed, 1]))
    seen, out = set(), []
    attempts = 0
    target = cap

    # index of -k for each flat index
    idx = np.arange(N ** 3).reshape(N, N, N)
    negidx = np.roll(np.flip(idx, axis=(0, 1, 2)), 1, axis=(0, 1, 2)).reshape(-1)
    while len(out) < target and attempts < 200 * target:
        attempts += 1
        a = int(ball[rng.integers(len(ball))]); b = int(ball[rng.integers(len(ball))])
        c_vec = -(K[a] + K[b])
        key = tuple(c_vec)
        c = lookup.get(key)
        if c is None:
            continue
        t = tuple(sorted((a, b, c)))
        tn = tuple(sorted((int(negidx[a]), int(negidx[b]), int(negidx[c]))))
        canon_t = min(t, tn)
        if canon_t in seen:
            continue
        seen.add(canon_t); out.append(canon_t)
    arr = np.array(out)
    meta = dict(kmax=kmax, N=N, cap=cap, seed=seed, n_triads=len(out), attempts=attempts,
                sha256=hashlib.sha256(arr.tobytes()).hexdigest())
    return arr[:, 0], arr[:, 1], arr[:, 2], meta


def hermitian_shuffle(uh, rng):
    N = uh.shape[-1]
    theta = np.angle(np.fft.fftn(rng.normal(size=(N, N, N))))
    return uh * np.exp(1j * theta)[None]


def c_tri(uh, tri):
    """Component-averaged amplitude-weighted resultant length and mean active weight W (convention C2)."""
    a, b, c = tri
    Cs, Ws = [], []
    for i in range(3):
        f = uh[i].reshape(-1)
        amp = np.abs(f)
        ph = np.angle(f)
        w = amp[a] * amp[b] * amp[c]
        W = w.sum()
        Cs.append(abs((w * np.exp(1j * (ph[a] + ph[b] + ph[c]))).sum()) / W if W > 0 else 0.0)
        Ws.append(W)
    return float(np.mean(Cs)), float(np.mean(Ws))


def separates(real_series, ens, need=NEED, pct=PCT):
    """real_series: (S,), ens: (S, M). Returns (separated, count, per-snapshot booleans)."""
    thr = np.percentile(ens, pct, axis=1, method="linear")
    hit = np.asarray(real_series) > thr
    return bool(hit.sum() >= need), int(hit.sum()), hit.tolist()


def null_calibration(ens, need=NEED, pct=PCT):
    """ens: (S, M). Each of the M columns in turn is 'real' against the other M-1."""
    S, M = ens.shape
    n_sep = 0
    counts = []
    for j in range(M):
        others = np.delete(ens, j, axis=1)
        ok, cnt, _ = separates(ens[:, j], others, need, pct)
        n_sep += ok; counts.append(cnt)
    return dict(false_positive_rate=n_sep / M, n_separating=n_sep, M=M,
                hit_count_distribution={str(k): int(v) for k, v in zip(*np.unique(counts, return_counts=True))})


def synthetic_field(N, rng, spectrum_power=-2.0, kpk=4.0):
    """Stand-in for a live snapshot: solenoidal, random phases, power-law-ish spectrum (demo only)."""
    K = kvec(N).astype(float)
    k2 = (K ** 2).sum(0); k2s = np.where(k2 == 0, 1, k2)
    uh = np.fft.fftn(rng.normal(size=(3, N, N, N)), axes=(1, 2, 3))
    uh = uh - K * ((K * uh).sum(0) / k2s)
    amp = np.sqrt(k2s) ** (spectrum_power / 2) * np.exp(-k2 / (2 * (N / 4) ** 2))
    uh = uh * amp * np.all(np.abs(K) <= N // 3, axis=0)   # 2/3-rule band, as a real solver state would have
    uh[:, 0, 0, 0] = 0
    return uh


def planted_field(uh, rng, x0=(0.7, 1.1, 0.4), sigma=0.5):
    """Planted triadic phase-lock (convention C5)."""
    N = uh.shape[-1]
    K = kvec(N).astype(float)
    g = np.angle(np.fft.fftn(rng.normal(size=(N, N, N))))
    phase = -(K[0] * x0[0] + K[1] * x0[1] + K[2] * x0[2]) + sigma * g
    return np.abs(uh) * np.exp(1j * phase)[None]


def run_demo(N, kmax, cap, M, nsnap, seed, quick=False):
    t0 = time.perf_counter()
    ta, tb, tc, meta = triad_set(N, kmax, cap, seed)
    tri = (ta, tb, tc)
    rng = np.random.default_rng(np.random.SeedSequence([seed, 2]))
    real_null, ens_null, real_pl, ens_pl, W = [], [], [], [], []
    for s in range(nsnap):
        base = synthetic_field(N, rng)
        c0, w0 = c_tri(base, tri)
        real_null.append(c0); W.append(w0)
        ens_null.append([c_tri(hermitian_shuffle(base, rng), tri)[0] for _ in range(M)])
        pl = planted_field(base, rng)
        real_pl.append(c_tri(pl, tri)[0])
        ens_pl.append([c_tri(hermitian_shuffle(pl, rng), tri)[0] for _ in range(M)])
    ens_null, ens_pl = np.array(ens_null), np.array(ens_pl)
    # shuffle must preserve |u| exactly
    chk = synthetic_field(N, rng); sh = hermitian_shuffle(chk, rng)
    amp_err = float(np.max(np.abs(np.abs(sh) - np.abs(chk))))
    div_err = float(np.max(np.abs((kvec(N) * sh).sum(0)))) / float(np.max(np.abs(chk)))
    herm_err = float(np.max(np.abs(np.fft.ifftn(sh[0], axes=(0, 1, 2)).imag)))
    ok_real, cnt_real, _ = separates(real_null, ens_null)
    ok_pl, cnt_pl, _ = separates(real_pl, ens_pl)
    return dict(id="NS-PRESS-II-SELFTEST-DEMO", status="PIPELINE_DEMO_ON_SYNTHETIC_FIELDS_NOT_A_RESULT",
                params=dict(N=N, kmax=kmax, cap=cap, M=M, snapshots=nsnap, seed=seed, need=NEED, pct=PCT),
                triad_set=meta,
                shuffle_checks=dict(max_abs_amplitude_change=amp_err, relative_divergence_after_shuffle=div_err,
                                    max_imag_part_of_ifft=herm_err),
                incoherent_field=dict(separates=ok_real, hit_count=cnt_real,
                                      mean_C_tri=float(np.mean(real_null)), mean_shuffle_C_tri=float(ens_null.mean()),
                                      mean_active_weight=float(np.mean(W))),
                null_calibration=null_calibration(ens_null),
                planted_control=dict(separates=ok_pl, hit_count=cnt_pl, mean_C_tri=float(np.mean(real_pl)),
                                     mean_shuffle_C_tri=float(ens_pl.mean())),
                runtime_s=time.perf_counter() - t0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--N", type=int, default=32); ap.add_argument("--kmax", type=int, default=8)
    ap.add_argument("--cap", type=int, default=200000); ap.add_argument("--M", type=int, default=M_DEFAULT)
    ap.add_argument("--snapshots", type=int, default=NSNAP_WINDOW); ap.add_argument("--seed", type=int, default=20261122)
    ap.add_argument("--out", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "selftest_demo.json"))
    a = ap.parse_args()
    r = run_demo(a.N, a.kmax, a.cap, a.M, a.snapshots, a.seed)
    json.dump(r, open(a.out, "w"), indent=1, sort_keys=True)
    print(json.dumps(r, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
