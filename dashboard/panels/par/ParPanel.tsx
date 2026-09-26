import React from "react"

export function ParPanel({ data }) {
  return (
    <div>
      <h2>PAR Economy</h2>
      <p>Total PAR Supply: {data.totalParSupply}</p>
      <p>PAR Cap: {data.parCap}</p>
      <p>PAR in Circulation: {data.parInCirculation}</p>
      <p>Stewardship Fund: {data.stewardshipFund}</p>
      <p>Humanitarian Pool: {data.humanitarianPool}</p>
      <p>PAR Velocity: {data.parVelocity}</p>
      <p>PAR Burn Rate: {data.parBurnRate}</p>
      <p>PAR Mint Rate: {data.parMintRate}</p>
    </div>
  )
}
