// cli/start.ts

import { runContinuous } from "../engine/run/runIntegration.js"
import { bootstrapAPI } from "../api/integration/apiBootstrap.js"

async function main() {
  console.log("PANoRAMic.OS: Starting planetary operating system...")

  // Start API + WebSocket
  await bootstrapAPI()

  // Start continuous planetary tick loop
  runContinuous()

  console.log("PANoRAMic.OS: Planetary engine running...")
}

main().catch(err => {
  console.error("PAN startup error:", err)
})
