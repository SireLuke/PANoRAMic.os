# Deprecated geometry engines

## Gosset local cell-star audit v1

- **Status:** Deprecated; retained as a frozen forensic reference only.
- **Path:** `experiments/gosset_local_cell_star_audit.py`
- **Reason:** Its Delaunay audit incorrectly imposed unit circumradius on both regular 8-simplex and 8-orthoplex cell orbits. The exact circumradius-squared values are (8/9) and (1), respectively.
- **Replacement:** `experiments/gosset_local_cell_star_audit_v2.py`
- **Policy:** Do not use v1 for validation or delete its historical source. Run the v2 test suite on the research branch. Do not merge into `main` until CI and independent review are complete.
