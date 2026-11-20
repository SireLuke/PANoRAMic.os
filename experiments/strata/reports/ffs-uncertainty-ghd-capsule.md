# FFS Uncertainty & Theory-Comparison Capsule (STRATA-003 follow-on)

**Status:** AUTHORISED as the FFS fork packet by Lucas, 2026-11-20 14:45 CST.
Filed to PANoRAMic.os as PR #105 on 2026-11-20 (branch `strata/ffs-capsule`;
this capsule + the Stage 0 inventory at `experiments/strata/reports/`),
at Lucas's direction ("fork that to repo"). Merge is the maintainer's
call. No code written, no STRATA re-grade. Prepared 2026-11-20 from the OpenAI five-thread
audit relayed by Lucas that morning (2026-11-20 10:18 CST) and Cosmo's
in-chat grading of it. Decision 2 decided 2026-11-20 (SEM first, Stage 1
in parallel); decision 3 stands as the proposed default; decision 4 was
answered by the direct license check. Stage 0 done; Stage 1 interim
returned — see `ffs-stage0-inventory.md`.

## Why this capsule exists

The Gosset thread's last computational condition is now satisfied: OS
workflow run 44680238462 ("Gosset local cell-star and E10 exact audits #229")
completed 23:46 CST 2026-11-19 — all 5 jobs green, cell-star 27m 17s. What
remains on Gosset is human: independent review of the Delaunay proof's
assumptions. OpenAI's own priority, stated in the same audit, is therefore
the live one: **Gosset proof scrutiny + FFS uncertainty/GHD forward.** This
capsule is the forkable packet for the second half — the FFS half — so that
when Lucas picks the lane, the benches start from a preregistered scope
instead of re-deriving it.

## What the audit established (verbatim numbers, from the 2026-11-20 audit)

Figure 3B, measured correlation diagnostics (Zeng experimental CSVs, fetched
and checksum-verified by the current main-branch workflow):

| Quantity | L2 fractional sea | L4 fractional sea |
| --- | --- | --- |
| First zero crossing | 1.2624 μm | 0.9931 μm |
| First trough location | 1.5983 μm | 1.1624 μm |
| Trough correlation | −0.03201 | −0.02656 |
| Effective homogeneous-sinc kF diagnostic | 1.2443 μm⁻¹ | 0.7909 μm⁻¹ |

L0 control: 431 measured points; late sign changes occur near the noise
floor and are **not** counted as FFS oscillations.

Two readings, kept separate:

1. **Descriptive reproduction — genuine.** The trough locations land around
   the published ~1.6 μm and ~1.2 μm features.
2. **Physical estimate — not licensed.** The two effective-kF diagnostics
   (1.2443 vs 0.7909 μm⁻¹) disagree too much for either to be read as a
   trap-corrected physical estimate. The audit's warning, endorsed in
   Cosmo's grading: do not interpret either as one.

STRATA-003 stays **INCONCLUSIVE** — correctly. Provenance and one-domain
checks pass; cross-domain and uncertainty tests have not been performed.

## The concrete gap (the capsule's whole job)

The Figure 3B CSVs already contain the missing ingredients; the current
script retains them but does not use them:

- **Experimental error columns** — present, not propagated.
- **GHD simulation mean/min/max columns** — present, not compared against.
- **Figure 3C** — checksum-verified only, not analysed.

Nothing needs to be invented or synthesised. The work is to use what is
already on disk.

## New source the audit surfaced

The companion **theoretical-data record (Zenodo 18702729)** contains
Mathematica figure material and raw one-particle-correlation data — more than
the three Figure 3 CSVs the audit currently uses (it also holds Figure 4A/4B
and a lifetime-point dataset in the experimental record). That raw data is
the route to investigating whether **run-level resampling** is possible. If
it is not, the fallback is **pointwise SEM perturbations only as a
sensitivity analysis**, with the independence assumption stated explicitly —
never presented as a measured uncertainty.

## License gate — verified for 18702729, still open for 18697242

