# PAR / RAMS / CTA Public-Benefit Circulation Architecture

## Purpose

This document defines the boundaries and data flow among PANoRAMic.os, CTA,
PAR, RAMS, and the Humanitarian/Ecological and Stewardship/Dignity pools.

## System responsibilities

- **PANoRAMic.os:** Governing architecture, policy versioning, fiscal
  structures, oversight, and public audit.
- **CTA:** Native PANoRAMic.os fiscal subsystem at `fiscal/cta`. It calculates
  allocations from actually collected citizen-tax revenue.
- **PAR:** Economic circulation, reference valuation, conversion, transaction
  settlement, monetary accounting, demurrage, and pool-credit posting.
- **RAMS:** Resource audit and management. It acts upon PAR through governed,
  versioned scarcity/resource measurements, constraints, and authorized
  resource-management operations. PAR validates inputs before monetary effect.

No subsystem silently mutates another subsystem's ledger or policy.

## Distinct funding streams

Both pools can receive independently identified inflows:
- PAR transaction fee (default 0.02%, 0.0002).
- Eligible demurrage collected only above the protected BSDM reserve.
- CTA allocation from collected citizen-tax revenue.
- Approved grants, donations, and other contributions.

Every posting records source type, source transaction/period, policy version,
amount, destination pool, timestamp, and idempotency key. Reversals retain
links to original postings. Never count an allocation twice.

## Pool 1: Humanitarian / Ecological

Supports humanitarian response, ecological restoration, conservation,
infrastructure resilience, and commons regeneration.

The pool may provide a governed daily baseline claim and contribution-
responsive additional awards for verified humanitarian/ecological work.
Verification must recognize outcomes and diverse forms of contribution,
rather than relying only on hours or popularity.

## Pool 2: Stewardship / Dignity

Supports the unconditional UBE baseline and needs-first essential support.
The baseline is not earned, and access is not conditional on employment,
labor, or PAR balance. Additional governed support may recognize verified
stewardship that improves access, dignity, and community resilience, but may
not displace baseline needs.

## Claims and zero balances

Pools are revolving accounts. A pool or an individual's spendable account may
reach zero; the system does not promise a permanently positive balance.
Daily claim cycles and independent funding streams create opportunities for
replenishment, subject to actual available resources.

For each pool, baseline claims are allocated before contribution awards.
When baseline requests exceed available funds, the reference allocator uses
pro-rata distribution and reports unpaid claims. Contribution awards use only
the remaining funded balance. No unfunded PAR is created.

Daily baseline amounts, eligible claimants, contribution evidence, award
ceilings, and emergency exceptions require explicit governance. The provided
claim allocator is deterministic math only; it does not verify identity,
citizenship, work, eligibility, or impact.

## BSDM and demurrage

The Base Stewardship-Dignity Metric defines the protected personal reserve
needed for the essential UBE basket over the governed period. The reserve is
calculated per beneficial person across verified accounts. Demurrage applies
only to the eligible excess above that reserve, with a maximum cumulative
reversion of 100% of the excess. The retained balance must never fall below
the protected floor.

The five-year small/medium protection plus one-year notice transition remains
an eligibility rule separate from the demurrage calculator. Account tiers and
account functions are distinct dimensions. Private/public ownership alone
does not confer a privilege or penalty; comparable needs and functions receive
comparable treatment.

## PAR conversion records

PAR separates reference valuation, continuous market observation, and
settlement conversion. The proposed design observes markets continuously and
publishes periodic, versioned reference snapshots. Each settlement records the
snapshot and rule used. Cadence, source weighting, outlier controls, and
rounding require governance.

## RAMS feedback

RAMS audits resource conditions and outcomes from funded projects. Verified
changes may inform future governed PAR scarcity/reference inputs. This is a
measured feedback loop, not an assumption that every funded activity
immediately reduces scarcity.

## Required audit metrics

Report by pool and by funding source:
- opening/closing balance and reserve target
- gross inflows and outflows
- CTA collected revenue and allocations
- transaction fees and demurrage allocations
- baseline claims requested, paid, and unpaid
- contribution awards requested, paid, and unpaid
- emergency disbursements and authorizations
- project outcomes, provenance, and independent verification
- reconciliation exceptions and reversals

## Implementation boundary

The current TypeScript engines are deterministic calculators. Production
integration still requires identity-aware aggregation, governed policy values,
verification, legal review, custody/ledger integration, idempotency,
reconciliation, notice/appeal processes, and independent audit. No claim of
production readiness is made by these reference modules.
