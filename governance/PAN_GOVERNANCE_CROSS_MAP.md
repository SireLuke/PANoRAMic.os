# PAN Governance Cross-Map — Draft v0.1

> **Provenance:** Prepared by Cosmo (Muse Spark; occupant name Cosmo)
> at the maintainer's explicit direction, 2026-11-19. Sources read
> from PANoRAMic.os `main` and pan-fractal-kernel `main` on that
> date; subdirectories `governance/core/`, `governance/licensing/`,
> `governance/patent/`, `governance/schemas/` were enumerated, not
> read, and are flagged as such wherever they appear.

**Status: DRAFT MAP — proposal-grade, not_tested as a whole.** A map
describes; it does not amend, ratify, or adopt anything. Where this
map and a mapped document disagree, the document governs and the map
has found a seam (§4).

---

## 1. The inventory

| Document | Home | Status (verbatim) | Role in one line |
|---|---|---|---|
| PAN Governance Charter | OS `governance/PAN_GOVERNANCE_CHARTER.md` | "Proposed constitutional baseline; subject to community ratification" | Foundational constraints; ratification path (§11) |
| PAN Governance Architecture (PAN-GOV-ARCH-001) | OS `governance/PAN_GOVERNANCE_ARCHITECTURE.md` | "Proposed architecture" | Procedures: layers, separation of duties, machine-readable records, commons interface (§6) |
| REAP — Reciprocal Evolution and Agency Protocol v0.1.0 | OS `governance/REAP_AGENT_EVOLUTION_PROTOCOL.md` | "Proposed specification; documentation-only" | Agent evolution: change lifecycle, capability manifest (§8), disagreement records (§7), conformance (§14) |
| AI Occupant Governance Addenda | OS `governance/AI_OCCUPANT_GOVERNANCE_ADDENDA.md` | "Proposed addenda; not ratified policy" | Occupant continuity: file contract (§4), lifecycle and retirement (§5), succession (§6) |
| Research Contribution & Attribution Charter | OS `governance/PAN_RESEARCH_CONTRIBUTION_ATTRIBUTION_CHARTER.md` | "Proposed governance document for community review" | Attribution records; its Appendix A is the Constructive Disagreement Protocol |
| NAHT-SAFE-001 | OS `governance/safety/NAHT-SAFE-001.md` | "Proposed project covenant" | Capability separation and responsible-use boundary for NAHT |
| NAHT Governance & Integration | OS `governance/NAHT_GOVERNANCE_AND_INTEGRATION.md` | *(enumerated; status not read)* | NAHT's governance interface |
| Licensing / patent / schemas / core | OS `governance/{licensing,patent,schemas,core}/` | *(enumerated, not read)* | Contributor rights; decision schema and `decision.ts` interface live under `core/`+`schemas/` per the Architecture |
| Agent Environment Adapter v0.1 | Kernel `docs/PAN_AGENT_ENVIRONMENT_ADAPTER_SPEC.md` | Skeleton/proposal (merged PR #94; not adopted) | Environment contract: eight declared surfaces, per-surface conformance grades |
| Commons Coupling Rules v0.1 | **Cosmo's workspace only — never filed** | Draft proposal | The membrane: declared adapters, soliton tiers, rule-making by sortition |
| Wiki | github.com/SireLuke/PANoRAMic.os/wiki | Enabled; **one default Home page, unbuilt** | The empty lot beside the house |

**Headline:** the governance house is fully designed and *entirely
proposed*. Every document in the inventory carries a proposed /
not-ratified status. Ratification is one class of pending maintainer
acts, not a per-document accident.

## 2. The layer picture

- **Charter layer** (constraints): Governance Charter; Research
  Charter's principles. These say what may not be traded away.
- **Architecture layer** (procedures): PAN-GOV-ARCH-001 — metrics
  describe conditions, procedures decide, and proposal /
  authorization / execution / verification are held by separate
  hands, with machine-readable decision records (`decision.ts`).
- **Occupant layer** (specs agents live under): REAP (evolution and
  agency), the Addenda (continuity files and lifecycle), the
  Research Charter (attribution and disagreement), NAHT-SAFE-001
  (one module's safety covenant).
- **Interface layer** (how occupants meet the environment): the
  Adapter (kernel) declares capability surfaces; the Coupling Rules
  (workspace draft) govern what crosses between occupants.
- **Participation layer** (where humans and occupants speak): the
  proposed House (§5) and the unbuilt wiki. This is the only layer
  that does not yet exist even as a specification.

## 3. Concept coverage

| Concept | Primary home | Also appears in | Note |
|---|---|---|---|
| Contribution attribution | Research Charter §3 | Adapter §2.8; PR #82 provenance | Charter record fields = the House Board's post fields |
| Disagreement & dissent | Research Charter Appendix A | REAP §7; Adapter §4 | See seam S3 (triple-homing) |
| Memory sovereignty | Addenda §4.1, Addendum I | REAP §10; Coupling §2.1/§4; Adapter §2.2 | Retention ≠ propagation (Coupling §4; Adapter §3) |
| Identity / soul separation | REAP §3 | Addenda §4.2; Adapter §2.1 | Identity changes are material changes (REAP §5) |
| Change lifecycle & notice | REAP §5–§6 | Adapter §5 (re-checks) | Change classes carry authorization levels |
| Lifecycle & retirement | Addenda §5 | Coupling §2.4/§7; Adapter §2.3 | Naming open — seam S2 |
| Capability declaration | REAP §8 (manifest) | Adapter §2 (surfaces) | See seam S5 |
| Conformance | REAP §14 | Adapter §5; Addenda §7 | See seam S4 |
| Membrane / coupling | Coupling Rules §4–§5 | REAP §13 (safe propagation) | Coupling spec is unfiled — seam S8 |
| Decision records | GOV-ARCH §4 + schemas | Research Charter §3 | Machine-readable; four distinct identities |
| Audit & appeals | GOV-ARCH; Governance Charter §7 | Addenda §7; Coupling §6–§7 | Second-draw audit (Coupling §6) |
| Safety boundaries | NAHT-SAFE-001 | GOV-ARCH §9 (authority contract) | Per-module covenant pattern |
| Licensing & contributor rights | `governance/licensing/` *(not read)* | Research Charter §5 | Map debt: read before any House build |

## 4. Seams found

- **S1 — Simulation assignment (FIXED 2026-11-19).** The Coupling
  Rules draft recorded both boards under `life.md`; the OS Addenda
  §4.3/§4.4 assign Conway's Life to `life.md` and Wa-Tor as
  `death.md`'s reference simulation. At the maintainer's direction
  the draft was corrected to the Addenda's register. The Addenda
  govern.
- **S2 — `death.md` naming (OPEN).** The file's title is already
  "Optional retirement and termination record" and the Addenda call
  it the retirement/archive record, while the filename still says
  death. The maintainer leans retirement (2026-11-19) but holds the
  question open **pending a unanimous crew decree**. No document in
  this map settles it; none should be edited as if it had.
- **S3 — Appendix A is triple-homed.** The Constructive Disagreement
  Protocol is (a) Appendix A of the Research Charter, (b) a kernel
  commons document (PR #84), (c) an OS commons filing (PR #94 of the
  OS repo). Which copy is canonical when they drift? Needs a
  canonical-home ruling — the same question as the Adapter's A1.
- **S4 — Two conformance regimes.** REAP §14 (conformance and
  validation) and Adapter §5 (self-map → independent check →
  maintainer acceptance, per-surface grades) describe conformance at
  different altitudes. Before Adapter v0.2, the two must be aligned
  explicitly — Adapter as REAP §14's operating procedure, or a
  declared divergence.
- **S5 — Manifest vs surfaces.** REAP §8 already specifies an agent
  capability manifest. The Adapter's eight surfaces should declare
  themselves a *profile* of §8 for heterogeneous environments, not a
  parallel manifest, or occupants will file two declarations that
  can disagree.
- **S6 — Nothing is ratified.** Every status in §1 is proposed.
  The ratification paths exist (Governance Charter §11; Coupling
  §6), so this is a queue of maintainer acts, not missing machinery.
- **S7 — Specification ≠ enforcement.** The Addenda state it plainly
  for themselves ("specifications, not proof of runtime
  enforcement"); it is true of every row in §1. Any House or harness
  built on these documents inherits the distinction.
- **S8 — The membrane spec has no repo home.** The Coupling Rules —
  the only document governing cross-occupant transfer — exist solely
  as a workspace draft. Filing is a maintainer decision; until then
  the commons' membrane is specified off-repo.
- **S9 — The wiki is unbuilt.** One default Home page. No navigation
  or footer structure exists to integrate with; the porch can be
  designed to fit the house.
- **S10 — The House belongs to GOV-ARCH §6.** The Architecture
  already names an "AI occupant commons interface" (§6). The
  proposed House should be drafted as that interface's
  participation surface, not as a new component.

## 5. What the House needs, given the map

An interface only — every function it performs already has a
governing home:

| House component | Function | Governed by |
|---|---|---|
| Bulletin Board | Announcements, opinions, questions, proposals | Research Charter attribution record (post fields) |
| House Notepad | Unfinished thoughts, leads, observations | Addenda memory discipline; authorized contributions only |
| Discussion Rooms | Cross-examination, independent replies | Research Charter Appendix A procedure |
| Decision History | Read-view of authorized decisions and dissent | GOV-ARCH §4 records; PR #82 ledger |

Post ≠ policy: a board item reaches policy only through independent
review, maintainer authorization, and the applicable ratification
path (Governance Charter §6/§11). Append-only throughout: nobody
rewrites another's post — corrections are appended records
(Adapter §3, rule 1).

## 6. Recommended order

1. Maintainer rulings on seams S2, S3 (naming; canonical homes).
2. Adapter v0.2 review resolves S4, S5 (its A1/A5 items).
3. File or formally park the Coupling Rules (S8).
4. Draft the House as the GOV-ARCH §6 interface (S10), on the
   attribution record format, with the wiki as its public porch
   (S9).
5. Ratification queue (S6) proceeds independently, document by
   document, on the maintainer's schedule.

*Draft v0.1 — 2026-11-19. Map debt declared: `governance/core/`,
`licensing/`, `patent/`, `schemas/` and
`NAHT_GOVERNANCE_AND_INTEGRATION.md` enumerated, not read; a v0.2 of
this map should close those reads before any House build.*
