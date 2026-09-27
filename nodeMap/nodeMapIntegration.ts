// nodeMap/nodeMapIntegration.ts

import { NodeMap, createNodeMap } from "./nodeMap"
import { updateNodes, emitNodeMapSignals, auditNodeMap } from "./nodeMap"
import { evolveNodeMap } from "./nodeEvolutionEngine"
import { propagateStress } from "./nodeConnections"

import { globalSignals } from "../signals/globalSignals"
import { modesEngine } from "../engine/modes/modesEngine"
import { dashboardEngine } from "../engine/dashboard/dashboardEngine"
import { systemAudit } from "../rams/system/systemAudit"

/**
 * NodeMapIntegration
 *
 * This module integrates the unified node map into:
 * - globalLoop
 * - systemLoop
 * - signals
 * - modes
 * - RAMS
 * - dashboard
 * - API
 */

export interface NodeMapIntegration {
  map: NodeMap
}

/**
 * Initialize the node map integration layer
 */
export function initNodeMapIntegration(): NodeMapIntegration {
  const map = createNodeMap()
  return { map }
}

/**
 * Run one full integration tick
 */
export function runNodeMapIntegration(integration: NodeMapIntegration) {
  const { map } = integration

  // 1. Stress propagation across connections
  propagateStress(map)

  // 2. Update node states using node engines
  updateNodes(map)

  // 3. Evolve nodes over time
  evolveNodeMap(map)

  // 4. Emit node signals
  const nodeSignals = emitNodeMapSignals(map)

  // 5. Merge node signals into global signals
  globalSignals.nodes = nodeSignals

  // 6. Run modes engine using updated signals
  const modesState = modesEngine(globalSignals)

  // 7. Run RAMS audits on node map
  const nodeAudits = auditNodeMap(map)
  const systemAudits = systemAudit(globalSignals)

  // 8. Push everything into dashboard
  dashboardEngine.update({
    nodeMap: map,
    nodeSignals,
    nodeAudits,
    modesState,
    systemAudits,
  })

  // 9. Return updated integration state
  return integration
}
