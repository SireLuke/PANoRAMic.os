# 6_21 / E10 bounded reflection-orbit experiment

Run:

```bash
python experiments/e10_6_21_reflection_orbit.py --depth 12
```

This uses the exact rational Coxeter Gram matrix for the ([3^{6,2,1}])
diagram and applies the ten simple reflections to roots represented in the
simple-root basis. It checks that each generator preserves the Gram form,
that generated roots remain integral in this basis, and that every generated
root has norm 1.

The depth parameter bounds reflection word length from the ten simple roots.
The result is a reproducible finite patch of the real-root orbit, not a
complete enumeration of the infinite root system and not a geometric
realization of all honeycomb cells.

Terminology: the full symmetry group is the hyperbolic Coxeter group
(ar T_9=[3^{6,2,1}]), associated with hyperbolic E10. The affine E9 Weyl
group is a proper affine subgroup, not the full symmetry group.
