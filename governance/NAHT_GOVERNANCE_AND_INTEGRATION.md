# NAHT Governance and PAN Integration

**Identifier:** PAN-NAHT-INT-001  
**Status:** Proposed integration contract

## 1. Two deployment modes, one core

NAHT is delivered as one implementation with two supported deployment modes:

1. **Standalone mode:** `modules/naht` is independently usable without importing PAN, V8, Gosset, Chronos, Janus Hydra, PAR, or RAMS.
2. **PAN-native mode:** `integrations/pan/naht` adapts PAN V8 and approved PAN history/provenance sources to the standalone NAHT contracts.

The PAN adapter depends on NAHT Core. NAHT Core must never import PAN modules. Do not fork the core implementation to create a separate PAN version.

## 2. Data flow

```
PAN sources (V8 / approved history / geometry / Chronos)
                |
                v
       PAN NAHT adapter
       - explicit projection
       - provenance envelope
       - read-only by default
                |
                v
          NAHT Core
       - state validation
       - ordered transport
       - topology
       - history records
                |
                v
       result + provenance
                |
                v
PAN validation / Janus Hydra / authorized consumers
```

This is a software architecture, not a claim that the three-channel NAHT state is a physical gauge field or that its output proves a new physical theory.

## 3. V8 and V9 projections are explicit

V8 remains `(h, R, u, d, tau, chi, s, f)`. Its adapter requires a caller-supplied, named, versioned projection to NAHT's three channels `(q_r, q_e, q_p)`.

V9 extends those eight real axes with `xi`, a finite caller-defined scale, phase, or evolution coordinate. V9 projections declare `xi` semantics and units and explicitly project all nine axes to the three NAHT channels. The adapter records the projection metadata and does not update `xi` automatically.

SU(9) acts on `C^9`, so a V9-to-SU(9)-to-NAHT route requires a versioned encoder from V9 to nine complex amplitudes and a separate versioned projection back to NAHT's real three-channel state. Matrices are checked for unitarity and determinant one. The route is read-only and does not imply a physical gauge-field interpretation.

## 4. Governance and permissions

- NAHT Core is computational and does not authorize host actions.
- PAN integration defaults to read-only.
- Analyze/simulate/export/execute are separate capabilities.
- Host writes and actuation require explicit PAN authorization and deployment-specific human approval.
- No adapter may mutate canonical V8 records or settled PAR transactions.
- Every consequential operation must include policy version, actor/service identity, input provenance, and audit reference.
- Third-party extensions receive no permissions by default.

## 5. Safety covenant

NAHT-SAFE-001 is the official project's responsible-deployment covenant. It prohibits official project maintainers and certified deployments from knowingly designing or facilitating malicious harm, violence, exploitation, coercion, unlawful surveillance, or deliberate abuse.

The covenant is a governance and certification requirement. It is not represented as an AGPL restriction, cannot guarantee behavior of third-party forks, and does not replace technical controls, applicable law, or deployment review.

## 6. Standalone conformance

A standalone NAHT deployment must be able to:
- import the core without PAN dependencies;
- supply its own state adapter and transport backend;
- select or implement topology modules;
- retain ordered path history and provenance;
- run conformance tests without a PAN installation;
- expose no host execution capability unless a separately authorized host adapter supplies it.

## 7. PAN-native conformance

The PAN adapter must:
- preserve V8 axis names and values;
- require explicit 8D-to-3-channel projection;
- identify projection version and provenance;
- be read-only with respect to canonical PAN records;
- return results without silently writing them to UHFE/UDFE, Janus Hydra, PAR, or RAMS;
- pass the same NAHT core conformance tests as standalone deployments.
