// cli/governance/governanceCommands.ts

export function governanceCommands(globalState: any) {
  const governance = globalState?.governance

  if (!governance) {
    console.log("Governance subsystem not found in global state.")
    return
  }

  console.log("=== Governance Subsystem ===")
  console.log("Stability:", governance.stability)
  console.log("Integrity:", governance.integrity)
  console.log("Signals:", governance.signals)
  console.log("Policies:", governance.policies)
  console.log("Risk:", governance.risk)
  console.log("Mode:", governance.mode)
}
