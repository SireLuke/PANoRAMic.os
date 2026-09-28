import React, { useEffect, useState } from "react"
import { buildDashboard } from "../engine/world/dashboard.ts"
import { WorldState } from "../engine/world/worldState.ts"
import { TickResult } from "../engine/world/tick.ts"
import { createLiveStream } from "./liveStream.ts"
import PlanetView from "./PlanetView.tsx"
import PlanetFlow from "./PlanetFlow.tsx"

interface Props {
  world: WorldState
  onTick: () => TickResult
}

export default function PANDashboard({ world }: Props) {
  const [packet, setPacket] = useState(() =>
    buildDashboard({ world, signals: world.synthesis, tick: world.tick })
  )

  const stream = createLiveStream("http://localhost:3000")

  useEffect(() => {
    stream.connect()

    stream.onPlanetUpdate(packet => {
      setPacket(packet)
    })

    return () => stream.disconnect()
  }, [])

  return (
    <div style={styles.container}>
      <h1 style={styles.header}>🌍 PANoRAMic.os — Planetary Dashboard</h1>
      <h2 style={styles.subheader}>{packet.headline}</h2>

      <div style={styles.grid}>
        <Panel title="Overall Health" value={packet.overallHealth} />
        <Panel title="Collapse Risk" value={packet.collapseRisk} />
        <Panel title="Recovery Strength" value={packet.recoveryStrength} />
        <Panel title="Coherence" value={packet.coherence} />
      </div>

      <h3 style={styles.section}>Node Health</h3>
      <div style={styles.grid}>
        <Panel title="Healthy Nodes" value={packet.nodesHealthy} />
        <Panel title="Unstable Nodes" value={packet.nodesUnstable} />
        <Panel title="Critical Nodes" value={packet.nodesCritical} />
      </div>

      <h3 style={styles.section}>Subsystem Summary</h3>
      <div style={styles.subsystemGrid}>
        {Object.entries(packet.subsystem).map(([key, value]) => (
          <Panel key={key} title={key} value={value} />
        ))}
      </div>

      {/* Planet Map */}
      <PlanetView packet={packet} />

      {/* Planet Flow */}
      <PlanetFlow packet={packet} />
    </div>
  )
}

function Panel({ title, value }: { title: string; value: number }) {
  return (
    <div style={styles.panel}>
      <h4>{title}</h4>
      <div style={styles.value}>
        {typeof value === "number" ? value.toFixed(3) : value}
      </div>
    </div>
  )
}

const styles = {
  container: {
    padding: "20px",
    fontFamily: "Arial, sans-serif",
    color: "#eee",
    backgroundColor: "#111",
    minHeight: "100vh",
  },
  header: {
    fontSize: "2rem",
    marginBottom: "10px",
  },
  subheader: {
    fontSize: "1.2rem",
    marginBottom: "20px",
    color: "#ccc",
  },
  section: {
    marginTop: "30px",
    marginBottom: "10px",
    fontSize: "1.3rem",
  },
  grid: {
    display: "grid",
    gridTemplateColumns: "repeat(4, 1fr)",
    gap: "15px",
  },
  subsystemGrid: {
    display: "grid",
    gridTemplateColumns: "repeat(5, 1fr)",
    gap: "15px",
  },
  panel: {
    backgroundColor: "#222",
    padding: "15px",
    borderRadius: "8px",
    textAlign: "center",
    border: "1px solid #333",
  },
  value: {
    marginTop: "10px",
    fontSize: "1.4rem",
    fontWeight: "bold",
    color: "#4caf50",
  },
}

