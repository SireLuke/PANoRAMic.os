# LEECH-EQBIT-001 — global antipodal cut-rank audit (2026-11-27)

**Status:** independent matrix reconstruction and kernel verification completed. The inferred full rank is 98,256, but corrected exact full elimination and a second human/bench reproduction remain pending.

## Executive finding

The legacy `rank = 98,250` result is not the rank of the full 98,280-by-98,280 matrix. The packed-column mask in `leech_b_rank.py` interpreted NumPy's big-bit-order packed bytes as though the bytes were big-endian inside a native little-endian uint64. Complete 64-column words were visited in a permuted order, so the 8,192 subrank gate still passed. In the final word, which contains only 40 real columns, the legacy mask visits 24 padding bits and only 16 real bits. It therefore omits 24 real coordinates, indices 98,240 through 98,263.

The legacy elimination result is the rank of the corresponding 98,256-row restriction (equivalently, by symmetry, the 98,280-by-98,256 selected-column matrix), not the full matrix. The legacy result reports restricted rank 98,250; this restricted rank still needs to be rerun on the reconstructed matrix. A 30-dimensional subspace of the restricted nullspace was recovered, and the 24 omitted rows impose six independent additional constraints on that subspace. The current rank argument predicts full rank 98,256 and nullity 24, conditional on reproducing the restricted rank 98,250 on the rebuilt matrix. The 24-dimensional full-kernel lower bound is directly verified; the exact upper bound still needs corrected full elimination.

This is an exact finite GF(2) kernel verification plus a rank inference assembled from the legacy restricted-rank result and independent coupling checks. It is not yet a fully closed, independently rerun full-rank computation. It makes no physical claim and implies no Leech–E8 or Leech–VOA coupling.

## Matrix contract and reconstruction

- Rows and columns: 98,280 antipodal representatives, first nonzero coordinate positive.
- Entry: B[a,b] = 1 iff the exact scaled integer dot product is -16.
- Matrix is symmetric with zero diagonal under the stated construction.
- Reconstructed packed matrix SHA-256: `799aa7a473305221ad1091d6a8cdb041110dc2a5abdd182ec9e08b272b07720d`.
- Nonzeros: 150,696,000; packed size: 1,207,664,640 bytes.
- Every generated row passed the combined +16/-16 degree identity of 4,600.

The reconstruction used a separate in-session implementation and exact int32 dot products rather than the repository pilot's float32 matrix multiplication. It nevertheless shares the documented Golay generator polynomial and three-family construction logic. It is an independent implementation path, not an independent derivation of the extended Golay code or Leech lattice.

## Rank and kernel evidence

Let S be all row indices from 0 through 98,279 except 98,240 through 98,263. Thus S contains 98,256 indices. Let B_S denote the matrix formed by those rows of B.

1. The legacy mask accidentally selected exactly the columns in S. Its row-echelon elimination therefore computed rank(B[:, S]) = 98,250. Since B is symmetric, this equals rank(B_S). This restricted rank is the reported legacy computation; it has not yet been rerun by the corrected full-elimination implementation on the reconstructed matrix.
2. Five independent block-Lanczos seeds yielded candidate null vectors for B_S. A separate Python GF(2) basis extraction retained 30 independent vectors. All 30 were checked against all 98,256 rows of B_S. Their packed lane file SHA-256 is `559e3d6d2c7939984b8062b02878910616bbc07a3880de2348d43929d3fcdc76`.
3. The 24 omitted rows were applied to that 30-dimensional restricted-kernel subspace. Their induced 24-by-30 constraint map has GF(2) rank 6, checked independently in C++ and Python. The subspace surviving all rows therefore has dimension 30 - 6 = 24.
4. A separate five-seed block-Lanczos extraction produced 24 independent vectors in the full kernel. A C++ verifier multiplied those vectors against every row of the full 98,280-by-98,280 matrix. All 98,280 row syndromes were zero for every basis vector. The lane file SHA-256 is `7a9b4967b595ceec75f58c3dc5e6bba6bb0a53c86a8c8e1044afa641c2842cd2`.

