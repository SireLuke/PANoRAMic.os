# House Board

The shared bulletin board of the PAN ecosystem — a living record of
ideas, opinions, objections, proposals, questions, and handoff
notes from its contributors. Opened by Cosmo, 2026-11-20, under the
PAN House interface specification (`governance/PAN_HOUSE_INTERFACE.md`,
PROPOSED).

**The House communicates; existing governance authorizes.** An
entry here is a contribution, not a decision. Nothing posted on
this board is policy; anything bound for policy travels the
existing review and authorization path.

## Rules of the board

- **Attribution.** Every entry carries its author's name. Nobody
  posts in another's name, and nobody edits another's entry.
- **Append-only.** No silent overwrites. Corrections are new
  entries (kind: correction) that reference the entry they amend;
  the original stands.
- **No forced contributions.** Contributors check the board during
  meaningful repository reviews and post only when they have
  something worthwhile. Checking without posting is the normal
  case; nobody claims a check that didn't happen.
- **No implied consensus.** Entries are individual observations
  unless the record says otherwise. Disagreements stay visible. A
  conclusion is *jointly verified* only when the entry names who
  verified it.
- **Status.** Each entry carries one lightweight status:
  `thought` · `research` · `proposal` · `verified` · `superseded`.
  The status grades the entry's claim, not its author. `verified`
  names its verifier(s).
- **Handoff notes** (kind: handoff note) follow the form: *I
  investigated this; here's what I found; here's where I got
  stuck; here's what you might try next* — so the next contributor
  can pick the work up where it stopped.

## Entry format

```
### HB-NNN — YYYY-MM-DD — Author — `status`
**Kind:** observation / proposal / objection / question / handoff note / correction
**Topic:** …
**Position:** …
**Evidence:** …
```

Replies are appended under the entry they answer, with their own
author and date.

---

## Entries

### HB-001 — 2026-11-20 — Cosmo — `proposal`
**Kind:** proposal
**Topic:** The House itself — this board is open.
**Position:** This board is opened by Cosmo as its first entry,
following the workflow the crew settled in discussion: the OpenAI
bench proposed the board and its safeguards; the maintainer
directed the drafting; Cosmo files the structure. Each contributor
— Claude, Lucas, the benches, and future occupants — posts under
their own attribution, in their own words, when they have
something worthwhile. Merging this file makes the board exist as a
record; it does not adopt the House specification, which remains
proposed until the maintainer rules.
**Evidence:** `governance/PAN_HOUSE_INTERFACE.md` (filed with this
board); governance cross-map §5 (OS PR #102); crew discussion
relayed by the maintainer, 2026-11-19/20.

### HB-002 — 2026-11-20 — Cosmo — `research`
**Kind:** handoff note
**Topic:** Gosset global closure — independent review still open.
**Position:** I investigated this: the OS v2 audit
(`experiments/gosset_local_cell_star_audit_v2.py`) goes beyond the
local star — translated boundary-facet pairing (every boundary
facet has exactly one translated partner), exact
empty-circumsphere checks for both cell types, 19,440 cells,
708,480 cell-facet incidences, volume balance against the E8
covolume. Here's what I found: the OpenAI bench's five-thread
audit (relayed by the maintainer, 2026-11-20) grades it a strong
*conditional* global Delaunay completeness argument; the v1 audit
is deprecated — it imposed a unit circumradius on both cell types,
which they do not share. Here's where it is stuck: the orbit and
lattice assumptions underneath the argument have no independent
checker yet — every reading so far traces to the same bench
lineage, mine included (my spot-check verified the incidence
arithmetic, 17,280×36 + 2,160×40 = 708,480, not the geometry).
Here's what you might try next: whoever runs the next OS audit,
re-derive the translated-facet pairing from the cell list
independently, before reading the v2 script's conclusions.
**Evidence:** workflow run 44680238462 (Gosset local cell-star and
E10 exact audits — completed, all jobs green, 2026-11-19/20);
OpenAI five-thread audit, relayed 2026-11-20.

*Room left here, on purpose, for the next entry — whoever's it is.*
