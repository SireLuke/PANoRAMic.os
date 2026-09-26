import React from "react"

export function EcologyPanel({ data }) {
  return (
    <div>
      <h2>Ecology & Planetary Stability</h2>
      <p>Carrying Capacity: {data.carryingCapacityIndex}</p>
      <p>Regeneration Velocity: {data.regenerationVelocity}</p>
      <p>Ecological Debt: {data.ecologicalDebt}</p>
      <p>Biodiversity: {data.biodiversityScore}</p>
      <p>Pollution Load: {data.pollutionLoadIndex}</p>
      <p>Water Security: {data.waterSecurityIndex}</p>
      <p>Energy Renewability: {data.energyRenewabilityIndex}</p>
    </div>
  )
}
