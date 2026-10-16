# harmIndex Specification

The **harmIndex** subsystem defines how PAN♾RAMic.os computes the global harm score across all 12 pillars of civilization.  
It provides a unified metric used by the engine, dashboard, audits, and world stability systems.

---

## Purpose

The harmIndex:

- merges all pillar values into a single structure  
- computes a global harm score  
- normalizes the score for synthesis and dashboard use  
- provides risk-tier flags for stability and governance logic  

It does **not** gather data itself.  
It receives pre-processed values from other core subsystems.

---

## Inputs

The `computeHarm()` function expects a `data` object containing:

### Environmental
- `environmental` — pollution, emissions, waste, water, land use

### Humanitarian
- `humanRights` — violations, abuses  
- `trafficking` — forced labor, exploitation, child trafficking  
- `migration` — displacement, refugees, asylum pressure

### Governance
- `governance` — corruption, governance failures  
- `supplyChain` — labor violations, exploitation, ESG harm

All values are expected to be **0–100** scaled indicators.

---

## Outputs

### `computeHarm(data)`
Returns a merged structure:

```ts
{
  environmental: number,
  humanRights: number,
  trafficking: number,
  migration: number,
  governance: number,
  supplyChain: number
}
```

`computeHarm()` currently passes these six domain totals through (defaulting missing values to `0`). It does not itself average the 12 leaf pillars listed in `core/civilization/spec.md`.

### `scoreHarm(impact)`

Sums the six domain totals and returns:

```ts
{
  total: number,          // sum of the six domains
  normalized: number      // total / 100
}
```

`normalized` follows the implementation (`total / 100`). It is not hard-clamped to `0..1`; a full 100 on every domain yields `6`.

### `harmFlags(score)`

Risk tiers from `score.total`:

- `severe` — total > 70  
- `moderate` — 40 < total ≤ 70  
- `low` — total ≤ 40

