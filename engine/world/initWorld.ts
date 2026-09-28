// engine/world/initWorld.ts

import { WorldState } from "./worldState.ts"
import { NodeProfile } from "../../core/pillars/nodes/NodeProfile.ts"
import { createNodeMap } from "../../nodeMap/nodeMap.ts"

// Initializers for subsystem slices
// (Replace these with your real subsystem initializers as needed)
function initPopulation() {
  return { total: 0, distribution: {} }
}

function initResources() {
  return {
    resourceScore: 0,
    scarcityScore: 0,
    sustainabilityScore: 0,
  }
}

function initGovernance() {
  return { panitarianScore: 0 }
}

function initRights() {
  return { accessScore: 0 }
}

function initEducation() {
  return { equityScore: 0 }
}

function initEconomy() {
  return {
    parSupply: 0,
    parCap: 0,
    stewardshipFund: 0,
    humanitarianPool: 0,
    taxLoad: 0,
  }
}

function initEcology() {
  return { healthScore: 0 }
}

function initMetabolism() {
  return { renewables: 0 }
}

function initInfrastructure() {
  return { integrityScore: 0 }
}

function initHumanitarian() {
  return { needScore: 0, reliefScore: 0 }
}

function initMigration() {
  return { migrationScore: 0 }
}

function initTrafficking() {
  return { traffickingScore: 0 }
}

function initHarmIndex() {
  return { harmScore: 0 }
}

function initICC() {
  return { score: 0 }
}

function initSynthesis() {
  return { weights: 0 }
}

function initClassified() {
  return { records: {} }
}

// Main initializer
export function initWorld(profiles: NodeProfile[]): WorldState {
  const nodes = createNodeMap(profiles)

  return {
    tick: 0,

    nodes,

    population: initPopulation(),
    resources: initResources(),
    governance: initGovernance(),
    rights: initRights(),
    education: initEducation(),
    economy: initEconomy(),
    ecology: initEcology(),
    metabolism: initMetabolism(),
    infrastructure: initInfrastructure(),
    humanitarian: initHumanitarian(),
    migration: initMigration(),
    trafficking: initTrafficking(),
    harmindex: initHarmIndex(),
    icc: initICC(),
    synthesis: initSynthesis(),

    classified: initClassified(),
  }
}
