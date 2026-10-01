/**
 * ⚠️ DEPRECATED: Use 'npm start' or 'deno run src/boot.ts'
 * 
 * This file is maintained for backward compatibility only.
 * All functionality now delegates to src/boot.ts
 */

export { bootSystem } from "./src/boot.ts";

if (import.meta.main) {
  const { bootSystem } = await import("./src/boot.ts");
  await bootSystem();
}
