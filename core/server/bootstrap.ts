// core/server/bootstrap.ts

import { startWorldApiServer } from "./worldApi"
import { Actuator } from "../actuation/actuator"
import { wireActuation } from "../actuation/wireActuation"
import { pollNasaPower } from "../feeds/nasaPower"

const pillarDefaults: any = { /* your existing defaults */ }
let world: any = { /* your initial world */ }

export function startPanOs() {
  console.log("PAN-OS: Booting planetary operating system...")

  startWorldApiServer()
  console.log("PAN-OS: World API started.")

  const actuator = new Actuator()
  wireActuation(actuator)
  console.log("PAN-OS: Actuation layer online.")

  // Real NASA POWER feed loop
  setInterval(async () => {
    try {
      world = await pollNasaPower(world, pillarDefaults)
    } catch (err) {
      console.error("NASA POWER feed error:", err)
    }
  }, 10_000) // every 10 seconds, tune as needed

  console.log("PAN-OS: NASA POWER feed loop active.")
}

if (require.main === module) {
  startPanOs()
}