// dashboard/src/components/PlanetView/SignalBridge.ts
useEffect(() => {
  listenToPanOsSignals((signal) => {
    if (signal.type === "nodeUpdate" && signal.payload.sourceName === "NOAA") {
      applyNoaaOverlay(earthRef.current, signal.payload)
    }
  })
}, [])
let handlers: Array<(signal: any) => void> = []

export function listenToPanOsSignals(handler: (signal: any) => void) {
  handlers.push(handler)
}

// This would be replaced with WebSocket or SSE later
export function emitPanOsSignal(signal: any) {
  handlers.forEach((h) => h(signal))
}