- Companion theory record **18702729**: **VERIFIED 2026-11-20 10:35–10:36 CST
  by direct read of the Zenodo record page** — license stated verbatim as
  "Creative Commons Attribution 4.0 International". This confirms the
  2026-11-20 audit's NLM-based claim and supersedes the 2026-11-19 STRATA
  review's description of the supplementary record as blank-license /
  unregistered. Record: "Exotic critical states as fractional Fermi seas in
  the one-dimensional Bose gas", dataset v1, published 2026-02-19,
  DOI 10.5281/zenodo.18702729, Open access. Single file: Zenodo.zip,
  175.0 MB, md5 dd22fdd862d4cd8de5fe173761eef60f. Contents confirmed
  (sizes below are UNCOMPRESSED sizes from the zip central directory;
  compressed sizes differ — e.g. Make_fig_2_3.nb is 16,203,192 B
  compressed, 27,210,413 B uncompressed; READ_ME.txt is 452 B
  compressed, 851 B uncompressed — verified 2026-11-20, so a
  compressed-size reading is not a discrepancy):
  Mathematica figure notebooks (Make_fig_2_3.nb 27.2 MB, Make_fig4.nb,
  Conv_MC.nb, Fig_SM_N.nb, Read.nb) and raw one-particle-correlation data
  (Raw_data/30F_S_all_data.mat 18.0 MB, 30F_S_c_hol.mat, Read.nb).
  Two small trip hazards for Stage 1: the description points to
  "README.txt" in Raw_data_g1, but the preview shows only READ_ME.txt
  (851 B) there; and the paper citation in the description names Z. Wang
  and X. Yu, who do not appear in the record's Authors/Creators list.
  No link to record 18697242 appears on this record's page.
- Experimental record **18697242**: both bench reports said no declared
  license. **CORRECTED 2026-11-20 by direct check:** Zenodo API metadata
  for the record states license **cc-by-4.0** ("Realization of fractional
  Fermi seas"; files served individually, including figure3B_data.csv and
  figure3C_data.csv).
- **Gate as it now stands (revised 2026-11-20):** BOTH records are
  CC BY 4.0 per Zenodo's own metadata, checked directly — usable with
  attribution. The earlier split gate (theory usable, experimental
  local-only) is superseded. The two records remain distinct sources and
  must never be conflated; only the license treatment changed. Full
  record, including the preserved Zenodo API metadata excerpt and the
  source-published file checksums (which match the downloaded files):
  `ffs-stage0-inventory.md`.

## Stages (report-first; this packet filed as PR #105 at Lucas's direction)

- **Stage 0 — Inventory. DONE 2026-11-20 (Cosmo).** Error columns and sim
  mean/min/max columns confirmed present in figure3B/3C CSVs; hashes
  recorded; 431 measured points per curve reconciled against the audit.
  See `ffs-stage0-inventory.md`.
- **Stage 1 — Resampling feasibility.** Inspect the companion record's raw
  one-particle-correlation data: does it support run-level resampling?
  Yes → design the resampling; No → record why, and proceed to Stage 2.
  **Interim signal 2026-11-20:** the theory zip's central directory (158
  entries, listed by range request, archive not downloaded) shows five
  `*_all_data.mat` experimental aggregates — resampling looks plausible;
  confirmation requires opening one .mat file.
- **Stage 2 — Uncertainty sensitivity.** Pointwise SEM perturbations of the
  Figure 3B curves; report how the zero crossings, trough locations and
  effective-kF diagnostics move. Labelled sensitivity, not measurement.
  Note (per the paper, relayed in OpenAI's PR #105 review, 2026-11-20;
  Cosmo has not yet read the paper text directly): the Figure 3
  experimental data average ten repetitions and the published error bars
  are the standard error of the mean. That supports this stage's design —
  and it does NOT make pointwise perturbation equivalent to resampling
  entire experimental runs. The two methods stay separate, as staged.
