# Leech global rank pilot — RESULT

- **Result: rank(B) = 98,250; nullity = 30; n = 98,280.**
- Preregistration: OS PR #166 (Veldora). Script: `leech_b_rank.py`
  (this folder). Definition per `leech_b_rank.md`: B is the GF(2)
  antipodal matrix of the Leech minimal shell, B[a][b] = 1 iff
  ⟨a,b⟩ = −16 scaled, over the 98,280 first-nonzero-positive
  transversal representatives.
- rank(B) is the antipodal cut entanglement of the Leech graph state
  in ebits; the nullity is the number of independent dark antipodal
  modes (kernel vectors of B).

## Run record — Lucas's PC (the completed run)

- Machine: Ryzen 5600X, 48 GB RAM, Windows, Python 3.14.
- 2026-11-24: `gen` (98,280 reps; families A/B/C = 552 / 48,576 /
  49,152), `build` (nonzeros 150,696,000; density 0.0156; row audit
  passed), `probe` (KERNEL HIT coord0==+4, weight 46; 1 hit,
  1 independent).
- 2026-11-26 16:31 CST: `probe` re-verified from cache — identical hit.
- 2026-11-26 16:47 CST: `subrank` —
  `{'submatrix': 8192, 'rank': 8170, 'nullity': 22}` (the gate value;
  the run proceeded because it matched).
- 2026-11-26 16:50:37 CST: `eliminate` launched. Completed the same
  evening; `rank_result.json` received by Cosmo 21:10 CST
  (wall time ≈ 3.9 h). Pace observed from the runner's own progress
  lines: first checkpoint (rank 512) in 51 s; blocks of 512 pivots at
  ~2 min 12 s early, tightening steadily to ~26 s in the final
  stretch; no interruption.
- Result file: `results/rank_result.json` (this folder), exactly as
  written by the script: `{"rank": 98250, "nullity": 30, "n": 98280}`.

## Dual-machine status

- The construction half — `gen`, `build`, `probe`, `subrank` — was
  reproduced **bit-for-bit** on Cosmo's VM on 2026-11-24 (identical
  family counts, nonzero count, kernel hit, and subrank 8170 / 22),
  so the matrix eliminated on Lucas's PC is the preregistered matrix.
- Cosmo's own `eliminate` lane is **still in flight** (checkpoint
  rank 6,144 at filing time, checkpoint-resumed across repeated host
  reboots). The second full-machine confirmation of 98,250 is
  therefore **pending**, and this record will be updated when it
  lands. Until then the result stands as: one complete run,
  dual-verified construction, exact deterministic arithmetic
  (any correct re-run must agree exactly).

## Consistency checks

- 98,250 + 30 = 98,280 ✓
- Respects the proven bound rank ≤ 98,279 (nullity ≥ 1, from the
  probe's kernel vector) ✓ — nullity 30 ≥ 1.
- Advance estimate on record (Cosmo, chat, 2026-11-25): nullity in
  the tens to low hundreds. Measured: 30.

## Reading

- The Leech antipodal cut carries **98,250 ebits**; the kernel —
  patterns the antipodal relation annihilates completely — has
  dimension **30**, a dark fraction of 0.03%. The Gosset/E8 analogue
  is 112 of 120 (nullity 8, dark fraction 6.67%): proportionally the
  Leech cut is over 200× tighter.
- One kernel vector is known explicitly (the probe's coord0==+4
  indicator, weight 46). This run measured the rank only; a kernel
  **basis** was not extracted and remains an open follow-on.
- Scope fence: this is an exact computation about the τ = 2
  antipodal matrix of the Leech shell as defined in
  `leech_b_rank.md` — the Leech rung of the antipodal ladder. It
  certifies nothing beyond that matrix.

Filed 2026-11-26 at Lucas's direction ("push them to git … share our
results"). Run by Lucas; record written by Cosmo.
