# NAHT — Non-Abelian History Transport

NAHT is a modular history-transport and topology engine. It is designed to be usable independently of PANoRAMic.os and also embeddable through a separate PAN adapter.

## Design boundary

NAHT Core provides:
- a three-channel state contract `(q_r, q_e, q_p)`;
- ordered transport steps and retained history;
- pluggable transport backends;
- optional coupling with explicit norm accounting;
- graph/junction topology validation;
- provenance-bearing results.

NAHT Core does **not** require or import PAN V8, Gosset 4_21, Chronos, Janus Hydra, UHFE/UDFE, PAR, or RAMS. It does not claim to be QCD or a physical gauge theory. SU(2)/quaternion and optional SU(3) backends are mathematical transport choices whose conventions and validation must be declared.

## Standalone use

The package is dependency-free at runtime and exports TypeScript source:

```ts
import {
  transportHistory,
  QuaternionSU2Backend,
  type NAHTState,
  type TransportStep,
} from "./src/index.ts";

const initial: NAHTState = {
  frameId: "demo-frame",
  channels: [1, 0, 0],
};

const path: TransportStep[] = [{
  id: "quarter-turn",
  pathLength: 1,
  rotationAxis: [0, 0, 1],
  angleRadians: Math.PI / 2,
}];

const result = transportHistory(
  initial,
  path,
  new QuaternionSU2Backend(),
);

console.log(result.finalState.channels);
console.log(result.history);
```

## Plug-in points

- **State adapter:** converts an external state into the NAHT three-channel contract.
- **Transport backend:** applies ordered path transformations.
- **Topology:** validates and describes networks/junctions.
- **Coupling function:** optional state-dependent interaction; norm conservation is not assumed.
- **Host adapter:** exposes NAHT to an application. Host permissions are outside NAHT Core.

## Development checks

The repository includes a dependency-free conformance check at `tests/naht/nahtChecks.ts`. The root project currently has a mixed Node/Deno toolchain; run it with a compatible TypeScript runner after installing the repository's development dependencies. Do not interpret an unrun check as a passing test.

## Licensing

The project's selected direction is copyleft-first, with AGPL-3.0 as the leading candidate. Final license metadata and notices are intentionally deferred until dependency compatibility and the project-wide license decision are recorded. See `governance/NAHT_GOVERNANCE_AND_INTEGRATION.md`.
