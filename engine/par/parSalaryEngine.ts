import { ParState } from "../../core/pillars/par/PAR_STATE"
import { WorkforceRotationState } from "../../core/pillars/workforce/WORKFORCE_ROTATION_STATE"
import { NodeState } from "../../core/pillars/nodes/NODES_STATE"

export function computeParSalary({
  par,
  workforceRotation,
  nodes,
}: {
  par: ParState
  workforceRotation: WorkforceRotationState
  nodes: NodeState[]
}) {
  // 1. Dignity Floor (everyone gets this)
  const dignityFloor = par.parCap * 0.000001 // 0.0001% of PAR cap per person

  // 2. Stewardship Salary (you + maintainers)
  const stewardshipSalary =
    dignityFloor +
    (par.parCap * 0.00001) + // 0.001% of PAR cap
    workforceRotation.skillGainRate * 0.5

  // 3. Contribution Salary (workforce rotation)
  const contributionSalary =
    workforceRotation.skillGainRate +
    workforceRotation.burnoutReductionIndex +
    workforceRotation.workforceSatisfactionIndex

  // 4. Node Dividend (distributed to nodes)
  const nodeDividend = nodes.map(node => ({
    nodeId: node.nodeId,
    dividend:
      (node.nodeHealthIndex +
        node.nodeAutonomyIndex +
        node.nodeConnectivityIndex) *
      0.01, // 1% of node health/autonomy/connectivity
  }))

  return {
    dignityFloor,
    stewardshipSalary,
    contributionSalary,
    nodeDividend,
  }
}
