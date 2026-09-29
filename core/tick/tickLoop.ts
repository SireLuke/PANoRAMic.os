// core/tick/tickLoop.ts

import { WorldState } from "../worldstate/WorldState"
import { updateNodeMap } from "../../nodeMap/updateNodeMap"
import { computeGlobalSignals } from "../worldstate/globalSignalsEngine"

import { updatePopulation } from "../pillars/population/populationEngine"
import { updateResources } from "../pillars/resources/resourcesEngine"
import { updateEconomy } from "../pillars/economy/economyEngine"
import { updateGovernance } from "../pillars/governance/governanceEngine"
import { updateHumanitarian } from "../pillars/humanitarian/humanitarianEngine"
import { updateMedical } from "../pillars/medical/medicalEngine"
import { updateAntiGenocide } from "../pillars/antigenocide/antigenocideEngine"
import { updateMarkets } from "../pillars/markets/marketsEngine"
import { updateCrime } from "../pillars/crime/crimeEngine"
import { updateEducation } from "../pillars/education/educationEngine"
import { updateMigration } from "../pillars/migration/migrationEngine"
import { updateTrafficking } from "../pillars/trafficking/traffickingEngine"
import { updateTransparency } from "../pillars/transparency/transparencyEngine"
import { updateCorporateCapture } from "../pillars/corporatecapture/corporateCaptureEngine"
import { updateEpistemic } from "../pillars/epistemic/epistemicEngine"
import { updateRepairability } from "../pillars/repairability/repairabilityEngine"
import { updateQuantum } from "../pillars/quantum/quantumEngine"

export function tick(world: WorldState): WorldState {
  let updated = { ...world }

  // 1. Update nodes
  updated.nodes = updateNodeMap(updated.nodes)

  // 2. Update pillars
  updated.population = updatePopulation(updated)
  updated.resources = updateResources(updated)
  updated.economy = updateEconomy(updated)
  updated.governance = updateGovernance(updated)
  updated.humanitarian = updateHumanitarian(updated)
  updated.medical = updateMedical(updated)
  updated.antigenocide = updateAntiGenocide(updated)
  updated.markets = updateMarkets(updated)
  updated.crime = updateCrime(updated)
  updated.education = updateEducation(updated)
  updated.migration = updateMigration(updated)
  updated.trafficking = updateTrafficking(updated)
  updated.transparency = updateTransparency(updated)
  updated.corporatecapture = updateCorporateCapture(updated)
  updated.epistemic = updateEpistemic(updated)
  updated.repairability = updateRepairability(updated)
  updated.quantum = updateQuantum(updated)

  // 3. Compute global signals
  updated = computeGlobalSignals(updated)

  return updated
}

