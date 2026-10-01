import { serve } from "https://deno.land/std@0.224.0/http/server.ts";
import { serveDir } from "https://deno.land/std@0.224.0/http/file_server.ts";

export async function initDashboard() {
  console.log("[DASH] Starting PlanetView server on http://localhost:3000");

  const openCommand = Deno.build.os === "windows"
    ? ["cmd", "/c", "start", "http://localhost:3000"]
    : ["xdg-open", "http://localhost:3000"];
  Deno.run({ cmd: openCommand });

  await serve((req) => {
    return serveDir(req, {
      fsRoot: "./dashboard",
      urlRoot: "",
      showDirListing: false,
      enableCors: true,
    });
  }, { port: 3000 });
}
