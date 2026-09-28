import React, { useEffect, useState } from "react"
import { DashboardPacket } from "../engine/world/dashboard.ts"

interface Props {
  packet: DashboardPacket
}

interface TimelinePoint {
  tick: number
  collapse: number
  recovery: number
  coherence: number
}

export default function PlanetTimeline({ packet }: Props) {
  const [timeline, setTimeline] = useState<TimelinePoint[]>([])

  useEffect(() => {
    const point: TimelinePoint = {
      tick: packet.tick,
      collapse: packet.collapseRisk,
      recovery: packet.recoveryStrength,
      coherence: packet.coherence,
    }

    setTimeline(prev => [...prev.slice(-99), point]) // keep last 100 ticks
  }, [packet])

  return (
    <div style={styles.container}>
      <h2 style={styles.header}>⏳ Planet Timeline</h2>

      <div style={styles.chart}>
        {timeline.map((p, i) => (
          <div key={i} style={styles.row}>
            <div style={styles.tickLabel}>Tick {p.tick}</div>

            <Bar label="Collapse" value={p.collapse} color="#f44336" />
            <Bar label="Recovery" value={p.recovery} color="#4caf50" />
            <Bar label="Coherence" value={p.coherence} color="#2196f3" />
          </div>
        ))}
      </div>
    </div>
  )
}

function Bar({
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
    <div style={styles.barItem}>
      <div style={styles.barLabel}>{label}</div>
      <div style={styles.barOuter}>
        <div
          style={{
            ...styles.barInner,
            width: `${pct}%`,
            backgroundColor: color,
          }}
        />
      </div>
      <div style={styles.barValue}>{value.toFixed(3)}</div>
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
  chart: {
    display: "flex",
    flexDirection: "column",
    gap: "12px",
    maxHeight: "500px",
    overflowY: "auto",
  },
  row: {
    display: "grid",
    gridTemplateColumns: "120px 1fr 1fr 1fr",
    gap: "10px",
    alignItems: "center",
  },
  tickLabel: {
    color: "#ccc",
    fontSize: "0.9rem",
  },
  barItem: {
    display: "flex",
    flexDirection: "column",
    gap: "4px",
  },
  barLabel: {
    fontSize: "0.8rem",
    color: "#bbb",
  },
  barOuter: {
    width: "100%",
    height: "16px",
    backgroundColor: "#333",
    borderRadius: "8px",
    overflow: "hidden",
  },
  barInner: {
    height: "100%",
    borderRadius: "8px",
    transition: "width 0.3s ease",
  },
  barValue: {
    fontSize: "0.75rem",
    color: "#aaa",
  },
}
