// dashboard/src/Pulse.tsx

import React, { useEffect, useState } from "react"
import { theme } from "./theme"

export const Pulse = ({ trigger }) => {
  const [active, setActive] = useState(false)

  useEffect(() => {
    if (trigger) {
      setActive(true)
      setTimeout(() => setActive(false), 600)
    }
  }, [trigger])

  return (
    <div
      style={{
        ...styles.pulse,
        opacity: active ? 0.8 : 0,
        transform: active ? "scale(1.4)" : "scale(1)",
      }}
    />
  )
}

const styles = {
  pulse: {
    position: "absolute",
    top: "50%",
    left: "50%",
    width: "200px",
    height: "200px",
    borderRadius: "50%",
    background: theme.accent,
    filter: "blur(40px)",
    transform: "translate(-50%, -50%)",
    transition: "all 0.6s ease-out",
    pointerEvents: "none",
  },
}