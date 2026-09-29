// core/data/validate.ts

/**
 * validateField:
 * Ensures a field exists and has the correct type.
 * If missing or wrong type, returns a safe default.
 */
export function validateField<T>(
  obj: any,
  key: string,
  defaultValue: T,
  type: string
): T {
  if (obj == null) return defaultValue
  if (typeof obj[key] !== type) return defaultValue
  return obj[key]
}

/**
 * validateNode:
 * Ensures node structure is correct.
 */
export function validateNode(node: any): any {
  return {
    id: validateField(node, "id", "unknown", "string"),
    name: validateField(node, "name", "Unnamed Node", "string"),
    nodeType: validateField(node, "nodeType", "unknown", "string"),

    latitude: validateField(node, "latitude", 0, "number"),
    longitude: validateField(node, "longitude", 0, "number"),

    populationCapacity: validateField(node, "populationCapacity", 0, "number"),
    resourceCapacity: validateField(node, "resourceCapacity", 0, "number"),

    healthIndex: validateField(node, "healthIndex", 0, "number"),
    stressIndex: validateField(node, "stressIndex", 0, "number"),
    autonomyIndex: validateField(node, "autonomyIndex", 0, "number"),
    connectivityIndex: validateField(node, "connectivityIndex", 0, "number"),

    stability: validateField(node, "stability", 0, "number"),
    risk: validateField(node, "risk", 0, "number"),
    load: validateField(node, "load", 0, "number"),
    resilience: validateField(node, "resilience", 0, "number"),
    collapseRisk: validateField(node, "collapseRisk", 0, "number"),

    ecologicalDependency: validateField(node, "ecologicalDependency", 0, "number"),
    infrastructureDependency: validateField(node, "infrastructureDependency", 0, "number"),
    economicDependency: validateField(node, "economicDependency", 0, "number"),

    connections: Array.isArray(node.connections) ? node.connections : []
  }
}

/**
 * validatePillar:
 * Ensures pillar structure is correct.
 */
export function validatePillar(pillar: any, defaults: any): any {
  const out: any = {}
  for (const key in defaults) {
    const expectedType = typeof defaults[key]
    out[key] = validateField(pillar, key, defaults[key], expectedType)
  }
  return out
}

/**
 * validateWorld:
 * Ensures world structure is correct.
 */
export function validateWorld(world: any, pillarDefaults: any): any {
  const validatedNodes: any = {}
  for (const id in world.nodes) {
    validatedNodes[id] = validateNode(world.nodes[id])
  }

  const validatedPillars: any = {}
  for (const pillarName in pillarDefaults) {
    validatedPillars[pillarName] = validatePillar(
      world[pillarName],
      pillarDefaults[pillarName]
    )
  }

  return {
    ...world,
    nodes: validatedNodes,
    ...validatedPillars
  }
}
