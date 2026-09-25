# Trafficking Specification

The **trafficking** subsystem models exploitation indicators from public humanitarian datasets.

---

## Purpose

- represent trafficking harm  
- unify forced labor, exploitation, child trafficking, and migration abuse  
- provide scoring and flags for harmIndex  

---

## Inputs

Expected fields:

- forcedLabor  
- sexualExploitation  
- childTrafficking  
- migrationAbuse  

Values are 0–100 scaled indicators.

---

## Outputs

### `computeTrafficking(data)`
Returns normalized trafficking impact.

### `scoreTrafficking(impact)`
Returns:
- total  
- normalized  

### `traffickingFlags(score)`
Returns:
- severe  
- moderate  
- low  

---

## Notes

- uses UNODC, UNICEF, Global Slavery Index  
- public data only  
- no personal tracking  
