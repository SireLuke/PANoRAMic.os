# PAR Demurrage, Pool Routing, and UBE Policy

## Architecture boundary
PAR is the economic circulation and accounting layer. It maintains two
separate destinations:
1. Humanitarian Pool — humanitarian infrastructure, ecological restoration,
   and commons regeneration.
2. Stewardship Fund / Dignity Pool — the universal dignity baseline and
   Universal Basic Everything (UBE) support.

Their allocation shares are explicit policy inputs and must sum to 100%.

## Transaction micro-levy
The canonical fee is 0.02%:
\[
F = T \times 0.0002
\]
where T is eligible transaction value. The complete fee is allocated between
the two pools. A production ledger must record transaction identity, fee,
policy version, both allocations, and an idempotency key to prevent duplicate
collection.

## Compounding demurrage
For eligible opening balance B, initial demurrage rate r, compounding factor g,
and completed cycle n:
\[
R_n = \min\left(1,\ r(1+g)^{n-1}\right), \quad n\geq1
\]
\[
D_n = B\left(R_n-R_{n-1}\right), \quad R_0=0
\]
R_n is cumulative percentage of the opening balance reverted by cycle n;
D_n is the incremental amount charged in that cycle. The cumulative rate is
capped at 1 (100%), so total demurrage cannot exceed the opening balance. At
the cap, the entire eligible opening balance has been routed to the two pools.

For humanitarian share s_H and stewardship share s_S:
\[
A_H=D_n s_H,\qquad A_S=D_n s_S,\qquad s_H+s_S=1
\]

The cycle counter and prior cumulative rate must be ledger-derived or persisted
immutably. Do not pass a newly reduced wallet balance as the opening balance
on every invocation: that changes the schedule and can double-count. The
engine is a deterministic calculator; eligibility, custody, dispute, hardship,
notice, and appeal rules require separate governance and legal review.

## Keep inactivity decay separate
decayReversionEngine models normalized inactive/stagnant capital indices and
explicitly does not touch PAR wallet balances. demurrageEngine calculates the
compounding wallet-balance schedule. Keep these mechanisms distinct.

## UBE service outcomes
The Stewardship Fund supports a universal basic floor across healthcare,
housing, nutrition, water and sanitation, energy, education, mobility, and
connectivity. Measure service coverage, quality, continuity, geographic equity,
and accessibility independently of monetary balances.

The Humanitarian Pool supports ecological restoration, resilient infrastructure,
and commons regeneration. Track projects against independently verifiable
baselines, outcomes, provenance, and maintenance obligations.

## Production safeguards
- Pool shares must be finite, non-negative, and sum to 1.
- Use deterministic cycle IDs and idempotent ledger postings.
- Never let cumulative demurrage exceed 100% of opening balance.
- Preserve auditable opening balance and cycle-by-cycle rate history.
- Provide notice, correction, hardship, dispute, and appeal mechanisms.
- Keep UBE access independent of an individual's PAR balance or labor status.
- Do not treat modelled impact indices as verified real-world outcomes.
