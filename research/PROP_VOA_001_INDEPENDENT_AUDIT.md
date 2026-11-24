# PROP-VOA-001 — independent specification audit

**Status:** preliminary independent audit; no preregistered experiment run.
**Implementation target:** Python standard library, existing PANoRAMic.os modules.

## Reuse map

- `experiments/moonshine_sierpinski/lattice_modular_audit.py`:
  `leech_theta_reference` supplies the exact Leech shell coefficients from
  (E_4^3-720\Delta).
- `experiments/moonshine_sierpinski/leech_z2_orbifold_character.py`:
  `leech_z2_orbifold_character` supplies the independent aggregate
  untwisted/twisted q-series census.
- `core/seed_sharing/contract.py`:
  `SeedEnvelope.to_record` supplies canonical JSON, provenance, and a
  SHA-256 content address for the immutable B1/B2 base.
- `experiments/menger_seed/propagation.py` is reused as an engineering
  pattern only: immutable base reference, bounded local deltas, fail-closed
  budgets. Its Menger face graph is deliberately not imported or used.

All new arithmetic is exact integer arithmetic. No NumPy or third-party
runtime dependency is introduced.

## Explicit interpretation used for the diagnostic

For an occupancy (r_m) of one oscillator mode, the 24 bosonic colors
contribute ({23+r_m\choose23}). The multiplicity for a partition type is
the product over its occupied modes.

- Untwisted shell (k=0): only even oscillator-count classes are projected
  into the orbifold census. Odd-count classes are retained as explicitly
  marked, unprojected bridge nodes so a one-grade D1 path can pass through
  the odd sector.
- Untwisted shell (k>0): each antipodal pair ({\lambda,-\lambda})
  contributes one invariant combination for every oscillator state. Both
  oscillator parities therefore occur, with multiplicity
  (S_k/2) times the oscillator color multiplicity.
- Twisted sector: the 4096-dimensional ground space is at weight (3/2);
  fixed classes have an odd number of half-integer oscillators. A half-mode
  is encoded by its odd doubled mode number (1,3,5,\ldots).

This makes the distinction between projected census classes and transit-only
bridge classes explicit instead of silently counting unprojected states.

## Preliminary diagnostic results

The standard-library enumerator produces 44 class records across floors 0–5,
of which 34 are projected census classes and 10 are unprojected vacuum-shell
bridge classes. Per-floor record counts are 1, 1, 4, 7, 12, 19.

The projected class multiplicities reproduce the PR #197 sector splits:

| Floor | Untwisted fixed | Twisted fixed | Total |
|---:|---:|---:|---:|
| 0 | 1 | 0 | 1 |
| 1 | 0 | 0 | 0 |
| 2 | 98,580 | 98,304 | 196,884 |
| 3 | 10,745,856 | 10,747,904 | 21,493,760 |
| 4 | 432,155,586 | 432,144,384 | 864,299,970 |
| 5 | 10,122,903,552 | 10,122,952,704 | 20,245,856,256 |

The canonical class-table JSON is 4,891 bytes in this diagnostic encoding,
below the 65,536-byte ceiling. Floor 5 describes approximately 4.14 million
states per serialized byte. This is a diagnostic measurement, not yet the
frozen preregistered result.

## Specification discrepancies that must be reconciled before the formal run

1. **Vacuum-sector closure.** If the class table contains only projected
   (\lambda=0) states, floor 2's two-mode class has no floor-1 parent,
   because floor 1 is projected out. The same issue recurs for all-ones
   even-count partitions. The diagnostic includes odd-count (\lambda=0)
   bridge nodes, marked `projected=false`; they contribute no census
   multiplicity. Confirm that these transit-only nodes are permitted.
2. **Twisted seed.** The floor-2 twisted class is seeded from the 3/2-weight,
   4096-dimensional twisted ground space plus one 1/2-mode. It is not a
   Leech shell seed and has no integer-floor-1 parent. The D2/D3 seed
   distinction must be explicit.
3. **Twisted D1 step.** A one-grade transition in the half-integer sector
   either raises one half-mode by 1, or adjoins a pair of 1/2-modes. Adjoining
   one 1/2-mode alone changes the conformal weight by 1/2 and leaves the
   integer-floor grading. Clarify that the budget means one unit of
   conformal grade, not necessarily one oscillator creation operator.
4. **Permutation control.** Permuting multiplicities among classes within
   one floor and sector preserves the aggregate sector sum. It therefore
   cannot fail aggregate C1 as currently worded. Add a classwise C1 check
   against the canonical formula/table; the permutation control should fail
   that check while the aggregate sum remains unchanged.

## Current disposition

The arithmetic and compression diagnostic is promising, and the class graph
closes under the explicitly declared D1/D2/D3 rules. The formal PROP-VOA-001
run remains gated on independent-spec reconciliation, particularly the four
items above. No states, Griess product, vertex operators, or Monster action
are constructed or claimed.
