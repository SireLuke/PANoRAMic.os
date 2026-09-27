// engine/par/parEngine.ts

import { ParState } from "../../core/pillars/par/PAR_STATE"
import { WorkforceRotationState } from "../../core/pillars/workforce/WORKFORCE_ROTATION_STATE"
import { ModesState } from "../../core/pillars/modes/MODES_STATE"
import { NodeState } from "../../core/pillars/nodes/NODES_STATE"
import { MarketsState } from "../../core/pillars/markets/MARKETS_STATE"
import { EcologyState } from "../../core/pillars/ecology/ECOLOGY_STATE"
import { InfrastructureState } from "../../core/pillars/infrastructure/INFRASTRUCTURE_STATE"

import { computeParCap } from "../../core/pillars/par/PAR_CAP"
import { computeParSalary } from "./parSalaryEngine"
import { enforceParRules } from "./parEnforcementEngine"

export function computePar({
  par,
  workforceRotation,
  modes,
  nodes,
  markets,
  ecology,
  infrastructure,
}: {
  par: ParState
  workforceRotation: WorkforceRotationState
  modes: ModesState
  nodes: NodeState[]
  markets: MarketsState
  ecology: EcologyState
  infrastructure: InfrastructureState
}): ParState {
  // 1. Compute PAR Cap
  const parCap = computeParCap({
    population: par.population,
    dignityFloat: par.dignityFloat,
    resourceModifier: par.resourceModifier,
    marketBurden: markets.extractivePressureIndex,
    ecologyRegen: ecology.regenerationIndex,
    infrastructureResilience: infrastructure.resilienceIndex,
  })

  // 2. Compute PAR Salary Logic
  const parSalary = computeParSalary({
    par,
    workforceRotation,
    nodes,
  })

  // 3. Build preliminary PAR state (before enforcement)
  const parPreEnforcement: ParState = {
    ...par,
    parCap,

    parVelocity:
      workforceRotation.skillGainRate +
      markets.cooperativeMarketShare,

    parMintRate:
      (parCap * 0.01) +
      ecology.regenerationIndex +
      infrastructure.resilienceIndex -
      markets.extractivePressureIndex,

    dignityFloor: parSalary.dignityFloor,
    stewardshipSalary: parSalary.stewardshipSalary,
    contributionSalary: parSalary.contributionSalary,
    nodeDividend: parSalary.nodeDividend,
  }

  // 4. Enforce rules
  const enforced = enforceParRules({
    par: parPreEnforcement,
    modes,
    nodes,
  })

  // 5. Return final PAR state
  return {
    ...parPreEnforcement,
    dignityFloor: enforced.dignityFloor,
    stewardshipSalary: enforced.stewardshipSalary,
    contributionSalary: enforced.contributionSalary,
    nodeDividend: enforced.nodeDividend,
    parMintRate: enforced.parMintRate,
    parVelocity: enforced.parVelocity,
    parCapCompliance: enforced.parCapCompliance,
  }
}
