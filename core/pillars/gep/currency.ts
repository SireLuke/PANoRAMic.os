// core/pillars/gep/Currency.ts

export interface CurrencyProfile {
  code: string               // e.g., USD, EUR, JPY
  name: string               // e.g., United States Dollar
  nation: string             // issuing nation
  exchangeRateToUSD: number  // conversion rate
  inflationRate: number      // annual inflation %
  ppp: number                // purchasing power parity
  stabilityIndex: number     // 0–1 stability score
  currencyRiskIndex: number  // 0–1 risk score
}

export function computeGlobalCurrencyMetrics(currencies: CurrencyProfile[]) {
  const avgInflation =
    currencies.reduce((sum, c) => sum + c.inflationRate, 0) / currencies.length

  const avgPPP =
    currencies.reduce((sum, c) => sum + c.ppp, 0) / currencies.length

  const avgStability =
    currencies.reduce((sum, c) => sum + c.stabilityIndex, 0) / currencies.length

  const avgRisk =
    currencies.reduce((sum, c) => sum + c.currencyRiskIndex, 0) / currencies.length

  return {
    avgInflation,
    avgPPP,
    avgStability,
    avgRisk,
  }
}

export function evaluateCurrencyHealth(currency: CurrencyProfile) {
  let healthScore =
    currency.stabilityIndex * 60 +
    (1 - currency.currencyRiskIndex) * 40

  // Inflation reduces health
  healthScore -= currency.inflationRate * 0.5

  // PPP mismatch reduces health
  if (currency.ppp < 0.8 || currency.ppp > 1.2) {
    healthScore -= 10
  }

  // Normalize to 0–100
  healthScore = Math.max(0, Math.min(healthScore, 100))

  let healthMode = "stable"
  if (healthScore < 40) healthMode = "critical"
  else if (healthScore < 70) healthMode = "unstable"

  return {
    healthScore,
    healthMode,
  }
}