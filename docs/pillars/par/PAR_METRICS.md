# PAR Metrics and Outcome Accounting

## Monetary and pool state
- totalParSupply
- parCap
- parInCirculation
- stewardshipFund
- humanitarianPool
- parVelocity
- parBurnRate
- parMintRate
- transactionFeesCollected (cumulative fee ledger total)
- demurrageCollected (cumulative demurrage ledger total)

The Humanitarian Pool and Stewardship Fund are distinct accounting destinations.
Their allocation shares are explicit policy inputs, finite, non-negative, and
must sum to 1. Do not silently hard-code an unapproved split.

## Transaction fee
The default PAR transaction fee is 0.0002 (0.02%) of eligible transaction
value. The fee engine routes the full collected fee across the two pools and
checks conservation.

## Demurrage and protected dignity floor
Demurrage is calculated against eligible balance above the holder's protected
Base Stewardship-Dignity Metric (BSDM) reserve. The protected reserve is
aggregated per beneficial person across verified accounts; the identity-aware
policy layer supplies the floor to the deterministic calculator.

The cumulative rate is capped at 100% of eligible excess, never the protected
floor. The retained balance invariant is B_after >= BSDM_protected_balance.
If the opening balance does not exceed the protected floor, the charge is zero.

The engine is separate from `decayReversionEngine`, which models normalized
inactive/stagnant capital indices and does not mutate PAR balances.

## Account classification and fairness
Track governed balance tier and account function independently. Ownership
(private/public) is not a standalone basis for preferential treatment or
penalty. Where balance bands are used, apply rates marginally to the portion
within each band. Publish tier definitions, eligibility rules, and appeals.

## Five-plus-one small/medium transition
- qualifyingSmallMediumAccountCount
- protectedAccountCount
- noticeIssuedCount
- noticeDeliveryConfirmedCount
- noticeGraceAccountCount
- qualifyingActivityAccountCount
- demurrageEligibleAfterGraceCount
- appealedEligibilityDecisionCount
- correctedEligibilityDecisionCount

The canonical transition is five years of protection followed by one full
year of notice/grace. No demurrage is eligible before the sixth anniversary.

## CTA — native PANoRAMic.os fiscal structure
CTA is located under `fiscal/cta`. Track gross citizen-tax revenue actually
collected, policy version, approved pool shares, calculated allocations,
posting references, reversals, and reconciliation status. CTA allocations
are a distinct funding stream, not PAR transaction fees or demurrage.

## Daily claims and contribution awards
Report baseline claims and contribution awards separately for each pool.
Baseline claims are needs-first and not conditioned on labor. Contribution
awards require separately verified evidence and must not displace baseline
claims. Report requested, paid, unpaid, and closing balances. The allocator
uses transparent pro-rata treatment when available funds are insufficient;
it does not create unfunded balances.

## Universal Basic Everything outcomes
Initial service coverage domains: healthcare, housing, nutrition, water and
sanitation, energy, education, mobility, and connectivity. Each coverage
measure is normalized to [0, 1]. Fund balances are not substitutes for measured
service access, quality, continuity, affordability, or geographic equity.

## Ecological and humanitarian performance
Report allocations and verified outcomes for ecological restoration,
infrastructure resilience, and commons regeneration. Record baseline, target,
measured result, geography, time window, provenance, maintenance liability,
and independent review.

The Stewardship Fund reports dignity-floor backing and UBE service coverage
separately. A large balance alone does not establish delivery of a guarantee.
