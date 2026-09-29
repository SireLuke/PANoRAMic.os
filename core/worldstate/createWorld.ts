// core/worldstate/createWorld.ts

import { WorldState, createWorldState } from "./WorldState"
import { NodeState } from "../pillars/nodes/NODES_STATE"

/**
 * createWorld:
 * Builds the initial world before the tick loop runs.
 * You can later expand this to load real data, seed nodes,
 * or import configurations from JSON.
 */

export function createWorld(): WorldState {
  const world = createWorldState()

  // Example: seed nodes (optional)
  // You can remove this or expand it later.
  const nodeA: NodeState = {
    id: "A",
    name: "Alpha",
    nodeType: "city",
    latitude: 0,
    longitude: 0,
    populationCapacity: 1000,
    resourceCapacity: 1,
    healthIndex: 0.8,
    stressIndex: 0.2,
    autonomyIndex: 0.5,
    connectivityIndex: 0.6,
    stability: 0.7,
    risk: 0.3,
    load: 0.4,
    resilience: 0.6,
    ecologicalDependency: 0.3,
    infrastructureDependency: 0.4,
    economicDependency: 0.5,
    collapseRisk: 0.2,
    connections: ["B"]
  }

  const nodeB: NodeState = {
    id: "B",
    name: "Beta",
    nodeType: "city",
    latitude: 1,
    longitude: 1,
    populationCapacity: 800,
    resourceCapacity: 0.8,
    healthIndex: 0.75,
    stressIndex: 0.25,
    autonomyIndex: 0.45,
    connectivityIndex: 0.55,
    stability: 0.65,
    risk: 0.35,
    load: 0.45,
    resilience: 0.55,
    ecologicalDependency: 0.35,
    infrastructureDependency: 0.45,
    economicDependency: 0.55,
    collapseRisk: 0.25,
    connections: ["A"]
  }

  world.nodes = {
    A: nodeA,
    B: nodeB
  }

  return world
}
