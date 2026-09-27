// dashboard/src/PARCurve.tsx

import React from "react"
import { theme } from "./theme"

export const PARCurve = ({ history }) => {
  if (!history || history.length === 0) return null

  const max = Math.max(...history)
  const min = Math.min(...history)

  const points = history
    .map((value, index) => {
      const x = (index / (history.length - 1)) * 100
      const y = 100 - ((value - min) / (max - min || 1)) * 100
      return `${x},${y}`
    })
    .join(" ")

  return (
    <div style={styles.container}>
      <h3 style={styles.header}>PAR Adoption Curve</h3>

      <svg viewBox="0 0 100 100" preserveAspectRatio="none" style={styles.svg}>
        <polyline
          points={points}
          fill="none"
          stroke={theme.accent}
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />

        {/* Glow */}
        <polyline
          points={points}
          fill="none"
          stroke={theme.glow}
          strokeWidth="6"
          strokeLinecap="round"
          strokeLinejoin="round"
          opacity="0.3"
        />
      </svg>
    </div>
  )
}

const styles = {
  container: {
    backgroundColor: theme.baseLight,
    padding: "1.5rem",
    borderRadius: "12px",
    border: `1px solid ${theme.accent}`,
    boxShadow: `0 0 12px ${theme.glow}`,
    marginBottom: "1.5rem",
  },
  header: {
    color: theme.accent,
    marginBottom: "1rem",
    fontSize: "1.4rem",
  },
  svg: {
    width: "100%",
    height: "200px",
  },
}