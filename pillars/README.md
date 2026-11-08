# Pillars: wiring status

`core/tick/tickLoop.ts` calls one `update*` function per pillar each tick. This table records what exists, so nobody mistakes a placeholder for a model.

## Wired into the tick loop (17)
Population, resources, economy, Governance, humanitarian, medical, antigenocide, markets, crime, education, migration, trafficking, transparency, corporatecapture, epistemic, repairability, quantum.

Each has a `<name>Engine.ts` that is a **hold engine** (`pillars/holdPillar.ts`): it returns the pillar's declared default state with the current state merged over it, and throws on non-finite numbers. **No dynamics are defined for these pillars yet**, so the tick loop runs but these states do not evolve. Replace an engine body only when a stated, tested model exists for that pillar. `tests/tick/tickWiringChecks.ts` pins the current behaviour (runs, deterministic, pure, defaults, rejects bad data).

Nodes are updated separately by `nodeMap/updateNodeMap`; global signals come from `computeGlobalSignals`.

## Not wired into `WorldState` / the tick loop (22)
- **Substantial modules** (several files each): commons, culture, ecology, gep, health, infrastructure, labor, microAI, modes, nodes (via nodeMap), par, rights, workforce.
- **State stubs only** (a single `STATE.ts` or one file, no engine, no `WorldState` field): commonsip, cultural, harmindex, planet, rams, regulation, rightslabor, stability, timewealth.

Wiring any of these means adding a `WorldState` field, an engine and a test; the modules above already have cores/profiles that engines can build on. `par` has a tested demurrage/fee engine under `engine/par/` that is not called from the tick loop.

## Known pre-existing issues (not changed here)
`nodeMap/*` and `rams/nodes/nodesAudit.ts` have type errors: `NodeState` and `NodeProfile` are two incompatible node models.
