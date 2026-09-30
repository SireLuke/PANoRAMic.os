// dashboard/src/components/PlanetView/PlanetCanvas.tsx

import { Canvas } from "@react-three/fiber"
import EarthRenderer from "./EarthRenderer"

export default function PlanetCanvas() {
  return (
    <div style={{ width: "100%", height: "100%" }}>
      <Canvas camera={{ position: [0, 0, 5], fov: 45 }}>
        <EarthRenderer />
      </Canvas>
    </div>
  )
}