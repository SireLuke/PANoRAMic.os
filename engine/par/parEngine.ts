// engine/par/parEngine.ts

import { computeParCap } from "../../core/pillars/par/PAR_CAP"
import { computeParSalary } from "./parSalaryEngine"
import { enforceParRules } from "./parEnforcementEngine"

export function parEngine(state: any) {
  const { par, ecology, infrastructure, markets, workforceRotation, nodes } = state

  // Compute PAR Cap
  const parCap = computeParCap({
    population: par.population,
    dignityFloat: par.dignityFloat,
    resourceModifier: par.resourceModifier,
    marketBurden: markets.extractivePressureIndex,
    ecologyRegen: ecology.regenerationIndex,
    infrastructureResilience: infrastructure.resilienceIndex,
  })

  par.parCap = parCap

  // Compute salaries
  const salaries = computeParSalary({
    par,
    workforceRotation,
    nodes,
  })

  // Enforce rules
  const enforcement = enforceParRules({
    par,
    salaries,
    markets,
    ecology,
    infrastructure,
  })

  // Update PAR velocity (simple model)
  par.parVelocity = Math.max(
    0.1,
    1 -
      markets.extractivePressureIndex * 0.3 +
      ecology.regenerationIndex * 0.2 +
      infrastructure.resilienceIndex * 0.2
  )

  // Update mint rate (bounded by cap)
  par.parMintRate = Math.min(par.parMintRate, par.parCap)

  return {
    ...state,
    par,
    salaries,
    enforcement,
  }
}

}
