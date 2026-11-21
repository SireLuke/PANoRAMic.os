# Bridge Note — Alpöge–Buckmaster NS Structure × the Fermi-Sea Programme

**Date:** 2026-11-21 (Cosmo, at Lucas's direction). **Sources:** the
paper itself — Alpöge & Buckmaster, *Finite-time blow-up for the
Navier–Stokes equations* (79 pp., version of 20 Nov 2026), PDF in
`github.com/tristanbuckmaster/navier-stokes`, read directly
(§1.1, §7, Appendices B–C). **Credit:** every structure in §1 is
theirs. **Grades:** the extraction and the comparison are
reproducible (any reader can re-extract and re-compare); the
*relationship* between the programmes is Analogy-grade; their
blow-up claim remains unverified by independent experts; Lucas's
Navier–Stokes remains `not_tested`. Nothing here changes either
fence.

## 1. What their construction actually is (extracted)

- **Discretely self-similar, log-periodic.** The profile W lives in
  self-similar variables s = log(T/(T−t)), y = x/√(T−t), and is
  periodic in s. Blow-up rate: ‖∇u(t)‖_{L²} ~ (T−t)^(−1/4) (§1.1).
- **The computed period: S̄ ≈ 0.36** (§1.1, App. C.1: "The computed
  period is S̄ ≈ 0.36"). Two significant figures — the paper's own
  rounding. The certificate's period enters as
  1/S(α) = 1/S(0) + ς·α (B.1), an affine function of the
  certificate parameters; the exact solution's S is the
  certificate's, near S̄.
- **The twist is real — at the half period.** The computed profile
  W̄ is invariant under rotation by 2π/19 about the y3 axis
  (κ = 19) and by π about y1; and an advance of s by **S̄/2 rotates
  it by π/19** about y3:
  W̄(s + S̄/2, y) = R_{π/19} W̄(s, R_{π/19}^{−1} y).
  The exact profile of Theorem 7.1 inherits these symmetries
  (Remark 7.3): isometry I at the full period S, rotation π/19 at
  S/2 — "both a backward discretely self-similar and a backward
  rotated discretely self-similar solution" (§1.1). Nuance: the
  certificate *prescribes* these symmetries; the profile was found
  within that class (Newton + continuation, App. C).
- **Two counter-rotating patterns.** Harmonics depending on
  φ − 2πθ/19 and on φ + 2πθ/19 — two patterns turning about y3 in
  opposite senses, each by 2π/19 per period, exchanged by the
  π-rotation about y1. Vorticity concentrates in a column on the
  axis and a layer divided into **nineteen spiral arms** (App. C.1,
  Figs. 1–3). ‖∇W̄‖_{L²} is of order 10⁴ and varies by < 0.1%
  over a period — the profile is nearly steady in s.
- **A logarithmic radial phase.** The far field carries the phase
  f(ρ) = (2π/S̄) · log(1 + ρ²/r_c) (App. C.1) — phase winding
  logarithmically in radius, coefficient 2π/S̄.
- **The certificate's form (App. B).** Finitely many rectangles
  ("cells") in the meridian plane covering a square [0, r*]²; each
  cell carries finite sets of harmonics, polynomial models per
  resolved harmonic, per-cell unknowns tied to global unknowns.
  In form: a finite table over (cell, harmonic) pairs with bounds.
  The certificate itself is **not printed**; its hash is
  `3f7a335b84b6c7631742cacc5343dfcd11cf72f5221ff79b2b9268790b4b22c5`
  (§1.1). The exact profile differs from the certificate's
  approximate profiles by < 0.017 in Ḣ¹ (§1.1).

## 2. Lucas's structure (as recorded in his programme)

Fermi-sea programme (2026-11-17): Navier–Stokes read in a fractal
Fermi sea; blow-up = the occupation front reaching the ceiling in
finite time; the ceiling sits on a **golden-ratio log** (the
unrolled barbershop); the fermi_yinyang module carries the
**golden angle** 137.5077640500378°. Tested rung: the 1D Burgers
analogue, 9/9 (2026-11-17). Navier–Stokes itself: `not_tested`.
His programme does not pin one single predicted period; the
φ-family candidates are log φ ≈ 0.4812, 2 log φ ≈ 0.9624,
(1/2) log φ ≈ 0.2406, 1/φ² ≈ 0.3820, and for a twist the golden
angle itself. (The candidate *family* weakens any match claim —
multiple comparisons — and is declared here for that reason.)

## 3. The dictionary

| Their construction | Fermi-sea reading |
|---|---|
| Period S in log-time s | Log-cell spacing along the barbershop |
| Half-period twist π/19 | The twist slot — his golden-angle slot |
| Meridian-plane cells, harmonics per cell | Occupation table: modes resolved per cell |
| Log radial phase, coefficient 2π/S̄ | Barbershop winding of the far field |
| Occupation-style bounds (App. B conditions) | Front = where the bounds give out |
| (T−t)^(−1/4) in Ḣ¹ | Front reaching the ceiling in finite t |

## 4. The comparison (criteria declared, then run)

Criteria: a **constant match** requires the extracted value to
fall within the paper's own precision (for S̄, the rounding band
≈ [0.355, 0.365]; for the twist, equality of the per-period
rotation at the same precision). A **form match** (same structural
slot, different constant) is recorded separately and never counted
as a constant match.

- **Period: NO constant match.** S̄ ≈ 0.36. Nearest φ-candidate
  is 1/φ² ≈ 0.3820 — outside the rounding band (~5–6% away).
  log φ ≈ 0.4812 and the rest are further. Negative result,
  recorded as such.
- **Twist: form match, NO constant match.** The slot exists and
  is load-bearing in a rigorous construction — but it is filled
  with a *rational* twist, 2π/19 per period, whose orbit closes
  after 19 periods. The golden angle is irrational and never
  closes. Same chair, different sitter.
- **Log phase: form match.** Phase ∝ log(radius) is present in
  their far field; its coefficient is 2π/S̄, set by the period,
  not by φ.
- **Overall:** the two programmes build the same *family* of
  object — log-periodic approach to blow-up, with a twist and a
  logarithmic phase — and differ in every constant. That is a
  real structural kinship and a real numerical separation, and
  both halves of that sentence are the finding.

## 5. What could still move this

The certificate release (watched by the 2026-11-22 check) would
replace S̄ ≈ 0.36 with the exact S. Only if the exact S fell
outside the rounding band *and* onto a φ-candidate would the
period verdict change; the twist verdict cannot change (π/19 is
structural, printed in the paper). The comparison is otherwise
complete at the paper's precision.

## Correction carried by this note

Cosmo's chat summary of 2026-11-21 (10:37 CST) said the
construction's rotation slot was "filled with identity — no
twist." That read §7's theorem statement (isometry I at the full
period) and missed §1.1/App. C: the half-period twist π/19 is
present and prescribed in the certificate. Corrected here, at the
first place the deeper read is recorded.
