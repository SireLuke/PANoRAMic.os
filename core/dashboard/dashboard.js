async function fetchJSON(url) {
  const res = await fetch(url)
  return await res.json()
}

async function updateDashboard() {
  try {
    const signals = await fetchJSON("http://localhost:3000/signals")
    const nodes = await fetchJSON("http://localhost:3000/nodes")
    const pillars = await fetchJSON("http://localhost:3000/pillars")

    document.getElementById("signals").textContent =
      JSON.stringify(signals, null, 2)

    document.getElementById("nodes").textContent =
      JSON.stringify(nodes, null, 2)

    document.getElementById("pillars").textContent =
      JSON.stringify(pillars, null, 2)

  } catch (err) {
    console.error("Dashboard error:", err)
  }
}

// Update every second
setInterval(updateDashboard, 1000)

updateDashboard()
