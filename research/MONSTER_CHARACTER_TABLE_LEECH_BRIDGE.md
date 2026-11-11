# Monster character table and Leech involution bridge

## Scope

This audit uses GAP's Character Table Library (CTblLib) as a versioned,
external source of the Monster ordinary character table. It does not attempt
to construct the Monster group or its 194 irreducible representations from
scratch. It checks the stored table's internal character-theoretic
consistency exactly, then checks selected graded traces against published
McKay-Thompson coefficients.

## Part A — full character-table orthogonality

For the Monster ordinary character table, the audit requires 194 conjugacy
classes and 194 irreducible characters and checks all 194^2 row inner products:

For irreducible characters `chi_i` and `chi_j`, the row identity is:

It also checks all 194^2 column orthogonality identities exactly:

`sum_chi chi(g) conjugate(chi(h)) = 0` for distinct classes, and
`|C_M(g)|` when the classes coincide.

The GAP computation uses exact cyclotomic arithmetic, not floating-point
approximations.

## Part B — graded traces on 2A, 2B and 3A

The existing Leech orbifold calculation supplies the graded multiplicities
of the selected Monster irreducibles. The GAP table supplies their character
values on the indicated conjugacy classes. The trace is the integer sum
`sum_i multiplicity_i(q^n) * chi_i(g)`.

Selected degrees:
1, 196883, 21296876, 842609326, 19360062527 (chi_1, chi_2, chi_3,
chi_4, chi_6; chi_5 is intentionally skipped in the q^4 Serre decomposition).

Expected first four coefficients:

| Class | q^1 | q^2 | q^3 | q^4 |
|---|---:|---:|---:|---:|
| 2A | 4,372 | 96,256 | 1,240,002 | 10,698,752 |
| 2B | 276 | -2,048 | 11,202 | -49,152 |
| 3A | 783 | 8,672 | 65,367 | 371,520 |

These are graded traces computed from published ordinary-character data and
the already audited low-degree multiplicities. They are not traces from
explicitly constructed matrices acting on the VOA.

## Part C — Leech automorphisms and Monster involutions

The Leech lattice automorphism group is Co_0, with Co_0 = 2.Co_1.
The Monster involution centralizers have two distinct structures:

- 2A: C_M(2A) is 2.B, where B is the Baby Monster.
- 2B: C_M(2B) is 2^(1+24).Co_1.

The audit checks the exact centralizer orders from the Monster table:
`|C_M(2A)| = 2 |B|` and
`|C_M(2B)| = 2^25 |Co_1|`.
It also records `|Co_0| = 2 |Co_1|`.

This is the important structural match: the Leech/Conway symmetry sits in
the 2B centralizer, not the 2A centralizer. The order identities corroborate
the quotient-size relationship but do not by themselves prove the extension
structure or construct the Monster action. Those structural identifications
are established in the group/VOA literature.

## Reproducibility

Requires GAP and CTblLib. On Ubuntu CI:

`sudo apt-get update`
`sudo apt-get install -y gap-core gap-character-tables`
`gap -q -b -r scripts/monster_character_table_audit.g`

Sources:
- Breuer, Magaard, Wilson, *Verification of the conjugacy classes and ordinary character table of the Monster*, Journal of Algebra 703 (2026), DOI 10.1016/j.jalgebra.2025.09.034.
- Breuer, Magaard, Wilson, *Some steps in the verification of the ordinary character table of the Monster* (GAP session protocol).
- Frenkel, Lepowsky, Meurman, *Vertex Operator Algebras and the Monster*.
- GAP Character Table Library documentation.
