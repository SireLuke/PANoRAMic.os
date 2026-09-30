// dashboard/src/components/PlanetView/overlays/NoaaOverlay.ts

import * as THREE from "three"

export function applyNoaaOverlay(earthMesh, payload) {
  const { temperature, windSpeed, shortForecast, lat, lon } = payload

  // Convert lat/lon to 3D position
  const phi = (90 - lat) * (Math.PI / 180)
  const theta = (lon + 180) * (Math.PI / 180)

  const x = -Math.sin(phi) * Math.cos(theta)
  const y = Math.cos(phi)
  const z = Math.sin(phi) * Math.sin(theta)

  const pos = new THREE.Vector3(x, y, z)

  // Storm spiral if thunderstorms
  if (shortForecast.toLowerCase().includes("storm")) {
    const spiral = new THREE.Mesh(
      new THREE.RingGeometry(0.1, 0.3, 32),
      new THREE.MeshBasicMaterial({
        color: "rgba(255, 255, 255, 0.8)",
        side: THREE.DoubleSide
      })
    )

    spiral.position.copy(pos.multiplyScalar(1.01))
    spiral.rotation.x = Math.PI / 2

    earthMesh.add(spiral)

    // Animate spiral
    let t = 0
    const animate = () => {
      t += 0.02
      spiral.rotation.z = t
      requestAnimationFrame(animate)
    }
    animate()
  }

  // Wind arc
  const windIntensity = Math.min(windSpeed / 50, 1)

  const arcMaterial = new THREE.LineBasicMaterial({
    color: `rgba(0, 150, 255, ${windIntensity})`
  })

  const arcPoints = []
  for (let i = 0; i < 20; i++) {
    arcPoints.push(
      new THREE.Vector3(
        pos.x * (1 + i * 0.01),
        pos.y * (1 + i * 0.01),
        pos.z * (1 + i * 0.01)
      )
    )
  }

  const arcGeometry = new THREE.BufferGeometry().setFromPoints(arcPoints)
  const arc = new THREE.Line(arcGeometry, arcMaterial)

  earthMesh.add(arc)

  // Temperature glow
  const tempIntensity = Math.min(temperature / 120, 1)

  const spriteMaterial = new THREE.SpriteMaterial({
    color: new THREE.Color(`hsl(${(temperature / 120) * 60}, 100%, 50%)`),
    opacity: 0.5
  })

  const sprite = new THREE.Sprite(spriteMaterial)
  sprite.scale.set(0.25, 0.25, 0.25)
  sprite.position.copy(pos.multiplyScalar(1.01))

  earthMesh.add(sprite)
}