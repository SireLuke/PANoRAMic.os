# Migration Specification

The **migration** subsystem models displacement and refugee pressure using public humanitarian indicators.

---

## Purpose

- unify migration stress indicators  
- compute migration harm  
- provide scoring and flags for harmIndex  

---

## Inputs

Expected fields:

- displaced  
- refugees  
- asylumSeekers  
- conflictDriven  

Values are 0–100 scaled indicators.

---

## Outputs

### `computeMigration(data)`
Returns migration impact.

### `scoreMigration(impact)`
Returns:
- total  
- normalized  

### `migrationFlags(score)`
Returns:
- severe  
- moderate  
- low  

---

## Notes

- uses UNHCR, IOM, UNICEF  
- public data only  
