# Seed-sharing contract v0 (research)

## Purpose

Define safe seed propagation between PAN-compatible state holders. A shared seed is an additive, provenance-bearing input. It is not a replacement snapshot and must never reset or overwrite the receiver's base memory.

This is a research contract and reference implementation only. It is not wired into the production world lifecycle.

## Terms

- **Base memory:** receiver-owned state that exists before a share operation.
- **Seed envelope:** immutable identity, source, version, optional parent lineage, and a JSON-compatible payload.
- **Seed ledger:** receiver-owned collection of accepted seed envelopes, keyed by seed identity.
- **Share operation:** validate and append an envelope to the ledger while preserving base memory and all previously accepted seeds.

## Required invariants

1. **Base-memory preservation:** the receiver's base memory is deeply equal before and after sharing. The operation does not replace, clear, or merge into it.
2. **Additive propagation:** accepted information is stored in a separate seed ledger.
3. **Provenance:** every envelope retains its seed ID, source ID, version, parent seed IDs, payload, and canonical content digest.
4. **Idempotency:** sharing the same seed ID with identical canonical content is a no-op.
5. **Collision safety:** the same seed ID with different canonical content is rejected; last-write-wins is forbidden.
6. **No mutation:** the input receiver state and input envelope are not mutated.
7. **Lineage retention:** parent seed IDs are carried as metadata; this contract does not infer missing ancestors or fabricate lineage.
8. **No implicit execution:** accepting a seed does not automatically execute payload instructions or mutate world subsystems.

## Reference API

`share_seed(receiver, envelope) -> new_receiver`

The reference implementation validates JSON-compatible content, computes SHA-256 over canonical envelope content, and returns a new state. It intentionally does not decide trust, authorization, semantic compatibility, or whether a payload should be applied. Those require separate policies.

## Required tests

- base memory remains byte-for-byte equivalent under canonical JSON serialization;
- existing seed ledger entries remain present;
- a new seed is appended without writing into base memory;
- identical re-sharing is idempotent;
- same-ID/different-content collision is rejected;
- caller-owned objects remain unchanged;
- parent lineage and source provenance survive serialization.

## Explicit non-goals

No cross-device synchronization protocol, encryption, access-control model, conflict-resolution policy beyond reject-on-collision, memory summarization, or automatic semantic merge is defined here. Do not treat this contract as a complete distributed-memory system.
