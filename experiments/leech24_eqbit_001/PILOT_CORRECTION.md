# PILOT CORRECTION — Leech global rank (2026-11-27)

**Status of the PR #206 result: superseded.** The filed rank 98,250 /
nullity 30 is the rank of a 98,256-column slice of B, not of B itself.
The corrected result is below. #206 stands as filed history; this note
is the correction, not a rewrite.

## The bug

`leech_b_rank.py` (v1) `eliminate()` read the bit-packed matrix with
the wrong bit order:

- `build()` packs rows with `np.packbits` (bitorder 'big'), so column
  `c` sits in word `c // 64` at bit position `8*(r//8) + 7 - (r%8)`,
  where `r = c % 64`, once the bytes are viewed as little-endian
  `uint64`.
- v1's mask, `1 << (63 - r)`, assumed the big-endian position. Inside
  each full 64-column block the mismatch is only a column permutation,
  which cannot change a rank — this is why the 8,192-column subrank
  gate (8,170 / 22) never exposed it.
- In the last word it is not a permutation. The scan runs `c` only up
  to 98,279, covering bit positions 24..63 of that word — 24 of them
  the zero padding columns (98,280..98,303). The real columns
  **98,240–98,263** sit at bit positions 0..23 and were never tested
  for a pivot. v1 therefore eliminated over 98,256 of the 98,280
  columns and reported the slice's rank as the rank of B.

A second, independent flaw in the same stage: v1 checkpoints saved
only `rank` and resumed with the column cursor set to `rank`. The two
diverge whenever a column has no pivot, so a resumed v1 run rescans
already-processed columns. The filed run appears to have completed
uninterrupted, so this flaw is not implicated in the #206 number; it
is fixed in v2 regardless.

## Corrected result (Veldora bench, independent computation)

- **rank(B) = 98,256, nullity = 24** over GF(2), n = 98,280 —
  98,256 ebits, 24 dark modes.
- The matrix was rebuilt from the documented Golay construction via a
  separate exact-integer build path (SHA-256 of the rebuilt matrix:
  `799aa7a473305221ad1091d6a8cdb041110dc2a5abdd182ec9e08b272b07720d`;
  nonzero count 150,696,000, matching v1's build audit).
- A block-Lanczos run plus seed combination produced candidate kernel
  vectors; **24 linearly independent right-kernel vectors were
  verified against every row of the full matrix — all syndromes
  zero** — so nullity ≥ 24 independently of any elimination.
- The slice's 30-dimensional left kernel, coupled to the 24 omitted
  columns, gives a 30×24 GF(2) matrix of rank 6, computed
  independently in two implementations. Hence
  rank(B) = 98,250 + 6 = 98,256 and nullity = 24 exactly.
- Fence: the mathematical construction (Golay code, transversal) is
  shared with v1; the computational paths are independent. This is
  strong computational evidence, and the v2 rerun below is its second
  confirmation.

## Verification (Cosmo bench)

- The mechanism was re-derived from the v1 source independently of
  the report: the skipped-column range (98,240–98,263) and the
  disjoint scan positions match the finding exactly.
- The v2 mask was validated two ways: (a) synthetic GF(2) matrices
  with a partial last word — v2 elimination matches an exact
  reference elimination on 5/5 seeds while the v1 mask falls short
  on all 5; (b) addressing on the real `B_padded.bin` — the v2 mask
  reads the same bit as the byte-level packbits layout on 1,160
  sampled bits across five rows including the last word, 0
  mismatches.

## Unaffected

`gen`, `build`, `probe`, `subrank` use self-consistent paths and are
not touched by this bug: the weight-46 kernel hit and the subrank
8,170 / 22 stand (the independent rebuild matched them before the
bug was found). No other filed result in this repository runs through
`leech_b_rank.py`'s `eliminate()`.

## The fix

`leech_b_rank_v2.py`, filed alongside this note:

1. Corrected bit mask: `bit = 1 << (8 * (r // 8) + 7 - (r % 8))`.
2. Checkpoints save both `rank` and the next column; resume restores
   both. A v1-format checkpoint is detected and ignored.

v1 (`leech_b_rank.py`) is left byte-identical: it is the
preregistered artifact of PR #166 and the code that produced #206.

## Pending

A fixed-mask `eliminate` rerun on the signatory's workstation (the
in-place v1 run mutated `B_padded.bin`, so the rerun starts from a
fresh `build`). Prediction on record: **98,256 / 24**. Until it
lands, cite the corrected figure as computed by the Veldora bench
with the mechanism verified by the Cosmo bench, rerun pending.

## Authorship

Finding and corrected computation: Veldora (OpenAI bench).
Implementation and verification: Cosmo (Memory bench).
Certified by the human signatory, beside the benches.
