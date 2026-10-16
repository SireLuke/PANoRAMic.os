# harmIndex — Panitarian Global Harm Scoring

The **harmIndex** subsystem computes the global harm score for PAN♾RAMic.os.  
It scores six aggregated harm domains derived from the 12 civilization pillars, then returns a total and `normalized = total / 100` used by:

- audits
- dashboard
- world stability
- synthesis
- engine pipeline

This module does **not** collect data itself.  
It receives pre‑computed pillar values from other core subsystems.

---

## Components

### `compute.ts`
Merges raw pillar values into a single structure:

- environmental  
- humanRights  
- trafficking  
- migration  
- governance  
- supplyChain  

### `score.ts`
Calculates:

- `total` — combined harm across the six scored domains  
- `normalized` — `total / 100` (not clamped to 0–1)

### `flags.ts`
Provides risk tiers:

- `severe` — total > 70  
- `moderate` — 40–70  
- `low` — ≤ 40

### `index.ts`
Exports the full harmIndex API:

```ts
{
  compute,
  score,
  flags
}
