const canvas = document.getElementById("mapCanvas")
const ctx = canvas.getContext("2d")

canvas.width = window.innerWidth
canvas.height = window.innerHeight

async function fetchNodes() {
  const res = await fetch("http://localhost:3000/nodes")
  return await res.json()
}

function latLongToXY(lat, long) {
  // Simple equirectangular projection
  const x = (long + 180) * (canvas.width / 360)
  const y = (90 - lat) * (canvas.height / 180)
  return { x, y }
}

function drawNode(node) {
  const { x, y } = latLongToXY(node.latitude, node.longitude)

  const size = 10 + node.load * 20
  const stabilityColor = `rgb(${(1 - node.stability) * 255}, ${node.stability * 255}, 50)`
  const resilienceColor = `rgba(0, 255, 255, ${node.resilience})`

  // Node fill (stability)
  ctx.fillStyle = stabilityColor
  ctx.beginPath()
  ctx.arc(x, y, size, 0, Math.PI * 2)
  ctx.fill()

  // Node outline (resilience)
  ctx.strokeStyle = resilienceColor
  ctx.lineWidth = 3
  ctx.stroke()
}

async function renderMap() {
  ctx.clearRect(0, 0, canvas.width, canvas.height)

  const nodes = await fetchNodes()

  Object.values(nodes).forEach(drawNode)
}

setInterval(renderMap, 1000)
renderMap()
