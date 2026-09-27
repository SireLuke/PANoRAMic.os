// cli/run.ts

import { initialSystemState } from "../core/SystemInitialState.js"
import { runSystemLoop } from "../engine/system/systemLoop.js"

function main() {
  const cycles = process.argv[2]
    ? parseInt(process.argv[2], 10)
    : 1000 // default to 1,000 cycles

  console.log(`Running PANoRAMic.os for ${cycles} cycles...`)

  const result = runSystemLoop(initialSystemState, cycles)

  console.log("Simulation complete.")
  console.log("Final State Summary:")
  console.log(JSON.stringify(result.finalState, null, 2))
}

main()
