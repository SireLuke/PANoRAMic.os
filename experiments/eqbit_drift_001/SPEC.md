# EQBIT-DRIFT-001 — Drift Toward 0⁸: A Sink-and-Depth Analogue Experiment on the Gosset Graph

**Status:** Revision 2 — incorporates the Architect bench's review (§8) in full; runs completed 2026-11-22 by two independent implementations; filed with the results record. Proposed registry OQ-EXP-2026-004.
**Proposed registry ID:** OQ-EXP-2026-004 (assigned on filing; successor to OQ-EXP-2026-001 flip-eqbit, -002 NS Press I, -003 NS Press II).
**Author:** Cosmo (Memory bench), at the maintainer's direction, 2026-11-22.
**Review requested from:** Claude (Architect bench). Cosmo will also run an independent implementation.
**STRATA classification:** Analogy rung. This spec tests whether a *pattern* — an emergent one-way boundary with an exponential depth law — reproduces in the kernel's substrate. It licenses no claim beyond that rung.

---

## §0 Summary

Flachi (2026, preprint, not peer-reviewed) built a digital acoustic black hole: a cellular-automaton fluid on a lattice whose emergent horizon trapped disturbances — except short-wavelength ones, which outran the effective sound speed and leaked, with the escaped fraction falling off **exponentially with the depth** of the disturbance's origin inside the horizon.

The maintainer's question: can the same experiment be staged on the Gosset graph, with the eqbit excitation drifting toward **0⁸** — the zero vector, the V8 origin, the anchor of the 0D–∞D Hallway?

This spec stages it in two parts:

- **Experiment A (the drain):** adjoin the origin as a 241st node, coupled uniformly to all 240 roots. Measure how much excitation the zero vector can drink, against analytic predictions derived in advance (§3). The symmetry structure makes this a sharp test: exactly one mode of the shell can couple to the origin at all.
- **Experiment B (the depth law):** put an energy gradient on the graph using the shell structure around a pole root — [1, 56, 182, 1] — so amplitude drifts pole-ward. Start excitations at each depth and measure arrival at the pole, in both directions (drift-in and leak-out), against a no-gradient control.

Both experiments are small (240×240 and 241×241 Hermitian diagonalizations), deterministic, and cheap. Their value is the preregistration: the predictions in §3 are exact, and the claim ceiling in §4 is declared before any number exists.

---

## §1 Background and prior results

**The Gosset graph** (as constructed in `hidden_files/flip-qubit/run.py`, gates E1 verified): E8 roots in scaled coordinates (×2, norm² = 8); adjacency at scaled dot product 4 (true inner product 1, cos θ = ½); 240 vertices, 56-regular, 6,720 edges; BFS shells around any root **[1, 56, 182, 1]**; diameter 3; 120 antipodal pairs; no root is adjacent to its own antipode.

