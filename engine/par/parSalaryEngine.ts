// engine/par/parSalaryEngine.ts

export function computeParSalary({
  par,
  workforceRotation,
  nodes,
}: {
  par: any
  workforceRotation: any
  nodes: any[]
}) {
  // Dignity floor scales with population + dignityFloat
  const dignityFloor = par.dignityFloat * 100

  // Stewardship salary rewards ecological + infrastructure care
  const stewardshipSalary =
    dignityFloor +
    workforceRotation.skillGainRate * 50 +
    nodes.length * 2

  // Contribution salary rewards productive participation
  const contributionSalary =
    dignityFloor +
    workforceRotation.rotationIndex * 40

  // Node dividend distributes PAR to node operators
  const nodeDividend = nodes.length > 0
    ? (par.parMintRate * 0.05) / nodes.length
    : 0

  return {
    dignityFloor,
    stewardshipSalary,
    contributionSalary,
    nodeDividend,
  }
}
