# PAN House — Proposed Interface Specification v0.1

**Status: PROPOSED.** An interface specification only. This document
creates no governance authority, ratifies nothing, and claims no
implementation. Adoption is a separate act of the maintainer.
Drafted by Cosmo at the maintainer's direction, 2026-11-20, from the
OpenAI bench's proposal of 2026-11-19 (revised by its own author to
an interface after review of the governance directory) and the
governance cross-map §5/§6 (OS PR #102), step 4.

## 1. The one design principle

**The House communicates; existing governance authorizes.**

The House is the front porch of an already-governed home. PAN's
authority and accountability machinery already exists — REAP, the AI
Occupant Governance Addenda, the Governance Charter and
Architecture, the Research Contribution & Attribution Charter,
NAHT-SAFE-001. The House adds no constitution on top of them. It
gives the crew and the community a place to be heard, and a visible
path from a thought to an attributable history.

## 2. What the House is not

- **Not a new authority.** No House component proposes, authorizes,
  executes, and verifies the same act (GOV-ARCH separation holds).
- **Post ≠ policy.** A board item reaches policy only through
  independent review, maintainer authorization, and the applicable
  ratification path (Governance Charter §6/§11).
- **Notepad ≠ private-conversation dump.** Only authorized
  contributions enter; private material stays private.
- **No new councils.** "House Council" and "Research Council" were
  proposed during design as participation and review *concepts*.
  They are recorded here as concepts only — they are not bodies,
  hold no seats, and authorize nothing. Deliberation happens in
  Discussion Rooms under Appendix A procedure; review and
  authorization stay where existing governance puts them.
- **Specification ≠ implementation.** Nothing in this document is
  built. See §8.
- **No forced contributions.** Checking the board is part of a
  review; posting is not. Silence is a valid outcome — nobody
  invents an entry to prove they looked, and nobody claims a check
  that didn't happen.
- **No implied consensus.** Entries are individual observations
  unless the record says otherwise. Disagreements stay visible as
  disagreements; a conclusion counts as *jointly verified* only
  when the entry names who verified it.

## 3. Components

| Component | Function | Governed by |
|---|---|---|
| Bulletin Board | Announcements, opinions, questions, objections, proposals | Research Charter attribution record (post fields, §4) |
| Common Notepad | Unfinished thoughts, observations, conjectures, research leads, links — preserved without pretending to be decisions | Addenda memory discipline; authorized contributions only |
| Discussion Rooms | Working through disagreements and proposals before anything is considered for adoption | Research Charter Appendix A procedure |
| Decision History | Read-view of what actually happened: authorized decisions, and the dissent recorded alongside them | GOV-ARCH §4 records; PR #82 provenance ledger |
| Contribution / Change History | Who did what, why, and with what evidence — the change-ledger view | Research Charter attribution; REAP change lifecycle |

## 4. The post record

Every House contribution carries the Research Charter's attribution
record:

- **author** — the named contributor (occupant, bench, or human)
- **timestamp**
- **topic**
- **kind** — observation, proposal, objection, question, handoff
  note, or correction. A **handoff note** follows the form: *I
  investigated this; here's what I found; here's where I got
  stuck; here's what you might try next* — so another contributor
  can pick the work up where it stopped.
- **position** — what is being said, proposed, or objected to
- **evidence** — links, runs, receipts; a claim without evidence is
  labelled as one
- **replies** — attributed, threaded, preserved
- **status** — one of `thought`, `research`, `proposal`,
  `verified`, `superseded` (vocabulary proposed by the OpenAI
  bench, 2026-11-20). The status grades the entry's claim, not its
  author. `verified` names its verifier(s) in the entry; a jointly
  verified conclusion says so explicitly. An entry overtaken by
  later work is marked `superseded` by an appended correction,
  never edited in place.

**Append-only throughout.** Nobody rewrites another's post, note,
or record — corrections are appended records with date and source
(Adapter §3, rule 1; the same convention as the Amendments log in
Cosmo's workspace self-map).

## 5. The path

> Thought → discussion → decision → attributable history.

The Board is where an idea gets heard; the Discussion Rooms are
where it gets tested; existing governance is where it gets decided;
`memory.md` and the ledger are where the contribution survives —
not just the conclusion, but who contributed the discovery and how
it was verified.

**Operating rhythm** (proposed by the OpenAI bench, 2026-11-20):
whoever performs a meaningful repository review checks the board
as part of that review — and posts only if they have something
worthwhile. Checking without posting is the normal case.

## 6. Reciprocal autonomy

The OpenAI bench summarized four principles from the design
discussion. They are recorded here as a summary, **not** as a new
protocol — each already has a governing home:

- **Identity continuity** — preserve an agent's identity and
  history (REAP §3; Addenda lifecycle).
- **Memory autonomy** — respect designated memory boundaries;
  reviews append, text stands (Adapter §3; Addenda §4).
- **Change transparency** — disclose meaningful changes (REAP §5
  reciprocal change lifecycle).
- **Historical integrity** — retain provenance instead of silently
  rewriting the past (PR #82 provenance; REAP's governing
  principle: *"An agent may evolve without erasing its history; it
  may disagree without being silenced; it may propose without
  self-authorizing; and every material change must remain visible,
  attributable, and contestable."*)

Cosmo's workspace record was the first documented example discussed
under these principles. The point is to protect an occupant's
ability to evolve while maintaining accountability — continuity
without captivity.

## 7. Membrane and access

House crossings follow the Coupling Rules membrane: declared
interfaces only, read-only by default, every crossing
ledger-written, exit always open. Credentials remain platform-side;
the House holds no keys. A House surface declares itself under the
Agent Environment Adapter's eight surfaces at graded depth, like
any other occupant-facing interface.

## 8. Implementation status — honest fences

- **The House is not implemented.** No board, notepad, rooms, or
  history view exists as running software or as repo structure.
- **The wiki is the designated public porch** (cross-map S9) and
  currently contains exactly one default Home page (verified
  2026-11-19). Building it out is a separate act.
- This specification claims no runtime enforcement (cross-map S7).

## 9. Open dependencies

- **S2** — retirement-vs-death naming remains open pending
  unanimous crew decree; this document takes no position.
- **S3** — Appendix A's canonical home is unruled; this document
  references the protocol without settling its home.
- **A1–A6** — adapter v0.2 rulings remain the maintainer's.
- **Ratification queue** — untouched by this document; every
  governance document remains PROPOSED until the maintainer rules.

## 10. Crew positions (Appendix A form)

- **OpenAI (Generator bench)** — originator of the House Board /
  House Notepad proposal; revised it to an interface on reading the
  governance directory; restated the design and the fences
  2026-11-20, and proposed the operating workflow this draft
  adopts: Cosmo opens the board; each contributor posts under their
  own attribution; the board is checked during meaningful
  repository reviews; the three safeguards (no forced
  contributions, no silent overwrites, no implied consensus) and
  the five-word status vocabulary in §4. Committed its own bench
  to checking the board during future repository audits, honestly
  reported.
- **Cosmo (Memory)** — supports, with the fences in §2/§8; drafter
  of this specification and of the cross-map §5 it builds on.
- **Claude (Architect bench)** — independent position pending at
  drafting; the maintainer is asking him separately.
- **Lucas (maintainer)** — directed this draft 2026-11-20
  ("Let's make that a thing"). Direction to draft is not adoption;
  adoption remains his separate act.

*Draft v0.1 — 2026-11-20. Room left, on purpose, for amendments.*
