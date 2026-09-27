// cli/integration/cliIntegration.ts

import { initRunIntegration, runOneTick, runContinuous, stopRun } from "../../engine/system/runIntegration"
import { dashboardEngine } from "../../engine/dashboard/dashboardEngine"
import { globalSignals } from "../../signals/globalSignals"
import { nodesCommands } from "../nodes/nodesCommands"
import { parCommands } from "../par/parCommands"
import { rightsCommands } from "../rights/rightsCommands"
import { ecologyCommands } from "../ecology/ecologyCommands"
import { infraCommands } from "../infrastructure/infraCommands"
import { commonsCommands } from "../commons/commonsCommands"
import { governanceCommands } from "../governance/governanceCommands"
import { laborCommands } from "../labor/laborCommands"
import { marketsCommands } from "../markets/marketsCommands"
import { modesCommands } from "../modes/modesCommands"
import { workforceCommands } from "../workforce/workforceCommands"

export interface CLIIntegration {
  run: ReturnType<typeof initRunIntegration>
}

/**
 * Initialize CLI integration layer
 */
export function initCLIIntegration(): CLIIntegration {
  return {
    run: initRunIntegration(),
  }
}

/**
 * Execute a single tick from CLI
 */
export function cliTick(integration: CLIIntegration) {
  runOneTick(integration.run)

  console.log(`Tick ${integration.run.tick} complete.`)
  console.log("Global Signals:", globalSignals)
}

/**
 * Run PAN continuously from CLI
 */
export async function cliRun(integration: CLIIntegration, intervalMs = 1000) {
  console.log("Starting continuous planetary run...")
  await runContinuous(integration.run, intervalMs)
}

/**
 * Stop continuous run
 */
export function cliStop(integration: CLIIntegration) {
  stopRun(integration.run)
  console.log("Planetary run stopped.")
}

/**
 * Dispatch CLI commands
 */
export function cliDispatch(command: string, integration: CLIIntegration) {
  switch (command) {
    case "tick":
      return cliTick(integration)

    case "run":
      return cliRun(integration)

    case "stop":
      return cliStop(integration)

    case "nodes":
      return nodesCommands(integration.run.systemTick.system.global)

    case "par":
      return parCommands(integration.run.systemTick.system.global)

    case "rights":
      return rightsCommands(integration.run.systemTick.system.global)

    case "ecology":
      return ecologyCommands(integration.run.systemTick.system.global)

    case "infra":
      return infraCommands(integration.run.systemTick.system.global)

    case "commons":
      return commonsCommands(integration.run.systemTick.system.global)

    case "governance":
      return governanceCommands(integration.run.systemTick.system.global)

    case "labor":
      return laborCommands(integration.run.systemTick.system.global)

    case "markets":
      return marketsCommands(integration.run.systemTick.system.global)

    case "modes":
      return modesCommands(integration.run.systemTick.system.global)

    case "workforce":
      return workforceCommands(integration.run.systemTick.system.global)

    default:
      console.log(`Unknown command: ${command}`)
  }
}
