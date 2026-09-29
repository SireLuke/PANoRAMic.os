// core/data/normalize.ts

/**
 * normalizeNumber:
 * Ensures a number is finite, not NaN, and within a safe range.
 */
export function normalizeNumber(
  value: any,
  min: number = 0,
  max: number = 1
): number {
  if (typeof value !== "number" || !isFinite(value)) return min
  return Math.max(min, Math.min(max, value))
}

/**
 * normalizeNode:
 * Ensures node fields are valid and safe.
 */
export function normalizeNode(node: any): any {
  return {
    ...node,
    stability: normalizeNumber(node.stability),
    risk: normalizeNumber(node.risk),
    load: normalizeNumber(node.load),
    resilience: normalizeNumber(node.resilience),
    collapseRisk: normalizeNumber(node.collapseRisk),
    healthIndex: normalizeNumber(node.healthIndex),
    stressIndex: normalizeNumber(node.stressIndex),
    autonomyIndex: normalizeNumber(node.autonomyIndex),
    connectivityIndex: normalizeNumber(node.connectivityIndex),
  }
}

/**
 * normalizePillar:
 * Ensures pillar values are safe.
 */
export function normalizePillar(pillar: any): any {
  const out: any = {}
  for (const key in pillar) {
    out[key] = normalizeNumber(pillar[key])
  }
  return out
}

/**
 * normalizeWorld:
 * Applies normalization to nodes and pillars.
 */
export function normalizeWorld(world: any): any {
  const normalizedNodes: any = {}
  for (const id in world.nodes) {
    normalizedNodes[id] = normalizeNode(world.nodes[id])
  }

  const normalizedPillars: any = {}
  for (const key in world) {
    if (typeof world[key] === "object" && key !== "nodes") {
      normalizedPillars[key] = normalizePillar(world[key])
    }
  }

  return {
    ...world,
    nodes: normalizedNodes,
    ...normalizedPillars,
  }
}