- **Stage 3 — Theory comparison, three-way and separate.** Measured curves
  vs supplied GHD curves vs the homogeneous-sinc reference — compared
  separately, never blended into one fitted number.
- **Stage 4 — Figure 3C.** Analyse (not just checksum) the Figure 3C data
  and record what it does and does not add.
- **Stage 5 — Re-grade (only if earned).** Revisit STRATA-003's dimensions
  only where Stages 1–4 actually move them. INCONCLUSIVE stands until
  cross-domain and uncertainty dimensions are genuinely tested — a better
  error bar alone does not promote it.

## Fences (carried from the audit and the STRATA rules)

- No physical kF claim from either diagnostic; the divergence *is* the
  finding until a trap-corrected analysis exists.
- No data redistribution in PR #105 (docs only; no data files committed).
  Both Zenodo records are CC BY 4.0 (direct check, 2026-11-20; evidence
  excerpt preserved in `ffs-stage0-inventory.md`); any future reuse of
  their data must preserve CC BY 4.0 attribution and license information.
- No STRATA promotion without held-out evaluation and a second domain.
- Further repo changes or legend amendments arising from this capsule
  need Lucas's per-turn go-ahead. (The capsule itself was filed as
  PANoRAMic.os PR #105 at Lucas's direction on 2026-11-20.)
- Visual resemblance alone never qualifies; failures retained (STRATA v0.1).

## Suggested casting (proposal only — Lucas's call)

- **OpenAI (Generator):** Stages 1–3 — the GHD/theory comparison is its
  thread; it found the companion record.
- **Claude (Architect):** independent rerun / check of Stages 2–3 when the
  first pass lands — nobody verifying their own work.
- **Cosmo:** verification of the Stage 0 inventory and the license gate,
  and the STRATA-003 re-grade in Stage 5.

## Open decisions for Lucas

1. ~~Authorise this capsule as the FFS fork packet, or hold it with the
   placement capsule's five questions?~~ **DECIDED 2026-11-20: authorised
   as the fork packet (Lucas, in-chat tap + confirmation).**
2. ~~If forked: run-level resampling first (Stage 1), or straight to SEM
   sensitivity (Stage 2) while Stage 1 is investigated in parallel?~~
   **DECIDED 2026-11-20: SEM sensitivity first, Stage 1 feasibility
   checked in parallel (Lucas, in-chat tap).** Stage 0 completed and the
   Stage 1 interim signal returned the same day.
3. Home for the work when it lands: PANoRAMic.os `experiments/strata/`
   (where STRATA-003/004 live), or elsewhere? **Standing default
   2026-11-20: OS `experiments/strata/`, as proposed; Lucas raised no
   objection. Nothing files there until he says so.**
4. ~~License gate: is a direct Zenodo-page check enough to clear it, or
   does he want the NLM listing checked too?~~ **ANSWERED BY EVIDENCE
   2026-11-20:** the direct check was performed (Zenodo API metadata) and
   cleared MORE than expected — both records are CC BY 4.0. See the
   license section above and `ffs-stage0-inventory.md`.

## Sources

- OpenAI five-thread audit, relayed by Lucas 2026-11-20 10:18 CST (in-chat;
  message `5a81e087-6f23-474a-a75b-954fa0ecb224`): FFS diagnostics, GHD/error
  columns unused, companion record 18702729, license seam, STRATA-003
  INCONCLUSIVE.
- Cosmo's grading of the same audit, 2026-11-20 10:19 CST (in-chat;
  message `assistant-msg-025b9a93-1cc7-4bc5-bd7f-9c79d0e891e5`).
- OpenAI weekly STRATA validation review, relayed 2026-11-19 21:08
  (memory/2026-11-19.md): empirical layer INCONCLUSIVE; supplementary
  record 18702729 then described as unregistered / blank-license — the
  source of the license conflict flagged above.
- Gosset run closure: run 44680238462 completed 23:46 CST 2026-11-19, all 5
  jobs green (verified 2026-11-20 10:25 CST via API + Lucas's screenshot;
  memory/2026-11-20.md).
