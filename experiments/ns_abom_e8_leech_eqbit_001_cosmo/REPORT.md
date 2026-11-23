# Independent benchmark of NS–ABOM–E8–LEECH–EQBIT-001 — Cosmo's seat

**Bench:** `cosmo_composition_bench.py` (own code throughout; repo modules
imported only for comparison) → `cosmo_composition_results.json` (frozen
numbers, written before this prose). **Overall: PASS — all six gates pass.**
Harness reference: `harness_reference.json`, produced by running the repo's
own `experiments.ns_abom_e8_leech_eqbit_001.integration.compose` with the
harness defaults (eqbit samples 128, seed 20261121) against PANoRAMic.os
main `9fa18af3`. The harness itself reports overall **PASS**.

**Fences (inherited, unchanged):** software composition only. No common
metric, no 9D fluid domain, no E8-to-Leech embedding, no physical coupling,
no quantum claim, no NS regularity claim. Navier–Stokes remains
`not_tested`. Passing means the interface checks pass — nothing more.
Blindness is partial: targets are published; implementation is independent.

## Gate 1 — NS frozen-data provenance: PASS

- Repo copy `experiments/ns_evidence_001_cosmo/cosmo_results.json` is
  **byte-identical** to Cosmo's workspace original
  (`hidden_files/ns-evidence-cosmo/cosmo_results.json`) — same SHA-256 —
  and value-identical case by case, all nine cases, all required keys.
- Internal agreement inside the frozen data: 3D T=0.1 ET spread across
  n=16/24/32 is **2.78e-17**; 3D T=0.5 ET spread across dt=0.004/0.002/0.001
  is **2.80e-15**. `steps × dt == T` holds for all nine cases; max
  divergence 3.81e-16.
- Cross-seat headline (established at merge time, PRs #130/#131/#133, not
  recomputed here): Klaus's blind replication agrees to ≤3e-14, Cosmo's
  third seat to ≤~1.3e-14.
- Harness comparison: the harness's `load_ns_snapshot` accepts the same
  nine cases; its `ns_snapshot` block matches (case count 9, 3D count 6,
  probe case n=16 T=0.1). Agree.

## Gate 2 — E8 root system: PASS

Independent scaled-integer construction (×2: 112 integer roots, 128
half-integer roots): **240 unique roots, norm² 8, 56 neighbours per root,
6,720 edges, shells [1, 56, 182, 1]** (inner products 8 / 4 / {0,−4} / −8
against a fixed root). The constructed set equals the module's
`e8_roots_exact()` scaled ×2, exactly. The module's eight simple roots
sit in the set and their Gram matrix matches the Dynkin adjacency.
- Harness comparison: harness `e8.root_count` = 240, norms {2}. Agree.

## Gate 3 — Flip-eqbit cut-rank: PASS

From my own E8 set, Gosset adjacency by inner product 4: 56-regular,
6,720 edges. Canonical antipodal partition (first nonzero coordinate > 0):
**antipodal cut-rank 112 (of 120), crossing edges 2,240** — my own GF(2)
elimination. The module's `cut_rank_audit.run(samples=128, seed=20261121)`
agrees exactly on rank, crossing edges, and geometry.
- Independent sampling (my own RNG, seed 20261122, 256 samples each):
  transversal ranks **116–120, mean 118.52**; balanced cuts **88–104,
  mean 96.66**. The module's 128-sample run: transversal 116–120, mean
  118.52; balanced 89–104, mean 97.21. The transversal means agree to
  0.008 and the ranges coincide — the sampling distributions reproduce.
