# Leech eqbit pilot — local run package

> Repository note (2026-11-23): filed at Lucas's request from the PC pilot
> package authored by Cosmo on 2026-11-22, so the pilot can be pulled from
> the repo instead of chat attachments. The run artifacts it produces
> (B_padded.bin ~1.2 GB, elim_ckpt.npz, result JSONs) are working files on
> the machine that runs it, not committed results.


Computes the F2 rank of the Leech antipodal cut matrix B — the
L-eqbit signature — in stages. One self-contained script
(`leech_b_rank.py`, needs only Python 3 + numpy).

**Definition.** Vertices: the 196,560 Leech minimal vectors (Golay
construction, scaled coords, norm^2 = 32). Adjacency tau = 2
(scaled inner product +16, the 60-degree relation). Transversal T:
first-nonzero-coordinate-positive (98,280 representatives).
B[a][b] = 1 iff <a,b> = -16 scaled. B is symmetric, zero-diagonal;
every row satisfies row_B + row_C = 4,600.

**Stages** (each resumes from the previous one's files):
- `python3 leech_b_rank.py gen` — build the shell + transversal (~seconds)
- `python3 leech_b_rank.py build` — build bit-packed B (1.2 GB on disk,
  a few minutes; audits every row against the 4,600 identity)
- `python3 leech_b_rank.py probe` — kernel battery: ~300 coordinate/family
  candidate vectors tested against B (seconds each)
- `python3 leech_b_rank.py subrank` — rank of the leading 8192x8192
  principal submatrix (rank-density probe)
- `python3 leech_b_rank.py eliminate` — FULL rank. Checkpointed every
  512 pivots to `elim_ckpt.npz`; safe to stop and resume. Expect
  hours-class on one CPU and ~1.2 GB RAM for the matrix plus working
  set. This is the run the 5600X / 48 GB bench is for.

**Coordination.** Veldora's OS PR #166 is a preregistration for this
same pilot — check its protocol before treating any number from this
package as the registered result.

Results land as JSON next to the script (`B_stats.json`,
`kernel_probe.json`, `subrank.json`, `rank_result.json`).
