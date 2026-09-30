// core/server/bootstrap.ts

/**
 * PAN-OS Bootstrap:
 * Wires up funnels, world model, and starts the World API server.
 */

import { startWorldApiServer } from "./worldApi"
import { registerFunnel } from "../data/funnelManager"
import "./../data/funnels/libraryOfAlexandria"

// Initial world state
const world: any = {
  nodes: [],
  pillars: {},
  globalSignals: {
    stability: 0.5,
    risk: 0.5,
    collapsePressure: 0.5,
    recoveryStrength: 0.5,
    synthesis: 0.5
  }
}

// Pillar defaults (can be expanded later)
const pillarDefaults: any = {
  population: {},
  resources: {},
  economy: {},
  governance: {},
  medical: {},
  humanitarian: {},
  markets: {},
  crime: {},
  education: {},
  migration: {},
  trafficking: {},
  transparency: {},
  corporatecapture: {},
  epistemic: {},
  repairability: {},
  quantum: {}
}

// Register core funnels (Library of Alexandria already self-registers)
function initializeFunnels() {
  console.log("PAN-OS: Funnels initialized.")
}

// Start world API
function initializeApi() {
  startWorldApiServer()
  console.log("PAN-OS: World API started.")
}

// Main bootstrap
export function startPanOs() {
  console.log("PAN-OS: Booting planetary operating system...")
  initializeFunnels()
  initializeApi()
  console.log("PAN-OS: System online.")
}

// Auto-start if run directly
if (require.main === module) {
  startPanOs()
}