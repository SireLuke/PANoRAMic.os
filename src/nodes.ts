export interface Node {
  id: string;
  type: "local" | "regional" | "biome" | "infrastructure" | "humanitarian";
  stability: number;
}

export function initNodes(): Node[] {
  const nodes: Node[] = [
    { id: "node-local-1", type: "local", stability: 0.8 },
    { id: "node-biome-1", type: "biome", stability: 0.75 },
    { id: "node-infra-1", type: "infrastructure", stability: 0.7 },
  ];

  return nodes;
}
