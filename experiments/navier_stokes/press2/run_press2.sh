#!/usr/bin/env bash
# Press II production launcher.
#
# Every parameter below is pinned to NS_PRESS_II_PREREGISTRATION.md
# (filed as PR #169, ruled by the maintainer 2026-11-22). Do not edit
# the numbers here without amending the preregistration first.
#
# Usage:
#   ./run_press2.sh [outdir]     detached (default); log lands in outdir
#   FG=1 ./run_press2.sh         run in the foreground instead
#
# Re-running the same command resumes from the last checkpoint
# (<tag>.ckpt.npz, written every 1.0 time units). The outdir is
# relative to the repository root.
set -euo pipefail
cd "$(dirname "$0")/../../.."

TAG=press2_re1600_n128
OUT="${1:-experiments/navier_stokes/press2/press2_runs}"
mkdir -p "$OUT"

CMD=(python3 -m experiments.navier_stokes.press2.tg_press2 run
     --out "$OUT" --tag "$TAG"
     --N 128 --Re 1600 --T 12 --dt 0.005 --M 100 --cap 200000 --kmax 32)

if [[ "${FG:-0}" == "1" ]]; then
  exec "${CMD[@]}"
fi

nohup "${CMD[@]}" > "$OUT/$TAG.log" 2>&1 &
echo "Press II launched: pid $!"
echo "  log:      $OUT/$TAG.log"
echo "  progress: tail -f $OUT/$TAG.log    (a step line every 200 steps = one checkpoint)"
echo "  resume:   re-run this script; it picks up from the last checkpoint"
echo "  analyze:  python3 -m experiments.navier_stokes.press2.tg_press2 analyze --out $OUT --tag $TAG"
