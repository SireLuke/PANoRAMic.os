// dashboard/src/PANDashboard.tsx

import React from "react"
import { theme } from "./theme"
import { Pulse } from "./Pulse"

export const PANDashboard = ({ synthesis, risk, stability, globalScore }) => {
  return (
    <main style={styles.container}>
      <div style={styles.starfield}></div>

      <h1 style={styles.header}>PANoRAMic.OS</h1>
      <h2 style={styles.subheader}>Global Planetary Dashboard</h2>

      <section style={styles.globalScore}>
        <h3 style={styles.sectionHeader}>Global Score</h3>
        <div style={styles.scoreValue}>{globalScore.toFixed(2)}</div>
      </section>

      <section style={styles.grid}>
        {Object.keys(synthesis).map((pillar) => (
          <div key={pillar} style={styles.card}>
            <h3 style={styles.cardHeader}>{pillar.toUpperCase()}</h3>

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
          </div>
        ))}
      </section>
    </main>
  )<section style={styles.globalScore}>
  <Pulse trigger={globalScore} />
  <h3 style={styles.sectionHeader}>Global Score</h3>
  <div style={styles.scoreValue}>{globalScore.toFixed(2)}</div>
</section>
}

const styles = {
  container: {
    position: "relative",
    padding: "2rem",
    background: `linear-gradient(180deg, #07122a, #0a1a3d, #11245a)`,
    color: theme.text,
    minHeight: "100vh",
    fontFamily: "Segoe UI, sans-serif",
    overflow: "hidden",
  },

  starfield: {
    position: "absolute",
    top: 0,
    left: 0,
    width: "100%",
    height: "100%",
    backgroundImage: generateStarfield(),
    backgroundRepeat: "repeat",
    opacity: 0.35,
    pointerEvents: "none",
  },

  header: {
    fontSize: "3rem",
    textAlign: "center",
    color: theme.accent,
    marginBottom: "0.5rem",
    textShadow: "0 0 12px rgba(212,175,55,0.6)",
  },

  subheader: {
    fontSize: "1.4rem",
    textAlign: "center",
    color: theme.text,
    marginBottom: "2rem",
  },

  globalScore: {
    textAlign: "center",
    marginBottom: "2rem",
  },

  scoreValue: {
    fontSize: "3.5rem",
    fontWeight: "bold",
    color: theme.accent,
    textShadow: "0 0 18px rgba(212,175,55,0.7)",
  },

  grid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(300px, 1fr))",
    gap: "1.5rem",
  },

  card: {
    backgroundColor: theme.card,
    padding: "1.5rem",
    borderRadius: "12px",
    border: `1px solid ${theme.accent}`,
    boxShadow: "0 0 12px rgba(212,175,55,0.25)",
  },

  cardHeader: {
    marginBottom: "1rem",
    fontSize: "1.4rem",
    color: theme.accent,
  },

  metric: {
    display: "flex",
    justifyContent: "space-between",
    marginBottom: "0.5rem",
    fontSize: "1.1rem",
  },
}

// Generates a golden starfield background
function generateStarfield() {
  const stars = []
  for (let i = 0; i < 200; i++) {
    const x = Math.random() * 100
    const y = Math.random() * 100
    const size = Math.random() * 1 + 0.5
    const opacity = Math.random() * 0.5 + 0.3
    stars.push(
      `radial-gradient(circle ${size}px at ${x}% ${y}%, ${theme.star} ${opacity}, transparent 70%)`
    )
  }
  return stars.join(", ")
}