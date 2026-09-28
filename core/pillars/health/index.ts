// core/pillars/health/index.ts
// Medical subsystem exports

export {
  MedicalMetric,
  MedicalNormalizedScores,
  MedicalAggregatedState,
  MedicalDataSource,
  MedicalAuditResult,
  MedicalGlobalSignals,
  MedicalSubsystemState,
} from './MedicalState'

export { MedicalMetricsNormalizer } from './MedicalMetrics'
export { MedicalSubsystemEngine } from './MedicalSubsystemEngine'
export { MedicalDataIntegration } from './MedicalDataIntegration'
