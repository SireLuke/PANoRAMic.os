const canvas = document.getElementById("mapCanvas")
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

function drawConnection(nodeA, nodeB) {
  const { x: xA, y: yA } = latLongToXY(nodeA.latitude, nodeA.longitude)
  const { x: xB, y: yB } = latLongToXY(nodeB.latitude, nodeB.longitude)

  // Color based on stability/risk
  const stability = (nodeA.stability + nodeB.stability) / 2
  const risk = (nodeA.risk + nodeB.risk) / 2

  const color = `rgba(${risk * 255}, ${stability * 255}, 50, 0.7)`

  // Thickness based on resilience
  const resilience = (nodeA.resilience + nodeB.resilience) / 2
  const thickness = 1 + resilience * 4

  ctx.strokeStyle = color
  ctx.lineWidth = thickness

  ctx.beginPath()
  ctx.moveTo(xA, yA)
  ctx.lineTo(xB, yB)
  ctx.stroke()
}

function drawNode(node) {
  const { x, y } = latLongToXY(node.latitude, node.longitude)

  const size = 10 + node.load * 20
  const stabilityColor = `rgb(${(1 - node.stability) * 255}, ${node.stability * 255}, 50)`
  const resilienceColor = `rgba(0, 255, 255, ${node.resilience})`

  ctx.fillStyle = stabilityColor
  ctx.beginPath()
  ctx.arc(x, y, size, 0, Math.PI * 2)
  ctx.fill()

  ctx.strokeStyle = resilienceColor
  ctx.lineWidth = 3
  ctx.stroke()

  return { x, y, size }
}

function renderMap() {
  ctx.clearRect(0, 0, canvas.width, canvas.height)

  // Draw connections first
  Object.values(nodes).forEach(node => {
    node.connections.forEach(connId => {
      const target = nodes[connId]
      if (target) drawConnection(node, target)
    })
  })

  // Draw nodes on top
  Object.values(nodes).forEach(drawNode)
}

function getClickedNode(xClick, yClick) {
  for (const node of Object.values(nodes)) {
    const { x, y } = latLongToXY(node.latitude, node.longitude)
    const size = 10 + node.load * 20

    const dx = xClick - x
    const dy = yClick - y
    if (Math.sqrt(dx * dx + dy * dy) <= size) {
      return node
    }
  }
  return null
}

canvas.addEventListener("click", (event) => {
  const rect = canvas.getBoundingClientRect()
  const xClick = event.clientX - rect.left
  const yClick = event.clientY - rect.top

  const node = getClickedNode(xClick, yClick)
  if (node) {
    document.getElementById("nodeName").textContent = node.name
    document.getElementById("nodeData").textContent =
      JSON.stringify(node, null, 2)
    document.getElementById("infoPanel").style.display = "block"
  }
})

async function loop() {
  await fetchNodes()
  renderMap()
}

setInterval(loop, 1000)
loop()
