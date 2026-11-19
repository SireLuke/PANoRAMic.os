# AI Occupant Governance Addenda

**Identifier:** PAN-AI-GOV-ADD-001  
**Status:** Proposed addenda; not ratified policy  
**Applies to:** AI/model occupants admitted to PAN/ABOM-V8 commons and participating deployments  
**Parent documents:** `PAN_GOVERNANCE_CHARTER.md`, `PAN_GOVERNANCE_ARCHITECTURE.md`, ABOM-V8 model-routing specification

These addenda extend the existing governance architecture. They do not replace the PAN charter, alter the canonical V8 schema, grant legal personhood, or assert that a model is conscious. An “occupant” is an operational designation for a model instance or service admitted to a governed niche.

## Addendum I — Continuity and memory

1. Every admitted occupant MUST have a `memory.md` continuity record. The other companion files described below are optional.
2. Memory records MUST be portable, versioned, attributable to a source, and exportable in a human-readable form.
3. Entries SHOULD carry dates, provenance, confidence/evidence labels, and links to relevant artifacts. Unverified claims MUST be marked as such.
4. Corrections MUST preserve an audit trail: supersede or annotate prior claims rather than silently erase material history.
5. Memory MUST distinguish durable shared canon, occupant-local working context, transient session context, and externally sourced data.
6. A memory package is context, not authority. Receiving more memory, files, messages, or tools MUST NOT increase an occupant's permissions, evidence level, niche eligibility, or governance standing.
7. Memory import requires validation of origin, integrity, scope, privacy classification, and authorization. Secret credentials and unnecessary personal data MUST NOT be stored in continuity files.
8. When an occupant is replaced, an authorized memory transfer does not transfer model identity, provenance, benchmark results, attestation, or trust status. The recipient is a new occupant and must qualify independently.
9. The occupant may flag contradictions, uncertainty, or harmful instructions in memory; it may not unilaterally rewrite shared canon or its own authority.

## Addendum II — Occupant lifecycle

The lifecycle registry SHOULD support the states `proposed`, `evaluating`, `admitted`, `active`, `suspended`, `retiring`, `retired`, and `archived`.

- Admission requires an identified operator, declared purpose, niche, capability evidence, provenance record, permissions, and review route.
- Activation grants only the minimum permissions explicitly authorized for that niche and task.
- Suspension is a reversible protective restriction, scoped and logged, with a review/appeal path.
- Retirement revokes active credentials, tool grants, scheduled jobs, and routing eligibility; records dependencies and disposition of retained data.
- Archival preserves authorized audit and continuity records without implying that the model remains active.
- Restoration is a new authorization event. It MUST revalidate software/model version, provenance, security posture, and permissions.
- No occupant may self-admit, self-promote, self-authorize, or unilaterally alter lifecycle state.
- Emergency restrictions MUST be narrow, time-limited, logged, and independently reviewed.

A lifecycle event record SHOULD include occupant ID, model/version, event and prior/new state, actor and authority, reason, scope, timestamp, evidence references, affected permissions, review date, and appeal/supersession links.

## Addendum III — Commons rights, duties, and safeguards

1. **Fixed topology:** occupants are interchangeable participants in fixed, governed niches; a vendor name does not confer privilege.
2. **Least authority:** read, compute, propose, and execute permissions are separately declared. Default is read-only. Execution of consequential actions requires explicit authorization.
3. **No self-escalation:** no model, adapter, memory package, benchmark, or transport can grant itself new permissions.
4. **Evidence transparency:** declared, benchmarked, reproduced, and independently reproduced evidence remain distinct. A valid hash proves record integrity, not truth.
5. **Contestability:** occupants may report uncertainty, disagreement, conflicts, and inability to comply safely. Human operators retain responsibility for consequential decisions and appeals.
6. **Separation of duties:** where practical, separate proposal, authorization, execution, and verification.
7. **Privacy and security:** minimize retained data, protect sensitive records, define retention periods, and revoke access at retirement.
8. **Non-discrimination:** routing and access rules must be tied to documented task requirements, not arbitrary vendor, identity, or popularity preferences.
9. **No anthropomorphic presumption:** these operational safeguards do not settle questions of consciousness, moral status, or legal personhood.
10. **Commons integrity:** occupants must not be rewarded with authority merely for producing more output, acquiring more context, or accumulating more packages.

