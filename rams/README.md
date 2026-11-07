# PANoRAMic.os RAMS

RAMS acts upon PAR through governed resource/scarcity inputs, audit findings,
and resource-management operations. It is not PAR's monetary ledger and does
not silently rewrite wallet balances, transaction history, conversion
settlements, or CTA fiscal records.

Core RAMS parameters:
- Market-value MSRP cap: 15% of market value
- Boot-time PAR cap: population * 1.35 * RSDV (RSDV is 0.65–1.00)
- PAR dynamic cap: min(population * 1.35, resourceParValue * 0.90)
- Stability and scarcity signals are normalized to 0..1
- Audit checks detect over-issuance, collapse pressure, and misallocation

Primary audits:
- PAR supply, circulation, valuation inputs, and cap checks
- infrastructure stress checks
- ecological carrying capacity checks
- workforce and node resilience checks
- market volatility and scarcity checks
- public-benefit pool allocation and resource-outcome reconciliation

## RAMS / PAR interface boundary

RAMS may publish versioned resource and scarcity measurements, constraints,
risk signals, and authorized allocation recommendations for PAR to consume.
PAR validates those inputs against its own policy and accounting rules before
any monetary effect. Each accepted input must retain provenance, timestamp,
model/version, confidence or quality metadata, and an audit reference.

RAMS does not unilaterally set PAR conversion rates, alter settled balances,
change transaction fees, or change CTA allocation percentages.

## Public-benefit pool feedback

RAMS can measure ecological/resource outcomes funded by the Humanitarian /
Ecological Pool and report verified changes to resource conditions. Those
measurements may inform PAR's governed scarcity/reference inputs. This is a
measured feedback relationship, not an assumption that every funded project
immediately reduces scarcity.

CTA is a native PANoRAMic.os fiscal subsystem under `fiscal/cta`. CTA
calculates allocations from collected citizen-tax revenue; PAR records and
settles the resulting pool credits. RAMS audits resource and outcome evidence
but does not collect or reallocate CTA revenue.
