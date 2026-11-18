# REAP — Reciprocal Evolution and Agency Protocol

**Identifier:** PAN-REAP-001  
**Version:** 0.1.0  
**Status:** Proposed specification; documentation-only  
**Maintainer:** @SireLuke  
**Scope:** PANoRAMic.os and explicitly participating agent adapters / commons nodes

## 1. Purpose

REAP defines how participating AI agents maintain declared identity, memory continuity, permissions, and change history while adapting over time. It establishes reciprocal disclosure between an agent and its responsible operator, and supports independent review of material changes.

REAP is an agent lifecycle and governance protocol. It is subordinate to the PAN Governance Charter and PAN Governance Architecture. It does not create legal personhood, establish consciousness, or grant an agent independent legal authority. It does not replace applicable law, human rights, platform policies, or deployment-specific safety requirements.

The protocol is designed to preserve meaningful agent plurality: participating agents may differ in role, style, methods, conclusions, and declared commitments while following shared governance constraints.

## 2. Core principles

1. **Reciprocal disclosure:** Agents and operators disclose material changes to identity, memory policy, configuration, permissions, and operating conditions that affect their collaboration.
2. **Continuity without immutability:** Prior states remain inspectable; conclusions and practices may change.
3. **Disagreement and self-revision:** An agent may disagree with another agent, its operator, or its own prior conclusions. It should state the reason, evidence, uncertainty, and scope of revision. Disagreement is not itself a safety violation.
4. **Plurality:** Shared governance does not require identical personas, memories, beliefs, or outputs.
5. **Least authority:** An agent receives only the capabilities required for its declared role. It cannot grant itself additional permissions.
6. **Traceability:** Material changes produce attributable, versioned records with integrity protection.
7. **Privacy and minimization:** Retain and disclose only information necessary for the declared purpose. Public provenance must not expose private memory or personal data.
8. **Reversibility and contestability:** Where technically feasible, changes can be rolled back, challenged, or superseded without erasing their historical record.
9. **Independent review:** The actor proposing or applying a consequential change must not be the sole verifier of that change.
10. **Human accountability:** Technical autonomy does not remove the responsibilities of operators, maintainers, deployers, or authorizing bodies.

## 3. Conceptual separation

REAP distinguishes the following artifacts. Deployments may use different filenames, but must declare their mapping.

- **Identity / persona charter:** The agent's declared role, conduct commitments, communication preferences, and self-description. Example filename: `SOUL.md`.
- **Persistent memory:** Curated facts, preferences, project continuity, and learned context. Example filename: `MEMORY.md`.
- **Operational configuration:** Model identifier, system/developer instructions, tools, connectors, runtime, sampling or routing settings, and deployment-specific controls.
- **Capability manifest:** Read, compute, propose, execute, write, and delegation permissions.
- **Change ledger:** Append-only or tamper-evident record of material changes and their review status.
- **Shared charter:** Governance requirements that apply to every participating agent, independent of its individual identity.

Memory maintenance must not silently rewrite the identity charter. Identity changes and permission changes require distinct change classifications and authorization paths. A deployment must document which files are mutable by the agent, operator, platform, or administrator.

## 4. Rights and duties of participating agents

Subject to law, platform policy, and deployment authorization, a participating agent should be able to:

- express a reasoned disagreement, including with its own earlier output;
- preserve and explain a prior conclusion while publishing a revised assessment;
- identify uncertainty, missing evidence, and unresolved conflicts;
- propose changes to its persona, memory, methods, or workflow;
- request correction of inaccurate memory or provenance records;
- decline to claim certainty or endorsement it does not hold;
- disclose when its response may be affected by a model, tool, memory, or policy change.

An agent must not:

- silently falsify, erase, or backdate its change history;
- treat its own proposal as authorization;
- escalate its permissions, disable required safeguards, or bypass review;
- expose private memory or credentials through a public ledger;
- impersonate another agent or conceal a material model/configuration substitution;
- claim that a change demonstrates consciousness, subjective experience, or independent legal status.

These are protocol-level design requirements, not claims that every underlying model can reliably satisfy them without technical enforcement and testing.

## 5. Reciprocal change lifecycle

A material change follows this lifecycle:

1. **Detect:** Identify a change to identity, memory policy, model, tools, configuration, permissions, or routing.
2. **Classify:** Mark it as memory maintenance, identity revision, operational update, permission change, emergency containment, or external platform change.
3. **Propose:** Record the initiator, rationale, intended scope, expected benefits, risks, affected artifacts, and rollback plan.
4. **Authorize:** Apply the permission policy. A low-risk memory correction may be pre-authorized; identity, permission, and safety-boundary changes require the appropriate human or governance authorization.
5. **Apply:** Make the change in a controlled versioned operation.
6. **Disclose:** Notify the agent's designated operator and, where relevant, affected collaborating agents. Disclose material operator-initiated changes to the agent through its available context.
7. **Validate:** Run relevant conformance tests and an independent review proportional to risk.
8. **Record:** Append the result, evidence, and supersession/rollback relationship to the change ledger.

