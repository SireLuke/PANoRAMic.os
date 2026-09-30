// core/data/mappingRules.ts

/**
 * Mapping Rules Engine:
 * Defines how external data updates pillars, nodes, and global signals.
 *
 * This engine is universal — it supports WHO, NASA, IMF, World Bank,
 * WTO, FTC, NOAA, USGS, EPA, DOE, humanitarian feeds, climate feeds,
 * energy feeds, and more.
 */

export type MappingRule = {
  sourceKey: string
  targetKey: string
  scale?: number
  clampMin?: number
  clampMax?: number
}

export type MappingRuleSet = {
  pillarRules?: Record<string, MappingRule[]>
  globalRules?: MappingRule[]
  nodeRules?: MappingRule[]
}

export function applyMappingRules(
  incomingValues: Record<string, number>,
  rules: MappingRule[]
): Record<string, number> {
  const result: Record<string, number> = {}

  for (const rule of rules) {
    const raw = incomingValues[rule.sourceKey]
    if (raw === undefined) continue

    let scaled = raw * (rule.scale ?? 1)

    if (rule.clampMin !== undefined) scaled = Math.max(scaled, rule.clampMin)
    if (rule.clampMax !== undefined) scaled = Math.min(scaled, rule.clampMax)

    result[rule.targetKey] = scaled
  }

  return result
}

/**
 * Universal mapping rule library.
 * These rules cover the broadest categories:
 * - NASA climate + space weather
 * - WHO health + outbreak
 * - IMF / World Bank economic stress
 * - FTC regulatory pressure
 * - NOAA weather
 * - USGS earthquakes
 * - EPA pollution
 * - DOE energy flux
 */

export const UniversalMappingRules: MappingRuleSet = {
  pillarRules: {
    medical: [
      { sourceKey: "infectionRate", targetKey: "strain", scale: 1 },
      { sourceKey: "hospitalLoad", targetKey: "capacityStress", scale: 1 }
    ],

    humanitarian: [
      { sourceKey: "displacement", targetKey: "pressure", scale: 1 },
      { sourceKey: "casualties", targetKey: "severity", scale: 1 }
    ],

    resources: [
      { sourceKey: "droughtIndex", targetKey: "waterStress", scale: 1 },
      { sourceKey: "cropLoss", targetKey: "foodStress", scale: 1 }
    ],

    economy: [
      { sourceKey: "sovereignRisk", targetKey: "instability", scale: 1 },
      { sourceKey: "currencyStress", targetKey: "volatility", scale: 1 }
    ],

    governance: [
      { sourceKey: "regulatoryPressure", targetKey: "oversight", scale: 1 },
      { sourceKey: "corruptionIndex", targetKey: "capture", scale: 1 }
    ],

    markets: [
      { sourceKey: "tradeImbalance", targetKey: "stress", scale: 1 },
      { sourceKey: "marketManipulation", targetKey: "distortion", scale: 1 }
    ],

    crime: [
      { sourceKey: "traffickingRate", targetKey: "severity", scale: 1 },
      { sourceKey: "organizedCrime", targetKey: "influence", scale: 1 }
    ],

    quantum: [
      { sourceKey: "reactorFlux", targetKey: "fluxStability", scale: 1 },
      { sourceKey: "magneticConfinement", targetKey: "containment", scale: 1 }
    ]
  },

  globalRules: [
    // NASA + NOAA + USGS + EPA
    { sourceKey: "co2ppm", targetKey: "collapsePressure", scale: 0.001 },
    { sourceKey: "methanePpm", targetKey: "collapsePressure", scale: 0.002 },
    { sourceKey: "oceanTemp", targetKey: "risk", scale: 0.05 },
    { sourceKey: "solarFlareIntensity", targetKey: "risk", scale: 0.1 },
    { sourceKey: "geomagneticStorm", targetKey: "instability", scale: 0.1 },
    { sourceKey: "earthquakeMagnitude", targetKey: "collapsePressure", scale: 0.2 },
    { sourceKey: "pollutionIndex", targetKey: "collapsePressure", scale: 0.01 },

    // WHO
    { sourceKey: "globalInfectionRate", targetKey: "risk", scale: 0.05 },
    { sourceKey: "pandemicSeverity", targetKey: "collapsePressure", scale: 0.1 },

    // IMF / World Bank
    { sourceKey: "globalDebtStress", targetKey: "instability", scale: 0.05 },
    { sourceKey: "inflationRate", targetKey: "risk", scale: 0.02 },

    // FTC / governance
    { sourceKey: "antitrustViolations", targetKey: "instability", scale: 0.03 }
  ],

  nodeRules: [
    { sourceKey: "localStormSeverity", targetKey: "weatherStress", scale: 1 },
    { sourceKey: "localOutbreak", targetKey: "healthStress", scale: 1 },
    { sourceKey: "localCrimeRate", targetKey: "crimeStress", scale: 1 },
    { sourceKey: "localResourceLoss", targetKey: "resourceStress", scale: 1 }
  ]
}