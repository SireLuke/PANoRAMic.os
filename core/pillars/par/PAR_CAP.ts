// core/pillars/par/PAR_CAP.ts

export function computeParCap({
  population,
  dignityFloat,
  resourceModifier,
  marketBurden,
  ecologyRegen,
  infrastructureResilience,
}: {
  population: number
  dignityFloat: number
  resourceModifier: number
  marketBurden: number
  ecologyRegen: number
  infrastructureResilience: number
}) {
  // Base cap from population + dignity
  const baseCap = population * dignityFloat * resourceModifier

  // Planetary conditions modify cap
  const ecologyFactor = ecologyRegen * 0.5
  const infrastructureFactor = infrastructureResilience * 0.5

  // Market extraction reduces cap
  const marketPenalty = marketBurden * 0.3

  // Final PAR Cap
  const parCap = baseCap * (1 + ecologyFactor + infrastructureFactor - marketPenalty)

  return Math.max(0, parCap)
}
