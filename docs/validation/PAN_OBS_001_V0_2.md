# PAN-OBS-001 v0.2 — Topological Invariance Under Observation Channels

**Status:** Experimental implementation  
**Repository branch:** \`feat/pan-obs-001-v0.2\`  
**Scope:** Classical synthetic point-cloud robustness experiment

## Objective

Test whether persistent topological features reconstructed from a known latent
manifold remain stable under controlled changes in sampling density, angular
sampling bias, additive noise, and rigid coordinate rotation.

This protocol does not claim to eliminate the observer effect. It does not
simulate quantum measurement, collapse, decoherence, dissipation, or physical
measurement back-action.

## Ground-truth system

The initial latent system is an evenly sampled unit circle embedded in
\(\mathbb R^3\). Its topology is known by construction:

- one connected component (\(\beta_0=1\));
- one independent loop (\(\beta_1=1\)).

The clean full point cloud is used as a reference persistence diagram. This
reference is available only because the experiment is synthetic.

## Experimental factors

| Factor | Levels |
|---|---|
| Sampling fraction | 0.25, 0.50, 0.75, 1.00 |
| Sampling strategy | Uniform, sector-biased |
| Additive isotropic noise | 0.00, 0.02, 0.05, 0.10 |
| Observation channel | Identity, rigid XYZ rotation |
| Replicates | 30 per condition by default |
| Bootstrap draws | 1,000 by default |

Sector-biased sampling uses weights proportional to
\(\exp(\kappa\cos\theta)\). Sampling is without replacement. At fraction 1.0,
both sampling strategies necessarily select every point; this is a useful
control showing that sampling bias vanishes when no points are omitted.

The identity and rotated channels are paired: they receive the same sampled,
noisy point cloud. A rigid rotation should preserve pairwise distances and
therefore the Vietoris–Rips filtration, up to numerical tolerance.

## Metrics

1. **H0/H1 persistent feature counts:** Number of finite-lifetime features
   whose persistence is at least the preregistered threshold.
2. **H1 bottleneck distance:** Distance between the observed H1 persistence
   diagram and the clean full-reference H1 diagram.
3. **Replicate-level bootstrap 95% percentile interval:** Resample independent
   experiment replicates within each condition and report the interval for
   each metric's mean.

Bootstrap resampling is performed over experiment replicates, not over
individual points. The resulting intervals quantify Monte Carlo variability
under this synthetic design; they are not population-level scientific
confidence intervals.

## Reproducibility

Default random seed: \`20261108\`.

The seed, point count, replicate count, bootstrap count, sampling fractions,
noise levels, bias concentration, and persistence threshold are written into
the summary report. Raw replicate-level metrics are retained in CSV.

Run:

\`\`\`bash
pip install -r requirements-observer.txt
python tools/validation/pan_obs_001_v02.py --out results/pan_obs_001_v02
python -m unittest tests.test_pan_obs_001_v02 -v
\`\`\`

For a quick smoke run:

\`\`\`bash
python tools/validation/pan_obs_001_v02.py \\
  --points 80 --replicates 3 --bootstraps 100 \\
  --noise-levels 0,0.05 --sample-fractions 0.5,1.0 \\
  --out results/pan_obs_001_v02_smoke
\`\`\`

## Interpretation and limitations

- Topological stability is not equivalent to complete reconstruction accuracy.
- A rigid coordinate rotation is an isometry; this is a control, not a difficult
  invariance challenge.
- Noise, undersampling, and nonuniform sampling can change the reconstructed
  diagrams even when the latent topology is unchanged.
- A clean synthetic reference is not available in most empirical settings.
- The experiment does not establish that topology is universally superior to
  conventional statistical reconstruction. A later benchmark should compare
  against PCA and non-topological baselines under matched data and compute.
- The circle is a baseline only. Gosset \(4_{21}\) geometry is a later,
  separate experiment and must not be inferred from this result.

## Acceptance checks for v0.2

1. Helper tests pass.
2. Same seed produces identical sampled indices and summary metrics.
3. Rotation matrix is orthonormal and preserves pairwise distances.
4. At full sampling and zero noise, identity and rotated H1 diagrams agree
   within numerical tolerance.
5. Bootstrap intervals are present for at least two replicates and explicitly
   absent for a single replicate.
6. Both sampling strategies, every configured fraction, noise level, and
   observation channel appear in the output.
7. Raw replicate-level rows and protocol metadata are retained.

These checks validate software behavior and the synthetic experiment only.
They do not establish observer-effect avoidance or physical validity.
