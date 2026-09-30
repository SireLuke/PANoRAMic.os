import React from "react"
import { DashboardPacket } from "../engine/world/dashboard.ts"

interface Props {
  packet: DashboardPacket
}

export default function PlanetHUD({ packet }: Props) {
  return (
    <div style={styles.hud}>
      <div style={styles.left}>
        <div style={styles.tick}>Tick {packet.tick}</div>
        <div style={styles.headline}>{packet.headline}</div>
      </div>

      <div style={styles.center}>
        <HUDMetric label="Health" value={packet.overallHealth} color="#4caf50" />
        <HUDMetric label="Collapse" value={packet.collapseRisk} color="#f44336" />
        <HUDMetric label="Recovery" value={packet.recoveryStrength} color="#8bc34a" />
        <HUDMetric label="Coherence" value={packet.coherence} color="#2196f3" />
      </div>

      <div style={styles.right}>
        <Pulse />
      </div>
    </div>
  )
}

function HUDMetric({
  label,
  value,
  color,
}: {
  label: string
  value: number
  color: string
}) {
  return (
    <div style={styles.metric}>
      <div style={styles.metricLabel}>{label}</div>
      <div style={{ ...styles.metricValue, color }}>{value.toFixed(3)}</div>
    </div>
  )
}

function Pulse() {
  return <div style={styles.pulse} />
}

const styles: Record<string, React.CSSProperties> = {
  hud: {
    position: "fixed",
    top: 0,
    left: 0,
    right: 0,
    height: "60px",
    backgroundColor: "#000000cc",
    backdropFilter: "blur(6px)",
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    padding: "0 20px",
    zIndex: 999,
    borderBottom: "1px solid #333",
    color: "#eee",
  },
  left: {
    display: "flex",
    flexDirection: "column",
    gap: "2px",
  },
  tick: {
    fontSize: "0.9rem",
    color: "#ccc",
  },
  headline: {
    fontSize: "1rem",
    fontWeight: "bold",
  },
  center: {
    display: "flex",
    gap: "20px",
  },
  metric: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
  },
  metricLabel: {
    fontSize: "0.75rem",
    color: "#bbb",
  },
  metricValue: {
    fontSize: "1rem",
    fontWeight: "bold",
  },
  right: {
    display: "flex",
    alignItems: "center",
  },
  pulse: {
    width: "12px",
    height: "12px",
    borderRadius: "50%",
    backgroundColor: "#4caf50",
    animation: "pulse 1.2s infinite ease-in-out",
  },
}
