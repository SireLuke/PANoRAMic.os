// core/data/trustEngine.ts

/**
 * Epistemic Trust Engine:
 * Scores incoming datasets based on consistency, provenance,
 * historical reliability, and structural integrity.
 */

export type TrustFactors = {
  sourceReputation?: number      // 0–1
  structuralIntegrity?: number   // 0–1
  historicalConsistency?: number // 0–1
  recency?: number               // 0–1
  crossSourceAgreement?: number  // 0–1
}

export function computeTrustScore(factors: TrustFactors): number {
  const weights = {
    sourceReputation: 0.30,
    structuralIntegrity: 0.25,
    historicalConsistency: 0.20,
    recency: 0.15,
    crossSourceAgreement: 0.10
  }

  let score = 0

  for (const key in weights) {
    const value = factors[key as keyof TrustFactors] ?? 0
    score += value * weights[key as keyof typeof weights]
  }

  return Math.max(0, Math.min(1, score))
}

/**
 * Structural integrity check:
 * Ensures incoming data is well-formed.
 */
export function checkStructuralIntegrity(data: any): number {
  if (!data || typeof data !== "object") return 0
  try {
    JSON.stringify(data)
    return 1
  } catch {
    return 0
  }
}

/**
 * Historical consistency:
 * Compares new data with previous patterns.
 */
export function computeHistoricalConsistency(
  previous: any[],
  incoming: any
): number {
  if (!previous.length) return 0.5

  const last = previous[previous.length - 1]
  const hashIncoming = JSON.stringify(incoming)
  const hashLast = JSON.stringify(last)

  return hashIncoming === hashLast ? 1 : 0.5
}