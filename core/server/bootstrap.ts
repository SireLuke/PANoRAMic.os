// core/server/bootstrap.ts

import { startWorldApiServer } from "./worldApi"
import { Actuator } from "../actuation/actuator"
import { wireActuation } from "../actuation/wireActuation"

// Current real feeds
import { pollNasaPower } from "../feeds/nasaPower"
import { pollNoaa } from "../feeds/noaa"
import { pollUsgs } from "../feeds/usgs"

// Future feeds (add implementations as you go)
import { pollWho } from "../feeds/who"           // WHO outbreaks
import { pollImf } from "../feeds/imf"           // IMF economic stress
import { pollWorldBank } from "../feeds/worldBank" // World Bank indicators
import { pollEpa } from "../feeds/epa"           // EPA pollution
import { pollDoe } from "../feeds/doe"           // DOE energy / flux
import { pollFtc } from "../feeds/ftc"           // FTC regulatory pressure
import { pollTokamak } from "../feeds/tokamak"   // your reactor board

const pillarDefaults: any = { /* your pillar defaults */ }
let world: any = { /* your initial world */ }

export function startPanOs() {
  console.log("PAN-OS: Booting planetary operating system...")

  // World API
  startWorldApiServer()
  console.log("PAN-OS: World API started.")

  // Actuation Layer
  const actuator = new Actuator()
  wireActuation(actuator)
  console.log("PAN-OS: Actuation layer online.")

  // === REAL FEEDS (already implemented) ===

  // NASA POWER
  setInterval(async () => {
    try {
      world = await pollNasaPower(world, pillarDefaults)
    } catch (err) {
      console.error("NASA POWER feed error:", err)
    }
  }, 10_000)

  // NOAA
  setInterval(async () => {
    try {
      world = await pollNoaa(world, pillarDefaults)
    } catch (err) {
      console.error("NOAA feed error:", err)
    }
  }, 10_000)

  // USGS
  setInterval(async () => {
    try {
      world = await pollUsgs(world, pillarDefaults)
    } catch (err) {
      console.error("USGS feed error:", err)
    }
  }, 10_000)

  // === FUTURE FEEDS (wire now, implement later) ===

  // WHO outbreaks
  setInterval(async () => {
    try {
      world = await pollWho(world, pillarDefaults)
    } catch (err) {
      console.error("WHO feed error:", err)
    }
  }, 15_000)

  // IMF economic stress
  setInterval(async () => {
    try {
      world = await pollImf(world, pillarDefaults)
    } catch (err) {
      console.error("IMF feed error:", err)
    }
  }, 20_000)

  // World Bank indicators
  setInterval(async () => {
    try {
      world = await pollWorldBank(world, pillarDefaults)
    } catch (err) {
      console.error("World Bank feed error:", err)
    }
  }, 20_000)

  // EPA pollution
  setInterval(async () => {
    try {
      world = await pollEpa(world, pillarDefaults)
    } catch (err) {
      console.error("EPA feed error:", err)
    }
  }, 25_000)

  // DOE energy / flux
  setInterval(async () => {
    try {
      world = await pollDoe(world, pillarDefaults)
    } catch (err) {
      console.error("DOE feed error:", err)
    }
  }, 25_000)

  // FTC regulatory pressure
  setInterval(async () => {
    try {
      world = await pollFtc(world, pillarDefaults)
    } catch (err) {
      console.error("FTC feed error:", err)
    }
  }, 30_000)

  // Tokamak flux board (your hardware)
  setInterval(async () => {
    try {
      world = await pollTokamak(world, pillarDefaults)
    } catch (err) {
      console.error("Tokamak feed error:", err)
    }
  }, 30_000)

  console.log("PAN-OS: All feed loops wired (current + future).")
}

if (require.main === module) {
  startPanOs()
}