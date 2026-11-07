export interface TopologyNode {
  readonly id: string;
  readonly kind?: "endpoint" | "junction" | "observation";
}

export interface TopologyEdge {
  readonly from: string;
  readonly to: string;
  readonly weight?: number;
}

export interface TopologyGraph {
  readonly directed: boolean;
  readonly nodes: readonly TopologyNode[];
  readonly edges: readonly TopologyEdge[];
}

export interface TopologyValidation {
  readonly valid: boolean;
  readonly errors: readonly string[];
}

/** Structural validation only; it does not infer physical junction dynamics. */
export function validateTopology(graph: TopologyGraph): TopologyValidation {
  const errors: string[] = [];
  const ids = new Set<string>();

  for (const node of graph.nodes) {
    if (!node.id || ids.has(node.id)) errors.push(`Invalid or duplicate node id: ${node.id}`);
    ids.add(node.id);
  }

  for (const edge of graph.edges) {
    if (!ids.has(edge.from)) errors.push(`Unknown edge source: ${edge.from}`);
    if (!ids.has(edge.to)) errors.push(`Unknown edge target: ${edge.to}`);
    if (edge.weight !== undefined && (!Number.isFinite(edge.weight) || edge.weight < 0)) {
      errors.push(`Edge weight must be finite and non-negative: ${edge.from}->${edge.to}`);
    }
  }

  return Object.freeze({ valid: errors.length === 0, errors: Object.freeze(errors) });
}
