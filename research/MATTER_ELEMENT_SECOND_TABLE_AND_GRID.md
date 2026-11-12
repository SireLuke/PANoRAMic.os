# Matter elements: second table replication and grid placement

Status: results of two pre-registered tests (each written into its module before the first run). Declared v0 map,
non-canonical. Code: `experiments/matter_elements/second_table.py`, `grid_layout.py`; tests:
`tests/test_second_table_and_grid.py`; figure: `research/figures/element_v8_grid.png`;
export: `experiments/matter_elements/grid_elements.json`.

## 1. Second table
Source: user-supplied attachment (118 rows, `data/SecondTable_user_supplied.csv`, sha256 in the provenance file).
Upstream origin and licence are not stated and not verified.

Cross-checks:
- Symbols and Z match the PubChem table exactly. Period, group and valence agree with the Madelung layout wherever given.
- It is **not independent** of PubChem: Spearman >= 0.99 on shared properties (electronegativity 0.997, ionisation 0.999,
  density 0.9999, melting point 0.993, boiling point 0.998). Atomic radius differs by definition (0.79). Agreement shows
  consistency, not independent confirmation.
- Label errors in `Type`: At = Noble Gas (should be halogen), Rn = Alkali Metal (noble gas), Fr = Alkaline Earth Metal
  (alkali), Ra = Actinide (alkaline earth), Ts blank. Labels were used as given in the pre-registered runs.
- It supplies density and ionisation energy for all six natural noble gases, but electronegativity is blank for them, so
  they enter only the (s, d) test.

Pre-registered replication (5000 shuffles, seed 20261112):
| Test | n | A (null p99) | C (null p99) | pass |
|---|---|---|---|---|
| six properties | 80 | 0.742 (0.263) | 0.543 (0.286) | yes |
| V8 primary (chi, s, d) | 93 | 0.692 (0.222) | 0.459 (0.297) | yes |
| V8 secondary (s, d) | 99 | 0.586 (0.205) | 0.349 (0.279; 4 shuffles >= obs) | yes |

The PubChem baseline (A 0.69, C 0.57) and the PubChem V8 result (0.674 / 0.421) are reproduced in kind. The V8 map still
trails the six-property result on C.

Class recall in the (s, d) space (fraction of each element's 3 nearest neighbours with the same label), reported only:
noble gas 0.33 (6), halogen 0.08 (4), alkali 0.61 (6), alkaline earth 0.22 (6). **Post-hoc, not pre-registered:** with
labels replaced by the group-defined family, noble gas 0.50, halogen 0.07, alkali 0.94, alkaline earth 0.28.
Reading: the mislabelled Rn/Fr/At/Ra depress the as-given numbers, but halogens and alkaline earths remain poorly
recovered by (s, d) alone, and noble gases are only about half recovered. The earlier weak spots are therefore not
explained by this table's label errors.

## 2. Grid placement
Cell positions come from the Madelung layout (He in column 18, La/Ac start the f-rows, Lu/Lr in group 3); 118 unique
cells. Similarity is used only to ask whether the measurement agrees with the placement.

Pre-registered statistic G = median Chebyshev grid distance from each element to its 1-nearest neighbour in measured
(s, d) space (PubChem, 96 elements). Observed G = 1 cell; shuffled-position null median 6, 1st percentile 4; 0 of 5000
shuffles <= observed. PASS.

Pattern breakers (largest grid distance to the nearest measured neighbour): H-N (14), Be-S (14), Mg-Si (12), Al-Sr (11),
Ca-Al (11), Sr-Al (11), Y-Ga (10), Mo-Bi (9), Tl-Th (9), Th-Tl (9). They are mostly elements whose (s, d) values sit
between families (hydrogen, alkaline earths, post-transition metals).

## Non-claims
The grid is a display convention. Neither test shows V8 explains the periodic table or beats a plain embedding of the
same properties. The second table is not independent evidence. No E8-root mapping is asserted.
