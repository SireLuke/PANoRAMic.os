# Stewardship Fund Specification

The Stewardship Fund (SF) provides ethical, transparent compensation for the system steward.

---

## Principles

- voluntary contributions only  
- no public funds  
- no humanitarian pool funds  
- no tax allotment funds  
- no decay reversion funds  
- capped annual income  
- full audit transparency  
- steward cannot influence contributions  

---

## Annual Cap

The steward may receive at most:

`median_national_income × 1.2`

This ensures comfort without excess.

---

## API

- `createStewardshipFund(stewardId, annualCap)`
- `addContribution(fund, contribution)`
- `canPaySteward(fund, amount)`
- `applyStewardPayment(fund, amount)`
- `auditStewardship(contributions)`