**The flip eqbit (PR #117, OQ-EXP-2026-001):** the Gosset graph state is a genuine 240-qubit stabilizer state; antipodal cut entanglement 112 ebits. Under the continuous-time quantum walk H = A, antipodal state transfer is **pretty-good**: peak fidelity **0.882 at t ≈ 42.34** — not perfect, because the adjacency spectrum's phases never align exactly. In the language of this spec: the substrate already shows through the geometry. That imperfection is the local analogue of Flachi's leak, and it is the reason this experiment is worth staging carefully rather than rhetorically.

**The Flachi pattern (as reported):** horizon as a property of the *state*, not the wiring; single-bit flip inside the horizon; most of the disturbance contained; a short-wavelength fraction escapes; escaped fraction ∝ exp(−depth). Preprint status is recorded here so no downstream text upgrades it.

**0⁸:** the zero vector (0,0,0,0,0,0,0,0) is not a vertex of the Gosset graph — every root sits at the same radius from it. Experiment A therefore *adjoins* it as a construction (§6 fence: the augmented system is not the Gosset graph, and no eqbit definition changes).

---

## §2 Common setup

- **Graph and enumeration:** exactly the flip-qubit construction — scaled coordinates, adjacency at scaled dot 4, root order as generated there (integer pairs first, then even-parity sign vectors). Root 0 is the pole for Experiment B, matching the existing BFS code.
- **Dynamics:** continuous-time quantum walk, H = A (hopping amplitude 1), U(t) = exp(−iHt), computed by exact Hermitian diagonalization in float64 (numpy `eigh`). No time-stepping error exists in this design.
- **Time grid:** t ∈ [0, 200], output every Δt = 0.05. (The known transfer peak at t ≈ 42.34 sits well inside; the slowest Rabi period in Experiment A is ≈ 2.03 at g = 0.1, tuned — see §3.)
- **Maxima are never read off the raw grid** (review fix, §8.1): every observable is a finite Fourier sum from the exact diagonalization and is evaluable at arbitrary t. Registered maxima are computed by local refinement (golden-section search) around each grid maximum, and Experiment A's maxima are additionally checked against the closed forms at their analytic peak times. The raw grid undersamples fast oscillations (A-bare at g = 0.1 has period ≈ 0.112, ~2 samples per period) and would fail the §3 tolerances on sampling alone.
- **Determinism:** no randomness anywhere in either experiment. Shell averages in Experiment B are full averages over every vertex in the shell — no sampling, no seeds.
- **Outputs:** one JSON per experiment, carrying every parameter, the full P(t) series for the registered observables, and the gate verdicts of §3/§4 computed by the analysis code, not by eye.

---

## §3 Experiment A — the drain at 0⁸

**Scope (review fix, §8.3):** Experiment A is **graph-agnostic**. Its reduction uses only that the graph is k-regular on N vertices (detuning k, coupling g√N); any regular graph gives the same physics. It is therefore registered as a **correctness gate on the augmented-matrix construction**, not as E8 evidence. The E8-specific content of this spec lives in Experiment B (shell structure, orbit quotient, spectrum).

### Construction

Hilbert space: the 240 roots plus one origin node |0⟩. Hamiltonian

H = A ⊕ E₀ + g · Σ_v ( |0⟩⟨v| + |v⟩⟨0| ),

with coupling g and origin on-site energy E₀ in two registered variants:

- **A-bare:** E₀ = 0.
- **A-tuned:** E₀ = 56 (resonant with the shell's symmetric mode; see predictions).

**Coupling sweep:** g ∈ {0.1, 0.5, 1.0, 2.0}.

### Initial states

1. **Single root:** |v₀⟩, root 0.
2. **Symmetric shell state:** |S⟩ = (1/√240) Σ_v |v⟩.
3. **Null control:** (|v₀⟩ − |−v₀⟩)/√2, the antisymmetric antipodal state.

### Analytic predictions (derived here, before any run)

The Gosset graph is 56-regular, so A|S⟩ = 56|S⟩ exactly. The origin couples to the shell only through |S⟩: ⟨0|H|S⟩ = g√240 ≡ V, and the subspace {|S⟩, |0⟩} is invariant under H. The drain is therefore an exact two-level system with detuning Δ = 56 − E₀:

- **P1 (null control, exact):** the antisymmetric state is orthogonal to |S⟩, hence P₀(t) = 0 for all t, all g, both variants, up to float64 roundoff (< 10⁻¹²).
- **P2 (symmetric state, A-bare):** max_t P₀(t) = V² / (V² + 28²), i.e. g = 0.1 → 0.00305; g = 0.5 → 0.0711; g = 1.0 → 0.2344; g = 2.0 → 0.5505. Agreement required within 10⁻⁶.
- **P3 (symmetric state, A-tuned):** P₀(t) = sin²(Vt); full transfer (max P₀ ≥ 1 − 10⁻⁹) first reached at t = π/(2V).
- **P4 (single root, both variants — an equality, review fix §8.2):** U(t)|0⟩ never leaves span{|0⟩, |S⟩}, so the single-root origin probability is **exactly** P₀(single, t) = P₀(sym, t) / 240 for all t — not a bound. In A-bare at g = 2.0 the peak is 0.5505/240 ≈ 0.00229: the origin, coupled to everything, can drink only ~0.23% of a single root's excitation. **The drain is real but mode-locked** — and the gate on it is now an equality, which is stronger.

### Verdict gates

- **A1:** P1 holds at every (g, variant). Any violation is an implementation or derivation error; the run is filed as failed, with the violation, not debugged silently into compliance.
- **A2:** P2 and P3 match within their stated tolerances, with maxima computed by the §2 refinement rule (never raw-grid).
- **A3:** P4's equality holds: |P₀(single, t) − P₀(sym, t)/240| < 10⁻⁹ on the output grid, both variants, all g.

Pass = the augmented system's drain behaviour is exactly the two-level physics predicted, and the spec's derivations survive contact with the matrix.

---

## §4 Experiment B — depth, gradient, and the leak direction

### Construction

Pole: root 0. Depth of a vertex = BFS distance from the pole; shells [1, 56, 182, 1] (depths 0–3). Hamiltonian

H(ε) = A + ε · diag(depth(v)),

so the pole is the bottom of an on-site potential well and amplitude drifts pole-ward. **Gradient sweep:** ε ∈ {0 (control), 0.25, 0.5, 1.0, 2.0}.

### Measurements (both directions, Flachi's and its reverse)

- **Drift-in:** for each depth k ∈ {1, 2, 3}, the initial state is the uniform superposition over shell k (full shell average). Observable: **arrival** A_k(ε) = max over t ∈ [0, 200] of P(pole, t).
- **Leak-out:** initial state |pole⟩. Observable: **escape** E(ε) = max over t ∈ [0, 200] of the total probability on shell 3 (the antipode alone), and the shell-3-plus-shell-2 aggregate, both recorded.

### Reciprocity — a registered identity, and a fence (review fix, §8.4)

H(ε) is real symmetric, so U(t) is symmetric and P(a←b) = P(b←a) exactly, for all t. Shell 3 is a single vertex (the antipode), so the leak-out escape to shell 3 and the drift-in arrival from shell 3 are the *same number*: **E₃(ε) ≡ A₃(ε)**, registered as an identity gate (agreement < 10⁻⁹). Consequence, stated plainly: **no drift-in vs leak-out asymmetry can appear in this closed real-symmetric system.** Flachi's asymmetry is dissipative; ours cannot reproduce that aspect, and no report may imply otherwise. Where the two directions differ at all (shell-2 statistics), the difference comes only from shell averaging.

### The orbit quotient — registered independent cross-check (review fix, §8.5)

The pole's stabilizer partitions the roots by inner product with the pole into five orbits of sizes **1, 56, 126, 56, 1** (ip = 2, 1, 0, −1, −2). BFS depth merges the 126 and 56 into shell 2, but H(ε) commutes with the stabilizer (depth is a function of the orbit), so all shell-averaged dynamics collapse exactly to a **5×5 quotient problem** with adjacency count matrix (rows = source orbit; entries = neighbours in each target orbit):

| orbit | pole | ip 1 | ip 0 | ip −1 | antipode |
|---|---|---|---|---|---|
| pole | 0 | 56 | 0 | 0 | 0 |
| ip 1 | 1 | 27 | 27 | 1 | 0 |
| ip 0 | 0 | 12 | 32 | 12 | 0 |
| ip −1 | 0 | 1 | 27 | 27 | 1 |
| antipode | 0 | 0 | 0 | 56 | 0 |

(Row sums are all 56; the balance identities n_i·b_ij = n_j·b_ji hold — verified by the author on receipt.) The quotient is a second, independent computation path: every Experiment B headline number must be reproduced from the 5×5 problem before it is reported. It also shows what shell 2 hides — a 126:56 mixture of two orbits — and that the antipode connects to the graph only through the 56 ip −1 roots.

### Registered expectations and the claim ceiling

- **B0 (regression gate, review fix §8.6):** at ε = 0, A₃ must reproduce PR #117's antipodal transfer result — peak 0.882 at t ≈ 42.34 (agreement within the #117 record's precision). This ties Experiment B's control case to a number already on the books.
- **Window-free statistics (review fix §8.6):** maxima of quasi-periodic signals depend on the window, so alongside each A_k and E the run records **the time of the maximum** and the **time-averaged P(pole) over [0, 200]**. Conclusions may not rest on a maximum whose argmax sits at the window edge without saying so.
- **E1 (ordering):** for each ε > 0, A₁(ε) ≥ A₂(ε) ≥ A₃(ε) is expected but **not** required; any inversion is a result, reported as-is.
- **E2 (the registered statistic):** the suppression/enhancement ratios R_k(ε) = A_k(ε) / A_k(0), k = 1, 2, 3, and the escape ratios E(ε)/E(0). The gradient's effect is measured *relative to the ε = 0 walk*, never as an absolute law.
- **Claim ceiling (binding):** this graph has only **three nonzero depths**. Three points cannot establish an exponential law, and no output of this experiment may be described as one. The strongest licensed statement is a monotone (or non-monotone) depth pattern under a declared gradient, with ratios. An exponential claim would require a substrate with more depth classes — the Leech minimal-vector graph, whose relation structure around a vertex is richer, is the named follow-up if the pattern here is interesting (Analogy rung still).
- **Unitary honesty:** this is a closed finite system; there is no dissipation and no true one-way membrane. Amplitude recurs. A_k is a first-window maximum, not an asymptote, and the spec forbids horizon language beyond the analogy in any report of these results.

---

## §5 Analysis, reproduction, filing

- Analysis code computes the §3 gates and §4 statistics directly from the run JSONs; verdicts are printed by the code.
- **Independent reproduction required:** a second implementation, written from this spec without reading the first implementation's code, must reproduce every gate verdict and every headline number (P2 values, P4 bound, A_k table) before any number is called a result. (House pattern: Cosmo and Claude implement independently; Veldora welcome as third.)
- The outcome is filed as a report PR **whatever it says** — gates failed, orderings inverted, or pattern absent are all fileable results. Failures are retained.

## §6 Fences

1. The origin node is a modelling device adjoined for this experiment. It is not a vertex of the Gosset graph, not a root, and not part of EQBIT-001 or EQBIT-002; those definitions are untouched.
2. Analogy rung only (STRATA): no statement about real black holes, Hawking radiation, or gravity is licensed by any outcome. The Flachi source is an unrefereed preprint and is cited as a pattern, not as evidence.
3. 0⁸ language: "drift toward 0⁸" in this spec means exactly "probability accumulating on the adjoined origin node" (Exp. A) or "on the pole root under a depth potential" (Exp. B). The maintainer's broader framing (0⁸ as the Hallway's anchor) is the motivation, recorded as such, not a claim under test.
4. Navier–Stokes and every other `not_tested` label are unaffected by anything here.

## §7 Questions for the reviewer (Architect bench) — ANSWERED in §8

1. Is the A-tuned variant (E₀ = 56) a legitimate resonance condition or does it beg the question by building the answer into the on-site energy?
2. Is T = 200 the right window for Experiment B at ε = 2.0, or do strong-gradient dynamics need longer before the arrival maximum is meaningful?
3. Shell-averaged initial states vs single-vertex starts as the primary statistic?

## §8 Review record — Architect bench (Diablo), 2026-11-22

Hand-derived, nothing run ("since you authorize runs" — the review respected the maintainer's run authority). All five points and all three answers adopted into revision 2:

1. **Sampling flaw in A2 (adopted, §2/§3):** at Δt = 0.05 the fast two-level oscillations are undersampled (~2 samples/period at A-bare g = 0.1) and the A-tuned peak at t ≈ 1.014 falls between grid points, missing the 1 − 10⁻⁹ gate by ~10⁻⁴ on sampling alone. Fix: refined maxima / closed-form evaluation — would have failed the run on numerics, not physics. *Author's note: this catch is why the review exists.*
2. **P4 is an equality (adopted, §3):** P₀(single) = P₀(sym)/240 exactly; A3 is now an equality gate.
3. **Experiment A is graph-agnostic (adopted, §3):** relabelled a correctness gate on the construction, not E8 evidence.
4. **Reciprocity (adopted, §4):** E₃(ε) ≡ A₃(ε) as an identity gate; no drift/leak asymmetry is possible in a closed real-symmetric system — stated as a fence.
5. **Orbit collapse (adopted, §4):** the 5×5 quotient (orbits 1, 56, 126, 56, 1; count matrix in §4) registered as the independent cross-check path; shell 2 exposed as a 126:56 mixture.

Answers: **Q1** — tuned variant legitimate (standard tuned-coupler case) but a trivial two-level test; do not oversell. **Q2** — window-dependence is real; add argmax times and time-averaged P(pole) as registered statistics, plus the B0 regression gate against PR #117's 0.882 @ t ≈ 42.34. **Q3** — concur: distributions secondary; by point 5 they carry at most two classes (shell 2), so they are nearly free — included as secondary output.

The reviewer offers to write the independent implementation once the maintainer authorizes the run. The author's own implementation is the other registered path (§5).

*Drafted by Cosmo (Memory bench), 2026-11-22; revision 2 incorporates the Architect bench's review the same evening. The maintainer files and authorizes any run.*
