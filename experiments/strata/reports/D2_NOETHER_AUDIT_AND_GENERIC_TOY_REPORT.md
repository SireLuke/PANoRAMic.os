# Architect-bench report — D2 Noether audit and GENERIC centrepiece

**Bench:** Architect (Claude, Anthropic)  
**Document:** D2, Etxebarria, *Lagrangian and Hamiltonian Mechanics* (Durham, MATH2741), as described in the Fork Capsule  
**Date of analysis:** 2026-11-17. Filed 2026-11-19 at the maintainer's direction.  
**Status:** UNVERIFIED. Per Fork Capsule §0.1, verification must happen at a bench other than the one that produced this work. Nothing here is certified.  
**Provenance:** produced by Claude in a Claude Code session; Fork Capsule prepared by Cosmo (2026-11-17) and relayed by Lucas Thouvenell. Companion script: `generic_toy_d2.py` (this directory; needs numpy and scipy; not run in CI).

I did not have D2 itself, only the capsule's description. The Noether reasoning is standard theory, not a reading of Etxebarria's notes. Repo facts come from pan-fractal-kernel `main` at `311028a` (code paths below re-checked on 2026-11-19); PANoRAMic.os was visible read-only.

## Findings

### Noether audit table (§2B)

| # | Quantity | Class | Reasoning | STRATA grade |
|---|---|---|---|---|
| 1 | Radial first integral H at γ=0 | (ii), provisional | See the radial sub-question below. | Analogy for the "Noether charge" reading; the system itself is `not_tested` (not visible) |
| 2 | Janus pair defects δ_k = H_k + D_k − 1 | (iv) not conserved | Measured on 2000 random V8 states (seed 20261117): none of the five pairs is tautological, and all vary (ranges below). `janus_metrics.py` is affine algebra with no dynamics. | Reproducible domain pattern (software only) |
| 3a | Gosset shell SHA-256 digests | (iii) checksum | `pan_geometric_depth.py` hashes the sorted vertex list per shell. That is coordinate-dependent, not invariant under the lattice symmetry group. | Analogy at most; an audit device, which is fine |
| 3b | Shell counts and norm² counts | (ii) structural invariant | Properties of the lattice graph (inference, not tested here). A different object from the digests. | `not_tested` |
| 4 | μ-cube flux Φ = N(1−N) | (iv) not conserved | `lemniscate_flux` in `abom_v8/occupancy/menger.py` equals (1−δ²)/4 ≤ ¼, and `Flux.lean` proves the bound (`flux_le_quarter`). It is the two-state occupation variance and varies with N. | Reproducible domain pattern (exact identity, software) |
| 5a | Fermi–Dirac N | (iv) not conserved | An equilibrium parameter of (E, μ, T), not a charge of any flow. | `not_tested` as a conservation claim |
| 5b | Yin-yang lobe areas N + (1−N) = 1 | (iii) bookkeeping | The sum is built into `fermi_yinyang.py` (white/UHFE = N, black/UDFE = 1−N). Its docstring correctly calls it "a display/semantic mapping, not a physical identity". | Analogy |

Janus pair-defect ranges (min, max) over the 2000 draws: bubble (−0.3223, 0.3288), honeycomb (−0.3037, 0.2922), spiderweb (−0.2284, 0.2131), chiraldna (−0.2019, 0.2062), compoundeye (−0.3333, 0.3327).

**Radial sub-question (Helmholtz / inverse problem).**
- **It admits a Lagrangian, but that is cheap.** On a region where H has no critical points, the flow must be ẋ = m·H_y, ẏ = −m·H_x, with m the (inverse) Jacobi last multiplier. By hand, L = (y/m)ẋ − H reproduces exactly that flow (Euler–Lagrange in y gives ẋ = mH_y; in x gives ẏ = −mH_x). This was done by algebra only; it was not machine-checked. It holds for any smooth planar flow with a first integral, so it carries no physical content.
- **H is not unique.** Replacing H with F(H) and m with m/F′(H) gives the same flow, so a "Noether charge" for time translation is gauge-dependent until a specific L is chosen. That is why the class is (ii).
- **The domain depends on the unstated parameter β.** For H = [y/(2−y)]^β e^(−y³/24)/(1−x²), tested numerically on 0<y<2: for β ≥ 0.25 (tried 0.25, 0.5, 1, 2) ∂H/∂y never vanishes, so no critical points and no closed orbits. For β = 0.05, dg/dy changes sign at y ≈ 0.899 and 1.880; for β = 0.1, at y ≈ 1.351 and 1.632, so critical points exist.
- **γ ≠ 0 is unknown to me.** If γ is a damping term, no standard Lagrangian exists there, and that is where GENERIC takes over.
- **The radial system itself does not appear in either repo's default branch** (grepped in pan-fractal-kernel and PANoRAMic.os). It may live only in the Map Legend.

