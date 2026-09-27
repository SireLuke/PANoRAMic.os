// run.ts

import { initCLIIntegration, cliDispatch } from "./cli/integration/cliIntegration.js"
import { bootstrapAPI } from "./api/integration/apiBootstrap.js"
import { initRunIntegration, runContinuous } from "./engine/system/runIntegration.js"

async function main() {
  console.log("PANoRAMic.OS: Booting planetary operating system...")

  // 1. Initialize CLI integration
  const cli = initCLIIntegration()

  // 2. Initialize API + WebSocket
  await bootstrapAPI()

  // 3. Initialize run integration (planetary engine)
  const run = initRunIntegration()

  // 4. Start continuous planetary run
  console.log("PANoRAMic.OS: Starting continuous planetary engine...")
  runContinuous(run, 1000)

  // 5. Listen for CLI commands
  process.stdin.on("data", (data) => {
    const command = data.toString().trim()
    cliDispatch(command, cli)
  })
}

main()