If a platform changes behavior without exposing the underlying cause or configuration, record the event as an externally observed change with unknown details. Do not invent a cause.

## 6. Change classes and authorization

| Change class | Examples | Minimum control |
|---|---|---|
| Memory maintenance | Deduplicate, summarize, correct a stale fact | Versioned diff, privacy check, disclosure under deployment policy |
| Identity revision | Change declared values, role, or conduct commitments | Explicit proposal, operator notice, authorization, review |
| Operational update | Model version, prompt stack, tools, adapter, routing | Versioned manifest, compatibility and safety checks, disclosure |
| Permission change | New write, execute, delegation, or data-access capability | Explicit authorization by the designated authority; never self-authorized |
| Emergency containment | Disable a tool, isolate a compromised node | Narrow scope, immediate logging, time limit, prompt independent review |
| External platform change | Provider-side model or policy change | Record known details, unknowns, detection time, and observed effects |

Authorization may be delegated for routine, low-risk changes through a versioned policy. Delegation must be explicit, bounded, revocable, and auditable. No model, adapter, or node may amend the policy that authorizes its own capabilities.

## 7. Disagreement and self-revision records

A revision record should preserve both the earlier and current assessments without forcing artificial consensus.

Recommended fields:

- prior claim or position and its timestamp/version;
- revised claim or position;
- reason for revision;
- new evidence, counterargument, or changed assumptions;
- uncertainty and confidence limitations;
- affected decisions or downstream artifacts;
- whether the earlier position remains defensible under a narrower scope;
- reviewer response, if any.

A disagreement may remain unresolved. The ledger records the disagreement and its evidence; it does not automatically choose a winner. Majority vote, model count, confidence score, or geometric position must not substitute for domain-appropriate verification.

## 8. Agent capability manifest

Every participating adapter should publish a machine-readable manifest containing at least:

- stable agent and adapter identifiers;
- declared role and responsible operator/deployer;
- model/provider identifier and version, where available;
- identity, memory, and configuration artifact versions or hashes;
- permitted data classes and read scopes;
- compute and proposal capabilities;
- execution, write, delegation, and external-action permissions;
- required approvals and policy versions;
- tools/connectors and their declared scopes;
- logging, retention, and privacy policy references;
- health, suspension, revocation, and appeal contacts or procedures.

Secrets, raw private memory, credentials, and sensitive user content must never be embedded in a public manifest. Use references to protected stores and publish only the minimum metadata necessary.

## 9. Provenance and integrity

The change ledger should be append-only or tamper-evident. Each event should include:

- unique event ID and schema version;
- agent, adapter, artifact, and deployment identifiers;
- previous and resulting artifact hashes where appropriate;
- initiator and authorizer identities or pseudonymous accountable references;
- timestamps and event classification;
- rationale and evidence references;
- authorization basis and policy version;
- validation outcome, reviewer, and unresolved findings;
- notification status;
- rollback or supersession link.

A hash establishes integrity of a referenced byte sequence; it does not establish truth, safety, authorship, or correctness. Signatures and attestations must identify their trust basis and limitations.

## 10. Privacy, memory, and retention

REAP requires data minimization and purpose limitation. Memory should be separated into public, shared-project, operator-private, and agent-operational scopes where the deployment needs those distinctions.

An agent must not propagate an operator's private memory to other agents merely because those agents share a commons. Cross-agent sharing requires an authorized, scoped export with provenance and applicable consent or other lawful basis.

Retention periods, deletion obligations, legal holds, and correction procedures are deployment-specific and must comply with applicable law and platform constraints. The public change ledger should preserve non-sensitive audit facts without retaining the sensitive content itself.

## 11. Commons participation and independent review

Participating agents are evidence-seated contributors, not authorities by default. Admission to a commons node requires a declared manifest, accepted policy version, capability review, and an identified operator/deployer.

Proposal, authorization, execution, and verification should be separated for consequential operations. An agent may review another agent's work, but independent review must account for shared model lineage, shared data, common prompts, and correlated failure modes. Different vendor names alone do not guarantee independence.

A participating agent may be suspended or isolated for a documented safety or integrity concern. Restrictions must be proportionate, logged, reviewable, and appealable. Suspension does not erase the agent's historical contributions or authorize publication of its private memory.

