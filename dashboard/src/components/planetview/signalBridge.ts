// dashboard/src/components/PlanetView/SignalBridge.ts

let handlers: Array<(signal: any) => void> = []

export function listenToPanOsSignals(handler: (signal: any) => void) {
  handlers.push(handler)
}

// This would be replaced with WebSocket or SSE later
export function emitPanOsSignal(signal: any) {
  handlers.forEach((h) => h(signal))
}