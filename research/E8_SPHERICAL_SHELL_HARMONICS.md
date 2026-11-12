# E8 spherical shells, harmonic resolution, and root-graph spectrum

This experiment translates three supplied Claude research scripts into a
reproducible PAN research track, using the repository's canonical exact E8
root system rather than an external local path or an unavailable NPZ file.

## Exact shell construction

The E8 lattice is generated as D8 union (D8 + (1/2,...,1/2)). The first
three nonzero squared-norm shells contain:

| Norm squared | Points |
|---:|---:|
| 2 | 240 |
| 4 | 2,160 |
| 6 | 6,720 |

Coordinates are stored doubled as integers. The construction checks shell
cardinality and norm exactly.

## Spherical moments

For a unit vector uniformly distributed on S^7 and even multi-index
(2b_1,...,2b_8), the exact moment is

`prod_i (2b_i-1)!! / prod_{j=0}^{m-1}(8+2j)`, where `m=sum_i b_i`.

The audit checks every all-even coordinate monomial at degrees 2, 4, 6, and 8.
It also verifies all 28 pairwise coordinate sign flips, which generate the
even-sign subgroup of E8. For total degree at most 6, every mixed-parity
monomial has an odd exponent in at least one coordinate and an even exponent
in another, so a pair flip changes its sign and its shell average is zero.
Central symmetry makes every odd-total-degree monomial average zero. Thus
the exact all-even checks plus verified symmetries establish agreement of
all polynomial moments through degree 7. Degree-8 moments differ, so these
shells are spherical 7-designs but not 8-designs.

## Polynomial resolution

On a fixed-radius sphere, restrictions of polynomials of degree <= l are
spanned by homogeneous monomials of degrees l and l-1, because multiplication
by the squared radius identifies degrees differing by two. The audit uses
the same construction as the supplied Claude script.

Numerical SVD is applied to deterministic samples of at most 500 shell
points. A full expected rank in the sampled matrix certifies that the full
shell evaluation matrix has at least that rank; a deficient sampled rank is
only a lower bound. The rank threshold is explicitly reported. This is a
numerical diagnostic, not an exact rational-rank proof.

## E8 root graph

The graph has 240 vertices and an edge when two roots have inner product 1.
Its Laplacian spectrum is checked numerically against exact integer
multiplicities. The Gegenbauer prediction uses `C_l^3` on S^7 at cosine
1/2. The observed multiplicities are 1, 8, 35, 112, 84; the first four
match the S^7 harmonic dimensions for degrees 0 through 3. The final 84 is
the residual dimension after restricting degrees <=3 to 240 root points.
The degree-4 full harmonic dimension is 294, so this finite graph does not
resolve all degree-4 harmonics.

## Relationship to Leech / Moonshine

This is an E8-side geometric diagnostic, not a construction of the Leech
lattice or a VOA. Its value is methodological: the same exact moment and
harmonic-resolution questions can later be asked of the 196,560 Leech
minimal vectors, while the Leech theta series and lattice VOA character
remain separate algebraic/spectral layers. No Monster action, orbifold, or
quantum-gravity duality is inferred here.

## Reproduction

`python -m unittest tests.test_e8_spherical_shell_audit -v`
`python experiments/e8_spherical_shell_audit.py`
