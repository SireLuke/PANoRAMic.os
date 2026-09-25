# Audits Specification

The **audits** subsystem collects and normalizes public‑dataset indicators across the 12 pillars of civilization.  
It does not gather private data or perform surveillance.  
It provides structured inputs for harmIndex, dashboard, and world stability.

---

## Purpose

- unify public indicators into a consistent structure  
- provide adapters for environmental, humanitarian, and governance datasets  
- compute impact values  
- generate audit flags  
- feed harmIndex and synthesis  

---

## Inputs

Adapters provide raw values from:

### Environmental
- pollution  
- emissions  
- waste  
- water  
- land use  

### Humanitarian
- human rights violations  
- trafficking  
- child trafficking  
- forced migration  

### Governance
- corruption  
- governance failures  
- labor violations  

---

## Outputs

### `computeImpact(data)`
Returns merged pillar values.

### `score(impact)`
Returns:
- total harm  
- normalized harm  

### `flags(score)`
Returns:
- severe  
- moderate  
- low  

---

## Notes

- public datasets only  
- no personal data  
- no surveillance  
- transparent and humanitarian‑aligned  
