// engine/par/parVelocityEngine.ts

export function computeParVelocity({
  markets,
  ecology,
  infrastructure,
  nodes,
  microAi,
}: {
  markets: any
  ecology: any
  infrastructure: any
  nodes: any[]
  microAi: any
}) {
  const extractionPenalty = markets.extractivePressureIndex * 0.3
  const ecologyBoost = ecology.regenerationIndex * 0.2
  const infrastructureBoost = infrastructure.resilienceIndex * 0.2
  const nodeBoost = (nodes.length > 0 ? nodes.length : 1) * 0.01
  const microAiBoost = microAi.microAiCoverageIndex * 0.15

  let velocity =
    1 -
    extractionPenalty +
    ecologyBoost +
    infrastructureBoost +
    nodeBoost +
    microAiBoost

  // Bound velocity between 0.1 and 2.0
  velocity = Math.max(0.1, Math.min(velocity, 2.0))

  return velocity
}
