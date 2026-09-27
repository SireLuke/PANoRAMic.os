import React from "react"

export function NodesPanel({ data }) {
  return (
    <div>
      <h2>Node Status</h2>
      <p>Node ID: {data.nodeId}</p>
      <p>Health: {data.nodeHealthIndex}</p>
      <p>Autonomy: {data.nodeAutonomyIndex}</p>
      <p>Connectivity: {data.nodeConnectivityIndex}</p>
      <p>Storage Capacity: {data.nodeStorageCapacity}</p>
      <p>AI Presence: {data.nodeAiPresenceIndex}</p>
    </div>
  )
}
