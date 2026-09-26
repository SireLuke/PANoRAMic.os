import React from "react"

export function MicroAiPanel({ data }) {
  return (
    <div>
      <h2>Micro-AI & Node Intelligence</h2>
      <p>Node Intelligence: {data.nodeIntelligenceIndex}</p>
      <p>Retrieval Quality: {data.retrievalQualityIndex}</p>
      <p>Cooperative Agent Count: {data.cooperativeAgentCount}</p>
      <p>Local Autonomy: {data.localAutonomyIndex}</p>
      <p>Safety Guardrails: {data.safetyGuardrailIndex}</p>
      <p>Micro-AI Coverage: {data.microAiCoverageIndex}</p>
    </div>
  )
}
