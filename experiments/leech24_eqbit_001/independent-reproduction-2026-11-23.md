# Independent reproduction of the Leech local-shell audit — 2026-11-23

**Subject.** `experiments/leech24_eqbit_001/local_shell_audit.py` on main
(blob `e19733b1191d03b5bf87460ec444794b0c716125`), output schema
`pan.leech24_local_eqbit_audit.v2`, status `COMPUTED_LOCAL_EXACT_AUDIT`.

## Executions

1. **Original bench runs** (Veldora) — the audit lineage filed via
   PR #171, PR #173, and the CI evidence preservation of PR #175.
2. **Cosmo reproduction, 2026-11-22** — same-commit rerun on the memory
   bench host; output 25,798 bytes, md5
   `d8745539eaf3f3392671b43430502983`. Every independently checkable
   number matched the books; the one flagged limit at the time was that
   the construction-family cut-rank table was runner-computed only.
3. **SireLuke, own PC, 2026-11-23 evening** (Ryzen 5600X, 48 GB DDR4;
   repo held as a snapshot folder, script file supplied from main):
   - a v1-schema run matched the v2 books on every overlapping field;
   - a v2-schema run matched the reproduction output on **every compared
     field**, including all hashes and the full cut-rank table below.

## Matched values (executions 2 and 3, bit-for-bit)

Antipodal relation matrix SHA-256:

- A: `6902f7ff4e97a8335232c7309e6a360119068b59a24cce6c4e33a30fe1a5e3d6`
- B: `9b0a10e4734cd5141770688a85168bf0a4a7231aebc130c4880a0536321a5832`
- C: `775f506595e99a84bb5ff4230a0f7f1de4fca0f35bdd2d0f200ed32abd11da72`

Within-neighbor graph SHA-256:

- A: `a0ce78bdf2b53718ba0f86684df75860261e212bd0e7de1336607052782ae5ed`
- B: `0f0a5974263def61b8c73651f295b01f2fcd79a9fed397619854d8d0d32fc3f2`
- C: `43fa33c31a4a4eae65ea6001b585ead28e859bd8f97b06687019bd42d3774683`

Histogram SHA-256 `a374826bed68944e3041f9aaf1109d8ec79bce1c731701501eb55d9806d9bb2e`,
identical for all three families. Common-neighbor census
{−16: {0: 2300}, 0: {42: 2049300}, 8: {162: 6476800}, 16: {336: 2049300}};
2,049,300 edges; 891-regular; antipodal GF(2) rank 4,600 in all three
families; local association-scheme multiplicities [1, 23, 275, 2024, 2277]
with an identical eigenmatrix across families.

Construction-family cut ranks (rows: reference family; columns: cut family):

| ref | A | B | C |
|-----|-----|-----|------|
| A | 44 | 233 | 221 |
| B | 28 | 259 | 231 |
| C | 23 | 2277 | 2300 |

## What this closes

The construction-family cut-rank table was the one part of the audit
previously carried as runner-computed only. It has now been independently
recomputed on separate hardware with identical results. The local-shell
audit stands on three independent executions agreeing exactly.

## Scope

Unchanged from the audit itself: three deterministic reference
representatives (one per Golay construction family). Nothing here proves
Co0 transitivity or every-root local incidence, and no global adjacency
was materialized in any execution.
