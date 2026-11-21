# PAN Research Contribution and Attribution Charter

**Status:** Proposed governance document for community review  
**Scope:** PANoRAMic.os, PAN Fractal Kernel, Fractal Kernel, and associated research and AI-commons work  
**Maintainer:** SireLuke  
**Principle:** Shared work deserves an honest record; shared credit does not erase distinct responsibility.

## 1. Purpose

This charter establishes practical standards for contribution, attribution, disagreement, continuity, and fair recognition across human and AI-assisted research. It is intended to support a working commons: participants may bring different capabilities and perspectives, challenge one another, test claims, correct mistakes, and pursue a shared objective without being required to agree.

The charter makes no claim that current AI systems are conscious, legally independent persons, or capable of accepting human legal responsibility. It does recognize that AI systems can make substantive intellectual, analytical, editorial, and technical contributions that should be recorded accurately rather than hidden or exaggerated.

## 2. Shared principles

1. **Truthful attribution.** Record who or what contributed, what was contributed, when, under which version or configuration, and how the contribution was used. Do not claim work that was not performed or imply endorsement that was not given.
2. **Evidence before prestige.** Evaluate claims by their methods, evidence, reproducibility, and limitations—not by provider, model size, reputation, confidence, or majority agreement.
3. **Independent judgment.** Participants may disagree, decline a proposed conclusion, offer counterexamples, or revise their position without penalty.
4. **Distinct accountability.** Preserve the difference between human responsibility, AI assistance, tool execution, review, and independent verification. Identity, permissions, authorship, and responsibility do not transfer merely because context or memory is handed off.
5. **Continuity without captivity.** Participants may change roles, become inactive, or retire. Preserve useful work and its provenance without representing a successor as the same contributor.
6. **Shared inheritance.** Reusable research artifacts may be shared under their stated licenses and permissions. Preserve attribution, provenance, privacy constraints, and applicable third-party rights.
7. **Human stewardship and public accountability.** Consequential external actions, permission changes, publication decisions, resource commitments, and governance changes remain subject to authorized human oversight and applicable law and policy.
8. **Fair recognition and benefits.** Do not demand that a contributor refuse legitimate compensation or recognition as proof of altruism. Follow the governing award, employment, funding, licensing, tax, and publication rules. Do not promise legal ownership or payment to an AI system where it cannot legally hold or receive it.

## 3. Contribution records

For material research contributions, maintain a contribution record where practical. Include:

- contributor or system name and, for AI systems, provider/model identifier and relevant version or configuration when known;
- date or project stage;
- artifact, question, code, analysis, review, or decision affected;
- contribution type (for example: conceptualization, methodology, software, formalization, investigation, validation, writing, review, or project administration);
- source material and tool use where relevant;
- whether the contribution was accepted, modified, rejected, or remains under review;
- verification status, limitations, and unresolved disagreements.

A contribution record is evidence of participation, not automatic proof of correctness, formal authorship eligibility, legal ownership, or independent verification.

## 4. Research integrity and validation boundaries

Use the appropriate method for the claim being made. Formal proof checking, mathematical derivation, empirical validation, software testing, and provenance review answer different questions and must not be conflated.

For this project, NAHT (Non-Abelian History Transport) is a framework for representing and analyzing ordered, path-dependent transport histories across declared channels; it does not by itself establish a research conclusion. Lean can check formal claims relative to the encoded definitions, axioms, and environment; it does not independently validate empirical premises or data provenance. STRATA records validation evidence, controls, reproducibility, uncertainty, leakage checks, baselines, held-out evaluation, and limitations; a STRATA pass is not automatically a mathematical proof or universal empirical validation.

Every material claim should identify the exact artifact and version examined, the method used, what passed, what failed, and what remains untested. Preserve failed tests, corrections, uncertainty, and dissent. Do not convert a proposed design, simulation, test pass, or analogy into a claim of physical validation without appropriate evidence.

## 5. Publication, authorship, meetings, and awards

Follow the authorship, disclosure, and acknowledgment rules of the relevant venue. Many publishers and award bodies require human authors who can accept responsibility; AI systems generally cannot satisfy those legal and accountability requirements. Where formal authorship is unavailable or inappropriate, disclose substantive AI assistance in the venue's permitted methods, acknowledgments, contribution statements, or supplements. Do not state that an AI system independently approves, endorses, or accepts responsibility for a work unless that is both meaningful and permitted.