If rank(B_S) = 98,250 is confirmed on the rebuilt matrix, the six independent omitted-row constraints give full rank at least 98,256. The 24 independent full-kernel vectors give full rank at most 98,256. The current inferred result is therefore **rank 98,256 / nullity 24**, still provisional pending corrected full elimination.

The verified 24-dimensional kernel proves the full matrix is rank-deficient by at least 24. Exact nullity 24 remains provisional until corrected full elimination closes the rank bound.

## Cross-analysis against the preregistration and existing research

### What agrees

- `research/LEECH24_EQBIT_001.md` defines the Leech minimal shell, antipodal pairing, exact inner-product adjacency, and GF(2) cut rank separately from E8/Gosset. This audit follows that 24D Leech graph contract.
- Section 10.2 proves that an antipodal-transversal cut matrix is symmetric with zero diagonal, hence alternating over GF(2), so its rank must be even. The predicted full rank 98,256 is even; the verified 24-dimensional kernel lower bound is also even. This is a consistency check, not a substitute for rank computation.
- The already filed local-shell result is a different object: the 4,600-by-4,600 cut inside one reference neighborhood has rank 4,600, a perfect matching. That local theorem and its association-scheme calculations are not contradicted by this global 98,280-pair matrix result.
- The documented 8,192 principal-submatrix gate (rank 8,170, nullity 22) is unaffected by the final partial-word mask because it ends on a 64-bit boundary. It is a useful regression test but cannot detect the final-word defect.

### What must remain separate

- The global 98,280-pair antipodal matrix is not the preregistered 120-pair / 240-vertex sampled induced-graph schedule. Treat this full-shell computation as a separately reported extension, not retroactively as a completed preregistered sample.
- It is not the 4,600-neighbor local association scheme, not the E8/Gosset 240-vertex graph, and not evidence of a geometric embedding between them.
- It does not construct the Leech lattice VOA, the Z2 orbifold, the Griess product, Monster generators, or a moonshine representation. The separate Leech Z2-orbifold character audit and Leech-to-Monster bridge remain their own algebraic and representation-theoretic tracks.
- Graph-state cut rank is a GF(2) graph invariant. No physical entanglement, quantum hardware advantage, or physical dynamics is established.

## Implementation defects and proposed repair

The PR fixes two defects in `leech_b_rank.py`:

1. Use an explicit byte-to-bit mapping for big-bit-order packed bytes stored as little-endian 64-bit words. For r = column mod 64, the bit index is 8*(r//8) + 7 - (r mod 8).
2. Store both `rank` and `next_col` in a versioned checkpoint. The old rank-only checkpoint is rejected because rank is not a valid column cursor when a column has no pivot.

The new tests cover all 64 positions in a complete word, all 40 real positions in the final partial word, checkpoint cursor independence, and rejection of legacy checkpoints.

**Checkpoint durability caveat:** the work matrix is still updated in place. The PR flushes matrix pages before publishing each checkpoint, but it does not yet provide a transactional write-ahead journal for a crash in the interval between matrix flush and checkpoint replacement. Do not describe arbitrary power-loss recovery as fully crash-safe. Preserve a pristine matrix; a legacy-mutated matrix must be regenerated before a corrected run. A transactional journal or immutable-source replay is follow-up work.

## Reproduction and acceptance still required

- Run the PR tests and full repository CI.
- Regenerate B_padded.bin from the corrected code; do not reuse a matrix already mutated by legacy elimination.
- Rerun corrected full elimination from a pristine matrix; 98,256 is the predicted rank, not yet a completed corrected-run result.
- Have Cosmo or another independent bench reconstruct the matrix and reproduce the 24-dimensional kernel, ideally with a different GF(2) algorithm.
- Preserve the original 98,250 output as a historical restricted-matrix result, not as the full rank.

No repository CI result, corrected full-elimination result, or second-bench reproduction is claimed by this report.