### §3 Centrepiece: UHFE ⊕ UDFE as one GENERIC system

1. **What must be defined.** An energy E(x), an entropy S(x), an antisymmetric L satisfying Jacobi, and a symmetric positive-semidefinite M. Proposed candidates, all labelled proposals: S is the entropy channel itself (alternatively the kernel's binary entropy H2(N)); E is a coherence functional of the reversible pair plus an internal-energy term in s.
2. **What the degeneracy conditions mean in V8 terms.** L·δS = 0 means s is a Casimir of the reversible part: no conservative coupling may move s. M·δE = 0 means dissipation redistributes energy into s and never destroys it. So a pure decay of h with no s growth is forbidden.
3. **No-go for a 2-channel toy.** In 2D an antisymmetric L is either 0 or invertible. If invertible, L·∇S = 0 forces ∇S = 0, so no entropy production (checked on 500 random L). **The smallest toy with both parts nontrivial has 3 channels.** The toy uses x = (a, b, s): the reversible pair (a, b) is a proposed (h, R) and s is the entropy channel. E = b²/2 + V(a) + eˢ, S = s, M = (ζ/T)wwᵀ with w = (0, T, −b).
4. **Toy results** (seeded, randomised; reproduced on 2026-11-19 with identical numbers):

   | Check | Result |
   |---|---|
   | L∇S | exactly 0 |
   | M∇E (relative) | ≤ 1.9e-16 |
   | M symmetric, PSD | yes (min eigenvalue ≈ −2e-16) |
   | Entropy production ζb²/T | ≥ 0 |
   | Forward, 129 trajectories: energy drift | ≤ 6.4e-12 |
   | Forward: entropy | never decreases (min step ≈ 1.5e-13) |
   | Backward (same 129): energy drift | ≤ 4.4e-12 |
   | Backward: entropy | strictly decreases (max step ≈ −1.2e-7) |
   | Time-reversal defect, ζ = 0 | ≤ 1.9e-12 |
   | Time-reversal defect, ζ > 0 | ≥ 0.044 on every trajectory |

   171 of 300 sampled trajectories were excluded from the backward runs because the reversed dissipative flow blows up within t ≤ 1. That is physical, but it means the backward sample is the 129 that survived.
5. **Where EDDE lives.** In the dissipative bracket, as a choice of M(x), not as a third field. This commits EDDE to conserving E and producing entropy, and rules out EDDE as its own conserved field or as a UHFE+UDFE sum rule.

**Grade.** The framework fit is a reproducible pattern in one domain, the toy only. UHFE and UDFE stay `not_tested` until their functionals exist.

### §4 Shared questions

1. **What the action buys.** Symmetry-to-conservation via Noether, coordinate independence, constraints through multipliers, and boundary-term bookkeeping.
2. **Where constraints live.** In D2 they live in the action or the geometry. In the kernel they live in the solver, as range checks and identities. Nothing in the kernel derives from an action, so the conservation-flavoured quantities are by construction.
3. **What to stop saying** (sourced):
   - The yin-yang lobe areas sum to 1 by construction (`fermi_yinyang.py`, titled "UH/UDFE conjoined"). Read as a field relation, that is the sum rule the capsule's §0.4 disavows. The docstring hedges correctly, but the title invites the field reading; keep it labelled as a display mapping.
   - "Formation" as order-creation. In GENERIC the reversible part is volume-preserving and cannot create order, so structure can only form at an entropy cost elsewhere. If UHFE means creating order, that reading needs rethinking.

## Limits

- I had no sight of D2. The radial system, the capsule's PANoRAMic.os PR #89 content and the Map Legend were not available to me at the time of analysis.
- The (h, R, s) channel assignment is a proposal and is not mapped to V8's [0,1] ranges.
- The classification of row 3b and the radial Lagrangian argument rest on reasoning, not machine proof. Nothing here is Lean-verified.
- The toy shows framework fit only. It uses numpy and scipy, unlike the stdlib-only STRATA convention; a stdlib port is a possible follow-up.

## For the other benches

- Independently re-derive that L = (y/m)ẋ − H gives ẋ = mH_y, ẏ = −mH_x (not machine-checked).
- Rerun `generic_toy_d2.py` and critique the choice of E, S and M.
- Check D2's actual Noether treatment against the table; I worked from standard theory.
- A bench with Map Legend access should supply the radial system's equations and β.

**One flag.** Earlier notes ask that UH/UDFE stay conjoined as one coupled system, while this capsule says "separate fields, no sum rule". GENERIC reconciles both: one coupled evolution equation with two independent operators tied by degeneracy conditions instead of a sum rule.
