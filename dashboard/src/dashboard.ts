import { serve } from "https://deno.land/std/http/server.ts";

export async function initDashboard() {
  console.log("[DASH] Starting PlanetView server on http://localhost:3000");
// Auto-open browser
const openCommand = Deno.build.os === "windows"
  ? ["cmd", "/c", "start", "http://localhost:3000"]
  : ["xdg-open", "http://localhost:3000"];

const p = Deno.run({ cmd: openCommand });

  serve(async (req) => {
    const url = new URL(req.url);

    if (url.pathname === "/") {
      return new Response(await Deno.readTextFile("./dashboard/index.html"), {
        headers: { "content-type": "text/html" },
      });
    }

    if (url.pathname === "/planet.js") {
      return new Response(await Deno.readTextFile("./dashboard/planet.js"), {
        headers: { "content-type": "application/javascript" },
      });
    }

    return new Response("Not found", { status: 404 });
  }, { port: 3000 });
}
