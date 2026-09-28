import { createNodeMap } from "./nodeMap" // if you have createNodeMap, else build a small map
import { updateNodeMap } from "./updateNodeMap"

// sample minimal NodeState objects (match your NODES_STATE shape)
const nodes = {
  "n1": createNodeState({ id: "n1", name: "A", nodeType: "city", latitude:0, longitude:0, populationCapacity:1000, resourceCapacity:1 }),
  "n2": createNodeState({ id: "n2", name: "B", nodeType: "city", latitude:1, longitude:1, populationCapacity:800, resourceCapacity:0.8 })
}

// connect them if your state uses connections
nodes["n1"].connections = ["n2"]
nodes["n2"].connections = ["n1"]

console.log("before", nodes["n1"].healthIndex, nodes["n2"].healthIndex)
const updated = updateNodeMap(nodes)
console.log("after", updated["n1"].healthIndex, updated["n2"].healthIndex)
