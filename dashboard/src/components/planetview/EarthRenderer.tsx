// dashboard/src/components/PlanetView/EarthRenderer.tsx

import { useRef, useEffect } from "react"
import { useFrame } from "@react-three/fiber"
import * as THREE from "three"
import { listenToPanOsSignals } from "./SignalBridge"
import { applyNasaOverlay } from "./overlays/NasaOverlay"

useEffect(() => {
  listenToPanOsSignals((signal) => {
    if (signal.type === "nodeUpdate" && signal.payload.sourceName === "NASA POWER") {
      applyNasaOverlay(earthRef.current, signal.payload)
    }
  })
}, [])

export default function EarthRenderer() {
  const earthRef = useRef<THREE.Mesh>(null)

  // Basic Earth sphere
  const texture = new THREE.TextureLoader().load("/textures/earth_day.jpg")

  useEffect(() => {
    listenToPanOsSignals((signal) => {
      // We will attach NASA overlays here later
      console.log("Planet received signal:", signal)
    })
  }, [])

  useFrame(() => {
    if (earthRef.current) {
      earthRef.current.rotation.y += 0.0005
    }
  })

  return (
    <mesh ref={earthRef}>
      <sphereGeometry args={[1, 64, 64]} />
      <meshStandardMaterial map={texture} />
    </mesh>
  )
}