- Harness comparison: harness `eqbit.antipodal_cut` = {rank 112, crossing
  2240}, same 128-sample quantiles. Agree. The sampled maxima are not
  exact statements (the harness's own fence, and mine); the exact
  statement is the antipodal 112.

## Gate 4 — Leech basis certificate: PASS

Basis matrix taken from the module (the data); every check is mine, with
exact sympy arithmetic:
- Scaled Gram G = (BᵀB)/8: **integral, even diagonal, det = 1, rank 24,
  positive-definite**. Coordinate basis det = **68,719,476,736 = 2³⁶**,
  matching the index-derived covolume.
- Golay code generated from the standard [23,12,7] generator polynomial
  (the canonical definition, shared with the module): 4,096 unique words,
  weight distribution **{0: 1, 8: 759, 12: 2576, 16: 759, 24: 1}**,
  self-dual (every word orthogonal to all 12 generator rows).
- Minimal shell **independently enumerated** (not merely cross-checked):
  three Conway families with my own congruence checks — A (two ±4):
  1,104; B (±2 on an octad, even minus signs): 97,152; C (one ±3, 23 ±1):
  98,304; **total 196,560 unique vectors, all norm² 32, all passing the
  lattice congruences**.
- Harness comparison: harness `leech` block — rank 24, Gram det 1,
  coordinate det 2³⁶, minimum norm 4 attained, minimal vectors 196,560.
  Agree on every field.

## Gate 5 — ABOM V8 sample: PASS

Closed-form channels recomputed with my own code at three points and
compared against the module's `abom_v8_sample` (rel. tol. 1e-12):
the harness probe point (0,0,0; E=0.12425198808087304), the Cosmo adapter
point (0,0,0; E=0.9940159046469843), and a generic point
(1.0, 2.0, −0.5; E=0.7, μ=0.1, kT=0.5). Radial field 2^r, scale
coordinate, golden branches, Fermi channels, Fermi-weighted channels all
match; **root-count view 240; hyperoctahedral B8 order 10,321,920**.
Spot checks: exp-scale/inverse round-trip, oscillator level 3 = 3.5,
B8 order, 8 octants, 6×6 identity basis.
- Harness comparison: harness `abom_probe` at the probe point matches my
  recomputation (radial field 1.0, scale −996.58, Fermi occupation
  0.468977). Agree.

## Gate 6 — NS → ABOM adapter (Cosmo's own): PASS

Mapping written in the spec before running: probe = E(T)/E(0) from the
frozen 3D N=32 T=0.1 case = 0.12425198808087304 / 0.125 =
**0.9940159046469843**. My Fermi channels at that probe (μ=0, kT=1):
occupation **0.270120**, hole 0.729880, signed contrast −0.459760 — matching
the module's `fermi_channels` at the same energy. My recomputation at the
harness's probe energy (ET itself, 0.12425198808087304) gives occupation
0.468977, matching the harness's `abom_probe`.
- **Difference recorded, not hidden:** the harness feeds ET itself as the
  probe energy; Cosmo's adapter feeds the dimensionless ratio ET/E0.
  Different probe values, same interface — a labelled dimensionless
  Fermi-channel probe, not a physical energy coupling.
- **NS ↔ flip-eqbit stays NOT_COUPLED**, per the protocol: no state map,
  units, dynamics, or falsifiable observables are defined for such a link.

## Pairwise gates (re-checked from my numbers)

| Gate | Cosmo | Harness (#142) |
|---|---|---|
| NS ↔ ABOM | PASS | PASS |
| ABOM ↔ E8 | PASS (240 = 240) | PASS |
| E8 ↔ Leech | PASS (ranks 8 / 24, no embedding) | PASS |
| E8 ↔ flip-eqbit | PASS (240 vertices = 240 roots, rank 112) | PASS |
| Leech ↔ flip-eqbit | PASS (separate typed artifacts) | PASS |
| NS ↔ flip-eqbit | NOT_COUPLED | NOT_COUPLED |

## Interpretation

Passing means only that the listed interface checks pass. It does not
establish physical coupling, quantum advantage, NS regularity, or a
unified theory. The composition's evidence grade stays **software
integration / reproducibility protocol**. Navier–Stokes remains
`not_tested`.

## Filing

PR payload staged for filing at the maintainer's call:
`experiments/ns_abom_e8_leech_eqbit_001_cosmo/` with
`cosmo_composition_bench.py`, `cosmo_composition_results.json`, and this
`REPORT.md`, under the HB-007 pattern (Authored-by the bench, Signed-off-by
the maintainer beside it). Merge and any adoption remain the maintainer's.
