# Leech lattice VOA character precursor

The Leech lattice VOA has graded character

`ch(V_Lambda)=Theta_Lambda(q)/eta(q)^24`.

This module computes the oscillator factor exactly as
`prod_{n>=1}(1-q^n)^(-24)`, multiplies it by the Leech theta-series
reference, and verifies the initial graded dimensions:

- weight 0: 1
- weight 1: 24
- weight 2: 196884
- weight 3: 21493760

This is a genuine Leech lattice VOA character calculation, but it is not yet
the Frenkel-Lepowsky-Meurman Moonshine module. The latter requires the
`Z2` fixed-point subalgebra `V_Lambda^+`, the twisted module, and the
appropriate extension. The fact that the weight-one dimension is 24 in
`V_Lambda` and zero in `V^natural` is a useful audit target, not permission
to obtain the orbifold character by simply subtracting 24. Twisted-sector
graded contributions must be derived explicitly.

No Monster action or McKay-Thompson series is constructed by this precursor.
