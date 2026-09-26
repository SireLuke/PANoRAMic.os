import React from "react"

export function LaborPanel({ data }) {
  return (
    <div>
      <h2>Labor & Cooperative Work</h2>
      <p>Labor Dignity: {data.laborDignityIndex}</p>
      <p>Fair Compensation: {data.fairCompensationIndex}</p>
      <p>Labor Safety: {data.laborSafetyIndex}</p>
      <p>Skill Mobility: {data.skillMobilityIndex}</p>
      <p>Labor Stability: {data.laborStabilityIndex}</p>
      <p>Cooperative Labor Rate: {data.cooperativeLaborRate}</p>
    </div>
  )
}
