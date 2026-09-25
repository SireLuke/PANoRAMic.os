# Dashboard Specification

The **dashboard** subsystem produces the data model for the Humanitarian Life‑Feed Earth Dashboard.

---

## Purpose

- unify world health indicators  
- expose environmental, humanitarian, governance, and stability metrics  
- provide normalized values for UI rendering  
- feed synthesis and world modeling  

---

## Inputs

Receives:

- harmIndex results  
- audits  
- stability engine outputs  
- renewable grid metrics  
- population model  

---

## Outputs

### World Health
- global harm score  
- environmental stress  
- humanitarian pressure  
- governance integrity  
- renewable infrastructure health  

### Stability
- world stability score  
- catastrophe risk  
- dampening modifiers  

### Humanitarian
- trafficking  
- migration  
- human rights  

---

## Notes

This subsystem does not compute harm — it aggregates and formats it.
