// cli/install.ts

import { execSync } from "child_process"
import path from "path"
import fs from "fs"

function main() {
  console.log("Installing PANoRAMic.os CLI globally...")

  const cliPath = path.resolve(__dirname, "pan.ts")
  const binDir = path.resolve(__dirname, "../../bin")

  // Ensure /bin exists
  if (!fs.existsSync(binDir)) {
    fs.mkdirSync(binDir)
  }

  const binFile = path.join(binDir, "pan")

  // Create a small launcher script
  const launcher = `#!/usr/bin/env node
require("${cliPath.replace(/\\/g, "/")}")
`

  fs.writeFileSync(binFile, launcher)
  fs.chmodSync(binFile, 0o755)

  // Link globally using npm
  try {
    execSync(`npm link`, { stdio: "inherit" })
    console.log("PANoRAMic.os CLI installed globally.")
    console.log("Run commands like: pan start, pan status, pan stream")
  } catch (err) {
    console.error("Failed to link globally:", err)
  }
}

main()
