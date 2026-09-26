import React from "react"

export function WorkforcePanel({ data }) {
  return (
    <div>
      <h2>Eco-Humanitarian Workforce</h2>
      <p>Participation Rate: {data.participationRate}</p>
      <p>Dignity Access: {data.dignityAccessScore}</p>
      <p>Skill Development: {data.skillDevelopmentIndex}</p>
      <p>Ecological Impact: {data.ecologicalImpactScore}</p>
      <p>Community Impact: {data.communityImpactScore}</p>
      <p>PAR Flow: {data.parEarningsFlow}</p>
      <p>Reintegration Score: {data.reintegrationScore}</p>
    </div>
  )
}

