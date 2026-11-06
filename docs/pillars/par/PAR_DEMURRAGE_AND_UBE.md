# PAR Demurrage, Pool Routing, and UBE Policy

## Architecture boundary

PANoRAMic.os is the governing architecture for policy, fiscal structures,
governance, and public audit. Citizen Tax Allocation (CTA) is a native
PANoRAMic.os subsystem under `fiscal/cta`.

PAR is the economic circulation, valuation, conversion, transaction, and
monetary-accounting layer. RAMS acts upon PAR through governed resource,
scarcity, stability, and allocation inputs, and through resource-management
operations. RAMS does not silently mutate PAR balances, override PAR ledger
entries, or unilaterally change fiscal policy.

The two shared public-benefit destinations are:
1. Humanitarian / Ecological Pool — humanitarian response, ecological
   restoration, infrastructure resilience, and commons regeneration.
2. Stewardship / Dignity Pool — UBE baseline support and essential-needs
   continuity.

Pool shares are explicit, versioned policy inputs. Each funding source keeps
its own source identity and accounting trail.

## Independent funding streams

The pools may receive funds from distinct, non-interchangeable streams:
- PAR transaction micro-levy: canonical default 0.02% (0.0002) of eligible
  transaction value.
- Eligible PAR demurrage: only value above the protected personal dignity floor.
- Citizen Tax Allocation (CTA): a native PANoRAMic.os fiscal allocation from
  actually collected citizen-tax revenue.
- Grants, donations, and other approved public-benefit contributions.

Do not merge source totals or double-count an allocation. CTA is not a PAR
transaction fee and does not itself mint PAR. CTA calculates allocations;
PAR records and settles pool credits through its accounting boundary.

## Transaction micro-levy

For eligible transaction value T:
\[
F = T \times 0.0002
\]
The complete fee is allocated between the two pools. A production ledger must
record transaction identity, fee, policy version, both allocations, and an
idempotency key to prevent duplicate collection.

## Demurrage and the Base Stewardship-Dignity Metric

The Base Stewardship-Dignity Metric (BSDM) defines the protected PAR-value
reserve required to support the holder's essential UBE needs over the governed
accounting period. It is derived from the approved essential-needs basket and
its current, auditable costs, not from a fixed arbitrary token amount.

The protected reserve is calculated per beneficial person across their
verified accounts, not once per wallet. The identity-aware policy layer
aggregates the person's eligible reserve and supplies the resulting protected
balance floor to the demurrage calculator. Additional organization-level
operating reserves may be recognized only for verified essential-service
obligations, under ownership-neutral criteria and separate governance.

For opening balance B, protected floor P, and eligible excess E:
\[
E = \max(0, B-P)
\]
For initial rate r, compounding factor g, and completed cycle n:
\[
R_n = \min\left(1,\ r(1+g)^{n-1}\right), \quad n\geq1
\]
\[
D_n = E\left(R_n-R_{n-1}\right), \quad R_0=0
\]
Only the eligible excess is subject to the cumulative schedule. The 100% cap
can revert at most E; it can never consume P. The retained balance must satisfy:
\[
B_{after} \geq P
\]
The incremental charge is routed to the two pools according to the approved
shares. If B is at or below P, demurrage is zero.

The calculator accepts a protected floor as an input. Production integration
must calculate that floor across wallets using privacy-preserving identity
controls, prevent duplicate person-level coverage, preserve correction and
appeal rights, and never treat the wallet-level input as proof of identity.

## Compounding demurrage pool routing

For humanitarian share s_H and stewardship share s_S:
\[
A_H=D_n s_H,\qquad A_S=D_n s_S,\qquad s_H+s_S=1
\]
The cycle counter and prior cumulative rate must be ledger-derived or persisted
immutably. Do not pass a newly reduced wallet balance as the opening balance
on every invocation: that changes the schedule and can double-count. The
engine is a deterministic calculator; eligibility, custody, dispute, hardship,
notice, and appeal rules require separate governance and legal review.

## Account classification: ownership-neutral treatment

Account policy uses two independent dimensions:

- Balance tier: micro, small, medium, large, or other explicitly governed
  bands. Demurrage thresholds are marginal: crossing a band applies the next
  rate only to the balance portion within that band, not retroactively to the
  entire balance.
