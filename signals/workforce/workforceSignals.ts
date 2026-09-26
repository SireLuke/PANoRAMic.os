import { WorkforceState } from "../../core/pillars/workforce/WORKFORCE_STATE"

export function emitWorkforceSignals(state: WorkforceState) {
  return {
    workforceParticipation: state.participationRate,
    workforceDignity: state.dignityAccessScore,
    workforceSkills: state.skillDevelopmentIndex,
    workforceEcoImpact: state.ecologicalImpactScore,
    workforceCommunityImpact: state.communityImpactScore,
    workforceParFlow: state.parEarningsFlow,
    workforceReintegration: state.reintegrationScore,
  }
}

