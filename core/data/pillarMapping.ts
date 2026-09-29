// core/data/pillarMapping.ts

/**
 * Pillar Mapping Layer:
 * Determines how incoming datasets update pillar values.
 */

export function applyPillarUpdates(
  world: any,
  pillarName: string,
  updates: Record<string, number>
): any {
  const updatedPillar = {
    ...world[pillarName],
    ...updates
  }

  return {
    ...world,
    [pillarName]: updatedPillar
  }
}

/**
 * mapIncomingToPillar:
 * Converts incoming external data into pillar updates.
 * This is where semantic meaning is applied.
 */
export function mapIncomingToPillar(
  incoming: any,
  pillarName: string,
  mappingRules: Record<string, string>
): Record<string, number> {
  const updates: Record<string, number> = {}

  for (const incomingKey in mappingRules) {
    const pillarKey = mappingRules[incomingKey]

    if (typeof incoming[incomingKey] === "number") {
      updates[pillarKey] = incoming[incomingKey]
    }
  }

  return updates
}