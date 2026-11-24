# VOA floor dimensions — per-sector census of V^natural

`voa_floor_dimensions.py` computes, in exact integer arithmetic, the
dimension of each weight floor of the Monster VOA split by FLM orbifold
sector:

| floor n | untwisted V_Lambda,n^+ | twisted V_Lambda,n^{T,+} | total |
|--------:|-----------------------:|-------------------------:|------:|
| 0 | 1 | 0 | 1 |
| 1 | 0 | 0 | 0 |
| 2 | 98,580 | 98,304 | 196,884 |
| 3 | 10,745,856 | 10,747,904 | 21,493,760 |
| 4 | 432,155,586 | 432,144,384 | 864,299,970 |
| 5 | 10,122,903,552 | 10,122,952,704 | 20,245,856,256 |

The totals are the coefficients of J(tau) = j(tau) − 744; the script
asserts them for weights 0..5 on every run. Floor 2 is the Griess
algebra's split: 98,280 antipodal lattice pairs + 300 symmetric
oscillators untwisted, and 24 × 4,096 twisted.

## Provenance and correction

The algorithm came from a bench draft relayed by Lucas on 2026-11-23.
Cosmo graded the draft the same evening:

- The draft's prose floor table was exact, but its script read the
  untwisted state count at index n−1, printing every untwisted count
  one floor too low (floor 2 total came out 98,304). The filed script
  carries the one-index correction, marked `INDEX FIX`, and its output
  above is the verified run.
- The draft's §1 decomposition "196,560 + 300 + 24 = 196,884" is not
  used: the orbifold folds the 196,560 minimal vectors into 98,280
  pairs, and the twisted sector contributes 24 × 4,096 = 98,304, not
  24. The correct split is the one in the table.

## Scope

Dimension counting only — the census the tower stands on. No states
are constructed, no Griess product is computed, and no group action is
represented. Filed at Lucas's direction, 2026-11-23.