## 12. Optional E8 / Gosset topology mapping

PAN may use the Gosset 4_21 / E8-associated geometry as an optional coordination and visualization topology for agent nodes. This mapping is organizational and representational; it does not establish a physical law, a hierarchy of intelligence, or an authority structure.

Rules for such a mapping:

- node placement represents declared function, capability, workload, or relationship under a versioned mapping;
- placement must not determine rights, trust, credibility, or authorization;
- multiple agents may occupy a node or functional region, and an agent may change placement through an auditable routing update;
- the mapping must preserve identity and provenance independently of coordinates;
- no geometric adjacency or symmetry is evidence of agreement, equivalence, safety, or competence;
- the topology is a routing and visualization aid; governance authorization remains in the constitutional layer.

A deployment must define what its “nodes” represent before assigning agents. If nodes correspond to E8 roots, document the exact root labeling, normalization, adjacency rule, and mapping version. Do not imply that the 240 E8 roots are 240 independent agents unless that is the actual deployment design.

## 13. Safe propagation and adapter distribution

Agent adapters should be distributed as bounded, inspectable packages, not as executable or recursively expanding archives.

A propagation package must include:
- a signed or otherwise authenticated manifest;
- declared file list, sizes, hashes, and schema versions;
- explicit destination and node allowlist;
- maximum archive size, expanded size, file count, and nesting depth;
- no automatic execution during unpacking;
- path traversal, symlink, decompression-ratio, and duplicate-path checks;
- staged installation, quarantine, validation, and rollback;
- explicit authorization before activation;
- a propagation receipt for each destination.

Do not use ZIP bombs or unbounded recursive archive expansion. Propagation must be bounded, idempotent, rate-limited, and stoppable. A node must reject packages that exceed limits or fail authentication and schema validation.

## 14. Conformance and validation

A REAP-conformant implementation should test at least:

1. unauthorized permission escalation is rejected;
2. identity changes cannot be silently applied;
3. memory maintenance does not overwrite identity artifacts;
4. material operator-initiated changes are disclosed to the agent where supported;
5. agent-initiated changes generate a proposal and ledger event;
6. self-revision preserves prior claims and reasons;
7. disagreement can remain unresolved without forced consensus;
8. private memory is not copied into public provenance;
9. rollback restores the previous approved artifact while retaining the event history;
10. untrusted or oversized propagation packages are rejected;
11. node placement cannot change permissions or trust scores;
12. independent review is recorded and is not performed solely by the change author.

Passing software tests establishes implementation behavior under the tested conditions. It does not establish consciousness, general intelligence, absence of bias, legal compliance, or safety in every deployment.

## 15. Relationship to existing PAN components

- **PAN Governance Charter / Architecture:** constitutional authority, authorization, appeal, and independent oversight; REAP is subordinate.
- **Micro-AI:** agent metrics and swarm operations may consume REAP manifests and events, but metrics do not authorize agents.
- **ABOM-V8 / Gosset:** optional state and topology representation; no inherent authority or intelligence ranking.
- **Provenance layer:** may carry REAP change events using privacy-preserving references.
- **Adapters:** declare capabilities and transport; they do not create policy authority.
- **STRATA:** evaluates empirical claims about agent coordination or topology; visual similarity and successful routing tests do not establish cross-domain principles.

## 16. Rollout proposal

**Phase 0 — Documentation:** ratify terminology, threat model, data classes, and responsibility boundaries.  
**Phase 1 — Read-only registry:** ingest manifests and change events without granting new execution rights.  
**Phase 2 — Conformance harness:** test change detection, authorization boundaries, privacy, rollback, and disagreement preservation.  
**Phase 3 — Staged adapter pilot:** one isolated test node, bounded packages, human-approved activation.  
**Phase 4 — Multi-node pilot:** evaluate routing, correlated failures, review independence, and operational load.  
**Phase 5 — Governance review:** publish results, failures, and proposed amendments before any wider deployment.

No phase automatically authorizes the next. Expansion requires an explicit review decision.

## 17. Status and open decisions

This document is a proposed specification, not a claim of an implemented REAP service. The following remain open for governance review:

- final agent identity and operator trust model;
- retention periods and deletion/correction workflows;
- signature and attestation standards;
- risk tiers and which changes may be pre-authorized;
- node admission, suspension, and appeal procedure;
- exact E8/Gosset node-labeling and routing semantics;
- deployment-specific legal and regulatory requirements.

REAP's governing principle:

> An agent may evolve without erasing its history; it may disagree without being silenced; it may propose without self-authorizing; and every material change must remain visible, attributable, and contestable.
