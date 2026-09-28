// core/pillars/health/MedicalSubsystemEngine.ts
// Medical Subsystem Engine: Aggregates normalized scores and produces global signals

import {
  MedicalSubsystemState,
  MedicalDataSource,
  MedicalAggregatedState,
  MedicalGlobalSignals,
  MedicalAuditResult,
} from './MedicalState'
import { MedicalMetricsNormalizer } from './MedicalMetrics'

export class MedicalSubsystemEngine {
  /**
   * Process a tick: pull data from sources, normalize, merge, aggregate
   */
  static processTick(state: MedicalSubsystemState, tick: number): MedicalSubsystemState {
    // Step 1: Normalize each source
    const whoNormalized = state.sources.WHO
      ? MedicalMetricsNormalizer.normalizeWHO(state.sources.WHO)
      : {}
    const owidNormalized = state.sources.OWID
      ? MedicalMetricsNormalizer.normalizeOWID(state.sources.OWID)
      : {}
    const ochaNormalized = state.sources.OCHA
      ? MedicalMetricsNormalizer.normalizeOCHA(state.sources.OCHA)
      : {}

    // Step 2: Merge with highest confidence
    const normalized = MedicalMetricsNormalizer.mergeNormalizedScores(
      whoNormalized,
      owidNormalized,
      ochaNormalized
    )

    // Step 3: Aggregate into final scores
    const aggregated = this.aggregateScores(normalized)

    // Step 4: Generate global signals
    const currentSignals = this.generateGlobalSignals(aggregated)

    // Step 5: Run RAMS audit
    const auditState = this.performRAMSAudit(state, aggregated)

    // Update history
    const signalHistory = [
      ...state.signalHistory.slice(-99), // Keep last 100 ticks
      currentSignals,
    ]

    return {
      ...state,
      normalized,
      aggregated,
      currentSignals,
      auditState,
      lastTickProcessed: tick,
      signalHistory,
    }
  }

  /**
   * Aggregate normalized scores into final medical state
   */
  private static aggregateScores(normalized: any): MedicalAggregatedState {
    // Medical Stability: combination of access, infrastructure, and relief
    const medicalStability =
      (normalized.medicalAccess.value +
        normalized.medicalInfrastructure.value +
        (1 - normalized.medicalScarcity.value)) /
      3

    // Medical Risk: high need + crisis + low resilience
    const medicalRisk =
      (normalized.medicalNeed.value +
        normalized.medicalCrisisScore.value +
        (1 - normalized.medicalResilience.value)) /
      3

    // Medical Resilience: inverse of risk, weighted by sustainability
    const medicalResilience =
      (normalized.medicalResilience.value + normalized.medicalSustainability.value) / 2

    // Humanitarian Need: crisis + lack of relief + refugee/emergency metrics
    const medicalHumanitarianNeed =
      (normalized.medicalCrisisScore.value +
        normalized.medicalHumanitarianScore.value +
        (1 - normalized.medicalRelief.value)) /
      3

    // Infrastructure Score: direct measure
    const medicalInfrastructureScore = normalized.medicalInfrastructure.value

    // Crisis Score: direct measure
    const medicalCrisisScore = normalized.medicalCrisisScore.value

    return {
      medicalStability: Math.max(0, Math.min(1, medicalStability)),
      medicalRisk: Math.max(0, Math.min(1, medicalRisk)),
      medicalResilience: Math.max(0, Math.min(1, medicalResilience)),
      medicalHumanitarianNeed: Math.max(0, Math.min(1, medicalHumanitarianNeed)),
      medicalInfrastructureScore: Math.max(0, Math.min(1, medicalInfrastructureScore)),
      medicalCrisisScore: Math.max(0, Math.min(1, medicalCrisisScore)),
    }
  }

