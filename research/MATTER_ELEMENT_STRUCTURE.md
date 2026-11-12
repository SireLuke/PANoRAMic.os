# Matter track step 2a: rule-derived periodic-table structure and a validator for sourced data

**Status:** derived structure plus validation tooling; contains no measured element data.
**Adds:** `experiments/matter_elements/element_structure.py`, `tests/test_element_structure.py`, a workflow, this note. Based on `main`; no existing module is changed.

## Why no numbers yet

Atomic masses, radii, electronegativities, ionisation energies and observed ground-state configurations are measured data. They need a cited source (NIST, IUPAC CIAAW, PubChem) with version and date, and none of them is typed in from memory here. The authoring session could not download NIST data (no network route from the shell; the NIST data pages were not fetchable), so this step builds everything that can be derived and checked offline, and a validator that will vet the real table when it is supplied.

## What is derived and tested

- Madelung filling order (n + l, then n) and subshell capacities 2, 6, 10, 14, giving period lengths 2, 8, 8, 18, 18, 32, 32 and noble-gas closures at Z = 2, 10, 18, 36, 54, 86, 118.
- Predicted configuration for every Z = 1..118, block (s/p/d/f), period, and an 18-column long-form layout with the f-block on two rows below (28 f, 40 d elements). All 118 cells are unique.
- Convention: He in group 18; La..Yb and Ac..No on the f rows; Lu and Lr in group 3 (IUPAC 2021 provisional). Other layouts exist.
- Symbols and names (118 each, unique, definitional) checked for internal consistency.

## What it deliberately does not claim

The Madelung rule is empirical and fails for about 20 elements. The tests pin one example: it predicts Cr as 3d4 4s2, observed 3d5 4s1. Predicted configurations are labelled predictions; observed ones must come from the sourced table. Layout choices (He, La/Ac vs Lu/Lr) are conventions, not physics. Nothing here maps V8 coordinates onto elements.

## Validator for the sourced table

`validate_table(rows)` reports, without editing data: atomic numbers not exactly 1..118, symbol mismatches against Z, non-positive masses, and mass-order inversions (a few are real, such as Ar/K, Co/Ni and Te/I, so inversions are listed for review, not failed). `load_csv(path)` reads a CSV such as the PubChem periodic-table export or a NIST-derived file.

## Planck and unit scales

Not part of the element table. Planck length, time and energy are derived reference scales (see `qwave.py`) and are not stored as element properties. Element lengths stay in SI metres with provenance; a Planck-length ratio, if wanted for display, is computed on demand by QWAVE and labelled as a unit conversion.

## Next

Supply a sourced CSV (for example PubChem's periodic-table export or NIST atomic-weight data), run `validate_table`, record source, version and date per field, then build the similarity layout over the sourced properties and test whether the periodic grid emerges.
