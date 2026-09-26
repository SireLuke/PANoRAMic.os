import React from "react"

export function WorkforceRotationPanel({ data }) {
  return (
    <div>
      <h2>Workforce Rotation System</h2>
      <p>Rotation Length (Hours): {data.rotationLengthHours}</p>
      <p>Disciplines Per Cycle: {data.disciplinesPerCycle}</p>
      <p>Skill Gain Rate: {data.skillGainRate}</p>
      <p>Burnout Reduction: {data.burnoutReductionIndex}</p>
      <p>Workforce Satisfaction: {data.workforceSatisfactionIndex}</p>
    </div>
  )
}
