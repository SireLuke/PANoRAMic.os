import React from "react"

export function CommonsPanel({ data }) {
  return (
    <div>
      <h2>Commons & Shared Resources</h2>
      <p>Shared Resource Access: {data.sharedResourceAccessIndex}</p>
      <p>Public Goods Health: {data.publicGoodsHealthIndex}</p>
      <p>Stewardship Participation: {data.stewardshipParticipationRate}</p>
      <p>Commons Sustainability: {data.commonsSustainabilityIndex}</p>
      <p>Cooperative Use Rate: {data.cooperativeUseRate}</p>
      <p>Commons Equity: {data.commonsEquityIndex}</p>
    </div>
  )
}
