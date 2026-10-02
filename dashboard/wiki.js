export async function runSearch() {
  const query = document.getElementById("searchBox").value;

  const res = await fetch("/api/library/search", {
    method: "POST",
    body: JSON.stringify({ query }),
    headers: { "Content-Type": "application/json" }
  });

  const results = await res.json();
  const container = document.getElementById("results");
  container.innerHTML = "";

  results.forEach(r => {
    const div = document.createElement("div");
    div.className = "node";
    div.innerHTML = `
      <h3>${r.title}</h3>
      <p>${r.snippet}</p>
      <p><b>Relevance:</b> ${r.relevanceScore.toFixed(2)}</p>
      <p><b>Cultural:</b> ${r.culturalAlignment.toFixed(2)}</p>
      <p><b>Nuance:</b> ${r.nuanceAlignment.toFixed(2)}</p>
    `;
    container.appendChild(div);
  });
}
