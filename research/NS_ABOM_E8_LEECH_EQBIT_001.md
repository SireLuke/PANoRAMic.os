# NS–ABOM–E8–LEECH–EQBIT-001
## Read-only multi-module composition experiment

**Status:** initial executable integration harness; interface-level validation only.  
**Branch:** `research/ns-abom-e8-leech-eqbit-001`

## Objective
Compose existing PANoRAMic.os research artifacts without rewriting their
implementations or implying that they describe one physical system. The
experiment asks whether outputs can be orchestrated, provenance-tracked, and
checked together while preserving each module's mathematical domain.

## Existing components
| Component | Existing source | Boundary |
|---|---|---|
| Navier–Stokes | `experiments/ns_evidence_001_cosmo/cosmo_results.json` | Frozen finite-time 2D/3D diagnostics; solver is not rerun |
| ABOM V8 | `core/abom_v8/abom_v8_model.py` | Exploratory sample; Fermi, scale, field and root-count channels remain separate |
| E8 | `core/geometry/e8_root_system.py` | Exact 240-root system in rank 8 |
| Leech | `experiments/moonshine_sierpinski/leech_unimodular_basis.py` | Rank-24 even-unimodular and minimum-norm certificate |
| Flip-eqbit | `experiments/flip_qubit/cut_rank_audit.py` | Gosset graph and GF(2) cut-rank audit |

The harness calls existing module entry points rather than copying their
algorithms. It emits a combined JSON artifact and leaves source evidence
unchanged.

## Dimensional firewall
- Navier–Stokes spatial dimension: 2D/3D benchmark domains (main fluid case 3D).
- PAN V8: eight state coordinates `(h,R,u,d,tau,chi,s,f)`.
- E8: rank-8 root space, 240 roots.
- Leech: rank-24 lattice.
- Gosset/flip-eqbit: 240 graph vertices derived from E8.

No common metric, 9D fluid domain, E8-to-Leech embedding, or solver-to-quantum
dynamics map is defined.

## Pairwise gates
1. **NS ↔ ABOM:** a frozen 3D NS energy diagnostic is used as an explicitly
   dimensionless Fermi-channel probe. Interface test only; not physical energy coupling.
2. **ABOM ↔ E8:** compare ABOM's root-count view with canonical exact E8 roots (240).
3. **E8 ↔ Leech:** verify both certified structures while retaining rank 8 and rank 24; no embedding.
4. **E8 ↔ flip-eqbit:** reconstruct Gosset graph contract and check 240 vertices against E8 root count.
5. **Leech ↔ flip-eqbit:** retain lattice and graph-state outputs as separate typed artifacts.
6. **NS ↔ flip-eqbit:** explicitly not coupled; a future link requires a declared state map, units, dynamics, and falsifiable observables.

## Controls and interpretation
- Frozen NS data is read-only; solvers and result files are unchanged.
- Flip-eqbit sample count and seed are recorded; sampled maxima are not exact statements.
- Leech's exact basis certificate is not conflated with shell moments or the VOA/Monster story.
- ABOM's Fermi probe does not assert a literal negative-energy sea.
- Passing means only that listed interface checks passed. It does not establish
  physical coupling, quantum advantage, NS regularity, or a unified theory.

## Run
```bash
python -m unittest tests.test_ns_abom_e8_leech_eqbit_integration -v
python -m experiments.ns_abom_e8_leech_eqbit_001.integration --eqbit-samples 128 --eqbit-seed 20261121
```
The full run may be computationally heavier because the Leech certificate
enumerates its minimal shell and flip-eqbit rebuilds the 240-vertex graph.
Output defaults to `ns-abom-e8-leech-eqbit-001.json` in the working directory.

## Next stages
1. Run the harness and retain JSON output with a run manifest.
2. Add randomized adapter controls and ablation runs without changing source modules.
3. Ask independent benches to reproduce the output, then independently implement one adapter.
4. Only after those gates pass, propose an explicit cross-module mathematical map.

## Evidence grade
**Software integration / reproducibility protocol.** Not a physical validation
claim. The NS report's boundary remains unchanged: Navier–Stokes itself is
`not_tested`.
