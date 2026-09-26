import React from "react"

export function RightsPanel({ data }) {
  return (
    <div>
      <h2>Universal Human Rights</h2>
      <p>Gender Equality: {data.genderEqualityIndex}</p>
      <p>Identity Inclusion: {data.identityInclusionScore}</p>
      <p>Bodily Autonomy: {data.bodilyAutonomyAccessIndex}</p>
      <p>Anti-Discrimination: {data.antiDiscriminationSignal}</p>
      <p>Violence Risk: {data.violenceRiskIndex}</p>
      <p>Rights Protection: {data.rightsProtectionIndex}</p>
    </div>
  )
}
