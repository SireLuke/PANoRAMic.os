import { createWorldState } from "../../core/worldstate/WorldState"
import { tick } from "../../core/tick/tickLoop"
import { holdPillar } from "../../pillars/holdPillar"
import { Quantum_STATE } from "../../pillars/quantum/STATE"
import { Economy_STATE } from "../../pillars/economy/STATE"

function assert(ok: boolean, message: string): void {
  if (!ok) throw new Error("tick wiring check failed: " + message)
}
const PILLARS = ["population","resources","economy","governance","humanitarian","medical","antigenocide","markets",
  "crime","education","migration","trafficking","transparency","corporatecapture","epistemic","repairability","quantum"] as const

// 1. The tick loop runs end to end for many ticks and keeps every pillar populated.
let world = createWorldState()
for (let i = 0; i < 25; i++) world = tick(world)
for (const p of PILLARS) assert(world[p] && typeof world[p] === "object" && Object.keys(world[p]).length > 0, `pillar ${p} populated`)

// 2. Hold engines return the declared defaults (no dynamics are invented).
assert(JSON.stringify(world.quantum) === JSON.stringify(Quantum_STATE), "quantum equals declared default")
assert(JSON.stringify(world.economy) === JSON.stringify(Economy_STATE), "economy equals declared default")

// 3. Deterministic: two independent runs agree exactly.
const run = () => { let w = createWorldState(); for (let i = 0; i < 10; i++) w = tick(w); return JSON.stringify(w.globalSignals) + JSON.stringify(w.quantum) }
assert(run() === run(), "deterministic")

// 4. Purity: input state is not mutated, and existing pillar values are preserved over defaults.
const before = createWorldState(); before.quantum = { coherence: 0.7 }
const snapshot = JSON.stringify(before)
const after = tick(before)
assert(JSON.stringify(before) === snapshot, "tick does not mutate its input")
assert(after.quantum.coherence === 0.7 && after.quantum.entanglement === 0, "current value wins, defaults fill gaps")

// 5. Bad data is rejected, not propagated.
let rejected = false
try { holdPillar(Quantum_STATE, { coherence: NaN }, "Quantum") } catch { rejected = true }
assert(rejected, "non-finite value rejected")

// 6. Tick counter / global signals shape survive.
assert(typeof world.globalSignals.stability === "number", "global signals present")
console.log("Tick wiring checks passed.")
