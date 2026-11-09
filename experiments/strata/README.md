# STRATA-002 experiment scaffold

This branch contains a reproducible, deliberately modest first implementation of STRATA. It is isolated from PAN runtime code and does not change V8, Janus Hydra, UHFE/UDFE, or canonical data.

## Run

From the repository root:

```bash
python -m unittest discover -s experiments/strata/tests -v
python experiments/strata/run_strata_002.py
```

Only the Python standard library is required.

## Scope and interpretation

The current fixtures are synthetic. They verify that the test machinery executes, that E8 root construction has expected mathematical invariants, and that scale/representation/control reporting works. They do **not** validate cross-domain empirical transfer or establish a universal invariant.

## Next empirical milestone

Add sourced datasets only after recording license, source URL/identifier, retrieval date, checksum, preprocessing, inclusion criteria, and domain-specific baseline. Keep each domain adapter independently testable. Do not tune on blind data.


## Evidence record and validation

The STRATA run record schema is `strata-run.schema.json`. The checked-in audit at `runs/STRATA-002-GEOMETRY-AUDIT-2026-11-09.json` records the current synthetic STRATA-002 smoke run and the bounded Gosset/E8, Sierpinski, and E10/E9 checks.

Validate the record with the dependency-free structural validator:

```bash
python experiments/strata/validate_run.py
```

The run record marks the other catalogue geometries and 11D parameter sweep as `not_tested`: the repository currently has no runnable implementations for those items. A valid record verifies structure and provenance fields, not the scientific interpretation.
