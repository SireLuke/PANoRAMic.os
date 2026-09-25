# Civilization — 12 Pillars Specification

The **civilization** subsystem defines the 12 Pillars of Civilization used across PAN♾RAMic.os.

It provides a unified reference for:

- audits  
- harmIndex  
- dashboard  
- world model  
- stability engine  
- synthesis  

This module contains no logic — only definitions.

---

## Pillar Groups

### Environmental (5)
- pollution  
- emissions  
- waste  
- waterUse  
- landUse  

### Human Rights (4)
- violations  
- forcedMigration  
- trafficking  
- childTrafficking  

### Governance (3)
- corruption  
- laborViolations  
- governanceFailures  

---

## API

### `civilization()`
Returns:

```ts
{
  pillars: CivilizationPillars,
  count: 12
}
