async function fetchProvenance() {
  const res = await fetch("http://localhost:3000/provenance")
  return await res.json()
}

function renderProvenance(records) {
  const body = document.getElementById("provBody")
  body.innerHTML = ""

  records.forEach(rec => {
    const tr = document.createElement("tr")

    const time = new Date(rec.timestamp).toLocaleString()
    const affected = [
      ...(rec.affectedNodes || []),
      ...(rec.affectedPillars || []),
      ...(rec.affectedGlobals || [])
    ].join(", ")

    tr.innerHTML = `
      <td>${time}</td>
      <td>${rec.funnelType}</td>
      <td>${rec.sourceName}</td>
      <td>${(rec.trustScore * 100).toFixed(1)}%</td>
      <td>${affected}</td>
    `

    body.appendChild(tr)
  })
}

async function update() {
  try {
    const records = await fetchProvenance()
    renderProvenance(records)
  } catch (err) {
    console.error("Provenance viewer error:", err)
  }
}

setInterval(update, 2000)
update()