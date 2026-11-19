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
