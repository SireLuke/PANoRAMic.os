# harmIndex — Panitarian Global Harm Scoring

The **harmIndex** subsystem computes the global harm score for PAN♾RAMic.os.  
It merges all 12 pillars of civilization into a single normalized value used by:

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

- `total` — combined harm across all pillars  
- `normalized` — scaled to 0–1 range (total / 100)

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
