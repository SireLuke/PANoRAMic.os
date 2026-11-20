# FFS Stage 0 Inventory + Stage 1 Feasibility (interim)

**Status:** Stage 0 COMPLETE; Stage 1 interim signal returned. Workspace
only; nothing filed to a repo. Performed by Cosmo 2026-11-20, after Lucas
authorised the FFS capsule as the fork packet (14:45 CST) and chose the
sequencing "SEM sensitivity first, Stage 1 feasibility checked in parallel"
(15:23 CST). Parent document: `ffs-uncertainty-ghd-capsule.md`.
STRATA-003 remains **INCONCLUSIVE**; nothing here re-grades it.

## License gate — CORRECTED by direct check

Both Zenodo records were read through Zenodo's own API metadata on
2026-11-20 (~15:24 CST):

- Theory record **18702729** ("Exotic critical states as fractional Fermi
  seas in the one-dimensional Bose gas"): license **cc-by-4.0**.
- Experimental record **18697242** ("Realization of fractional Fermi
  seas"): license **cc-by-4.0**.

The capsule's earlier gate — experimental record treated as unlicensed
because both bench reports said it declared none, its own page not yet
checked — is **superseded**. The owed check has now been done, and it
clears both records for use with attribution. The two records remain
distinct sources and are still never to be conflated; only the license
treatment changes.

## Stage 0 — Inventory (experimental record 18697242)

Files are served individually (no archive). Downloaded 2026-11-20 to the
review goal's `hidden_files/ffs-data/`:

| File | Bytes (API-listed = on-disk) | MD5 (on-disk) |
| --- | --- | --- |
| figure3B_data.csv | 400,292 | 2319b4d9cf9114466addc103525cd92d |
| figure3C_data.csv | 399,461 | b98af0284338f88a4fb39e8ea82972b4 |

Also listed on the record (not downloaded): figure3A_data.csv (164,234 B),
lifetime_point_C_data.csv (481 B), figure4A_data.csv (195 B),
figure4B_data.csv (7,590 B).

**Schema — identical for 3B and 3C, 21 columns.** For each of L0, L2, L4:
`exp_x`, `exp_y`, `exp_err` (measured correlation + its error column), and
`sim_x`, `sim_mean`, `sim_min`, `sim_max` (the supplied theory/GHD band).
The capsule's premise is confirmed against the data itself: the error
columns and the sim mean/min/max columns are present and were unused by
the audit's diagnostics.

**Counts.** 1,203 data rows per file. Each experimental curve carries
exactly **431 measured points** (x from 0 to 62.478), the remaining rows
empty in the exp columns (file padded to the sim grid length) — the
audit's "L0: 431 points" reconciles, and holds for L2 and L4 as well.
`exp_err` is nonzero at 430 of 431 points (zero at x = 0, the
normalisation point where y = 1). The sim grid is 1,203 points spanning
−30..30 — a different grid and range from the experimental axis, so
grid alignment/interpolation is a Stage 3 concern, to be declared there,
not silently absorbed.

**Figure 3C** carries the same schema and counts; its analysis is Stage 4,
not done here.

## Stage 1 — Feasibility, interim signal

Method: the theory record's 175 MB Zenodo.zip was **not** downloaded. Its
zip central directory (158 entries) was fetched by HTTP range requests
and listed — filenames only, no data files opened.

Findings: alongside the Mathematica figure notebooks (Make_fig_2_3.nb,
Make_fig4.nb, Read.nb), the archive holds per-configuration experimental
aggregates in `Figures_generation/Fig_2_3_S4_S5/Data_exp/` — five
`*_all_data.mat` files (30F, 30F_S, 30, 50, Final; ~15–22 MB each) plus
parameter files — and a `Raw_data_g1/Raw_data/30F_S_all_data.mat`. The
archive therefore contains substantially more than the published 431-point
mean curves.

**Interim verdict: run-level resampling looks plausible, NOT confirmed.**
Feasibility turns on the internal structure of the `*_all_data.mat` files
(whether they hold per-run/per-shot values or only finer aggregates).
Confirming requires opening one .mat file — that is the first task of
Stage 1 proper. If the .mat files hold only aggregates, Stage 1 records
"No" and the programme proceeds on Stage 2 (SEM sensitivity) alone, as
preregistered.

## What remains

- Stage 1 confirmation: open one `*_all_data.mat`, record its variables.
- Stage 2 (SEM sensitivity): OpenAI's seat per the capsule's casting;
  inputs are in hand (figure3B_data.csv + this inventory).
- Stage 3: three-way comparison, grids declared. Stage 4: Figure 3C.
- Stage 5 re-grade only if earned. INCONCLUSIVE stands.
