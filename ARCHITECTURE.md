# PANoRAMic.OS Multi-Platform Architecture

## System Overview

PANoRAMic.OS is a **multi-platform, always-on planetary coordination engine** designed to run continuously across different environments and interfaces.

### Platform Tiers

```
┌─────────────────────────────────────────────────────────┐
│  Frontend Layer (React Web)                             │
│  - Real-time planetary dashboard                        │
│  - Interactive pillar management                        │
│  - Live signal stream visualization                     │
│  Location: /app (separate npm workspace)                │
└──────────────────┬──────────────────────────────────────┘
                   │ HTTP + WebSocket (port 3000)
                   ▼
┌─────────────────────────────────────────────────────────┐
│  API Layer (Express + WebSocket)                        │
│  - REST endpoints (/state, /nodes, /signals, etc.)      │
│  - Live stream broadcasting                             │
│  - Pillar routes integration                            │
│  Location: /api/integration/apiBootstrap.ts             │
└──────────────────┬──────────────────────────────────────┘
                   │
        ┌──────────┼──────────┐
        ▼          ▼          ▼
┌────────────┐ ┌─────────┐ ┌─────────────┐
│CLI Layer   │ │Engine   │ │Dashboard    │
│            │ │Loop     │ │Broadcasting │
│Interactive │ │         │ │             │
│Commands    │ │Planetary│ │Real-time    │
│            │ │Tick     │ │State Stream │
│Location:   │ │         │ │             │
│/cli        │ │Location:│ │Location:    │
│            │ │/engine  │ │/core        │
└────────────┘ └─────────┘ └─────────────┘
        │          │
        └──────────┼──────────┘
                   ▼
┌─────────────────────────────────────────────────────────┐
│  Core Runtime Layer (Node.js)                           │
│                                                         │
│  ┌──────────────────────────────────────────────────┐   │
│  │  System Loop Integration                         │   │
│  │  - Nodes, Pillars, Modes, Audits                 │   │
│  │  - Tick-by-tick state transitions                │   │
│  │  Location: /engine/system/systemLoopIntegration.ts│  │
│  └──────────────────────────────────────────────────┘   │
│                                                         │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Planetary Systems                               │   │
│  │  ├─ RAMS: Resource Audit & Management            │   │
│  │  ├─ PAR: Planetary Autonomous Resource Economy   │   │
│  │  ├─ Ecology: Biome & Regeneration                │   │
│  │  ├─ Infrastructure: Networks & Grid              │   │
│  │  ├─ Labor: Workforce & Rotation                  │   │
│  │  ├─ Markets: Economic Circulation                │   │
│  │  ├─ Rights: Human Dignity & Justice              │   │
│  │  ├─ Commons: Shared Resources                    │   │
│  │  ├─ Culture: Collective Knowledge                │   │
│  │  └─ Governance: Decision Structures              │   │
│  │  Location: /core/pillars, /engine                │   │
│  └──────────────────────────────────────────────────┘   │
│                                                         │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Data Layer                                      │   │
│  │  ├─ World State (global conditions)              │   │
│  │  ├─ Event Log (all transactions)                 │   │
│  │  ├─ Signals (system health indicators)           │   │
│  │  ├─ Provenance (audit trail)                     │   │
│  │  └─ Feeds (external data sources)                │   │
│  │  Location: /core/data, /signals                  │   │
│  └──────────────────────────────────────────────────┘   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Entry Points

### Canonical Entry Point: `start.ts` (Root)

The **primary entry point** that activates the entire multi-platform system:

```bash
npm start
```

This initializes:
1. **CLI Layer** — Interactive commands
2. **API Server** — REST + WebSocket on port 3000
3. **Engine Runtime** — Continuous planetary loop
4. **Dashboard Broadcasting** — Live state stream

**Output:**
```
🌍 PANoRAMic.OS: Initializing Planetary Operating System...
📋 Architecture: Multi-Platform (Backend + API + CLI + Frontend)
🔌 [1/4] Initializing CLI integration...
🔌 [2/4] Initializing API server (port 3000)...
🔌 [3/4] Initializing planetary engine...
🔌 [4/4] Starting continuous planetary simulation...
✅ PANoRAMic.OS: Fully operational
📡 API: http://localhost:3000
⌨️  CLI: Ready for commands
🎨 Web Dashboard: http://localhost:3000/dashboard
```

### Platform-Specific Entry Points

#### API Only
```bash
npm run api
```
Starts the Express server without CLI or engine loop. Useful for server-only deployments.

#### Engine Only (CLI-Only Mode)
```bash
npm run cli
```
**Deprecated.** CLI-only mode with no API or dashboard. Use for debugging/testing in isolation.

#### Frontend Development
```bash
npm run app:dev
```
Starts Vite dev server on port 5173 with hot reload. Connects to API on localhost:3000.

```bash
npm run app:build
```
Production build of React frontend.

## Directory Structure

```
PANoRAMic.os/
├── start.ts                      # 🚀 Canonical entry point (multi-platform boot)
├── run.ts                        # ⚠️  Deprecated (backward compat)
├── package.json                  # Root workspace config
├── tsconfig.json                 # Shared TypeScript config
│
├── api/                          # 📡 API Layer
│   ├── integration/
│   │   ├── apiBootstrap.ts      # API server initialization
│   │   ├── apiIntegration.ts    # Route binding
│   │   └── liveStreamIntegration.ts
│   ├── routes/
│   │   └── planetRouter.ts
│   ├── server.ts
│   └── liveStream.ts
│
├── engine/                       # ⚙️  Planetary Runtime
│   ├── system/
│   │   ├── systemLoopIntegration.ts   # Main loop
│   │   ├── systemTickIntegration.ts
│   │   └── systemEngine.ts
│   ├── run/
│   │   └── runIntegration.js    # Deprecated
│   ├── nodes/                   # Node engines
│   ├── par/                     # PAR economy engines
│   ├── ecology/                 # Ecology engines
│   ├── infrastructure/          # Infrastructure engines
│   ├── markets/                 # Market engines
│   └── ... (other engines)
│
├── cli/                         # ⌨️  CLI Layer
│   ├── integration/
│   │   └── cliIntegration.ts   # Command dispatch
│   ├── start.ts                 # ⚠️  Deprecated
│   ├── nodes/
│   ├── par/
│   ├── ecology/
│   └── ... (domain-specific commands)
│
├── core/                        # 🧠 Planetary Systems
│   ├── worldstate/              # Global state objects
│   ├── pillars/                 # Pillar definitions
│   ├── audits/                  # RAMS audit engines
│   ├── data/                    # Data adapters & normalization
│   └── ...
│
├── signals/                     # 📊 Signal Computation
│   ├── globalSignals.ts
│   └── (pillar-specific signals)
│
├── dashboard/                   # 🎨 Dashboard/Visualization
│   ├── src/                     # TypeScript components
│   ├── panels/                  # Pillar panels
│   └── core/dashboard/          # Browser-based HTML/JS
│
├── app/                         # 🖥️  React Frontend
│   ├── package.json
│   ├── src/
│   │   ├── App.tsx
│   │   └── components/
│   └── tsconfig.json
│
├── ARCHITECTURE.md              # This file
└── README.md                    # Overview
```

## Module Resolution

All modules use **ESM (ES Module)** syntax with proper path aliases:

```typescript
// ✅ Correct (using path aliases)
import { systemLoop } from "@engine/system/systemLoopIntegration"
import { globalSignals } from "@signals/globalSignals"
import { cliDispatch } from "@cli/integration/cliIntegration"

