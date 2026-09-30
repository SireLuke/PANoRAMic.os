import { serveDir } from "https://deno.land/std@0.224.0/http/file_server.ts";

export async function initDashboard() {
  console.log("[DASH] Starting PlanetView server on http://localhost:3000");

  // Auto‑open browser
  const openCommand = Deno.build.os === "windows"
    ? ["cmd", "/c", "start", "http://localhost:3000"]
    : ["xdg-open", "http://localhost:3000"];
  Deno.run({ cmd: openCommand });

  // Serve the dashboard directory with correct MIME types
  await serveDir({
    fsRoot: "./dashboard",
    port: 3000,
    showDirListing: false,
    enableCors: true,
  });
}
