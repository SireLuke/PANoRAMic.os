# Sierpiński recursion symmetry notes

## Classical triangle

The seed is an equilateral triangle with vertices (v_0,v_1,v_2).
The three contractions are (F_i(x)=(x+v_i)/2).

The triangle's full Euclidean symmetry group is the dihedral group (D_3)
(order 6), isomorphic to (S_3). It consists of:

- identity;
- rotations by 120° and 240°;
- three reflections, each fixing one vertex and exchanging the other two.

A convenient pair of generators acting on vertex labels is:

- (r=(0\ 1\ 2)), the 120° cycle;
- (s=(1\ 2)), a reflection.

They satisfy (r^3=e), (s^2=e), and (srs=r^{-1}).

For any symmetry (g) inducing vertex permutation (sigma),

[
g(F_i(x))=F_{\sigma(i)}(g(x)).
]

This is the precise recursive symmetry statement: the group action commutes
with the IFS up to relabeling its contraction maps. At every finite depth,
the collection of cells is permuted by (D_3); the limiting attractor is
invariant under the same group.

## General regular simplex

For an n-simplex, the full symmetry group of the regular seed is
(S_{n+1}), with order ((n+1)!). The same equivariance identity holds.
For n=8, the simplex has nine vertices and its own regular-simplex symmetry
group (S_9) (order 362880). This is not the Weyl group of E8 and must not
be confused with Gosset 4_21 symmetry.

## Gosset comparison questions

To test a relationship with Gosset 4_21, obtain a documented coordinate
realization and explicit group action. For each candidate triangular triple:

1. determine its stabilizer in the Gosset symmetry group;
2. calculate the orbit of the triple under that group;
3. compare projected edge lengths and angles under a named projection;
4. check which stabilizer symmetries survive projection;
5. seed the Sierpiński IFS only after the projected triple passes equilateral
   tolerance checks.

The projection may destroy symmetries; an equilateral projected triple does
not imply the original 8D configuration has the same stabilizer. Report
projection distortion and provenance with every result.
