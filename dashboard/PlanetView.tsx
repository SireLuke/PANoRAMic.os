import React, { useEffect, useState } from "react"
import { DashboardPacket } from "../engine/world/dashboard.ts"

interface Props {
  packet: DashboardPacket
}

export default function PlanetView({ packet }: Props) {
  const [nodes, setNodes] = useState(() => packet.status.nodesHealthy + packet.status.nodesUnstable + packet.status.nodesCritical)

  useEffect(() => {
    setNodes(packet.status.nodesHealthy + packet.status.nodesUnstable + packet.status.nodesCritical)
  }, [packet])

  return (
    <div style={styles.container}>
      <h2 style={styles.header}>🪐 Planet View</h2>

      <div style={styles.map}>
        {Object.entries(packet.report.world.nodes).map(([id, node]) => {
          const color = getNodeColor(node)
          return (
            <div key={id} style={{ ...styles.node, backgroundColor: color }}>
              <div style={styles.nodeLabel}>{id}</div>
            </div>
          )
        })}
      </div>
    </div>
  )
}

function getNodeColor(node: any): string {
  if (node.collapse >= 0.7) return "#ff3b3b" // critical
  if (node.stability <= 0.6) return "#ffb347" // unstable
  return "#4caf50" // healthy
}

const styles: Record<string, React.CSSProperties> = {
  container: {
    marginTop: "40px",
    padding: "20px",
    backgroundColor: "#181818",
    borderRadius: "10px",
  },
  header: {
    fontSize: "1.6rem",
    marginBottom: "20px",
    color: "#eee",
  },
  map: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fill, minmax(80px, 1fr))",
    gap: "10px",
  },
  node: {
    width: "80px",
    height: "80px",
    borderRadius: "8px",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    color: "#fff",
    fontSize: "0.8rem",
    fontWeight: "bold",
    border: "1px solid #333",
  },
  nodeLabel: {
    textAlign: "center",
  },
}
