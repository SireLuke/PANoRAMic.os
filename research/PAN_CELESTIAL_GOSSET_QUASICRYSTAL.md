# PAN Celestial–Gosset / E8 Quasicrystal Research Track — v0

**Status:** isolated research branch. No production wiring. This is a reproducible
mathematical baseline, not a new physical theory.

## 1. Celestial-amplitude reference

The starting reference is Sabrina Pasterski, *Lectures on Celestial Amplitudes*
(2021), especially the celestial primary dictionary, Mellin transform and
conformally soft limits. In four-dimensional massless scattering, a celestial
primary is labelled by conformal dimension \(\Delta\), celestial spin \(J\),
and a point \(z,\bar z\) on the celestial sphere. For radiative massless
primaries, \(J\) is identified with the helicity, subject to the chosen
incoming/outgoing and spin convention.

The two-dimensional weights are

\[
h=\frac{\Delta+J}{2},\qquad
\bar h=\frac{\Delta-J}{2}.
\]

The Mellin transform of a momentum-space leg is

\[
\mathcal M[f](\Delta)=\int_0^\infty d\omega\,
\omega^{\Delta-1}f(\omega).
\]

If a soft expansion contains \(A(\omega)\sim \omega^{-p}A^{(p)}\), the
infrared contribution with cutoff \(\Lambda\) is

\[
\int_0^\Lambda d\omega\,\omega^{\Delta-1-p}
=\frac{\Lambda^{\Delta-p}}{\Delta-p}.
\]

It has a pole at \(\Delta=p\), with residue \(A^{(p)}\). In particular, a
leading \(1/\omega\) soft factor produces the conformally soft pole at
\(\Delta=1\). This is the first analytic target implemented here.

For a fixed color-generator component, the leading holomorphic soft-gluon
current Ward kernel is represented as

\[
\sum_i \frac{T_i^a}{z-z_i}.
\]

The implementation stores a scalar matrix-element coefficient for a chosen
color component. It does not implement the full non-Abelian operator algebra,
loop corrections, or a complete celestial CFT.

## 2. Eight-coordinate chart versus PAN V8 and E8 Cartan

The code defines a lossless eight-real-coordinate *celestial data chart* for
one massless colored external leg:

\[
(\Re\Delta,\Im\Delta,J,\Re z,\Im z,q_1,q_2,\eta).
\]

Here \(q_1,q_2\) are weights in a caller-declared SU(3) Cartan basis and
\(\eta=\pm1\) labels outgoing/incoming. This chart is not the PAN V8 tuple
\((h,R,u,d,\tau,\chi,s,f)\), and it is not an E8 Cartan weight. It is a typed
coordinate chart for external celestial data. Round-trip tests verify that
this bookkeeping representation loses no information.

No automatic assignment of \(\Delta\), helicity, or color weights to V8 axes
is made. The V8 semantics remain canonical. A Janus-Hydra-to-V8 adapter must
be separately declared and tested before any such assignment is accepted.

## 3. E8-derived cut-and-project experiment

The repository already contains the exact E8 root set and first three E8
lattice shells. The new experiment reuses the same doubled-integer shell
convention and checks its shell sets against the existing exact shell audit.

For \(x=(a,b)\in\mathbb R^4\oplus\mathbb R^4\), the experimental split is

\[
x_\parallel=\frac{a+\phi b}{\sqrt{1+\phi^2}},\qquad
x_\perp=\frac{\phi a-b}{\sqrt{1+\phi^2}}.
\]

The corresponding \(8\times8\) block matrix is orthogonal. Since \(\phi\) is
irrational and E8 has rational coordinates in the standard basis, neither
four-dimensional subspace contains a nonzero E8 lattice vector. This gives
a generic irrational 4+4 cut-and-project setup.

