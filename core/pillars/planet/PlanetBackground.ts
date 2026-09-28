// core/pillars/planet/PlanetBackground.ts

export interface PlanetBackground {
  // Identity
  name: string
  age: number // billions of years
  type: "terrestrial" | "gas" | "ocean" | "hybrid"
  biosphereType: "earthlike" | "synthetic" | "unknown"

  // Planetary Constants (never change)
  gravity: number
  landmassDistribution: number // 0–1
  waterDistribution: number // 0–1
  energyPotential: number // 0–1
  foodPotential: number // 0–1
  mineralPotential: number // 0–1
  recyclingPotential: number // 0–1
  infrastructurePotential: number // 0–1
  educationPotential: number // 0–1
  humanitarianPotential: number // 0–1

  // Civilization Baselines (starting values)
  initialPopulation: number
  initialResourceStock: number
  initialGovernanceIntegrity: number // 0–1
  initialHumanitarianAlignment: number // 0–1
  initialHarmIndex: number // 0–1
  initialMarketIntegrity: number // 0–1
  initialCommonsOpenness: number // 0–1
  initialEpistemicIntegrity: number // 0–1
  initialTransparency: number // 0–1
  initialCorporateCapture: number // 0–1
  initialEcologicalDebt: number // 0–1
  initialTimeWealth: number // 0–1
  initialRepairability: number // 0–1
  initialCulturalDiversity: number // 0–1

  // Floors (minimum allowed values)
  humanitarianFloor: number
  rightsFloor: number
  dignityFloor: number

  // Ceilings (maximum allowed values)
  ecologicalCeiling: number
  resourceCeiling: number
  populationCapacity: number
}

// Default Earth-like background
export const DefaultPlanetBackground: PlanetBackground = {
  name: "PAN-Earth",
  age: 4.5,
  type: "terrestrial",
  biosphereType: "earthlike",

  gravity: 1.0,
  landmassDistribution: 0.29,
  waterDistribution: 0.71,
  energyPotential: 0.85,
  foodPotential: 0.75,
  mineralPotential: 0.80,
  recyclingPotential: 0.60,
  infrastructurePotential: 0.70,
  educationPotential: 0.65,
  humanitarianPotential: 0.55,

  initialPopulation: 8000000000,
  initialResourceStock: 1.0,
  initialGovernanceIntegrity: 0.40,
  initialHumanitarianAlignment: 0.35,
  initialHarmIndex: 0.30,
  initialMarketIntegrity: 0.45,
  initialCommonsOpenness: 0.20,
  initialEpistemicIntegrity: 0.30,
  initialTransparency: 0.25,
  initialCorporateCapture: 0.60,
  initialEcologicalDebt: 0.55,
  initialTimeWealth: 0.20,
  initialRepairability: 0.30,
  initialCulturalDiversity: 0.70,

  humanitarianFloor: 0.10,
  rightsFloor: 0.15,
  dignityFloor: 0.20,

  ecologicalCeiling: 1.0,
  resourceCeiling: 1.0,
  populationCapacity: 12000000000
}
