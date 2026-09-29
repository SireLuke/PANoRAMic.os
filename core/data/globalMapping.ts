// core/data/globalMapping.ts

/**
 * Global Signal Mapping Layer:
 * Converts incoming external data into global signal updates.
 */

export function mapIncomingToGlobal(
  incoming: any,
  mappingRules: Record<string, string>
): Record<string, number> {
  const updates: Record<string, number> = {}

  for (const incomingKey in mappingRules) {
    const globalKey = mappingRules[incomingKey]

    if (typeof incoming[incomingKey] === "number") {
      updates[globalKey] = incoming[incomingKey]
    }
  }

  return updates
}

/**
 * applyGlobalUpdates:
 * Applies updates to global signals.
 */
export function applyGlobalUpdates(
  world: any,
  updates: Record<string, number>
): any {
  return {
    ...world,
    globalSignals: {
      ...world.globalSignals,
      ...updates
    }
  }
}