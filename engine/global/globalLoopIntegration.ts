// engine/global/globalLoopIntegration.ts

import { initNodeMapIntegration, runNodeMapIntegration } from "../../nodeMap/nodeMapIntegration.js"
import { globalSignals } from "../../signals/globalSignals.js"
import { modesEngine } from "../modes/modesEngine.js"
import { dashboardEngine } from "../dashboard/dashboardEngine.js"
import { systemAudit } from "../../rams/system/systemAudit.js"
import { runPARFlowEngine } from "../par/PARFlowEngine.js"
import { runRightsFlowEngine } from "../rights/RightsFlowEngine.js"
import { runEcologyFlowEngine } from "../ecology/EcologyFlowEngine.js"
import { runInfrastructureFlowEngine } from "../infrastructure/InfrastructureFlowEngine.js"
import { runCommonsFlowEngine } from "../commons/CommonsFlowEngine.js"
import { runGovernanceFlowEngine } from "../governance/GovernanceFlowEngine.js"
import { runPopulationFlowEngine } from "../population/PopulationFlowEngine.js"

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
