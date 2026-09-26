import React from "react"

export function InfrastructurePanel({ data }) {
  return (
    <div>
      <h2>Planetary Infrastructure</h2>
      <p>Desalination Capacity: {data.desalinationCapacity}</p>
      <p>Solar Belt Output: {data.solarBeltOutput}</p>
      <p>Recycling Loop Efficiency: {data.recyclingLoopEfficiency}</p>
      <p>Waste-to-Energy Rate: {data.wasteToEnergyRate}</p>
      <p>Cooperative Housing Units: {data.cooperativeHousingUnits}</p>
      <p>Grid Stability: {data.gridStabilityIndex}</p>
      <p>Infrastructure Health: {data.infrastructureHealthIndex}</p>
    </div>
  )
}