- Account function: household/individual, cooperative, enterprise,
  essential-service operator, public institution, or other governed purpose.

Private/public ownership is recorded for accountability but is not, by itself,
a basis for preferential treatment or penalty. Equivalent balances, activity,
verified needs, and economic functions receive equivalent treatment.
Verified essential-needs and service-delivery reserves may be protected under
the same evidence-based criteria regardless of ownership. Avoid arbitrary
thresholds until public governance defines and reviews them.

## Five years plus one year: small/medium protection

Qualifying small and medium accounts receive five full years of demurrage
protection. At the fifth anniversary, the holder receives notice that continued
protection from inactivity-based demurrage requires qualifying account
activity. Notice explains the activity rule, consequences, effective date,
and correction and appeal routes.

A full one-year grace interval follows notice. No demurrage may be charged
during that interval. The earliest demurrage eligibility date is the sixth
account anniversary. At or after that date, an account that remains inactive
under the published qualifying-activity rule may enter the existing schedule.
Qualifying activity maintains protection while the account meets the rule.

This is an eligibility transition, not an account freeze or loss of UBE.
Account operation and access to UBE must not be disabled because of inactivity
or PAR balance. The eligibility evaluator remains separate from the
compounding calculator. Account-size bands, qualifying activity, account-age
origin, identity verification, wallet aggregation, notice delivery, hardship,
and appeal workflows require governance before production use.

## Daily pool claims and contribution-responsive increases

The pools are revolving public-benefit accounts. A balance may reach zero;
there is no promise that every account always has a positive balance.
Replenishment is expected through independent, recorded inflows, including
PAR transaction fees, eligible demurrage, CTA, and approved contributions.

Daily baseline claims are separate from contribution-based awards:
- The Stewardship / Dignity Pool supports an unconditional daily baseline and
  UBE needs-first assistance. Baseline access is not earned through labor and
  is not conditional on PAR balance or employment.
- The Humanitarian / Ecological Pool supports its governed daily baseline
  claim and additional claims for verified humanitarian and ecological work.
- Verified contributions may increase claims from the relevant pool. The
  contribution mechanism must recognize outcomes and different forms of
  service, not merely hours, popularity, or a single activity leaderboard.
- Emergency assistance is separately accounted for and may use governed
  emergency authorization.

For each pool, baseline claims take priority over contribution awards. If
available funds cannot meet all baseline claims, the shortfall must be reported
and allocated under a transparent, equitable rule (the reference allocator
uses pro-rata distribution). Contribution awards are then allocated from
remaining available funds, also with transparent rules. No engine may create
unfunded claims or imply guaranteed payment beyond available resources.

The pool claim calculator is deterministic allocation logic only. It does not
verify work, decide eligibility, establish daily allotment values, or post
payments. Those require separately governed services and auditable evidence.

## Keep inactivity decay separate

`decayReversionEngine` models normalized inactive/stagnant capital indices
and explicitly does not touch PAR wallet balances. `demurrageEngine` calculates
the compounding wallet-balance schedule above. Keep these mechanisms distinct.

## UBE service outcomes

The Stewardship / Dignity Pool supports a universal basic floor across
healthcare, housing, nutrition, water and sanitation, energy, education,
mobility, and connectivity. Measure service coverage, quality, continuity,
geographic equity, and accessibility independently of monetary balances.

The Humanitarian / Ecological Pool supports ecological restoration, resilient
infrastructure, and commons regeneration. Track projects against independently
verifiable baselines, outcomes, provenance, and maintenance obligations.

## Production safeguards

- Pool shares must be finite, non-negative, and sum to 1.
- Use deterministic cycle IDs and idempotent ledger postings.
- Never let cumulative demurrage exceed 100% of the eligible excess balance.
- Never allow demurrage to cross the BSDM-protected reserve.
- Preserve auditable opening balance and cycle-by-cycle rate history.
- Keep CTA, transaction-fee, demurrage, and grant inflows separately identified.
- Provide notice, correction, hardship, dispute, and appeal mechanisms.
- Keep UBE access independent of an individual's PAR balance or labor status.
- Do not treat modelled impact indices as verified real-world outcomes.
- Publish pool inflows, outflows, available balances, reserve targets,
  outstanding claims, and replenishment rates.