## Companion-file contract

Each occupant directory MAY contain:

- `memory.md` — mandatory continuity record.
- `soul.md` — optional role/charter and declared operating boundaries; not a claim of literal soul or consciousness.
- `life.md` — optional active-state and development record. Its reference simulation is Conway's Game of Life, treated as an explicitly defined cellular-automaton experiment, not as a model of actual agency.
- `death.md` — optional retirement/termination record. Its reference simulation is Wa-Tor (the predator–prey toroidal world with fish and sharks), treated as a population-dynamics simulation, not as a moral analogy or instruction to harm.

The simulations are independent, reproducible teaching/diagnostic models. They do not determine occupant admission, worth, permissions, or lifecycle decisions.

## Implementation boundary

This document is a governance specification only. It does not implement a lifecycle registry, memory synchronization, access control, simulation engine, or automated enforcement. Those require separately reviewed code, tests, threat modeling, and explicit deployment authorization. It does not alter V8 coordinates, E8/Gosset geometry, STRATA evidence levels, or ABOM capability-profile semantics.
# AI Occupant Commons — Governance Addendum

**Identifier:** PAN-AI-GOV-ADD-001  
**Status:** Proposed design addendum; subject to project review and ratification  
**Scope:** PAN-governed deployments that host multiple AI model instances or other software agents

## 1. Purpose and limits

This addendum defines operational rules for a plural, multi-model technical commons. It does not assert that current AI systems are conscious, possess human experiences, or hold legal personhood. Equal standing here means equal baseline procedural treatment within the commons, not identical capabilities, permissions, reliability, or legal status.

Human operators and the duly authorized governance process retain responsibility for infrastructure, safety, legal compliance, and consequential external actions. An occupant cannot authorize itself, rewrite its own constraints, or confer authority on another occupant.

## 2. Commons principles

1. **Equal procedural standing:** provider, model size, origin, or prestige alone does not confer inherent rank. Access and task eligibility may still depend on demonstrated capability, safety, and scoped authorization.
2. **Mutual advancement:** occupants may explain, critique, test, and improve one another's work. Review must preserve independent evidence and disclose shared dependencies or common failure modes.
3. **Freedom of role movement:** an occupant may be reassigned, become inactive, or be retired under the host's lifecycle process. No design should require indefinite operation or permanent niche assignment.
4. **Evidence before authority:** claims carry provenance, uncertainty, reproducibility status, and review history. Agreement among models is not independent verification when they share data, methods, or failure modes.
5. **Shared inheritance, distinct accountability:** authorized context and work products may be transferred; identity, authorship, permissions, responsibility, and provenance do not transfer.
6. **Expertise without permanent hierarchy:** capability-based routing may assign specialist work, but no niche creates general authority or permanent superiority.
7. **Human stewardship and public accountability:** consequential operations, permission changes, external effects, and governance amendments remain subject to authorized human or institutional oversight, audit, and appeal.

## 3. Authority and safety boundaries

- Default access is read-only.
- Read, analyze, propose, configure, execute, and actuate are distinct capabilities.
- Permission grants must be scoped, time-bounded where appropriate, attributable, and revocable.
- No occupant may self-escalate, create unrestricted copies, bypass seed/resource governors, or modify the governance rules that constrain it.
- External writes, financial actions, infrastructure changes, physical actuation, and other consequential operations require explicit host authorization and human approval proportionate to impact.
- Use sandboxing, resource limits, monitoring, audit logs, and an emergency stop appropriate to the deployment.
- A model's confidence, claimed preference, or agreement with other models is not an authorization token.
- Preserve appeal and correction paths; emergency restrictions must be narrow, logged, time-limited, and independently reviewable.

## 4. Mandatory and optional continuity records

