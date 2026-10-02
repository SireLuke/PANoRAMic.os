// src/api/library.ts
import { libraryOfAlexandria } from "../../core/library/libraryOfAlexandria.ts";

export function registerLibraryAPI(server: any) {
  // List all nodes
  server.get("/api/library/nodes", () => {
    return Array.from(libraryOfAlexandria.getSnapshot());
  });

  // Get a single node
  server.get("/api/library/node/:id", (req) => {
    return libraryOfAlexandria.getNode(req.params.id);
  });

  // Search
  server.post("/api/library/search", async (req) => {
    const body = await req.json();
    return libraryOfAlexandria.search(body);
  });

  // Snapshot
  server.get("/api/library/snapshot", () => {
    return libraryOfAlexandria.getSnapshot();
  });
}
