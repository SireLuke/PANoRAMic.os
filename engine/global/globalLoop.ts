// engine/global/globalLoop.ts

import { computeMarketFlow, computeMarketRisk, computeMarketStability, computeMarketSynthesis, applyMarketCollapse, applyMarketRecovery } from "../markets"
import { computeEcologyFlow, computeEcologyRisk, computeEcologyStability, computeEcologySynthesis, applyEcologyCollapse, applyEcologyRecovery } from "../ecology"
import { computeInfrastructureFlow, computeInfrastructureRisk, computeInfrastructureStability, computeInfrastructureSynthesis, applyInfrastructureCollapse, applyInfrastructureRecovery } from "../infrastructure"
import { computeWorkforceFlow, computeWorkforceRisk, computeWorkforceStability, computeWorkforceSynthesis, applyWorkforceCollapse, applyWorkforceRecovery } from "../workforce"
import { computeGovernanceFlow, computeGovernanceRisk, computeGovernanceStability, computeGovernanceSynthesis, applyGovernanceCollapse, applyGovernanceRecovery } from "../governance"
import { computePopulationFlow, computePopulationRisk, computePopulationStability, computePopulationSynthesis, applyPopulationCollapse, applyPopulationRecovery } from "../population"
import { computeRightsFlow, computeRightsRisk, computeRightsStability, computeRightsSynthesis, applyRightsCollapse, applyRightsRecovery } from "../rights"
import { computePARFlow, computePARRisk, computePARStability, computePARSynthesis, applyPARCollapse, applyPARRecovery } from "../par"
import { computeCommonsFlow, computeCommonsRisk, computeCommonsStability, computeCommonsSynthesis, applyCommonsCollapse, applyCommonsRecovery } from "../commons"

export function runGlobalLoop(state: any) {
  const actions: string[] = []

  // FLOW
  actions.push("Running flow engines...")
  computeMarketFlow(state.markets)
  computeEcologyFlow(state.ecology)
  computeInfrastructureFlow(state.infrastructure)
  computeWorkforceFlow(state.workforce)
  computeGovernanceFlow(state.governance)
  computePopulationFlow(state.population)
  computeRightsFlow(state.rights)
  computePARFlow(state.par)
  computeCommonsFlow(state.commons)

  // COLLAPSE
  actions.push("Applying collapse engines...")
  applyMarketCollapse(state.markets)
  applyEcologyCollapse(state.ecology)
  applyInfrastructureCollapse(state.infrastructure)
  applyWorkforceCollapse(state.workforce)
  applyGovernanceCollapse(state.governance)
  applyPopulationCollapse(state.population)
  applyRightsCollapse(state.rights)
  applyPARCollapse(state.par)
  applyCommonsCollapse(state.commons)

  // RECOVERY
  actions.push("Applying recovery engines...")
  applyMarketRecovery(state.markets)
  applyEcologyRecovery(state.ecology)
  applyInfrastructureRecovery(state.infrastructure)
  applyWorkforceRecovery(state.workforce)
  applyGovernanceRecovery(state.governance)
  applyPopulationRecovery(state.population)
  applyRightsRecovery(state.rights)
  applyPARRecovery(state.par)
  applyCommonsRecovery(state.commons)

  // RISK
  const risk = {
    markets: computeMarketRisk(state.markets),
    ecology: computeEcologyRisk(state.ecology),
    infrastructure: computeInfrastructureRisk(state.infrastructure),
    workforce: computeWorkforceRisk(state.workforce),
    governance: computeGovernanceRisk(state.governance),
    population: computePopulationRisk(state.population),
    rights: computeRightsRisk(state.rights),
    par: computePARRisk(state.par),
    commons: computeCommonsRisk(state.commons),
  }

  // STABILITY
  const stability = {
    markets: computeMarketStability(state.markets),
    ecology: computeEcologyStability(state.ecology),
    infrastructure: computeInfrastructureStability(state.infrastructure),
    workforce: computeWorkforceStability(state.workforce),
    governance: computeGovernanceStability(state.governance),
    population: computePopulationStability(state.population),
    rights: computeRightsStability(state.rights),
    par: computePARStability(state.par),
    commons: computeCommonsStability(state.commons),
  }

  // SYNTHESIS
  const synthesis = {
    markets: computeMarketSynthesis(state.markets),
    ecology: computeEcologySynthesis(state.ecology),
    infrastructure: computeInfrastructureSynthesis(state.infrastructure),
    workforce: computeWorkforceSynthesis(state.workforce),
    governance: computeGovernanceSynthesis(state.governance),
    population: computePopulationSynthesis(state.population),
    rights: computeRightsSynthesis(state.rights),
    par: computePARSynthesis(state.par),
    commons: computeCommonsSynthesis(state.commons),
  }

  // GLOBAL SYNTHESIS SCORE
  const globalScore =
    synthesis.markets.synthesisScore * 0.1 +
    synthesis.ecology.synthesisScore * 0.1 +
    synthesis.infrastructure.synthesisScore * 0.1 +
    synthesis.workforce.synthesisScore * 0.1 +
    synthesis.governance.synthesisScore * 0.1 +
    synthesis.population.synthesisScore * 0.1 +
    synthesis.rights.synthesisScore * 0.1 +
    synthesis.par.synthesisScore * 0.15 +
    synthesis.commons.synthesisScore * 0.15

  return {
    actions,
    risk,
    stability,
    synthesis,
    globalScore,
  }
}