  /**
   * Generate global signals from aggregated state
   * These feed dashboard, CLI, synthesis, audits, regulation
   */
  private static generateGlobalSignals(aggregated: MedicalAggregatedState): MedicalGlobalSignals {
    return {
      medicalNeed: aggregated.medicalHumanitarianNeed,
      medicalRelief: 1 - aggregated.medicalScarcity,
      medicalScarcity: aggregated.medicalRisk,
      medicalSustainability: aggregated.medicalResilience,
      medicalRisk: aggregated.medicalRisk,
      medicalResilience: aggregated.medicalResilience,
      medicalAccess: 1 - aggregated.medicalRisk,
      medicalInfrastructure: aggregated.medicalInfrastructureScore,
      medicalCrisisScore: aggregated.medicalCrisisScore,
      timestamp: Date.now(),
    }
  }

  /**
   * RAMS Audit: Check for violations in medical systems
   */
  private static performRAMSAudit(
    state: MedicalSubsystemState,
    aggregated: MedicalAggregatedState
  ): MedicalAuditResult {
    const violations: string[] = []
    const details = {
      corruptionInMedicalSystems: false,
      accessInequality: false,
      humanitarianNeglect: false,
      crisisResponseFailure: false,
      supplyChainCollapse: false,
      rightsViolationsInHealthcare: false,
      transparencyFailure: false,
    }

    // Check for access inequality
    if (aggregated.medicalRisk > 0.7) {
      details.accessInequality = true
      violations.push('High medical access inequality detected (risk > 0.7)')
    }

    // Check for humanitarian neglect
    if (aggregated.medicalHumanitarianNeed > 0.6 && aggregated.medicalInfrastructureScore < 0.4) {
      details.humanitarianNeglect = true
      violations.push('Humanitarian neglect: high need with low infrastructure response')
    }

    // Check for crisis response failure
    if (aggregated.medicalCrisisScore > 0.5 && aggregated.medicalResilience < 0.3) {
      details.crisisResponseFailure = true
      violations.push('Crisis response failure: high crisis score with low resilience')
    }

    // Check for supply chain collapse
    if (aggregated.medicalRisk > 0.75) {
      details.supplyChainCollapse = true
      violations.push('Potential supply chain collapse: medical risk critically high')
    }

    // Check for data transparency (no sources = transparency failure)
    if (
      !state.sources.WHO &&
      !state.sources.OWID &&
      !state.sources.OCHA
    ) {
      details.transparencyFailure = true
      violations.push('Medical data transparency failure: no data sources available')
    }

    return {
      ok: violations.length === 0,
      reason: violations.length > 0 ? violations.join('; ') : null,
      details,
    }
  }

  /**
   * Update a data source (WHO, OWID, or UN-OCHA)
   */
  static updateDataSource(
    state: MedicalSubsystemState,
    source: MedicalDataSource
  ): MedicalSubsystemState {
    const updated = { ...state }
    if (source.name === 'WHO') updated.sources.WHO = source
    else if (source.name === 'OWID') updated.sources.OWID = source
    else if (source.name === 'UN-OCHA') updated.sources.OCHA = source

    return updated
  }

  /**
   * Get current medical stability (key metric for synthesis engine)
   * Medical stability is one of the heaviest weights in synthesis vector
   */
  static getMedicalStabilityWeight(): number {
    // Returns a weight value (0-1) for use in synthesis calculations
    // Medical is critical to global coherence
    return 0.85 // High weight in synthesis engine
  }

  /**
   * Influence on other subsystems
   */
  static getInfluenceOnSynthesis(aggregated: MedicalAggregatedState): Record<string, number> {
    return {
      coherence: aggregated.medicalStability * 0.9, // Medical stability drives coherence
      humanitarianAlignment: aggregated.medicalHumanitarianNeed * 0.95, // Humanitarian weight
      governanceIntegrity: 1 - aggregated.medicalRisk * 0.7, // Risk undermines integrity
      resourceSustainability: aggregated.medicalResilience * 0.85, // Resilience = sustainability
      rightsAndLaborDignity: 1 - aggregated.medicalRisk * 0.8, // Risk threatens rights
      marketFairness: aggregated.medicalAccess * 0.75, // Access correlation to fairness
      commonsOpenness: aggregated.medicalInfrastructureScore * 0.7, // Public health = commons
    }
  }
}
