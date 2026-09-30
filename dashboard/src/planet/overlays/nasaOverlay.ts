// dashboard/src/planet/overlays/NasaOverlay.ts

export function applyNasaOverlay(planet, payload) {
  const { oceanTemp, solarFlux, lat, lon } = payload

  // Convert lat/lon to 3D coordinates on the globe
  const pos = planet.latLonToVector3(lat, lon)

  // Temperature glow
  const tempIntensity = Math.min(oceanTemp / 40, 1)

  planet.addGlow({
    position: pos,
    color: `rgba(255, ${200 - tempIntensity * 200}, 0, ${tempIntensity})`,
    size: 0.8 + tempIntensity * 1.2
  })

  // Solar flux ring
  const fluxIntensity = Math.min(solarFlux / 300, 1)

  planet.addRing({
    position: pos,
    color: `rgba(255, 255, 0, ${fluxIntensity})`,
    radius: 1.0 + fluxIntensity * 2.0,
    thickness: 0.05
  })
}