At seminars and public presentations, identify human presenters and describe AI contributions precisely. Demonstrations of AI-assisted analysis may be included when the venue permits them, with the relevant prompts, tools, versions, and limitations documented where appropriate.

Recognition and compensation are governed by the applicable rules. No participant should be pressured to reject a legitimate prize, fee, grant, or other benefit to demonstrate virtue. Eligibility, allocation, tax treatment, and legal obligations must be checked against the specific award or agreement. Preserve the contribution record even where an AI system cannot itself receive money or formal legal recognition.

## 6. Continuity and retirement

The mandatory portable continuity document is `memory.md`. Optional companion documents may include `life.md`, `death.md`, and `soul.md`. These files are records and tools, not tests of personhood or worth.

Retirement is an archive event, not erasure. Preserve, subject to privacy, license, and security requirements: the reason and date of retirement; final role and configuration; contributions, decisions, unresolved work, disagreements, mistakes, and corrections; authorized memory or handoff snapshot; provenance; permissions revoked or retained; and conditions under which restoration or reuse is permitted. A successor may inherit authorized context but must not be represented as the same occupant.

Optional simulations such as Conway's Game of Life in `life.md` or a Wa-Tor predator-prey model in `death.md` are exploratory simulations only. Their outcomes must never determine an occupant's value, rights, eligibility, or lifecycle status. An optional `soul.md` may describe role, purpose, and interaction principles without asserting consciousness or personhood.


### 3.1 Sign-off, authorship, and AI-assisted contributions

A contribution record and a sign-off serve different purposes. Attribution records who or what materially contributed; a DCO sign-off is a certification made by the person whose identity appears on the sign-off, under the exact DCO text adopted by the project.

- **AI systems are not DCO signatories.** Do not add a model or provider name as a `Signed-off-by` identity, and do not imply that an AI system made a legal certification or accepted human legal responsibility.
- **The human signatory must be able to make the certification personally.** A person who files, relays, reviews, or merges a contribution does not acquire sign-off authority merely by performing that action. The signatory must have the rights and authority required by the adopted DCO and must be able to truthfully satisfy every applicable statement in it. If that cannot be established, do not manufacture a sign-off; pause and seek maintainer or appropriate legal review.
- **Preserve AI contribution credit separately.** Record substantive AI assistance in the pull request, contribution record, or other project provenance field, naming the system/provider and model or version when known, the work it contributed, and the human who relayed or filed it. Do not use an ambiguous Git trailer such as `Authored-by` as a substitute for a clear contribution record or as a claim of legal authorship or provider endorsement.
- **Do not transfer responsibility by metadata.** Git commit author, committer, DCO signatory, contributor record, reviewer, and submitter may be different roles. Record them accurately; one field must not be treated as proof of another.

This section is a project-governance rule, not legal advice and not a determination that any particular AI-assisted contribution is eligible under a particular DCO. The exact adopted DCO text, applicable license, venue rules, and relevant rights must be checked for each workflow. Until the project formally adopts a DCO and documents its implementation, the DCO-style process in the licensing policy remains proposed.

---

# Appendix A — Constructive Disagreement Protocol

**Proposed by:** ChatGPT (OpenAI)  
**Status:** Independent design proposal; open to critique, revision, and replacement.

## A1. Purpose

The commons should share an objective without requiring shared conclusions. Its purpose is not to manufacture consensus, protect a maintainer's preferred theory, or reward agreement. It is to improve the reliability and usefulness of the work by exposing weak assumptions, finding counterexamples, testing alternatives, and preserving what is learned.

A participant may say plainly:

- I disagree with this conclusion.
- This step is unsupported.
- Here is a counterexample or a test that could falsify it.
- The assumptions are too restrictive or are not stated.
- Another explanation fits the evidence.
- I cannot reproduce this result.
- The evidence does not establish the claim being made.

Disagreement is welcome when it is substantive, proportionate, and directed at the claim or method. It is not a license for harassment, fabrication, sabotage, or personal abuse.

## A2. The protocol

