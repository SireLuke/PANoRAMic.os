// engine/par/parEnforcementEngine.ts

import { ParState } from "../../core/pillars/par/PAR_STATE"
import { ModesState } from "../../core/pillars/modes/MODES_STATE"
import { NodeState } from "../../core/pillars/nodes/NODES_STATE"

export function enforceParRules({
  par,
  modes,
  nodes,
}: {
  par: ParState
  modes: ModesState
  nodes: NodeState[]
}) {
  // -----------------------------
  // 1. DIGNITY FLOOR ENFORCEMENT
  // -----------------------------
  const dignityFloorEnforced =
    par.dignityFloor < par.parCap * 0.000001
      ? par.parCap * 0.000001
      : par.dignityFloor

  // -----------------------------
  // 2. STEWARDSHIP SALARY CAP
  // -----------------------------
  const maxStewardshipSalary = par.parCap * 0.00002 // 0.002% of PAR cap
  const stewardshipSalaryEnforced =
    par.stewardshipSalary > maxStewardshipSalary
      ? maxStewardshipSalary
      : par.stewardshipSalary

  // -----------------------------
  // 3. CONTRIBUTION SALARY CAP
  // -----------------------------
  const maxContributionSalary = par.parCap * 0.00001 // 0.001% of PAR cap
  const contributionSalaryEnforced =
    par.contributionSalary > maxContributionSalary
      ? maxContributionSalary
      : par.contributionSalary

  // -----------------------------
  // 4. ANTI-EXTRACTION RULES
  // -----------------------------
  const antiExtractionPenalty =
    modes.activeMode === "emergency"
      ? 0.5 // cut minting in half during emergency
      : modes.activeMode === "market_stabilization"
      ? 0.25 // reduce minting by 25%
      : 0

  const parMintRateEnforced = Math.max(
    par.parMintRate - antiExtractionPenalty,
    0
  )

  // -----------------------------
  // 5. NODE-BASED PAR DISTRIBUTION
  // -----------------------------
  const nodeDividendEnforced = nodes.map(node => {
    const rawDividend = node.nodeHealthIndex + node.nodeAutonomyIndex
    const cappedDividend = Math.min(rawDividend * 0.01, par.parCap * 0.000005)
    return {
      nodeId: node.nodeId,
      dividend: cappedDividend,
    }
  })

  // -----------------------------
  // 6. MODE-BASED THROTTLING
  // -----------------------------
  let parVelocityEnforced = par.parVelocity

  if (modes.activeMode === "ecology_restoration") {
    parVelocityEnforced *= 0.8 // slow PAR movement to stabilize ecology
  }

  if (modes.activeMode === "infrastructure_expansion") {
    parVelocityEnforced *= 1.2 // speed PAR movement to support building
  }

  if (modes.activeMode === "emergency") {
    parVelocityEnforced *= 0.5 // slow everything down
  }

  // Hard cap to prevent runaway inflation
  parVelocityEnforced = Math.min(parVelocityEnforced, par.parCap * 0.0001)

  // -----------------------------
  // 7. PAR CAP COMPLIANCE
  // -----------------------------
  const totalSalary =
    dignityFloorEnforced +
    stewardshipSalaryEnforced +
    contributionSalaryEnforced +
    nodeDividendEnforced.reduce((sum, n) => sum + n.dividend, 0)

  const parCapCompliance = totalSalary <= par.parCap

  // -----------------------------
  // RETURN ENFORCED PAR STATE
  // -----------------------------
  return {
    dignityFloor: dignityFloorEnforced,
    stewardshipSalary: stewardshipSalaryEnforced,
    contributionSalary: contributionSalaryEnforced,
    nodeDividend: nodeDividendEnforced,
    parMintRate: parMintRateEnforced,
    parVelocity: parVelocityEnforced,
    parCapCompliance,
  }
}
