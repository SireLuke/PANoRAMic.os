import React from "react"

export function ModesPanel({ data }) {
  return (
    <div>
      <h2>System Modes</h2>
      <p>Active Mode: {data.activeMode}</p>
      <p>Stability: {data.stabilityIndex}</p>
      <p>Responsiveness: {data.responsivenessIndex}</p>
      <p>Autonomy Level: {data.autonomyLevel}</p>
      <p>Safety Level: {data.safetyLevel}</p>
      <p>Mode Transition Rate: {data.modeTransitionRate}</p>
    </div>
  )
}
