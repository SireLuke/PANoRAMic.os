# 600-cell / S^3 harmonic spectrum audit

The supplied Claude script constructs the 120 vertices of the 600-cell on
S^3, forms the nearest-neighbour graph using inner product phi/2, and compares
its eigenspaces with S^3 harmonic dimensions and the Fock momentum-space
hydrogen analogy.

The source groups eigenvalues in ascending order, then enumerates those
groups as harmonic degrees l=0,1,... . For an adjacency operator, the
Gegenbauer prediction for increasing l starts at the largest eigenvalue.
The translation therefore sorts eigenspaces in descending adjacency
eigenvalue before assigning harmonic degree.

The 12-regular graph's first six eigenspaces match:
- l=0: eigenvalue 12, multiplicity 1;
- l=1: eigenvalue 9.70820393..., multiplicity 4;
- l=2: eigenvalue 6.47213595..., multiplicity 9;
- l=3: eigenvalue 3, multiplicity 16;
- l=4: eigenvalue 0, multiplicity 25;
- l=5: eigenvalue -2, multiplicity 36.

These multiplicities are (l+1)^2, the dimensions of degree-l harmonics on
S^3. Higher eigenspaces do not continue as a simple n^2 sequence, so the
claim is limited to the first six resolved levels.

This provides a useful parallel with the E8 root graph on S^7: the 600-cell
resolves six low-degree S^3 harmonic levels, while the 240-root E8 graph
resolves four full S^7 harmonic levels and a residual finite-shell
representation at the next level. These are finite graph/sphere comparisons,
not evidence for a physical hydrogen or quantum-gravity mechanism.
