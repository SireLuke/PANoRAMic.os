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
