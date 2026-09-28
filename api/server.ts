// api/server.ts
import { initWorld } from "../engine/world/initWorld.ts"
import { tick } from "../engine/world/tick.ts"
import { buildDashboard } from "../engine/world/dashboard.ts"
import { createServer } from "http"
import { Server } from "socket.io"

const world = initWorld([])

const httpServer = createServer((req, res) => {
  if (req.url === "/" && req.method === "GET") {
    res.writeHead(200, { "Content-Type": "text/html" })
    res.end(`
      <!DOCTYPE html>
      <html>
      <head>
        <title>PANoRAMic.os Dashboard</title>
        <style>
          body {
            font-family: monospace;
            background: #0a0e27;
            color: #00ff88;
            margin: 20px;
            line-height: 1.6;
          }
          h1 {
            color: #00ffff;
          }
          #data {
            background: #1a1a2e;
            padding: 20px;
            border-radius: 5px;
            border: 1px solid #00ff88;
            max-height: 80vh;
            overflow-y: auto;
          }
          pre {
            margin: 0;
            color: #00ff88;
          }
          .status {
            color: #ffaa00;
            font-weight: bold;
          }
        </style>
      </head>
      <body>
        <h1>🌍 PANoRAMic.os Live Stream</h1>
        <p class="status" id="status">Connecting...</p>
        <div id="data">Waiting for data...</div>
        <script src="https://cdn.socket.io/4.5.4/socket.io.min.js"></script>
        <script>
          const socket = io();
          
          socket.on('connect', () => {
            document.getElementById('status').textContent = '✓ Connected';
            document.getElementById('status').style.color = '#00ff88';
          });
          
          socket.on('planet_update', (data) => {
            document.getElementById('data').innerHTML = '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
          });
          
          socket.on('disconnect', () => {
            document.getElementById('status').textContent = '✗ Disconnected';
            document.getElementById('status').style.color = '#ff0000';
          });
        </script>
      </body>
      </html>
    `)
  } else {
    res.writeHead(404)
    res.end("Not Found")
  }
})

const io = new Server(httpServer, {
  cors: { origin: "*" }
})

io.on("connection", socket => {
  console.log("client connected")
})

setInterval(() => {
  const result = tick(world)
  const packet = buildDashboard({
    world: result.world,
    signals: result.signals,
    tick: result.tick
  })

  io.emit("planet_update", packet)
}, 1000)

httpServer.listen(3000, () => {
  console.log("PANoRAMic.os live stream running on http://localhost:3000")
})
