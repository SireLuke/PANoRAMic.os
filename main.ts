import { bootSystem } from "./src/boot.ts";

export { bootSystem };

if (import.meta.main) {
  await bootSystem();
}
