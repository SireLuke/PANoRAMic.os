// engine/par/parMintEngine.ts

export function computeParMintRate({
  par,
  ecology,
  infrastructure,
  markets,
  dashboard,
}: {
  par: any
  ecology: any
  infrastructure: any
  markets: any
  dashboard: any
}) {
  // Base mint rate from dignity + population
  let mintRate =
    par.population * 0.00001 * par.dignityFloat * par.resourceModifier

  // Ecology boosts minting when healthy
  mintRate += ecology.regenerationIndex * 50

  // Infrastructure boosts minting when resilient
  mintRate += infrastructure.resilienceIndex * 40

  // Markets reduce minting when extraction pressure is high
  mintRate -= markets.extractivePressureIndex * 60

  // Immune system activation reduces minting to stabilize the planet
  if (dashboard.immuneSystemActive) {
    mintRate *= 0.8
  }

  // Catastrophe probability reduces minting sharply
  mintRate *= 1 - dashboard.catastropheProbability * 0.5

  // Bound mint rate by PAR Cap
  mintRate = Math.min(mintRate, par.parCap)

  // Ensure mint rate never goes negative
  mintRate = Math.max(0, mintRate)

  return mintRate
}
