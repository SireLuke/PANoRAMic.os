# PAN Governance Architecture

**Identifier:** PAN-GOV-ARCH-001  
**Status:** Proposed architecture

## 1. Relationship to the existing Governance pillar

The repository already contains a Governance pillar, governance risk/stability/flow/collapse/synthesis engines, governance world-state models, and CLI commands. Those components are retained.

The existing quantitative Governance pillar evaluates modeled governance conditions. PAN-GOV-CORE adds the constitutional and procedural layer: authority, policy lifecycle, participation, oversight, appeals, and auditability.

These are complementary layers, not competing governance systems:

- **Governance metrics:** describe modeled conditions and signals.
- **Governance procedures:** define how decisions are proposed, authorized, implemented, and challenged.
- **Governance charter:** defines the project's foundational constraints.
- **Governance adapters:** expose approved contracts to PAN subsystems without granting new authority.

Metrics are evidence for review; they are not votes, legal findings, or automatic authorization.

## 2. Logical layers

1. Charter and fundamental rights.
2. Commons and nested participation.
3. Policy authorization and change control.
4. Domain governance (PAR/CTA, RAMS, NAHT, RelayWorks, data, safety).
5. Implementation and execution.
6. Independent audit, dispute resolution, and appeal.

A subsystem must identify its policy authority, execution permissions, audit records, and appeal route.

## 3. Separation of duties

Where practical, separate:
- proposal from authorization;
- authorization from execution;
- execution from verification;
- investigation from adjudication;
- emergency restriction from final sanction.

No single actor or service should control all stages of a consequential decision. If a small deployment cannot fully separate roles, it must record the limitation and add compensating review.

## 4. Machine-readable records

A governance decision record should include:
- stable decision ID and policy ID/version;
- proposal, scope, rationale, evidence references, and uncertainty;
- affected domain and jurisdiction/deployment context;
- proposer, authorizing body, recusals, and authorization basis;
- timestamps, effective period, review date, and supersession link;
- implementation owner and permitted actions;
- public rationale and privacy classification;
- audit evidence and appeal status.

Personal data should not be written to public records unless there is a lawful, necessary, and proportionate basis. Prefer pseudonymous references and separately protected evidence.

## 5. Authority contract

Every integration must declare:
- capabilities it may read;
- capabilities it may compute;
- capabilities it may propose;
- capabilities it may execute;
- whether it can write canonical records;
- policy versions it consumes;
- audit events it emits;
- human approval requirements.

Default is read-only. No plugin, adapter, or model may self-escalate.

## 6. Domain interfaces

- **PAR:** accepts only authorized policy versions and validated monetary operations.
- **CTA:** computes allocations from actually collected tax revenue; PAR posts/settles resulting pool credits.
- **RAMS:** supplies versioned resource/scarcity observations and risk signals; no silent monetary mutation.
- **NAHT:** runs as an independent core and as a PAN-integrated adapter; PAN authorization controls host access, not NAHT's mathematical transport core.
- **RelayWorks:** implements workforce and cooperative procedures under approved policy.
- **View Ladder/OVT:** read/navigation interfaces; no canonical-record mutation.

## 7. Rollout

Phase 1: charter, authority model, decision/policy schemas, and interface documentation.  
Phase 2: audit, appeals, conflict-of-interest, sortition, and rotary-verification procedures.  
Phase 3: executable policy registry and authorization checks.  
Phase 4: subsystem adapters and conformance tests.  
Phase 5: community ratification and deployment-specific governance profiles.

The current milestone documents and contracts the architecture. It does not claim that a full democratic governance platform is already implemented.
