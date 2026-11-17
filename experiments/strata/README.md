# STRATA research implementation

The consolidated implementation lives on `main` under `experiments/strata/`; research code remains isolated from PAN runtime code and does not change V8, Janus Hydra, UHFE/UDFE, or canonical data.

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


## STRATA-003: Fermi disk partition and Zeng FFS dataset

Run the analytic Fermi disk-partition audit and transient Zeng et al. empirical
figure-data ingestion with:

```bash
PYTHONPATH=. python experiments/strata/run_strata_003.py
python -m unittest tests.test_strata_003_fermi_disk_partition -v
```

The independent area verifier reproduces the Fractal Kernel's exact unit-disk
partition: `A_white = pi/2 - pi*d_black^2/8 + pi*d_white^2/8`, where
`d_black=1-delta`, `d_white=1+delta`, and `delta=2N-1`. Since the diameters
sum to 2, this simplifies exactly to `A_white=pi*N`; the black area is
`pi*(1-N)`. Decorative lemniscate/Gerono-style eye marks are excluded. The
Kernel's Gerono transport curve is a separate geometry experiment.


The Zeng et al. Figure 3 CSVs are fetched at run time, checked against the
MD5 digests published by Zenodo, and assigned SHA-256 digests in the run
output. The accessible Zenodo record does not declare a dataset license;
the files are not bundled or redistributed. This is descriptive empirical
data ingestion, not held-out prediction, GHD reproduction, or cross-domain
validation. See `datasets/manifest.yaml` for provenance and preprocessing.
