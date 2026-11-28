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

## Running it in plain language (added 2026-11-26, at Lucas's request)

There is only **one** script file: `leech_b_rank.py`. There are no other
pilot files to find, install, or open.

The words `gen`, `build`, `probe`, `subrank`, `eliminate` are **stage
words**. They are not files, buttons, or menu items. You type one stage
word at the end of the command, after the script's file path, and the
script runs that one stage. Running the script with **no** stage word
runs `gen`, `build`, and `probe` in order, then stops.

Run the stages **in this order, one at a time**:

1. `gen` — builds the list of Leech vectors. Seconds.
2. `build` — builds the matrix file `B_padded.bin` (~1.2 GB, next to the
   script). A few minutes. If the files already exist, both of these
   print `cached` and skip — that is normal, not an error.
3. `probe` — a sanity check. **You should see:**
   `KERNEL HIT coord0==+4 (weight 46)` and `1 hits, 1 independent`.
4. `subrank` — a rehearsal on a small corner of the matrix.
   **You should see:** `{'submatrix': 8192, 'rank': 8170, 'nullity': 22}`.
   **Gate: if the rank is anything other than 8170, STOP.** Do not run
   the next stage — a different number means the matrix on your machine
   is not the same matrix, and the long run would be wasted.
5. `eliminate` — the full computation. It prints one line every 512
   pivots (e.g. `eliminate: rank 512 (col 513)`) and saves a checkpoint
   file, `elim_ckpt.npz`, at the same moments. Silence between lines is
   normal; it is working. When it finishes, it writes `rank_result.json`
   next to the script — that file is the result.

**Stopping and resuming is safe.** If the window is closed, the machine
reboots, or power is lost, run the same `eliminate` command again: it
reads the checkpoint and resumes where it left off. Nothing already
printed is lost.

**One rule:** once `eliminate` has started, do not re-run `probe` or
`subrank`. `eliminate` is the last stage, and it changes the matrix file
as it works; the earlier stages must stay as they were run, in order.

**Windows / PowerShell notes** (learned live, 2026-11-26):

- The command must start with the `&` symbol, then the Python path in
  quotes, then the script path in quotes, then the stage word with no
  quotes, like this:

  ```
  & 'C:\Python314\python.exe' 'c:/path/to/leech_b_rank.py' subrank
  ```

- If you see a `>>` prompt, PowerShell is waiting for a quote you left
  open. Press **Ctrl+C** to cancel and start the line over.
- Dropping the `&` gives an "Unexpected token" error — the paths alone
  are not a command.

**Observed pace** (one data point, not a promise): on a Ryzen 5600X
(48 GB RAM), 2026-11-26, the first `eliminate` checkpoint printed after
~1 minute and the next seven blocks arrived every ~2 minutes 12 seconds
per 512 pivots, steady. Later blocks slow down as the matrix fills in;
plan on an overnight-class run.


## Global rank audit correction (2026-11-27)

The first reported full-run value `rank=98250` was not the full 98,280-by-98,280 rank. A packed-bit endian mismatch caused the final partial 64-bit word to test 24 padding positions and omit 24 real columns (indices 98,240–98,263). Because the matrix is symmetric, the legacy elimination measured the rank of the corresponding 98,256-row restriction.

An independent reconstruction and kernel/coupling analysis gives full-matrix rank **98,256** and nullity **24**. See [the detailed audit](../../research/LEECH_EQBIT_GLOBAL_RANK_AUDIT_2026-11-27.md). The 8,192-by-8,192 subrank gate (8,170 / 22) does not detect this final-word issue because it ends on a 64-bit boundary.

The corrected implementation uses an explicit packed-byte mask and a versioned checkpoint containing both `rank` and `next_col`. A pristine matrix must be regenerated before rerunning; do not reuse a matrix mutated by the legacy elimination. CI and a second independent bench reproduction remain pending.
