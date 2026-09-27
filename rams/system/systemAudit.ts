// rams/system/systemAudit.ts
import { SystemState } from "../../core/SystemState"
import { auditMarkets } from "../markets/marketsAudit"
import { auditMicroAi } from "../microAI/microAiAudit"
import { auditWorkforceRotation } from "../workforce/workforceRotationAudit"
import { auditNode } from "../nodes/nodesAudit"

export function auditSystem(state: SystemState) {
  const marketsAudit = auditMarkets(state.markets)
  const microAiAudit = auditMicroAi(state.microAi)
  const workforceAudit = auditWorkforceRotation(state.workforceRotation)
  const nodeAudits = state.nodes.map(auditNode)

  return {
    dataIntegrity: true,
    marketsAudit,
    microAiAudit,
    workforceAudit,
    nodeAudits,
  }
}
