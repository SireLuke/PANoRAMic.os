# Citizen Tax Allocation (CTA)

CTA is a native fiscal subsystem of PANoRAMic.os, located at
`fiscal/cta`. It calculates governed allocations from collected citizen-tax
revenue to the two shared PAR public-benefit pools:

1. Humanitarian / Ecological Pool
2. Stewardship / Dignity Pool

CTA is a fiscal allocation source distinct from PAR transaction fees and
demurrage. It does not mint PAR, set PAR conversion rates, debit wallets, or
post ledger entries. Approved allocations are handed to PAR's accounting
boundary for idempotent posting and reconciliation.

## Separation of responsibilities

- PANoRAMic.os hosts CTA policy, governance, fiscal records, versioning, and audit.
- CTA calculates allocations from actually collected citizen-tax revenue.
- PAR records and settles pool credits and all monetary movements.
- RAMS acts upon PAR through governed resource/scarcity inputs and resource
  management operations; it does not silently rewrite PAR balances or CTA policy.

## Accounting requirements

Every CTA period must preserve gross collected revenue, policy version,
approved pool shares, calculated allocations, posting references, reversals,
and reconciliation status. Uncollected or disputed tax is not allocatable
revenue. Never count a CTA allocation again as a PAR transaction fee or
demurrage receipt.

The initial engine is deterministic calculation only. Tax bases, rates,
exemptions, collection authority, jurisdiction, allocation percentages,
appeals, and production posting require explicit governance and legal review.
