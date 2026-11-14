# Starter molecule set (with H3+) and partial electron-affinity / Allen table

Status: data intake with consistency checks. No physics claims. Code: `experiments/matter_molecules/molecule_starter.py`;
tests: `tests/test_molecule_starter.py`; data: `experiments/matter_molecules/data/molecules_starter.json`,
`experiments/matter_elements/data/EA_Allen_partial_user_supplied.csv`.

## Source
User-supplied one-page PDF (sha256 in the data file). It cites no primary sources. Its subtitle mentions isotope
classifications and energy levels, but the file contains neither.

## Molecules (7)
Six supplied by the user (H2O, CH4, CO2, NH3, HCl, C2H4) with SMILES, one named bond length and one named angle, plus
**H3+ added at the user's request** from Wikipedia: equilateral triangle, 0.90 A side, 60 degrees, two electrons shared over
three centres, formed by H2+ + H2 -> H3+ + H. The 0.90 A figure is a rounded web value; the ab initio equilibrium value is
believed to be about 0.87 A and should be confirmed against NIST CCCBDB or a primary paper. H3+ has no single standard
SMILES, so that field is null.
Checks: SMILES atom counts match each formula; CH4 angle is tetrahedral to 0.1 degrees; CO2 is 180; H2O is 104 to 105;
NH3 is below tetrahedral; all bond lengths lie in a plausible 0.7 to 1.5 A window. The geometry values of the six supplied
molecules are **not yet** checked against CCCBDB.

## Electron affinity and Allen electronegativity (10 elements)
H, He, Li, C, N, O, F, Ne, Cl, Ar. Electron affinities match the commonly quoted values; negative entries (He, Ne, Ar, N)
mean the anion is unbound and the noble-gas figures are literature estimates.
**Conflict:** the PDF lists Allen Cl = 3.481. The Wikipedia Allen column (fetched 2026-11-13) gives 2.869, and the Allen scale
places each noble gas above the preceding halogen (Ar 3.242 > Cl 2.869), which 3.481 would break. The supplied value is kept
as supplied and flagged in `allen_conflicts`; it is not corrected silently. The other nine match the reference within 0.005.

## What this does and does not do
- Gives He, Ne and Ar an electronegativity on a single (Allen) scale, which the Pauling-based chi channel lacks.
- Does **not** fill the halogen gap (only F and Cl present; Br and I absent) or Kr, Xe, Rn.
- Not used in any test yet. Mixing Allen values into the Pauling-based chi would mix scales; the intended use is a declared
  alternative chi built from a complete Allen column, tested with a new pre-registered run.

## Needed next
Allen electronegativity and electron affinity for all elements (one table, one scale), CCCBDB geometries for the six
molecules, and the missing isotope and energy-level tables.
