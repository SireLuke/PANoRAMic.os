import React from "react"
import { DashboardPacket } from "../engine/world/dashboard.ts"

interface Props {
  packet: DashboardPacket
}

export default function PlanetSignals({ packet }: Props) {
  const s = packet.status.signals

  return (
    <div style={styles.container}>
      <h2 style={styles.header}>📡 Planetary Signals</h2>

      <div style={styles.grid}>
        <SignalBar label="Stability" value={s.stability} color="#4caf50" />
        <SignalBar label="Risk" value={s.risk} color="#ff9800" />
        <SignalBar label="Resilience" value={s.resilience} color="#03a9f4" />
        <SignalBar label="Synthesis" value={s.synthesis} color="#9c27b0" />
        <SignalBar label="Flow" value={s.flow} color="#00bcd4" />
        <SignalBar
          label="Collapse Pressure"
          value={s.collapsePressure}
          color="#f44336"
        />
        <SignalBar
          label="Recovery Strength"
          value={s.recovery}
          color="#8bc34a"
        />
        <SignalBar label="Coherence" value={s.coherence} color="#3f51b5" />
      </div>
    </div>
  )
}

function SignalBar({
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
    <div style={styles.item}>
      <div style={styles.label}>{label}</div>
      <div style={styles.barOuter}>
        <div
          style={{
            ...styles.barInner,
            width: `${pct}%`,
            backgroundColor: color,
          }}
        />
      </div>
      <div style={styles.value}>{value.toFixed(3)}</div>
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
  grid: {
    display: "grid",
    gridTemplateColumns: "1fr",
    gap: "20px",
  },
  item: {
    display: "flex",
    flexDirection: "column",
    gap: "8px",
  },
  label: {
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
  value: {
    fontSize: "0.9rem",
    color: "#aaa",
  },
}
