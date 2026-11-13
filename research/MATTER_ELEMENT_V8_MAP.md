# Matter element -> V8 map, v0 (declared, non-canonical)

Status: **declared hypothesis**, tested once against a shuffle null. Not canonical, not a physical identity.
Code: `experiments/matter_elements/v8_element_map.py`; tests: `tests/test_v8_element_map.py`.

## Sources used
- Eight-coordinate state and ranges (chi in [-1,1], others in [0,1]): `docs/PAN_V8_DYNAMIC_PHASE_LAYER.md` (experimental, unmerged there).
- Channel contract (named channel, declared source/transform, "not a derived physical identity"; unmapped = None):
  `core/abom_v8/physics_adapters.map_scalar_to_v8`, extended to several channels.
- V9 affine-E8 `xi` traversal is a **display layer only** (orthogonal view frames, not lattice automorphisms). It is not
  used here and no element-to-E8-root mapping is asserted.
- Phase idea (theta wraps at each noble gas) from a brainstorm the user relayed; period lengths come from Madelung
  filling (2,8,8,18,18,32,32), not 2n^2.

## The map
| Channel | Kind | Definition |
|---|---|---|
| R | structural | (period - 1) / 6 |
| h | structural | position in period / period length; exactly 1 at each noble gas; theta = 2*pi*h wraps there |
| u | structural | occupancy of last-filled subshell / its capacity 2(2l+1) |
| chi | measured | (electronegativity - table median) / max abs deviation |
| s | measured | min-max of log10(density) |
| d | measured | min-max of ionisation energy |
| tau, f | unassigned | None (atomic number is an ordering, not time) |

Structural channels are exact functions of the Madelung configuration. They place elements on the grid and are **not**
tested for group recovery, because they largely determine group and block (circular). Only measured channels enter the
null test.

## Pre-registered test (written before the first run)
Features: primary (chi, s, d) on complete cases; secondary (s, d). Metrics A (3-NN GroupBlock purity) and C (s/p-block
1-NN group purity), labels shuffled 5000 times, seed 20261112. PASS: A and C each above null p99.

## Result (single run)
| | complete cases | A (null p99) | C (null p99) | shuffles >= observed (A, C) | pass |
|---|---|---|---|---|---|
| primary (chi, s, d) | 88 | 0.674 (0.223) | 0.421 (0.289) | 0, 0 | yes |
| secondary (s, d) | 96 | 0.628 (0.205) | 0.333 (0.262) | 0, 6 | yes |

Six-property baseline for comparison: A = 0.69, C = 0.57. The three-channel map nearly matches the baseline on A and is
clearly below it on C.

## Reading
- Measured channels alone, in V8 form, recover block neighbourhoods far above chance.
- It does **not** beat the six-property baseline, so promotion criterion 1 (match or beat baseline) is **not met**.
- Excluded from the primary test (missing electronegativity or density): Ar, He, Ne, Rn and many superheavy elements, so
  noble gases are still barely tested.
- Routing properties through V8 gives no evidence of an advantage over any plain embedding of the same properties.

## Non-claims
No claim that V8 explains the periodic table, that tau or f have element meanings, that hydrogen or E8 geometry is
involved, or that this map is canonical. Canonical status needs: criteria 1 to 4 (baseline parity, a second data source
or held-out elements, noble gas and halogen fixes, defined tau and f) and promotion of the experimental phase layer.