**Important distinction:** this golden-block split is an experimental
orthogonal irrational decomposition. It is not claimed to reproduce the
canonical Elser–Sloane \(H_4=[3,3,5]\)-invariant projection. The published
Elser–Sloane construction projects E8 onto an invariant four-space and uses
the projection of the E8 Voronoi cell as its acceptance window. Their window
has 720 vertices (a 600-cell and a concentric 120-cell); their construction
also establishes a 4D quasicrystal with \(H_4\) point group. The exact
Elser–Sloane basis/window is a later milestone, not silently substituted by
the ball window in this v0.

## 4. Undulating acceptance window

For the initial finite-shell experiment, use a compact four-dimensional ball
window

\[
W(\theta)=\{y\in\mathbb R^4:\|y-c(\theta)\|\le R(\theta)\},
\]

with

\[
R(\theta)=R_0e^{a\sin\theta},\qquad
c(\theta)=b\sin\theta\,e_1.
\]

The radius term is a uniform breathing deformation; the center shift is an
internal-space phason parameter. At every phase the window remains compact
with nonempty interior. Lattice points can enter or leave the selected set
only when their internal projections cross the window boundary.

This is a family of finite-shell model-set samples, not a physical time
evolution. The current code enumerates only the first three nonzero E8
lattice shells (240, 2,160 and 6,720 vectors). It does not claim to construct
the complete infinite quasicrystal.

## 5. Why this is relevant to the undulating Gosset programme

This gives two distinct but compatible geometric layers:

1. The finite Gosset \(4_{21}\) root polytope: 240 norm-two roots, exact
   incidence and Coxeter-plane projection audits.
2. The E8 lattice model-set layer: infinitely many lattice points filtered
   through a four-dimensional internal acceptance window, with a controlled
   phase-dependent window family.

The first is a finite root polytope; the second is an aperiodic point set
derived from the full E8 lattice. They must not be conflated. The finite
240-root shell is only one shell of the lattice and is not itself the
quasicrystal.

The current undulation is applied to the *acceptance window*, not by
arbitrarily moving the E8 lattice roots. This preserves the lattice as the
fixed parent object and makes boundary crossings explicit.

## 6. Test plan and evidence levels

| Test | Current implementation target | Evidence |
|---|---|---|
| Celestial weights | \(h,\bar h\) from \(\Delta,J\) | exact formula / unit test |
| Mellin soft pole | pole at \(\Delta=p\), residue coefficient | analytic formula / unit test |
| Current kernel | fixed-component \(\sum_i T_i^a/(z-z_i)\) | deterministic evaluation |
| Eight-coordinate chart | round-trip all typed labels | exact bookkeeping test |
| E8 shell source | 240 / 2,160 / 6,720 and set equality | exact integer shell test |
| 4+4 split | norm preservation | floating-point orthogonality residual |
| Window breathing | positive radius, periodicity, boundary selection changes | finite computational test |
| Canonical ESQC | reproduce Elser–Sloane H4 basis and 720-vertex Voronoi window | **not yet implemented** |
| Celestial ↔ V8/E8 coupling | preserve Lorentz/conformal action and Ward identities after mapping | **not yet implemented** |

## 7. Reproduction

\`\`\`bash
python -m unittest tests.test_celestial_gosset_quasicrystal -v
python experiments/celestial_gosset_quasicrystal_audit.py
\`\`\`

The workflow runs only these focused tests and the deterministic audit runner.
A passing result validates this finite reference implementation, not a
celestial holographic duality, E8 gauge unification, or new physical law.

## References

- V. Elser and N. J. A. Sloane, *A highly symmetric four-dimensional
  quasicrystal*, J. Phys. A 20 (1987) 6161–6168,
  DOI: 10.1088/0305-4470/20/18/016.
- J. F. Sadoc and R. Mosseri, *The E8 lattice and quasicrystals*,
  J. Phys. A 26 (1993) 1789, DOI: 10.1088/0305-4470/26/8/009.
- S. Pasterski, *Lectures on celestial amplitudes*, Eur. Phys. J. C 81,
  1062 (2021), arXiv:2108.04801.
