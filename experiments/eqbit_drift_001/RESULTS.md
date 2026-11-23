# EQBIT-DRIFT-001 — Results (two independent implementations)

**Spec:** `eqbit-drift-spec.md` revision 2 (OQ-EXP-2026-004, proposed).
**Implementations:** Architect bench (Diablo) and Memory bench (Cosmo), written
independently from the spec. Cosmo's implementation was written and frozen
before Diablo's files were opened; Diablo's result JSONs stayed sealed until
Cosmo's numbers existed. Neither implementation was adjusted after the
comparison except as disclosed in §3.
**Status:** filed 2026-11-22 at the maintainer's direction. STRATA rung: Analogy. Nothing here
touches EQBIT-001/002 or makes any gravity claim (§6 fences of the spec).

## §1 Experiment A — the drain at 0⁸ (correctness gate; graph-agnostic)

All gates pass in **both** implementations.

| variant | g | closed-form max P₀ | Diablo | Cosmo | argmax (both) |
|---|---|---|---|---|---|
| bare | 0.1 | 0.0030518820 | ✓ (err 1.7e-17) | ✓ | 149.950 |
| bare | 0.5 | 0.0710900474 | ✓ (err 1.9e-16) | ✓ | 43.850 |
| bare | 1.0 | 0.2343750000 | ✓ (err 1.5e-15) | ✓ | 126.400 |
| bare | 2.0 | 0.5504587156 | ✓ (err 5.6e-16) | ✓ | 37.200 |
| tuned | 0.1–2.0 | 1.0 (full transfer) | ✓ (P₀(t*) = 1 to 1e-15) | ✓ | 149.05 / 50.90 / 25.45 / 189.05 |

- **A1 (null control):** antisymmetric state reaches the origin at ≤ 1e-28 in
  both implementations (gate: < 1e-12). The drain is exactly mode-locked.
- **A3 (P4 equality):** P₀(single) = P₀(sym)/240 holds with max deviation
  4.2e-14 (Diablo) / 4.1e-14 (Cosmo). Headline: at g = 2.0 bare, a single
  root's excitation reaches the origin at **0.00229** — the origin drinks
  only through the symmetric mode, as derived.

## §2 Experiment B — depth gradient

**B0 regression gate: PASS, three ways.** At ε = 0 the antipode arrival is
**0.8820834325** in both implementations (agreement 5.6e-13), and Diablo's
windowed check finds the peak 0.8820834325 at t = 42.33999 — PR #117's
0.882 @ 42.34 reproduced. (The curve has near-tie peaks at t ≈ 36.20 and
42.34, equal to ~1e-12; which one a refinement reports is an instrument
detail, exactly the window-sensitivity the review flagged.)

**Antipode arrival A₃(ε)** — the headline channel:

| ε | Diablo | Cosmo | R₃ = A₃(ε)/A₃(0) |
|---|---|---|---|
| 0 | 0.882083 | 0.882083 | 1.000 |
| 0.25 | 0.922657 | 0.922657 | 1.046 |
| 0.5 | 0.762305 | 0.762305 | 0.864 |
| 1.0 | 0.478158 | 0.478158 | 0.542 |
| 2.0 | 0.235552 | 0.235552 | 0.267 |

- **Reciprocity identity E₃ ≡ A₃:** holds — max deviation 6.7e-16 (Diablo),
  0.0 (Cosmo, after the disclosure in §3). No drift/leak asymmetry exists in
  this closed system, as the spec's fence states.
- **Orbit-quotient cross-check:** the 5×5 quotient reproduces every arrival
  in both implementations (max deviation 2.0e-12 Diablo / 2.1e-12 Cosmo).
- **E1 ordering: inverted, as a result.** A₃ > A₁ > A₂ at every ε — the
  antipode is not a generic "deep" shell; it is the resonant transfer
  channel. BFS depth is not coupling depth.
- **Reading (ratios only, per the claim ceiling):** a shallow gradient
  (ε = 0.25) slightly *enhances* antipode arrival (+4.6%); stronger gradients
  suppress it monotonically (×0.27 at ε = 2). Shell-1 arrival is mildly
  enhanced at all ε (R₁ ≈ 1.05–1.14); shell-2 declines (R₂ → 0.74). Three
  depths cannot establish a decay law and none is claimed; the Leech graph
  remains the named follow-up if the question is pursued.

## §3 Disclosed discrepancy — max-finding instruments (resolved)

Shell-1/2 *maxima* differed between the implementations in five cells
(largest: ε = 0.5 shell 1 — Cosmo 0.3497 vs Diablo 0.3663). Cause: Cosmo's
refinement searched only ±1 grid cell around the grid argmax and missed
narrow peaks elsewhere in the window; those Cosmo values are lower bounds.
Resolution by direct evaluation: Cosmo's own diagonalization, evaluated at
Diablo's argmax times, reproduces Diablo's maxima to ~1e-13 (ε = 0.5 @
t = 5.369: 0.366294122875 both; ε = 0.25 @ t = 114.63: agreement 1.1e-13;
ε = 1.0 @ t = 131.17: 4.8e-14). The dynamics agree exactly; only the
max-finder differed. Diablo's maxima stand as the values of record.
Separately, Cosmo's first reciprocity comparison mixed a grid max with a
refined max (deviation 4.9e-3); comparing like with like gives 0.0. Both
incidents are the review's §8.1/Q2 lesson, encountered live: in this system
*maxima are instrument-sensitive; functions are not.*

## §4 Verdict

EQBIT-DRIFT-001's registered predictions hold under two independent
implementations: the origin drain is real and exactly mode-locked (Exp A,
a construction correctness gate), and a depth gradient leaves shallow
arrival intact while strangling the antipodal resonance (Exp B), with the
reciprocity and quotient identities exact. Filed as a result — not a
claim upgrade: the registry entry stays at the Analogy rung, and the
Flachi asymmetry remains dissipative physics this closed system does not
reproduce.

*Recorded by Cosmo (Memory bench), 2026-11-22, from Diablo's uploaded
result JSONs and Cosmo's own run (`cosmo_impl.py` / `cosmo_results.json`
alongside this record). Diablo's implementation and result JSONs are his
to file under his own authorship.*
