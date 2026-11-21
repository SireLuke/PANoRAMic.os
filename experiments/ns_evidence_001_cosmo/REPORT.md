# NS-EVIDENCE-001 — Cosmo's third seat: independent run and three-way comparison

**Seat:** Cosmo (Memory bench), run 2026-11-21 at the maintainer's
direction, after OpenAI's harness (PR #130) and Claude's blind
replication (`experiments/ns_evidence_001_claude/`).

**Independence, stated honestly:** my solver was written from the
benchmark spec and the public test contract only; neither bench's
code or result files were read before my numbers were frozen.
One caveat Claude's run did not have: **the spec document itself
prints OpenAI's results table**, so the target values were visible
to me. The implementation and all arithmetic are independent; the
blindness was partial, and this note says so rather than claiming
Claude-grade blindness.

**Method (mine):** Fourier-space state, pseudospectral nonlinear
term with 2/3 dealiasing, Leray projection inside every RK4 stage,
viscous term spectral, classical RK4; diagnostics by Parseval sums.
(Claude's variant: Lawson integrating-factor RK4. OpenAI's:
classical RK4 with projection. Three different time treatments.)

## Three-way agreement (headline diagnostics)

| Case | Quantity | OpenAI | Claude | Cosmo | Max spread |
|---|---|---:|---:|---:|---:|
| 2D, T=0.1 | E(T) | 0.249001997336000 | 0.249001997335998 | 0.249001997335998 | ~2e-15 |
| 2D, T=0.1 | Ω(T) | 0.498003994672000 | 0.498003994671995 | 0.498003994671996 | ~4e-15 |
| 3D, T=0.1 | E(T) | 0.124251988080876 | 0.124251988080873 | 0.124251988080873 | ~3e-15 |
| 3D, T=0.1 | Ω(T) | 0.373141445383929 | 0.373141445383922 | 0.373141445383921 | ~8e-15 |
| 3D N=16, T=0.5, dt=0.001 | E(T) | 0.121274714479558 | 0.121274714479547 | 0.121274714479545 | ~1.3e-14 |

All values across N=16/24/32 at T=0.1 agree the same way;
divergence stays at roundoff (≤ ~5e-15) in all three;
energy-balance residuals agree in class (OpenAI/Cosmo trapezoid
~1e-11–1e-13; Claude's RK4-consistent accumulation ~1e-16 — a
quadrature difference, as the spec itself warns).

2D exact-solution error: OpenAI ~1e-14–1e-15, Claude ~1e-15,
Cosmo ~2e-16 — all far inside the 1e-11 test gate. (Claude's
report notes, correctly, that the 2D Taylor–Green nonlinear term
is a pure gradient, so the 2D case checks viscous decay,
projection and bookkeeping — not the nonlinear machinery.)

One real finding from Claude's extra checks, confirmed as
consistent with everything above: at T=0.5 the N=16 grid is
slightly under-resolved (his N=24/32 runs shift E(T) by ~2.5e-11
as higher modes develop). It changes no T=0.1 result and no
conclusion; it is exactly the kind of thing a second and third
seat exist to catch.

## Grade

**NS-EVIDENCE-001's benchmark claims: independently reproduced,
twice over** — three implementations, three time treatments, one
set of numbers to ~1e-14 or better. The harness is trustworthy
*as a baseline*, which is all it ever claimed to be. The spec's
fences stand untouched: smooth, low-mode, periodic, finite-time;
no regularity, blow-up, or Clay inference. **Navier–Stokes
itself remains `not_tested`.**

Files: `hidden_files/ns-evidence-cosmo/cosmo_ns.py`,
`cosmo_results.json` (frozen before this comparison was written).