// ✅ Correct (relative with .js extension for ESM)
import { bootstrapAPI } from "./api/integration/apiBootstrap.js"

// ❌ Avoid (mixed patterns)
import { runContinuous } from "../engine/run/runIntegration.js"  // Wrong path
```

**Path Aliases (tsconfig.json):**
- `@api/*` → `api/*`
- `@engine/*` → `engine/*`
- `@cli/*` → `cli/*`
- `@core/*` → `core/*`
- `@rams/*` → `rams/*`
- `@signals/*` → `signals/*`
- `@dashboard/*` → `dashboard/*`

## Deployment Scenarios

### Scenario 1: Full Platform (Recommended)
```bash
npm install
npm start
cd app && npm run build
# Access: http://localhost:3000
```

### Scenario 2: Backend-Only (Headless Server)
```bash
npm install
npm run api
# API available at http://localhost:3000
# CLI disabled
```

### Scenario 3: Docker Deployment
```dockerfile
FROM node:20
WORKDIR /app
COPY . .
RUN npm install
RUN npm run build
RUN npm run app:build
CMD ["npm", "start"]
EXPOSE 3000
```

### Scenario 4: Monorepo CI/CD
```bash
# Root backend build
npm install && npm run build

# App frontend build
cd app
npm install && npm run build
```

## Language Composition

| Language   | Purpose                              | Path          |
|-----------|--------------------------------------|---------------|
| TypeScript | Core runtime, engine, API, CLI       | Root + /api, /engine, /cli, /core, /signals |
| TypeScript | Frontend UI components               | /app/src      |
| JavaScript | Compiled output (if using .js)       | /dist (generated) |
| HTML/CSS   | Browser-based dashboards             | /core/dashboard, /dashboard |
| JSON       | Configuration, data                  | *.json        |

**Expected Composition:**
- **TypeScript: ~97%** (main runtime)
- **JavaScript: ~2%** (legacy/output)
- **Other: ~1%** (configs, HTML, etc.)

## Inter-Platform Communication

### Backend ↔ Frontend
**WebSocket (Real-time):**
```typescript
// Server: engine/system/systemLoopIntegration.ts
broadcast({
  tick: integration.tick,
  global: integration.system.global,
  signals: globalSignals,
  dashboard: dashboardEngine.getState(),
})

// Client: app/src/liveStream.ts
ws.onmessage = (event) => {
  const state = JSON.parse(event.data)
  updateDashboard(state)
}
```

**REST (On-demand):**
```typescript
// GET /state
// GET /nodes
// GET /signals
// GET /dashboard
```

### CLI ↔ Engine
**Direct Function Calls:**
```typescript
// CLI: cli/integration/cliIntegration.ts
cliDispatch("tick", integration)
  → runOneTick(integration)
  → updates shared state
```

## Debugging & Development

### Enable Full Verbose Logging
```bash
DEBUG=* npm start
```

### Run Engine Only (No API)
```bash
npm run engine
```

### Inspect API Responses
```bash
curl http://localhost:3000/state
curl http://localhost:3000/nodes
curl http://localhost:3000/signals
```

### Frontend Dev with Hot Reload
```bash
npm run app:dev
# Vite dev server: http://localhost:5173
# Connects to backend: http://localhost:3000
```

## Future Extensions

This architecture supports:
- **Mobile apps** (React Native via shared core modules)
- **CLI tools** (Standalone binaries via pkg)
- **Embedded systems** (IoT nodes via minimal engine)
- **Distributed deployment** (Multiple engine nodes + central coordinator)
- **Plugin system** (Custom pillars, audits, commands)

---

**Last Updated:** 2026-09-30  
**Canonical Entry:** `start.ts`  
**Platform:** Node.js 18+, React 18+, TypeScript 5.0+
