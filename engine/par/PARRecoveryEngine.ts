// engine/par/PARRecoveryEngine.ts

export interface PARRecoveryProfile {
  flowIndex: number               // output from PARFlowEngine
  stabilityIndex: number          // global stability (0–1)
  dignityIndex: number            // rights + autonomy + safety (0–1)
  renewableBackingIndex: number   // ecological + renewable support (0–1)
  shockIndex: number              // recent volatility or collapse pressure (0–1)
}

export interface PARRecoveryResult {
  recoveryBoostIndex: number
  updatedFlowIndex: number
}

/**
 * PAR Recovery Engine
 *
 * - Stabilizes PAR after shocks or volatility
 * - Uses dignity, renewable backing, and stability to counteract shockIndex
 * - Ensures PAR flow remains smooth and non-destructive
 */
export function runPARRecoveryEngine(
  profile: PARRecoveryProfile
): PARRecoveryResult {
  const {
    flowIndex,
    stabilityIndex,
    dignityIndex,
    renewableBackingIndex,
    shockIndex,
  } = profile

  // Recovery strength grows with stability + dignity + renewable backing
  const recoveryBase =
    stabilityIndex * 0.4 +
    dignityIndex * 0.3 +
    renewableBackingIndex * 0.3

  // Shock dampening reduces recovery effectiveness
  const shockDampening = 1 - shockIndex

  const recoveryBoostIndex = recoveryBase * shockDampening

  // Updated flow: recovery boosts flow, shock reduces it
  const updatedFlowIndex = Math.min(
    1,
    Math.max(0, flowIndex + recoveryBoostIndex - shockIndex * 0.2)
  )

  return {
    recoveryBoostIndex,
    updatedFlowIndex,
  }
}

}
