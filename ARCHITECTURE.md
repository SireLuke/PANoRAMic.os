# PANoRAMic.OS Architecture

## System Overview

PANoRAMic.OS is an always-on planetary coordination engine. The repository currently mixes a Deno-style boot path (`src/boot.ts`) with Node/Express API code, CLI commands, engine loops, and several dashboard surfaces. Not every layer is wired together by `npm start`.

### Platform Tiers

```
┌─────────────────────────────────────────────────────────┐
│  Frontend Layer                                         │
│  - Vite/React app stub: /app                            │
│  - Static dashboard: /dashboard                         │
│  - Additional HTML dashboards: /core/dashboard          │
│  - React planetary views: /src/dashboard                │
└──────────────────┬──────────────────────────────────────┘
                   │ HTTP (port 3000 when a server is started)
                   ▼
┌─────────────────────────────────────────────────────────┐
│  API Layer                                              │
│  - Express/Socket.IO live stream: /api/server.ts        │
│  - Bootstrap helper: /api/integration/apiBootstrap.ts   │
│  Note: `npm start` does not launch this layer.          │
└──────────────────┬──────────────────────────────────────┘
                   │
        ┌──────────┼──────────┐
        ▼          ▼          ▼
┌────────────┐ ┌─────────┐ ┌─────────────┐
│CLI Layer   │ │Engine   │ │Dashboard    │
│/cli        │ │/engine  │ │boot serves  │
│commands    │ │tick/    │ │/dashboard   │
│exist; not  │ │loops    │ │via Deno in  │
│started by  │ │         │ │src/dashboard.ts
│npm start   │ │         │ │             │
└────────────┘ └─────────┘ └─────────────┘
                   ▼
┌─────────────────────────────────────────────────────────┐
│  Core Runtime                                           │
│  - Canonical boot: src/boot.ts                          │
│  - Models: /core (worldstate, pillars, audits, data)    │
│  - RAMS: /rams                                          │
│  - Signals: /signals                                    │
└─────────────────────────────────────────────────────────┘
```

## Entry Points

### Canonical runtime: `src/boot.ts`

`src/boot.ts` is the boot sequence used by the compatibility shims. It:

1. Initializes the kernel and feed layer  
2. Runs a RAMS pre-audit  
3. Computes RSDV  
4. Initializes PAR, demurrage, and stagnation  
5. Boots the node network  
6. Serves `./dashboard` on port 3000 (Deno `serve` in `src/dashboard.ts`)

### `npm start`

Root `package.json` currently has a single script:

```bash
npm start
```

That runs `ts-node cli/start.ts`, which re-exports `bootSystem` from `src/boot.ts`. Boot files use Deno-style `import.meta.main` and `.ts` imports, so Node/`ts-node` and Deno are not interchangeable without extra flags.

Direct Deno invocation (as documented in `STARTUP.md`):

```bash
deno run --allow-all src/boot.ts
```

### Compatibility shims (deprecated)

These delegate to `src/boot.ts` and should not be treated as separate runtimes:

- `boot.ts`
- `start.ts`
- `run.ts`
- `main.ts`
- `src/main.ts`
- `cli/start.ts`
- `cli/run.ts`

### Scripts that are not defined at the repo root

The root `package.json` does **not** define `api`, `cli`, `engine`, `build`, `app:dev`, or `app:build`.

To run the React app workspace:

```bash
cd app
npm install
npm run dev      # Vite, typically http://localhost:5173
npm run build
```

To run the Express live-stream server (separate from `src/boot.ts`):

```bash
# api/server.ts listens on http://localhost:3000
```

Do not run the Deno dashboard server and `api/server.ts` at the same time; both bind port 3000.

## Directory Structure

```
PANoRAMic.os/
├── src/boot.ts                   # Canonical boot sequence
├── start.ts / boot.ts / run.ts / main.ts / cli/start.ts  # Shims
├── package.json                  # Root scripts (currently `start` only)
├── tsconfig.json                 # CommonJS, no path aliases
│
├── api/                          # HTTP/WebSocket layer
│   ├── integration/
│   │   ├── apiBootstrap.ts
│   │   ├── apiIntegration.ts
│   │   ├── liveStreamIntegration.ts
│   │   └── pillarRoutesIntegration.ts
│   ├── routes/planetRouter.ts
│   ├── server.ts
│   └── liveStream.ts
│
├── engine/                       # Planetary runtime
│   ├── system/
│   │   ├── systemLoopIntegration.ts
│   │   ├── systemTickIntegration.ts
│   │   └── systemEngine.ts
│   ├── dashboard/
│   ├── nodes/, par/, ecology/, infrastructure/, markets/, ...
│
├── cli/                          # Command modules
│   ├── integration/cliIntegration.ts
│   ├── src/commands/
│   └── domain command folders (par, nodes, ecology, ...)
│
├── core/                         # Models, audits, worldstate, pillars
├── rams/                         # Resource Audit & Management System
├── signals/                      # Signal computation
├── dashboard/                    # Static/HTML dashboard + panels
├── app/                          # Vite + React frontend workspace
├── ARCHITECTURE.md
├── STARTUP.md
└── README.md
```

