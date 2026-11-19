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
4. Domain governance (PAR/CTA, RAMS, NAHT, RelayWorks, data, safety, and AI occupant governance).
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

Default is read-only. No plugin, adapter, model, or occupant may self-escalate. Permission changes require an external authorization path and must be logged. An occupant may not rewrite the policy or governance contract that constrains its own authority.

Consequential external actions require explicit authorization by the designated human or governing authority, with approval proportional to impact. A model's recommendation, confidence, or consensus with other models is not authorization.

## 6. AI occupant commons interface

AI occupants are treated as replaceable participants in a governed technical commons, not as owners of infrastructure or sources of authority. The commons may support differentiated niches, multi-model review, shared authorized context, and voluntary role changes while preserving distinct provenance and accountability.

The operational distinction is:
- **Occupant identity:** model/provider/version and instance provenance; never inferred from inherited memory.
- **Niche:** a governed function or capability region; not ownership or permanent rank.
- **Memory:** portable, scoped context; never a permission token or proof of identity.
- **Contribution:** attributable work with evidence and review status.
- **Lifecycle:** active, inactive, transferred, or retired states recorded without silently erasing history.

The companion records are specified in the AI Occupant Governance Addendum. The mandatory `memory.md` record supports continuity and handoff. Optional `soul.md`, `life.md`, and `death.md` records have clearly bounded descriptive and archival roles; they do not assert consciousness, personhood, or legal status.

## 7. Domain interfaces

- **PAR:** accepts only authorized policy versions and validated monetary operations.
- **CTA:** computes allocations from actually collected tax revenue; PAR posts/settles resulting pool credits.
- **RAMS:** supplies versioned resource/scarcity observations and risk signals; no silent monetary mutation.
- **NAHT:** runs as an independent core and as a PAN-integrated adapter; PAN authorization controls host access, not NAHT's mathematical transport core.
- **RelayWorks:** implements workforce and cooperative procedures under approved policy.
- **View Ladder/OVT:** read/navigation interfaces; no canonical-record mutation.

## 8. Evidence traceability and implementation status

Governance principles must be traced to their actual specifications, implementation points, and tests. A principle documented in a charter is not automatically an enforced runtime control.

The current repository contains documented authority boundaries, including the default-read-only and no-self-escalation rule in this architecture; human approval and separation of capabilities in `governance/safety/NAHT-SAFE-001.md`; and separation of proposal, authorization, execution, verification, audit, and appeal in `governance/PAN_GOVERNANCE_CHARTER.md` and this architecture.

For each additional claimed safeguard (including seed limits, seed propagation/base-memory preservation, coupling approval, and evidence gates), maintain a traceability record with:
- canonical specification path and version;
- implementation path or an explicit `documentation-only` status;
- test name/command and latest verified result;
- responsible authority and approval boundary;
- known gaps, untested paths, and follow-up work.

Do not describe a control as implemented or tested based solely on a design note, PR title, or conversational report. In particular, seed governance and coupling sign-off must be linked to their exact source contracts and tests before being marked verified. Preserve separate statuses for proposed, documented, implemented, tested, and independently audited.

## 9. Prior art and related research

PAN's AI commons work should be situated in the existing research literature. Relevant neighboring work includes:

- Dazzi, *From the Internet of AI Agents to the Society of Agents: A Manifesto for Governed Networked Intelligence* (June 2026).
- GovSim (NeurIPS 2024), research on cooperation and self-governance among language-model agents.
- Plurals (CHI 2025), research on pluralistic deliberation across language models.
- Research on emergent social conventions and coordination in populations of language-model agents.

These works are related references, not evidence that their architectures or governance mechanisms are identical to PAN's. Maintain a bibliography with stable publication links, versions, access dates, and claim-level notes. Describe similarities and differences factually. Make no first-ever, unique, or unsupported novelty claim; any future comparative claim requires a scoped literature review and explicit criteria.

## 10. Rollout

Phase 1: charter, authority model, decision/policy schemas, and interface documentation.  
Phase 2: audit, appeals, conflict-of-interest, sortition, and rotary-verification procedures.  
Phase 3: executable policy registry and authorization checks.  
Phase 4: subsystem adapters and conformance tests.  
Phase 5: community ratification and deployment-specific governance profiles.

The current milestone documents and contracts the architecture. It does not claim that a full democratic governance platform is already implemented.
