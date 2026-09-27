import React from "react"
import { Card } from "./Card"
import { Pulse } from "./Pulse"
import { theme } from "./theme"

export const PANDashboard = ({ synthesis, risk, stability, globalScore }) => {
  return (
    <div>
      <Pulse trigger={globalScore} />

      <h1 style={styles.header}>PANoRAMic.OS</h1>
      <h2 style={styles.subheader}>Planetary Command Dashboard</h2>

      <Card title="Global Score">
        <div style={styles.score}>{globalScore.toFixed(2)}</div>
      </Card>

      <div style={styles.grid}>
        {Object.keys(synthesis).map((pillar) => (
          <Card key={pillar} title={pillar.toUpperCase()}>
            <div style={styles.metric}>
              <span>Synthesis</span>
              <strong>{synthesis[pillar].synthesisScore.toFixed(2)}</strong>
            </div>
            <div style={styles.metric}>
              <span>Risk</span>
              <strong>{risk[pillar].riskScore.toFixed(2)}</strong>
            </div>
            <div style={styles.metric}>
              <span>Stability</span>
              <strong>{stability[pillar].stabilityScore.toFixed(2)}</strong>
            </div>
          </Card>
        ))}
      </div>
    </div>
  )
}

const styles = {
  header: {
    fontSize: "3rem",
    textAlign: "center",
    color: theme.accent,
    textShadow: `0 0 12px ${theme.glow}`,
    marginBottom: "0.5rem",
  },
  subheader: {
    fontSize: "1.4rem",
    textAlign: "center",
    color: theme.textDim,
    marginBottom: "2rem",
  },
  score: {
    fontSize: "3.5rem",
    color: theme.accent,
    textShadow: `0 0 18px ${theme.glow}`,
    textAlign: "center",
  },
  grid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(300px, 1fr))",
    gap: "1.5rem",
  },
  metric: {
    display: "flex",
    justifyContent: "space-between",
    marginBottom: "0.5rem",
    fontSize: "1.1rem",
  },
}