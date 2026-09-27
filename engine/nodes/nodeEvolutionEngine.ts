// engine/nodes/nodeEvolutionEngine.ts

import { NodeState } from "../../core/pillars/nodes/NODES_STATE"
import { EcologyState } from "../../core/pillars/ecology/ECOLOGY_STATE"
import { InfrastructureState } from "../../core/pillars/infrastructure/INFRASTRUCTURE_STATE"
import { MicroAiState } from "../../core/pillars/microAI/MICRO_AI_STATE"

export function evolveNodes({
  nodes,
  ecology,
  infrastructure,
  microAi,
}: {
  nodes: NodeState[]
  ecology: EcologyState
  infrastructure: InfrastructureState
  microAi: MicroAiState
}): NodeState[] {
  const newNodes: NodeState[] = []

  for (const node of nodes) {
    let health = node.nodeHealthIndex
    let autonomy = node.nodeAutonomyIndex
    let connectivity = node.nodeConnectivityIndex

    // 1. Ecology affects node health
    health += ecology.regenerationIndex * 0.05
    health -= ecology.degradationIndex * 0.1

    // 2. Infrastructure affects connectivity
    connectivity += infrastructure.resilienceIndex * 0.05
    connectivity -= infrastructure.failureIndex * 0.1

    // 3. Micro-AI affects autonomy
    autonomy += microAi.microAiCoverageIndex * 0.05
    autonomy -= microAi.microAiFailureIndex * 0.1

    // 4. Node death condition
    if (health <= 0) {
      continue // node dies, do not add to newNodes
    }

    // 5. Node specialization
    if (autonomy > 0.8 && connectivity > 0.8) {
      // becomes a "Prime Node"
      autonomy += 0.05
      connectivity += 0.05
    }

    // 6. Node replication
    if (health > 0.9 && autonomy > 0.7) {
      const childNode: NodeState = {
        ...node,
        nodeId: `${node.nodeId}-child-${Math.random().toString(36).slice(2)}`,
        nodeHealthIndex: health * 0.5,
        nodeAutonomyIndex: autonomy * 0.5,
        nodeConnectivityIndex: connectivity * 0.5,
      }
      newNodes.push(childNode)
    }

    // 7. Node merging (rare)
    if (Math.random() < 0.0001 && nodes.length > 1) {
      const partner = nodes[Math.floor(Math.random() * nodes.length)]
      const mergedNode: NodeState = {
        ...node,
        nodeId: `${node.nodeId}-merge-${partner.nodeId}`,
        nodeHealthIndex: (health + partner.nodeHealthIndex) / 2,
        nodeAutonomyIndex: (autonomy + partner.nodeAutonomyIndex) / 2,
        nodeConnectivityIndex: (connectivity + partner.nodeConnectivityIndex) / 2,
      }
      newNodes.push(mergedNode)
      continue
    }

    // 8. Push updated node
    newNodes.push({
      ...node,
      nodeHealthIndex: health,
      nodeAutonomyIndex: autonomy,
      nodeConnectivityIndex: connectivity,
    })
  }

  return newNodes
}
