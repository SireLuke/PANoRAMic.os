// engine/nodes/nodesEngine.ts

import { NodeProfile } from "../../core/pillars/nodes/NodeProfile"

/**
 * computeNode:
 * Final per‑tick node computation after all engines and RAMS audits.
 * This is where stability, risk, load, and resilience settle into final values.
 */

export function computeNode(node: NodeProfile): NodeProfile {
  let updated = { ...node }

  // Final stability calculation
  updated.stabilityIndex = Math.max(
    0,
    Math.min(
      1,
      updated.stabilityIndex -
        updated.riskIndex * 0.05 +
        updated.resilienceIndex * 0.03
    )
  )

  // Final risk calculation
  updated.riskIndex = Math.max(
    0,
    Math.min(
      1,
      updated.riskIndex +
        updated.stressIndex * 0.04 -
        updated.resilienceIndex * 0.02
    )
  )

  // Final load calculation
  updated.loadIndex = Math.max(
    0,
    Math.min(
      1,
      updated.loadIndex +
        updated.ecologicalDependencyIndex * 0.02 +
        updated.infrastructureDependencyIndex * 0.02 +
        updated.economicDependencyIndex * 0.02
    )
  )

  return updated
}
