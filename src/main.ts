/**
 * Canonical boot entry point for src/main.ts
 * Delegates to src/boot.ts implementation
 */

export { bootSystem } from "./boot.ts";

if (import.meta.main) {
  const { bootSystem } = await import("./boot.ts");
  await bootSystem();
}
import { registerLibraryAPI } from "./api/library.ts";

if (import.meta.main) {
  const { bootSystem } = await import("./boot.ts");
  const server = await bootSystem();

  // Register Alexandria API routes
  registerLibraryAPI(server);
}
