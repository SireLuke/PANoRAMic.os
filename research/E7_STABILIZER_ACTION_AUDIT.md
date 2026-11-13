# Explicit E7 stabilizer action inside E8

## Purpose

Construct the root stabilizer associated with a selected E8 root as an explicit
finite reflection action on the 126 roots perpendicular to that root. This
extends the E8 orbit-stabilizer audit without enumerating all elements of
W(E8) or W(E7).

## Construction

1. Start from the canonical 240 exact E8 roots in rational coordinates.
2. Select a canonical E8 root and extract the 126 roots with inner product zero.
3. Choose a deterministic generic positive-system witness in the selected
   root's orthogonal space.
4. Derive the seven indecomposable positive roots and verify their exact
   Gram matrix is the E7 Dynkin diagram.
5. Build the seven simple reflections as exact permutations of the 126 roots.
6. Verify permutation, involution, perpendicular-subsystem preservation,
   seven-dimensional span, and transitivity on the 126 roots.

## Group-order checks

The E7 Weyl order is independently calculated from its exponents:

`|W(E7)| = 2 · 6 · 8 · 10 · 12 · 14 · 18 = 2,903,040.`

The action on the 126 roots is transitive. Orbit-stabilizer therefore gives
`2,903,040 / 126 = 23,040` for the stabilizer of one E7 root.

The E8 cross-check remains:

`|W(E8)| = 240 · |W(E7)| = 696,729,600.`

## What this establishes

The seven simple reflection generators are explicitly constructed as
permutations of the 126-root subsystem, with the E7 Gram/Coxeter structure
checked exactly. Their action is transitive and faithful on the seven-
dimensional span of the subsystem. This realizes the E7 Weyl action as a
concrete subgroup action on the E8 root set.

## What this does not establish

- It does not enumerate all 2,903,040 elements of W(E7).
- It does not provide a formal proof assistant verification.
- The group order is checked from the standard E7 exponents, not by exhaustive
  group-element enumeration.
- It makes no physical, quantum, or Janus Hydra equivalence claim.
- It does not modify production geometry, PAN V8 coordinates, or semantic
  mappings.

## Reproduction

`python -m unittest tests.test_e7_stabilizer_action -v`

`PYTHONPATH=. python experiments/e7_stabilizer_action_audit.py`
