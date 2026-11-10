# E10 Lorentzian Coordinate Audit — 2026-11-10

## Purpose and scope

This isolated research increment constructs an exact rational Lorentzian coordinate model for the rank-ten Coxeter simplex with arms (6,2,1). It is a coordinate realization and ideal-vertex-link audit, not a construction or proof of completeness of the global hyperbolic 6_21 honeycomb.

## Exact Lorentzian realization

The Coxeter Gram matrix is factored over the rationals as

\[
G=LJL^{\mathsf T},\qquad
J=\operatorname{diag}\left(1,\frac34,\frac23,\frac58,\frac35,\frac7{12},\frac47,\frac9{16},\frac59,-\frac1{20}\right).
\]

Taking the ten simple-root vectors to be the rows of L in the diagonal metric J gives their Gram matrix exactly equal to G. The signature is (9,1), and det(G)=-1/1024.

The dual vertex vectors are the columns of

\[
\Omega=J^{-1}L^{-1},
\]

so that \(LJ\Omega=I\) and \(\Omega^{\mathsf T}J\Omega=G^{-1}\). Their exact squared norms, in the script's node order, are

\[
(-84,-60,-40,-24,-12,-4,0,-36,-8,-20).
\]

Thus nine vertex rays are timelike and one, node 6, is null. The time coordinates of all ten dual rays have the same sign; reversing all rays together places the nine finite vertices in one sheet of the hyperboloid and the null ray on its ideal boundary.

## Reflection validation

The script constructs each simple-root reflection in the ambient diagonal Lorentz metric. It verifies exactly that each reflection squares to the identity and preserves J. Products of adjacent generators have order three; nonadjacent generators commute. The complete defining Coxeter relation count is 10 + 9 + 36 = 55.

## Ideal vertex link

Deleting node 6 gives a rank-nine positive-semidefinite Gram matrix. All 511 nonempty principal minors are checked exactly: 510 positive and one zero. The positive primitive null-root marks, in the retained node order, are

\[
(6,5,4,3,2,1,4,2,3).
\]

The link is the affine E8 Coxeter diagram (also described as E9 in the E10 vertex-link ladder). Its affine Weyl group acts on an 8-dimensional Euclidean space. This identifies the Euclidean affine symmetry underlying the cusp link.

Important distinction: the affine E8 Coxeter simplex is a Euclidean alcove. The 5_21 honeycomb is a distinct uniform Wythoffian with the same affine E8 symmetry and vertex figure 4_21; the affine alcove alone is not the full 5_21 cell decomposition. The next step is to construct the Wythoffian from the affine link and verify its simplex/orthoplex incidence data, then use it as the horospherical cusp link of the hyperbolic chamber.

## Next obligations for a genuine 6_21 construction

1. Normalize the nine timelike dual rays to the hyperboloid and compute the ideal ray's horosphere section.
2. Build the affine E8 cusp-link Wythoffian explicitly and independently recover the 5_21 vertex figure/cell incidences.
3. Verify that the hyperbolic simplex reflections generate the intended chamber adjacency, including finite and ideal vertex stabilizers.
4. Establish local finiteness and completeness of the hyperbolic honeycomb; do not infer this from the Coxeter matrix alone.

## Reproducibility

Run: python -m unittest tests.test_e10_hyperbolic_621_coordinate_audit -v

All arithmetic uses Python's standard-library fractions.Fraction. The workflow for this branch runs only this focused test, has a 10-minute timeout, and does not cancel an in-progress run on a subsequent push.

## Interpretation boundary

No physical claim follows from this geometry. The E10 construction is a mathematical/hyperbolic extension of the Gosset/E8 research ladder. PAN V8, Janus Hydra, UHFE, and UDFE remain unchanged.
