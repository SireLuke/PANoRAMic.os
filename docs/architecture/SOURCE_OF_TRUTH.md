# Source of truth: pan-fractal-kernel vs PANoRAMic.os

Status: **declared by the repository owner on 2026-11-13; migration not yet performed.** This note records the intent and
a proposed procedure. It does not move any code.

## Declared ownership
| Item | Owner | PANoRAMic.os role |
|---|---|---|
| V8 coordinate schema `(h, R, u, d, tau, chi, s, f)`, ranges (chi in [-1,1], others [0,1]), tau = temporal | pan-fractal-kernel | consumes; `core/library/types.ts` mirrors it |
| Janus Hydra projections and the V8 phase layer | pan-fractal-kernel | consumes |
| V9 affine-E8 view (`xi` traversal, display only) | pan-fractal-kernel | consumes |
| Gosset / E8 geometry engines, spectroscopy, QCD and hydrogen benchmarks | pan-fractal-kernel | uses engines |
| Tests and experiments for the above | pan-fractal-kernel | copies kept until migration is confirmed |
| Application layer (TypeScript modules, Library of Alexandria, governance, economy) | PANoRAMic.os | owns |
| Declared V8 map for elements, element/molecule data, MatterNode catalog | PANoRAMic.os today; proposed to move to the kernel with the V8 schema | owns until migrated |

Conflict rule: if the mirrored V8 types in PANoRAMic.os disagree with the kernel, the kernel wins.

## Proposed migration procedure (copy first, then switch)
1. Copy the relevant modules, tests, notes and workflows into the kernel on one branch, keeping history references in the
   commit message.
2. Run the kernel's CI. Do not delete anything in PANoRAMic.os yet.
3. Pin the kernel version PANoRAMic.os consumes (a commit hash recorded in this file), and add a check that the mirrored
   V8 types match the kernel schema.
4. Only after both CIs pass, remove the duplicated copies from PANoRAMic.os in a separate PR.

## Open points
- The matter layer imports `core/abom_v8` and the repo's data files; moving it needs those paths made relocatable.
- The kernel is a flat layout; PANoRAMic.os is nested. A move needs a naming decision (for example `matter/`).
- Which repo hosts the data files (PubChem table, second table, molecule PDF extract) and their provenance hashes.