## Module Resolution

Root `tsconfig.json` uses **CommonJS** (`"module": "CommonJS"`) and does **not** define `@engine/*` (or similar) path aliases.

The React app (`app/tsconfig.json`) defines:

- `@engine/*` → `../engine/*`
- `@dashboard/*` → `../src/dashboard/*`

Boot and several engine files still use Deno-style `.ts` specifiers and `import.meta.main`. Treat module style as mixed, not a uniform ESM+alias setup.

## Deployment (current repo)

### Boot the canonical sequence

```bash
npm install
npm start
# or: deno run --allow-all src/boot.ts
```

### Frontend workspace

```bash
cd app
npm install
npm run dev
```

Root Docker/`npm run build` examples are not backed by root scripts yet.

## Language Composition

| Language   | Purpose                              | Path          |
|-----------|--------------------------------------|---------------|
| TypeScript | Core runtime, engine, API, CLI       | Root + /api, /engine, /cli, /core, /signals, /src |
| TypeScript | Frontend UI components               | /app/src, /src/dashboard, /dashboard/panels |
| HTML/CSS/JS | Browser dashboards                 | /dashboard, /core/dashboard |
| JSON       | Configuration, data                  | *.json        |

## Inter-Platform Communication

### Backend live stream

`api/server.ts` ticks the world and emits `planet_update` over Socket.IO on port 3000.

`api/integration/apiBootstrap.ts` is written to listen on port 3000 and start the live-stream helper. It is not invoked by `npm start`.

### CLI ↔ Engine

CLI command modules live under `/cli`. `cli/integration/cliIntegration.ts` exists for dispatch, but there is no root `npm run cli` script.

## Debugging & Development

```bash
npm start
```

API inspection only applies if `api/server.ts` (or `bootstrapAPI()`) is running:

```bash
curl http://localhost:3000/
```

Frontend hot reload (app workspace):

```bash
cd app && npm run dev
```

## PAR naming and caps

- **PAR** = Panitarian Asset Receipt (see `docs/whitspaper.md` and `src/boot.ts`)
- Boot cap in `src/par.ts`: `population * 1.35 * rsdv`
- RAMS dynamic cap in `core/economy/src/dynamicFloat.ts`: `min(population * 1.35, resourceParValue * 0.90)`

---

**Last Updated:** 2026-10-03  
**Canonical boot:** `src/boot.ts`  
**npm start:** `ts-node cli/start.ts` → `src/boot.ts`  
**Platform mix:** Node.js (Express, ts-node) + Deno-style boot files + React 18 / TypeScript 5


## Governance and NAHT modules (proposed foundation)

The repository's existing quantitative Governance pillar remains in place. The new `/governance` layer defines the constitutional/procedural architecture, policy lifecycle, decision records, oversight, and domain interfaces. See:

- `governance/PAN_GOVERNANCE_CHARTER.md`
- `governance/PAN_GOVERNANCE_ARCHITECTURE.md`
- `governance/NAHT_GOVERNANCE_AND_INTEGRATION.md`

NAHT has one core and two deployment modes:

- `modules/naht`: standalone, dependency-light transport/topology package with no PAN imports.
- `integrations/pan/naht`: PAN-native adapter that provides explicit, versioned projections from V8 `(h,R,u,d,tau,chi,s,f)` or V9 `(h,R,u,d,tau,chi,s,f,xi)` into NAHT `(q_r,q_e,q_p)`. V9 requires declared `xi` semantics and units. An optional SU(9) route requires explicit V9-to-C^9 encoding and a separate C^9-to-NAHT projection. No mapping is declared canonical; callers must supply and version each one.

The canonical boot sequence reports the native adapter registration as read-only. It does not activate a V8 projection, mutate canonical records, or execute host actions. Standalone NAHT remains independently usable.

The initial module includes ordered history transport, a unit-quaternion/SU(2) backend, graph topology validation, provenance records, and explicit norm-change accounting for optional coupling. SU(3), Chronos, Gosset, Janus Hydra, and additional host adapters remain pluggable extensions rather than core dependencies.

## STRATA — Scale-Transition Research and Analysis

STRATA is the platform's independent research and validation layer. It evaluates whether proposed patterns survive declared changes in scale, domain, representation, and observer/implementation, using preregistered baselines and randomized or structure-preserving controls.

STRATA is intentionally outside the canonical runtime boot path. It is non-authoritative: it reports evidence and failure states but cannot promote claims into PAN canon or mutate canonical records.

Architectural boundaries:

- V8 remains the canonical eight-coordinate state vector `(h, R, u, d, τ, χ, s, f)`.
- Janus Hydra may translate features/geometries but does not validate its own outputs.
- UHFE/UDFE remain distinct paired formation/dissolution representations.
- Gosset `4_21` / E8 remains the primary geometry target where applicable; other geometries are comparison controls.
- Empirical claims require provenance, held-out evaluation, independent domains, uncertainty, and published negative/null results.

Specification: [docs/STRATA_LAYER.md](docs/STRATA_LAYER.md).

The first experimental implementation is maintained separately on `research/strata-002`; no experiment code is wired into production boot or merged into the canonical branch.