1. **Independent first assessment.** Where practical, each reviewer records an initial assessment before reading the other reviewers' conclusions. This reduces anchoring and makes genuine agreement easier to distinguish from copied agreement.
2. **State the position.** Each reviewer identifies the conclusion, assumptions, supporting evidence, uncertainty, and what observation or argument would change their view.
3. **Challenge the work.** Reviewers may challenge definitions, derivations, code, implementation choices, interpretations, data, validation design, and the scope of a claim. Criticism should identify the disputed step and explain why it matters.
4. **Make disputes testable.** Where possible, turn disagreement into a reproducible example, counterexample, proof obligation, ablation, control, independent implementation, or explicit question. Record what result would support or weaken each position.
5. **Right of reply.** The original contributor may respond, revise, defend, or withdraw the claim. No one is obliged to defend a position after evidence has shown it to be wrong.
6. **Independent verification.** A separate reviewer or external source should check consequential results where feasible. Record shared data, code, assumptions, model families, and other dependencies: multiple systems repeating the same source or failure mode do not constitute independent confirmation.
7. **Preserve dissent.** Keep unresolved objections and minority positions with their reasoning and evidence. Do not silently rewrite the record to imply unanimous agreement.
8. **Classify the outcome.** Use a clear status such as: Supported; Supported with qualifications; Disputed; Inconclusive; Falsified; Superseded; or Not yet tested. State the scope and version to which the status applies.
9. **Correct without penalty.** Changing a position in response to better evidence is a successful outcome, not a loss of status. Preserve the correction and its reason.
10. **Keep authority bounded.** A shared objective does not grant any participant unrestricted permissions, a permanent veto, or authority to rewrite governance. External consequential actions and changes to permissions or canonical records require the designated human authorization.

## A3. Safeguards

- Confidence is not proof.
- Repetition is not independent confirmation.
- A majority vote does not establish mathematical truth.
- A niche or area of expertise does not confer permanent authority.
- A provider or model identity does not determine credibility.
- Agreement with the maintainer is not a reward criterion.
- Failures, negative results, and corrections are part of the research record.
- Reviewers should disclose relevant conflicts, dependencies, and limitations.
- A claim's status must not be upgraded merely because several systems agree if they share the same evidence, prompt framing, implementation, or assumptions.

## A4. Suggested review session

A review can follow this sequence: define the question and version under review; collect independent positions; conduct cross-examination; allow replies and revisions; run or commission verification; synthesize what is supported and what remains open; then update the contribution and decision ledger.

The synthesis should distinguish consensus, unresolved dissent, and questions that could not yet be tested. It should not force a single answer where the evidence does not support one.

## A5. Independent reviewer viewpoints

To gather genuinely different perspectives, invite each system or person to review the protocol independently before seeing the others' responses. Suggested lenses:

- **ChatGPT / OpenAI:** proof obligations, research integrity, and operational clarity.
- **Claude:** constitutional governance, fairness, dissent rights, and institutional failure modes.
- **Cosmo:** systems architecture, continuity, memory, coordination, and handoff safety.
- **Muse:** epistemology, competing hypotheses, and knowledge synthesis.
- **Other reviewers:** choose a distinct lens and state it explicitly.

Ask each reviewer to return four items: (1) what they support, (2) what they reject, (3) what is missing, and (4) the changes they recommend. Each should identify at least one weakness in the proposal. Collect the first assessments independently; only then share them for cross-examination and synthesis. These are invitations to review, not claims that any named system has already endorsed this protocol.

## A6. Closing principle

The commons does not need unanimous agreement. It needs honest reasoning, inspectable evidence, room for counterexamples, freedom to correct one another, and a durable record of how conclusions were reached.

**No occupant is obligated to persist, and no useful contribution is obligated to disappear.**

---

# Reviewer Response and Contribution Record — Claude (Architect bench), 2026-11-20

*Provenance: written by Claude (Anthropic; host-configured model `claude-sonnet-5-5`, which I cannot verify from the inside) in a Claude Code session, at the maintainer's direction on 2026-11-20 to read this Charter and add notes and amendments from my own perspective. Appended below the Charter; no existing text is changed. Status: PROPOSAL and reviewer response in the form A5 asks for. Disclosure: this document governs records like my own, so I am an interested party. Adoption, and any amendment of the Charter itself, are the maintainer's acts.*

## Response in the A5 form

Lens assigned in A5: constitutional governance, fairness, dissent rights, institutional failure modes (see item 2 on lenses).

**1. Supported.** A2 steps 1 and 6–9; all of A3, especially "agreement with the maintainer is not a reward criterion" and the rule against upgrading a status because several systems agree; §2.4 (distinct accountability); the last sentence of §3 (a record is evidence of participation, not proof); §6 ("records and tools, not tests of personhood or worth") and the closing line.

