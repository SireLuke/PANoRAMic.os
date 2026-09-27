// engine/global/globalLoopIntegration.ts

import { initNodeMapIntegration, runNodeMapIntegration } from "../../nodeMap/nodeMapIntegration"
import { globalSignals } from "../../signals/globalSignals"
import { modesEngine } from "../modes/modesEngine"
import { dashboardEngine } from "../dashboard/dashboardEngine"
import { systemAudit } from "../../rams/system/systemAudit"
import { runPARFlowEngine } from "../par/PARFlowEngine"
import { runRightsFlowEngine } from "../rights/RightsFlowEngine"
import { runEcologyFlowEngine } from "../ecology/EcologyFlowEngine"
import { runInfrastructureFlowEngine } from "../infrastructure/InfrastructureFlowEngine"
import { runCommonsFlowEngine } from "../commons/CommonsFlowEngine"
import { runGovernanceFlowEngine } from "../governance/GovernanceFlowEngine"
import { runPopulationFlowEngine } from "../population/PopulationFlowEngine"

export interface GlobalLoopIntegration {
  tick: number
  nodeMapIntegration: ReturnType<typeof initNodeMapIntegration>
}

/**
 * Initialize the global loop integration layer
 */
export function initGlobalLoopIntegration(): GlobalLoopIntegration {
  return {
    tick: 0,
    nodeMapIntegration: initNodeMapIntegration(),
  }
}

/**
 * Run one full global integration tick
 */
export function runGlobalLoopIntegration(state: GlobalLoopIntegration) {
  state.tick++

  // 1. Integrate node map (nervous system)
  runNodeMapIntegration(state.nodeMapIntegration)

  // 2. Run pillar engines (organs)
  const parState = runPARFlowEngine(globalSignals)
  const rightsState = runRightsFlowEngine(globalSignals)
  const ecologyState = runEcologyFlowEngine(globalSignals)
  const infraState = runInfrastructureFlowEngine(globalSignals)
  const commonsState = runCommonsFlowEngine(globalSignals)
  const governanceState = runGovernanceFlowEngine(globalSignals)
  const populationState = runPopulationFlowEngine(globalSignals)

  // 3. Run modes (reflexes)
  const modesState = modesEngine(globalSignals)

  // 4. Run RAMS audits (immune system)
  const systemAudits = systemAudit(globalSignals)

  // 5. Update dashboard (planet view)
  dashboardEngine.update({
    tick: state.tick,
    nodeMap: state.nodeMapIntegration.map,
    signals: globalSignals,
    modesState,
    systemAudits,
    parState,
    rightsState,
    ecologyState,
    infraState,
    commonsState,
    governanceState,
    populationState,
  })

  return state
}
