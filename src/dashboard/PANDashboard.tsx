import React, { useEffect, useState } from "react"
import { buildDashboard } from "../../engine/world/dashboard.ts"
import { WorldState } from "../../engine/world/worldState.ts"
import { TickResult } from "../../engine/world/tick.ts"
import PlanetView from "./PlanetView.tsx"
import PlanetFlow from "./PlanetFlow.tsx"
import PlanetTimeline from "./PlanetTimeline.tsx"

interface Props {
  world: WorldState
  onTick?: () => TickResult
}

export default function PANDashboard({ world }: Props) {
  const [packet, setPacket] = useState(() =>
    buildDashboard({ world, signals: world.synthesis, tick: world.tick })
  )

  useEffect(() => {
    setPacket(
      buildDashboard({ world, signals: world.synthesis, tick: world.tick })
    )
  }, [world])

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
        {Object.entries(packet.subsystem ?? {}).map(([key, value]) => (
          <Panel key={key} title={key} value={value as number} />
        ))}
      </div>

      <PlanetView packet={packet} />
      <PlanetFlow packet={packet} />
      <PlanetTimeline packet={packet} />
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

const styles: Record<string, React.CSSProperties> = {
  container: {
    padding: "20px",
    fontFamily: "Arial, sans-serif",
    color: "#eee",
    backgroundColor: "#111",
    minHeight: "100vh",
  },
  header: {
    marginBottom: "0.25rem",
  },
  subheader: {
    fontWeight: "normal",
    color: "#aaa",
  },
  section: {
    marginTop: "1.5rem",
  },
  grid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(160px, 1fr))",
    gap: "12px",
  },
  subsystemGrid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(140px, 1fr))",
    gap: "12px",
  },
  panel: {
    background: "#1c1c1c",
    padding: "12px",
    borderRadius: "8px",
  },
  value: {
    fontSize: "1.25rem",
  },
}
