// core/data/nodeMapping.ts

/**
 * Node Mapping Layer:
 * Determines which nodes should receive updates from incoming datasets.
 * This is the geospatial + semantic mapping logic.
 */

export type Node = {
  id: string
  name: string
  latitude: number
  longitude: number
  country?: string
  region?: string
  city?: string
  [key: string]: any
}

/**
 * matchByLocation:
 * Matches incoming data to nodes based on country/region/city.
 */
export function matchByLocation(nodes: Record<string, Node>, incoming: any): string[] {
  const matches: string[] = []

  for (const id in nodes) {
    const node = nodes[id]

    if (incoming.country && node.country === incoming.country) matches.push(id)
    if (incoming.region && node.region === incoming.region) matches.push(id)
    if (incoming.city && node.city === incoming.city) matches.push(id)
  }

  return matches
}

/**
 * matchByRadius:
 * Matches nodes within a geographic radius.
 */
export function matchByRadius(
  nodes: Record<string, Node>,
  lat: number,
  long: number,
  radiusKm: number
): string[] {
  const matches: string[] = []

  const R = 6371 // Earth radius in km

  for (const id in nodes) {
    const node = nodes[id]

    const dLat = (node.latitude - lat) * (Math.PI / 180)
    const dLon = (node.longitude - long) * (Math.PI / 180)

    const a =
      Math.sin(dLat / 2) ** 2 +
      Math.cos(lat * Math.PI / 180) *
      Math.cos(node.latitude * Math.PI / 180) *
      Math.sin(dLon / 2) ** 2

    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))
    const distance = R * c

    if (distance <= radiusKm) matches.push(id)
  }

  return matches
}

/**
 * applyNodeUpdates:
 * Applies incoming updates to matched nodes.
 */
export function applyNodeUpdates(
  world: any,
  nodeIds: string[],
  updates: any
): any {
  const updatedNodes = { ...world.nodes }

  nodeIds.forEach(id => {
    updatedNodes[id] = {
      ...updatedNodes[id],
      ...updates
    }
  })

  return {
    ...world,
    nodes: updatedNodes
  }
}