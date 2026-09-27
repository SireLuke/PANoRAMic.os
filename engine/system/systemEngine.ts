// engine/system/systemEngine.ts

import { SystemState } from "../../core/SystemState"
import { computeWorkforceRotation } from "../workforce/workforceRotationEngine"
import { computeMicroAi } from "../microAI/microAiEngine"
import { computeMarkets } from "../markets/marketsEngine"
import { computeModes } from "../modes/modesEngine"
import { computeParCap } from "../../core/pillars/par/PAR_CAP"
import { computeParSalary } from "../par/parSalaryEngine"
import { auditSystem } from "../../rams/system/systemAudit"

export function computeSystem(state: SystemState): SystemState {

  // 1. Compute subsystem updates
  const workforceRotation = computeWorkforceRotation(state.workforceRotation)
  const microAi = computeMicroAi(state.microAi)
  const markets = computeMarkets(state.markets)
  const modes = computeModes(state.modes)

  // 2. Compute PAR Cap
  const parCap = computeParCap({
    population: state.par.population,
    dignityFloat: state.par.dignityFloat,
    resourceModifier: state.par.resourceModifier,
    marketBurden: markets.extractivePressureIndex,
    ecologyRegen: state.ecology.regenerationIndex,
    infrastructureResilience: state.infrastructure.resilienceIndex,
  })

  // 3. Compute PAR Salary Logic
  const parSalary = computeParSalary({
    par: state.par,
    workforceRotation,
    nodes: state.nodes,
  })

  // 4. Update PAR economy
  const par = {
    ...state.par,

    // PAR Cap (max mintable PAR)
    parCap,

    // PAR Velocity (how fast PAR moves through system)
    parVelocity:
      workforceRotation.skillGainRate +
      markets.cooperativeMarketShare +
      microAi.microAiCoverageIndex,

    // PAR Mint Rate (how much PAR is created this cycle)
    parMintRate:
      (parCap * 0.01) + // 1% of cap per cycle
      state.ecology.regenerationIndex +
      state.infrastructure.resilienceIndex -
      markets.extractivePressureIndex,

    // Salary Logic
    dignityFloor: parSalary.dignityFloor,
    stewardshipSalary: parSalary.stewardshipSalary,
    contributionSalary: parSalary.contributionSalary,
    nodeDividend: parSalary.nodeDividend,
  }

  // 5. Update nodes
  const nodes = state.nodes.map(node => ({
    ...node,
    nodeHealthIndex:
      node.nodeHealthIndex +
      state.ecology.regenerationIndex +
      state.infrastructure.resilienceIndex,

    nodeAiPresenceIndex:
      microAi.nodeIntelligenceIndex +
      microAi.microAiCoverageIndex,
  }))

  // 6. Update modes
  const modesAdjusted = {
    ...modes,
    stabilityIndex:
      markets.stabilityIndex +
      state.ecology.regenerationIndex +
      state.infrastructure.resilienceIndex,

    responsivenessIndex:
      microAi.retrievalQualityIndex +
      workforceRotation.skillGainRate,
  }

  // 7. Build new state
  const newState = {
    ...state,
    workforceRotation,
    microAi,
    markets,
    modes: modesAdjusted,
    par,
    nodes,
  }

  // 8. Global audit
  const audit = auditSystem(newState)

  return {
    ...newState,
    audit,
  }
}

