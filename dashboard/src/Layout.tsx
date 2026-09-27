import React from "react"
import { generateStarfield } from "./starfield"
import { theme } from "./theme"

export const Layout = ({ children }) => {
  return (
    <div style={styles.container}>
      <div style={styles.starfield}></div>
      {children}
    </div>
  )
}

const styles = {
  container: {
    position: "relative",
    minHeight: "100vh",
    padding: "2rem",
    background: `linear-gradient(180deg, ${theme.baseDark}, ${theme.base}, ${theme.baseLight})`,
    color: theme.text,
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
}