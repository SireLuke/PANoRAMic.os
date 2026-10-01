/**
 * PANoRAMic.os Canonical Boot Entry Point
 * 
 * This is the single source of truth for system initialization.
 * All other entrypoints delegate to src/boot.ts
 * 
 * To start PANoRAMic.os:
 *   npm start
 *   or
 *   deno run --allow-all src/boot.ts
 */

export { bootSystem } from "./src/boot.ts";

if (import.meta.main) {
  const { bootSystem } = await import("./src/boot.ts");
  await bootSystem();
}
