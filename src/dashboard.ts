import { serve } from "https://deno.land/std@0.224.0/http/server.ts";
import { serveDir } from "https://deno.land/std@0.224.0/http/file_server.ts";

// Wait until port is open before launching browser
async function waitForPort(port: number, timeout = 5000) {
  const start = Date.now();
  while (Date.now() - start < timeout) {
    try {
      const conn = await Deno.connect({ hostname: "127.0.0.1", port });
      conn.close();
      return true;
    } catch {
      await new Promise((r) => setTimeout(r, 200));
    }
  }
  return false;
}

export async function initDashboard() {
  const port = 3000;
  console.log(`[DASH] Starting PlanetView server on http://localhost:${port}`);

  // Start the server asynchronously
  const serverPromise = serve((req) => {
    return serveDir(req, {
      fsRoot: "./dashboard",
      urlRoot: "",
      showDirListing: false,
      enableCors: true,
    });
  }, { port });

  // Wait for the port to be ready
  const ready = await waitForPort(port);
  if (ready) {
    const openCommand = Deno.build.os === "windows"
      ? ["cmd", "/c", "start", `http://localhost:${port}`]
      : ["xdg-open", `http://localhost:${port}`];
    Deno.run({ cmd: openCommand });
  } else {
    console.error("[DASH] Port check timed out — browser not launched.");
  }

  await serverPromise;
}

}
