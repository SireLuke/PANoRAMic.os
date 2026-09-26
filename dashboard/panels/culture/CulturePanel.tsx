import React from "react"

export function CulturePanel({ data }) {
  return (
    <div>
      <h2>Culture & Identity</h2>
      <p>Cultural Cohesion: {data.culturalCohesionIndex}</p>
      <p>Identity Expression: {data.identityExpressionIndex}</p>
      <p>Heritage Preservation: {data.heritagePreservationIndex}</p>
      <p>Narrative Health: {data.narrativeHealthIndex}</p>
      <p>Cultural Access: {data.culturalAccessIndex}</p>
      <p>Cultural Vitality: {data.culturalVitalityIndex}</p>
    </div>
  )
}
