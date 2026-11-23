#!/usr/bin/env python3
"""NS-EVIDENCE-001 addendum 02 (Claude bench): is the N=16 excess in the forced-NS MMS test aliasing?

Background: ADDENDUM_01 found the time-integration error at N=16 slightly larger than at N>=24. HB-013/HB-014:
turning the 2/3 dealiasing mask OFF removes about two thirds (2D) of the excess but a residual remains, and the
residual decays fast with N, which is what aliasing of the error field's quadratic products would do.
This script isolates it. Three variants on the same retained band |k_i| < N/2 (Nyquist excluded) at each N:
  A  '2/3 rule'     : the frozen solver unchanged (mask |k_i| <= N//3)
  B  'band, aliased': retained band |k_i| < N/2, products evaluated on the N-grid (aliased)
  C  'band, exact'  : same retained band, products evaluated on a 2N grid (zero padded; alias-free for the
                      retained band because wrapped modes land at |k| >= 1.5 N)
If aliasing is the cause of the residual, C should sit much closer to the large-N limit than B.
The frozen solver and ns_mms.py are imported unmodified; the subclass only replaces the nonlinear term."""
import json, os, sys, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import ns_spectral as ns
import ns_mms as M


class BandNS(M.ForcedNS):
    def __init__(self, N, d, exact=False, **kw):
        super().__init__(N, d, **kw)
        self.exact = exact
        self.mask = np.all(np.abs(self.k) < N / 2, axis=0)          # retained band, Nyquist excluded
        self.U0h = self.U0h * self.mask; self.Gh = self.Gh * self.mask; self.Lh = self.Lh * self.mask
        k1 = np.fft.fftfreq(N, d=1.0 / N).astype(int)
        self.Mg = 2 * N
        self.idx = np.ix_(*([k1 % self.Mg] * d))
        self.scale = (self.Mg / N) ** d

    def _pad(self, fh):
        out = np.zeros((fh.shape[0],) + (self.Mg,) * self.d, dtype=complex)
        out[(slice(None),) + self.idx] = fh
        return out

    def nonlinear(self, uh):
        if not self.exact:
            return super().nonlinear(uh)
        ax = self.ax
        u = np.fft.ifftn(self._pad(uh), axes=ax).real * self.scale
        adv = np.zeros_like(u)
        for j in range(self.d):
            dudx = np.fft.ifftn(self._pad(1j * self.k[j] * uh), axes=ax).real * self.scale
            adv += u[j] * dudx
        F = np.fft.fftn(adv, axes=ax) / self.scale
        nh = F[(slice(None),) + self.idx] * self.mask
        nh = -self.project(nh)
        nh[(slice(None),) + (0,) * self.d] = 0.0
        return nh


def err(S, T, dt):
    uh = M.a_of(0.0) * S.U0h
    Ef = np.exp(-S.nu * S.k2 * dt); E2 = np.exp(-0.5 * S.nu * S.k2 * dt)
    for n in range(int(round(T / dt))):
        uh = S.step_forced(uh, n * dt, dt, Ef, E2)
    ex = M.a_of(T) * S.U0h
    return float(np.sqrt((abs(uh - ex) ** 2).sum() / (abs(ex) ** 2).sum()))


def main():
    out = dict(id="NS-EVIDENCE-001-ADDENDUM-02", T=1.0, dt=0.05, cases={})
    # sanity: on an alias-free state (N=25, retained |k|<=8 so 3*8 < 25) the padded nonlinear equals the frozen one
    # to roundoff. (At N divisible by 3 the frozen 2/3 rule, kc = N/3 exactly, has boundary-shell aliasing: with
    # N=24, kc=8 the same comparison differs by ~0.10 (2D) / ~0.39 (3D) on a random state; recorded below.)
    for d in (2, 3):
        for N, kmax in ((25, 8), (24, 8)):
            S0 = ns.PeriodicNS(N, d)
            Sx = BandNS(N, d, exact=True)
            m = np.all(np.abs(S0.k) <= kmax, axis=0)
            S0.mask = m; Sx.mask = m
            rng = np.random.default_rng(0)
            uh = S0.project(S0.to_hat(rng.normal(size=(d,) + (N,) * d)))
            a, b = S0.nonlinear(uh), Sx.nonlinear(uh)
            out["sanity_padded_vs_frozen_d%d_N%d_kmax%d" % (d, N, kmax)] = float(np.max(np.abs(a - b)) / np.max(np.abs(a)))
    limits = {2: None, 3: None}
    for d, Ns in ((2, (16, 20, 24, 32, 48)), (3, (16, 20, 24, 32))):
        rows = {}
        for N in Ns:
            t0 = time.perf_counter()
            A = err(M.ForcedNS(N, d), 1.0, 0.05)
            B = err(BandNS(N, d, exact=False), 1.0, 0.05)
            C = err(BandNS(N, d, exact=True), 1.0, 0.05) if N <= 32 else None
            rows[N] = dict(A_two_thirds=A, B_band_aliased=B, C_band_alias_free=C, secs=time.perf_counter() - t0)
        lim = rows[Ns[-1]]["A_two_thirds"]
        for N, r in rows.items():
            for k in ("A_two_thirds", "B_band_aliased", "C_band_alias_free"):
                r[k + "_excess_vs_largeN_A"] = None if r[k] is None else r[k] / lim - 1.0
        out["cases"]["%dD" % d] = dict(large_N_reference_error=lim, reference_N=Ns[-1], rows=rows)
        print(d, "ref", lim)
        for N, r in rows.items():
            print(" N%-3d A %+.3e  B %+.3e  C %s" % (N, r["A_two_thirds_excess_vs_largeN_A"], r["B_band_aliased_excess_vs_largeN_A"],
                  "n/a" if r["C_band_alias_free_excess_vs_largeN_A"] is None else "%+.3e" % r["C_band_alias_free_excess_vs_largeN_A"]))
    print({k: v for k, v in out.items() if k.startswith("sanity")})
    os.makedirs(os.path.join(HERE, "outputs"), exist_ok=True)
    json.dump(out, open(os.path.join(HERE, "outputs", "addendum02_results.json"), "w"), indent=1, sort_keys=True)


if __name__ == "__main__":
    main()
