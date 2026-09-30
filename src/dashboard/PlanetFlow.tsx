import React from "react"
import { DashboardPacket } from "../engine/world/dashboard.ts"

interface Props {
  packet: DashboardPacket
}

export default function PlanetFlow({ packet }: Props) {
  const { collapseRisk, recoveryStrength, coherence } = packet

  return (
    <div style={styles.container}>
      <h2 style={styles.header}>🌐 Planetary Flow</h2>

      <div style={styles.flowGrid}>
        <FlowBar
          label="Collapse Pressure"
          value={collapseRisk}
          color="#ff3b3b"
        />

        <FlowBar
          label="Recovery Strength"
          value={recoveryStrength}
          color="#4caf50"
        />

        <FlowBar
          label="Coherence"
          value={coherence}
          color="#2196f3"
        />
      </div>
    </div>
  )
}

function FlowBar({
  label,
  value,
  color,
}: {
  label: string
  value: number
  color: string
}) {
  const pct = Math.min(Math.max(value, 0), 1) * 100

  return (
    <div style={styles.flowItem}>
      <div style={styles.flowLabel}>{label}</div>
      <div style={styles.barOuter}>
        <div
          style={{
            ...styles.barInner,
            width: `${pct}%`,
            backgroundColor: color,
          }}
        />
      </div>
      <div style={styles.flowValue}>{value.toFixed(3)}</div>
    </div>
  )
}

const styles: Record<string, React.CSSProperties> = {
  container: {
    marginTop: "40px",
    padding: "20px",
    backgroundColor: "#181818",
    borderRadius: "10px",
    color: "#eee",
  },
  header: {
    fontSize: "1.6rem",
    marginBottom: "20px",
  },
  flowGrid: {
    display: "grid",
    gridTemplateColumns: "1fr",
    gap: "20px",
  },
  flowItem: {
    display: "flex",
    flexDirection: "column",
    gap: "8px",
  },
  flowLabel: {
    fontSize: "1rem",
    color: "#ccc",
  },
  barOuter: {
    width: "100%",
    height: "20px",
    backgroundColor: "#333",
    borderRadius: "10px",
    overflow: "hidden",
  },
  barInner: {
    height: "100%",
    borderRadius: "10px",
    transition: "width 0.4s ease",
  },
  flowValue: {
    fontSize: "0.9rem",
    color: "#aaa",
  },
}
