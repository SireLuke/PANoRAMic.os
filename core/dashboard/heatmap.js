const canvas = document.getElementById("heatCanvas")
const ctx = canvas.getContext("2d")

canvas.width = window.innerWidth
canvas.height = window.innerHeight

let nodes = {}

async function fetchNodes() {
  const res = await fetch("http://localhost:3000/nodes")
  nodes = await res.json()
}

function latLongToXY(lat, long) {
  const x = (long + 180) * (canvas.width / 360)
  const y = (90 - lat) * (canvas.height / 180)
  return { x, y }
}

function drawHeatPoint(node) {
  const { x, y } = latLongToXY(node.latitude, node.longitude)

  const pressure = node.collapseRisk + node.risk + node.load - node.resilience
  const intensity = Math.max(0, Math.min(1, pressure))

  const radius = 40 + intensity * 80

  const gradient = ctx.createRadialGradient(x, y, 0, x, y, radius)
  gradient.addColorStop(0, `rgba(255, ${100 - intensity * 100}, 0, 0.8)`)
  gradient.addColorStop(1, `rgba(255, 0, 0, 0)`)

  ctx.fillStyle = gradient
  ctx.beginPath()
  ctx.arc(x, y, radius, 0, Math.PI * 2)
  ctx.fill()
}

async function renderHeatmap() {
  ctx.clearRect(0, 0, canvas.width, canvas.height)

  Object.values(nodes).forEach(drawHeatPoint)
}

async function loop() {
  await fetchNodes()
  renderHeatmap()
}

setInterval(loop, 1000)
loop()
