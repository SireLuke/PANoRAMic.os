// core/SystemState.ts

export type EcologyState = {
  regenerationIndex: number
  degradationIndex: number
}

export type InfrastructureState = {
  resilienceIndex: number
  failureIndex: number
}

export type MarketsState = {
  stabilityIndex: number
  extractivePressureIndex: number
  cooperativeMarketShare: number
}

export type ModesState = {
  activeMode: string
  stabilityIndex: number
  responsivenessIndex: number
}

export type ParState = {
  parCap: number
  parMintRate: number
  parVelocity: number

  dignityFloor: number
  stewardshipSalary: number
  contributionSalary: number
  nodeDividend: number

  parCapCompliance: boolean

  population: number
  dignityFloat: number
  resourceModifier: number
}

export type MicroAiState = {
  microAiCoverageIndex: number
  retrievalQualityIndex: number
  nodeIntelligenceIndex: number
}

export type WorkforceRotationState = {
  skillGainRate: number
  rotationIndex: number
}

export type NodeState = {
  id: string
  nodeHealthIndex: number
  nodeAiPresenceIndex: number
  nodeConnectivityIndex: number
}

export type DashboardState = {
  globalHealth: number
  globalStability: number
  globalRisk: number
  globalSynthesis: number
  catastropheProbability: number
  immuneSystemActive: boolean
  activeMode: string
  par: any
  ecology: any
  infrastructure: any
  markets: any
  nodes: number
}

export type AuditState = any

export type SystemState = {
  ecology: EcologyState
  infrastructure: InfrastructureState
  markets: MarketsState
  modes: ModesState
  par: ParState
  microAi: MicroAiState
  workforceRotation: WorkforceRotationState
  nodes: NodeState[]
  dashboard: DashboardState | null
  audit: AuditState | null
}