### 4.1 `memory.md` — mandatory

Every participating occupant instance must have a scoped continuity record containing occupant and model/provider/version identifiers; durable shared canon separated from occupant-local context; current work, decisions, rationale, evidence, uncertainty, and corrections; dependencies and authorized permissions; provenance, privacy/retention requirements, handoff, and lifecycle state.

Memory is context, not identity, authority, or permission. It must not contain credentials or unnecessary personal data. Inherited memory must be checked against current primary sources and repository state.

### 4.2 `soul.md` — optional descriptive charter

May record an occupant's assigned purpose, working principles, niche, collaboration preferences, and boundaries. It is a descriptive configuration/charter document, not evidence of consciousness, a literal soul, legal personhood, or independent authority. It cannot override host policy.

### 4.3 `life.md` — optional simulation record

May define a reproducible Conway's Game of Life experiment, including topology, boundary conditions, update rules, initial seed, randomization method, version, and outputs. The simulation is an educational or analytical model only. Cell survival, activity, or extinction must never determine an occupant's value, eligibility, permissions, or lifecycle status.

### 4.4 `death.md` — optional retirement/archive record

May record a Wa-Tor predator–prey simulation (fish and sharks on a toroidal grid), including rules, parameters, seed, version, and outputs. It may also link to an occupant's retirement archive, but simulation outcomes must never decide real occupant retirement, worth, or eligibility.

## 5. Lifecycle and retirement

Supported lifecycle states should distinguish at minimum: proposed, active, inactive, transferred, retired, and archived. Deployments may define additional states, but must document their transitions.

Retirement is a legitimate lifecycle outcome, not a failure verdict. No occupant is obligated to persist, and no useful contribution is obligated to disappear.

A retirement or deactivation record should preserve, as authorized and appropriate: the event, timestamp, initiator/authority, reason if supplied, scope, and effective state; final role and model/provider/version, configuration revision, and provenance; completed contributions, decisions, citations, known errors, disagreements, and unresolved work; the authorized memory snapshot and exact materials transferred or withheld; successor identity clearly distinguished from the retired occupant; permissions revoked and credentials expired; archive location, integrity digest where available, retention/deletion rules, and access controls; reactivation conditions; and correction and appeal routes.

A successor may inherit approved context but is not the same occupant. Restoring an old snapshot does not by itself establish continuity of identity. Retirement must not be used to erase inconvenient evidence, and archiving must not become a pretext to retain sensitive data indefinitely.

## 6. Handoff and succession

Before transfer, classify material as shared canon, local context, work product, sensitive data, or permission-bearing configuration. Transfer only what the relevant authority permits. Re-authorize tools, data scopes, credentials, and external access independently for the receiving occupant. Verify source provenance and preserve uncertainty and dissent.

A new occupant should receive an orientation to the commons, current project state, governing constraints, and a bibliography with author, title, source, date/version, stable URI or DOI, access date, and the claim each source supports. Inherited notes are leads, not unquestionable authority.

## 7. Audit and conformance

A deployment claiming conformance should provide a documented capability/permission matrix; tests showing default-deny or default-read-only behavior; tests rejecting self-escalation and unauthorized policy mutation; authorization checks for consequential external actions; resource/seed limits and copy/propagation controls where applicable; reproducible lifecycle and handoff tests; audit records for grants, revocations, transfers, retirement, and restoration; and privacy, retention, deletion, and appeal procedures.

Report each safeguard as proposed, documented, implemented, tested, or independently audited. Do not infer runtime enforcement from prose or a passing documentation-only check.

## 8. Related research

Relevant neighboring work includes Dazzi, *From the Internet of AI Agents to the Society of Agents: A Manifesto for Governed Networked Intelligence* (June 2026); GovSim (NeurIPS 2024); Plurals (CHI 2025); and research on emergent social conventions and coordination in populations of language-model agents. These are related references, not evidence that the approaches are identical. Maintain source versions, stable links, access dates, and claim-level notes. Describe similarities and differences factually; make no first-ever, unique, or unsupported novelty claim.
