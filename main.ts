import { bootSystem } from "./src/boot.ts";

if (import.meta.main) {
  await bootSystem();
}
