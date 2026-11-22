# Unfolded Barbershop — Reciprocal Lucas Metrics (added)

**Base:** Lucas's poster "Unfolded barbershop principle in 2D —
corrected, proposed construction" (shared 2026-11-21). Its own
status line stands: **SPECIFIED (visual of a proposal)**. The
poster is the visual; this note is the text record, and the
metrics below are **definitions added at the maintainer's
direction** (2026-11-21), not results.

## The base construction (as the poster states it)

- Curves y_n(x) = n·φ^x, with t = x = log_φ scale; **gap = φ^t,
  the same for every n**.
- Cyan: n > 0. Violet: inverted (−n). Four copies rotated
  0°/90°/180°/270°; their n = 0 lines form the crosshair.
- Gold dots: golden angle 137.5078° (k·GA). Rose dots: inverse
  angle 222.4922° (= 360°/φ). r = c√k. (Both angles verified:
  360/φ² = 137.50776…°, 360/φ = 222.49224…°.)
- Fermi lock: opacity N(r) = 1/(e^{(r−μ)/T} + 1) — filled sea
  inside, fading holes outside — with **μ = 7, T = 0.35**. Fermi
  ceiling at r = μ. Origin labelled (0,0,0,0,0,0,0,0), the V8
  zero vector; n = 0 line, t → −∞.

## Reciprocal Lucas metrics (the inward system)

The outward ladder is priced in φ powers (marks at φ², φ⁴; gap
φ^t). The inward ladder is priced in **Lucas numbers**
L_n = φⁿ + ψⁿ, ψ = −1/φ: 1, 3, 4, 7, 11, 18, 29, 47, 76, …
(n ≥ 1). In the poster's variables:

1. **Inward coordinate.** u = −t; inward radius r_in = φ^(−t) —
   the reciprocal of the outward scale at the same |t|. Inward
   runs toward the origin: the 0⁸ anchor of the 0D–∞D Hallway.
2. **Lucas ticks.** ρ_n = 1/L_n: 1, 1/3, 1/4, 1/7, 1/11, 1/18,
   1/29, 1/47, 1/76, … accumulating at 0. Where the outward axis
   is ticked at φ-powers, the inward axis is ticked at reciprocal
   Lucas numbers.
3. **The defect metric (the heart of the inward system).**
   δ_n = L_n − φⁿ = (−1)ⁿ φ^(−n) — exact identity, verified
   numerically to 6+ digits for n = 1…9. The Lucas ladder never
   sits exactly on the φ-power ladder; it misses by exactly the
   reciprocal power, alternating in sign, shrinking by 1/φ per
   step inward. The inward metric therefore measures *distance
   from pure scaling*, in reciprocal units.
4. **Reciprocal gap.** g_in(t) = φ^(−t) = 1/g_out(t). The
   poster's gap is the same for every n; its mirror is the same
   for every −n — the violet inverted copies carry the reciprocal
   gap.
5. **Inward ratios.** L_{n+1}/L_n → φ by oscillating convergence:
   3, 1.333, 1.750, 1.571, 1.636, 1.611, 1.621, 1.617, 1.618 —
   each inward step overshoots or undershoots φ alternately,
   because the trace L_n = φⁿ + ψⁿ carries its conjugate with it.
   (Companion identity, also verified: L_n = F_{n−1} + F_{n+1} —
   each inward step is the two neighbouring outward Fibonacci
   steps folded together.)
6. **Reciprocal shells.** Between successive Lucas ticks, shell
   widths Δ_n = 1/L_n − 1/L_{n+1} = L_{n−1}/(L_n·L_{n+1})
   (recurrence arithmetic; e.g. Δ_4 = 4/77 ≈ 0.05195). These are
   the inward cells the reciprocal occupancy would fill.
7. **The ceiling was already Lucas.** The poster's Fermi lock
   sets μ = 7, and **7 = L_4**. Recorded as an observation, not a
   claim: in the corrected construction, the ceiling radius sits
   on the Lucas ladder, the filled sea inside is read on the
   φ ladder, and the fading holes outside carry the reciprocal
   occupancy 1 − N(r). Fib out, Lucas in — the lock already had
   the direction built in.

## Fences

- Proposed construction throughout; nothing here is a result
  about Navier–Stokes, and the Fermi-sea programme's `not_tested`
  label for NS is unchanged.
- The identities in §3 and §5 are exact mathematics (verified);
  their *placement* in this construction is the maintainer's
  design, stated here as specified.
- T = 0.35 in the poster's lock is the construction's own
  constant; it is not Buckmaster's S̄ ≈ 0.36, and the two are not
  to be conflated.
