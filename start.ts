// start.ts

import { bootstrapAPI } from "./api/integration/apiBootstrap.js"
import { initRunIntegration, runContinuous } from "./engine/system/runIntegration.js"
import { initCLIIntegration, cliDispatch } from "./cli/integration/cliIntegration.js"


async function startPAN() {
  console.log("PANoRAMic.OS: Starting planetary operating system...")

  // 1. Initialize CLI
  const cli = initCLIIntegration()

  // 2. Initialize API + WebSocket
  await bootstrapAPI()

  // 3. Initialize planetary engine
  const run = initRunIntegration()

  // 4. Begin continuous planetary tick loop
  console.log("PANoRAMic.OS: Planetary engine running...")
  runContinuous(run, 1000)

  // 5. Enable interactive CLI commands
  process.stdin.on("data", (data) => {
    const command = data.toString().trim()
    cliDispatch(command, cli)
  })
}

startPAN()
