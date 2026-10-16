/**
 * src-level boot entry. Delegates to src/boot.ts.
 *
 * bootSystem() does not return an HTTP server; library API registration
 * belongs with a real server (see api/server.ts), not this entry.
 */

export { bootSystem } from "./boot.ts";

if (import.meta.main) {
  const { bootSystem } = await import("./boot.ts");
  await bootSystem();
}
