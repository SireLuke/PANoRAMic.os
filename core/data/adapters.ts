// core/data/adapters.ts

import { registerFunnel } from "./funnelManager"

/**
 * Utility:
 * Safely merge incoming pillar data into the world.
 */
function mergePillar(world: any, pillarName: string, incoming: any): any {
  return {
    ...world,
    [pillarName]: {
      ...world[pillarName],
      ...incoming[pillarName]
    }
  }
}

/**
 * Utility:
 * Safely merge incoming node data into the world.
 */
function mergeNodes(world: any, incoming: any): any {
  const updatedNodes: any = { ...world.nodes }

  for (const id in incoming.nodes) {
    updatedNodes[id] = {
      ...world.nodes[id],
      ...incoming.nodes[id]
    }
  }

  return {
    ...world,
    nodes: updatedNodes
  }
}

/**
 * Utility:
 * Merge global signals.
 */
function mergeGlobal(world: any, incoming: any): any {
  return {
    ...world,
    globalSignals: {
      ...world.globalSignals,
      ...incoming.globalSignals
    }
  }
}

/**
 * Create adapters for each funnel type.
 * These will be expanded in Steps 25–29.
 */

// Node adapter
registerFunnel("nodes", (incoming, world) => {
  return mergeNodes(world, incoming)
})

// Global signals adapter
registerFunnel("global", (incoming, world) => {
  return mergeGlobal(world, incoming)
})

// Pillar adapters
const pillarNames = [
  "population",
  "resources",
  "economy",
  "governance",
  "medical",
  "humanitarian",
  "markets",
  "crime",
  "education",
  "migration",
  "trafficking",
  "transparency",
  "corporatecapture",
  "epistemic",
  "repairability",
  "quantum"
]

pillarNames.forEach(pillarName => {
  registerFunnel(pillarName as any, (incoming, world) => {
    return mergePillar(world, pillarName, incoming)
  })
})

// Placeholder for Library of Alexandria (Step 30)
registerFunnel("libraryOfAlexandria", (incoming, world) => {
  console.warn("Library of Alexandria adapter not implemented yet.")
  return world
})
