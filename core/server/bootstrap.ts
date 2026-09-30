// core/server/bootstrap.ts

import { startWorldApiServer } from "./worldApi"
import { Actuator } from "../actuation/actuator"
import { wireActuation } from "../actuation/wireActuation"

import { pollNasaPower } from "../feeds/nasaPower"
import { pollNoaa } from "../feeds/noaa"
import { pollUsgs } from "../feeds/usgs"

const pillarDefaults: any = { /* your pillar defaults */ }
let world: any = { /* your initial world */ }

export function startPanOs() {
  console.log("PAN-OS: Booting planetary operating system...")

  startWorldApiServer()
  console.log("PAN-OS: World API started.")

  const actuator = new Actuator()
  wireActuation(actuator)
  console.log("PAN-OS: Actuation layer online.")

  // NASA POWER feed loop
  setInterval(async () => {
    try {
      world = await pollNasaPower(world, pillarDefaults)
    } catch (err) {
      console.error("NASA POWER feed error:", err)
    }
  }, 10_000)

  // NOAA feed loop
  setInterval(async () => {
    try {
      world = await pollNoaa(world, pillarDefaults)
    } catch (err) {
      console.error("NOAA feed error:", err)
    }
  }, 10_000)

  // USGS earthquake feed loop
  setInterval(async () => {
    try {
      world = await pollUsgs(world, pillarDefaults)
    } catch (err) {
      console.error("USGS feed error:", err)
    }
  }, 10_000)

  console.log("PAN-OS: USGS feed loop active.")
}

if (require.main === module) {
  startPanOs()
}