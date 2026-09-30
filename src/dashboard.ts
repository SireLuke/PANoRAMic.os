import { serve } from "https://deno.land/std/http/server.ts";

export async function initDashboard() {
  console.log("[DASH] Starting PlanetView server on http://localhost:3000");

  serve(async (req) => {
    return new Response(await Deno.readTextFile("./dashboard/index.html"), {
      headers: { "content-type": "text/html" },
    });
  }, { port: 3000 });
}
