import React from "react"
import { theme } from "./theme"

export const Card = ({ title, children }) => {
  return (
    <div style={styles.card}>
      <h3 style={styles.header}>{title}</h3>
      {children}
    </div>
  )
}

const styles = {
  card: {
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
}