// nodeMap/nodeProfile.ts

export interface NodeProfile {
  id: string
  name: string
  region: string

  // Core state
  healthIndex: number        // 0–1
  stressIndex: number        // 0–1
  autonomyIndex: number      // 0–1
  connectivityIndex: number  // 0–1
  storageIndex: number       // 0–1
  aiPresenceIndex: number    // 0–1

  // Connections to other nodes
  connections: string[]

  // Classification
  type:
    | "ecology"
    | "infrastructure"
    | "population"
    | "rights"
    | "commons"
    | "governance"
    | "markets"
    | "labor"
    | "microAI"
    | "par"
    | "culture"
    | "workforce"
}
