# SU(2) Lattice Gauge Foundations — v0

## Purpose

Establish a small, reproducible finite-lattice gauge-theory baseline before attempting continuum scaling, renormalization-group analysis, or any Yang–Mills existence/mass-gap question.

## Mathematical object

The first implementation is a two-dimensional periodic square lattice. Each oriented positive-direction link carries an element of SU(2), represented by a unit quaternion
\[
q=(a,b,c,d),\qquad a^2+b^2+c^2+d^2=1.
\]
The defining representation has \(\tfrac12\operatorname{Tr}(q)=a\). Quaternion multiplication implements the group product and quaternion conjugation is the inverse for unit elements.

For a plaquette based at \(x\), with directions \(\mu=0\), \(\nu=1\),
\[
U_{01}(x)=U_0(x)U_1(x+\hat 0)U_0(x+\hat 1)^{-1}U_1(x)^{-1}.
\]
A sitewise gauge transformation acts by
\[
U_\mu(x)\mapsto g(x)U_\mu(x)g(x+\hat\mu)^{-1}.
\]
Consequently the plaquette transforms by conjugation at its base point, so its trace and the Wilson action
\[
S_W=\beta\sum_p\left(1-\tfrac12\operatorname{Tr}U_p\right)
\]
are gauge invariant.

## Implemented baseline

- Exact group formulas represented numerically by unit quaternions.
- Periodic 2D lattice with one outgoing link per site and direction.
- Plaquette holonomy and Wilson action.
- Sitewise random gauge transformations.
- Deterministic seeded regression tests and JSON audit.

## Evidence classification

The quaternion multiplication/inverse/conjugation formulas are algebraic identities. The current test suite checks their numerical implementation and checks gauge covariance/invariance using floating-point arithmetic and explicit tolerances. These are computational regression tests, not formal proofs.

## Lean target (next milestone)

Formalize the quaternion identity
\[
\operatorname{scalar}(gq\bar g)=\operatorname{scalar}(q)
\]
under \(\lVert g\rVert^2=1\), then derive invariance of the plaquette half-trace under sitewise gauge transformation. The Lean theorem should use explicit quaternion multiplication and conjugation definitions and should not import the numerical implementation as an axiom. A Lean target is not counted as complete until it compiles in CI with no sorry and with dependencies recorded.

## Deliberate exclusions

This baseline does not claim:
- a continuum limit or Osterwalder–Schrader reconstruction;
- four-dimensional Yang–Mills existence;
- uniqueness of an infinite-volume limit;
- a positive mass gap, confinement, or a physical prediction;
- a special role for E8/Gosset geometry in SU(2) gauge theory.

E8/Gosset work remains a separate symmetry/geometry research track. Any future bridge must be stated as a testable construction with controls, not assumed from visual or algebraic resemblance.
