# Shared E8 root-system harness

This change centralizes only the canonical E8 root coordinates. The four
existing consumers retain their own geometry algorithms and public function
names; the independent PAN V9 affine-E8 validation harness is deliberately
not modified.

Canonical representation: 240 exact rational vectors in R^8, comprising
112 integer roots and 128 half-integer roots, each with squared norm 2.

The harness checks:
- cardinality, uniqueness, and exact norm;
- the root graph has 6,720 edges and degree 56 at every vertex;
- ABOM-v8, Gosset local-cell-star, STRATA, and Gosset Sierpinski adapters
  reproduce exactly the same set;
- conversion to floating point is explicit and lossless for these dyadic
  coordinates.

This is a root-data consolidation, not a consolidation of geometry engines,
and it does not establish any additional physical interpretation.
