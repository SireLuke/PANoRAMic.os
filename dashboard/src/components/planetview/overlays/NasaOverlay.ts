// dashboard/src/components/PlanetView/overlays/NasaOverlay.ts

import * as THREE from "three"

export function applyNasaOverlay(earthMesh, payload) {
  const { oceanTemp, solarFlux, lat, lon } = payload

  // Convert lat/lon to 3D position
  const phi = (90 - lat) * (Math.PI / 180)
  const theta = (lon + 180) * (Math.PI / 180)

  const x = -Math.sin(phi) * Math.cos(theta)
  const y = Math.cos(phi)
  const z = Math.sin(phi) * Math.sin(theta)

  const pos = new THREE.Vector3(x, y, z)

  // Create a glow sprite
  const spriteMaterial = new THREE.SpriteMaterial({
    color: new THREE.Color(`hsl(${(oceanTemp / 40) * 60}, 100%, 50%)`),
    opacity: 0.6
  })

  const sprite = new THREE.Sprite(spriteMaterial)
  sprite.scale.set(0.2, 0.2, 0.2)
  sprite.position.copy(pos.multiplyScalar(1.01))

  earthMesh.add(sprite)
}