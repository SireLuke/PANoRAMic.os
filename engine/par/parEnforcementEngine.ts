// engine/par/parEnforcementEngine.ts

export function enforceParRules({
  par,
  salaries,
  markets,
  ecology,
  infrastructure,
}: {
  par: any
  salaries: any
  markets: any
  ecology: any
  infrastructure: any
}) {
  let parCapCompliance = true
  let warnings: string[] = []

  // Enforce dignity floor
  if (salaries.dignityFloor < 50) {
    warnings.push("Dignity floor critically low — raising minimum.")
    salaries.dignityFloor = 50
  }

  // Enforce stewardship salary
  if (salaries.stewardshipSalary < salaries.dignityFloor) {
    warnings.push("Stewardship salary below dignity floor — correcting.")
    salaries.stewardshipSalary = salaries.dignityFloor + 20
  }

  // Enforce contribution salary
  if (salaries.contributionSalary < salaries.dignityFloor) {
    warnings.push("Contribution salary below dignity floor — correcting.")
    salaries.contributionSalary = salaries.dignityFloor + 10
  }

  // Enforce PAR Cap
  if (par.parMintRate > par.parCap) {
    warnings.push("PAR mint rate exceeds PAR Cap — reducing mint rate.")
    par.parMintRate = par.parCap
    parCapCompliance = false
  }

  // Enforce extraction pressure limits
  if (markets.extractivePressureIndex > 0.7) {
    warnings.push("Extraction pressure dangerously high — activating dampening.")
    markets.extractivePressureIndex *= 0.8
  }

  // Enforce ecological protection
  if (ecology.degradationIndex > ecology.regenerationIndex) {
    warnings.push("Ecology degrading faster than regenerating — activating eco‑shield.")
    ecology.degradationIndex *= 0.9
  }

  // Enforce infrastructure protection
  if (infrastructure.failureIndex > 0.5) {
    warnings.push("Infrastructure failure rising — activating resilience boost.")
    infrastructure.failureIndex *= 0.85
  }

  return {
    par,
    salaries,
    markets,
    ecology,
    infrastructure,
    parCapCompliance,
    warnings,
  }
}

