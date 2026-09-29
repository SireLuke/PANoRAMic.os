async function fetchPillars() {
  const res = await fetch("http://localhost:3000/pillars")
  return await res.json()
}

function renderPillars(pillars) {
  const container = document.getElementById("pillarContainer")
  container.innerHTML = ""

  Object.entries(pillars).forEach(([name, data]) => {
    const div = document.createElement("div")
    div.className = "pillar"

    div.innerHTML = `
      <h2>${name.toUpperCase()}</h2>
      <pre>${JSON.stringify(data, null, 2)}</pre>
    `

    container.appendChild(div)
  })
}

async function update() {
  try {
    const pillars = await fetchPillars()
    renderPillars(pillars)
  } catch (err) {
    console.error("Pillar dashboard error:", err)
  }
}

setInterval(update, 1000)
update()
