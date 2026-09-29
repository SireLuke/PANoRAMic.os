async function fetchSignals() {
  const res = await fetch("http://localhost:3000/signals")
  return await res.json()
}

function createChart(ctx, label, color) {
  return new Chart(ctx, {
    type: "line",
    data: {
      labels: [],
      datasets: [{
        label,
        data: [],
        borderColor: color,
        backgroundColor: "rgba(0,0,0,0)",
        borderWidth: 2
      }]
    },
    options: {
      animation: false,
      scales: {
        x: { ticks: { color: "#ccc" } },
        y: { ticks: { color: "#ccc" }, min: 0, max: 1 }
      },
      plugins: {
        legend: { labels: { color: "#eee" } }
      }
    }
  })
}

const stabilityChart = createChart(
  document.getElementById("stabilityChart"),
  "Stability",
  "rgb(0,200,0)"
)

const riskChart = createChart(
  document.getElementById("riskChart"),
  "Risk",
  "rgb(200,0,0)"
)

const synthesisChart = createChart(
  document.getElementById("synthesisChart"),
  "Synthesis",
  "rgb(0,150,255)"
)

const collapseChart = createChart(
  document.getElementById("collapseChart"),
  "Collapse Pressure",
  "rgb(255,150,0)"
)

const recoveryChart = createChart(
  document.getElementById("recoveryChart"),
  "Recovery Strength",
  "rgb(0,255,255)"
)

let tickCount = 0

async function updateCharts() {
  const signals = await fetchSignals()
  tickCount++

  const charts = [
    [stabilityChart, signals.stability],
    [riskChart, signals.risk],
    [synthesisChart, signals.synthesis],
    [collapseChart, signals.collapsePressure],
    [recoveryChart, signals.recoveryStrength]
  ]

  charts.forEach(([chart, value]) => {
    chart.data.labels.push(tickCount)
    chart.data.datasets[0].data.push(value)
    chart.update()
  })
}

setInterval(updateCharts, 1000)
updateCharts()
