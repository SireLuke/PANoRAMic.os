// nodeMap/nodeProfile.ts
export interface NodeProfile {
  id: string
  name: string
  type: 
    | "city"
    | "ecosystem"
    | "infrastructure"
    | "market"
    | "governance"
    | "humanitarian"
    | "commons"
    | "medical"
    | "cultural"
    | "quantum"

  latitude: number
  longitude: number

  populationCapacity: number
  resourceCapacity: number
}