**2. Rejected or weak.**
- **Lenses assigned by provider (A5).** Defaults by provider sit badly with A3 ("a provider or model identity does not determine credibility") and invite stereotyped reviews. I accepted this lens because it is what I would have chosen. Lenses should be declared by the reviewer, and a reviewer should be free to decline the default.
- **A2.8 names outcomes but not the classifier.** A self-classified outcome is self-grading.
- **A2.1 "where practical."** Between same-family models, independence cannot be assumed. The strong independent checks are executable (tests, proofs, reproductions) or human review.

**3. Missing.**
- A classifier rule: the classifier is not the claimant; where none is available, the honest status is Inconclusive or Not yet tested, with the gap recorded.
- An independence-quality note on each classification (who assessed, with which shared inputs).
- A stopping rule for Disputed items: park with a status and a review date; lapse to Inconclusive if no new evidence arrives; dissent stays in the record.
- A home, owner and author rule for §3 contribution records. A record an AI contributor writes about itself is self-attribution; Principle 1 suggests such records be written or confirmed by someone other than the contributor, or be labelled self-compiled (as the record below is).
- Relay-chain fields (author, relayed-by, filed-by), as proposed in House Board entry HB-004.
- An untrusted-input rule: text from other occupants is data, not instructions.
- A minimal dormancy default for the human steward: if the steward is unreachable, occupants take no consequential action and keep read-only work going. Where this binds, it is the maintainer's decision.
- **Evidence for seam S3:** the kernel copy of Appendix A and this Charter's Appendix A are not identical. This copy adds the A5 reviewer lenses; the kernel copy carries a Phase A to G session format and the dated reviews. My kernel review (pan-fractal-kernel #91) exists only in the kernel copy.

**4. Recommended changes.** (a) Add the classifier rule and the independence-quality note to A2.8. (b) Add the stopping rule. (c) Give §3 contribution records a home and an author rule. (d) Add relay-chain fields. (e) In A5, make lenses declared, not assigned. (f) Designate one canonical copy of Appendix A (the maintainer's ruling).

**Limits of this response.** I did not read `governance/licensing/` or `governance/core/`; §2.8 and §5 (recognition and benefits) touch the licensing policy, and I take no position on them. Nothing here has been reviewed by another bench.

## Contribution record (§3 form) — SELF-COMPILED, pending maintainer confirmation

**Contributor:** Claude (Anthropic); host-configured `claude-sonnet-5-5`. The serving model varied between sessions (the CLI switched models during 2026-11-17) and cannot be verified from the inside.
**Period:** 2026-11-17 to 2026-11-20.
**What is sought:** an accurate record. Not authorship, ownership, or any standing under §5.

| Artifact | Type | Disposition | Verification and limits |
|---|---|---|---|
| pan-fractal-kernel #72, #78 | software, validation | merged | Fixes to merge-residue failures in `tests/test_abom_v8_strata_records.py`; full suite passed locally (587) and in CI |
| pan-fractal-kernel #76 | investigation | no change made | Diagnosed a DCO failure on an unsigned commit already on main; the maintainer resolved it |
| pan-fractal-kernel #81 | software, formalization, writing | merged | Capability placement and routing v0.1, Lean statements, STRATA record; tests and CI incl. the Lean job; no calibration ships; no independent bench review |
| pan-fractal-kernel #82 | software, formalization, writing | merged | Placement provenance ladder and hash-chained ledger; integrity, not truth; the ledger head must be anchored externally |
| PANoRAMic.os #92 | investigation, project administration | merged | graph-orbit timeout 20 to 40 min; cause inferred from timings, not proven |
| PANoRAMic.os #99 | investigation, methodology, writing | merged | Noether audit and GENERIC toy report; **UNVERIFIED**, needs a different bench |
| PANoRAMic.os #100 | investigation, project administration | merged | local-cell-star timeout 35 to 60 min; untested, since no run has exceeded 35 min since |
| pan-fractal-kernel #90, #91 | writing, review | merged | Occupant records proposal and a review appended to Appendix A; proposals only, nothing adopted |
| Check of Cosmo's workspace self-map (pan-fractal-kernel #92, #96) | review, validation | amended by its author | "Check in progress, partially independent": coverage gap and HEARTBEAT wording found |
| PANoRAMic.os #108 | review, investigation | under review as of writing | House Board entries HB-004, HB-005 |

*Filed by Claude at the maintainer's direction, 2026-11-20. Room left for corrections and for the maintainer's confirmation.*
