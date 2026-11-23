# Valdora Leech local association-algebra reconstruction audit 001

**Status:** PASS — exact rational reconstruction of the recorded local eigenmatrix.
**Scope:** Algebraic consistency audit of the 4-class scheme recorded for one Family-A reference neighborhood in `experiments/leech24_eqbit_001/results/local_shell_audit.json`.
**Not claimed:** a fresh execution of `local_shell_audit.py`, a fresh enumeration of the 196,560-vector shell, cross-family scheme equality, or a global Leech graph computation.

## 1. Question

Does the recorded 4-class local eigenmatrix and multiplicity vector reconstruct a valid set of integral, nonnegative intersection parameters under the standard association-scheme inversion formula?

This is the next algebraic gate after the direct local-shell report. It is deliberately separate from the earlier seven-relation global spectral-parameter audit.

## 2. Frozen input

The local relation order is `[I, R16, R8, R0, R-16]`, with valencies

`k = [1, 891, 2816, 891, 1]`

and primitive multiplicities

`m = [1, 23, 275, 2024, 2277]`.

The first eigenmatrix used (rows are primitive eigenspaces; columns are the five relations in the order above) is

```text
P = [
  [1,  891,  2816,  891,  1],
  [1,  297,     0, -297, -1],
  [1,   63,  -128,   63,  1],
  [1,   -9,    16,   -9,  1],
  [1,   -3,     0,    3, -1],
]
```

The local neighborhood has `v = 4600` vertices. Inputs were read from the recorded local-association-scheme section of the result artifact; they were not regenerated from the shell in this audit.

## 3. Exact reconstruction

For relation indices (i,j,k), reconstruct

[
p_{ij}^{k} = \frac{1}{v k_k}
\sum_{r=0}^{4} m_r P_{ri}P_{rj}P_{rk}.
]

All arithmetic was performed with exact rational numbers (SymPy rationals), not floating point.

**Result:** all 125 ordered intersection parameters (5 × 5 × 5) are nonnegative integers. Their distinct values are

`{0, 1, 42, 162, 336, 512, 567, 891, 1680, 1792, 2816}`.

The maximum reconstructed parameter is 2,816.

## 4. Invariants checked

- Eigenmatrix orthogonality: `P^T diag(m) P = 4600 diag(k)` — PASS.
- Integrality and nonnegativity of all 125 reconstructed (p_{ij}^{k}) — PASS.
- Commutativity: (p_{ij}^{k}=p_{ji}^{k}) for all indices — PASS.
- Identity relation: (p_{ij}^{0}=k_i\delta_{ij}) — PASS.
- Weighted balance identities (k_k p_{ij}^{k}=k_i p_{kj}^{i}) and (k_k p_{ij}^{k}=k_j p_{ik}^{j}) — PASS (250 scalar checks).
- Weighted product sums (sum_k k_k p_{ij}^{k}=k_i k_j) — PASS (25 scalar checks).
- Total valency including identity: (sum_i k_i=4600) — PASS.

## 5. Interpretation

The stored local eigenmatrix and multiplicities are internally consistent with a symmetric 4-class association algebra. This independently verifies the algebraic reconstruction of the table; it does **not** independently verify that the recorded eigenmatrix arose from the actual Leech shell. That geometric evidence remains the exact integer-dot enumeration and packed-bitset pair census in the source result artifact.

The induced 4,600-vertex graph is not strongly regular: its nonadjacent pairs split across multiple inner-product relations with different common-neighbor counts. The association-scheme description is therefore the more appropriate local object than a single strongly-regular-graph parameter set.

## 6. Next gate

The next useful geometric computation is to execute the repository runner from a frozen commit and compare its emitted output against the recorded result artifact, then run the full local relation-closure audit for Family B and Family C (or establish the transport through a cited Co0 action argument). Do not promote the Family-A local scheme to a universal all-root result based only on this reconstruction.

## 7. Provenance and reproducibility

- Repository: `SireLuke/PANoRAMic.os`
- Input artifact: `experiments/leech24_eqbit_001/results/local_shell_audit.json`
- Runner inspected: `experiments/leech24_eqbit_001/local_shell_audit.py`
- Computation: independent analysis runtime; exact rational arithmetic.
- This report is an algebraic reconstruction audit, not a claim that the repository runner or CI was executed in this batch.
