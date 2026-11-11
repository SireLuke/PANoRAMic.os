# Leech Z2 orbifold: exact graded-character sector audit

## Mathematical construction being audited

Let theta be the canonical lift of lattice negation on the Leech lattice VOA.
The moonshine module has vector-space decomposition

`V^natural = V_Lambda^+ + V_Lambda^{T,+}`,

where the first term is the theta-fixed subspace of the untwisted Leech VOA
and the second is the theta-fixed subspace of its unique theta-twisted module.

For the untwisted sector, the exact character and theta trace are

`Z_V(q) = q^-1 Theta_Lambda(q) prod_{n>=1}(1-q^n)^-24`

and

`Z_{V,theta}(q) = q^-1 prod_{n>=1}(1+q^n)^-24`.

The fixed-sector character is their average. This correctly projects out
the 24 weight-one Heisenberg currents.

The twisted module has ground conformal weight 3/2 and a 2^12-dimensional
ground space. Its full oscillator character is

`2^12 q^(1/2) prod_{m>=0}(1-q^(m+1/2))^-24`.

With the canonical involution acting by -1 on the twisted ground space and
by -1 on each half-integer oscillator, the theta-fixed sector is the
odd-oscillator projection. In t=q^(1/2), its integer-weight dimensions are
computed exactly as

`2^11 [t^(2h-3)] ( prod_{r odd>=1}(1-t^r)^-24 - prod_{r odd>=1}(1+t^r)^-24 )`.

## Results through weight four

| Conformal weight | Untwisted fixed | Twisted fixed | Total |
|---:|---:|---:|---:|
| 0 | 1 | 0 | 1 |
| 1 | 0 | 0 | 0 |
| 2 | 98,580 | 98,304 | 196,884 |
| 3 | 10,745,856 | 10,747,904 | 21,493,760 |
| 4 | 413,443,380 | 450,856,590 | 864,299,970 |

The totals match the first graded dimensions of J(q)=j(q)-744.
The weight-two equality is now derived by separately projecting both sectors:
98,580 retained untwisted states plus 98,304 twisted states.

## Evidence boundary

This is an exact finite q-series calculation of graded dimensions and parity
projections. It does not construct the vertex operators/intertwining operators
that make the direct sum into a VOA, prove locality and associativity of that
extension, or construct the Monster action. Those require additional algebraic
data and independent checks. Matching several graded dimensions is not a
proof of the full FLM construction.

## Reproduction

`python -m unittest tests.test_leech_z2_orbifold_character -v`
`python experiments/moonshine_sierpinski/leech_z2_orbifold_character.py`
