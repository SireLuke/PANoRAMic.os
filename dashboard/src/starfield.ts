import { theme } from "./theme"

export function generateStarfield(count = 200) {
  const stars = []
  for (let i = 0; i < count; i++) {
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