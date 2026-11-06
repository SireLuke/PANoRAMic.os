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

## Compounding demurrage
Demurrage is a compounding percentage schedule applied to an eligible wallet's
opening balance. The cumulative rate is capped at 100%. Each cycle charges only
the increase since the preceding cumulative rate, so the same portion cannot
be charged twice. At 100%, the full eligible opening balance is routed to the
Humanitarian Pool and Stewardship Fund using configured shares.

The demurrage engine is separate from decayReversionEngine, which models
normalized inactive/stagnant capital indices and does not mutate PAR balances.

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
