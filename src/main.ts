import { bootSystem } from "./boot.ts";

if (import.meta.main) {
  await bootSystem();
}
