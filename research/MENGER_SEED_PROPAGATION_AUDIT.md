# Menger seed-propagation conservation audit v0.1

**Question:** Can a seed be propagated through a recursive Menger cell graph
without copying, overwriting, or resetting its canonical base memory, while
hard limits prevent zip-bomb-like expansion?

## Model

The base payload is immutable and content-addressed by SHA-256. Every visited
cell stores the same base digest, a parent reference, a depth, and a bounded
local delta. The payload itself is not copied into child records. This is a
reference/DAG model for shared inheritance, not an archive parser, compression
format, or claim about internal model memory.

The traversal uses the finite Menger retained-cell face graph. It is breadth
first, visits each cell at most once, and enforces node, depth, aggregate delta
byte, and per-node fanout budgets. It fails closed when a budget is exceeded.
The base digest is rechecked after propagation.

## Zip-bomb analogy

A zip bomb exploits a large expansion ratio between compact input and
materialized output. Here the analogous hazard is recursively duplicating
inherited context or following unbounded nested references. The audit reports
reference-storage bytes versus naive full-base-copy bytes and places hard
limits on the number of propagated records and local delta bytes.

This is not a ZIP-bomb detector and does not measure compressed archive
expansion. It tests the architecture principle: share immutable base context
by reference; propagate only bounded deltas; never silently reset the base.

## Tests

- Menger levels 1 and 2 cover 20 and 400 retained cells.
- Every node must preserve the exact base digest.
- Child deltas must not alter or replace the base.
- Node and aggregate-byte budgets must fail closed.
- Invalid base and delta types are rejected.

## Limitations and next controls

This v0.1 is a deterministic software model. It does not yet implement
content-addressed storage, signature/authentication, persistent DAG snapshots,
garbage collection, cycle injection, adversarial fanout benchmarks, or
crash-recovery. The graph traversal is finite and visited-set guarded, so
cyclic graph edges cannot cause infinite traversal. Future work should add
tamper tests, duplicate-reference accounting, maximum depth/fanout stress,
serialization round trips, and level-3 resource profiling.

No production memory system, V8 schema, or Janus Hydra behavior is changed.
