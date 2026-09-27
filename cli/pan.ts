// cli/pan.ts

import { startPanServer } from "./start"
import { initialSystemState } from "../core/SystemInitialState"
import { computeSystem } from "../engine/system/systemEngine"
import { buildPlanetDashboard } from "../engine/dashboard/planetDashboard"

function printHelp() {
  console.log(`
PANoRAMic.os CLI Commands:

  pan start        - Start the full planetary server (REST + Live Stream)
  pan status       - Print the current planetary dashboard snapshot
  pan tick         - Advance the system by one tick
  pan audit        - Print the latest RAMS audit
  pan stream       - Show live updates in the terminal
  pan help         - Show this help menu
`)
}

async function main() {
  const command = process.argv[2]

  switch (command) {
    case "start":
      console.log("Starting PANoRAMic.os planetary server...")
      startPanServer()
      break

    case "status": {
      const dashboard = buildPlanetDashboard(initialSystemState)
      console.log("Planetary Status Snapshot:")
      console.log(JSON.stringify(dashboard, null, 2))
      break
    }

    case "tick": {
      const newState = computeSystem(initialSystemState)
      const dashboard = buildPlanetDashboard(newState)
      console.log("Tick complete. Updated dashboard:")
      console.log(JSON.stringify(dashboard, null, 2))
      break
    }

    case "audit": {
      const newState = computeSystem(initialSystemState)
      console.log("Latest RAMS Audit:")
      console.log(JSON.stringify(newState.audit, null, 2))
      break
    }

    case "stream": {
      console.log("Starting terminal live stream...")
      let state = initialSystemState
      setInterval(() => {
        state = computeSystem(state)
        const dashboard = buildPlanetDashboard(state)
        console.clear()
        console.log("PANoRAMic.os — Live Planet Feed")
        console.log(JSON.stringify(dashboard, null, 2))
      }, 1000)
      break
    }

    default:
      printHelp()
      break
  }
}

main()
