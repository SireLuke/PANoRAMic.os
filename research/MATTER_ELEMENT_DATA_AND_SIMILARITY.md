# Matter track step 2b: the supplied PubChem element table, and a property-similarity test

**Status:** data checks plus one pre-registered comparison. Positive for "properties carry group and block structure"; says nothing about V8.
**Adds:** `experiments/matter_elements/{pubchem_elements.py, similarity_layout.py}`, `data/PubChemElements_all.csv` and its provenance file, `tests/test_pubchem_elements.py`, this note. Built on the element-structure branch. No existing module changed.

## The data (as supplied, unedited)

`PubChemElements_all.csv`: 118 rows, 17 columns, supplied by the repository owner on 2026-11-12. The file carries no per-field source or units, so the provenance file records the file hash and says plainly that the origin of each property must be taken from PubChem's page before any value is cited as sourced.

Checks run (all in `tests/test_pubchem_elements.py`):
- Z = 1..118 once each, symbols match; every observed configuration sums to Z.
- **19 of 118 observed configurations depart from the filling rule**: Cr, Cu, Nb, Mo, Ru, Rh, Pd, Ag, La, Ce, Gd, Pt, Au, Ac, Th, Pa, U, Np, Cm. The test pins this exact set.
- Mass-order inversions listed for review: Ar/K, Co/Ni, Te/I (textbook cases) and five more (Th/Pa, U/Np, Pu/Am, Cm/Bk, Bh/Hs) at radioactive elements, where the listed mass depends on which isotope is chosen; not treated as errors.
- Quirks: US spellings (Aluminum, Cesium); eight masses rounded to 0-1 decimals (Li 7.0, Pb 207, ...); Pd colour code `6985` lost its leading zeros; Lu and Lr are labelled Lanthanide/Actinide while the layout convention puts them in group 3 (a convention difference, not an error); configurations for Mt..Og are marked calculated or predicted.
- Missing values (of 118): electron affinity 61, boiling point 25, electronegativity 23, density 22, radius 19, ionisation energy 16, melting point 15.

## Pre-registered test

Do six measured properties (electronegativity, radius, ionisation energy, melting point, boiling point, density; log scale for the last three) place elements near others of the same GroupBlock, and for s/p-block elements the same group, with no use of Z, group, period or configuration? Criteria and nulls were fixed in the module docstring before the first run.

| Metric | Observed | Null 99th pct (5000 shuffles) | Shuffles >= observed |
|---|---|---|---|
| A: 3-neighbour GroupBlock purity (85 complete elements) | 0.69 | 0.23 | 0 |
| C: 1-neighbour group match, s/p block (37 elements) | 0.57 | 0.27 | 0 |
| B: macro recall over 9 blocks (reported only) | 0.60 | 0.16 | 0 |

**Both criteria pass.** The result holds for k = 1, 3, 5 and when any one feature is dropped (A between 0.63 and 0.72 against nulls near 0.22).

## What it does and does not show

- It confirms the periodic law as a statement about the data: measured properties alone recover block and group neighbourhoods. Examples: Na's nearest neighbours are Ca, Sr, Li; Fe's are Co, Cr, Mn; Ce's are Pr, La, Nd.
- Recovery is uneven. Lanthanides (0.88) and transition metals (0.86; chance 0.33) are strong because their properties vary slowly across the row. Halogens (0.25), nonmetals (0.43) and alkaline earths (0.44) are weak. He, Ne and Ar fall out of the complete-case set (no electronegativity), so the noble-gas block is barely tested (Kr, Xe only).
- A 2D principal-axis layout (68% + 21% of variance) shows the neighbourhoods but is **not** the periodic grid: it orders by property magnitude, not by period and group. A layout that reproduces the table's rows and columns needs an explicit constraint and is a separate step.
- **No V8 mapping is used or implied.** The kernel's own convention is that every feature-to-V8 map is explicit and declared. Until one is, "similarity in V8" is not testable; this test uses standardised properties directly.

## Next

1. Declare a feature-to-V8 map (which property drives which of h, R, u, d, tau, chi, s, f) and re-run this test through it, with the same null, to see whether the map preserves the structure.
2. Grid layout step: place elements on the 18-column grid by constrained similarity and score against the real table.
3. Source each property field from PubChem's page and record it in the provenance file.
