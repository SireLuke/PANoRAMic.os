# Leech minimal shell moments and weight-two VOA grading

## Directional moment audit

The 196,560 minimal vectors are stored as integral coordinate vectors of
squared norm 32; dividing by sqrt(8) gives Leech lattice vectors of squared
norm 4, and dividing by sqrt(32) gives unit vectors on S^23.

For a fixed integer direction y, the audit computes exact rational moments

`average_v ((v dot y)^2m / (32 ||y||^2)^m)`

and compares them with the uniform S^23 moment

`(2m-1)!! / [24*26*...*(24+2m-2)]`.

Four fixed directions (coordinate axis, all-ones, alternating signs, and
one fixed integer probe) agree exactly through degree 10 and differ at
degree 12. Odd moments vanish by central symmetry. This is consistent with
the well-known 11-design behavior of the Leech minimal shell, but these four
directions alone do not constitute a complete proof of a spherical
11-design. A complete certificate would require all harmonic components or
a rigorous invariant-theoretic reduction.

## Weight-two Leech lattice VOA grading

The Leech lattice VOA character is `Theta_Lambda/eta^24`. At weight two,
the exact q-series separates into:

- 196,560 momentum states, one for each norm-four Leech lattice vector;
- 324 oscillator-only states from the rank-24 Heisenberg Fock factor.

Thus `dim(V_Lambda[2]) = 196560 + 324 = 196884`, matching the q^1
coefficient of `J(q)=j(q)-744`.

This is a striking arithmetic bridge, but it must not be overinterpreted:
the equality of dimensions does not construct the Moonshine module
`V^natural`, the `Z2` orbifold extension, or the Monster representation.
The decomposition `196884 = 1 + 196883` belongs to the Monster-module
representation-theoretic story and is not the same as the Leech VOA
momentum/oscillator split.

## Reproduction

`python -m unittest tests.test_leech_shell_design_and_voa_weight_two -v`
`python experiments/moonshine_sierpinski/leech_shell_design_moments.py`
`python experiments/moonshine_sierpinski/leech_voa_weight_two.py`
